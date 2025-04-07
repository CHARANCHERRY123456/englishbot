# routes/conversation.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from models.conversation import Conversation
from models.message import MessageCreate, Message
from database.mongo import get_db
from services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/conversations/", response_model=Conversation)
async def create_conversation(user_id: str):
    try:
        db = get_db()
        conversation = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        conversation_id = db.create_conversation(conversation)
        conversation["id"] = str(conversation_id)  # ✅ Add id
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}", response_model=List[Conversation])
async def get_conversations(user_id: str):
    try:
        db = get_db()
        conversations = db.get_conversations_by_user(user_id)

        for c in conversations:
            c["id"] = str(c["_id"])  # Map _id to id
            del c["_id"]

        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}/{conversation_id}", response_model=Conversation)
async def get_conversation(user_id: str, conversation_id: str):
    try:
        db = get_db()
        conversation = db.get_conversation(conversation_id)
        if not conversation or conversation.get("user_id") != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        conversation["id"] = str(conversation["_id"])  # ✅ Fix here too
        del conversation["_id"]

        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversations/{conversation_id}/messages/", response_model=Message)
async def send_message(conversation_id: str, message: MessageCreate):
    try:
        db = get_db()
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        user_msg = {
            "id": str(len(conversation["messages"]) + 1),
            "content": message.content,
            "sender": "user",
            "timestamp": datetime.now().isoformat()
        }
        conversation["messages"].append(user_msg)

        bot_response = await chatbot_service.get_response(
            message.content, conversation["messages"],
            correct_grammar=message.correct_grammar
        )

        bot_msg = {
            "id": str(len(conversation["messages"]) + 1),
            "content": bot_response,
            "sender": "bot",
            "timestamp": datetime.now().isoformat()
        }
        conversation["messages"].append(bot_msg)

        db.update_conversation(conversation_id, conversation)

        return bot_msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
