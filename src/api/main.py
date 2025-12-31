import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import agent, auth, chat
from src.memory.sql_store import init_db

app = FastAPI(title="Phoenix AI Agent API", version="1.0.0")

# Initialize DB
init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hacking, allow all. Tweak for prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
