# Tasks: KNOX Coach Experience

**Input**: Design documents from `/specs/001-knox-coach-experience/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/knox-api.yaml, quickstart.md

**Tests**: Required for backend services, interactive UI, memory behavior, streaming, and personality enforcement.
**Organization**: Tasks are grouped by user story for independent implementation and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on incomplete tasks)
- **[Story]**: User story label (`[US1]` ... `[US6]`) for story-phase tasks only
- Every task includes an exact file path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Workspace bootstrap and configuration guards required before implementation

- [x] T001 Create monorepo app skeleton for API and web in apps/api and apps/web
- [x] T002 Create backend dependency manifest for FastAPI/Pydantic/Supabase/OpenAI in apps/api/pyproject.toml
- [x] T003 Create frontend dependency manifest for React/Vite/testing in apps/web/package.json
- [x] T004 Create root environment schema documentation (required before config-dependent tasks) in docs/env-schema.md
- [x] T005 [P] Create backend environment example with required variables in apps/api/.env.example
- [x] T006 [P] Create frontend environment example with required variables in apps/web/.env.example
- [x] T007 [P] Configure backend pytest defaults and markers in apps/api/pytest.ini
- [x] T008 [P] Configure frontend test runner and setup in apps/web/vitest.config.ts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Identity, data, and backend core services that block all user story implementation

**CRITICAL**: Complete this phase before starting user stories

- [x] T009 Create initial Supabase migration for identity-scoped core tables in apps/api/db/migrations/001_knox_core.sql
- [x] T010 Add row-level security policies for authenticated user_id scoping in apps/api/db/migrations/002_knox_rls.sql
- [x] T011 Implement Supabase auth dependency (magic-link only session validation) in apps/api/app/api/dependencies/auth.py
- [x] T012 [P] Add contract test for unauthorized and cross-user access rejection in apps/api/tests/integration/test_auth_scope.py
- [x] T013 Implement typed core entities for conversations/memory/check-ins in apps/api/app/schemas/core.py
- [x] T014 [P] Add schema validation tests for core entities in apps/api/tests/unit/test_core_schemas.py
- [x] T015 Implement MemoryService read/write/edit/delete/reset interface in apps/api/app/services/memory_service.py
- [x] T016 [P] Add pytest unit tests for MemoryService interface behavior in apps/api/tests/unit/test_memory_service.py
- [x] T017 Implement memory inference confidence-threshold policy as discrete module in apps/api/app/services/memory_inference_policy.py
- [x] T018 [P] Add pytest unit tests for confidence-threshold logic in apps/api/tests/unit/test_memory_inference_policy.py
- [x] T019 Implement PersonalityEnforcementService (system prompt + tone guard) in apps/api/app/services/personality_enforcement_service.py
- [x] T020 [P] Add pytest unit tests for personality enforcement behavior in apps/api/tests/unit/test_personality_enforcement_service.py
- [x] T021 Implement model-agnostic LLM adapter (DeepInfra-compatible OpenAI client) in apps/api/app/integrations/llm_adapter.py
- [x] T022 [P] Add pytest unit tests for LLM adapter config and fallback behavior in apps/api/tests/unit/test_llm_adapter.py
- [x] T023 Implement chat orchestration service wiring MemoryService + PersonalityEnforcement + LLM adapter in apps/api/app/services/chat_service.py
- [x] T024 [P] Add pytest unit tests for chat orchestration service in apps/api/tests/unit/test_chat_service.py
- [x] T025 Implement SSE streaming endpoint contract handler for /v1/knox/chat/stream in apps/api/app/api/sse/chat_stream.py
- [x] T026 [P] Add integration tests for SSE stream chunk contract in apps/api/tests/integration/test_chat_stream_sse.py
- [x] T027 Implement SSE interruption retry/resume handling in apps/api/app/services/stream_resume_service.py
- [x] T028 [P] Add integration tests for SSE interruption retry/resume in apps/api/tests/integration/test_stream_resume.py
- [x] T029 Implement API router composition with orchestration-only route handlers in apps/api/app/api/routes/__init__.py
- [x] T030 [P] Add regression snapshots for KNOX personality drift guard in apps/api/tests/regression/test_knox_persona_snapshots.py

**Checkpoint**: Supabase identity/data foundation and backend core services are ready

---

## Phase 3: User Story 1 - Persistent KNOX Chat (Priority: P1) MVP

**Goal**: Deliver authenticated, persistent, streamed KNOX chat in dedicated workspace

**Independent Test**: User signs in via magic link, opens KNOX, sends messages, receives streamed replies, leaves and returns to preserved history

### Tests for User Story 1

- [x] T031 [P] [US1] Add API integration test for session message history endpoint in apps/api/tests/integration/test_session_messages.py
- [x] T032 [P] [US1] Add frontend integration test for streamed chat rendering and history reload in apps/web/tests/integration/chat_streaming_history.test.tsx

### Implementation for User Story 1

- [x] T033 [US1] Implement conversation repository for persisted session/message queries in apps/api/app/services/conversation_repository.py
- [x] T034 [P] [US1] Add pytest unit tests for conversation repository behavior in apps/api/tests/unit/test_conversation_repository.py
- [x] T035 [US1] Implement session messages route /v1/knox/sessions/{sessionId}/messages in apps/api/app/api/routes/sessions.py
- [x] T036 [US1] Create KNOX workspace shell page (name/role/character identity) in apps/web/src/features/chat/pages/KnoxWorkspacePage.tsx
- [x] T037 [US1] Implement SSE client service for chat stream consumption in apps/web/src/services/chatStreamClient.ts
- [x] T038 [US1] Implement chat timeline and composer UI with loading/error/empty states in apps/web/src/features/chat/components/ChatPanel.tsx
- [x] T039 [US1] Wire chat feature state management for stream + history persistence in apps/web/src/features/chat/state/chatStore.ts

**Checkpoint**: US1 is independently demoable and testable

---

## Phase 4: User Story 2 - Memory Visibility and Control (Priority: P1)

**Goal**: Expose user-editable memory panel with identity-scoped records influencing responses

**Independent Test**: User views memory, edits/deletes/resets records, and sees conversation behavior update accordingly

### Tests for User Story 2

- [X] T040 [P] [US2] Add API integration tests for memory list/update/delete/reset endpoints in apps/api/tests/integration/test_memory_routes.py
- [X] T041 [P] [US2] Add frontend integration tests for memory panel CRUD and reset flows in apps/web/tests/integration/memory_panel.test.tsx

### Implementation for User Story 2

- [X] T042 [US2] Implement memory routes for /v1/knox/memory and /v1/knox/memory/{memoryId} in apps/api/app/api/routes/memory.py
- [X] T043 [P] [US2] Add pytest unit tests for memory route orchestration guards in apps/api/tests/unit/test_memory_routes_unit.py
- [X] T044 [US2] Extend (do not rewrite) MemoryService from T015 by integrating memory inference policy into the write pipeline in apps/api/app/services/memory_service.py
- [X] T045 [P] [US2] Add pytest unit tests for implicit/existing memory merge behavior in apps/api/tests/unit/test_memory_inference_merge.py
- [X] T046 [US2] Build memory panel UI with loading/error/empty states in apps/web/src/features/memory/components/MemoryPanel.tsx
- [X] T047 [US2] Implement memory API client for list/edit/delete/reset actions in apps/web/src/services/memoryClient.ts
- [X] T048 [US2] Wire memory panel into KNOX workspace navigation in apps/web/src/features/chat/pages/KnoxWorkspacePage.tsx

**Checkpoint**: US2 is independently demoable and testable

---

## Phase 5: User Story 3 - Personalized Guidance Plans In Chat (Priority: P2)

**Goal**: Provide structured in-chat workout/habit plans with follow-up refinements

**Independent Test**: User asks for a plan, receives structured in-chat output, asks for revision, receives adapted plan without separate plan view

### Tests for User Story 3

- [ ] T049 [P] [US3] Add API integration tests for in-chat guidance generation prompts in apps/api/tests/integration/test_guidance_generation.py
- [ ] T050 [P] [US3] Add frontend integration tests for structured guidance message rendering in apps/web/tests/integration/guidance_in_chat.test.tsx

### Implementation for User Story 3

- [ ] T051 [US3] Implement guidance generation service (chat-delivered structure only) in apps/api/app/services/guidance_service.py
- [ ] T052 [P] [US3] Add pytest unit tests for guidance service personalization rules in apps/api/tests/unit/test_guidance_service.py
- [ ] T053 [US3] Integrate guidance service into chat orchestration pipeline in apps/api/app/services/chat_service.py
- [ ] T054 [P] [US3] Add pytest unit tests for chat+guidance orchestration in apps/api/tests/unit/test_chat_guidance_orchestration.py
- [ ] T055 [US3] Implement structured guidance message component with loading/error/empty states in apps/web/src/features/chat/components/GuidanceMessageCard.tsx

**Checkpoint**: US3 is independently demoable and testable

---

## Phase 6: User Story 4 - Accountability Check-ins (Priority: P2)

**Goal**: Support event-triggered check-ins from user commitments and adaptive follow-up

**Independent Test**: User creates commitment in chat, receives event-triggered check-in, responds, and receives adaptive follow-up

### Tests for User Story 4

- [ ] T056 [P] [US4] Add API integration tests for commitment/check-in event flow in apps/api/tests/integration/test_checkin_event_flow.py
- [ ] T057 [P] [US4] Add frontend integration tests for check-in prompt/response flows with loading/error/empty states in apps/web/tests/integration/checkins_panel.test.tsx

### Implementation for User Story 4

- [ ] T058 [US4] Implement commitment tracking service and persistence in apps/api/app/services/commitment_service.py
- [ ] T059 [P] [US4] Add pytest unit tests for commitment service transitions in apps/api/tests/unit/test_commitment_service.py
- [ ] T060 [US4] Implement event-driven check-in generation service in apps/api/app/services/checkin_service.py
- [ ] T061 [P] [US4] Add pytest unit tests for check-in trigger rules in apps/api/tests/unit/test_checkin_service.py
- [ ] T062 [US4] Implement check-in routes for list/respond endpoints in apps/api/app/api/routes/checkins.py
- [ ] T063 [P] [US4] Add pytest unit tests for check-in route orchestration in apps/api/tests/unit/test_checkin_routes_unit.py
- [ ] T064 [US4] Implement check-in UI module with loading/error/empty states in apps/web/src/features/checkins/components/CheckInPanel.tsx
- [ ] T065 [US4] Wire check-in prompt responses into chat composer flow in apps/web/src/features/chat/components/ChatPanel.tsx

**Checkpoint**: US4 is independently demoable and testable

---

## Phase 7: User Story 5 - Agent Shell and Coming Soon Roster (Priority: P3)

**Goal**: Present premium agent shell with KNOX active and other agents marked Coming Soon

**Independent Test**: User lands on home shell, sees KNOX card and can enter workspace; other agent slots are visible but non-interactive

### Tests for User Story 5

- [ ] T066 [P] [US5] Add frontend integration tests for agent shell selection and Coming Soon states in apps/web/tests/integration/agent_shell.test.tsx

### Implementation for User Story 5

- [ ] T067 [P] [US5] Implement agent profile data source for shell cards in apps/web/src/features/agent-shell/data/agentProfiles.ts
- [ ] T068 [US5] Build platform home agent shell with loading/error/empty states in apps/web/src/features/agent-shell/pages/AgentShellPage.tsx
- [ ] T069 [US5] Add Coming Soon voice placeholder controls in KNOX workspace UI in apps/web/src/features/chat/components/VoicePlaceholder.tsx

**Checkpoint**: US5 is independently demoable and testable

---

## Phase 8: User Story 6 - Longevity-Framed Coaching (Priority: P3)

**Goal**: Ensure KNOX naturally includes long-term longevity framing in relevant guidance

**Independent Test**: User asks sleep/nutrition/training questions and receives direct advice tied to long-term outcomes

### Tests for User Story 6

- [ ] T070 [P] [US6] Add regression tests for longevity framing in assistant outputs in apps/api/tests/regression/test_longevity_framing.py
- [ ] T071 [P] [US6] Add frontend integration tests for longevity context rendering in chat messages in apps/web/tests/integration/longevity_context.test.tsx

### Implementation for User Story 6

- [ ] T072 [US6] Implement longevity framing policy module in apps/api/app/services/longevity_policy.py
- [ ] T073 [P] [US6] Add pytest unit tests for longevity policy relevance rules in apps/api/tests/unit/test_longevity_policy.py
- [ ] T074 [US6] Integrate longevity policy into personality-enforced response pipeline in apps/api/app/services/chat_service.py
- [ ] T075 [P] [US6] Add pytest unit tests for chat pipeline longevity integration in apps/api/tests/unit/test_chat_longevity_integration.py

**Checkpoint**: US6 is independently demoable and testable

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final quality hardening across all user stories

- [ ] T076 [P] Document API and SSE behavior for consumers in docs/knox-api-overview.md
- [ ] T077 Validate critical-path coverage threshold (>=80%) across memory/AI/personality paths in apps/api/tests
- [ ] T078 [P] Refactor modules exceeding 300 lines in apps/api/app and apps/web/src
- [ ] T079 Validate loading/error/empty states across all shipped UI screens in apps/web/src/features
- [ ] T080 Validate authenticated user-id memory scoping with adversarial integration tests in apps/api/tests/integration/test_memory_scope_security.py
- [ ] T081 Run quickstart end-to-end validation checklist in specs/001-knox-coach-experience/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1): start immediately
- Foundational (Phase 2): depends on Setup; blocks all story phases
- User Story phases (Phase 3-8): depend on Foundational completion
- Polish (Phase 9): depends on all targeted stories

### Explicit Ordering Constraints Applied

- Supabase schema and auth foundation precede all other implementation work (T009-T012)
- Backend service layer is completed before frontend wiring for dependent features (T015-T030 before US1-4 UI tasks)
- SSE pipeline and interruption handling precede chat UI consumption (T025-T028 before T037-T039)
- Memory panel UI starts only after MemoryService and memory routes are stable (T015/T042 before T046)
- Check-in logic starts only after commitment tracking exists (T058 before T060-T063)
- Agent shell work is parallelizable with backend once foundational phase is complete (T067-T069)
- .env schema documentation is completed before config-dependent tasks are considered complete (T004 before T005+)

### User Story Dependencies

- US1 (P1): depends on Foundational only
- US2 (P1): depends on Foundational and uses US1 workspace wiring
- US3 (P2): depends on Foundational and US1 chat pipeline
- US4 (P2): depends on Foundational and commitment data model
- US5 (P3): depends on Foundational only and can run parallel with US1-US4
- US6 (P3): depends on Foundational and chat pipeline from US1

### Parallel Opportunities

- Setup parallel: T005-T008 after T004
- Foundational parallel tests: T012, T014, T016, T018, T020, T022, T024, T026, T028, T030
- Story-level parallel work: US5 can run in parallel with US1-US4 after Phase 2
- Within each story, test and UI tasks marked [P] can run in parallel on separate files

---

## Parallel Execution Examples

### User Story 1

```bash
Task: "T031 [US1] Add API integration test in apps/api/tests/integration/test_session_messages.py"
Task: "T032 [US1] Add frontend integration test in apps/web/tests/integration/chat_streaming_history.test.tsx"
Task: "T037 [US1] Implement SSE client in apps/web/src/services/chatStreamClient.ts"
```

### User Story 2

```bash
Task: "T040 [US2] Add API integration tests in apps/api/tests/integration/test_memory_routes.py"
Task: "T041 [US2] Add frontend integration tests in apps/web/tests/integration/memory_panel.test.tsx"
Task: "T047 [US2] Implement memory API client in apps/web/src/services/memoryClient.ts"
```

### User Story 5

```bash
Task: "T066 [US5] Add frontend integration tests in apps/web/tests/integration/agent_shell.test.tsx"
Task: "T067 [US5] Implement agent profile data in apps/web/src/features/agent-shell/data/agentProfiles.ts"
Task: "T069 [US5] Add voice placeholder in apps/web/src/features/chat/components/VoicePlaceholder.tsx"
```

---

## Implementation Strategy

### MVP First (US1 + US2)

1. Complete Phase 1 and Phase 2 foundations
2. Deliver US1 (persistent streaming chat)
3. Deliver US2 (memory visibility/control)
4. Validate end-to-end MVP loop (auth -> chat -> memory-influenced reply)

### Incremental Delivery

1. Add US3 for in-chat structured guidance
2. Add US4 for event-based accountability
3. Add US5 platform shell polish in parallel
4. Add US6 longevity framing enhancements
5. Complete Phase 9 hardening and final validation

### Notes

- All tasks follow checklist format with IDs and paths.
- Backend service implementation tasks include paired pytest tasks.
- Personality enforcement and memory confidence-threshold logic are discrete testable tasks.
- SSE interruption retry/resume handling is explicit and tested.
- UI tasks explicitly include loading, error, and empty states.
