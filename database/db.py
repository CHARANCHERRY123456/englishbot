from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()
import os

# get MONGO_URI from the env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "chatdb")

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db["users"]
conversations_collection = db["conversations"]

async def get_user_collection():
    return users_collection
async def get_conversation_collection():
    return conversations_collection
async def get_db():
    return db