from fastapi import APIRouter
from src.endpoints.conversation import router as conversation
from src.endpoints.storage import router as storage

routers = APIRouter(prefix="/api/v1", tags=["api"])
router_list = [conversation, storage]

for router in router_list:
    routers.include_router(router)
