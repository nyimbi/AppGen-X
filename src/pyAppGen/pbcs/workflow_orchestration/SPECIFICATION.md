# Workflow Orchestration PBC

## Purpose

Workflow Orchestration is the AppGen-X package that owns long-running process
coordination. It is responsible for workflow definition catalogs, executable
state machines, instance state, saga steps, timers, signals, compensation,
human work, policy gates, telemetry, retry evidence, and release evidence. It
coordinates other PBCs without sharing their tables. Cross-PBC activity is
represented only through declared APIs, AppGen-X events, and read-only
projections consumed through the package inbox.

The package is intentionally package-local. Its runtime, UI contract, source
registration metadata, and tests live under `src/pyAppGen/pbcs/workflow_orchestration`
and prove the same surfaces that generated applications must receive: owned
schema, migrations/schema descriptors, models, services, routes, event
contracts, handlers, workbench fragments, permissions, configuration schema,
rules, parameters, seed evidence, and release gates.

## Owned Datastore Boundary

The PBC owns exactly these logical tables:

- `workflow_definition`: tenant-scoped workflow key, semantic version, owner
  PBC, state list, transition graph, participant list, activation status, and
  definition invariants.
- `workflow_version`: publishable workflow version record with semantic
  version, status, workflow link, and release hash.
- `workflow_instance`: immutable lifecycle projection for a running or
  completed workflow, correlation ID, context payload, current state, history,
  tenant, and status.
- `workflow_signal`: accepted or rejected external signals with source PBC,
  payload, validation result, transition decision, and correlation key.
- `workflow_transition_guard`: compiled transition guard expressions for state,
  signal, and workflow-safe admission checks.
- `timer_task`: deadline, wake-up command, breach risk, jitter, retry budget,
  escalation state, and scheduling evidence.
- `workflow_retry_policy`: tenant-scoped retry budget, maximum attempts,
  backoff strategy, and status for workflow or participant operations.
- `workflow_sla_policy`: SLA threshold, severity, workflow binding, and
  activation evidence.
- `workflow_escalation_rule`: breach trigger, target group, status, and policy
  evidence for escalation routing.
- `saga_step`: participant PBC, command name, status, duration, idempotency
  key, completion flag, and compensation link.
- `compensation`: compensation command, failure reason, execution status, and
  side-effect boundary.
- `human_task`: approval or exception work item, assignee group, SLA, decision,
  escalation state, and evidence payload.
- `human_task_assignment`: auditable task assignment by group, instance, status,
  and assignment key.
- `workflow_approval_decision`: final approval decision, decider, task link,
  status, and evidence hash.
- `workflow_integration_endpoint`: declared participant PBC API route endpoint
  used by orchestration without sharing datastore tables.
- `workflow_event_correlation`: source event, business key, instance link, and
  tenant-scoped correlation evidence.
- `workflow_metric_snapshot`: point-in-time workflow telemetry, completion
  rate, compensation count, and audit hash.
- `workflow_exception_case`: exception type, severity, recommended action,
  instance link, and status.
- `workflow_simulation_run`: counterfactual simulation scenario, risk delta,
  workflow link, and result status.
- `workflow_policy_screening`: policy decision, workflow link, screening state,
  and evidence hash.
- `workflow_completion_proof`: sealed completion proof hash, proof type,
  instance link, and release status.
- `workflow_audit_entry`: immutable action log with payload hash and sealed
  status.
- `workflow_governed_model_evidence`: governed model metrics, drift score,
  approval state, and model evidence hash.
- `workflow_rule`: executable rules for signal admission, saga compensation,
  timer escalation, approval routing, release gates, and policy screening.
- `workflow_parameter`: numeric and textual runtime parameters that tune retry,
  SLA, compensation, parallelism, review, and workbench behavior.
- `workflow_configuration`: database backend, event topic, retry limit,
  timezone, versioning mode, allowed signal sources, and workbench limits.

Runtime event tables are also package-owned:
`workflow_orchestration_appgen_outbox_event`,
`workflow_orchestration_appgen_inbox_event`, and
`workflow_orchestration_dead_letter_event`. These are AppGen-X event contract
tables, not user-selectable streaming infrastructure. Ordinary backing stores
are limited to PostgreSQL, MySQL, and MariaDB. The runtime rejects any other
backend and rejects configuration fields that would expose event transport or
stream-engine selection.

Schema extensions are schema-on-read additions to owned tables only. The
runtime accepts extensions such as `context_payload` or `risk_annotations` on
`workflow_instance`, validates extension field names, and rejects attempts to
extend foreign tables. This keeps workflow extensibility local while allowing
generated applications to add tenant-specific context safely.

## Functional Scope

Standard workflow functionality includes definition authoring, definition
versioning, state-machine execution, instance start, signal handling, timer
scheduling, retry policy, saga step recording, compensation execution, workflow
completion, human task modeling, SLA breach scoring, escalation routing,
correlation IDs, idempotency keys, workbench telemetry, audit evidence, release
controls, and package registration metadata.

Service commands are explicit and stable:
`configure_runtime`, `set_parameter`, `register_rule`,
`register_schema_extension`, `receive_event`, `define_workflow`,
`publish_workflow_version`, `register_transition_guard`, `start_instance`,
`signal_instance`, `schedule_timer`, `register_retry_policy`,
`register_sla_policy`, `register_escalation_rule`, `record_step_result`,
`execute_compensation`, `assign_human_task`, `record_approval_decision`,
`register_integration_endpoint`, `correlate_event`,
`capture_metric_snapshot`, `open_exception_case`,
`record_simulation_run`, `record_policy_screening`,
`record_completion_proof`, `append_audit_entry`,
`register_governed_model_evidence`, `complete_workflow`,
`build_api_contract`, `permissions_contract`, `build_workbench_view`, and
`verify_owned_table_boundary`. Generated apps can map these commands to
service classes, API routes, and UI actions without guessing.

The runtime stores events as the source of lifecycle evidence. Every emitted
event receives a stable event ID, hash, payload, tenant, aggregate ID, outbox
entry, and idempotency key. Hash-chain control tests verify that emitted events
remain tamper-evident. State projections are derived into dictionaries for
definitions, instances, signals, timers, saga steps, compensations, rules,
parameters, inbox, dead-letter, and consumed dependency projections.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, trigger,
`allowed_signals`, compensation requirement, severity, and status. Active rules
drive policy screening and release evidence. The rule model is intentionally
domain-neutral so packages can express approval policies, compensation policies,
timer policies, signal policies, and release gates without hardcoding a single
business vertical.

Parameters include `default_retry_limit`, `timer_jitter_seconds`,
`sla_breach_threshold`, `compensation_risk_threshold`, `max_parallel_steps`,
and `review_sla_hours`. Unsupported parameter keys are rejected. These
parameters influence breach scoring, risk simulation, compensation thresholds,
resource allocation, and workbench behavior.

Configuration requires `database_backend`, `event_topic`, `retry_limit`, and
`default_timezone`; generated apps may also provide `allowed_signal_sources`,
`default_versioning`, and `workbench_limit`. The only valid event topic is
`appgen.workflow.events`, the event contract is always `AppGen-X`, the stream
engine picker is hidden, and users cannot select an alternate event contract.

## API Surface

The descriptor API contract exposes route dictionaries rather than loose route
strings. Each route names its command or query, owned tables touched, emitted
or consumed events, required permission, and idempotency key:

- `POST /workflows/definitions` calls `define_workflow`, writes
  `workflow_definition`, emits `WorkflowDefinitionPublished`, and requires
  `workflow_orchestration.define`.
- `POST /workflows/versions` calls `publish_workflow_version` and writes
  `workflow_version`.
- `POST /workflows/transition-guards` calls `register_transition_guard` and
  writes `workflow_transition_guard`.
- `POST /workflows/retry-policies`, `POST /workflows/sla-policies`, and
  `POST /workflows/escalation-rules` manage workflow retry, SLA, and
  escalation policy records.
- `POST /workflows/instances` calls `start_instance`, writes
  `workflow_instance`, emits `WorkflowStarted`, and requires
  `workflow_orchestration.start`.
- `POST /workflows/instances/{id}/signals` calls `signal_instance`, writes
  `workflow_signal` and `workflow_instance`, emits `WorkflowSignalAccepted`,
  and requires `workflow_orchestration.signal`.
- `POST /workflows/timers` calls `schedule_timer`, writes `timer_task`, emits
  `TimerScheduled`, and requires `workflow_orchestration.start`.
- `POST /workflows/instances/{id}/steps` calls `record_step_result`, writes
  `saga_step`, emits `SagaStepCompleted`, and requires
  `workflow_orchestration.signal`.
- `POST /workflows/instances/{id}/compensations` calls
  `execute_compensation`, writes `compensation`, emits
  `CompensationExecuted`, and requires `workflow_orchestration.compensate`.
- `POST /workflows/human-task-assignments` and
  `POST /workflows/approval-decisions` manage human task assignment and
  approval decision records.
- `POST /workflows/integration-endpoints`,
  `POST /workflows/event-correlations`, `POST /workflows/metric-snapshots`,
  and `POST /workflows/exception-cases` expose endpoint declaration,
  correlation, telemetry, and exception case commands.
- `POST /workflows/simulation-runs`, `POST /workflows/policy-screenings`,
  `POST /workflows/completion-proofs`, `POST /workflows/audit-entries`, and
  `POST /workflows/governed-model-evidence` persist advanced simulation,
  control, proof, audit, and governed-model evidence.
- `POST /workflows/events/inbox` calls `receive_event`, consumes declared
  AppGen-X events, and requires `workflow_orchestration.event`.
- `GET /workflows/workbench` calls `build_workbench_view`, reads owned tables,
  and requires `workflow_orchestration.audit`.

Shared table access is explicitly false. Boundary verification allows owned
tables, runtime event tables, declared consumed events, known API dependency
routes, and dependency projections such as `gateway_workflow_projection`,
`schema_workflow_projection`, `audit_workflow_projection`,
`identity_workflow_projection`, and `composition_workflow_projection`. Foreign
table references are reported as violations.

## Events and Handlers

Emitted AppGen-X events are `WorkflowDefinitionPublished`, `WorkflowStarted`,
`WorkflowSignalAccepted`, `SagaStepCompleted`, `TimerScheduled`,
`CompensationExecuted`, and `WorkflowCompleted`.

Consumed AppGen-X events are `InvoiceApproved`, `OrderVerified`,
`ShipmentDelivered`, `PaymentCaptured`, `SchemaAccepted`,
`AccessPolicyChanged`, and `RoutePublished`. Handlers are idempotent by
`event_type:event_id` unless a caller provides a stronger idempotency key.
Duplicate processed events return the prior handler evidence without mutating
state. Failed or unsupported events write inbox entries, retry evidence, and,
after the configured retry limit, dead-letter entries. Consumed events are
projected into package-owned projection maps rather than foreign tables:
schema subjects, access policies, routes, and business correlation views.

## UI and Workbench

The UI contract includes `WorkflowWorkbench`, `StateMachineDesigner`,
`WorkflowInstanceMonitor`, `SagaStepBoard`, `TimerConsole`, `SignalInbox`,
`CompensationPlanner`, `HumanTaskQueue`, `SlaDashboard`,
`WorkflowRuleStudio`, `WorkflowParameterConsole`, and
`WorkflowConfigurationPanel`. Panels bind to owned workflow tables, rules,
parameters, configuration, outbox, inbox, and dead-letter evidence.

Workbench rendering is permission-aware. Actions are visible only when the
principal has the permission declared by `workflow_orchestration_permissions_contract`.
The UI declares allowed database backends, the required AppGen-X event topic,
hidden stream picker evidence, owned table binding evidence, inbox count,
dead-letter count, outbox count, and state cards for definitions, instances,
completed instances, timers, saga steps, and compensations.

## Advanced Capabilities

The package proves advanced capability coverage through executable smoke
evidence: event-sourced lifecycle, graph-relational saga topology,
multi-tenant isolation, schema-on-read context extension, probabilistic SLA
breach scoring, real-time analytics, counterfactual saga policy simulation,
temporal health forecasting, autonomous compensation recommendations,
semantic intent parsing, predictive saga risk scoring, self-healing route
selection, zero-knowledge-style completion proofs, immutable audit trails,
dynamic policy screening, automated control testing, universal API and async
surfaces, cross-system federation, gateway/schema/audit/identity/composition
integration, decentralized actor identity verification, resilience drills,
crypto-agile authorization, carbon-aware scheduling, algebraic state-machine
minimization, mechanism-design resource allocation, information-theoretic
anomaly detection, stochastic exposure modeling, distributed-systems evidence,
probabilistic workflow risk models, cryptographic evidence, mathematical
optimization, and governed model drift checks.

## Release Evidence

Release readiness requires the runtime smoke to pass, the package-local source
contract to be valid, the UI contract to bind to owned state, descriptor APIs
to declare owned tables and permissions, configuration to reject unsupported
backends and eventing options, handlers to prove idempotency and dead-letter
behavior, schema extensions to be owned-table scoped, boundary verification to
reject foreign tables, and focused tests to exercise the package. Generated
applications should include this package as a self-registering PBC with models,
services, routes, events, handlers, workbench fragments, permissions, seed
data, and release audit evidence derived from these package-local contracts.

## Read-Only Workbench Query Surface

- `GET /workflow-orchestration-workbench` maps to `query_workflow_orchestration_workbench` and exposes a read-only workbench/query contract for this command-heavy PBC.
- The query route has read-table scope only, emits no outbox event, requires no idempotency key, and remains inside the PBC-owned datastore boundary.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `workflow_orchestration`
- Mesh: `platform`
- Datastore backend: `postgresql`

### Owned Tables

- `workflow_definition`
- `workflow_version`
- `workflow_instance`
- `workflow_signal`
- `workflow_transition_guard`
- `timer_task`
- `workflow_retry_policy`
- `workflow_sla_policy`
- `workflow_escalation_rule`
- `saga_step`
- `compensation`
- `human_task`
- `human_task_assignment`
- `workflow_approval_decision`
- `workflow_integration_endpoint`
- `workflow_event_correlation`
- `workflow_metric_snapshot`
- `workflow_exception_case`
- `workflow_simulation_run`
- `workflow_policy_screening`
- `workflow_completion_proof`
- `workflow_audit_entry`
- `workflow_governed_model_evidence`
- `workflow_rule`
- `workflow_parameter`
- `workflow_configuration`
- `workflow_orchestration_appgen_outbox_event`
- `workflow_orchestration_appgen_inbox_event`
- `workflow_orchestration_dead_letter_event`

### API Routes

- `PUT /workflows/configuration`
- `POST /workflows/parameters`
- `POST /workflows/rules`
- `POST /workflows/definitions`
- `POST /workflows/versions`
- `POST /workflows/transition-guards`
- `POST /workflows/retry-policies`
- `POST /workflows/sla-policies`
- `POST /workflows/escalation-rules`
- `POST /workflows/instances`
- `POST /workflows/instances/{id}/signals`
- `POST /workflows/timers`
- `POST /workflows/instances/{id}/steps`
- `POST /workflows/instances/{id}/compensations`
- `POST /workflows/human-task-assignments`
- `POST /workflows/approval-decisions`
- `POST /workflows/integration-endpoints`
- `POST /workflows/event-correlations`
- `POST /workflows/metric-snapshots`
- `POST /workflows/exception-cases`
- `POST /workflows/simulation-runs`
- `POST /workflows/policy-screenings`
- `POST /workflows/completion-proofs`
- `POST /workflows/audit-entries`
- `POST /workflows/governed-model-evidence`
- `POST /workflows/events/inbox`
- `GET /workflows/workbench`
- `GET /workflows/schema-contract`
- `GET /workflows/service-contract`
- `GET /workflows/release-evidence`

### Emitted Events

- `WorkflowDefinitionPublished`
- `WorkflowStarted`
- `WorkflowSignalAccepted`
- `SagaStepCompleted`
- `TimerScheduled`
- `CompensationExecuted`
- `WorkflowCompleted`

### Consumed Events

- `InvoiceApproved`
- `OrderVerified`
- `ShipmentDelivered`
- `PaymentCaptured`
- `SchemaAccepted`
- `AccessPolicyChanged`
- `RoutePublished`

### UI Fragments

- `WorkflowOrchestrationWorkbench`
- `WorkflowDefinitionConsole`
- `WorkflowInstanceBoard`
- `SignalInboxPanel`
- `TimerTaskConsole`
- `SagaStepTimeline`
- `CompensationConsole`
- `HumanTaskQueue`
- `WorkflowConfigurationPanel`

### Permissions

- `workflow_orchestration.define`
- `workflow_orchestration.start`
- `workflow_orchestration.signal`
- `workflow_orchestration.compensate`
- `workflow_orchestration.event`
- `workflow_orchestration.configure`
- `workflow_orchestration.audit`
- `workflow_orchestration.read`

### Configuration Keys

- `WORKFLOW_ORCHESTRATION_DATABASE_URL`
- `WORKFLOW_ORCHESTRATION_EVENT_TOPIC`
- `WORKFLOW_ORCHESTRATION_RETRY_LIMIT`
- `WORKFLOW_ORCHESTRATION_DEFAULT_TIMEZONE`
- `WORKFLOW_ORCHESTRATION_ALLOWED_SIGNAL_SOURCES`

### Standard Features

- `workflow_definition_catalog`
- `state_machine_authoring`
- `definition_versioning`
- `instance_orchestration`
- `signal_handling`
- `timer_scheduling`
- `retry_policy`
- `saga_step_execution`
- `compensation_execution`
- `human_task_queue`
- `approval_routing`
- `sla_policy`
- `escalation_policy`
- `correlation_id`
- `idempotent_handlers`
- `retry_dead_letter`
- `workflow_telemetry`
- `policy_gate`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`
- `release_gate`
- `audit_evidence`
- `package_registration_validation`
- `appgen_event_contract`

### Advanced Capabilities

- `event_sourced_workflow_lifecycle`
- `graph_relational_saga_topology`
- `multi_tenant_workflow_isolation`
- `schema_on_read_workflow_context`
- `probabilistic_sla_breach_scoring`
- `real_time_workflow_analytics`
- `counterfactual_saga_policy_simulation`
- `temporal_workflow_forecasting`
- `autonomous_compensation_recommendation`
- `semantic_workflow_intent_parsing`
- `predictive_saga_risk_scoring`
- `self_healing_workflow_route_selection`
- `zero_knowledge_workflow_completion_proof`
- `immutable_workflow_audit_trail`
- `dynamic_workflow_policy_screening`
- `automated_workflow_control_testing`
- `universal_api_async_workflow_surface`
- `cross_system_workflow_federation`
- `gateway_schema_audit_identity_composition_integration`
- `decentralized_workflow_actor_identity`
- `chaos_engineered_workflow_tolerance`
- `quantum_resistant_workflow_authorization`
- `carbon_aware_workflow_scheduling`
- `algebraic_state_machine_minimization`
- `mechanism_design_saga_resource_allocation`
- `information_theoretic_workflow_anomaly_detection`
- `temporal_workflow_exposure_stochastic_modeling`
- `distributed_systems_engineering`
- `probabilistic_ml_workflow_risk`
- `cryptographic_engineering`
- `mathematical_optimization`
- `workflow_mlops_governance`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
