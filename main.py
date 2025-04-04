from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
import logging
from datetime import datetime
from services.chatbot_service import ChatbotService
from models.message import Message, MessageCreate
from models.conversation import Conversation
from database.database import get_db, init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="English Learning Chatbot API", 
              description="A chatbot API to help users practice English with conversation history and grammar correction")

# Configure CORS for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot service
chatbot_service = ChatbotService()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "English Learning Chatbot API is running"}

# Create a new conversation
@app.post("/conversations/", response_model=Conversation)
async def create_conversation(user_id: str):
    """
    Create a new conversation for a user
    """
    try:
        db = get_db()
        conversation = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        conversation_id = db.create_conversation(conversation)
        print(conversation_id)
        conversation["id"] = conversation_id
        return conversation
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

# Get all conversations for a user
@app.get("/conversations/{user_id}", response_model=List[Conversation])
async def get_conversations(user_id: str):
    """
    Get all conversations for a specific user
    """
    try:
        db = get_db()
        conversations = db.get_conversations_by_user(user_id)
        return conversations
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve conversations: {str(e)}")

# Get a specific conversation
@app.get("/conversations/{user_id}/{conversation_id}", response_model=Conversation)
async def get_conversation(user_id: str, conversation_id: str):
    """
    Get a specific conversation by ID
    """
    try:
        db = get_db()
        conversation = db.get_conversation(conversation_id)
        if not conversation or conversation.get("user_id") != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve conversation: {str(e)}")

# Send a message and get a response
@app.post("/conversations/{conversation_id}/messages/", response_model=Message)
async def send_message(conversation_id: str, message: MessageCreate):
    """
    Send a message to the chatbot and get a response
    """
    try:
        # Get the conversation from the database
        db = get_db()
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Create user message
        user_message = {
            "id": str(len(conversation["messages"]) + 1),
            "content": message.content,
            "sender": "user",
            "timestamp": datetime.now().isoformat()
        }
        
        # Add user message to conversation
        conversation["messages"].append(user_message)
        
        # Get chatbot response
        bot_response = await chatbot_service.get_response(
            message.content, 
            conversation["messages"],
            correct_grammar=message.correct_grammar
        )
        print("bot response is : ", bot_response)
        # Create bot message
        bot_message = {
            "id": str(len(conversation["messages"]) + 1),
            "content": bot_response,
            "sender": "bot",
            "timestamp": datetime.now().isoformat()
        }
        
        # Add bot message to conversation
        conversation["messages"].append(bot_message)
        
        # Update conversation in database
        db.update_conversation(conversation_id, conversation)
        
        return bot_message
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
