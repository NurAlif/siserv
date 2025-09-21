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
def chat_with_ai(
    journal_date: date,
    request: schemas.AIChatRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Handles a real-time conversation turn with the AI.
    The AI's behavior and response format depend on the journal's current writing_phase.
    Returns the entire updated journal object to ensure UI reactivity.
    """
    journal = db.query(models.Journal).options(
        joinedload(models.Journal.chat_messages),
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
        
    # 1. Save user's message
    user_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.user,
        message_text=request.message,
        message_type=models.MessageType.conversation
    )
    db.add(user_message)
    db.commit()
    db.refresh(journal)

    # 2. Orchestrate AI response based on phase
    ai_message_text = "I'm not sure how to respond to that." # Default
    
    if journal.writing_phase == models.JournalPhase.scaffolding:
        chat_history = [{"role": msg.sender.name, "content": msg.message_text} for msg in journal.chat_messages]
        session_state = {
            "current_outline": journal.outline_content,
            "chat_history": chat_history,
            "topic_turn_count": journal.scaffolding_turn_count
        }
        user_context = journal.owner.context_profile.profile_data if journal.owner.context_profile and journal.owner.context_profile.profile_data else {}
        
        ai_response = ai_service.get_scaffolding_response(user_context, session_state)
        
        action = ai_response.get("action")
        payload = ai_response.get("payload", {})

        # UPDATE the journal's turn count with the new value from the AI's response
        journal.scaffolding_turn_count = payload.get("new_topic_turn_count", 0)

        if action == "ADD_TO_OUTLINE":
            journal.outline_content = (journal.outline_content or "") + payload.get("text_to_add", "")
            ai_message_text = payload.get("follow_up_question", "I've added that. What's next?")
        elif action in ["PROBE_TOPIC", "SUGGEST_BRANCH", "ASK_GENERAL_QUESTION", "ASK_QUESTION"]:
            ai_message_text = payload.get("question", "What would you like to discuss?")

    elif journal.writing_phase == models.JournalPhase.writing:
        ai_message_text = ai_service.get_writing_partner_response(
            user_message=request.message,
            outline=journal.outline_content,
            current_draft=journal.content
        )

    # 3. Save AI's response message
    ai_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.ai,
        message_text=ai_message_text,
        message_type=models.MessageType.conversation
    )
    db.add(ai_message)
    db.commit()
    db.refresh(journal)

    return journal
