from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.auth import AuthContext, get_auth_context
from app.schemas.core import CheckInPromptRecord, CheckInResponseOut, CheckInResponseRequest
from app.services.service_container import checkin_service


router = APIRouter(prefix="/knox/checkins", tags=["knox-checkins"])


@router.get("", response_model=list[CheckInPromptRecord])
def list_checkins(auth: AuthContext = Depends(get_auth_context)) -> list[CheckInPromptRecord]:
    return checkin_service.list_pending(auth.user_id)


@router.post("/{checkin_id}/respond", response_model=CheckInResponseOut)
def respond_to_checkin(
    checkin_id: UUID,
    request: CheckInResponseRequest,
    auth: AuthContext = Depends(get_auth_context),
) -> CheckInResponseOut:
    try:
        return checkin_service.respond(auth.user_id, checkin_id, request.response_text, request.outcome)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="checkin not found") from exc
