from app.services.longevity_policy import LongevityPolicy


def test_longevity_policy_detects_relevant_topics() -> None:
    policy = LongevityPolicy()

    assert policy.is_relevant("How can I improve sleep?")
    assert policy.is_relevant("Need nutrition strategy")
    assert policy.is_relevant("How should I train this week?")
    assert not policy.is_relevant("Tell me a joke")


def test_longevity_policy_appends_framing_naturally() -> None:
    policy = LongevityPolicy()

    out = policy.apply("How should I train?", "Start with compound lifts")
    assert "long-term health" in out.lower() or "years" in out.lower()

    unchanged = policy.apply("How should I train?", "Build long-term health with consistency")
    assert unchanged == "Build long-term health with consistency"
