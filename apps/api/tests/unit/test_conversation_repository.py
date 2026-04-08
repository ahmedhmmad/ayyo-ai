from uuid import uuid4

from app.services.conversation_repository import ConversationRepository


def test_conversation_repository_persists_and_filters_by_user() -> None:
    repository = ConversationRepository()
    session_id = uuid4()
    owner_id = uuid4()
    other_id = uuid4()

    repository.append_message(session_id, owner_id, "user", "hello")
    repository.append_message(session_id, other_id, "user", "hidden")

    owner_messages = repository.list_messages_for_user(session_id, owner_id)
    assert len(owner_messages) == 1
    assert owner_messages[0].content == "hello"
