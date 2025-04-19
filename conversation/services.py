from typing import List
from fastapi import Depends
from datetime import datetime

from conversation.schemas import (
    ConversationCreate, ConversationOut,
)
from database.db import get_db , get_conversation_collection
from fastapi import HTTPException, status

class ConversationService:
    def __init__(self, db):
        self.db = get_db()
        self.conversations = get_conversation_collection()

    async def create_conversation(self, data: ConversationCreate) -> ConversationOut:
        try:
            conversation_dict = data.dict()
            conversation_dict["created_at"] = datetime.utcnow()
            conversation_dict["last_message_at"] = None

            result = await self.conversations.insert_one(conversation_dict)
            conversation_dict["_id"] = str(result.inserted_id)
            return ConversationOut(**conversation_dict)
        except Exception as e:
            print(f"Error creating conversation: {e}")
            raise

    async def delete_conversation(self, conversation_id: str) -> bool:
        try:
            await self.conversations.delete_one({"_id": conversation_id})
            return True
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    async def get_conversations_by_user(self, user_id: str):
        try:
            cursor = self.conversations.find({"user_id": user_id})
            conversations =  await cursor.to_list(length=None)
            for conversation in conversations:
                conversation["_id"] = str(conversation["_id"])
            return conversations
        except Exception as e:
            print(f"Error fetching conversations by user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching conversations."
            )

# Dependency
def get_conversation_service(db=Depends(get_db)) -> ConversationService:
    return ConversationService(db)
