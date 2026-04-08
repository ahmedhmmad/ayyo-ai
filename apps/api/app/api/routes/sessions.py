from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import AuthContext, get_auth_context
from app.schemas.core import ConversationMessageOut
from app.services.conversation_repository import ConversationRepository


router = APIRouter(prefix="/knox/sessions", tags=["knox-sessions"])


@router.get("/{session_id}/messages", response_model=list[ConversationMessageOut])
def get_session_messages(session_id: UUID, auth: AuthContext = Depends(get_auth_context)) -> list[ConversationMessageOut]:
    repository = ConversationRepository()
    return repository.list_messages_for_user(session_id=session_id, user_id=auth.user_id)
