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
    corrections: Optional[List[dict]] = []
    grammar_score: Optional[float] = None
    rating: Optional[float] = None

class ConversationModel(BaseModel):
    participant_ids: List[str]
    context: Optional[dict] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
