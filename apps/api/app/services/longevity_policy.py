class LongevityPolicy:
    def is_relevant(self, message: str) -> bool:
        lowered = message.lower()
        return any(topic in lowered for topic in ["sleep", "nutrition", "diet", "train", "workout", "training"])

    def apply(self, message: str, response_text: str) -> str:
        if not self.is_relevant(message):
            return response_text

        framing = " This builds long-term health and preserves strength for years."
        if "long-term" in response_text.lower() or "longevity" in response_text.lower() or "years" in response_text.lower():
            return response_text
        return f"{response_text}{framing}"
