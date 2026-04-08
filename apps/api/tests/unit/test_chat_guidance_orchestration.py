import json
from uuid import uuid4

from app.integrations.llm_adapter import LLMAdapter, LLMConfig
from app.services.chat_service import ChatService
from app.services.conversation_repository import ConversationRepository
from app.services.memory_inference_policy import MemoryInferencePolicy
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


def _build_service() -> ChatService:
    return ChatService(
        memory_service=MemoryService(inference_policy=MemoryInferencePolicy(threshold=0.8)),
        personality_service=PersonalityEnforcementService(),
        llm_adapter=LLMAdapter(LLMConfig(api_key="k", base_url="u", model="m")),
        conversation_repository=ConversationRepository(),
    )


def test_chat_uses_guidance_service_for_plan_prompts() -> None:
    service = _build_service()
    user_id = uuid4()
    session_id = uuid4()

    chunks = service.stream_response(user_id, session_id, "build me a 3 day plan")

    payload = json.loads("".join(chunk.token for chunk in chunks))
    assert payload["type"] == "guidance_plan"
    assert len(payload["steps"]) == 3


def test_chat_revision_prompt_adapts_prior_guidance_context() -> None:
    service = _build_service()
    user_id = uuid4()
    session_id = uuid4()

    service.stream_response(user_id, session_id, "create a beginner plan")
    revised = service.stream_response(user_id, session_id, "revise it for 20 minutes")

    payload = json.loads("".join(chunk.token for chunk in revised))
    assert payload["type"] == "guidance_plan"
    assert "adapted" in payload["title"].lower()
    assert "20 minutes" in json.dumps(payload).lower()
