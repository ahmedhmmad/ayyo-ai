from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class MemoryCategory(str, Enum):
    health_goal = "health_goal"
    active_routine = "active_routine"
    struggle = "struggle"
    motivation_style = "motivation_style"
    health_priority = "health_priority"


class MemorySourceType(str, Enum):
    explicit = "explicit"
    implicit = "implicit"


class StreamState(str, Enum):
    complete = "complete"
    interrupted = "interrupted"


class ChatRequest(BaseModel):
    session_id: UUID = Field(alias="sessionId")
    message: str = Field(min_length=1)


class StreamChunk(BaseModel):
    session_id: UUID = Field(alias="sessionId")
    message_id: UUID = Field(alias="messageId")
    token: str
    done: bool


class ConversationMessageOut(BaseModel):
    session_id: UUID = Field(alias="sessionId")
    user_id: UUID = Field(alias="userId")
    role: str
    content: str


class MemoryRecord(BaseModel):
    id: UUID
    user_id: UUID
    category: MemoryCategory
    key: str
    value: str
    source_type: MemorySourceType
    confidence_score: float = Field(ge=0.0, le=1.0)
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class MemoryUpdateRequest(BaseModel):
    value: str = Field(min_length=1)


class CheckInOutcome(str, Enum):
    complete = "complete"
    partial = "partial"
    not_complete = "not_complete"


class CommitmentStatus(str, Enum):
    open = "open"
    completed = "completed"
    missed = "missed"
    replaced = "replaced"


class CheckInStatus(str, Enum):
    pending = "pending"
    answered = "answered"
    expired = "expired"


class CommitmentRecord(BaseModel):
    id: UUID
    user_id: UUID = Field(alias="userId")
    session_id: UUID = Field(alias="sessionId")
    statement: str
    status: CommitmentStatus
    created_at: datetime = Field(alias="createdAt")


class CheckInPromptRecord(BaseModel):
    id: UUID
    user_id: UUID = Field(alias="userId")
    commitment_id: UUID = Field(alias="commitmentId")
    prompt_text: str = Field(alias="promptText")
    trigger_event: str = Field(alias="triggerEvent")
    status: CheckInStatus
    created_at: datetime = Field(alias="createdAt")


class CheckInResponseRequest(BaseModel):
    response_text: str = Field(alias="responseText", min_length=1)
    outcome: CheckInOutcome


class CheckInResponseOut(BaseModel):
    follow_up_message: str = Field(alias="followUpMessage")

