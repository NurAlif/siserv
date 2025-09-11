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

