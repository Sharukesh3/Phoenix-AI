import os
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Database Configuration
# Default to localhost for local testing, overridden by env var in Docker
DATABASE_URL = os.getenv("POSTGRES_URI", "postgresql://user:password@localhost:5432/career_guide")

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    uid = Column(String, primary_key=True) # Firebase UID
    email = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(String, primary_key=True) # UUID
    user_id = Column(String, ForeignKey('users.uid'))
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey('chat_sessions.id'))
    role = Column(String) # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class UserSkills(Base):
    __tablename__ = 'user_skills'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.uid'), index=True) 
    resume_text = Column(String, nullable=True) # Store raw resume text
    skills_data = Column(JSON) # e.g. {"python": "expert"}
    github_data = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ApplicationHistory(Base):
    __tablename__ = 'application_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.uid'))
    job_id = Column(String)
    company = Column(String)
    status = Column(String) 
    feedback = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

class LearningRoadmap(Base):
    __tablename__ = 'learning_roadmap'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.uid'))
    topic = Column(String)
    status = Column(String)
    resources = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class RecoveryPlan(Base):
    __tablename__ = 'recovery_plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.uid'))
    # Storing the context that generated this plan
    rejection_context = Column(String) 
    job_description = Column(String)
    # The output from the agent
    diagnosis = Column(JSON)
    strategy = Column(JSON)
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
