import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Database Configuration
# Default to localhost for local testing, overridden by env var in Docker
DATABASE_URL = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/career_guide")

Base = declarative_base()

class UserSkills(Base):
    __tablename__ = 'user_skills'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True) # Could be linked to an auth system
    skills_data = Column(JSON) # e.g. {"python": "expert", "rust": "beginner"}
    updated_at = Column(DateTime, default=datetime.utcnow)

class ApplicationHistory(Base):
    __tablename__ = 'application_history'
    id = Column(Integer, primary_key=True)
    job_id = Column(String)
    company = Column(String)
    status = Column(String) # rejected, interview, etc.
    feedback = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

class LearningRoadmap(Base):
    __tablename__ = 'learning_roadmap'
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    status = Column(String) # todo, in_progress, done
    resources = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Engine and Session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
