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
        # We commit here to ensure user_error gets an ID for the history record
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


@router.post("/conceptual-feedback/{journal_date}", response_model=schemas.AIConceptualFeedbackResponse)
def get_conceptual_feedback(
    journal_date: date,
    request: schemas.AIFeedbackRequest,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Analyzes a journal entry's content for high-level conceptual feedback
    without saving any learning points.
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

    feedback_text = ai_service.get_ai_conceptual_feedback(request.text)

    if feedback_text is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service for conceptual feedback is currently unavailable."
        )

    return {"feedback_text": feedback_text}


@router.post("/chat/{journal_date}", response_model=schemas.AIChatResponse)
def chat_with_ai(
    journal_date: date,
    request: schemas.AIChatRequest, # We might want a new schema to accept outline_content from frontend
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Handles a conversation turn, using a different AI personality based on the journal's current phase.
    Gathers additional context like the current outline and previous entries to provide a more informed response.
    The AI can now perform actions like updating the journal's outline directly.
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
        
    # 1. Save the user's message
    user_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.user,
        message_text=request.message,
        message_type=models.MessageType.conversation
    )
    db.add(user_message)
    db.commit()

    # 2. Build conversation history
    history = ""
    db.refresh(journal) 
    for msg in journal.chat_messages:
        sender = "User" if msg.sender == models.MessageSender.user else "Lingo"
        history += f"{sender}: {msg.message_text}\n"

    # 3. (NEW) Gather additional context for the AI
    current_outline = journal.outline_content
    # This is a simplified summary. A more robust implementation could use another AI call
    # to summarize the last 3 journal entries.
    previous_journals = db.query(models.Journal.content).filter(
        models.Journal.user_id == current_user.id, 
        models.Journal.journal_date < journal_date
    ).order_by(models.Journal.journal_date.desc()).limit(3).all()
    previous_journal_summary = " ".join([j.content for j in previous_journals if j.content])
    
    # 4. Get structured response from the AI service
    ai_response_data = ai_service.get_ai_chat_response(
        history, 
        journal.writing_phase.value,
        current_outline,
        previous_journal_summary
    )

    if not ai_response_data:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable for chat."
        )

    # 5. (MODIFIED) Process the AI's response based on its action
    action = ai_response_data.get("action")
    payload = ai_response_data.get("payload", {})
    
    ai_message_text = "I'm not sure how to respond." # Default text

    if action == "ASK_QUESTION":
        ai_message_text = payload.get("question", ai_message_text)

    elif action == "SUGGEST_TOPICS":
        # Format the topics into a readable string for the chat history
        topics_str = "\\n".join([f"- {topic}" for topic in payload.get("topics", [])])
        ai_message_text = f"{payload.get('intro_text', 'What about these?')}\\n{topics_str}"

    elif action == "ADD_TO_OUTLINE":
        text_to_add = payload.get("text_to_add")
        if text_to_add:
            # IMPORTANT: The agent directly modifies the journal's outline
            journal.outline_content = (journal.outline_content or "") + text_to_add
            db.commit()
        ai_message_text = payload.get("follow_up_question", "I've added that. What's next?")

    # 6. Save the AI's conversational response to chat history
    ai_conversation_message = models.ChatMessage(
        journal_id=journal.id,
        sender=models.MessageSender.ai,
        message_text=ai_message_text,
        message_type=models.MessageType.conversation
    )
    db.add(ai_conversation_message)
    db.commit()
    db.refresh(ai_conversation_message)
    
    # The frontend will fetch the updated journal, including the new outline content
    return {"ai_message": ai_conversation_message}
