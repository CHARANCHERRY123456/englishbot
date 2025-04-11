from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    content: str
    sender_id: str = Field(..., min_length=3)
    conversation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    embedding: Optional[List[float]] = None  # For context-aware replies

class ConversationCreate(BaseModel):
    participant_ids: List[str] = Field(..., min_length=1)
    context: Optional[dict] = {}  # Store language learning context

class ConversationResponse(ConversationCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
