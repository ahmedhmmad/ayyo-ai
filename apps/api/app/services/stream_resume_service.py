from app.schemas.core import StreamChunk


class StreamResumeService:
    def resume(self, chunks: list[StreamChunk], from_index: int) -> list[StreamChunk]:
        if from_index < 0:
            from_index = 0
        if from_index >= len(chunks):
            return []
        return chunks[from_index:]
