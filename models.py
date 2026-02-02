from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

chat_users = Table(
    "chat_users",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chats.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    last_seen = Column(DateTime, nullable=True)
    is_online = Column(Boolean, default=False)

    chats = relationship("Chat", secondary=chat_users, backref="users")


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User")
    chat = relationship("Chat")

