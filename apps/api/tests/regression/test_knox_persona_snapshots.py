from app.services.personality_enforcement_service import PersonalityEnforcementService


def test_knox_persona_baseline_snapshot() -> None:
    service = PersonalityEnforcementService()
    output = service.enforce("As an AI, I cannot do that")
    assert output == "i cannot do that."
