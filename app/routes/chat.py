from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ChatRequest
from app.services.openai_chat import get_response
from app.models import Chat, Session as ChatSession, User
from app.database import get_db
import uuid
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat_endpoint(request_data: ChatRequest, request: Request, db: Session = Depends(get_db)):
    username = request.headers.get("X-Username")
    if not username:
        raise HTTPException(status_code=401, detail="Unauthorized: Username header missing.")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: User not found.")

    # Reuse last session or create new one
    last_session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user.id)
        .order_by(ChatSession.id.desc())
        .first()
    )

    if last_session:
        session_id = last_session.session_id
    else:
        session_id = str(uuid.uuid4())
        new_session = ChatSession(user_id=user.id, session_id=session_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    # Fetch previous chat history (in natural order)
    history = (
        db.query(Chat)
        .filter(Chat.user_id == user.id, Chat.session_id == session_id)
        .order_by(Chat.timestamp)
        .all()
    )
    context = [{"message": chat.message, "response": chat.response} for chat in history]

    # Get AI response
    reply = get_response(message=request_data.message, topic=request_data.topic, context=context)

    # Save new chat
    new_chat = Chat(
        user_id=user.id,
        session_id=session_id,
        message=request_data.message,
        response=reply,
        topic=request_data.topic,
        timestamp=datetime.utcnow()
    )
    db.add(new_chat)
    db.commit()

    return {"response": reply}
