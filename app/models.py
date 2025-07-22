from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, unique=True, nullable=False)

    user = relationship("User", back_populates="sessions")
    chats = relationship("Chat", back_populates="session", cascade="all, delete-orphan")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    topic = Column(String, nullable=True)  # ✅ Optional topic info for filtering
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")
    session = relationship("Session", back_populates="chats")
