# Production Control PBC Specification

## Purpose

`production_control` owns production scheduling and shop-floor execution: work centers, routings, production orders, finite capacity, operation sequencing, starts, completions, downtime, OEE, and release handoffs. It composes with MRP, inventory, maintenance, quality, asset lifecycle, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `production_control`
- Mesh: `opsmfg`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `work_center`, `production_order`, `routing_step`, `downtime_event`
- Owned event tables: `production_control_outbox`, `production_control_inbox`, `production_control_dead_letter`
- Consumed events: `PlannedOrderReleased`, `MaintenanceCompleted`
- Emitted events: `ProductionCompleted`, `AssetPlacedInService`, `DowntimeCaptured`
- External access rule: no shared MRP, inventory, maintenance, quality, or asset tables; use projections, APIs, and events only.

## Standard Table-Stakes Capabilities

1. Work center master capture with site, calendar, shift, capacity, efficiency, and status.
2. Routing step definition with sequence, work center, standard time, setup time, and quality gate.
3. Production order creation from planned-order projections.
4. Finite-capacity scheduling by site, work center, date, shift, and priority.
5. Dispatch list generation and operation sequencing.
6. Production start, pause, resume, split, merge, and completion lifecycle.
7. Operation confirmation with good quantity, scrap quantity, labor hours, and machine hours.
8. Downtime event capture, classification, duration, asset projection, and OEE impact.
9. OEE, throughput, schedule adherence, yield, and cycle-time analytics.
10. Material readiness and quality gate projection handling.
11. Maintenance completion projection handling.
12. Asset placed-in-service handoff where production creates commissioned equipment.
13. Production completion event generation for inventory and quality consumers.
14. Exception messages for capacity overload, missing material, quality hold, downtime, and late orders.
15. Multi-tenant, multi-site, and work-center isolation.
16. AppGen-X outbox/inbox idempotency.
17. Retry and dead-letter evidence.
18. RBAC descriptors for scheduler, supervisor, operator, maintenance coordinator, auditor, and admin actions.
19. Configuration schema for runtime installation.
20. Rule engine for dispatch, capacity, quality gate, downtime, completion, and asset commissioning policies.
21. Parameter engine for capacity threshold, OEE targets, scrap threshold, takt time, schedule horizon, and downtime severity.
22. Seed data for work-center classes, downtime reasons, operation statuses, dispatch priorities, and quality gates.
23. Package metadata, source registration, and release evidence.
24. Package-local workbench UI for work centers, orders, routing, schedule, downtime, OEE, rules, parameters, and configuration.

## Advanced Capability Requirements

The runtime must prove deterministic evidence for:

- Event-sourced production lifecycle and immutable audit trail.
- Graph-relational routing/work-center topology.
- Multi-tenant and multi-site execution isolation.
- Schema evolution for production attributes.
- Probabilistic downtime, yield, and schedule-risk scoring.
- Real-time OEE and execution analytics.
- Counterfactual dispatch and capacity simulation.
- Throughput, downtime, and completion forecasting.
- Autonomous production exception recommendations.
- Semantic shop-floor instruction parsing.
- Self-healing MES, maintenance, and inventory route selection.
- Zero-knowledge production completion proof generation.
- Dynamic production policy screening and automated controls.
- Universal API/event contracts and cross-system production federation.
- MRP, maintenance, inventory, quality, and asset integration through projections.
- Decentralized work center and asset identity verification.
- Resilience drills, crypto agility, and carbon-aware production scheduling.
- Algebraic schedule optimization and mechanism-design capacity allocation.
- Information-theoretic downtime anomaly detection.
- Stochastic production exposure modeling.
- Governed production model registration with lineage, drift, and explainability controls.

## Rules, Parameters, And Configuration

The PBC must understand and execute:

- Configuration: database backend, event topic, retry limit, allowed sites, allowed work-center types, allowed downtime reasons, allowed production routes, default timezone, and workbench limit.
- Parameters: capacity threshold, OEE target, scrap threshold, takt time minutes, schedule horizon days, and downtime severity minutes.
- Rules: work-center eligibility, routing eligibility, dispatch priority, capacity overload, quality gate, completion, downtime severity, and asset commissioning policies.

Rules are compiled into deterministic hashes, parameters are stored in owned runtime state, and configuration gates work-center, order, routing, downtime, scheduling, and completion operations.

## Runtime Completeness Contract

The runtime must prove that:

- Configuration rejects unsupported backends, rejects unsupported configuration fields, requires the fixed `appgen.production.events` AppGen-X topic, and exposes only the AppGen-X event contract without any user-facing stream-engine picker or event-contract choice.
- Parameter support is bounded to the package-local production-control parameter set and rejects unknown parameters.
- Rules require production-control binding fields, compile into deterministic hashes, and retain deterministic compilation evidence for workbench and release audits.
- Schema extensions may target only owned Production Control tables. The PBC can evolve `work_center`, `production_order`, `routing_step`, `downtime_event`, `production_rule`, `production_parameter`, and `production_configuration`; it must reject inventory, planning, maintenance, quality, asset, audit, identity, or shared platform tables.
- `receive_event` is the only consumed-event entry point. It accepts `PlannedOrderReleased` and `MaintenanceCompleted`, writes immutable inbox evidence, derives package-local projections, handles duplicates by idempotency key, records retry attempts, and moves unsupported or failed events to a package-local dead-letter evidence surface after the configured retry limit.
- Package-local workbench and UI surfaces expose evidence for configuration, rule, and parameter bindings without crossing the `production_control` package boundary.
- `build_api_contract` returns descriptor routes with owned-table, command/query, permission, event, and idempotency metadata. The descriptor must say `shared_table_access: false`, list only PostgreSQL/MySQL/MariaDB backends, and keep stream-engine selection hidden.
- `permissions_contract` binds every command, event handler, configuration action, and audit surface to explicit Production Control permissions.
- `verify_owned_table_boundary` accepts only owned tables, AppGen-X runtime tables, consumed events, declared API dependencies, declared projections, or `production_control_` runtime names. Foreign table references are violations.
- Standard and advanced capability claims remain testable through package-local runtime, UI, and release evidence.

## Event Handling Contract

Production Control emits `ProductionCompleted`, `AssetPlacedInService`, and
`DowntimeCaptured`. These events are written through the AppGen-X outbox with
deterministic idempotency keys derived from the PBC key, event type, and event
sequence. Consumers use those events to create inventory receipt, quality
completion, asset commissioning, analytics, and audit projections.

Production Control consumes `PlannedOrderReleased` and `MaintenanceCompleted`.
The consumed event handler never reaches into upstream tables. A planned-order
release becomes a `planned_order_projections` record that can seed production
orders and scheduling decisions. A maintenance completion becomes a
`maintenance_projections` record that can release work-center capacity or
support downtime explanations. Unsupported events and simulated handler
failures produce retry evidence first and dead-letter evidence when attempts
reach the configured limit. Duplicate event delivery returns the previous
handler evidence without mutating state.

## API, RBAC, And Boundary Contract

API descriptors are executable package metadata, not catalog prose. They cover
work-center registration, order creation, routing, scheduling, operation start,
downtime capture, operation confirmation, completion, event inbox handling, and
workbench reads. Each descriptor identifies the owned table or consumed event
surface it touches and the permission required to invoke it. Production
Control grants no shared-table capability; cross-PBC interaction is through
declared AppGen-X events, declared APIs, and projections only.

RBAC separates scheduling, operation, completion, event handling,
configuration, and audit responsibilities. Operators can start and confirm
operations and record downtime. Schedulers can create work centers, orders,
routings, and schedules. Completion users can finish orders and emit handoff
events. Event handlers require `production_control.event`. Configuration users
can manage rules, parameters, runtime settings, and schema extensions. Auditors
can read workbench and control evidence.

Boundary validation is part of release evidence. Generated code, hand-authored
runtime paths, and future package registrations can call
`verify_owned_table_boundary` with their table/API/event references. The check
allows owned tables, AppGen-X outbox/inbox/dead-letter tables, consumed event
types, declared integration APIs, declared projection names, and
`production_control_` runtime names. References such as external inventory,
quality, planning, maintenance, identity, or finance tables are rejected.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- Production control workbench.
- Work center console.
- Routing editor.
- Production order board.
- Finite schedule board.
- Downtime console.
- OEE dashboard.
- Rule studio.
- Parameter console.
- Runtime configuration panel.

UI actions are RBAC-gated and bind only to owned tables, projections, and AppGen-X event surfaces.
The workbench must also show owned table binding evidence, outbox, inbox,
dead-letter surfaces, fixed AppGen-X configuration, hidden event-engine
selection, and permission descriptors so generated applications can expose a
complete Production Control console without adding package-specific glue.

## Release Evidence

Completion requires:

- Package-local specification, runtime, UI, and tests.
- `pbc_implementation_contract("production_control")` returns an ok source package and advanced runtime.
- `pbc_implementation_release_audit(("production_control",))` passes.
- `pbc_implemented_capability_audit(("production_control",))` passes.
- Full 46-PBC generation smoke remains green.
