# Workflow Orchestration PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `workflow_orchestration`. The items focus on long-running process execution, state-machine governance, saga coordination, timers, human work, compensation, SLA control, exception management, and agent-safe workflow authoring.

## Current Domain Evidence Used

- Domain purpose: workflow definition catalogs, executable state machines, instance state, saga steps, timers, signals, compensation, human work, policy gates, telemetry, retry evidence, and release evidence.
- Owned boundary: workflow definitions, versions, instances, signals, transition guards, timers, retry policies, SLA policies, escalation rules, saga steps, compensations, human tasks, task assignments, approval decisions, integration endpoints, event correlations, metric snapshots, exception cases, simulations, policy screenings, completion proofs, audit entries, governed model evidence, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command surface: configure runtime, define/publish workflows, register guards, start/signal instances, schedule timers, register retry/SLA/escalation policy, record saga steps, execute compensation, assign human tasks, record approvals, register endpoints, correlate events, capture metrics, open exception cases, record simulations, screen policy, record completion proof, append audit entries, and verify owned-table boundaries.
- Existing events and dependencies: emits `WorkflowDefinitionPublished`, `WorkflowStarted`, `WorkflowSignalAccepted`, `SagaStepCompleted`, `TimerScheduled`, `CompensationExecuted`, and `WorkflowCompleted`; consumes business and platform events through AppGen-X projections without sharing tables.

## 50 Better-Than-World-Class Improvements

### 1. Workflow definition correctness proof

**Justification:** A workflow definition can be syntactically valid while containing unreachable states, dead ends, unguarded transitions, duplicate terminal paths, or impossible compensation order.

**Improvement:** Add a definition verifier that proves state reachability, terminal completeness, guard coverage, compensation reversibility, timer validity, participant endpoint availability, and version compatibility before publication. Store the proof with the workflow version and expose failures in the state-machine designer.

### 2. Visual state-machine diffing

**Justification:** Operators need to understand how a new workflow version differs from the active one before shifting live instances.

**Improvement:** Implement structural and semantic diffs for states, transitions, guards, timers, participant calls, human tasks, and compensation paths. The UI should highlight added, removed, renamed, and behavior-changing nodes with release impact evidence.

### 3. Instance migration planner

**Justification:** Long-running workflows can remain active across definition versions; upgrading them without a plan risks stranded or invalid state.

**Improvement:** Add migration plans that map old states to new states, specify in-flight task behavior, preserve correlation keys, handle timers, and validate compensation compatibility. Block version activation when active instances cannot be migrated or intentionally pinned.

### 4. Deterministic signal admission

**Justification:** Duplicate, stale, out-of-order, or unauthorized signals can corrupt workflow state if admission logic is loose.

**Improvement:** Add a signal admission engine that checks correlation, expected current state, sender PBC, schema version, idempotency key, ordering policy, replay window, and access policy projection. Persist accepted and rejected decisions with exact guard explanations.

### 5. Correlation-key strategy governance

**Justification:** Incorrect correlation keys cause events to start duplicate instances, update the wrong instance, or fail to join existing cases.

**Improvement:** Define correlation strategies per workflow, including key fields, tenant scope, source event types, uniqueness window, conflict behavior, and merge policy. Add simulations using historical events to validate the strategy before activation.

### 6. Saga participant contract registry

**Justification:** A saga step is only safe when the participant command, idempotency semantics, timeout, compensation command, and emitted event expectations are explicit.

**Improvement:** Add participant contract records linked to integration endpoints, declared APIs, schema contracts, idempotency requirements, compensation capability, retry policy, and side-effect class. Saga steps should reference certified participant contracts rather than loose command names.

### 7. Compensation completeness analysis

**Justification:** Incomplete compensation paths create irrecoverable partial failures in financial, order, inventory, and service workflows.

**Improvement:** Analyze every side-effecting step for compensating action, compensation preconditions, irreversible side effects, manual fallback, evidence requirements, and approval gate. Workflows with uncompensated high-risk steps should fail release evidence.

### 8. Compensation rehearsal mode

**Justification:** Compensation logic is often untested until a real failure occurs.

**Improvement:** Add rehearsal runs that simulate failed saga steps and execute compensation in non-mutating preview mode using owned evidence and declared API contracts. Store expected order, blocked actions, manual tasks, and recovery confidence.

### 9. Timer precision and calendar policy

**Justification:** Timers need business calendars, jurisdiction-specific holidays, maintenance windows, time zones, daylight-saving handling, and jitter semantics.

**Improvement:** Extend timer policies with calendar references, timezone resolution, holiday behavior, grace periods, jitter limits, breach calculation mode, and maintenance exclusions. The timer console should preview exact fire times before scheduling.

### 10. SLA burn and breach forecasting

**Justification:** SLA control should predict breach risk early enough to reassign work or escalate, not merely record that a breach happened.

**Improvement:** Forecast SLA burn for workflow instances using remaining steps, queue load, task assignments, timer deadlines, participant health, and historical durations. Surface breach probability and recommended interventions in the workbench.

### 11. Human task assignment optimizer

**Justification:** Human work depends on skill, authority, workload, availability, conflict of interest, escalation group, and task sensitivity.

**Improvement:** Add assignment policies that rank eligible groups/users by skill, permission, current load, SLA risk, segregation-of-duties constraints, and continuity. Store assignment rationale and allow manual override with audit reason.

### 12. Four-eyes and segregation-of-duties controls

**Justification:** Approval workflows often require separation between requester, preparer, approver, compensator, and auditor.

**Improvement:** Add SoD constraints to human tasks and approval decisions, using identity projections to prevent conflicted approvals. Release tests should prove a user cannot approve their own restricted task or compensate a step they executed when policy forbids it.

### 13. Escalation routing playbooks

**Justification:** Escalations need structured recipients, urgency, communication mode, expiry, and fallback path rather than a single assignee group.

**Improvement:** Model escalation playbooks with trigger, recipient chain, notification route, evidence needed, timeout, fallback group, and closure criteria. The UI should show active escalation ladder and missed handoffs.

### 14. Exception case management

**Justification:** Workflow exceptions are cases with root cause, impact, tasks, decisions, and closure evidence, not only error flags.

**Improvement:** Expand exception cases with classification, severity, impacted instances, customer/business impact, owner, remediation tasks, related dead letters, decision log, and post-resolution review. The agent should summarize cases and draft next-step plans.

### 15. Workflow replay and time travel

**Justification:** Auditors and debuggers need to reconstruct an instance exactly as it progressed and inspect alternate decisions.

**Improvement:** Implement replay from workflow events, signals, timers, task decisions, and saga results with as-of policy versions. Provide timeline and state snapshots plus a non-mutating counterfactual replay mode.

### 16. Long-running idempotency ledger

**Justification:** Workflow idempotency must survive retries, restarts, duplicate signals, human resubmits, and participant timeouts across long durations.

**Improvement:** Add idempotency ledger entries for instance starts, signals, saga steps, compensations, human decisions, and timer firings. Include scope, TTL, result replay, conflict state, and release tests for duplicate suppression.

### 17. Retry policy by failure class

**Justification:** Transient network failure, validation error, policy denial, timeout, participant rejection, and concurrency conflict require different retry behavior.

**Improvement:** Extend retry policies with failure-class matching, max attempts, backoff, jitter, escalation, circuit-breaker interaction, and no-retry reasons. Store retry decisions and expose them in saga and timer views.

### 18. Parallel branch join semantics

**Justification:** Parallel workflow branches need explicit join behavior for all-success, quorum, first-success, timeout, cancellation, and partial compensation.

**Improvement:** Add join node descriptors with branch cardinality, required outcomes, timeout behavior, cancellation propagation, compensation policy, and data merge rules. The verifier should reject ambiguous joins.

### 19. Data minimization for workflow context

**Justification:** Workflow context payloads easily become hidden shared business records or leak sensitive data across PBC boundaries.

**Improvement:** Add context schemas with allowed fields, redaction, retention, source event references, projection snapshots, and forbidden foreign-table data. The agent should warn when a workflow definition attempts to persist another PBC's domain data rather than a projection reference.

### 20. Workflow variable lineage

**Justification:** Decisions depend on variables derived from signals, human tasks, projections, and participant responses.

**Improvement:** Track variable lineage, source event, transformation, guard usage, human override, and retention policy. UI drilldowns should show why a guard passed or failed using variable provenance.

### 21. Policy gate test suites

**Justification:** Transition guards and policy screens need executable examples, not just expressions.

**Improvement:** Require guard fixtures covering pass, fail, missing data, stale projection, and conflicting policy cases. Compile guards with tests and store pass/fail evidence before workflow publication.

### 22. Workflow version rollout controller

**Justification:** Publishing a workflow version should not immediately move all traffic without staged exposure and rollback.

**Improvement:** Add rollout plans with eligible tenants, percentage, cohorts, new-instance routing, active-instance migration, success metrics, pause thresholds, and rollback version. Emit rollout events through AppGen-X evidence.

### 23. Business calendar simulation

**Justification:** Workflow duration and breach risk depend heavily on calendars and workload windows.

**Improvement:** Simulate workflow instances across business calendars, holidays, shifts, maintenance windows, and timer policies. Show expected completion distributions and high-risk steps before activation.

### 24. Cross-PBC dependency health

**Justification:** Workflow execution depends on gateway, schema, identity, audit, and participant PBC APIs/events.

**Improvement:** Track dependency projection freshness, API endpoint health, schema acceptance, permission policy state, and recent dead letters per participant. Use dependency health to pause starts, reroute tasks, or open exception cases.

### 25. Participant timeout negotiation

**Justification:** A workflow's timeout must align with participant API contracts, retry budgets, and compensation windows.

**Improvement:** Add timeout negotiation checks between workflow steps and participant contract projections. Block steps whose timeout is shorter than the participant's accepted behavior or longer than SLA/compensation safety permits.

### 26. Workflow observability model

**Justification:** Generic metrics are insufficient for workflow operations.

**Improvement:** Add metrics for instance starts, completions, stuck states, timer lag, signal rejection, step retries, compensation rate, human-task aging, escalation count, SLA burn, and version rollout health. Workbench panels should allow filtering by workflow, tenant, version, state, and owner.

### 27. Stuck-instance detector

**Justification:** Workflows can stall silently because a signal never arrives, a timer was misconfigured, a human task is unassigned, or a participant response was lost.

**Improvement:** Detect stuck instances using expected next events, timers, queue state, SLA policies, participant health, and historical durations. Open exception cases with likely cause and recovery recommendations.

### 28. Dead-letter guided recovery

**Justification:** Workflow dead letters often require careful replay, compensation, or manual correction.

**Improvement:** Build a dead-letter recovery workbench that groups failures by workflow, handler, event type, tenant, projection, and retry age. Provide replay preview, duplicate-risk analysis, compensation impact, and audit-safe closure.

### 29. Human task form contracts

**Justification:** Human tasks need structured forms, validations, evidence attachments, and decision semantics.

**Improvement:** Add form descriptors for each human task with required fields, attachments, validation rules, permitted decisions, default comments, and redaction. Generated UI should render these forms rather than generic approval records.

### 30. Attachment and evidence handling

**Justification:** Approvals and exceptions often rely on documents, screenshots, or external references.

**Improvement:** Add evidence descriptors with type, source, checksum, classification, retention, task link, decision link, and access policy. The agent should ingest instructions/documents into draft evidence records without embedding sensitive content into unrelated tables.

### 31. Agent-assisted workflow authoring

**Justification:** Users want to describe processes in natural language, but the agent must produce precise, testable definitions.

**Improvement:** Give the PBC agent a workflow-authoring skill that extracts states, transitions, participants, timers, approvals, exceptions, compensations, and SLAs from instructions. It should create draft definitions with validation findings and require approval before publication.

### 32. Agent-safe operational actions

**Justification:** Agents can help with stuck workflows, but mutating live orchestration state is risky.

**Improvement:** Require agent action previews for signal replay, timer reschedule, task reassignment, compensation execution, exception closure, and workflow cancellation. Each preview should include records touched, events emitted, rollback options, and required permission.

### 33. Workflow cancellation semantics

**Justification:** Cancellation is not just setting a status; it may need timers canceled, tasks withdrawn, participants notified, and compensation evaluated.

**Improvement:** Model cancellation policies with allowed states, requester roles, participant notifications, human task closure, compensation decision, timer cleanup, and completion proof. Add tests for cancellation idempotency.

### 34. Suspend and resume controls

**Justification:** Operators need to pause workflows during incidents, dependency outages, or policy review without losing state.

**Improvement:** Add suspend/resume commands with scope, reason, expiry, allowed incoming signals, timer behavior, and release evidence. UI should show suspended definitions and instances clearly.

### 35. Workflow template library

**Justification:** Many PBC compositions need reusable approval, fulfillment, exception, onboarding, and reconciliation patterns.

**Improvement:** Add package-local workflow templates with parameterized states, tasks, participant roles, SLAs, and compensation patterns. Templates should generate draft definitions and tests, not bypass publication gates.

### 36. Process mining from event history

**Justification:** Real execution often differs from designed workflow, revealing bottlenecks and shadow processes.

**Improvement:** Mine workflow event history to discover common paths, skipped steps, loops, delays, rework, and compensation hotspots. Provide recommendations tied to concrete definition changes and simulation evidence.

### 37. Bottleneck and capacity planning

**Justification:** Workflow throughput depends on human queues, participant capacity, retry storms, and timer spikes.

**Improvement:** Add capacity models for human groups, participant endpoints, timers, and saga steps. Forecast queue growth and recommend staffing, rate limits, or staged rollout changes.

### 38. Completion proof enrichment

**Justification:** A completion proof should demonstrate that required states, approvals, compensations, and audit entries exist, not merely hash a final status.

**Improvement:** Build completion proofs from instance timeline, terminal state, mandatory steps, approval decisions, compensation status, policy screenings, and audit hashes. Expose proof validation in release and workbench views.

### 39. Immutable audit with redaction views

**Justification:** Workflow audit entries must be tamper-evident while still protecting sensitive context payloads and human comments.

**Improvement:** Store hash-chained audit entries with redacted display views, classified payload references, actor, command, state transition, and source event. Provide audit export filters by tenant, workflow, instance, and decision.

### 40. Workflow-specific RBAC and ABAC

**Justification:** Permissions differ by definition owner, task assignee, tenant, state, sensitivity, and emergency status.

**Improvement:** Extend permissions with workflow-scoped actions, task ownership, emergency override, data classification, and state-aware constraints. The UI should hide actions that fail both static RBAC and dynamic policy checks.

### 41. Release readiness checklist

**Justification:** Workflow releases need more than schema depth; they require operational safety evidence.

**Improvement:** Add release gates for definition proof, guard tests, participant contracts, compensation coverage, timer policy, SLA policy, human task forms, rollout plan, dependency health, audit coverage, and agent competencies.

### 42. Tenant isolation test harness

**Justification:** Multi-tenant workflow engines risk cross-tenant correlation, task visibility, timer leakage, or shared exception queues.

**Improvement:** Add tests and release evidence for tenant-scoped correlation keys, instance queries, human queues, escalation rules, metrics, dead letters, and agent responses. Block package release on cross-tenant leakage.

### 43. Workflow data retention and purge

**Justification:** Long-running workflows accumulate context, evidence, audit entries, and samples that must be retained or purged by policy.

**Improvement:** Add retention policies per workflow, state, evidence type, and tenant, with legal hold support and purge proof. Agent and UI views should warn when a workflow stores data beyond retention needs.

### 44. External deadline and blackout calendar ingestion

**Justification:** Workflows often depend on regulatory deadlines, partner calendars, or operational blackout periods.

**Improvement:** Add projection-backed calendar ingestion with source, validity, tenant, and priority. Timers and SLA calculations should use these calendars without directly sharing external tables.

### 45. Incident-mode workflow controls

**Justification:** During major incidents, teams need special routing, approval shortcuts, freezes, or compensation constraints.

**Improvement:** Add incident-mode policies with activation reason, scope, expiry, allowed workflow changes, blocked starts, expedited approvals, and post-incident review. Store all incident-mode actions in completion and audit evidence.

### 46. Workflow explainability panel

**Justification:** Operators need to know why an instance is in its current state and what can happen next.

**Improvement:** Add an explainability panel showing current state, entering event, variables used, active timers, pending tasks, allowed signals, blocked transitions, next possible states, and policy reasons. The agent should answer these questions from owned evidence only.

### 47. Cross-version analytics

**Justification:** New workflow versions should be compared against prior versions for improvement or regression.

**Improvement:** Track completion time, stuck rate, compensation rate, human rework, SLA breaches, and exception counts by workflow version. Rollout plans should auto-pause on statistically meaningful regressions.

### 48. Boundary proof for orchestration-only ownership

**Justification:** Workflow orchestration coordinates domains but must not become a shared data store for invoices, orders, shipments, identities, or schemas.

**Improvement:** Add static and runtime release checks proving all commands use owned workflow tables plus declared APIs/events/projections. Include fixtures that attempt direct business-table reads and verify boundary rejection.

### 49. DSL expressiveness for workflow and agent skills

**Justification:** Composed applications must express workflows, human tasks, compensation, and workflow-agent skills in the AppGen-X DSL.

**Improvement:** Add DSL descriptors for workflow definitions, participant contracts, timers, human tasks, compensation policies, rollout plans, and agent competencies. Generated DSL should round-trip into the package runtime without losing release evidence.

### 50. Workflow competency catalog for composed agents

**Justification:** The single composed application agent must know when it can delegate to workflow orchestration skills and when it must ask for approval.

**Improvement:** Publish competencies for workflow authoring, stuck-instance triage, compensation planning, SLA risk explanation, dead-letter recovery, human-task reassignment, and release-readiness review. Each competency should declare permissions, safe reads, mutation previews, document inputs, and emitted AppGen-X events.
