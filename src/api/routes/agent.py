from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from src.api.models import AnalysisResponse, RecoveryResponse
from src.manager.workflow_graph import WorkflowGraph
from src.memory.sql_store import get_db, UserSkills, RecoveryPlan
import shutil
import os
import uuid
import json

router = APIRouter()
workflow_graph = WorkflowGraph() 

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/profile", response_model=AnalysisResponse)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    skill_record = db.query(UserSkills).filter(UserSkills.user_id == user_id).first()
    if not skill_record:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Reconstruct AnalysisResponse
    return AnalysisResponse(
        profile_summary={'resume_data': {'raw_text': skill_record.resume_text}}, # simplified
        skills={'technical_skills': skill_record.skills_data},
        github_stats=skill_record.github_data or {}
    )

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_profile(
    github_username: str = Form(None),
    user_id: str = Form(None),
    resume: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    resume_path = None
    if resume:
        file_ext = resume.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        resume_path = os.path.join(UPLOAD_DIR, file_name)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

    user_input = {
        'resume_path': resume_path,
        'github_username': github_username,
        'rejection_scenario': False
    }

    try:
        result = workflow_graph.run(user_input)
        
        final_output = result.get('final_output', {})
        profile_data = final_output.get('profile_summary', {})
        resume_data = profile_data.get('resume_data', {})
        
        # Save to DB if user_id provided
        if user_id:
            existing = db.query(UserSkills).filter(UserSkills.user_id == user_id).first()
            if not existing:
                existing = UserSkills(user_id=user_id)
                db.add(existing)
            
            existing.resume_text = resume_data.get('raw_text', '')
            existing.skills_data = profile_data.get('skills', {}).get('technical_skills', {})
            existing.github_data = profile_data.get('github_data', {})
            db.commit()

        # Cleanup
        if resume_path and os.path.exists(resume_path):
            os.remove(resume_path)
            
        return AnalysisResponse(
            profile_summary=profile_data,
            skills=profile_data.get('skills', {}),
            github_stats=profile_data.get('github_data', {})
        )

    except Exception as e:
        if resume_path and os.path.exists(resume_path):
            os.remove(resume_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recover", response_model=RecoveryResponse)
async def generate_recovery(
    context: str = Form(...),
    job_description: str = Form(...),
    user_id: str = Form(None),
    github_username: str = Form(None),
    db: Session = Depends(get_db)
):
    resume_text = None
    skills_data = {}
    
    # Context retrieval
    if user_id:
        user_skills = db.query(UserSkills).filter(UserSkills.user_id == user_id).first()
        if user_skills:
            resume_text = user_skills.resume_text
            skills_data = user_skills.skills_data
            # If no github provided in form, use saved one
            if not github_username and user_skills.github_data:
                 # It's stored as JSON, might need extracting username or just passing data
                 # For now, let's just rely on what we can pass. 
                 # Ideally, WorkflowGraph accepts 'profile_data' directly.
                 pass

    # If no resume text found, we might need to rely purely on context or ask user to re-upload.
    # For MVP, we assume some context is better than none.

    user_input = {
        'github_username': github_username,
        'rejection_scenario': True,
        'rejection_context': context,
        'rejected_job': {'description': job_description},
        'resume_text': resume_text, # Pass raw text if available
        'existing_skills': skills_data # Pass extracted skills
    }
    
    try:
        # We need to update WorkflowGraph to accept 'resume_text' direct injection 
        # instead of always parsing a file path.
        result = workflow_graph.run(user_input)
        final_output = result.get('final_output', {})
        
        diagnosis = final_output.get('diagnosis', {})
        strategy = final_output.get('recovery', {})

        # Save to DB if user_id is present
        if user_id:
            new_plan = RecoveryPlan(
                user_id=user_id,
                rejection_context=context,
                job_description=job_description,
                diagnosis=diagnosis,
                strategy=strategy
            )
            db.add(new_plan)
            db.commit()

        return RecoveryResponse(
            diagnosis=diagnosis,
            recovery_strategy=strategy
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list)
async def get_recovery_history(user_id: str, db: Session = Depends(get_db)):
    plans = db.query(RecoveryPlan).filter(RecoveryPlan.user_id == user_id).order_by(RecoveryPlan.created_at.desc()).all()
    # Simple list return, could define specific Pydantic model
    return [
        {
            "id": p.id,
            "created_at": p.created_at,
            "rejection_context": p.rejection_context,
            "job_title": p.strategy.get('detailed_analysis', {}).get('industry_expectations', {}).get('level', 'Unknown Role') if p.strategy else "Unknown",
            "diagnosis": p.diagnosis,
            "strategy": p.strategy
        }
        for p in plans
    ]

@router.delete("/recovery/plan/{plan_id}")
async def delete_recovery_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(RecoveryPlan).filter(RecoveryPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    db.delete(plan)
    db.commit()
    return {"status": "success", "message": "Recovery plan deleted"}