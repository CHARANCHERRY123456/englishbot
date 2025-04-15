from fastapi import APIRouter , HTTPException, Depends
from auth.schemas  import UserLogin,UserBase,UserSignin,Token
from auth.hepler_funcs import verify_password , decode_user , get_passowrd_hash , create_access_token
from logger import logger
from database.db import get_user_collection
router = APIRouter()
users = get_user_collection()

@router.post("/signup" , response_model=Token)
async def signup(user:UserSignin):
    try:
        existing_user = await users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_passowrd_hash(user.password)
        result = await users.insert_one({"email": user.email, "password": hashed_password})
        user_id = str(result.inserted_id)
        token = create_access_token({"sub": user_id , "email": user.email , "username": user.username})
        return {"access_token": token , "token_type": "bearer"}
    except Exception as e:
        logger.exception("Signup failed")
        raise HTTPException(status_code=500, detail="Signup error")

@router.post("/login" , response_model=Token)
async def login(user:UserLogin):
    try:
        db_user = await users.find_one({"email": user.email})
        if not db_user or not verify_password(user.password , db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_id = str(db_user["_id"])
        token = create_access_token({"sub": user_id , "email": user.email , "username": db_user["username"]})
        return {"access_token": token , "token_type": "bearer"}
    except Exception as e:
        logger.exception("Login failed")
        raise HTTPException(status_code=500, detail="Login error")

@router.get("/user", response_model=UserBase)
async def get_user(token:Token):
    try:
        user = decode_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return UserBase(**user)
    except Exception as e:
        logger.exception("Get user failed")
        raise HTTPException(status_code=500, detail="Get user error")





