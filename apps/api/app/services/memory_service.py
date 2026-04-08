from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.core import MemoryRecord, MemorySourceType


class MemoryService:
    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def list_records(self, user_id: UUID) -> list[MemoryRecord]:
        return [r for r in self._records if r.user_id == user_id and r.is_active]

    def create_record(
        self,
        user_id: UUID,
        category: str,
        key: str,
        value: str,
        source_type: MemorySourceType,
        confidence_score: float,
    ) -> MemoryRecord:
        now = datetime.now(tz=timezone.utc)
        record = MemoryRecord(
            id=uuid4(),
            user_id=user_id,
            category=category,
            key=key,
            value=value,
            source_type=source_type,
            confidence_score=confidence_score,
            created_at=now,
            updated_at=now,
            is_active=True,
        )
        self._records.append(record)
        return record

    def update_record(self, user_id: UUID, record_id: UUID, value: str) -> MemoryRecord:
        for idx, record in enumerate(self._records):
            if record.id == record_id and record.user_id == user_id:
                updated = record.model_copy(update={"value": value, "updated_at": datetime.now(tz=timezone.utc)})
                self._records[idx] = updated
                return updated
        raise KeyError("memory record not found")

    def delete_record(self, user_id: UUID, record_id: UUID) -> None:
        for idx, record in enumerate(self._records):
            if record.id == record_id and record.user_id == user_id:
                self._records[idx] = record.model_copy(update={"is_active": False})
                return
        raise KeyError("memory record not found")

    def reset_memory(self, user_id: UUID) -> None:
        for idx, record in enumerate(self._records):
            if record.user_id == user_id:
                self._records[idx] = record.model_copy(update={"is_active": False})
