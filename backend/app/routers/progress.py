from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from sqlalchemy.orm import joinedload
from datetime import date, timedelta

from .. import database, schemas, models, security

router = APIRouter(
    prefix="/api/progress",
    tags=["Progress"]
)

@router.get("/summary", response_model=schemas.ProgressSummary)
def get_progress_summary(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves a high-level summary of the user's learning progress,
    including total errors and top 3 most common error topics.
    """
    user_id = current_user.id

    # 1. Calculate total errors
    total_errors = db.query(models.UserError).filter(models.UserError.user_id == user_id).count()

    # 2. Calculate total unique topics encountered
    topics_encountered = db.query(func.count(func.distinct(models.UserError.topic_id))).filter(models.UserError.user_id == user_id).scalar() or 0

    # 3. Find the top 3 topics with the most errors
    # We join UserError with LearningTopic, group by topic,
    # count the errors in each group, and take the top 3.
    top_topics_query = db.query(
        models.LearningTopic.topic_name,
        func.count(models.UserError.id).label("error_count")
    ).join(
        models.LearningTopic, models.UserError.topic_id == models.LearningTopic.id
    ).filter(
        models.UserError.user_id == user_id
    ).group_by(
        models.LearningTopic.topic_name
    ).order_by(
        desc("error_count")
    ).limit(3).all()

    # Format the result to match the Pydantic schema
    top_topics = [schemas.TopTopic(topic_name=name, error_count=count) for name, count in top_topics_query]
    
    return {
        "total_errors": total_errors,
        "topics_encountered": topics_encountered,
        "top_topics": top_topics
    }

# --- New Endpoint 1: Get All Topics ---
@router.get("/topics", response_model=List[schemas.UserTopic])
def get_user_topics(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves all learning topics a user has encountered, along with the
    count of unique errors for each topic.
    """
    user_id = current_user.id

    topics_query = db.query(
        models.LearningTopic.id.label("topic_id"),
        models.LearningTopic.topic_name,
        func.count(models.UserError.id).label("error_count")
    ).join(
        models.LearningTopic, models.UserError.topic_id == models.LearningTopic.id
    ).filter(
        models.UserError.user_id == user_id
    ).group_by(
        models.LearningTopic.id, models.LearningTopic.topic_name
    ).order_by(
        desc("error_count")
    ).all()

    return topics_query


# --- New Endpoint 2: Get Topic Details ---
@router.get("/topics/{topic_id}", response_model=schemas.UserTopicDetails)
def get_topic_details(
    topic_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves detailed information for a specific topic, including all
    associated errors and their corresponding learning points (explanations).
    """
    user_id = current_user.id

    # 1. Get the topic info and error count first
    topic_info = db.query(
        models.LearningTopic.id.label("topic_id"),
        models.LearningTopic.topic_name,
        func.count(models.UserError.id).label("error_count")
    ).join(
        models.LearningTopic, models.UserError.topic_id == models.LearningTopic.id
    ).filter(
        models.UserError.user_id == user_id,
        models.LearningTopic.id == topic_id
    ).group_by(
        models.LearningTopic.id, models.LearningTopic.topic_name
    ).first()

    if not topic_info:
        raise HTTPException(status_code=404, detail="Topic not found for this user.")

    # 2. Get all errors for this topic, joining with history and learning points
    # to fetch the explanation and suggestion for each error.
    errors_query = db.query(
        models.UserError.incorrect_phrase,
        models.LearningPoint.suggestion_text,
        models.LearningPoint.explanation_text,
        models.UserError.repetition_count,
        models.UserError.last_occurred_at
    ).select_from(models.UserError).join(
        models.UserLearningHistory, models.UserError.id == models.UserLearningHistory.error_id
    ).join(
        models.LearningPoint, models.UserLearningHistory.learning_point_id == models.LearningPoint.id
    ).filter(
        models.UserError.user_id == user_id,
        models.UserError.topic_id == topic_id
    ).distinct().all()
    
    return {
        "topic_id": topic_info.topic_id,
        "topic_name": topic_info.topic_name,
        "error_count": topic_info.error_count,
        "errors": errors_query
    }

@router.get("/streak", response_model=schemas.StreakOut)
def get_user_streak(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Calculates the user's current writing streak based on consecutive daily
    journal entries.
    """
    # 1. Fetch all unique journal dates for the user, sorted from newest to oldest.
    journal_dates_query = db.query(models.Journal.journal_date).filter(
        models.Journal.user_id == current_user.id
    ).distinct().order_by(models.Journal.journal_date.desc()).all()
    
    # Extract date objects from the query result
    journal_dates = [item.journal_date for item in journal_dates_query]

    if not journal_dates:
        return {"streak_count": 0}

    # 2. Check if the streak is active.
    today = date.today()
    most_recent_date = journal_dates[0]
    
    # If the most recent entry is older than yesterday, the streak is broken.
    if most_recent_date < today - timedelta(days=1):
        return {"streak_count": 0}

    # 3. Calculate the streak length.
    streak_count = 1
    last_date = most_recent_date

    # Iterate through the rest of the dates to find consecutive days.
    for i in range(1, len(journal_dates)):
        current_date = journal_dates[i]
        # If the gap between the last date and the current date is exactly one day,
        # it's a consecutive entry.
        if last_date - current_date == timedelta(days=1):
            streak_count += 1
            last_date = current_date
        else:
            # If the chain is broken, stop counting.
            break
            
    return {"streak_count": streak_count}