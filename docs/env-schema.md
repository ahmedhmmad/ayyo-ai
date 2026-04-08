# Environment Schema

This document is the source of truth for environment configuration across Ayyo KNOX MVP.

## Backend (`apps/api/.env`)

- `SUPABASE_URL`: Supabase project URL.
- `SUPABASE_SERVICE_ROLE_KEY`: Service role key for server-side trusted operations.
- `SUPABASE_JWT_SECRET`: JWT verification secret for auth token validation.
- `DEEPINFRA_API_KEY`: API key used by DeepInfra-compatible OpenAI endpoint.
- `OPENAI_BASE_URL`: LLM base URL. Default: `https://api.deepinfra.com/v1/openai`.
- `OPENAI_DEFAULT_MODEL`: Default model id. Default: `zai-org/GLM-4.7-Flash`.
- `MEMORY_IMPLICIT_CONFIDENCE_THRESHOLD`: Float in `[0.0,1.0]` used before storing implicit memory.
- `KNOX_PERSONA_VERSION`: Active persona profile version for guardrail consistency.

## Frontend (`apps/web/.env`)

- `VITE_SUPABASE_URL`: Public Supabase URL for auth flows.
- `VITE_SUPABASE_ANON_KEY`: Public anonymous key for Supabase client auth.
- `VITE_API_BASE_URL`: Base URL for FastAPI backend API and SSE endpoints.

## Rules

- All config values are sourced from `.env`; hardcoded secrets are prohibited.
- Frontend must never hold service-role secrets.
- Backend validates required keys at startup.