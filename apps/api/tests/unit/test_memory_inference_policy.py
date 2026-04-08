from app.schemas.core import MemorySourceType
from app.services.memory_inference_policy import MemoryInferencePolicy


def test_explicit_always_stores() -> None:
    policy = MemoryInferencePolicy(threshold=0.9)
    assert policy.should_store(MemorySourceType.explicit, 0.1)


def test_implicit_requires_threshold() -> None:
    policy = MemoryInferencePolicy(threshold=0.8)
    assert not policy.should_store(MemorySourceType.implicit, 0.7)
    assert policy.should_store(MemorySourceType.implicit, 0.8)
