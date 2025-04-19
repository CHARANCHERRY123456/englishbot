# message , conversation schema
from pydantic import BaseModel , EmailStr,Field
from typing import List, Optional
from datetime import datetime



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

# when want to list all the conversations of an user
class ConversationOutList(BaseModel):
    conversations: List[ConversationOut]
    total: int

