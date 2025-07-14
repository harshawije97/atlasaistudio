from typing import Dict, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.service.get_all_vector_indexes import get_all_vector_indexes

router = APIRouter(prefix="/vector_storage", tags=["db_storage"])


# Get all clusters
@router.get("/get/all")
async def get_all_indexes():
    try:
        indexes_list = get_all_vector_indexes()
        return JSONResponse(
            content={"status": "success", "data": indexes_list},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Index by name


@router.get("/get/{index_name}")
async def get_index(index_name: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Save data to index
@router.post("/{index_name}/save")
async def save_data(data: Dict[str, List[str]]):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
