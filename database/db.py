from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import DB_NAME , MONGODB_URI


# Initialize async MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
USER_COLLECTION = db["users"]

def get_db():
    """
    Get the database client.
    """
    return db
def get_user_collection():
    """
    Get the user collection.
    """
    return USER_COLLECTION

