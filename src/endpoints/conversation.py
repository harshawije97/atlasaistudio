from fastapi import APIRouter, HTTPException
from src.service.conversation_init import chat_event_handler
from src.service.data_analysis import data_analysis_chain_event_handler
from src.service.qna_generation import chat_qna_generate_handler
from src.service.regular_conversation import chat_chain_event_handler
from src.utils.data_model import MessageModel, NewMessageModel

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/new")
async def new_conversation(data: NewMessageModel):
    try:
        return await chat_event_handler(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Continue with regular conversation
@router.post("/{conversation_id}/continue/regular")
async def continue_regular_conversation(conversation_id: str, data: MessageModel):
    try:
        return await chat_chain_event_handler(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Continue with Q & A builder
@router.post("/{conversation_id}/continue/qna")
async def continue_qna_conversation(conversation_id: str, data: MessageModel):
    try:
        return await chat_qna_generate_handler(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Continue with data analysis conversation
@router.post("/{conversation_id}/continue/qna")
async def continue_analysis_conversation(conversation_id: str, data: MessageModel):
    try:
        return await data_analysis_chain_event_handler(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
