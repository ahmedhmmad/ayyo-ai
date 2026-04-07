<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles:
	- IV. Structured Memory as Product Intelligence -> IV. Structured Memory & Identity Integrity
- Added sections:
	- None
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ updated: .specify/templates/plan-template.md
	- ✅ updated: .specify/templates/spec-template.md
	- ✅ updated: .specify/templates/tasks-template.md
	- ✅ updated: .specify/templates/commands/*.md (none present)
- Follow-up TODOs:
	- None
-->

# Ayyo Constitution

## Core Principles

### I. Code Quality & Modularity
All frontend code MUST be TypeScript with React strict mode enabled. All backend APIs MUST be
Python/FastAPI and MUST use typed Pydantic request/response models. Business logic MUST NOT live
in route handlers and MUST live in service/domain modules. Source files MUST remain at or below
300 lines; code exceeding this limit MUST be split into cohesive modules. Naming MUST be
descriptive and self-documenting, and abbreviations are prohibited unless they are established
domain standards. Frontend behavior SHOULD prefer pure/composable functions over classes unless
class semantics are explicitly required.

Rationale: strict typing, modularity, and readable naming reduce defects and keep the codebase
maintainable as features and agents expand.

### II. Testing Discipline & Coverage Gates
All backend service functions MUST have unit tests using pytest. All React components with user
interaction MUST have integration tests. Business-critical paths (memory system, AI response
pipeline, personality enforcement layer) MUST maintain at least 80% coverage. Tests MUST be
authored before or alongside implementation, and new feature work MUST include failing tests that
validate intended behavior before completion. AI prompt and persona logic MUST include
snapshot/regression tests that detect tone and behavior drift.

Rationale: enforced test coverage and regression controls preserve reliability for both product
logic and AI behavior.

### III. KNOX Personality Enforcement (NON-NEGOTIABLE)
KNOX has a fixed persona: tough, direct, disciplined, and motivational; generic or fluffy
responses are prohibited. No raw LLM output may reach end users. Every generated response MUST
flow through a personality enforcement layer that applies system-prompt constraints and a tone
guard. The LLM client MUST use a DeepInfra-compatible OpenAI SDK interface with configurable
environment values (default base URL https://api.deepinfra.com/v1/openai and default model
zai-org/GLM-4.7-Flash) and MUST remain model-agnostic. The agent architecture MUST support
multi-agent expansion with abstract, composable interfaces where KNOX is Agent 1 of N.

Rationale: the product's differentiator is consistent coaching identity, not generic chatbot output.

### IV. Structured Memory & Identity Integrity
User memory MUST be structured data in Supabase, not raw chat history. The memory schema MUST
include health goals, active routines, weak habits/struggles, motivation style, and health
priorities. All memory reads and writes MUST pass through a dedicated MemoryService; direct access
from route handlers or UI components is prohibited. Users MUST be able to view, edit, and reset
their memory in the UI. User identity MUST be managed via Supabase Auth, and memory records MUST
be scoped to authenticated user IDs. Memory context MUST influence every AI response and MUST NOT
be stored passively without retrieval and application.

Rationale: high-quality coaching depends on durable, structured context applied at response time,
and strict identity scoping prevents cross-user data leakage.

### V. Premium UX Consistency
The user interface MUST feel premium, clean, modern, and minimal across all surfaces. Every screen
MUST use one coherent design language for spacing, typography, and color. Voice interaction and
text chat MUST behave as one unified experience, not separate subsystems. Loading, error, and
empty states MUST always be explicit and user-friendly; placeholder spinners without context are
prohibited. "Coming Soon" modules (Meal Tracking, Recovery, Wearables, Challenges) MUST appear in
the UI and MUST be clearly marked non-functional.

Rationale: trust and perceived quality are product requirements, not cosmetic additions.

### VI. Performance & Responsiveness Standards
First meaningful paint MUST occur within 2 seconds on standard network conditions. AI responses
MUST stream incrementally; blocking until full completion is prohibited. Supabase queries MUST use
indexed access patterns and MUST avoid unfiltered full-table scans. Memory retrieval MUST NOT block
response generation and MUST be parallelized or preloaded at session start.

Rationale: responsiveness is essential for conversational systems and directly impacts engagement.

### VII. Architecture Boundaries & Delivery Simplicity
The UI, API, agent/AI, and memory layers MUST remain independent modules with explicit interfaces.
Frontend code MUST NOT call LLM providers directly; all AI traffic MUST pass through the FastAPI
backend boundary. Environment variables (API keys, base URLs, model names, Supabase config) MUST
be sourced from .env and documented in a schema file; hardcoded secrets/config are prohibited. The
system MUST remain deployable as a single-developer portfolio product and MUST avoid unnecessary
infrastructure beyond Supabase and one backend service unless a documented exception is approved.

Rationale: clear boundaries enable safer iteration, easier testing, and maintainable solo delivery.

## Operational Standards

- Required stack baseline:
	- Frontend: React + TypeScript strict mode.
	- Backend: Python + FastAPI + Pydantic-typed contracts.
	- Memory: Supabase with structured schema and indexed access.
	- LLM access: DeepInfra-compatible OpenAI SDK adapter.
- Engineering constraints:
	- Route handlers orchestrate only; domain/services contain business decisions.
	- Files over 300 lines require decomposition before merge.
	- Public interfaces for agents and memory are stable, typed, and composable.
- Quality gates for merge:
	- Required tests pass for changed scope.
	- Coverage threshold is preserved on critical paths.
	- Persona enforcement and memory influence are validated in tests.
	- UX states (loading/error/empty) are implemented for new screens.

## Speckit Phase Enforcement

- During /speckit.specify:
	- Specs MUST include requirements for typed contracts, memory integration, persona enforcement,
		UX states, and streaming behavior where applicable.
- During /speckit.plan:
	- Constitution Check MUST evaluate each core principle and document pass/fail with mitigation.
	- Project structure decisions MUST preserve layer separation and single-developer deployability.
- During /speckit.tasks:
	- Tasks MUST be organized so testing, persona safeguards, memory integration, and performance
		checks are explicit work items, not implicit assumptions.
- During /speckit.implement:
	- Implementations that violate any MUST rule are non-compliant and MUST be corrected before
		completion.

## Governance

This constitution is authoritative for technical decision-making and supersedes conflicting local
practices. Amendments require: (1) a documented rationale, (2) explicit impact analysis on active
specs/plans/tasks, and (3) updates to affected templates in .specify/templates/. Compliance review
is mandatory in planning and pull request review, and non-compliant changes MUST NOT be merged.
Versioning policy follows semantic intent:
- MAJOR: removing a principle, weakening a MUST requirement, or redefining governance semantics.
- MINOR: adding a new principle/section or materially expanding mandatory guidance.
- PATCH: clarifications, wording refinements, or typo-level changes without behavioral impact.

Enforcement expectations:
- Every plan MUST include a Constitution Check gate before design and after design.
- Every task list MUST map required tests and constraints to concrete file paths.
- Every implementation review MUST verify persona safety, memory usage, and architecture boundaries.

**Version**: 1.1.0 | **Ratified**: 2026-04-08 | **Last Amended**: 2026-04-08
