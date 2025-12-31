from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.memory.sql_store import get_db, ChatSession, ChatMessage
from src.api.models import ChatRequest, ChatResponse
import uuid
from src.llm.groq_client import GroqClient # Direct LLM for now, will connect to Agent later

router = APIRouter()
llm_client = GroqClient()

@router.post("/message", response_model=ChatResponse)
def chat_message(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get or Create Session
        session_id = request.session_id
        if not session_id:
            session_id = str(uuid.uuid4())
            new_session = ChatSession(id=session_id, user_id=request.user_id, title=request.message[:30])
            db.add(new_session)
            db.commit()
        
        # Save User Message
        user_msg = ChatMessage(session_id=session_id, role='user', content=request.message)
        db.add(user_msg)
        db.commit()

        # Generate Response (Simple LLM call for now, replacing full agent flow for chat)
        # RAG Retrieval
        try:
            from src.memory.vector_store import get_vector_store
            vector_store = get_vector_store()
            # Search for context
            docs = vector_store.similarity_search(request.message, k=3)
            context_text = "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            print(f"RAG Retrieval failed: {e}")
            vector_store = None
            context_text = ""

        system_prompt = "You are an empathetic career counselor AI. Help the user with their career rejections."
        if context_text:
            system_prompt += f"\n\nHere is some relevant context from the knowledge base/memory:\n{context_text}\n\nUse this context to answer if relevant, but prioritize empathy."

        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Load history
        history = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp).all()
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        ai_response_text = llm_client.chat_completion(messages)

        # Save AI Response
        ai_msg = ChatMessage(session_id=session_id, role='assistant', content=ai_response_text)
        db.add(ai_msg)
        db.commit()

        # Persist to Vector Store (Knowledge Base)
        if vector_store:
            try:
                # Add User Message
                vector_store.add_texts(
                    texts=[request.message],
                    metadatas=[{"role": "user", "session_id": session_id, "user_id": request.user_id, "type": "chat_history"}]
                )
                # Add AI Response
                vector_store.add_texts(
                    texts=[ai_response_text],
                    metadatas=[{"role": "assistant", "session_id": session_id, "user_id": request.user_id, "type": "chat_history"}]
                )
            except Exception as e:
                print(f"Failed to persist to vector store: {e}")

        return ChatResponse(response=ai_response_text, session_id=session_id)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
