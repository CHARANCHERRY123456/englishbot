from pydantic import BaseModel
from typing import List, Optional
from .message import Message

class Conversation(BaseModel):
    id: str
    user_id: str
    title: str
    type: str
    created_at: str
    messages: List[Message]
