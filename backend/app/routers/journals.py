from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from datetime import date
from typing import List
import os
import uuid
import aiofiles


from .. import database, schemas, models, security
from ..services import context_agent, ai_service

router = APIRouter(
    prefix="/api/journals",
    tags=["Journals"]
)

# Directory for storing user-uploaded images
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
    journal = db.query(models.Journal).options(
        joinedload(models.Journal.images),
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image)
    ).filter(
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
    journal_query = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    )
    journal = journal_query.first()

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
    # After commit, refetch with relations for the response
    updated_journal_response = journal_query.options(
        joinedload(models.Journal.images),
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image)
    ).first()
    
    return updated_journal_response

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
    journal_query = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    )
    journal = journal_query.first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found."
        )

    journal.writing_phase = updated_phase.phase 
    db.commit()

    if journal.writing_phase == models.JournalPhase.completed:
        background_tasks.add_task(
            context_agent.process_journal, journal.id, current_user.id
        )

    # After commit, refetch with relations for the response
    updated_journal_response = journal_query.options(
        joinedload(models.Journal.images),
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image)
    ).first()

    return updated_journal_response

@router.post("/{journal_date}/images", response_model=schemas.JournalOut)
async def upload_journal_image(
    journal_date: date,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Uploads an image for a specific journal entry and generates an AI description.
    This endpoint no longer creates a chat message directly.
    """
    journal = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(status_code=404, detail="Journal entry not found.")
    
    if journal.writing_phase != models.JournalPhase.scaffolding:
        raise HTTPException(status_code=400, detail="Images can only be added during the scaffolding phase.")

    # 1. Save the file
    safe_filename = file.filename.replace("..", "").replace("/", "")
    filename = f"{uuid.uuid4()}-{safe_filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    image_bytes = await file.read()
    async with aiofiles.open(file_path, 'wb') as out_file:
        await out_file.write(image_bytes)
    
    # 2. Get AI description
    description = ai_service.get_image_description(image_bytes)
    
    # 3. Save to DB
    db_image = models.JournalImage(
        journal_id=journal.id,
        file_path=f"/static/uploads/{filename}", # URL path for frontend
        ai_description=description
    )
    db.add(db_image)
    db.commit()
    
    # 4. Return the updated journal object
    updated_journal = db.query(models.Journal).options(
        joinedload(models.Journal.images),
        joinedload(models.Journal.chat_messages).joinedload(models.ChatMessage.image)
    ).filter(models.Journal.id == journal.id).first()
    
    return updated_journal
