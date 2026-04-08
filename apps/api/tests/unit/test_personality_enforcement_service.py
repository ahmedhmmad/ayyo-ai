from app.services.personality_enforcement_service import PersonalityEnforcementService


def test_personality_guard_strips_softened_ai_phrasing() -> None:
    service = PersonalityEnforcementService()
    result = service.enforce("As an AI I cannot coach you")
    assert "as an ai" not in result


def test_personality_guard_default_action() -> None:
    service = PersonalityEnforcementService()
    result = service.enforce("  ")
    assert "No excuses" in result
