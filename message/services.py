from typing import List
from message.schemas import MessageCreate , MessageOut
from message.utils import add_message_to_db, get_answer_using_gemini,get_conversation_history_for_gemini
from message.t5utils import get_answer_using_t5
from database.db import get_message_collection,get_conversation_collection,get_db
from fastapi import HTTPException

class MessageService:
    def __init__(self):
        self.db = get_db()
        self.messages= get_message_collection()
        self.conversations = get_conversation_collection()
    async def add_message(self, conversation_id: str, msg: MessageCreate) -> MessageOut:
        print(f"Starting to add message to conversation {conversation_id}")
        try:
            # 1. Save user message to DB
            print(f"Attempting to save user message: {msg}")
            user_message_data = await add_message_to_db(conversation_id, msg)
            if not user_message_data:
                print("Failed to add user message to the database")
                raise HTTPException(status_code=500, detail="Failed to add message to the database")
            print(f"User message saved successfully: {user_message_data}")
            # 2. Get conversation history
            print(f"Fetching conversation history for conversation ID: {conversation_id}")
            conversation_history = await get_conversation_history_for_gemini(conversation_id)
            if not conversation_history:
                print("No conversation history found")
                raise HTTPException(status_code=404, detail="Conversation history not found")
            print(f"Conversation history fetched successfully: {conversation_history}")

            # 3. Get Gemini response
            print(f"Fetching Gemini response for message content: {msg.content}")
            response = await get_answer_using_gemini(msg.content, history=conversation_history)
            if not response:
                print("No response received from Gemini")
                raise HTTPException(status_code=500, detail="Failed to get response from Gemini")
            if "error" in response:
                print(f"Gemini error: {response['error']}")
                raise HTTPException(status_code=500, detail="Invalid response format from Gemini")
            print(f"Received Gemini response: {response}")

            # get anohter model to correct grammer 
            response_t5 = await get_answer_using_t5(msg.content)

            # 4. Prepare reply message
            print("Preparing bot reply message")
            reply_msg = MessageCreate(
                content=response["reply"],
                sender_id="bot",
                conversation_id=conversation_id,
                reply_to=user_message_data.get("_id")
            )
            print(f"Attempting to save bot reply message: {reply_msg}")
            bot_reply_data = await add_message_to_db(conversation_id, reply_msg)
            if not bot_reply_data:
                print("Failed to add bot reply message to the database")
                raise HTTPException(status_code=500, detail="Failed to add reply message to the database")
            print(f"Bot reply message saved successfully: {bot_reply_data}")


            bot_reply_data["corrections"] = response_t5  #response["corrections"]
            bot_reply_data["content"] = response["reply"]
            bot_reply_data["grammar_score"] = response["rating"]

            # 4. Return the bot’s message
            print(f"Returning bot reply message: {bot_reply_data}")
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
            cursor = self.messages.find({"conversation_id": conversation_id}).sort("timestamp", -1).skip(offset).limit(limit)
            
            messages = await cursor.to_list(length=limit)

            for message in messages:
                message["_id"] = str(message["_id"])

            return [MessageOut(**msg) for msg in messages]
        except Exception as e:
            print(f"An error occurred while fetching conversation history: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch conversation history")

def get_message_service():
    return MessageService()