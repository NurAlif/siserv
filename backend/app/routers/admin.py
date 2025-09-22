from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, Date as SQLDate
from typing import List
from datetime import date, timedelta

from .. import database, schemas, models, security

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(security.get_current_admin_user)]
)

@router.get("/students", response_model=List[schemas.AdminStudentSummary])
def get_all_students(db: Session = Depends(database.get_db)):
    """
    Retrieves a list of all non-admin users (students) with summary stats.
    """
    students_query = db.query(
        models.User,
        func.count(models.Journal.id).label("journal_count"),
        func.max(models.Journal.updated_at).label("last_active")
    ).outerjoin(models.Journal, models.User.id == models.Journal.user_id)\
    .filter(models.User.is_admin == False)\
    .group_by(models.User.id).all()

    results = []
    for user, journal_count, last_active in students_query:
        total_errors = db.query(func.count(models.UserError.id)).filter(models.UserError.user_id == user.id).scalar()
        
        student_summary = schemas.AdminStudentSummary(
            id=user.id,
            username=user.username,
            email=user.email,
            # --- MODIFIED SECTION START ---
            realname=user.realname,
            student_id=user.student_id,
            group=user.group,
            # --- MODIFIED SECTION END ---
            created_at=user.created_at,
            is_admin=user.is_admin,
            journal_count=journal_count,
            total_errors=total_errors or 0,
            last_active=last_active
        )
        results.append(student_summary)
        
    return results

@router.get("/students/{student_id}", response_model=schemas.AdminStudentDetail)
def get_student_details(student_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieves detailed analytics for a specific student.
    """
    student = db.query(models.User).filter(models.User.id == student_id, models.User.is_admin == False).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Base summary stats
    journal_count = db.query(func.count(models.Journal.id)).filter(models.Journal.user_id == student_id).scalar()
    total_errors = db.query(func.count(models.UserError.id)).filter(models.UserError.user_id == student_id).scalar()
    last_active = db.query(func.max(models.Journal.updated_at)).filter(models.Journal.user_id == student_id).scalar()

    # Error distribution by topic
    error_distribution_query = db.query(
        models.LearningTopic.topic_name,
        func.count(models.UserError.id).label("error_count")
    ).join(models.LearningTopic, models.UserError.topic_id == models.LearningTopic.id)\
    .filter(models.UserError.user_id == student_id)\
    .group_by(models.LearningTopic.topic_name)\
    .order_by(desc("error_count")).all()
    
    # Error trend over the last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    error_trend_query = db.query(
        cast(models.UserError.last_occurred_at, SQLDate).label("date"),
        func.count(models.UserError.id).label("error_count")
    ).filter(
        models.UserError.user_id == student_id,
        models.UserError.last_occurred_at >= thirty_days_ago
    ).group_by(cast(models.UserError.last_occurred_at, SQLDate))\
    .order_by(cast(models.UserError.last_occurred_at, SQLDate)).all()

    return {
        "id": student.id,
        "username": student.username,
        "email": student.email,
        # --- MODIFIED SECTION START ---
        "realname": student.realname,
        "student_id": student.student_id,
        "group": student.group,
        # --- MODIFIED SECTION END ---
        "created_at": student.created_at,
        "is_admin": student.is_admin,
        "journal_count": journal_count,
        "total_errors": total_errors or 0,
        "last_active": last_active,
        "error_distribution": error_distribution_query,
        "error_trend": error_trend_query
    }


@router.get("/analytics/error-distribution", response_model=List[schemas.AdminErrorDistributionItem])
def get_class_error_distribution(db: Session = Depends(database.get_db)):
    """
    Gets the aggregated distribution of errors by topic for the entire class.
    """
    return db.query(
        models.LearningTopic.topic_name,
        func.count(models.UserError.id).label("error_count")
    ).join(models.LearningTopic, models.UserError.topic_id == models.LearningTopic.id)\
    .join(models.User, models.UserError.user_id == models.User.id)\
    .filter(models.User.is_admin == False)\
    .group_by(models.LearningTopic.topic_name)\
    .order_by(desc("error_count")).all()


@router.get("/analytics/error-trend", response_model=List[schemas.AdminErrorTrendPoint])
def get_class_error_trend(db: Session = Depends(database.get_db)):
    """
    Gets the trend of total errors per day for the entire class over the last 30 days.
    """
    thirty_days_ago = date.today() - timedelta(days=30)
    return db.query(
        cast(models.UserError.last_occurred_at, SQLDate).label("date"),
        func.count(models.UserError.id).label("error_count")
    ).join(models.User, models.UserError.user_id == models.User.id)\
    .filter(
        models.User.is_admin == False,
        models.UserError.last_occurred_at >= thirty_days_ago
    ).group_by(cast(models.UserError.last_occurred_at, SQLDate))\
    .order_by(cast(models.UserError.last_occurred_at, SQLDate)).all()

# NEW ENDPOINT to get all journals for a student
@router.get("/students/{student_id}/journals", response_model=List[schemas.JournalOut])
def get_student_journals(student_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieves all journal entries for a specific student.
    """
    student = db.query(models.User).filter(models.User.id == student_id, models.User.is_admin == False).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    journals = db.query(models.Journal).filter(models.Journal.user_id == student_id).order_by(models.Journal.journal_date.desc()).all()
    return journals

# NEW ENDPOINT to get a single journal for a student
@router.get("/students/{student_id}/journals/{journal_date}", response_model=schemas.JournalOut)
def get_student_journal_by_date(student_id: int, journal_date: date, db: Session = Depends(database.get_db)):
    """
    Retrieves a specific journal entry by date for a specific student.
    """
    journal = db.query(models.Journal).filter(
        models.Journal.user_id == student_id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=404,
            detail=f"Journal entry for date {journal_date} not found for student {student_id}."
        )
    
    return journal