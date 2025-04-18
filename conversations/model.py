from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MessageModel(BaseModel):
    content: str
    sender_id: str
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    message_type: str = "text"
    embedding: Optional[List[float]] = []
    corrections: str = "No corrections has available"
    grammar_score: Optional[float] = None

class ConversationModel(BaseModel):
    user_id : str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    context: Optional[dict] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None