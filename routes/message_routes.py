from fastapi import APIRouter, HTTPException
from models.message import Message, MessageCreate
from database.mongo_database import MongoDatabase
from services.chatbot_service import ChatbotService
from datetime import datetime

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/{conversation_id}/messages", response_model=Message)
async def send_message(conversation_id: str, message: MessageCreate):
    try:
        conversation = await MongoDatabase.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        user_msg = {
            "id": str(len(conversation["messages"]) + 1),
            "content": message.content,
            "sender": "user",
            "timestamp": datetime.utcnow().isoformat()
        }

        conversation["messages"].append(user_msg)

        bot_response = await chatbot_service.get_response(
            message.content + "also give the rating of the current message and if you suggest any new grammer and message optimisation then just do it",
            conversation["messages"],
            correct_grammar=message.correct_grammar
        )

        bot_msg = {
            "id": str(len(conversation["messages"]) + 1),
            "content": bot_response,
            "sender": "bot",
            "timestamp": datetime.utcnow().isoformat()
        }

        conversation["messages"].append(bot_msg)

        await MongoDatabase.update_conversation(conversation_id, conversation)

        return bot_msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
