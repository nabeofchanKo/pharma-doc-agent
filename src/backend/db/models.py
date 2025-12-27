from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from src.backend.db.database import Base

class ChatHistory(Base):
    """
    Database model for storing chat history.
    Table Name: chat_history
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)

    # Session ID allows grouping messages by conversation (future proofing)
    session_id = Column(String, index=True, default="default_session")

    # Role: 'user' or 'assistant'
    role = Column(String)

    # The actual message content
    content = Column(Text)

    # Timestamp of creation (auto-generated)
    created_at = Column(DateTime(timezone=True), server_default=func.now())