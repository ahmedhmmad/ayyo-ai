# Research: KNOX Coach Experience

## Decision 1: Authentication approach for MVP
- Decision: Use Supabase Auth magic-link only for MVP. Defer email/password.
- Rationale: Reduces onboarding friction and implementation scope while satisfying identity-scoped memory requirements.
- Alternatives considered:
  - Magic link + password in MVP: broader scope, higher QA surface.
  - Password-only: higher friction and weaker first-session conversion.

## Decision 2: Check-in triggering model
- Decision: Event-based only, driven by commitment/outcome events captured in chat.
- Rationale: Preserves personal coaching tone and avoids generic notification behavior.
- Alternatives considered:
  - Time-based schedule only: prone to generic/uncontextual prompts.
  - Hybrid time + event: useful later, unnecessary complexity for MVP.

## Decision 3: Voice interaction scope
- Decision: Render non-functional voice UI controls labeled Coming Soon.
- Rationale: Keeps UX vision visible while preserving focus on core text coaching loop.
- Alternatives considered:
  - Full voice input/output: larger infra and quality scope.
  - Voice input only: partial feature still expands testing/perf complexity.

## Decision 4: Memory inference policy
- Decision: Store explicit user statements plus high-confidence implicit signals only; all memory is user-editable in memory panel.
- Rationale: Balances personalization depth with user control and data quality.
- Alternatives considered:
  - Explicit-only: safer but less personalized continuity.
  - Aggressive implicit extraction: risk of incorrect memory and trust erosion.

## Decision 5: Guidance plan delivery UX
- Decision: Deliver structured plans inside chat only; no dedicated plan view.
- Rationale: Maintains one continuous conversational surface and minimizes MVP UI fragmentation.
- Alternatives considered:
  - Separate plan view: increases frontend complexity and context switching.
  - Chat + dedicated plan view: better long term but out of MVP scope.

## Decision 6: Streaming transport
- Decision: Use Server-Sent Events from FastAPI to React for token streaming.
- Rationale: Simpler than WebSockets for one-way token streams; sufficient for conversational delivery.
- Alternatives considered:
  - WebSockets: bidirectional flexibility not needed for this phase.
  - Polling/chunked fetch: poorer UX and latency behavior.

## Decision 7: Personality enforcement implementation point
- Decision: Enforce KNOX tone in backend via a dedicated PersonalityService/ToneGuard before emitting user-visible content.
- Rationale: Guarantees policy enforcement independent of client behavior.
- Alternatives considered:
  - Frontend-only filtering: bypass risk and policy inconsistency.
  - Prompt-only without guard: insufficient for drift prevention.

## Decision 8: Memory access architecture
- Decision: All memory reads/writes pass through MemoryService with authenticated user-id scoping and confidence thresholds.
- Rationale: Centralizes rules for identity safety, inference quality, and observability.
- Alternatives considered:
  - Direct route/database access: duplicates logic and increases leakage risk.
  - Client-managed memory state only: violates persistence and trust requirements.
