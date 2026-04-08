import json
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_sse_stream_endpoint_returns_event_stream() -> None:
    client = TestClient(app)
    response = client.post(
        "/v1/knox/chat/stream",
        headers={"Authorization": f"Bearer {uuid4()}"},
        json={"sessionId": str(uuid4()), "message": "push"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    body = response.text
    assert "data: " in body
    payload = body.split("data: ")[1].split("\n\n")[0]
    parsed = json.loads(payload)
    assert "token" in parsed
