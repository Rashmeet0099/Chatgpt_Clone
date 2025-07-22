from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    message: str
    topic: Optional[str] = "General"

class ChatResponse(BaseModel):
    response: str

class ChatHistorySchema(BaseModel):
    message: str
    response: str
    topic: Optional[str]
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }
