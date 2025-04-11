from pydantic import BaseModel
from typing import Optional

class MessageCreate(BaseModel):
    content: str
    correct_grammar: Optional[bool] = False

class Message(BaseModel):
    id: str
    content: str
    sender: str
    timestamp: str
    correction: Optional[str] = None
    rating: Optional[int] = None
