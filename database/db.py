from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import DB_NAME , MONGODB_URI


# Initialize async MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
USER_COLLECTION = db["users"]
MESSAGE_COLLECTION = db["messages"]
CONVERSATION_COLLECTION = db["conversations"]

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
def get_message_collection():
    """
    Get the message collection.
    """
    return MESSAGE_COLLECTION

def get_conversation_collection():
    """
    Get the conversation collection.
    """
    return CONVERSATION_COLLECTION