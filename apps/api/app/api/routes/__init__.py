from fastapi import APIRouter

from app.api.routes.checkins import router as checkins_router
from app.api.routes.memory import router as memory_router
from app.api.routes.sessions import router as sessions_router
from app.api.sse.chat_stream import router as chat_stream_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(chat_stream_router)
api_router.include_router(sessions_router)
api_router.include_router(memory_router)
api_router.include_router(checkins_router)

