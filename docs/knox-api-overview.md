# KNOX API and SSE Overview

## Base
- Base path: `/v1`
- Auth: `Authorization: Bearer <user_uuid>`
- Auth model: magic-link user identity represented as a UUID token in current MVP test harness.

## Authentication Behavior
- Missing bearer token -> `401 Unauthorized`
- Invalid bearer token format -> `401 Invalid token`
- All route reads/writes are scoped to authenticated `user_id`.

## Endpoints

### POST /v1/knox/chat/stream
- Purpose: stream assistant output for a user message.
- Request body:
  - `sessionId` (uuid)
  - `message` (string, min length 1)
- Response:
  - `200 text/event-stream`
  - Each event line is formatted as `data: <json>\n\n`
- Stream payload shape:
  - `sessionId` (uuid)
  - `messageId` (uuid)
  - `token` (string)
  - `done` (boolean)
- Pipeline behavior:
  - conversation persistence
  - memory read/write through MemoryService
  - commitment extraction and event-based check-in generation
  - guidance plan generation for plan/revision prompts
  - personality enforcement and longevity framing for natural conversational output

### GET /v1/knox/sessions/{sessionId}/messages
- Purpose: return persisted session messages for authenticated user only.
- Response:
  - `200 application/json` list of `{sessionId, userId, role, content}`

### GET /v1/knox/memory
- Purpose: list active memory records for authenticated user.
- Response:
  - `200 application/json` list of memory records

### PATCH /v1/knox/memory/{memoryId}
- Purpose: update one user-owned memory record value.
- Request body:
  - `value` (string, min length 1)
- Responses:
  - `200` updated memory record
  - `404 memory record not found` for unknown ID or cross-user access

### DELETE /v1/knox/memory/{memoryId}
- Purpose: deactivate one user-owned memory record.
- Responses:
  - `204`
  - `404 memory record not found` for unknown ID or cross-user access

### DELETE /v1/knox/memory
- Purpose: reset all memory records for authenticated user only.
- Response:
  - `204`

### GET /v1/knox/checkins
- Purpose: list pending check-ins generated from commitment events.
- Response:
  - `200 application/json` list of check-in prompts

### POST /v1/knox/checkins/{checkinId}/respond
- Purpose: submit outcome for one pending check-in.
- Request body:
  - `responseText` (string)
  - `outcome` (`complete` | `partial` | `not_complete`)
- Responses:
  - `200` with `{followUpMessage}`
  - `404 checkin not found` for unknown ID or cross-user access

## SSE Consumer Notes
- Parse line-delimited `data:` events.
- Concatenate `token` fields in order to reconstruct assistant text.
- Treat `done=true` as final chunk for the streamed assistant message.

## Security and Scope Notes
- Memory operations are user-scoped and reject cross-user mutation by ownership checks.
- Check-in responses are user-scoped and reject cross-user prompt access.
- Frontend does not call model providers directly; all model interactions pass through backend chat stream.

## Error Surface
- `401`: missing/invalid bearer token
- `404`: user-scoped object not found (memory/checkin)
- `200/204`: successful read/write operations
