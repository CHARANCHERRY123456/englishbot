from fastapi import APIRouter
from auth.schemas  import UserLogin,UserBase,UserSignin
from database.db import get_user_collection
router = APIRouter()


@router.post("/signup" , response_model=Token)
async def signup(user:UserSignin):
    try:
        users = get_user_collection()
    except Exception as e:
        print(e)
        return None








