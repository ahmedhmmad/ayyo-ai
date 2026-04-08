from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def test_cross_user_memory_access_is_rejected() -> None:
    client = TestClient(app)
    user_a = str(uuid4())
    user_b = str(uuid4())
    session_id = str(uuid4())

    seed = client.post(
        "/v1/knox/chat/stream",
        headers=_auth(user_b),
        json={"sessionId": session_id, "message": "goal improve sleep consistency"},
    )
    assert seed.status_code == 200

    user_b_records = client.get("/v1/knox/memory", headers=_auth(user_b)).json()
    assert len(user_b_records) >= 1
    user_b_memory_id = user_b_records[0]["id"]

    user_a_records = client.get("/v1/knox/memory", headers=_auth(user_a)).json()
    assert user_a_records == []

    patch_attempt = client.patch(
        f"/v1/knox/memory/{user_b_memory_id}",
        headers=_auth(user_a),
        json={"value": "malicious overwrite"},
    )
    assert patch_attempt.status_code == 404

    delete_attempt = client.delete(f"/v1/knox/memory/{user_b_memory_id}", headers=_auth(user_a))
    assert delete_attempt.status_code == 404

    reset_a = client.delete("/v1/knox/memory", headers=_auth(user_a))
    assert reset_a.status_code == 204

    user_b_after = client.get("/v1/knox/memory", headers=_auth(user_b)).json()
    assert len(user_b_after) >= 1
    assert user_b_after[0]["id"] == user_b_memory_id
