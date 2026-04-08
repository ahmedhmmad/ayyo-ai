import json
from uuid import uuid4

from app.integrations.llm_adapter import LLMAdapter, LLMConfig
from app.services.chat_service import ChatService
from app.services.conversation_repository import ConversationRepository
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


def _service() -> ChatService:
    return ChatService(
        memory_service=MemoryService(),
        personality_service=PersonalityEnforcementService(),
        llm_adapter=LLMAdapter(LLMConfig(api_key="k", base_url="u", model="m")),
        conversation_repository=ConversationRepository(),
    )


def _join(chunks) -> str:
    return "".join(chunk.token for chunk in chunks)


def test_chat_pipeline_adds_longevity_framing_for_training_topic() -> None:
    service = _service()
    out = _join(service.stream_response(uuid4(), uuid4(), "How should I structure training?"))
    assert "long-term" in out.lower() or "years" in out.lower() or "longevity" in out.lower()


def test_chat_pipeline_keeps_guidance_json_unmodified() -> None:
    service = _service()
    out = _join(service.stream_response(uuid4(), uuid4(), "build me a plan"))

    parsed = json.loads(out)
    assert parsed["type"] == "guidance_plan"
