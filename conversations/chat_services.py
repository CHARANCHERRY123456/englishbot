from conversations.db_services import ConversationService
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

class ContextualReplyService:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.db_client = db_client
        self.conversation_service = ConversationService(db_client)
        
    async def generate_reply(self, conversation_id: str, new_message: str):
        """Generate a context-aware reply using Gemini API"""
        try:
            # Get conversation context (last 10 messages)
            context_messages = await self.conversation_service.get_context_messages(conversation_id)
            
            # Generate reply using Gemini API
            reply = await self._call_gemini_api(new_message, context_messages)
            
            return {
                "reply": reply,
                "context_used": [msg["content"] for msg in context_messages[-5:]],
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logging.error(f"Reply generation failed: {str(e)}")
            raise HTTPException(500, detail="Failed to generate reply")

    async def _call_gemini_api(self, new_message: str, context_messages: list):
        """Call Gemini API with formatted conversation history"""
        try:
            headers = {"Content-Type": "application/json"}
            
            # Format conversation history for Gemini
            history = [
                {
                    "role": "user" if msg["sender_id"] != "system" else "model",
                    "parts": [{"text": msg["content"]}]
                }
                for msg in context_messages
            ]
            
            # Add new message to the history
            history.append({
                "role": "user",
                "parts": [{"text": new_message}]
            })
            
            payload = {
                "contents": history,
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95
                }
            }

            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    GEMINI_API_URL,
                    json=payload,
                    headers=headers
                )
                
                response.raise_for_status()
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
                
        except httpx.HTTPStatusError as e:
            logging.error(f"Gemini API error: {e.response.text}")
            return "I'm having trouble generating a response right now."
        except httpx.ReadTimeout:
            logging.error("Gemini API request timed out")
            return "The response is taking longer than expected. Please try again."
        except KeyError:
            logging.error("Unexpected response format from Gemini API")
            return "I couldn't process the response properly. Please rephrase your message."
