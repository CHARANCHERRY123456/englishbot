from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGODB_URL)
db = client["linguabot"]
users_collection = db["users"]
conversations_collection=db["conversations"]