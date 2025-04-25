from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from conversation.schemas import ConversationCreate, ConversationOut
from conversation.services import ConversationService, get_conversation_service
from auth.dependencies import get_current_user

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

@router.get("/{user_id}", response_model=List[ConversationOut])
async def get_user_conversations(
    user_id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    """
    Get all conversations of a user by user ID
    """
    try:
        print(f"Fetching conversations for user ID: {user_id}")
        return await service.get_conversations_by_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    service: ConversationService = Depends(get_conversation_service)
):
    """
    Delete a conversation by ID
    """
    try:
        print(f"Deleting conversation with ID: {conversation_id}")
        return await service.delete_conversation(conversation_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
