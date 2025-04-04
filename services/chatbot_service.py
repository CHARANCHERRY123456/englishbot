import google.generativeai as genai
from typing import List, Dict
import logging
from dotenv import load_dotenv
load_dotenv()
import os

# Configure logging
logger = logging.getLogger(__name__)

# ✅ Configure the API key (no need for a client object)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Load the model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")


class ChatbotService:
    async def get_response(self, user_input: str, conversation_history: List[Dict], correct_grammar: bool = True) -> str:
        try:
            # Optional: add conversation history formatting here if needed
            response = model.generate_content(user_input)
            return response.text
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {e}")
            return "I'm sorry, I encountered an error while processing your message. Please try again later."

    def _format_conversation_history(self, conversation_history: List[Dict]) -> str:
        """
        Format the conversation history for the model.
        """
        recent_history = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        formatted = ""
        
        for message in recent_history:
            sender = "User" if message["sender"] == "user" else "Assistant"
            formatted += f"{sender}: {message['content']}\n"
        
        return formatted
