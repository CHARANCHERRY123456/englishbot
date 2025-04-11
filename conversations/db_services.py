# File: app/conversations/services.py
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

class ConversationService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db = db_client.get_database("linguabot")
        self.messages = self.db.messages
        self.conversations = self.db.conversations

    async def get_context_messages(self, conversation_id: str, window_size: int = 10):
        try:
            pipeline = [
                {"$match": {"conversation_id": conversation_id}},
                {"$sort": {"timestamp": -1}},
                {"$limit": window_size},
                {"$project": {"content": 1, "sender_id": 1}}
            ]
            return await self.messages.aggregate(pipeline).to_list(window_size)
        except Exception as e:
            logging.error(f"Context retrieval failed: {str(e)}")
            raise HTTPException(500, "Failed to get conversation context")

class ContextualReplyService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.conversation_service = ConversationService(db_client)
        
    async def generate_reply(self, conversation_id: str, new_message: str):
        try:
            # Get conversation context
            context_messages = await self.conversation_service.get_context_messages(conversation_id)
            
            # Generate reply using Gemini API
            reply = await self._call_gemini_api(new_message, context_messages)
            
            # Return structured response
            return {
                "reply": reply,
                "context_used": [msg["content"] for msg in context_messages[-5:]],
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logging.error(f"Reply generation failed: {str(e)}")
            raise HTTPException(500, "Failed to generate reply")

    async def _call_gemini_api(self, message: str, context: list):
        try:
            headers = {"Content-Type": "application/json"}
            params = {"key": GEMINI_API_KEY}
            
            # Format conversation history
            history = "\n".join([f"{msg['sender_id']}: {msg['content']}" for msg in context])
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"Conversation history:\n{history}\n\nNew message: {message}\nAssistant response:"
                    }]
                }]
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    GEMINI_API_URL,
                    json=payload,
                    headers=headers,
                    params=params
                )
                
                if response.status_code != 200:
                    logging.error(f"Gemini API error: {response.text}")
                    return "I'm having trouble generating a response right now."

                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
                
        except httpx.ReadTimeout:
            logging.error("Gemini API request timed out")
            return "The response is taking longer than expected. Please try again."
        except KeyError:
            logging.error("Unexpected response format from Gemini API")
            return "I couldn't process the response properly. Please rephrase your message."
