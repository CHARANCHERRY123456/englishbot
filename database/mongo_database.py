# db/mongo_database.py
from typing import List, Dict, Optional
from .mongo import conversations_collection
from bson import ObjectId

class MongoDatabase:
    @staticmethod
    async def create_conversation(conversation: Dict) -> str:
        result = await conversations_collection.insert_one(conversation)
        return str(result.inserted_id)

    @staticmethod
    async def get_conversation(conversation_id: str) -> Optional[Dict]:
        return await conversations_collection.find_one({"_id": ObjectId(conversation_id)})

    @staticmethod
    async def get_conversations_by_user(user_id: str) -> List[Dict]:
        cursor = conversations_collection.find({"user_id": user_id})
        return [conv async for conv in cursor]

    @staticmethod
    async def update_conversation(conversation_id: str, updated_data: Dict) -> bool:
        result = await conversations_collection.replace_one(
            {"_id": ObjectId(conversation_id)}, updated_data
        )
        return result.modified_count > 0

    @staticmethod
    async def delete_conversation(conversation_id: str) -> bool:
        result = await conversations_collection.delete_one({"_id": ObjectId(conversation_id)})
        return result.deleted_count > 0
