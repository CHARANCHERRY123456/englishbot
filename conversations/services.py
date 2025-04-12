from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from .schemas import *
from conversations.model import MessageModel, ConversationModel
from conversations.gemini_services import GeminiService
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os

class ConversationService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.messages = db["chatdb"]["messages"]
        self.conversations = db["chatdb"]["conversations"]
        self.gemini = GeminiService(api_key=os.getenv("GEMINI_API_KEY"))
    def extract_from_reply(self,reply_text: str):
        result = {
            "corrected": "",
            "suggestion": "",
            "rating": 0.0,
            "reply": ""
        }

        for line in reply_text.splitlines():
            if "Correct grammar:" in line:
                result["corrected"] = line.split(":", 1)[1].strip().strip('"')
            elif "Better version:" in line:
                result["suggestion"] = line.split(":", 1)[1].strip()
            elif "Fluency" in line or "Rating" in line:
                try:
                    result["rating"] = float(line.split(":")[-1].split("/")[0].strip())
                except:
                    result["rating"] = 0.0
            elif "Natural reply:" in line:
                result["reply"] = line.split(":", 1)[1].strip().strip('"')

        return result

    async def create_conversation(self, data: ConversationCreate) -> ConversationOut:
        convo = ConversationModel(**data.dict())
        result = await self.conversations.insert_one(convo.dict())
        convo_dict = convo.dict()
        convo_dict["_id"] = str(result.inserted_id)
        return convo_dict
    
    async def add_message(self, conv_id: str, msg: MessageCreate):
        try:
            # Get recent message history
            history_cursor = self.messages.find(
                {"conversation_id": conv_id},
                sort=[("timestamp", -1)],
                limit=5
            )
            history = [doc async for doc in history_cursor]
            history_texts = [m["content"] for m in reversed(history)]

            # Call Gemini
            ai_result = await self.gemini.send(msg.content, history_texts)

            # Parse response
            corrected = ai_result.get("corrected", "-")
            suggestion = ai_result.get("suggestion", "-")
            rating = ai_result.get("rating", 0.0)
            reply_text = ai_result.get("reply", "I'm here to help!")

            # Save user message
            msg_doc = MessageModel(
                **msg.dict(),
                conversation_id=conv_id,
                corrections=[{
                    "original": msg.content,
                    "suggestion": corrected
                }],
                grammar_score=rating,
                rating=rating,
                timestamp=datetime.utcnow()
            ).dict()

            insert_user = await self.messages.insert_one(msg_doc)

            # Update conversation last activity
            await self.conversations.update_one(
                {"_id": ObjectId(conv_id)},
                {"$set": {"last_message_at": msg_doc["timestamp"]}}
            )

            # Save bot reply
            bot_doc = MessageModel(
                content=reply_text,
                sender_id="bot",
                conversation_id=conv_id,
                timestamp=datetime.utcnow()
            ).dict()

            insert_bot = await self.messages.insert_one(bot_doc)

            return {
                "user_message": {
                    "_id": str(insert_user.inserted_id),
                    "content": msg.content,
                    "corrections": [{
                        "original": msg.content,
                        "suggestion": corrected
                    }],
                    "grammar_score": rating,
                    "rating": rating,
                    "timestamp": msg_doc["timestamp"]
                },
                "bot_reply": {
                    "_id": str(insert_bot.inserted_id),
                    "content": reply_text,
                    "sender_id": "bot",
                    "timestamp": bot_doc["timestamp"]
                }
            }

        except Exception as e:
            print(f"Error while processing message: {e}")
            return {
                "error": str(e),
                "message": "Something went wrong while processing your message. Please try again."
            }


    async def get_conversation_history(self, conv_id: str, limit: int = 20, offset: int = 0):
        cursor = self.messages.find({"conversation_id": conv_id}).skip(offset).limit(limit).sort("timestamp", 1)
        print(len(cursor))
        return [self._serialize(doc) async for doc in cursor]

    def _serialize(self, doc):
        doc["_id"] = str(doc["_id"])
        return doc
