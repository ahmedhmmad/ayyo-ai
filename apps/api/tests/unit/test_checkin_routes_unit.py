from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def _auth(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_id}"}


def test_checkin_list_requires_auth() -> None:
    client = TestClient(app)

    response = client.get("/v1/knox/checkins")

    assert response.status_code == 401


def test_respond_missing_checkin_returns_404() -> None:
    client = TestClient(app)
    user_id = str(uuid4())

    response = client.post(
        f"/v1/knox/checkins/{uuid4()}/respond",
        headers=_auth(user_id),
        json={"responseText": "I missed it", "outcome": "not_complete"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "checkin not found"
