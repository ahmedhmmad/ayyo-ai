import json
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def _assistant_text(raw: str) -> str:
    parts: list[str] = []
    for line in raw.splitlines():
      if not line.startswith("data: "):
        continue
      payload = json.loads(line[6:])
      parts.append(payload["token"])
    return "".join(parts).lower()


def test_sleep_nutrition_training_include_longevity_framing() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    prompts = [
        "How should I improve sleep quality?",
        "Give me nutrition advice for better energy",
        "How should I structure weekly training?",
    ]

    for prompt in prompts:
        response = client.post(
            "/v1/knox/chat/stream",
            headers=_auth(user_id),
            json={"sessionId": session_id, "message": prompt},
        )
        assert response.status_code == 200
        text = _assistant_text(response.text)
        assert "long-term" in text or "longevity" in text or "years" in text
