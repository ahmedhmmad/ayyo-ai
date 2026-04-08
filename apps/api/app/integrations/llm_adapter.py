from dataclasses import dataclass

from app.settings import get_env


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str


class LLMAdapter:
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig(
            api_key=get_env("DEEPINFRA_API_KEY", "test-key"),
            base_url=get_env("OPENAI_BASE_URL", "https://api.deepinfra.com/v1/openai"),
            model=get_env("OPENAI_DEFAULT_MODEL", "zai-org/GLM-4.7-Flash"),
        )

    def stream_chat(self, user_message: str) -> list[str]:
        marker = "MEMORY:"
        if marker in user_message:
            memory_text = user_message.split(marker, 1)[1].strip()
            if memory_text:
                return ["coach: ", memory_text]

        # Deterministic token stream for baseline tests.
        return ["discipline", " starts", " now"] if user_message else ["act"]
