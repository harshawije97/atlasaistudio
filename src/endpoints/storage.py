from fastapi import APIRouter, HTTPException

from src.utils.data_model import SaveMessageModel

router = APIRouter(prefix="/storage", tags=["db_storage"])


# Save to db
@router.post("/save")
async def save_conversation(data: SaveMessageModel):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get from conversation Id
@router.get("/get/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
