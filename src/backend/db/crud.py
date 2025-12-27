from sqlalchemy.orm import Session
from src.backend.db import models
import uuid

def get_chat_history(db: Session, session_id: str, limit: int = 50):
    """
    Retrieve chat history for a specific session.
    Ordered by creation time (oldest first).
    """
    return db.query(models.ChatHistory)\
        .filter(models.ChatHistory.session_id == session_id)\
        .order_by(models.ChatHistory.created_at.asc())\
        .limit(limit)\
        .all()

def create_chat_message(db: Session, session_id: str, role: str, content: str):
    """
    Save a new chat message to the database.
    """
    db_message = models.ChatHistory(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message