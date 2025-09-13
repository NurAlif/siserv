app/
  routers/
    - ai.py
    - auth.py
    - journals.py
  services/
    - ai_service.py
  - config.py
  - database.py
  - main.py
  - models.py
  - schemas.py
  - security.py



# app/routers/ai.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime

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
    Handles the conversational chat with the AI. Appends user message and AI
    response to the journal content for the specified date.
    """
    # 1. Find the user's journal for the specified date
    journal = db.query(models.Journal).filter(
        models.Journal.user_id == current_user.id,
        models.Journal.journal_date == journal_date
    ).first()

    if not journal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Journal entry for date {journal_date} not found. Please create one before chatting."
        )

    # 2. Append the user's new message to the journal content (conversation history)
    user_message_formatted = f"\n\nUser: {request.message}"
    
    # Use current content as history. If content is None, initialize it.
    conversation_history = journal.content if journal.content else ""
    journal.content = conversation_history + user_message_formatted

    # 3. Call the AI service to get a chat response
    ai_reply = ai_service.get_ai_chat_response(
        conversation_history=journal.content,
        user_message=request.message
    )

    if not ai_reply:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is currently unavailable for chat."
        )

    # 4. Append the AI's response to the journal content
    ai_response_formatted = f"\n\nLingo: {ai_reply}"
    journal.content += ai_response_formatted

    # 5. Save the updated journal to the database
    db.commit()
    db.refresh(journal)

    return {
        "ai_response": ai_reply,
        "updated_journal_content": journal.content
    }

/* end of file*/

# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, security

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Handles user registration.
    - Hashes the password.
    - Checks for existing user/email.
    - Creates a new user in the database.
    """
    # Check if a user with the same email or username already exists
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )
    
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken."
        )

    # Hash the password before storing
    hashed_password = security.get_password_hash(user.password)
    
    # Create a new user instance and save to the database
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Refresh the instance to get the new ID and created_at

    return new_user


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Handles user login.
    - Verifies username and password.
    - Returns a JWT access token on success.
    """
    # Find the user by their username (form_data.username)
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # If user doesn't exist or password doesn't match, raise an error
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the access token
    access_token = security.create_access_token(
        data={"user_id": user.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    """
    Fetches the profile for the currently logged-in user.
    Requires a valid JWT in the Authorization header.
    """
    return current_user


/* end of file*/

# app/routers/journals.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from .. import database, schemas, models, security

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
        content=journal.content
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
    journal_query.update(updated_journal.dict(), synchronize_session=False)
    db.commit()
    
    return journal_query.first()



/* end of file*/

# app/services/ai_service.py
import google.generativeai as genai
from ..config import settings
import json

# Configure the Gemini API client
genai.configure(api_key=settings.gemini_api_key)

# A detailed system prompt to guide the AI's behavior
FEEDBACK_ANALYSIS_PROMPT = """
You are an expert English language tutor AI. Your name is Lingo.
Your task is to analyze a user's journal entry and provide clear, constructive feedback.
The user is an English language learner. Your tone should be encouraging, patient, and helpful.

Analyze the provided text based on the following criteria:
1.  **Grammar:** Identify grammatical mistakes (e.g., incorrect tense, subject-verb agreement, prepositions).
2.  **Vocabulary:** Find awkward phrasing or suggest more vivid and appropriate words.
3.  **Cohesion and Flow:** Check for issues in sentence structure and logical flow.

For each issue you find, you MUST provide the following information in a structured format:
- "error_type": A short category for the error (e.g., "Grammar: Tense", "Vocabulary: Awkward Phrasing").
- "incorrect_phrase": The exact phrase from the user's text that is incorrect.
- "suggestion": The corrected version of the phrase.
- "explanation": A concise, easy-to-understand explanation of why it was incorrect and why the suggestion is better.

IMPORTANT: Your final output must be a valid JSON object that is a list of these feedback items.
Do not include any text, greetings, or explanations outside of the JSON structure.
The JSON output should be a list of objects, like this:
[
  {
    "error_type": "Grammar: Tense",
    "incorrect_phrase": "I have go to the park.",
    "suggestion": "I have gone to the park.",
    "explanation": "When using the present perfect tense with 'have', you should use the past participle form of the verb. 'Gone' is the past participle of 'go'."
  },
  {
    "error_type": "Vocabulary: Awkward Phrasing",
    "incorrect_phrase": "The weather was very nice.",
    "suggestion": "The weather was beautiful.",
    "explanation": "While 'nice' is correct, using more descriptive words like 'beautiful' or 'gorgeous' makes your writing more vivid."
  }
]
If you find no errors, return an empty list: [].
"""

def get_ai_feedback_from_text(text: str):
    """
    Sends the user's text to the Gemini API and gets structured feedback.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        # Combine the system prompt and the user's text
        full_prompt = f"{FEEDBACK_ANALYSIS_PROMPT}\n\nHere is the user's journal entry to analyze:\n\n---\n{text}\n---"
        
        response = model.generate_content(full_prompt)
        
        # Clean the response to ensure it's valid JSON
        # The model might sometimes wrap the JSON in ```json ... ```
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        # Parse the JSON string into a Python list of dictionaries
        feedback_list = json.loads(cleaned_response)
        
        return feedback_list

    except Exception as e:
        # In a real app, you'd want more robust error logging here
        print(f"An error occurred with the Gemini API: {e}")
        return None


CONVERSATIONAL_PROMPT = """
You are Lingo, a friendly and encouraging AI English tutor. 
Your role is to have a natural conversation with a user about their day to help them practice English.
Keep your responses relatively short and always end with an open-ended question to keep the conversation flowing.
Ask about their feelings, the people they met, the food they ate, or interesting things they saw.
If the user makes a small grammatical mistake, gently correct it within your response.

Example of a gentle correction:
User says: "I go to the library yesterday."
Your response: "That sounds nice! When you talk about yesterday, it's better to say 'I *went* to the library.' What did you read there?"

Here is the conversation so far. Continue it naturally.
---
{conversation_history}
---
User: {user_message}
Lingo:"""

def get_ai_chat_response(conversation_history: str, user_message: str):
    """
    Sends the conversation history and new message to the Gemini API for a conversational response.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = CONVERSATIONAL_PROMPT.format(
            conversation_history=conversation_history,
            user_message=user_message
        )
        
        response = model.generate_content(prompt)
        
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred with the Gemini API during chat: {e}")
        return None


/* end of file*/

# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manages application settings loaded from environment variables.
    """
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    gemini_api_key: str # Added for the Gemini API

    class Config:
        env_file = ".env"

# Create a single instance of the settings to be used throughout the app
settings = Settings()



/* end of file*/

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# The database URL is read from our settings instance
SQLALCHEMY_DATABASE_URL = settings.database_url

# The engine is the entry point to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our ORM models will inherit from.
Base = declarative_base()

# Dependency for API endpoints to get a DB session
def get_db():
    """
    A dependency that provides a database session for each request,
    ensuring the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



/* end of file*/

# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import auth, journals, ai

# This line creates the database tables.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS Middleware Configuration ---
# This is the crucial part to fix the frontend connection errors.
# It tells the browser that it's safe for your frontend to make requests to this backend.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, ["*"] allows all origins. For production, you should restrict this to your frontend's domain, e.g., ["https://www.lingojourn.com"].
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, etc.).
    allow_headers=["*"],  # Allows all headers (including Authorization).
)
# --- End of CORS Configuration ---


@app.get("/")
def read_root():
    return {"message": "Welcome to the LingoJourn API!"}


# Include the routers from other files
app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(ai.router)



/* end of file*/

# app/models.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime

# --- Authentication and Journaling Models ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    
    journals = relationship("Journal", back_populates="owner")
    errors = relationship("UserError", back_populates="user")

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    journal_date = Column(Date, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"), onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="journals")

# --- Learning and Progress Tracking Models ---

class LearningTopic(Base):
    __tablename__ = "learning_topics"
    id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

class UserError(Base):
    __tablename__ = "user_errors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("learning_topics.id"), nullable=False)
    incorrect_phrase = Column(Text, nullable=False)
    repetition_count = Column(Integer, default=1, nullable=False)
    status = Column(String(50), default='active', nullable=False)
    first_occurred_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    last_occurred_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    
    user = relationship("User", back_populates="errors")
    topic = relationship("LearningTopic")
    history = relationship("UserLearningHistory", back_populates="error_instance")

class LearningPoint(Base):
    __tablename__ = "learning_points"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("learning_topics.id"), nullable=False)
    explanation_text = Column(Text, nullable=False)
    suggestion_text = Column(Text, nullable=False)

class UserLearningHistory(Base):
    __tablename__ = "user_learning_history"
    id = Column(Integer, primary_key=True, index=True)
    error_id = Column(Integer, ForeignKey("user_errors.id", ondelete="CASCADE"), nullable=False)
    learning_point_id = Column(Integer, ForeignKey("learning_points.id"), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    error_instance = relationship("UserError", back_populates="history")



/* end of file*/

# app/schemas.py
# ... existing user, token, journal, and AI feedback schemas ...
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List

# --- User Schemas ---

class UserBase(BaseModel):
    """Base schema for user data, containing common fields."""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """Schema for creating a new user. Includes the password."""
    password: str

class UserOut(UserBase):
    """Schema for returning user data to the client. Excludes the password."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Token Schemas for Login ---

class Token(BaseModel):
    """Schema for the response when a user logs in successfully."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema representing the data embedded within a JWT."""
    id: Optional[str] = None

# --- Journal Schemas ---

class JournalBase(BaseModel):
    """Base schema for journal data."""
    content: str
    title: Optional[str] = None

class JournalCreate(BaseModel):
    """Schema for creating a new journal entry."""
    content: str

class JournalUpdate(BaseModel):
    """Schema for updating an existing journal entry."""
    content: str

class JournalOut(JournalBase):
    """Schema for returning journal data to the client."""
    id: int
    user_id: int
    journal_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
# --- AI Schemas ---

class AIFeedbackRequest(BaseModel):
    """Schema for the request body when asking for AI feedback."""
    text: str = Field(..., min_length=10, description="The journal text to be analyzed.")

class AIFeedbackItem(BaseModel):
    """Schema for a single piece of feedback from the AI."""
    error_type: str = Field(..., description="e.g., 'Grammar: Tense', 'Vocabulary: Phrasing'")
    incorrect_phrase: str
    suggestion: str
    explanation: str

class AIFeedbackResponse(BaseModel):
    """The overall response schema for the AI feedback endpoint."""
    feedback: List[AIFeedbackItem]

# --- AI Chat Schemas (New) ---

class AIChatRequest(BaseModel):
    """Schema for the request body when sending a chat message."""
    message: str = Field(..., min_length=1)

class AIChatResponse(BaseModel):
    """Schema for the response from the AI chat endpoint."""
    ai_response: str
    updated_journal_content: str



/* end of file*/

# app/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

from . import database, models, schemas
from .config import settings

# This tells FastAPI where the client should go to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


# --- JWT Token Handling ---
def create_access_token(data: dict):
    """
    Creates a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """
    Verifies a JWT. Decodes it and validates the user ID.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(user_id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Dependency to get the current user from a token.
    This will be used to protect endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    if user is None:
        raise credentials_exception
        
    return user



/* end of file*/
