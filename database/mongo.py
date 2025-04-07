from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

MONGO_URI = "mongodb://localhost:27017"
DB_NAME="chat_db"

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

# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2N2YzZjBjMTVhZDM5Y2FmMmRlNjE0NmMiLCJleHAiOjE3NDQwNDM3Mjl9.Hovl7lWwDiBgwM0BhMjps7niRKI4vikEbYQdT7zMFfw",
#   "token_type": "bearer"
# }

# {
#   "id": "67f3f18de24182284cfce06b",
#   "user_id": "67f3f0c15ad39caf2de6146c",
#   "created_at": "2025-04-07T15:38:53.103088",
#   "messages": []
# }