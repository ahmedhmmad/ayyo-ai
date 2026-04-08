from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.core import CheckInOutcome, CommitmentRecord, CommitmentStatus
from app.services.checkin_service import CheckInService


def _commitment(statement: str) -> CommitmentRecord:
    return CommitmentRecord(
        id=uuid4(),
        userId=uuid4(),
        sessionId=uuid4(),
        statement=statement,
        status=CommitmentStatus.open,
        createdAt=datetime.now(tz=timezone.utc),
    )


def test_checkin_trigger_references_specific_commitment_text() -> None:
    service = CheckInService()
    commitment = _commitment("30-minute evening walks every day")

    prompt = service.generate_for_commitment(commitment)

    assert "30-minute evening walks every day" in prompt.prompt_text
    assert prompt.trigger_event == "commitment_created"


def test_non_completion_followup_uses_recovery_framing() -> None:
    service = CheckInService()
    commitment = _commitment("bedtime by 10:30pm")
    prompt = service.generate_for_commitment(commitment)

    result = service.respond(commitment.user_id, prompt.id, "I missed it", CheckInOutcome.not_complete)

    text = result.follow_up_message.lower()
    assert "recovery" in text or "reset" in text
    for banned in ["lazy", "pathetic", "weak", "failure", "worthless", "punish"]:
        assert banned not in text
