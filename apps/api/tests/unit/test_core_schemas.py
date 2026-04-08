from uuid import uuid4

from app.schemas.core import ChatRequest, MemoryRecord


def test_chat_request_validates_message() -> None:
    request = ChatRequest(sessionId=uuid4(), message="train")
    assert request.message == "train"


def test_memory_record_bounds() -> None:
    record = MemoryRecord(
        id=uuid4(),
        user_id=uuid4(),
        category="health_goal",
        key="goal",
        value="sleep 8h",
        source_type="explicit",
        confidence_score=1.0,
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        is_active=True,
    )
    assert record.confidence_score == 1.0
