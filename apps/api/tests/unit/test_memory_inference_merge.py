from uuid import uuid4

from app.services.memory_inference_policy import MemoryInferencePolicy
from app.services.memory_service import MemoryService


def test_explicit_memory_updates_existing_record() -> None:
    service = MemoryService(inference_policy=MemoryInferencePolicy(threshold=0.8))
    user_id = uuid4()

    first = service.ingest_message(user_id, "goal lose 10kg")
    assert first is not None

    second = service.ingest_message(user_id, "goal improve sleep quality")
    assert second is not None
    assert second.id == first.id

    records = service.list_records(user_id)
    assert len(records) == 1
    assert records[0].value == "improve sleep quality"


def test_low_confidence_implicit_memory_is_not_stored() -> None:
    service = MemoryService(inference_policy=MemoryInferencePolicy(threshold=0.8))
    user_id = uuid4()

    stored = service.ingest_message(user_id, "goal stay consistent")
    assert stored is not None

    not_stored = service.ingest_message(user_id, "I usually train at 7pm")
    assert not_stored is None

    records = service.list_records(user_id)
    assert len(records) == 1
