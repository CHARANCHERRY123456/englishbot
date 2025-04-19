from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from conversation.schemas import ConversationCreate, ConversationOut, MessageCreate, MessageOut
from conversation.services import ConversationService, get_conversation_service

router = APIRouter()

@router.post("/", response_model=ConversationOut)
async def create_conversation(
    data: ConversationCreate,
    service: ConversationService = Depends(get_conversation_service)
):
    """
    Create a new conversation
    """
    try:
        print("Creating conversation with data:", data)
        conversation =  await service.create_conversation(data)
        print(conversation)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/messages", response_model=MessageOut)
async def send_message(
    conversation_id: str,
    msg: MessageCreate,
    service: ConversationService = Depends(get_conversation_service)
):
    """
    Send a message to a conversation
    """
    try:
        return await service.add_message(conversation_id, msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}/history", response_model=List[MessageOut])
async def get_history(
    conversation_id: str,
    limit: int = 20,
    offset: int = 0,
    service: ConversationService = Depends(get_conversation_service)
):
    """
    Get conversation history
    """
    try:
        return await service.get_conversation_history(conversation_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
