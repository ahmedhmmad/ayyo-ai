from uuid import uuid4

from app.schemas.core import MemorySourceType
from app.services.memory_service import MemoryService


def test_memory_service_crud_flow() -> None:
    service = MemoryService()
    user_id = uuid4()
    record = service.create_record(user_id, "health_goal", "goal", "run", MemorySourceType.explicit, 1.0)
    assert len(service.list_records(user_id)) == 1
    updated = service.update_record(user_id, record.id, "walk")
    assert updated.value == "walk"
    service.delete_record(user_id, record.id)
    assert service.list_records(user_id) == []
