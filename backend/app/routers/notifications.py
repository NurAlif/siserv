from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import database, schemas, models, security

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)

# --- Admin Endpoints ---

@router.post("/", response_model=schemas.NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification(
    notification_data: schemas.NotificationCreate,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(security.get_current_admin_user)
):
    """
    [ADMIN] Creates a new notification (announcement or survey).
    It is unpublished by default.
    """
    new_notification = models.Notification(
        title=notification_data.title,
        content=notification_data.content,
        notification_type=notification_data.notification_type,
        is_published=False
    )
    db.add(new_notification)
    db.flush() # Flush to get the new_notification.id

    if notification_data.notification_type == models.NotificationType.survey:
        for q_data in notification_data.questions:
            new_question = models.SurveyQuestion(
                notification_id=new_notification.id,
                question_text=q_data.question_text,
                question_type=q_data.question_type
            )
            db.add(new_question)
            db.flush() # Flush to get new_question.id

            if q_data.options:
                for o_data in q_data.options:
                    new_option = models.SurveyOption(
                        question_id=new_question.id,
                        option_text=o_data.option_text
                    )
                    db.add(new_option)

    db.commit()
    db.refresh(new_notification)
    return new_notification

@router.get("/", response_model=List[schemas.NotificationOut])
def get_all_notifications(
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(security.get_current_admin_user)
):
    """
    [ADMIN] Retrieves all notifications created.
    """
    notifications = db.query(models.Notification).options(
        joinedload(models.Notification.questions).joinedload(models.SurveyQuestion.options)
    ).order_by(models.Notification.created_at.desc()).all()
    return notifications

@router.post("/{notification_id}/publish", response_model=schemas.NotificationOut)
def publish_notification(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(security.get_current_admin_user)
):
    """
    [ADMIN] Publishes a notification, making it visible to all users.
    """
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if notification.is_published:
        raise HTTPException(status_code=400, detail="Notification is already published")

    notification.is_published = True
    
    db.commit()
    db.refresh(notification)
    return notification


@router.get("/{notification_id}/results", response_model=List[schemas.SurveyResultOut])
def get_survey_results(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(security.get_current_admin_user)
):
    """
    [ADMIN] Retrieves the results for a specific survey.
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.notification_type == models.NotificationType.survey
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Survey not found")

    results = []
    for question in notification.questions:
        # Eager load related user and selected option data for efficiency
        responses = db.query(models.SurveyResponse).options(
            joinedload(models.SurveyResponse.user),
            joinedload(models.SurveyResponse.selected_option)
        ).filter(models.SurveyResponse.question_id == question.id).all()
        
        results.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "responses": responses
        })
        
    return results

# --- User Endpoints ---

@router.get("/active", response_model=List[schemas.NotificationOut])
def get_active_notifications_for_user(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    [USER] Retrieves all active, published notifications that the user has not yet interacted with.
    """
    # Subquery to get the notification IDs the user has already seen or completed
    subquery = db.query(models.UserNotificationStatus.notification_id).filter(
        models.UserNotificationStatus.user_id == current_user.id
    )

    # Main query to find all published notifications that are NOT in the subquery list, ordered by newest first
    active_notifications = db.query(models.Notification).options(
        joinedload(models.Notification.questions).joinedload(models.SurveyQuestion.options)
    ).filter(
        models.Notification.is_published == True,
        ~models.Notification.id.in_(subquery)
    ).order_by(models.Notification.created_at.desc()).all()
            
    return active_notifications


@router.post("/seen/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def mark_announcement_as_seen(
    notification_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    [USER] Marks an announcement-type notification as seen by creating a status entry.
    """
    notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notification or not notification.is_published:
        raise HTTPException(status_code=404, detail="Published notification not found.")
        
    if notification.notification_type != models.NotificationType.announcement:
        raise HTTPException(status_code=400, detail="This endpoint is only for announcements.")

    status_exists = db.query(models.UserNotificationStatus).filter(
        models.UserNotificationStatus.user_id == current_user.id,
        models.UserNotificationStatus.notification_id == notification_id
    ).first()

    if not status_exists:
        new_status = models.UserNotificationStatus(
            user_id=current_user.id,
            notification_id=notification_id,
            is_seen=True,
            is_completed=True # For announcements, seen and completed are the same
        )
        db.add(new_status)
        db.commit()
        
    return


@router.post("/responses", status_code=status.HTTP_204_NO_CONTENT)
def submit_survey_responses(
    survey_data: schemas.SurveyResponseCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    [USER] Submits responses for a survey and marks it as completed.
    """
    notification = db.query(models.Notification).filter(models.Notification.id == survey_data.notification_id).first()
    if not notification or not notification.is_published:
         raise HTTPException(status_code=404, detail="Published survey not found.")

    if notification.notification_type != models.NotificationType.survey:
        raise HTTPException(status_code=400, detail="This notification is not a survey.")

    status_exists = db.query(models.UserNotificationStatus).filter(
        models.UserNotificationStatus.user_id == current_user.id,
        models.UserNotificationStatus.notification_id == survey_data.notification_id
    ).first()

    if status_exists:
        raise HTTPException(status_code=400, detail="Survey has already been submitted.")

    for response_in in survey_data.responses:
        # Add validation here to ensure question_id belongs to the notification, etc.
        if response_in.text_response:
            new_response = models.SurveyResponse(
                user_id=current_user.id,
                question_id=response_in.question_id,
                text_response=response_in.text_response
            )
            db.add(new_response)
        elif response_in.selected_option_ids:
            for option_id in response_in.selected_option_ids:
                new_response = models.SurveyResponse(
                    user_id=current_user.id,
                    question_id=response_in.question_id,
                    selected_option_id=option_id
                )
                db.add(new_response)
    
    # Create the status entry to mark it as done
    new_status = models.UserNotificationStatus(
        user_id=current_user.id,
        notification_id=survey_data.notification_id,
        is_seen=True,
        is_completed=True
    )
    db.add(new_status)

    db.commit()
    return

@router.get("/history", response_model=List[schemas.UserNotificationStatusOut])
def get_notification_history_for_user(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    [USER] Retrieves all published notifications, along with the user's status for each.
    """
    results = db.query(
        models.Notification,
        models.UserNotificationStatus
    ).outerjoin(
        models.UserNotificationStatus,
        (models.Notification.id == models.UserNotificationStatus.notification_id) &
        (models.UserNotificationStatus.user_id == current_user.id)
    ).filter(models.Notification.is_published == True)\
    .options(
        joinedload(models.Notification.questions).joinedload(models.SurveyQuestion.options)
    ).order_by(models.Notification.created_at.desc()).all()

    return [
        {
            "notification": notif,
            "is_seen": status.is_seen if status else False,
            "is_completed": status.is_completed if status else False
        }
        for notif, status in results
    ]

