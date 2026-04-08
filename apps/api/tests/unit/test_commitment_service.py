from uuid import uuid4

from app.schemas.core import CommitmentStatus
from app.services.commitment_service import CommitmentService


def test_commitment_capture_and_open_listing() -> None:
    service = CommitmentService()
    user_id = uuid4()
    session_id = uuid4()

    created = service.capture_from_message(user_id, session_id, "I commit to 30-minute evening walks")

    assert created is not None
    assert "30-minute evening walks" in created.statement
    assert len(service.list_open_commitments(user_id)) == 1


def test_commitment_status_transitions_remove_from_open() -> None:
    service = CommitmentService()
    user_id = uuid4()
    session_id = uuid4()

    created = service.capture_from_message(user_id, session_id, "I commit to bedtime by 10:30pm")
    assert created is not None

    updated = service.update_status(user_id, created.id, CommitmentStatus.completed)
    assert updated.status == CommitmentStatus.completed
    assert service.list_open_commitments(user_id) == []
