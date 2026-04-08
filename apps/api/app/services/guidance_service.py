import json
from uuid import UUID

from app.schemas.core import MemoryRecord


class GuidanceService:
    def should_handle(self, message: str) -> bool:
        lowered = message.lower()
        return "plan" in lowered or "revise" in lowered

    def build_guidance(
        self,
        user_id: UUID,
        session_id: UUID,
        message: str,
        memory_records: list[MemoryRecord],
        history: list[str],
    ) -> str:
        _ = (user_id, session_id)
        constraints = [record.value for record in memory_records if record.value.strip()]
        prior_title = self._extract_last_title(history)

        if "revise" in message.lower() and prior_title:
            title = f"{prior_title} (Adapted)"
        else:
            title = "Personalized Guidance Plan"

        duration_hint = self._extract_duration(message)
        steps = [
            {"order": 1, "action": "Daily mobility warm-up", "scheduleHint": "Day 1"},
            {"order": 2, "action": "Low-impact strength session", "scheduleHint": "Day 2"},
            {"order": 3, "action": "Recovery walk and reflection", "scheduleHint": "Day 3"},
        ]

        if duration_hint:
            steps[0]["action"] = f"{steps[0]['action']} ({duration_hint})"

        payload = {
            "type": "guidance_plan",
            "title": title,
            "steps": steps,
            "constraints": constraints,
            "prompt": message,
        }
        return json.dumps(payload)

    def _extract_last_title(self, history: list[str]) -> str | None:
        for item in reversed(history):
            try:
                parsed = json.loads(item)
            except json.JSONDecodeError:
                continue

            if parsed.get("type") == "guidance_plan" and isinstance(parsed.get("title"), str):
                return parsed["title"]
        return None

    def _extract_duration(self, message: str) -> str | None:
        lowered = message.lower()
        marker = "minutes"
        if marker not in lowered:
            return None

        idx = lowered.find(marker)
        prefix = message[:idx].strip().split(" ")
        if not prefix:
            return None
        candidate = prefix[-1]
        if candidate.isdigit():
            return f"{candidate} minutes"
        return None
