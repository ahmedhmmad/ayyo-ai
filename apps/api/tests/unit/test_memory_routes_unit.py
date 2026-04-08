from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def test_update_nonexistent_memory_returns_404() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    missing_id = str(uuid4())

    response = client.patch(
        f"/v1/knox/memory/{missing_id}",
        headers=_auth(user_id),
        json={"value": "new value"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "memory record not found"


def test_delete_nonexistent_memory_returns_404() -> None:
    client = TestClient(app)
    user_id = str(uuid4())
    missing_id = str(uuid4())

    response = client.delete(f"/v1/knox/memory/{missing_id}", headers=_auth(user_id))

    assert response.status_code == 404
    assert response.json()["detail"] == "memory record not found"
