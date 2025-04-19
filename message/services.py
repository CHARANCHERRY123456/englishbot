from typing import List
from fastapi import Depends
from bson import ObjectId
from datetime import datetime

from message.schemas import MessageCreate , MessageOut
from database.db import get_message_collection,get_conversation_collection,get_db
from fastapi import HTTPException

class MessageService:
    def __init__(self):
        self.db = get_db()
        self.messages= get_message_collection()
        self.conversations = get_conversation_collection()
    async def add_message(self, conversation_id: str, msg: MessageCreate) -> MessageOut:
        try:
            message_data = msg.dict()
            message_data["conversation_id"] = conversation_id
            message_data["timestamp"] = datetime.utcnow()
            print(message_data)
            result = await self.messages.insert_one(message_data)

            # Update last_message_at in conversation
            await self.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"last_message_at": message_data["timestamp"]}}
            )

            message_data["_id"] = str(result.inserted_id)
            return MessageOut(**message_data)
        except Exception as e:
            print(f"An error occurred while adding the message: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while adding the message: {e}")

    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[MessageOut]:
        try:
            # No need to await `find()`, just chain methods
            cursor = self.messages.find({"conversation_id": conversation_id}).sort("timestamp", -1).skip(offset).limit(limit)
            
            # Use `to_list()` to retrieve the results
            messages = await cursor.to_list(length=limit)

            # Convert ObjectId to string for each message
            for message in messages:
                message["_id"] = str(message["_id"])

            # Return the list of messages as MessageOut objects
            return [MessageOut(**msg) for msg in messages]
        except Exception as e:
            print(f"An error occurred while fetching conversation history: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch conversation history")

def get_message_service():
    return MessageService()