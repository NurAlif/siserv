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

