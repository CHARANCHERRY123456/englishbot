# routes/chat.py
from fastapi import APIRouter, Depends
from models.user import ChatInput
from services.auth import get_current_user
from services.chat import process_message

router = APIRouter()

@router.post("/chat")
async def chat(input: ChatInput):
    corrected_message = process_message(input.message)
    return {
        "original": input.message,
        "corrected": corrected_message,
        "message": "Great effort! Here’s the improved version."
    }