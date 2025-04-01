from jose import JOSEError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Secret Key and Algorithm
SECRET_KEY = "Thisisnotaverynotbigtoken"
ALGORITHM = "HS256"

# Password Hashing
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy User Database
fake_users_db = {
    "charan": {
        "username": "charan",
        "hashed_password": pwd_content.hash("charan")
    }
}

# Verify password
def verify_password(plain_pwd, hashed_pwd):
    return pwd_content.verify(plain_pwd, hashed_pwd)

def get_users_data(token:str):
    return jwt.decode(token=token ,key=SECRET_KEY)

# Create JWT Access Token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authenticate User
def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user
