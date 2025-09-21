from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, List
import enum

# --- Import the new Enums from models ---
from .models import MessageSender, MessageType

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

# --- NEW ChatMessage Schemas ---
class ChatMessageBase(BaseModel):
    sender: MessageSender
    message_text: str
    message_type: MessageType

class ChatMessageOut(ChatMessageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# --- Journal Schemas ---

class JournalBase(BaseModel):
    """Base schema for journal data."""
    title: Optional[str] = None
    outline_content: Optional[str] = None
    content: Optional[str] = None

class JournalCreate(BaseModel):
    """Schema for creating a new journal entry."""
    content: str

class JournalUpdate(BaseModel):
    content: str
    outline_content: Optional[str] = None

class JournalPhase(str, enum.Enum):
    scaffolding = "scaffolding"
    writing = "writing"
    evaluation = "evaluation" # Changed from finishing
    completed = "completed"

class JournalPhaseUpdate(BaseModel):
    phase: JournalPhase


class JournalOut(JournalBase):
    """Schema for returning journal data to the client."""
    id: int
    user_id: int
    journal_date: date
    outline_content: Optional[str] = None
    writing_phase: JournalPhase
    created_at: datetime
    updated_at: datetime
    chat_messages: List[ChatMessageOut] = []
    
    class Config:
        from_attributes = True
        
# --- AI Schemas ---

class AIFeedbackRequest(BaseModel):
    """Schema for the request body when asking for AI feedback."""
    text: str = Field(..., min_length=10, description="The journal text to be analyzed.")

class AIFeedbackItem(BaseModel):
    """Schema for a single piece of feedback from the AI."""
    category: str = Field(..., description="e.g., 'Grammar: Tense', 'Vocabulary: Phrasing'")
    incorrect_phrase: str
    suggestion: str
    explanation: str

class AIFeedbackResponse(BaseModel):
    """The overall response schema for the AI feedback endpoint."""
    high_level_summary: str
    feedback_items: List[AIFeedbackItem]

class AIConceptualFeedbackResponse(BaseModel):
    """Schema for high-level conceptual feedback."""
    feedback_text: str

# --- AI Chat Schemas (New) ---

class AIChatRequest(BaseModel):
    """Schema for the request body when sending a chat message."""
    message: str = Field(..., min_length=1)

class AIChatResponse(BaseModel):
    """Schema for the response from the AI chat endpoint."""
    ai_message: ChatMessageOut

# --- Progress Tracking Schemas ---
class TopTopic(BaseModel):
    """Schema for representing a user's most frequent learning topics."""
    topic_name: str
    error_count: int

    class Config:
        from_attributes = True

class ProgressSummary(BaseModel):
    """Schema for the response of the progress summary endpoint."""
    total_errors: int
    topics_encountered: int
    top_topics: List[TopTopic]

class StreakOut(BaseModel):
    """Schema for returning the user's current streak."""
    streak_count: int

# --- New Schemas for Learning Hub ---

class TopicDetail(BaseModel):
    """Schema for a single error instance within a topic."""
    incorrect_phrase: str
    suggestion_text: str
    explanation_text: str
    repetition_count: int
    last_occurred_at: datetime

    class Config:
        from_attributes = True

class UserTopic(BaseModel):
    """Schema for a topic the user has encountered."""
    topic_id: int
    topic_name: str
    error_count: int

    class Config:
        from_attributes = True

class UserTopicDetails(UserTopic):
    """Extends UserTopic to include the full list of errors."""
    errors: List[TopicDetail]
