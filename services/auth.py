from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime , timedelta
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from config import settings
from db import user_collection



pwd_context = CryptContext(schemes=["bycrypt"],deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data:dict):
    data_copy = data.copy()
    expire = datetime.utcnow() + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy["exp"] = expire
    encoded_jwt = jwt.encode(data_copy,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(username:str,password:str):
    user = user_collection.find_one({"username" : username})
    if not user:
        return False
    if not verify_password(password,user["password"]):
        return False
    return user

async def get_current_user(token:str=Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username:str=payload.get("sub")
        if not username:
            raise HTTPException(status_code=401,detail="Invalid token")
        user = user_collection.find_one({
            "username" : username
        })
        return user
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
