# Implementation Plan: KNOX Coach Experience

**Branch**: `001-knox-coach-experience` | **Date**: 2026-04-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-knox-coach-experience/spec.md`

## Summary

Build Ayyo's first specialized agent workspace (KNOX) with streaming chat, structured and identity-scoped memory, in-chat personalized guidance plans, and event-driven accountability check-ins. The technical approach uses a React + TypeScript (strict) Vite frontend and a Python FastAPI backend with SSE streaming, Supabase Auth (magic link only), Supabase Postgres for memory/conversation data, and a model-agnostic DeepInfra-compatible OpenAI client. All user-visible output is routed through a personality enforcement layer and all memory operations through a dedicated MemoryService.

## Technical Context

**Language/Version**: Frontend TypeScript 5.x (strict), Backend Python 3.11  
**Primary Dependencies**: React 18, Vite, FastAPI, Pydantic v2, Supabase SDK, OpenAI Python SDK (DeepInfra-compatible usage)  
**Storage**: Supabase Postgres (conversation + memory + check-ins), Supabase Auth (magic link)  
**Testing**: pytest (unit/integration), React Testing Library + Vitest (interactive UI integration), prompt/persona regression snapshots  
**Target Platform**: Web (modern desktop/mobile browsers) with single backend service deployment  
**Project Type**: Web application (frontend + backend)  
**Performance Goals**: First meaningful paint <=2s on standard connections; first streamed token perceived within 3s for first reply; non-blocking memory fetch on response pipeline  
**Constraints**: No frontend direct LLM calls; route handlers orchestrate only; file size <=300 lines; magic-link-only auth for MVP; event-based check-ins only; voice UI placeholder only; in-chat guidance formatting only  
**Scale/Scope**: MVP single-agent launch (KNOX), initial single-developer portfolio deployment, early-user scale (<10k users)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate (Pass)

- Code-quality architecture rules: **PASS**
  - React + TypeScript strict and FastAPI + Pydantic are mandated in scope.
  - Service/domain ownership defined for chat, memory, inference, check-ins.
  - Modularization approach included to enforce <=300 line files.
- Test strategy coverage: **PASS**
  - Backend service unit tests and interactive frontend integration tests planned.
  - Critical-path >=80% coverage target retained (memory, AI pipeline, persona layer).
  - Prompt/personality regression snapshots included.
- AI/personality/memory architecture: **PASS**
  - No raw output reaches users; personality enforcement layer is mandatory.
  - MemoryService is mandatory for all memory IO.
  - Supabase Auth with authenticated user-id memory scoping is explicit.
  - Multi-agent composable architecture maintained (KNOX as Agent 1 of N).
- UX/performance constraints: **PASS**
  - SSE streaming-first response path selected.
  - FMP <=2s target defined with measurable criteria.
  - Loading/error/empty states required for chat, memory, check-ins.
- Boundary and delivery governance: **PASS**
  - Frontend-to-LLM direct calls forbidden by design.
  - All provider config in .env schema, no hardcoding.
  - Deployable as single backend service + Supabase.

### Post-Design Gate (Pass)

- research.md resolves technology and policy decisions without unresolved clarifications.
- data-model.md defines typed entities and lifecycle transitions for chat, memory, and check-ins.
- contracts/knox-api.yaml defines API/SSE contracts with auth and validation expectations.
- quickstart.md documents reproducible local setup and verification for all critical flows.
- No constitution violations identified requiring complexity exceptions.

## Project Structure

### Documentation (this feature)

```text
specs/001-knox-coach-experience/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── knox-api.yaml
└── tasks.md
```

### Source Code (repository root)

```text
apps/
├── api/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── sse/
│   │   ├── domain/
│   │   ├── services/
│   │   ├── schemas/
│   │   └── integrations/
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── regression/
└── web/
    ├── src/
    │   ├── app/
    │   ├── features/
    │   │   ├── chat/
    │   │   ├── memory/
    │   │   ├── checkins/
    │   │   └── agent-shell/
    │   ├── services/
    │   └── components/
    └── tests/
        └── integration/

packages/
└── shared/
    ├── contracts/
    └── types/
```

**Structure Decision**: Use a monorepo web-application structure under `apps/api` and `apps/web` with optional shared contracts/types in `packages/shared`. This keeps strict separation between UI/API/agent/memory concerns while preserving single-service deployment simplicity.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
