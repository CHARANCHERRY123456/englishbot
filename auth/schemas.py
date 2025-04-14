from pydantic import BaseModel, EmailStr

# scheamas to use in the req
class UserBase(BaseModel):
    email: EmailStr
    user_id : str
class UserSignin(UserBase):
    email: EmailStr
    user_id : str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id : str