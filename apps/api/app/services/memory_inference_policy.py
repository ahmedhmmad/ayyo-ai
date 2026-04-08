from app.schemas.core import MemorySourceType
from app.settings import get_float_env


class MemoryInferencePolicy:
    def __init__(self, threshold: float | None = None) -> None:
        self.threshold = threshold if threshold is not None else get_float_env("MEMORY_IMPLICIT_CONFIDENCE_THRESHOLD", 0.8)

    def should_store(self, source_type: MemorySourceType, confidence: float) -> bool:
        if source_type == MemorySourceType.explicit:
            return True
        return confidence >= self.threshold
