from app.integrations.llm_adapter import LLMAdapter
from app.services.chat_service import ChatService
from app.services.conversation_repository import ConversationRepository
from app.services.memory_service import MemoryService
from app.services.personality_enforcement_service import PersonalityEnforcementService


memory_service = MemoryService()
conversation_repository = ConversationRepository()
personality_service = PersonalityEnforcementService()
llm_adapter = LLMAdapter()
chat_service = ChatService(memory_service, personality_service, llm_adapter, conversation_repository)
