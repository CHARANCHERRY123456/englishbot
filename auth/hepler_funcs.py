# helping functions for routes
from passlib.context import CryptContext
from jose import jwt
from logger import logger
import os

SECRET_KEY = os.getenv("SECRET_KEY" , "mysecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return False

def get_passowrd_hash(password):
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {str(e)}")
        return None

def create_access_token(data: dict):
    try:
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"JWT encoding error: {str(e)}")
        return None

def decode_user(token:str):
    try:
        return jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])
    except Exception as e:
        logger.error(f"JWT decoding error: {str(e)}")
        return None
        