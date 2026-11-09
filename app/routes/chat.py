from fastapi import APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.chat.orchestrator import chat

router =APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("")
def chat_endpoint(req: ChatRequest, db:Session=Depends(get_db), current_user: User= Depends(get_current_user)):
    return {"reply": chat(db, current_user, req.message)}