from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Correction(BaseModel):
    suggestion: str

class MessageCreate(BaseModel):
    content: str
    sender_id: str
    message_type: str = "text"
    embedding: Optional[List[float]] = []
    reply_to: Optional[str] = None

class MessageOut(MessageCreate):
    id: str = Field(..., alias="_id")
    conversation_id: str
    timestamp: datetime
    corrections: str = "no correction is found"
    grammar_score: Optional[float] = 0
    reply:str="No reply found"

class ConversationCreate(BaseModel):
    participant_ids: List[str]

class ConversationOut(ConversationCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime
    last_message_at: Optional[datetime]