from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from message.models import MessageModel
from message.schemas import MessageCreate , MessageOut
from message.services import MessageService, get_message_service

router = APIRouter()


@router.post("/{conversation_id}/message", response_model=MessageOut)
async def send_message(
    conversation_id: str,
    msg: MessageCreate,
    service: MessageService = Depends(get_message_service)
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
    service: MessageService = Depends(get_message_service)
):
    """
    Get conversation history
    """
    try:
        return await service.get_conversation_history(conversation_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
