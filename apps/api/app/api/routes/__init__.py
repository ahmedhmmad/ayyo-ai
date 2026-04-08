from fastapi import APIRouter

from app.api.sse.chat_stream import router as chat_stream_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(chat_stream_router)

