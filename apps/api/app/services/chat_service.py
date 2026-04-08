from uuid import UUID, uuid4

from app.integrations.llm_adapter import LLMAdapter
from app.schemas.core import MemorySourceType, StreamChunk
from app.services.conversation_repository import ConversationRepository
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


class ChatService:
    def __init__(
        self,
        memory_service: MemoryService,
        personality_service: PersonalityEnforcementService,
        llm_adapter: LLMAdapter,
        conversation_repository: ConversationRepository,
    ) -> None:
        self.memory_service = memory_service
        self.personality_service = personality_service
        self.llm_adapter = llm_adapter
        self.conversation_repository = conversation_repository

    def stream_response(self, user_id: UUID, session_id: UUID, message: str) -> list[StreamChunk]:
        _ = self.memory_service.list_records(user_id)
        self.conversation_repository.append_message(session_id, user_id, "user", message)
        tokens = self.llm_adapter.stream_chat(message)
        message_id = uuid4()
        chunks: list[StreamChunk] = []
        assistant_parts: list[str] = []
        for idx, token in enumerate(tokens):
            text = self.personality_service.enforce(token)
            assistant_parts.append(text)
            chunks.append(
                StreamChunk(
                    sessionId=session_id,
                    messageId=message_id,
                    token=text,
                    done=idx == len(tokens) - 1,
                )
            )

        self.conversation_repository.append_message(
            session_id,
            user_id,
            "assistant",
            "".join(assistant_parts),
        )

        self.memory_service.create_record(
            user_id=user_id,
            category="health_goal",
            key="latest_message",
            value=message,
            source_type=MemorySourceType.explicit,
            confidence_score=1.0,
        )
        return chunks
