from uuid import uuid4

from app.integrations.llm_adapter import LLMAdapter, LLMConfig
from app.services.chat_service import ChatService
from app.services.conversation_repository import ConversationRepository
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


def test_chat_service_streams_and_stores_memory() -> None:
    service = ChatService(
        memory_service=MemoryService(),
        personality_service=PersonalityEnforcementService(),
        llm_adapter=LLMAdapter(LLMConfig(api_key="k", base_url="u", model="m")),
        conversation_repository=ConversationRepository(),
    )
    user_id = uuid4()
    session_id = uuid4()
    chunks = service.stream_response(user_id, session_id, "train")
    assert chunks
    assert chunks[-1].done is True
