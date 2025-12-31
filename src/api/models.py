from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    github_username: Optional[str] = None
    # In a real app, file upload is handled via Form/File, so we might not need resume_path here
    # but for manual/testing or if file is already on server:
    resume_path: Optional[str] = None 

class RejectionRequest(BaseModel):
    rejected_job_data: Dict[str, Any]
    rejection_context: str
    # We need the profile data context to generate a strategy. 
    # In a stateless API, client sends it back, or we retrieve from DB. 
    # For this hackathon MVP, we'll assume the client sends pertinent profile info or we re-fetch.
    github_username: Optional[str] = None

class AnalysisResponse(BaseModel):
    profile_summary: Dict[str, Any]
    skills: Dict[str, Any]
    github_stats: Dict[str, Any]

class RecoveryResponse(BaseModel):
    diagnosis: Dict[str, Any]
    recovery_strategy: Dict[str, Any]

class UserLoginRequest(BaseModel):
    uid: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class ChatRequest(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
