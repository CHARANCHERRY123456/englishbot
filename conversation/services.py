from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import Depends
from datetime import datetime

from conversation.schemas import (
    ConversationCreate, ConversationOut,
    MessageCreate, MessageOut
)
from database.db import get_db , get_conversation_collection , get_message_collection

class ConversationService:
    def __init__(self, db):
        self.db = get_db()
        self.conversations = get_conversation_collection()
        self.messages = get_message_collection()

    async def create_conversation(self, data: ConversationCreate) -> ConversationOut:
        conversation_dict = data.dict()
        conversation_dict["created_at"] = datetime.utcnow()
        conversation_dict["last_message_at"] = None

        result = await self.conversations.insert_one(conversation_dict)
        conversation_dict["_id"] = str(result.inserted_id)
        return ConversationOut(**conversation_dict)

    async def add_message(self, conversation_id: str, msg: MessageCreate) -> MessageOut:
        message_data = msg.dict()
        message_data["conversation_id"] = conversation_id
        message_data["timestamp"] = datetime.utcnow()

        result = await self.messages.insert_one(message_data)

        # Update last_message_at in conversation
        await self.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"last_message_at": message_data["timestamp"]}}
        )

        message_data["_id"] = str(result.inserted_id)
        return MessageOut(**message_data)

    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[MessageOut]:
        cursor = self.messages.find({"conversation_id": conversation_id}).sort("timestamp", -1).skip(offset).limit(limit)
        messages = await cursor.to_list(length=limit)

        for message in messages:
            message["_id"] = str(message["_id"])
        return [MessageOut(**msg) for msg in messages]

# Dependency
def get_conversation_service(db=Depends(get_db)) -> ConversationService:
    return ConversationService(db)
