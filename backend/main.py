from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid

# Import the chatbot logic
from chatbot import get_chatbot_response

app = FastAPI(title="SoulSync AI API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (In production, use Redis or a database)
sessions: Dict[str, Dict] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    is_risk: bool
    is_early_risk: bool

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "SoulSync AI Engine"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    
    # Create a new session if not provided or doesn't exist
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "history": [],
            "entities": [],
            "profile": {
                "common_emotions": [],
                "patterns": [],
                "entities": []
            }
        }
    
    session = sessions[session_id]
    
    try:
        reply, is_risk, is_early_risk = get_chatbot_response(
            request.message, 
            session["history"], 
            session["entities"], 
            session["profile"]
        )
        
        return ChatResponse(
            reply=reply,
            session_id=session_id,
            is_risk=is_risk,
            is_early_risk=is_early_risk
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "cleared"}
    return {"status": "not_found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
