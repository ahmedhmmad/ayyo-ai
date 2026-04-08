from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies.auth import AuthContext, get_auth_context
from app.schemas.core import MemoryRecord, MemoryUpdateRequest
from app.services.service_container import memory_service


router = APIRouter(prefix="/knox/memory", tags=["knox-memory"])


@router.get("", response_model=list[MemoryRecord])
def list_memory(auth: AuthContext = Depends(get_auth_context)) -> list[MemoryRecord]:
    return memory_service.list_records(auth.user_id)


@router.patch("/{memory_id}", response_model=MemoryRecord)
def update_memory(memory_id: UUID, request: MemoryUpdateRequest, auth: AuthContext = Depends(get_auth_context)) -> MemoryRecord:
    try:
        return memory_service.update_record(auth.user_id, memory_id, request.value)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="memory record not found") from exc


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(memory_id: UUID, auth: AuthContext = Depends(get_auth_context)) -> Response:
    try:
        memory_service.delete_record(auth.user_id, memory_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="memory record not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def reset_memory(auth: AuthContext = Depends(get_auth_context)) -> Response:
    memory_service.reset_memory(auth.user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
