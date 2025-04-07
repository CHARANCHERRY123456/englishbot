from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    correct_grammar: bool = True

class Message(MessageBase):
    id: str
    sender: str
    timestamp: str
    
    class Config:
        from_attributes = True