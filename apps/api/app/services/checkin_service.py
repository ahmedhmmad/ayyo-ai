from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.core import (
    CheckInOutcome,
    CheckInPromptRecord,
    CheckInResponseOut,
    CheckInStatus,
    CommitmentRecord,
    CommitmentStatus,
)


class CheckInService:
    def __init__(self) -> None:
        self._prompts: list[CheckInPromptRecord] = []

    def generate_for_commitment(self, commitment: CommitmentRecord) -> CheckInPromptRecord:
        existing = self._find_pending_for_commitment(commitment.id)
        if existing is not None:
            return existing

        prompt = CheckInPromptRecord(
            id=uuid4(),
            userId=commitment.user_id,
            commitmentId=commitment.id,
            promptText=f"You committed to {commitment.statement}. How did it go?",
            triggerEvent="commitment_created",
            status=CheckInStatus.pending,
            createdAt=datetime.now(tz=timezone.utc),
        )
        self._prompts.append(prompt)
        return prompt

    def list_pending(self, user_id: UUID) -> list[CheckInPromptRecord]:
        return [p for p in self._prompts if p.user_id == user_id and p.status == CheckInStatus.pending]

    def respond(
        self,
        user_id: UUID,
        checkin_id: UUID,
        response_text: str,
        outcome: CheckInOutcome,
    ) -> CheckInResponseOut:
        _ = response_text
        for idx, prompt in enumerate(self._prompts):
            if prompt.id == checkin_id and prompt.user_id == user_id:
                self._prompts[idx] = prompt.model_copy(update={"status": CheckInStatus.answered})
                return CheckInResponseOut(followUpMessage=self._follow_up(prompt.prompt_text, outcome))
        raise KeyError("checkin not found")

    def get_prompt(self, user_id: UUID, checkin_id: UUID) -> CheckInPromptRecord:
        for prompt in self._prompts:
            if prompt.id == checkin_id and prompt.user_id == user_id:
                return prompt
        raise KeyError("checkin not found")

    def mark_commitment_outcome(self, commitment: CommitmentRecord, outcome: CheckInOutcome) -> CommitmentStatus:
        if outcome == CheckInOutcome.complete:
            return CommitmentStatus.completed
        if outcome == CheckInOutcome.partial:
            return CommitmentStatus.open
        return CommitmentStatus.missed

    def _follow_up(self, prompt_text: str, outcome: CheckInOutcome) -> str:
        if outcome == CheckInOutcome.complete:
            return f"Strong follow-through. Keep momentum on this commitment: {prompt_text}"
        if outcome == CheckInOutcome.partial:
            return "Recovery framing: keep the streak alive with one smaller step today and build tomorrow."
        return "Recovery framing: no shame, reset with one concrete next step today and continue tomorrow."

    def _find_pending_for_commitment(self, commitment_id: UUID) -> CheckInPromptRecord | None:
        for prompt in self._prompts:
            if prompt.commitment_id == commitment_id and prompt.status == CheckInStatus.pending:
                return prompt
        return None
