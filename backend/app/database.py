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

