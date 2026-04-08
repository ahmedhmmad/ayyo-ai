# Data Model: KNOX Coach Experience

## Entity: AgentProfile
- Purpose: Defines visible identity and availability for agents listed in Ayyo shell.
- Fields:
  - id (uuid)
  - slug (string, unique, example: "knox")
  - display_name (string)
  - specialty (string)
  - coaching_style (string)
  - description (string)
  - status (enum: active, coming_soon)
- Validation:
  - slug lowercase kebab-case.
  - status=active only for KNOX in MVP.

## Entity: UserSessionIdentity
- Purpose: Represents authenticated Supabase user context.
- Fields:
  - user_id (uuid, Supabase Auth subject)
  - email (string)
  - auth_method (enum: magic_link)
  - last_authenticated_at (timestamp)
- Validation:
  - auth_method must equal magic_link in MVP.

## Entity: ConversationSession
- Purpose: Container for user-KNOX conversation timeline.
- Fields:
  - id (uuid)
  - user_id (uuid, FK -> UserSessionIdentity.user_id)
  - agent_slug (string, FK -> AgentProfile.slug)
  - started_at (timestamp)
  - last_message_at (timestamp)
  - status (enum: active, archived)
- Relationships:
  - One UserSessionIdentity has many ConversationSessions.
  - One ConversationSession has many ConversationMessages.

## Entity: ConversationMessage
- Purpose: Stores each turn in a conversation.
- Fields:
  - id (uuid)
  - session_id (uuid, FK -> ConversationSession.id)
  - role (enum: user, assistant, system)
  - content (text)
  - created_at (timestamp)
  - stream_state (enum: complete, interrupted)
  - persona_passed (boolean)
- Validation:
  - assistant messages must have persona_passed=true before persistence/display.

## Entity: UserMemoryRecord
- Purpose: Structured memory tied to user and coaching context.
- Fields:
  - id (uuid)
  - user_id (uuid, FK -> UserSessionIdentity.user_id)
  - category (enum: health_goal, active_routine, struggle, motivation_style, health_priority)
  - key (string)
  - value (text)
  - source_type (enum: explicit, implicit)
  - confidence_score (numeric 0.0-1.0)
  - created_at (timestamp)
  - updated_at (timestamp)
  - is_active (boolean)
- Validation:
  - implicit records require confidence_score >= configured threshold.
  - user_id scoping is mandatory for read/write/update/delete.

## Entity: MemoryAuditEvent
- Purpose: Captures user-directed memory edits/deletes/resets for traceability.
- Fields:
  - id (uuid)
  - user_id (uuid)
  - memory_record_id (uuid, nullable for reset-all)
  - action (enum: create, update, delete, reset_all)
  - action_at (timestamp)

## Entity: Commitment
- Purpose: User-stated commitment extracted from chat for accountability.
- Fields:
  - id (uuid)
  - user_id (uuid)
  - session_id (uuid)
  - statement (text)
  - target_window (string, nullable)
  - created_at (timestamp)
  - status (enum: open, completed, missed, replaced)

## Entity: CheckInPrompt
- Purpose: Event-triggered accountability prompt linked to commitment state.
- Fields:
  - id (uuid)
  - user_id (uuid)
  - commitment_id (uuid, FK -> Commitment.id)
  - trigger_event (enum: commitment_created, commitment_due, commitment_missed, user_requested)
  - prompt_text (text)
  - created_at (timestamp)
  - status (enum: pending, answered, expired)

## Entity: CheckInResponse
- Purpose: User reply to check-in and follow-up outcome.
- Fields:
  - id (uuid)
  - prompt_id (uuid, FK -> CheckInPrompt.id)
  - user_id (uuid)
  - response_text (text)
  - outcome (enum: complete, not_complete, partial)
  - responded_at (timestamp)

## Entity: GuidancePlanSnapshot
- Purpose: Captures structured in-chat plan output for continuity and auditing.
- Fields:
  - id (uuid)
  - user_id (uuid)
  - session_id (uuid)
  - source_message_id (uuid, FK -> ConversationMessage.id)
  - title (string)
  - steps_json (jsonb)
  - constraints_used_json (jsonb)
  - created_at (timestamp)

## State Transitions
- ConversationSession.status: active -> archived.
- Commitment.status: open -> completed | missed | replaced.
- CheckInPrompt.status: pending -> answered | expired.
- ConversationMessage.stream_state: interrupted -> complete (if resumed successfully).

## Access Rules
- Every entity with user_id is read/write scoped by authenticated Supabase user_id.
- Cross-user access is forbidden at service layer and must be reinforced by database policies.
