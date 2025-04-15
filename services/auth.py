# # services/auth.py
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from fastapi import HTTPException, Depends
# from fastapi.security import OAuth2PasswordBearer
# from config import settings
# from core.db import users_collection

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # OAuth2 scheme for token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# # Verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Hash password
# def get_password_hash(password):
#     return pwd_context.hash(password)

# # Create JWT token
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# # Authenticate user
# def authenticate_user(username: str, password: str):
#     user = users_collection.find_one({"username": username})
#     if not user or not verify_password(password, user["hashed_password"]):
#         return False
#     return user

# # Get current user from token
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         user = users_collection.find_one({"username": username})
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")