from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.memory.sql_store import get_db, User
from src.api.models import UserLoginRequest

router = APIRouter()

@router.post("/login")
def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.uid == request.uid).first()
        if not user:
            user = User(
                uid=request.uid,
                email=request.email,
                full_name=request.full_name
            )
            db.add(user)
        else:
            # Update info if changed
            if request.email: user.email = request.email
            if request.full_name: user.full_name = request.full_name
            
        db.commit()
        db.refresh(user)
        return {"status": "success", "user": {"uid": user.uid, "name": user.full_name}}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user/{uid}")
def delete_user(uid: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.uid == uid).first()
        if not user:
             raise HTTPException(status_code=404, detail="User not found")
        
        # 1. Collect Session IDs for Vector Deletion
        from src.memory.sql_store import ChatSession, ChatMessage, UserSkills, RecoveryPlan, ApplicationHistory, LearningRoadmap
        user_sessions = db.query(ChatSession).filter(ChatSession.user_id == uid).all()
        session_ids = [s.id for s in user_sessions]

        # 2. Manual Cascade Delete (SQL)
        # Delete Chat Messages
        if session_ids:
            db.query(ChatMessage).filter(ChatMessage.session_id.in_(session_ids)).delete(synchronize_session=False)
        
        # Delete Chat Sessions
        db.query(ChatSession).filter(ChatSession.user_id == uid).delete(synchronize_session=False)

        # Delete Recovery Plans
        db.query(RecoveryPlan).filter(RecoveryPlan.user_id == uid).delete(synchronize_session=False)

        # Delete User Skills
        db.query(UserSkills).filter(UserSkills.user_id == uid).delete(synchronize_session=False)
        
        # Delete Other History
        db.query(ApplicationHistory).filter(ApplicationHistory.user_id == uid).delete(synchronize_session=False)
        db.query(LearningRoadmap).filter(LearningRoadmap.user_id == uid).delete(synchronize_session=False)

        # Delete User
        db.delete(user)
        db.commit()

        # 3. Delete Vector Data (RAG Memory)
        try:
            from src.memory.vector_store import get_vector_store
            vector_store = get_vector_store()
            from qdrant_client.http import models
            
            # Delete by User ID (New data)
            vector_store.client.delete(
                collection_name=vector_store.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="metadata.user_id",
                                match=models.MatchValue(value=uid)
                            )
                        ]
                    )
                )
            )

            # Delete by Session IDs (Old data)
            if session_ids:
                 vector_store.client.delete(
                    collection_name=vector_store.collection_name,
                    points_selector=models.FilterSelector(
                        filter=models.Filter(
                            must=[
                                models.FieldCondition(
                                    key="metadata.session_id",
                                    match=models.MatchAny(any=session_ids)
                                )
                            ]
                        )
                    )
                )

        except Exception as vec_e:
            print(f"Vector delete warning: {vec_e}")

        return {"status": "success", "message": "User account and all data deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
