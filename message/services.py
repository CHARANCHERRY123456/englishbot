from typing import List
from message.schemas import MessageCreate , MessageOut
from message.utils import add_message_to_db, get_answer_using_gemini
from database.db import get_message_collection,get_conversation_collection,get_db
from fastapi import HTTPException

class MessageService:
    def __init__(self):
        self.db = get_db()
        self.messages= get_message_collection()
        self.conversations = get_conversation_collection()
    async def add_message(self, conversation_id: str, msg: MessageCreate) -> MessageOut:
        try:
            # 1. Save user message to DB
            user_message_data = await add_message_to_db(conversation_id, msg)
            if not user_message_data:
                raise HTTPException(status_code=500, detail="Failed to add message to the database")

            # 2. Get Gemini response
            response = await get_answer_using_gemini(msg.content)

            # 3. Prepare reply message
            reply_msg = MessageCreate(
                content=response["reply"],
                sender_id="bot",
                conversation_id=conversation_id,
                reply_to=user_message_data.get("_id")
            )
            bot_reply_data = await add_message_to_db(conversation_id, reply_msg)
            if not bot_reply_data:
                raise HTTPException(status_code=500, detail="Failed to add reply message to the database")
            
            bot_reply_data["corrections"] = response["corrections"]
            bot_reply_data["content"] = response["content"]
            bot_reply_data["grammar_score"] = response["grammar_score"]


            # 4. Return the bot’s message
            return MessageOut(**bot_reply_data)

        except Exception as e:
            print(f"Error in add_message: {e}")
            raise HTTPException(status_code=500, detail=f"Server error: {e}")


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