# models for the message and conversation in ai chat bot

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ConversationModel(BaseModel):
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None