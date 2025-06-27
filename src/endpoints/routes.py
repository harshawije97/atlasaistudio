from fastapi import APIRouter
from src.endpoints.conversation import router as conversation

routers = APIRouter(prefix="/api/v1", tags=["api"])
router_list = [conversation]

for router in router_list:
    routers.include_router(router)