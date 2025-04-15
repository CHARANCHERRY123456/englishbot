from fastapi import HTTPException
from auth.schemas import UserLogin, UserBase, UserSignin, Token
from auth.utils import verify_password, decode_access_token, get_password_hash, create_access_token
from database.db import get_user_collection

users = get_user_collection()

async def signup_user(user: UserSignin) -> Token:
    existing_email_user = await users.find_one({"email": user.email})
    exisiting_username_user = await users.find_one({"username": user.username})
    if exisiting_username_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    if existing_email_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    result = await users.insert_one({
        "email": user.email, 
        "password": hashed_password,
        "username": user.username
    })
    user_id = str(result.inserted_id)
    token = create_access_token({
        "userid": user_id,
        "email": user.email,
        "username": user.username
    })
    return {"access_token": token, "token_type": "bearer"}

async def login_user(user: UserLogin) -> Token:
    db_user = await users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(db_user["_id"])
    token = create_access_token({
        "sub": user_id,
        "email": user.email,
        "username": db_user.get("username", "")
    })
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: Token) -> UserBase:
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return UserBase(**user)