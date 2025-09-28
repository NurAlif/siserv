from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy.orm import joinedload
import json
import aiofiles

from .. import schemas, security, models, database
from ..services import ai_service

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)

# Define the chat turn limit as a constant
MAX_CHAT_TURNS = 40

@router.post("/feedback/{journal_date}", response_model=schemas.AIFeedbackResponse)
def get_and_save_ai_feedback(
    journal_date: date,
    request: schemas.AIFeedbackRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Analyzes a journal entry's content for the 'evaluation' phase, returns structured AI feedback,
    and saves any learning points derived from the feedback to the database.
    """
    journal = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )

    feedback_data = ai_service.get_evaluation_feedback(request.text)

    if not feedback_data or "feedback_items" not in feedback_data:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable or returned invalid data."
        )

    # Save learning points logic
    for item_data in feedback_data["feedback_items"]:
        item = schemas.AIFeedbackItem(**item_data)
        topic = db.query(models.LearningTopic).filter(models.LearningTopic.topic_name == item.category).first()
        if not topic:
            topic = models.LearningTopic(topic_name=item.category)
            db.add(topic)
            db.commit()
            db.refresh(topic)

        user_error = db.query(models.UserError).filter(
            models.UserError.user_id == current_user.id,
            models.UserError.topic_id == topic.id,
            models.UserError.incorrect_phrase == item.incorrect_phrase
        ).first()
        
        if user_error:
            user_error.repetition_count += 1
            user_error.last_occurred_at = datetime.utcnow()
        else:
            user_error = models.UserError(
                user_id=current_user.id,
                topic_id=topic.id,
                incorrect_phrase=item.incorrect_phrase
            )
            db.add(user_error)
        db.commit()
        db.refresh(user_error)

        learning_point = db.query(models.LearningPoint).filter(
            models.LearningPoint.topic_id == topic.id,
            models.LearningPoint.explanation_text == item.explanation
        ).first()

        if not learning_point:
            learning_point = models.LearningPoint(
                topic_id=topic.id,
                explanation_text=item.explanation,
                suggestion_text=item.suggestion
            )
            db.add(learning_point)
            db.commit()
            db.refresh(learning_point)

        history_record = models.UserLearningHistory(
            error_id=user_error.id,
            learning_point_id=learning_point.id
        )
        db.add(history_record)
        db.commit()

    return feedback_data

@router.post("/chat/{journal_date}", response_model=schemas.JournalOut)
async def chat_with_ai(
    journal_date: date,
    request: schemas.AIChatRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Handles a real-time conversation turn with the AI, including image captions.
    Optionally provides a quick correction if requested.
    Returns the entire updated journal object to prevent race conditions.
    """
    journal = db.query(models.Journal).options(
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image), # Eager load image data
        joinedload(models.Journal.owner).joinedload(models.User.context_profile)
    ).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )

    conversation_messages_count = sum(1 for msg in journal.chat_messages if msg.message_type == models.MessageType.conversation)
    if conversation_messages_count >= MAX_CHAT_TURNS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chat turn limit has been reached for this journal entry."
        )

    # 1. Prepare user's message and handle image captioning logic
    user_message_params = {
        "journal_id": journal.id,
        "sender": models.MessageSender.user,
        "message_text": request.message,
    }

    image_for_context = None
    image_bytes_for_api = None # Variable to hold image data for AI
    
    if request.image_id:
        image = db.query(models.JournalImage).filter(
            models.JournalImage.id == request.image_id, 
            models.JournalImage.journal_id == journal.id
        ).first()
        
        if image:
            image.user_caption = request.message
            user_message_params["image_id"] = request.image_id
            user_message_params["message_type"] = models.MessageType.image
            image_for_context = image
            
            # Read image file bytes to pass to the AI
            full_file_path = "app" + image.file_path
            try:
                async with aiofiles.open(full_file_path, 'rb') as f:
                    image_bytes_for_api = await f.read()
            except FileNotFoundError:
                print(f"ERROR: Image file not found at {full_file_path}")
                image_bytes_for_api = None
        else:
            user_message_params["message_type"] = models.MessageType.conversation
    else:
        user_message_params["message_type"] = models.MessageType.conversation

    user_message = models.ChatMessage(**user_message_params)
    db.add(user_message)

    # 2. Build rich chat history for the AI prompt
    temp_chat_history = []
    for msg in journal.chat_messages:
        content = f"{msg.sender.name}: {msg.message_text}"
        if msg.message_type == models.MessageType.image and msg.image and msg.image.ai_description:
             content += f" (related to image: {msg.image.ai_description})"
        temp_chat_history.append(content)
    
    temp_chat_history.append(f"user: {request.message}")

    # 3. Get AI responses
    ai_message_text = "I'm not sure how to respond to that."
    if journal.writing_phase == models.JournalPhase.scaffolding:
        session_state = {
            "current_outline": journal.outline_content,
            "chat_history": "\n".join(temp_chat_history),
        }
        if image_for_context:
            session_state["image_description"] = image_for_context.ai_description
            session_state["user_caption"] = image_for_context.user_caption

        user_context = journal.owner.context_profile.profile_data if journal.owner.context_profile and journal.owner.context_profile.profile_data else {}
        
        ai_response = ai_service.get_scaffolding_response(user_context, session_state, image_bytes=image_bytes_for_api)

        action = ai_response.get("action")
        payload = ai_response.get("payload", {})

        if action == "ADD_TO_OUTLINE":
            journal.outline_content = (journal.outline_content or "") + payload.get("text_to_add", "")
            ai_message_text = payload.get("follow_up_question", "I've added that. What's next?")
        else:
            ai_message_text = payload.get("question", "What would you like to discuss?")

    elif journal.writing_phase == models.JournalPhase.writing:
        ai_message_text = ai_service.get_writing_partner_response(
            user_message=request.message, outline=journal.outline_content, current_draft=journal.content
        )
    
    if request.enable_correction:
        correction_data = ai_service.get_quick_correction(request.message)
        if (correction_data and 'incorrect_phrase' in correction_data and correction_data.get('incorrect_phrase')):
            feedback_payload = correction_data
        else:
            feedback_payload = {"status": "no_errors"}

        feedback_message = models.ChatMessage(
            journal_id=journal.id, sender=models.MessageSender.ai,
            message_text=json.dumps(feedback_payload), message_type=models.MessageType.feedback
        )
        db.add(feedback_message)

    ai_conv_message = models.ChatMessage(
        journal_id=journal.id, sender=models.MessageSender.ai,
        message_text=ai_message_text, message_type=models.MessageType.conversation
    )
    db.add(ai_conv_message)

    # 4. Commit all changes and re-fetch the journal to ensure all relationships are loaded for the response
    db.commit()
    
    refreshed_journal = db.query(models.Journal).options(
        joinedload(models.Journal.images),
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image)
    ).filter(models.Journal.id == journal.id).first()

    return refreshed_journal

