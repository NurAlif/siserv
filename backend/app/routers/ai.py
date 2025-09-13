from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy.orm import joinedload
import json

from .. import schemas, security, models, database
from ..services import ai_service

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)

@router.post("/feedback/{journal_date}", response_model=schemas.AIFeedbackResponse)
def get_and_save_ai_feedback(
    journal_date: date,
    request: schemas.AIFeedbackRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Analyzes a journal entry's content, returns structured AI feedback,
    and saves the learning points to the database to track user progress.
    """
    # 1. Find the user's journal for the specified date
    journal = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )

    # 2. Call the AI service to get feedback
    feedback_data = ai_service.get_ai_feedback_from_text(request.text)

    if feedback_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable."
        )

    # 3. Process and save the feedback to the database
    for item in feedback_data:
        feedback_item = schemas.AIFeedbackItem(**item)
        
        # Get or create the LearningTopic
        topic = db.query(models.LearningTopic).filter(models.LearningTopic.topic_name == feedback_item.error_type).first()
        if not topic:
            topic = models.LearningTopic(topic_name=feedback_item.error_type)
            db.add(topic)
            db.commit()
            db.refresh(topic)

        # Check for existing UserError to track repetitions
        user_error = db.query(models.UserError).filter(
            models.UserError.user_id == current_user.id,
            models.UserError.topic_id == topic.id,
            models.UserError.incorrect_phrase == feedback_item.incorrect_phrase
        ).first()
        
        if user_error:
            user_error.repetition_count += 1
            user_error.last_occurred_at = datetime.utcnow()
        else:
            user_error = models.UserError(
                user_id=current_user.id,
                topic_id=topic.id,
                incorrect_phrase=feedback_item.incorrect_phrase
            )
            db.add(user_error)
        
        # We commit here to ensure user_error gets an ID for the history record
        db.commit()
        db.refresh(user_error)

        # Get or create the LearningPoint
        learning_point = db.query(models.LearningPoint).filter(
            models.LearningPoint.topic_id == topic.id,
            models.LearningPoint.explanation_text == feedback_item.explanation
        ).first()

        if not learning_point:
            learning_point = models.LearningPoint(
                topic_id=topic.id,
                explanation_text=feedback_item.explanation,
                suggestion_text=feedback_item.suggestion
            )
            db.add(learning_point)
            db.commit()
            db.refresh(learning_point)

        # Create the history link
        history_record = models.UserLearningHistory(
            error_id=user_error.id,
            learning_point_id=learning_point.id
        )
        db.add(history_record)
        db.commit()

    return {"feedback": feedback_data}


@router.post("/chat/{journal_date}", response_model=schemas.AIChatResponse)
def chat_with_ai(
    journal_date: date,
    request: schemas.AIChatRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Handles a turn in the conversation.
    1. Saves the user's message to the database.
    2. Gets a structured response from the AI (conversation + optional feedback).
    3. Saves the AI's messages to the database.
    4. Returns the AI's primary conversational message.
    """
    # 1. Find the user's journal for the specified date
    journal = db.query(models.Journal).options(joinedload(models.Journal.chat_messages)).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )

    # 2. Save the user's message
    user_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.user,
        message_text=request.message,
        message_type=models.MessageType.conversation
    )
    db.add(user_message)
    db.commit()

    # 3. Build conversation history string for the AI prompt
    history = ""
    # We refetch the journal to ensure the user_message is included
    db.refresh(journal) 
    for msg in journal.chat_messages:
        sender = "User" if msg.sender == models.MessageSender.user else "Lingo"
        history += f"{sender}: {msg.message_text}\n"

    # 4. Get structured response from the AI service
    ai_response_data = ai_service.get_ai_chat_response(history)

    if not ai_response_data:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable for chat."
        )

    # 5. Save the AI's conversational response
    ai_conversation_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.ai,
        message_text=ai_response_data.get("response_text", "I'm not sure how to respond to that."),
        message_type=models.MessageType.conversation
    )
    db.add(ai_conversation_message)
    db.commit()
    db.refresh(ai_conversation_message) # Refresh to get ID and timestamp

    # 6. If feedback was provided, save it as a separate message
    if ai_response_data.get("response_type") == "feedback" and ai_response_data.get("feedback"):
        feedback_message = models.ChatMessage(
            journal_id=journal.id,
            sender=models.MessageSender.ai,
            message_text=json.dumps(ai_response_data["feedback"]),
            message_type=models.MessageType.feedback
        )
        db.add(feedback_message)
        db.commit()

    return {"ai_message": ai_conversation_message}
