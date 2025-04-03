from pydantic import BaseModel

# Login schema
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatInput(BaseModel):
    message: str