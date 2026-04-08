from uuid import uuid4

from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies.auth import AuthContext, assert_user_scope, get_auth_context


router = APIRouter()


@router.get("/owned/{owner_id}")
def owned(owner_id: str, auth: AuthContext = Depends(get_auth_context)):
    assert_user_scope(auth, uuid4() if owner_id == "other" else auth.user_id)
    return {"ok": True}


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_rejects_unauthorized_request() -> None:
    client = _client()
    response = client.get("/owned/self")
    assert response.status_code == 401


def test_rejects_cross_user_scope() -> None:
    client = _client()
    response = client.get("/owned/other", headers={"Authorization": f"Bearer {uuid4()}"})
    assert response.status_code == 403
