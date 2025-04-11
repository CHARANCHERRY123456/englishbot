from fastapi import APIRouter, Depends, HTTPException
from conversations.model import MessageBase, ConversationCreate, ConversationResponse
from conversations.chat_services import ConversationService
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(tags=["conversations"])

def get_db_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient("mongodb://localhost:27017")

@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    conversation: ConversationCreate,
    service: ConversationService = Depends(lambda: ConversationService(get_db_client()))
):
    try:
        conv_response = ConversationResponse(**conversation.dict())
        return await service.create_conversation(conv_response)
    except Exception as e:
        raise HTTPException(500, f"Conversation creation failed: {str(e)}")

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: str,
    message: MessageBase,
    service: ConversationService = Depends(lambda: ConversationService(get_db_client()))
):
    try:
        message.conversation_id = conversation_id
        return await service.add_message(message)
    except Exception as e:
        raise HTTPException(500, f"Message send failed: {str(e)}")

@router.get("/{conversation_id}/history")
async def get_history(
    conversation_id: str,
    limit: int = 20,
    offset: int = 0,
    service: ConversationService = Depends(lambda: ConversationService(get_db_client()))
):
    return await service.get_conversation_history(conversation_id, limit, offset)
