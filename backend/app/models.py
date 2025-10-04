from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, Enum, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime

import enum

# Define an Enum for the sender type
class MessageSender(enum.Enum):
    user = "user"
    ai = "ai"

class MessageType(enum.Enum):
    conversation = "conversation"
    feedback = "feedback"
    image = "image" # New message type for images
    
# Define an Enum for the journal writing phase
class JournalPhase(enum.Enum):
    scaffolding = "scaffolding"
    writing = "writing"
    evaluation = "evaluation" # Changed from finishing
    completed = "completed"

# --- Authentication and Journaling Models ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    realname = Column(String(100), nullable=True)
    student_id = Column(String(50), unique=True, nullable=True, index=True)
    group = Column(String(50), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, server_default='f', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    
    journals = relationship("Journal", back_populates="owner")
    errors = relationship("UserError", back_populates="user")
    context_profile = relationship("UserContextProfile", back_populates="owner", uselist=False, cascade="all, delete-orphan")

# --- NEW Model for Student Whitelist ---
class StudentWhitelist(Base):
    __tablename__ = "student_whitelist"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))


class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    journal_date = Column(Date, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True, default='')
    outline_content = Column(Text, nullable=True, default='')
    # FIX: Set create_type=False to prevent SQLAlchemy from trying to re-create the ENUM.
    writing_phase = Column(Enum(JournalPhase, name="journalphase", create_type=False), default=JournalPhase.scaffolding, nullable=False)
    session_state = Column(JSONB, nullable=True) # New field for conversation state
    completion_metrics = Column(JSONB, nullable=True) # NEW: Field for storing writing metrics
    is_late = Column(Boolean, server_default='f', nullable=False) # New field for late submissions
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"), onupdate=datetime.utcnow)
    
    # Corrected relationships
    owner = relationship("User", back_populates="journals")
    # FIX: Added order_by to ensure chat messages are always sorted chronologically by their timestamp.
    chat_messages = relationship("ChatMessage", back_populates="journal", cascade="all, delete-orphan", order_by="ChatMessage.timestamp")
    images = relationship("JournalImage", back_populates="journal", cascade="all, delete-orphan", order_by="JournalImage.id") # New relationship

# --- NEW Journal Image Model ---
class JournalImage(Base):
    __tablename__ = "journal_images"
    id = Column(Integer, primary_key=True, index=True)
    journal_id = Column(Integer, ForeignKey("journals.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(512), nullable=False)
    ai_description = Column(Text, nullable=True)
    user_caption = Column(Text, nullable=True) # New field for user's caption
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    journal = relationship("Journal", back_populates="images")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    journal_id = Column(Integer, ForeignKey("journals.id", ondelete="CASCADE"), nullable=False)
    sender = Column(Enum(MessageSender, name="messagesender", create_type=False), nullable=False)
    message_text = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType, name="messagetype", create_type=False), default=MessageType.conversation, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    # New relationship to an image
    image_id = Column(Integer, ForeignKey("journal_images.id"), nullable=True)
    image = relationship("JournalImage")

    journal = relationship("Journal", back_populates="chat_messages")

# --- New User Context Profile Model ---
class UserContextProfile(Base):
    __tablename__ = "user_context_profiles"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    profile_data = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"), onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="context_profile")


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


# --- NEW Notification and Survey Models ---

class NotificationType(enum.Enum):
    announcement = "announcement"
    survey = "survey"

class SurveyQuestionType(enum.Enum):
    multiple_choice_single = "multiple_choice_single"
    multiple_choice_multiple = "multiple_choice_multiple"
    text = "text"

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType, name="notificationtype", create_type=False), nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    questions = relationship("SurveyQuestion", back_populates="notification", cascade="all, delete-orphan")

class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(SurveyQuestionType, name="questiontype", create_type=False), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    notification = relationship("Notification", back_populates="questions")
    options = relationship("SurveyOption", back_populates="question", cascade="all, delete-orphan")
    responses = relationship("SurveyResponse", back_populates="question", cascade="all, delete-orphan")

class SurveyOption(Base):
    __tablename__ = "survey_options"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("survey_questions.id", ondelete="CASCADE"), nullable=False)
    option_text = Column(String(500), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    question = relationship("SurveyQuestion", back_populates="options")

class UserNotificationStatus(Base):
    __tablename__ = "user_notification_status"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    notification_id = Column(Integer, ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    is_seen = Column(Boolean, default=False, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)

    user = relationship("User")
    notification = relationship("Notification")

class SurveyResponse(Base):
    __tablename__ = "survey_responses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("survey_questions.id", ondelete="CASCADE"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("survey_options.id", ondelete="CASCADE"), nullable=True)
    text_response = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())"))

    user = relationship("User")
    question = relationship("SurveyQuestion", back_populates="responses")
    selected_option = relationship("SurveyOption")
