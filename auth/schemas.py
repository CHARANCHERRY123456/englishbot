# scheamas to use in the req , res
from pydantic import BaseModel, EmailStr

# normal user model details
class UserBase(BaseModel):
    email: EmailStr
    username : str


# when getting the signup req
class UserSignin(UserBase):
    email: EmailStr
    username : str
    password: str

# when getting the login req
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# return after signup, login return the token then can get details with other route
class Token(BaseModel):
    access_token: str
    token_type: str
