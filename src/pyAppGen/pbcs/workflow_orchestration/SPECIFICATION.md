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
- `workflow_instance`: immutable lifecycle projection for a running or
  completed workflow, correlation ID, context payload, current state, history,
  tenant, and status.
- `workflow_signal`: accepted or rejected external signals with source PBC,
  payload, validation result, transition decision, and correlation key.
- `timer_task`: deadline, wake-up command, breach risk, jitter, retry budget,
  escalation state, and scheduling evidence.
- `saga_step`: participant PBC, command name, status, duration, idempotency
  key, completion flag, and compensation link.
- `compensation`: compensation command, failure reason, execution status, and
  side-effect boundary.
- `human_task`: approval or exception work item, assignee group, SLA, decision,
  escalation state, and evidence payload.
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
`start_instance`, `signal_instance`, `schedule_timer`, `record_step_result`,
`execute_compensation`, `complete_workflow`, `build_api_contract`,
`permissions_contract`, `build_workbench_view`, and
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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `workflow_orchestration`
- Mesh: `platform`
- Datastore backend: `None`

### Owned Tables

- `workflow_definition`
- `workflow_instance`
- `saga_step`
- `timer_task`

### API Routes

- `POST /workflows`
- `POST /instances`
- `POST /signals`

### Emitted Events

- `WorkflowStarted`
- `SagaCompensated`
- `WorkflowCompleted`

### Consumed Events

- `InvoiceApproved`
- `OrderVerified`
- `ShipmentDelivered`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
