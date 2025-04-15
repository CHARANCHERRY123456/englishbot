# extract the env variables here and use it everywhere

from dotenv import load_dotenv
load_dotenv()
import os

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
MONGODB_URI=os.getenv("MONGODB_URI")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
DB_NAME=os.getenv("DB_NAME")

