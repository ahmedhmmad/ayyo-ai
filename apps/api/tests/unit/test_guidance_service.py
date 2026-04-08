from uuid import uuid4

from app.schemas.core import MemoryRecord, MemorySourceType
from app.services.guidance_service import GuidanceService


def _memory(value: str) -> MemoryRecord:
    now = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    return MemoryRecord(
        id=uuid4(),
        user_id=uuid4(),
        category="health_priority",
        key="constraint",
        value=value,
        source_type=MemorySourceType.explicit,
        confidence_score=1.0,
        created_at=now,
        updated_at=now,
        is_active=True,
    )


def test_guidance_service_reflects_constraints() -> None:
    service = GuidanceService()

    output = service.build_guidance(
        user_id=uuid4(),
        session_id=uuid4(),
        message="build me a plan",
        memory_records=[_memory("no jumping")],
        history=[],
    )

    assert "guidance_plan" in output
    assert "no jumping" in output


def test_guidance_service_revision_adapts_prior_context() -> None:
    service = GuidanceService()
    prior = '{"type":"guidance_plan","title":"Personalized Guidance Plan"}'

    revised = service.build_guidance(
        user_id=uuid4(),
        session_id=uuid4(),
        message="revise it for 20 minutes per day only",
        memory_records=[],
        history=[prior],
    )

    assert "Adapted" in revised
    assert "20 minutes" in revised
