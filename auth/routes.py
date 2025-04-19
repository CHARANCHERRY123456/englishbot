from fastapi import APIRouter, HTTPException, Depends
from auth.schemas import UserLogin, GetUser, UserSignin, Token
from auth.services import signup_user, login_user, get_current_user
from logger import logger

router = APIRouter()

@router.post("/signup", response_model=Token)
async def signup(user: UserSignin):
    try:
        print("User signup request received")
        return await signup_user(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Signup failed")
        raise HTTPException(status_code=500, detail="Signup error")

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        return await login_user(user)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Login failed")
        raise HTTPException(status_code=500, detail="Login error")

@router.get("/user/{token}", response_model=GetUser)
async def get_user(token: str):
    try:
        print("Get user request received")
        return await get_current_user(token)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Get user error")