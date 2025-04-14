from fastapi import APIRouter, HTTPException, Depends, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from database.db import get_user_collection
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# JWT config
SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Models
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ----------------- Routes -----------------

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, users: AsyncIOMotorCollection = Depends(get_user_collection)):
    try:
        existing = await users.find_one({"email": user.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = get_password_hash(user.password)
        result = await users.insert_one({"email": user.email, "password": hashed_pw})
        user_id = str(result.inserted_id)

        token = create_access_token({"sub": user_id})
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.exception("Signup failed")
        raise HTTPException(status_code=500, detail="Signup error")


@router.post("/login", response_model=Token)
async def login(user: UserLogin, users: AsyncIOMotorCollection = Depends(get_user_collection)):
    try:
        db_user = await users.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user_id = str(db_user["_id"])
        token = create_access_token({"sub": user_id})
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.exception("Login failed")
        raise HTTPException(status_code=500, detail="Login error")
