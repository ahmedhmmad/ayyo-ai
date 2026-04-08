-- RLS policies for authenticated user scope

alter table if exists conversation_sessions enable row level security;
alter table if exists conversation_messages enable row level security;
alter table if exists user_memory_records enable row level security;
alter table if exists memory_audit_events enable row level security;
alter table if exists commitments enable row level security;
alter table if exists checkin_prompts enable row level security;
alter table if exists checkin_responses enable row level security;
alter table if exists guidance_plan_snapshots enable row level security;

drop policy if exists p_sessions_owner on conversation_sessions;
create policy p_sessions_owner on conversation_sessions
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_memory_owner on user_memory_records;
create policy p_memory_owner on user_memory_records
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_audit_owner on memory_audit_events;
create policy p_audit_owner on memory_audit_events
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_commitments_owner on commitments;
create policy p_commitments_owner on commitments
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_prompts_owner on checkin_prompts;
create policy p_prompts_owner on checkin_prompts
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_responses_owner on checkin_responses;
create policy p_responses_owner on checkin_responses
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists p_guidance_owner on guidance_plan_snapshots;
create policy p_guidance_owner on guidance_plan_snapshots
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
