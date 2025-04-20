from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from database.db import get_message_collection, get_conversation_collection
from message.schemas import MessageCreate, MessageOut
import uuid
from gemini.services import GeminiService
from config import GEMINI_API_KEY

gemini = GeminiService(GEMINI_API_KEY)

# getting the reply from the gemini
async def get_answer_using_gemini(content: str, history: List[str]) -> dict:
    try:
        response = gemini.send(content, history)
        return response
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while getting a reply from Gemini: {e}")
        return {"error": "Sorry, I couldn't process your request."}

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

# get conversation history to send to the gemini
async def get_conversation_history_for_gemini(conversation_id: str) -> List[str]:
    try:
        messages = await get_message_collection().find(
            {"conversation_id": conversation_id}
        ).sort("timestamp", -1).to_list(length=10)
        
        # Reversing to oldest-to-newest order
        return list(reversed([message["content"] for message in messages]))
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while fetching conversation history: {e}")
        return []