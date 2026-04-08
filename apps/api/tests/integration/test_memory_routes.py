from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def test_memory_routes_crud_and_reset_flow() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    # Seed memory via chat service write path.
    stream_response = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "struggle with mornings"},
    )
    assert stream_response.status_code == 200

    list_response = client.get("/v1/knox/memory", headers=_auth(user_id))
    assert list_response.status_code == 200
    records = list_response.json()
    assert len(records) >= 1

    memory_id = records[0]["id"]
    patch_response = client.patch(
        f"/v1/knox/memory/{memory_id}",
        headers=_auth(user_id),
        json={"value": "train before 7am"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["value"] == "train before 7am"

    delete_response = client.delete(f"/v1/knox/memory/{memory_id}", headers=_auth(user_id))
    assert delete_response.status_code == 204

    reset_response = client.delete("/v1/knox/memory", headers=_auth(user_id))
    assert reset_response.status_code == 204


def test_updated_memory_influences_next_chat_response() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    session_id = str(uuid4())

    client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "goal lose 10kg"},
    )

    list_response = client.get("/v1/knox/memory", headers=_auth(user_id))
    memory_id = list_response.json()[0]["id"]

    client.patch(
        f"/v1/knox/memory/{memory_id}",
        headers=_auth(user_id),
        json={"value": "priority sleep consistency"},
    )

    next_stream = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_id),
        json={"sessionId": session_id, "message": "what now"},
    )

    assert next_stream.status_code == 200
    assert "priority sleep consistency" in next_stream.text.lower()
