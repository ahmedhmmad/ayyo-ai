import json
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import AuthContext, get_auth_context
from app.schemas.core import ChatRequest
from app.services.chat_service import ChatService
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService
from app.integrations.llm_adapter import LLMAdapter


router = APIRouter(prefix="/knox", tags=["knox-sse"])


@router.post("/chat/stream")
def stream_chat(request: ChatRequest, auth: AuthContext = Depends(get_auth_context)) -> StreamingResponse:
    service = ChatService(MemoryService(), PersonalityEnforcementService(), LLMAdapter())
    chunks = service.stream_response(auth.user_id, UUID(str(request.session_id)), request.message)

    def event_source():
        for chunk in chunks:
            payload = json.dumps(chunk.model_dump(by_alias=True, mode="json"))
            yield f"data: {payload}\n\n"

    return StreamingResponse(event_source(), media_type="text/event-stream")
