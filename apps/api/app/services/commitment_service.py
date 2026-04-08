from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.core import CommitmentRecord, CommitmentStatus


class CommitmentService:
    def __init__(self) -> None:
        self._records: list[CommitmentRecord] = []

    def capture_from_message(self, user_id: UUID, session_id: UUID, message: str) -> CommitmentRecord | None:
        statement = self._extract_statement(message)
        if statement is None:
            return None

        record = CommitmentRecord(
            id=uuid4(),
            userId=user_id,
            sessionId=session_id,
            statement=statement,
            status=CommitmentStatus.open,
            createdAt=datetime.now(tz=timezone.utc),
        )
        self._records.append(record)
        return record

    def list_open_commitments(self, user_id: UUID) -> list[CommitmentRecord]:
        return [r for r in self._records if r.user_id == user_id and r.status == CommitmentStatus.open]

    def update_status(self, user_id: UUID, commitment_id: UUID, status: CommitmentStatus) -> CommitmentRecord:
        for idx, record in enumerate(self._records):
            if record.id == commitment_id and record.user_id == user_id:
                updated = record.model_copy(update={"status": status})
                self._records[idx] = updated
                return updated
        raise KeyError("commitment not found")

    def get_by_id(self, user_id: UUID, commitment_id: UUID) -> CommitmentRecord:
        for record in self._records:
            if record.id == commitment_id and record.user_id == user_id:
                return record
        raise KeyError("commitment not found")

    def _extract_statement(self, message: str) -> str | None:
        lowered = message.lower()
        marker = "commit to"
        if marker not in lowered:
            return None

        start = lowered.find(marker) + len(marker)
        statement = message[start:].strip(" .")
        return statement or None
