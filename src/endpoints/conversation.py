from fastapi import APIRouter, HTTPException
from src.service.conversation_init import chat_event_handler
from src.utils.data_model import MessageModel, NewMessageModel

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.post("/new")
async def new_conversation(data: NewMessageModel):
    try:
        return await chat_event_handler(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{conversation_id}/continue/regular")
async def continue_conversation(data: MessageModel):
    return