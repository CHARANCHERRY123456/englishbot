# routes/conversation.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from models.conversation import Conversation
from models.message import MessageCreate, Message
from bson import ObjectId
from database.mongo import get_db
from services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/start", response_model=Conversation)
async def start_conversation(user_id: str, type: str = "lifelong"):
    db = await get_db()
    now = datetime.now().isoformat()
    title = "Lifelong Chat" if type == "lifelong" else f"Daily Chat | {now[:10]}"

    new_conv = {
        "user_id": user_id,
        "title": title,
        "type": type,
        "created_at": now,
        "messages": []
    }

    result = await db.conversations.insert_one(new_conv)
    new_conv["id"] = str(result.inserted_id)
    return new_conv


@router.post("/conversations/", response_model=Conversation)
async def create_conversation(user_id: str):
    try:
        print("Arey bor i am in the precipus commit")
        db =await get_db()
        conversation = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        conversation_id =await db.create_conversation(conversation)
        conversation["id"] = str(conversation_id)  # ✅ Add id
        return conversation
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{user_id}", response_model=List[Conversation])
async def get_conversations(user_id: str):
    try:
        db = await get_db()
        conversations_cursor = db["conversations"].find({"user_id": user_id})
        conversations = await conversations_cursor.to_list(length=100)

        for c in conversations:
            c["id"] = str(c["_id"])  # Map _id to id
            del c["_id"]

        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/conversations/{user_id}/{conversation_id}", response_model=Conversation)
async def get_conversation(user_id: str, conversation_id: str):
    try:
        db = await get_db()
        conversation = await db["conversations"].find_one({"_id": ObjectId(conversation_id)})

        if not conversation or conversation.get("user_id") != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")

        conversation["id"] = str(conversation["_id"])
        del conversation["_id"]

        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/conversations/{conversation_id}/messages/", response_model=Message)
async def send_message(conversation_id: str, message: MessageCreate):
    try:
        db = await get_db()
        collection = db["conversations"]

        conversation = await collection.find_one({"_id": ObjectId(conversation_id)})
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

        await collection.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"messages": conversation["messages"]}}
        )

        return bot_msg
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

