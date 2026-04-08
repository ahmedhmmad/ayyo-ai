from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.core import MemoryCategory, MemoryRecord, MemorySourceType
from app.services.memory_inference_policy import MemoryInferencePolicy


class MemoryService:
    def __init__(self, inference_policy: MemoryInferencePolicy | None = None) -> None:
        self._records: list[MemoryRecord] = []
        self.inference_policy = inference_policy or MemoryInferencePolicy()

    def list_records(self, user_id: UUID) -> list[MemoryRecord]:
        return [r for r in self._records if r.user_id == user_id and r.is_active]

    def create_record(
        self,
        user_id: UUID,
        category: MemoryCategory | str,
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

    def ingest_message(self, user_id: UUID, message: str) -> MemoryRecord | None:
        inferred = self._infer_memory(message)
        if inferred is None:
            return None

        category, key, value, source_type, confidence = inferred
        if not self.inference_policy.should_store(source_type, confidence):
            return None

        existing = self._find_active_record(user_id=user_id, category=category, key=key)
        if existing is not None:
            return self.update_record(user_id=user_id, record_id=existing.id, value=value)

        return self.create_record(
            user_id=user_id,
            category=category,
            key=key,
            value=value,
            source_type=source_type,
            confidence_score=confidence,
        )

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

    def _find_active_record(self, user_id: UUID, category: MemoryCategory, key: str) -> MemoryRecord | None:
        for record in self._records:
            if record.user_id == user_id and record.category == category and record.key == key and record.is_active:
                return record
        return None

    def _infer_memory(
        self, message: str
    ) -> tuple[MemoryCategory, str, str, MemorySourceType, float] | None:
        text = message.strip()
        if not text:
            return None

        lowered = text.lower()
        if "goal" in lowered:
            value = self._extract_after_keyword(text, lowered, "goal")
            return (MemoryCategory.health_goal, "goal", value or text, MemorySourceType.explicit, 1.0)

        if "struggle" in lowered:
            value = self._extract_after_keyword(text, lowered, "struggle")
            return (MemoryCategory.struggle, "struggle", value or text, MemorySourceType.explicit, 1.0)

        if "priority" in lowered:
            value = self._extract_after_keyword(text, lowered, "priority")
            return (MemoryCategory.health_priority, "priority", value or text, MemorySourceType.explicit, 1.0)

        return (MemoryCategory.active_routine, "routine", text, MemorySourceType.implicit, 0.7)

    def _extract_after_keyword(self, text: str, lowered: str, keyword: str) -> str:
        start = lowered.find(keyword)
        if start < 0:
            return text
        return text[start + len(keyword) :].strip(" :.-")
