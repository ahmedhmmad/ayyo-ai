from collections import defaultdict
from dataclasses import dataclass
from uuid import UUID

from app.schemas.core import ConversationMessageOut


@dataclass
class _ConversationMessage:
    session_id: UUID
    user_id: UUID
    role: str
    content: str


class ConversationRepository:
    _messages: dict[UUID, list[_ConversationMessage]] = defaultdict(list)

    def append_message(self, session_id: UUID, user_id: UUID, role: str, content: str) -> None:
        self._messages[session_id].append(
            _ConversationMessage(session_id=session_id, user_id=user_id, role=role, content=content)
        )

    def list_messages_for_user(self, session_id: UUID, user_id: UUID) -> list[ConversationMessageOut]:
        messages = self._messages.get(session_id, [])
        filtered = [m for m in messages if m.user_id == user_id]
        return [
            ConversationMessageOut(
                sessionId=m.session_id,
                userId=m.user_id,
                role=m.role,
                content=m.content,
            )
            for m in filtered
        ]
