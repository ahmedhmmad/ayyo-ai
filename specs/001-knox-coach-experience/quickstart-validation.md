# Quickstart Validation Report (T081)

Date: 2026-04-09

## 1) Prerequisites
- Node.js 20+: VERIFIED (`v24.14.1`)
- Python 3.11+: VERIFIED (`Python 3.13.12`)
- Supabase project with magic link auth: GAP (not verifiable from local test harness alone)
- DeepInfra API key configured: GAP (runtime defaults used in test adapter)

## 2) Environment Configuration
- `apps/api/.env.example` exists: VERIFIED
- `apps/web/.env.example` exists: VERIFIED
- `docs/env-schema.md` exists: VERIFIED

## 3) Start Services
- Backend startup command documented: VERIFIED (documentation presence)
- Frontend startup command documented: VERIFIED (documentation presence)
- Live manual service startup in this run: GAP (not executed as persistent dev servers in this checkpoint)

## 4) Core Flows
- Auth and first entry (magic link-only UX): PARTIAL
  - Contract and dependency enforce bearer auth and magic-link context.
  - Full hosted Supabase email-link UX not executed in this local checkpoint.
- Streaming chat + persona: VERIFIED
  - `tests/integration/test_chat_stream_sse.py`
  - `tests/regression/test_knox_persona_snapshots.py`
- Memory inference + control: VERIFIED
  - `tests/integration/test_memory_routes.py`
  - `tests/integration/test_memory_scope_security.py`
- Guidance plans in chat only: VERIFIED
  - `tests/integration/test_guidance_generation.py`
  - `tests/integration/guidance_in_chat.test.tsx`
- Event-based check-ins: VERIFIED
  - `tests/integration/test_checkin_event_flow.py`
  - `tests/integration/checkins_panel.test.tsx`
- Voice placeholder (coming soon only): VERIFIED
  - `tests/integration/agent_shell.test.tsx` (shell behavior)
  - Workspace contains non-functional `VoicePlaceholder` with Coming Soon label

## 5) Test Commands
- Backend representative quickstart suite executed: VERIFIED (pass)
- Frontend representative quickstart suite executed: VERIFIED (pass)

## 6) Exit Criteria
- Critical-path tests pass: VERIFIED
- Personality enforcement on user-visible output: VERIFIED by regression and integration tests
- Memory access authenticated-user scoped: VERIFIED by adversarial scope tests
- SSE streaming end-to-end behavior: VERIFIED by stream integration tests
