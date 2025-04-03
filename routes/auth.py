from fastapi import APIRouter, HTTPException
from models.user import UserLogin, Token
from services.auth import authenticate_user, create_access_token, get_password_hash
from db import users_collection

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    authenticated_user = authenticate_user(user.username, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register(user: UserLogin):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = get_password_hash(user.password)
    user_dict = {"username": user.username, "hashed_password": hashed_password}
    users_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}