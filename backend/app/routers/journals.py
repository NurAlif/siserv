from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from .. import database, schemas, models, security
from ..services import context_agent

router = APIRouter(
    prefix="/api/journals",
    tags=["Journals"]
)

@router.post("/", response_model=schemas.JournalOut, status_code=status.HTTP_201_CREATED)
def create_journal(
    journal: schemas.JournalCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Creates a new journal entry for the current user for today's date.
    A user can only create one journal entry per day.
    """
    today = date.today()
    
    # Check if a journal entry for today already exists for this user
    existing_journal = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == today
    ).first()

    if existing_journal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A journal entry for today already exists."
        )

    # Create the new journal entry
    new_journal = models.Journal(
        user_id=current_user.id,
        journal_date=today,
        content=journal.content or "",
        outline_content = "" # Ensure it's not null
    )
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    
    return new_journal

@router.get("/", response_model=List[schemas.JournalOut])
def get_all_journals(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves all journal entries for the currently logged-in user.
    """
    journals = db.query(models.Journal).filter(models.Journal.user_id == current_user.id).order_by(models.Journal.journal_date.desc()).all()
    return journals

@router.get("/{journal_date}", response_model=schemas.JournalOut)
def get_journal_by_date(
    journal_date: date,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Retrieves a specific journal entry by date for the current user.
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
    
    return journal

@router.put("/{journal_date}", response_model=schemas.JournalOut)
def update_journal(
    journal_date: date,
    updated_journal: schemas.JournalUpdate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Updates the content of a specific journal entry by date for the current user.
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
    
    # Update the journal content
    journal.content = updated_journal.content
    if updated_journal.outline_content is not None:
        journal.outline_content = updated_journal.outline_content

    db.commit()
    db.refresh(journal)
    
    return journal

@router.put("/{journal_date}/phase", response_model=schemas.JournalOut)
def update_journal_phase(
    journal_date: date,
    updated_phase: schemas.JournalPhaseUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Updates the writing phase of a specific journal entry.
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

    # --- FIX STARTS HERE ---

    # 1. Add this line to update the phase from the request
    journal.writing_phase = updated_phase.phase 

    # 2. Add this line to save the change to the database
    db.commit()

    # --- FIX ENDS HERE ---

    # This part handles kicking off background tasks after a journal is completed
    if journal.writing_phase == models.JournalPhase.completed:
        background_tasks.add_task(
            context_agent.process_journal, journal.id, current_user.id
        )

    db.refresh(journal)

    return journal

