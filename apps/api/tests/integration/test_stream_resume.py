from uuid import uuid4

from app.schemas.core import StreamChunk
from app.services.stream_resume_service import StreamResumeService


def test_resume_returns_remaining_chunks() -> None:
    session_id = uuid4()
    message_id = uuid4()
    chunks = [
        StreamChunk(sessionId=session_id, messageId=message_id, token="a", done=False),
        StreamChunk(sessionId=session_id, messageId=message_id, token="b", done=True),
    ]
    service = StreamResumeService()
    resumed = service.resume(chunks, 1)
    assert len(resumed) == 1
    assert resumed[0].token == "b"
