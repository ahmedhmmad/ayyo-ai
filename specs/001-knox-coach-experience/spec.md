# Feature Specification: KNOX Coach Experience

**Feature Branch**: `001-knox-coach-experience`  
**Created**: 2026-04-08  
**Status**: Draft  
**Input**: User description: "Build KNOX, a specialized AI health and discipline agent inside Ayyo, including chat, memory, personalized guidance, accountability check-ins, platform shell, and longevity framing."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Persistent KNOX Chat (Priority: P1)

As an authenticated user, I open KNOX and have a continuous coaching conversation where replies stream progressively, stay in KNOX's voice, and persist when I return.

**Why this priority**: This is the core product interaction and the minimum experience required for users to trust KNOX as a real coach instead of a generic chatbot.

**Independent Test**: Can be fully tested by starting a new chat, sending messages, verifying streamed replies in-character, leaving the app, and confirming history remains available after return.

**Acceptance Scenarios**:

1. **Given** an authenticated user opens KNOX for the first time, **When** the chat screen loads, **Then** the user sees KNOX identity elements (name, role, and coaching character) before sending a message.
2. **Given** an authenticated user sends a message, **When** KNOX responds, **Then** the response appears progressively and maintains a direct, action-oriented tone.
3. **Given** an authenticated user has prior KNOX messages, **When** they leave and later return, **Then** prior conversation history is shown in chronological order in the same workspace.

---

### User Story 2 - Memory Visibility and Control (Priority: P1)

As an authenticated user, I can see, edit, delete, and reset what KNOX remembers, and KNOX uses that memory in later conversations.

**Why this priority**: Personalized continuity is the main differentiator; users must trust both usefulness and control of remembered context.

**Independent Test**: Can be tested by creating memory via conversation, opening the memory panel, editing/deleting/resetting entries, and validating response behavior changes accordingly in later chat.

**Acceptance Scenarios**:

1. **Given** KNOX has inferred goals/habits/struggles/motivation preferences, **When** the user opens memory, **Then** the memory panel shows these entries in a readable structured form.
2. **Given** the user edits or deletes a memory entry, **When** they continue chatting, **Then** KNOX uses updated memory and no longer uses deleted context.
3. **Given** the user resets all memory, **When** they send a new prompt, **Then** KNOX responds without previously stored user-specific memory and starts rebuilding context from new interactions.

---

### User Story 3 - Personalized Guidance Plans (Priority: P2)

As an authenticated user, I can ask KNOX for workout and habit plans that are personalized to my goals, schedule, constraints, and past outcomes.

**Why this priority**: Actionable personalized planning is the core paid value and turns conversations into real behavior change.

**Independent Test**: Can be tested by providing constraints and history, requesting a plan, requesting revisions, and verifying each output remains specific and actionable.

**Acceptance Scenarios**:

1. **Given** the user shares constraints (for example available time and disliked activities), **When** they request a plan, **Then** KNOX returns a structured plan aligned to those constraints.
2. **Given** the user asks follow-up questions or requests changes, **When** KNOX revises the plan, **Then** revisions preserve continuity with user context and include clear next actions.
3. **Given** the user previously failed a habit, **When** they request a new strategy, **Then** KNOX acknowledges prior outcomes and proposes an adjusted approach rather than repeating a generic recommendation.

---

### User Story 4 - Accountability Check-ins (Priority: P2)

As an authenticated user, I receive short, commitment-based check-ins from KNOX and can respond directly so KNOX can adapt next steps.

**Why this priority**: Follow-up accountability is a primary retention driver and key reason users choose a dedicated coach.

**Independent Test**: Can be tested by creating a commitment in chat, triggering a check-in cycle, responding with success/failure, and verifying appropriate follow-up behavior.

**Acceptance Scenarios**:

1. **Given** the user commits to a goal in chat, **When** check-ins are generated, **Then** prompts reference the specific commitment and feel personal rather than generic.
2. **Given** the user confirms completion, **When** KNOX responds, **Then** KNOX briefly acknowledges progress and advances to the next action.
3. **Given** the user reports non-completion, **When** KNOX responds, **Then** KNOX avoids shaming language and reframes toward an immediate recovery action.

---

### User Story 5 - Agent Shell and KNOX Positioning (Priority: P3)

As a user entering Ayyo, I see KNOX presented as a premium specialized agent, can enter KNOX's workspace, and can view other agent slots as clearly marked Coming Soon.

**Why this priority**: Clear platform framing improves trust and conveys intentional product direction without pretending unfinished agents are available.

**Independent Test**: Can be tested by launching the app, confirming KNOX profile details on home, entering KNOX workspace, and verifying non-KNOX slots are visible but non-interactive.

**Acceptance Scenarios**:

1. **Given** the user opens Ayyo home, **When** agent cards render, **Then** KNOX's name/specialty/style are visible and selectable.
2. **Given** the user selects KNOX, **When** workspace opens, **Then** visual and textual framing clearly indicate this is KNOX's dedicated environment.
3. **Given** other agent slots are shown, **When** the user views them, **Then** each is labeled Coming Soon and cannot be started.

---

### User Story 6 - Longevity-Framed Coaching (Priority: P3)

As an authenticated user, I receive long-term health framing inside normal KNOX responses so daily actions connect to future outcomes.

**Why this priority**: Longevity framing increases motivation and positions KNOX above commodity fitness assistants.

**Independent Test**: Can be tested by asking about sleep/nutrition/training topics and verifying responses include relevant long-term consequences in natural conversational format.

**Acceptance Scenarios**:

1. **Given** the user asks about sleep habits, **When** KNOX answers, **Then** guidance includes practical short-term action and relevant long-term health implications.
2. **Given** the user asks about nutrition, **When** KNOX answers, **Then** KNOX connects recommendations to sustained energy, disease-risk reduction, or long-term performance.
3. **Given** the user asks for direct next steps, **When** KNOX responds, **Then** longevity framing is integrated naturally and not presented as detached tips.

---

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- A user has no prior memory: KNOX must still provide clear coaching and begin memory capture without implying known history.
- A user resets memory and immediately asks for guidance: KNOX must not reference pre-reset data.
- A user has conflicting goals or constraints (for example fat loss plus very limited schedule): KNOX must request prioritization and provide a feasible first step.
- Check-in prompts are overdue or missed: KNOX must recover without duplicate spam-like prompts.
- Conversation history retrieval is delayed: the UI must communicate state clearly and prevent blank/ambiguous failure states.
- Streaming response is interrupted mid-message: user receives a clear retry/continue path without losing context.
- Unauthorized or expired session: user must be prompted to re-authenticate before any memory-bound data is shown.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST present KNOX as a distinct agent identity with name, specialty, and coaching style in both platform entry and dedicated workspace.
- **FR-002**: System MUST allow authenticated users to send chat messages to KNOX and receive streamed, incremental responses.
- **FR-003**: System MUST persist conversation history for each authenticated user so prior KNOX exchanges remain available across sessions.
- **FR-004**: System MUST enforce KNOX persona constraints so user-visible responses remain direct, disciplined, motivational, and non-generic.
- **FR-005**: System MUST route all user-visible model responses through a personality enforcement step before display.
- **FR-006**: System MUST capture and maintain structured user memory that includes goals, routines, struggles, motivation style, and health priorities.
- **FR-007**: System MUST scope all memory records to authenticated user identity and prevent cross-user memory access.
- **FR-008**: Users MUST be able to view, edit, delete individual memory items, and reset all memory from a dedicated memory panel.
- **FR-009**: System MUST apply relevant memory context in every KNOX response where user-specific context exists.
- **FR-010**: System MUST generate personalized workout and habit guidance that reflects user goals, constraints, and prior outcomes.
- **FR-011**: System MUST support follow-up refinement of guidance plans through conversational iteration without losing context.
- **FR-012**: System MUST generate commitment-based accountability check-ins tied to prior user commitments.
- **FR-013**: System MUST allow users to respond to check-ins directly in KNOX chat and receive adaptive follow-up based on outcome.
- **FR-014**: System MUST present non-KNOX agent slots as visible but clearly non-functional Coming Soon entries.
- **FR-015**: System MUST integrate longevity framing into coaching responses for relevant topics (sleep, nutrition, training, recovery) as part of natural conversation.
- **FR-016**: System MUST provide explicit user feedback states for loading, empty, and error conditions in chat, memory, and check-in experiences.
- **FR-017**: System MUST preserve user trust by preventing raw system internals, raw model output, or unformatted metadata from appearing in end-user responses.
- **FR-018**: System MUST preserve the following as out of scope for this feature release: meal logging/calorie tracking, wearables integration, real phone/video calls, social/community features, and interaction with agents other than KNOX.
- **FR-019**: System MUST handle user authentication through Supabase Auth using either email/password or magic link sign-in.

### Constitution Alignment *(mandatory)*

- **CA-001 Code Quality**: Feature scope must comply with constitution-mandated typed frontend/backend quality standards, descriptive naming, and modular boundaries.
- **CA-002 Layer Boundaries**: Business decisions for chat, memory, guidance generation, and check-ins belong to domain/service layers; interface handlers remain orchestration-only.
- **CA-003 Testing**: Test design must include backend service tests, interactive UI flow tests, and regression coverage for memory influence and KNOX personality consistency on critical paths.
- **CA-004 Personality Safety**: All user-visible responses must pass persona enforcement so KNOX tone is consistently direct and action-oriented.
- **CA-005 Memory Integration**: Memory retrieval/update must occur through dedicated memory application flows and must influence subsequent responses.
- **CA-005a Identity Scoping**: User identity governs all memory access, and memory operations are authorized and scoped per authenticated user.
- **CA-006 UX Quality**: Chat, check-ins, and memory panel must provide cohesive UX with explicit loading, empty, and error behaviors.
- **CA-007 Performance**: Response delivery must be streaming-first, and memory retrieval must not block initial response generation.
- **CA-008 Configuration Governance**: Provider and environment configuration are externalized and must not be embedded in feature behavior definitions.

### Key Entities *(include if feature involves data)*

- **AgentProfile**: Public-facing identity definition for a specialized agent including display name, specialty, coaching style summary, and availability state.
- **ConversationSession**: A user-agent conversation container with status, timestamps, and ordered message references.
- **ConversationMessage**: A single inbound or outbound turn containing speaker role, content, timestamp, and stream completion state.
- **UserMemoryRecord**: Structured memory item tied to one authenticated user, categorized by goals, routines, struggles, motivation style, or priorities, with edit/delete/reset auditability.
- **GuidancePlan**: Structured personalized workout or habit strategy generated from user context, constraints, and previous outcomes.
- **Commitment**: A user-declared goal or promise with intended timeframe and expected check-in cadence.
- **CheckInPrompt**: A generated accountability prompt linked to a specific commitment and follow-up state.
- **CheckInResponse**: User reply to a check-in with outcome status and next-action intent.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 95% of authenticated users can send a first message and receive the first streamed KNOX response within 3 seconds of submit under normal load.
- **SC-002**: 95% of returning users can view prior KNOX conversation history within 2 seconds of entering the agent workspace.
- **SC-003**: At least 90% of sampled KNOX responses in acceptance testing are rated as persona-consistent (direct, disciplined, motivational, non-generic) by predefined rubric.
- **SC-004**: At least 85% of users who create at least one memory-backed goal receive responses that reference relevant prior context in subsequent sessions.
- **SC-005**: At least 80% of users can successfully edit or reset memory from the memory panel on first attempt without support.
- **SC-006**: At least 70% of users who receive check-ins respond to at least one prompt within 7 days of commitment creation.
- **SC-007**: At least 80% of generated guidance plans include user-specific constraints and clear step-by-step actions according to acceptance rubric.

## Assumptions

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right assumptions based on reasonable defaults
  chosen when the feature description did not specify certain details.
-->

- Users interact with KNOX only after authentication and have one primary personal profile.
- Authentication onboarding is intentionally minimal for this release and is not treated as a primary product feature.
- This feature release targets one specialized agent (KNOX) and intentionally excludes live interactions with additional agents.
- Check-in delivery appears in-app (home/workspace prompts) for this release; external push channels are not required.
- Memory records are user-editable and should prefer clarity over exhaustive historical transcript detail.
- Guidance plans are advisory coaching content and do not replace professional medical diagnosis or treatment.
- Standard network variability exists; users may occasionally experience partial streaming interruptions that require retry.

## Out of Scope

- Meal logging or calorie tracking workflows.
- Wearable device data ingestion or sync.
- Real phone calls, video calls, or telephony experiences.
- Social/community features, leaderboards, or peer accountability loops.
- Any interactive agent beyond KNOX (other slots remain Coming Soon only).
