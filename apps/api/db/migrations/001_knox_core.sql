-- Core tables for KNOX MVP

create extension if not exists pgcrypto;

create table if not exists agent_profiles (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  display_name text not null,
  specialty text not null,
  coaching_style text not null,
  description text not null,
  status text not null check (status in ('active', 'coming_soon'))
);

create table if not exists conversation_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  agent_slug text not null,
  started_at timestamptz not null default now(),
  last_message_at timestamptz not null default now(),
  status text not null default 'active' check (status in ('active', 'archived'))
);

create table if not exists conversation_messages (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references conversation_sessions(id) on delete cascade,
  role text not null check (role in ('user', 'assistant', 'system')),
  content text not null,
  created_at timestamptz not null default now(),
  stream_state text not null default 'complete' check (stream_state in ('complete', 'interrupted')),
  persona_passed boolean not null default true
);

create table if not exists user_memory_records (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  category text not null check (category in ('health_goal', 'active_routine', 'struggle', 'motivation_style', 'health_priority')),
  key text not null,
  value text not null,
  source_type text not null check (source_type in ('explicit', 'implicit')),
  confidence_score numeric(3,2) not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  is_active boolean not null default true
);

create index if not exists idx_user_memory_user_id on user_memory_records(user_id);
create index if not exists idx_sessions_user_id on conversation_sessions(user_id);

create table if not exists memory_audit_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  memory_record_id uuid,
  action text not null check (action in ('create', 'update', 'delete', 'reset_all')),
  action_at timestamptz not null default now()
);

create table if not exists commitments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  session_id uuid,
  statement text not null,
  target_window text,
  created_at timestamptz not null default now(),
  status text not null default 'open' check (status in ('open', 'completed', 'missed', 'replaced'))
);

create table if not exists checkin_prompts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  commitment_id uuid references commitments(id) on delete cascade,
  trigger_event text not null check (trigger_event in ('commitment_created', 'commitment_due', 'commitment_missed', 'user_requested')),
  prompt_text text not null,
  created_at timestamptz not null default now(),
  status text not null default 'pending' check (status in ('pending', 'answered', 'expired'))
);

create table if not exists checkin_responses (
  id uuid primary key default gen_random_uuid(),
  prompt_id uuid not null references checkin_prompts(id) on delete cascade,
  user_id uuid not null,
  response_text text not null,
  outcome text not null check (outcome in ('complete', 'partial', 'not_complete')),
  responded_at timestamptz not null default now()
);

create table if not exists guidance_plan_snapshots (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  session_id uuid,
  source_message_id uuid,
  title text not null,
  steps_json jsonb not null,
  constraints_used_json jsonb not null,
  created_at timestamptz not null default now()
);
