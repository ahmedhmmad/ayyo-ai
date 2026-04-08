from app.integrations.llm_adapter import LLMAdapter
from app.services.chat_service import ChatService
from app.services.checkin_service import CheckInService
from app.services.commitment_service import CommitmentService
from app.services.conversation_repository import ConversationRepository
from app.services.guidance_service import GuidanceService
from app.services.longevity_policy import LongevityPolicy
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


memory_service = MemoryService()
conversation_repository = ConversationRepository()
personality_service = PersonalityEnforcementService()
llm_adapter = LLMAdapter()
guidance_service = GuidanceService()
commitment_service = CommitmentService()
checkin_service = CheckInService()
longevity_policy = LongevityPolicy()
chat_service = ChatService(
	memory_service,
	personality_service,
	llm_adapter,
	conversation_repository,
	guidance_service,
	commitment_service,
	checkin_service,
	longevity_policy,
)
