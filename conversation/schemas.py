# message , conversation schema
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

# sending bot reply to sender
class MessageOut(MessageCreate):
    id : str = Field(..., alias="_id")
    conversation_id : str
    timestamp : datetime
    corrections : str = "no correction is found"
    content : str = "No reply found"
    grammar_score : Optional[float] = 0.0

# when creating a conversation
class ConversationCreate(BaseModel):
    user_id : str
    description : Optional[str] = None
    image : Optional[str] = None
    title : str

# when sending a conversation to the user
class ConversationOut(ConversationCreate):
    id : str = Field(..., alias="_id")
    created_at : datetime
    last_message_at : Optional[datetime] = None


