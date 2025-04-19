# models for the message and conversation in ai chat bot

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageModel(BaseModel):
    content: str
    sender_id: str
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    message_type: str = "text"
    embedding: list = []
    corrections: str = "No corrections available"
    grammar_score: Optional[float] = None

class ConversationModel(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None