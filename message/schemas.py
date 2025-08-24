from pydantic import BaseModel , EmailStr,Field
from typing import List, Optional
from datetime import datetime

# when sending a message to the bot
class MessageCreate(BaseModel):
    content : str
    sender_id : str


    message_type : str = "text"
    embedding : Optional[List[float]] = None
    reply_to : Optional[str] = None
    corrections : Optional[str] = "Seems you are pro at english"

# sending bot reply to sender
class MessageOut(MessageCreate):
    id : str = Field(..., alias="_id")
    conversation_id : str
    timestamp : datetime

    
    corrections : str = "no correction is found"
    content : str = "No reply found"
    grammar_score : Optional[float] = 0.0