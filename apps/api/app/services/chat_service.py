from uuid import UUID, uuid4

from app.integrations.llm_adapter import LLMAdapter
from app.schemas.core import StreamChunk
from app.services.checkin_service import CheckInService
from app.services.commitment_service import CommitmentService
from app.services.conversation_repository import ConversationRepository
from app.services.guidance_service import GuidanceService
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


class ChatService:
    def __init__(
        self,
        memory_service: MemoryService,
        personality_service: PersonalityEnforcementService,
        llm_adapter: LLMAdapter,
        conversation_repository: ConversationRepository,
        guidance_service: GuidanceService | None = None,
        commitment_service: CommitmentService | None = None,
        checkin_service: CheckInService | None = None,
    ) -> None:
        self.memory_service = memory_service
        self.personality_service = personality_service
        self.llm_adapter = llm_adapter
        self.conversation_repository = conversation_repository
        self.guidance_service = guidance_service or GuidanceService()
        self.commitment_service = commitment_service or CommitmentService()
        self.checkin_service = checkin_service or CheckInService()

    def stream_response(self, user_id: UUID, session_id: UUID, message: str) -> list[StreamChunk]:
        history_messages = self.conversation_repository.list_messages_for_user(session_id=session_id, user_id=user_id)
        history_assistant = [m.content for m in history_messages if m.role == "assistant"]
        records = self.memory_service.list_records(user_id)
        memory_context = " | ".join(f"{record.key}: {record.value}" for record in records)
        prompt = message if not memory_context else f"{message}\nMEMORY: {memory_context}"

        self.conversation_repository.append_message(session_id, user_id, "user", message)
        commitment = self.commitment_service.capture_from_message(user_id=user_id, session_id=session_id, message=message)
        if commitment is not None:
            self.checkin_service.generate_for_commitment(commitment)

        if self.guidance_service.should_handle(message):
            guidance_payload = self.guidance_service.build_guidance(
                user_id=user_id,
                session_id=session_id,
                message=message,
                memory_records=records,
                history=history_assistant,
            )
            tokens = [guidance_payload]
        else:
            tokens = self.llm_adapter.stream_chat(prompt)
        message_id = uuid4()
        chunks: list[StreamChunk] = []
        assistant_parts: list[str] = []
        for idx, token in enumerate(tokens):
            if token.lstrip().startswith("{"):
                text = token
            else:
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

        self.memory_service.ingest_message(user_id=user_id, message=message)
        return chunks
