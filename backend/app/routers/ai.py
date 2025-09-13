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
    This is primarily used for the 'finishing' phase.
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

    feedback_data = ai_service.get_ai_feedback_from_text(request.text)

    if feedback_data is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable."
        )

    # ... (rest of the database saving logic remains the same)
    for item in feedback_data:
        feedback_item = schemas.AIFeedbackItem(**item)
        topic = db.query(models.LearningTopic).filter(models.LearningTopic.topic_name == feedback_item.error_type).first()
        if not topic:
            topic = models.LearningTopic(topic_name=feedback_item.error_type)
            db.add(topic)
            db.commit()
            db.refresh(topic)

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
        
        db.commit()
        db.refresh(user_error)

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
    Handles a conversation turn, using a different AI personality based on the journal's current phase.
    """
    journal = db.query(models.Journal).options(joinedload(models.Journal.chat_messages)).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )
        
    # --- MODIFIED LOGIC ---
    # 1. Save the user's message (same as before)
    user_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.user,
        message_text=request.message,
        message_type=models.MessageType.conversation
    )
    db.add(user_message)
    db.commit()

    # 2. Build conversation history (same as before)
    history = ""
    db.refresh(journal) 
    for msg in journal.chat_messages:
        sender = "User" if msg.sender == models.MessageSender.user else "Lingo"
        history += f"{sender}: {msg.message_text}\n"

    # 3. Get AI response, PASSING IN THE CURRENT PHASE
    ai_response_data = ai_service.get_ai_chat_response(history, journal.writing_phase.value)

    if not ai_response_data:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable for chat."
        )

    # 4. Save AI's conversational response (same as before)
    ai_conversation_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.ai,
        message_text=ai_response_data.get("response_text", "I'm not sure how to respond to that."),
        message_type=models.MessageType.conversation
    )
    db.add(ai_conversation_message)
    db.commit()
    db.refresh(ai_conversation_message)

    # 5. Handle and save feedback if provided (same as before, though scaffolding prompt won't provide it)
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
