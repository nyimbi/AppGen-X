# Distributed Workflow Orchestration PBC

## Purpose

The Distributed Workflow Orchestration PBC owns visual and executable
long-running business processes across AppGen-X compositions. It manages
workflow definitions, versioned state machines, workflow instances, saga steps,
timers, retries, signals, compensation plans, human approvals, policy gates,
instance telemetry, and release evidence.

The PBC coordinates other PBCs only through declared APIs, AppGen-X events, and
read-only projections. It does not share tables with domain packages.

## Owned Datastore Boundary

The PBC owns:

- `workflow_orchestration_workflow_definition`: tenant, workflow key, version,
  states, transitions, signals, owner PBC, activation state, and invariants.
- `workflow_orchestration_workflow_instance`: immutable instance event stream,
  current state projection, context, status, correlation ID, and tenant.
- `workflow_orchestration_saga_step`: ordered command, participant PBC,
  retry policy, compensation command, status, and idempotency key.
- `workflow_orchestration_timer_task`: timer, deadline, escalation, retry,
  backoff, jitter, and wake-up command.
- `workflow_orchestration_signal`: external signal payload, source PBC,
  validation result, correlation key, and handler decision.
- `workflow_orchestration_human_task`: approval, review, exception, escalation,
  assignee group, SLA, and decision evidence.
- `workflow_orchestration_compensation`: compensation sequence, status,
  failure handling, and side-effect boundary.
- `workflow_orchestration_outbox`, `workflow_orchestration_inbox`, and
  `workflow_orchestration_dead_letter`: AppGen-X event contract tables for
  exactly-once handlers, retries, and dead-letter triage.

Supported backing stores are PostgreSQL, MySQL, and MariaDB.

## Standard Table-Stakes Capabilities

The PBC fully implements:

- Workflow definition catalog and versioning.
- Visual state-machine authoring metadata.
- State, transition, guard, action, signal, timer, and invariant descriptors.
- Workflow instance start, signal, transition, pause, resume, cancel, complete,
  and compensation execution.
- Saga step orchestration with command and compensation boundaries.
- Timer scheduling, retry budgets, exponential backoff, and deadline handling.
- Human approval and review tasks.
- SLA policies, escalation rules, and exception routing.
- Correlation IDs and idempotent command/event handling.
- AppGen-X event outbox, inbox, retry, and dead-letter evidence.
- Workbench views for definitions, instances, timers, sagas, human tasks,
  compensations, telemetry, policy rules, parameters, and configuration.
- RBAC descriptors for read, define, start, signal, approve, compensate,
  configure, and audit actions.
- Configuration schema, executable rules, runtime parameters, seed workflows,
  generated APIs, generated DSL evidence, package metadata, and release gates.

## Advanced Capabilities

The runtime proves:

- Event-sourced workflow lifecycle with hash-chain auditability.
- Graph-relational saga topology and dependency analysis.
- Multi-tenant workflow isolation.
- Schema-on-read context extension.
- Probabilistic SLA, retry, and compensation-risk scoring.
- Real-time workflow analytics and instance health.
- Counterfactual saga policy simulation.
- Temporal workflow throughput and breach forecasting.
- Autonomous compensation and remediation recommendations.
- Semantic workflow intent parsing.
- Predictive saga risk scoring.
- Self-healing workflow route selection when participants fail.
- Zero-knowledge-style workflow completion proofs.
- Dynamic policy screening and automated control testing.
- Universal API and asynchronous workflow contract surfaces.
- Cross-system workflow federation through read-only projections.
- Gateway, schema, audit, identity, and composition integration contracts.
- Decentralized workflow actor identity verification.
- Resilience drills for timer, participant, and signal failures.
- Crypto-agile workflow authorization.
- Carbon-aware scheduling for large workflow batches.
- Algebraic state-machine minimization.
- Mechanism-design allocation of scarce saga resources.
- Information-theoretic anomaly detection.
- Temporal stochastic exposure modeling.
- Governed probabilistic models for workflow risk and drift.

## Rules, Parameters, and Configuration

Rules are executable records with `rule_id`, tenant, scope, trigger,
allowed signals, compensation requirement, SLA severity, status, and optional
participant filters. Parameters include `default_retry_limit`,
`timer_jitter_seconds`, `sla_breach_threshold`, `compensation_risk_threshold`,
`max_parallel_steps`, and `review_sla_hours`.

Configuration includes database backend, event topic, retry limit, default
timezone, default workflow versioning mode, allowed signal sources, and
workbench limits. Runtime configuration rejects unsupported databases and uses
the AppGen-X event contract for ordinary eventing.

## Public APIs

- `POST /workflows/definitions`
- `POST /workflows/instances`
- `POST /workflows/instances/{id}/signals`
- `POST /workflows/instances/{id}/steps`
- `POST /workflows/instances/{id}/compensations`
- `POST /workflows/timers`
- `POST /workflows/human-tasks`
- `GET /workflows/definitions`
- `GET /workflows/instances`
- `GET /workflows/workbench`

## Events

Emitted events:

- `WorkflowDefinitionPublished`
- `WorkflowStarted`
- `WorkflowSignalAccepted`
- `SagaStepCompleted`
- `TimerScheduled`
- `CompensationExecuted`
- `WorkflowCompleted`

Consumed events:

- `InvoiceApproved`
- `OrderVerified`
- `ShipmentDelivered`
- `PaymentCaptured`
- `SchemaAccepted`
- `AccessPolicyChanged`
- `RoutePublished`

Handlers are idempotent by `workflow_orchestration:{event_type}:{event_id}`,
retry at least three times, and write failures to
`workflow_orchestration_dead_letter`.

## UI and Workbench

The UI exposes a workflow workbench, state-machine designer, instance monitor,
saga step board, timer console, signal inbox, compensation planner, human task
queue, SLA dashboard, workflow rule studio, parameter console, configuration
panel, and audit evidence view. Actions are permission-bound and rendered from
package-owned state.

## Release Evidence

Release readiness requires passing runtime smoke, package-local UI contract,
owned tables, API/event/handler surfaces, AppGen-X event contract evidence,
configuration/rule/parameter execution, generated DSL smoke compatibility,
package registration metadata, workbench rendering, and focused unit tests.
