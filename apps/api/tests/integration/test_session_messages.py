from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_session_message_history_available_after_stream() -> None:
    client = TestClient(app)
    auth_user = uuid4()
    session_id = uuid4()

    stream_response = client.post(
        "/v1/knox/chat/stream",
        headers={"Authorization": f"Bearer {auth_user}"},
        json={"sessionId": str(session_id), "message": "coach me"},
    )
    assert stream_response.status_code == 200

    history_response = client.get(
        f"/v1/knox/sessions/{session_id}/messages",
        headers={"Authorization": f"Bearer {auth_user}"},
    )
    assert history_response.status_code == 200
    payload = history_response.json()
    assert len(payload) >= 2
    assert payload[0]["role"] == "user"
    assert payload[1]["role"] == "assistant"
