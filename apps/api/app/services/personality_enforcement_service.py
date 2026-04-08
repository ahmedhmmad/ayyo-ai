class PersonalityEnforcementService:
    def enforce(self, text: str) -> str:
        cleaned = text.strip()
        if not cleaned:
            return "No excuses. Start with one actionable step now."

        # Minimal tone guard baseline used by regression tests.
        banned = ["as an ai", "i'm just"]
        lower = cleaned.lower()
        for token in banned:
            lower = lower.replace(token, "")
        guarded = " ".join(lower.replace(",", " ").split()).strip()
        if not guarded.endswith("."):
            guarded += "."
        return guarded
