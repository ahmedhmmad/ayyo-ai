# Quickstart: KNOX Coach Experience

## 1. Prerequisites
- Node.js 20+
- Python 3.11+
- Supabase project with Auth (magic link enabled) and Postgres
- DeepInfra API key

## 2. Environment Configuration
Create environment files (values are examples only):

- Backend env (`apps/api/.env`)
  - `SUPABASE_URL=`
  - `SUPABASE_SERVICE_ROLE_KEY=`
  - `SUPABASE_JWT_SECRET=`
  - `DEEPINFRA_API_KEY=`
  - `OPENAI_BASE_URL=https://api.deepinfra.com/v1/openai`
  - `OPENAI_DEFAULT_MODEL=zai-org/GLM-4.7-Flash`
  - `MEMORY_IMPLICIT_CONFIDENCE_THRESHOLD=0.80`
  - `KNOX_PERSONA_VERSION=v1`

- Frontend env (`apps/web/.env`)
  - `VITE_SUPABASE_URL=`
  - `VITE_SUPABASE_ANON_KEY=`
  - `VITE_API_BASE_URL=http://localhost:8000`

## 3. Start Services
- Start backend:
  - `cd apps/api`
  - `uvicorn app.main:app --reload --port 8000`
- Start frontend:
  - `cd apps/web`
  - `npm run dev`

## 4. Validate Core Flows

### Auth and First Entry
- Sign in via Supabase magic link.
- Confirm KNOX workspace loads after authentication.
- Confirm email/password flow is not exposed.

### Streaming Chat + Persona
- Send first message in KNOX chat.
- Verify response streams token-by-token via SSE.
- Verify output is direct, disciplined, motivational (persona checks pass).

### Memory Inference + Control
- Provide explicit and implicit context in chat.
- Verify only explicit + high-confidence implicit memory records are saved.
- Open memory panel; edit, delete, and reset entries.
- Verify subsequent responses reflect updated memory state.

### Guidance Plans In Chat
- Ask for a workout/habit plan.
- Verify plan appears in structured format inside chat.
- Verify no separate dedicated plan view is available.

### Event-Based Check-ins
- Create a commitment in chat.
- Trigger follow-up event and verify check-in prompt appears in app.
- Respond "complete" and "not complete" in separate attempts; verify adaptive follow-up behavior.

### Voice Placeholder
- Confirm voice controls are visible and labeled Coming Soon.
- Confirm no functional voice capture/output occurs.

## 5. Test Commands
- Backend tests: `cd apps/api && pytest`
- Frontend integration tests: `cd apps/web && npm test`
- Regression tests (persona/prompt): `cd apps/api && pytest tests/regression`

## 6. Exit Criteria
- All critical-path tests pass.
- User-visible responses always pass personality enforcement.
- Memory access is authenticated-user scoped.
- SSE streaming works end-to-end without blocking on full completion.
