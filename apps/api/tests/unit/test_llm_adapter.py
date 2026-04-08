from app.integrations.llm_adapter import LLMAdapter, LLMConfig


def test_llm_adapter_uses_config() -> None:
    adapter = LLMAdapter(LLMConfig(api_key="k", base_url="u", model="m"))
    assert adapter.config.model == "m"


def test_llm_adapter_streams_tokens() -> None:
    adapter = LLMAdapter(LLMConfig(api_key="k", base_url="u", model="m"))
    tokens = adapter.stream_chat("go")
    assert len(tokens) > 0
