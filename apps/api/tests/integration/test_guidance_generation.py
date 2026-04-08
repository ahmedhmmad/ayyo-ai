import json
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def _assistant_text_from_stream(raw: str) -> str:
    parts: list[str] = []
    for line in raw.splitlines():
        if not line.startswith("data: "):
            continue
        payload = json.loads(line[6:])
        parts.append(payload["token"])
    return "".join(parts)


def test_guidance_plan_reflects_user_constraints_from_memory() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    seed = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "goal run 5k without knee pain"},
    )
    assert seed.status_code == 200

    memories = client.get("/v1/knox/memory", headers=_auth(user_id)).json()
    memory_id = memories[0]["id"]
    client.patch(
        f"/v1/knox/memory/{memory_id}",
        headers=_auth(user_id),
        json={"value": "knee pain no jumping and no deep squats"},
    )

    constrained = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "build me a 3 day training plan"},
    )
    assert constrained.status_code == 200

    constrained_text = _assistant_text_from_stream(constrained.text).lower()
    assert "guidance_plan" in constrained_text
    assert "no jumping" in constrained_text

    client.patch(
        f"/v1/knox/memory/{memory_id}",
        headers=_auth(user_id),
        json={"value": "shoulder pain no overhead pressing"},
    )

    changed = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "build me a 3 day training plan"},
    )
    changed_text = _assistant_text_from_stream(changed.text).lower()

    assert "no overhead pressing" in changed_text
    assert changed_text != constrained_text


def test_followup_revision_adapts_existing_plan_context() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    first = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "create a beginner sleep and training plan"},
    )
    assert first.status_code == 200
    first_text = _assistant_text_from_stream(first.text)
    assert "guidance_plan" in first_text.lower()

    revised = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "revise it for 20 minutes per day only"},
    )
    assert revised.status_code == 200

    revised_text = _assistant_text_from_stream(revised.text).lower()
    assert "guidance_plan" in revised_text
    assert "20 minutes" in revised_text
    assert revised_text != first_text.lower()
