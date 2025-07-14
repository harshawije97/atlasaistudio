from fastapi import APIRouter
from src.endpoints.conversation import router as conversation
from src.endpoints.storage import router as storage
from src.endpoints.vector_storage import router as vector_storage

routers = APIRouter(prefix="/api/v1", tags=["api"])
router_list = [conversation, storage, vector_storage]

for router in router_list:
    routers.include_router(router)
