from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from conversations.services import ConversationService
from conversations.schemas import *

router = APIRouter(prefix="/conversations", tags=["Conversations"])

def get_db():
    return AsyncIOMotorClient("mongodb://localhost:27017")

def get_service():
    return ConversationService(get_db())

@router.post("/", response_model=ConversationOut)
async def create_conversation(data: ConversationCreate, service: ConversationService = Depends(get_service)):
    return await service.create_conversation(data)

@router.post("/{conversation_id}/messages", response_model=MessageOut)
async def send_message(conversation_id: str, msg: MessageCreate, service: ConversationService = Depends(get_service)):
    try:
        return await service.add_message(conversation_id, msg)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.get("/{conversation_id}/history", response_model=List[MessageOut])
async def get_history(conversation_id: str, limit: int = 20, offset: int = 0, service: ConversationService = Depends(get_service)):
    return await service.get_conversation_history(conversation_id, limit, offset)