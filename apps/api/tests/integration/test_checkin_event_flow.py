from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


SHAMING_WORDS = ["lazy", "pathetic", "weak", "failure", "worthless", "punish"]


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def test_commitment_message_triggers_checkin_referencing_commitment_text() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    message = "I commit to 30-minute evening walks every day"
    chat = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": message},
    )
    assert chat.status_code == 200

    checkins = client.get("/v1/knox/checkins", headers=_auth(user_id))
    assert checkins.status_code == 200
    payload = checkins.json()
    assert len(payload) >= 1
    assert "30-minute evening walks" in payload[0]["promptText"].lower()


def test_non_completion_response_uses_recovery_not_shaming() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    chat = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "I commit to bedtime by 10:30pm"},
    )
    assert chat.status_code == 200

    checkins = client.get("/v1/knox/checkins", headers=_auth(user_id)).json()
    checkin_id = checkins[0]["id"]

    response = client.post(
        f"/v1/knox/checkins/{checkin_id}/respond",
        headers=_auth(user_id),
        json={"responseText": "I did not complete it", "outcome": "not_complete"},
    )
    assert response.status_code == 200

    content = response.json()["followUpMessage"].lower()
    assert "recovery" in content or "reset" in content or "next step" in content
    for word in SHAMING_WORDS:
        assert word not in content
