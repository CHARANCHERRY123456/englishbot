from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi import HTTPException
from .schemas import *
from conversations.model import MessageModel, ConversationModel
from conversations.gemini_services import GeminiService
import json
from datetime import datetime
from dotenv import load_dotenv
import re
load_dotenv()
import os

class ConversationService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.messages = db["chatdb"]["messages"]
        self.conversations = db["chatdb"]["conversations"]
        self.gemini = GeminiService(api_key=os.getenv("GEMINI_API_KEY"))

    async def create_conversation(self, data: ConversationCreate) -> ConversationOut:
        convo = ConversationModel(**data.dict())
        result = await self.conversations.insert_one(convo.dict())
        convo_dict = convo.dict()
        convo_dict["_id"] = str(result.inserted_id)
        return convo_dict

    async def add_message(self, conv_id: str, msg: MessageCreate):
        try:
            # 1. Get message history (last 5)
            history_cursor = self.messages.find(
                {"conversation_id": conv_id},
                sort=[("timestamp", -1)],
                limit=5
            )
            history = [doc async for doc in history_cursor]
            history_texts = [m["content"] for m in reversed(history)]

            # 2. Send to Gemini
            ai_result = self.gemini.send(msg.content, history_texts)  # add await if needed
            ai_res = ai_result["reply"]

            # 3. Clean and parse JSON
            cleaned_res = re.sub(r"```json\n|```", "", ai_res)
            ai_json = json.loads(cleaned_res)
            print(type(ai_json), ai_json)

            # 5. Create user message doc
            msg_doc = MessageModel(
                **msg.dict(),
                conversation_id=conv_id,
                corrections=ai_json["corrections"],
                grammar_score=ai_json["rating"],
            ).dict()


            # 6. Insert user message
            insert = await self.messages.insert_one(msg_doc)

            # 7. Update conversation's last message time
            await self.conversations.update_one(
                {"_id": ObjectId(conv_id)},
                {"$set": {"last_message_at": msg_doc["timestamp"]}}
            )

            # 8. Insert bot reply
            bot_reply = MessageModel(
                content=ai_json["reply"],
                sender_id="bot",
                conversation_id=conv_id
            ).dict()

            await self.messages.insert_one(bot_reply)

            # 9. Return inserted message with ID
            msg_doc["_id"] = str(insert.inserted_id)
            return msg_doc

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")


    async def get_conversation_history(self, conv_id: str, limit: int = 20, offset: int = 0):
        cursor = self.messages.find({"conversation_id": conv_id}).skip(offset).limit(limit).sort("timestamp", 1)
        return [self._serialize(doc) async for doc in cursor]

    def _serialize(self, doc):
        doc["_id"] = str(doc["_id"])
        return doc
