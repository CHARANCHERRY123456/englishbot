from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from database.db import get_message_collection, get_conversation_collection
from message.schemas import MessageCreate, MessageOut
import uuid

# getting the reply from the gemini
async def get_answer_using_gemini(content: str) -> str:
    return {
        "corrections" : " no corrections all are correct",
        "content" : "hi hlo how are you",
        "grammar_score" : 10
    }

# save message to the database
async def add_message_to_db(conversation_id: str, msg: MessageCreate) -> MessageOut:
    try:
        doc = msg.dict()
        doc["conversation_id"] = conversation_id
        doc["timestamp"] = datetime.utcnow()
        # update last_message_at for conversation
        await update_last_message_in_conversation(conversation_id)

        result = await get_message_collection().insert_one(doc)
        if result.inserted_id:
            doc["_id"] = str(result.inserted_id)
            return doc
        return None
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while adding the message to the database: {e}")
        return None

# update last message in the conversation
async def update_last_message_in_conversation(conversation_id: str) -> bool:
    try:
        result = await get_conversation_collection().update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"last_message_at": datetime.utcnow()}},
        )
        return result.modified_count > 0
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while updating the conversation: {e}")
        return False