# Production Control PBC Specification

## Purpose

`production_control` owns production scheduling and shop-floor execution: work centers, routings, production orders, finite capacity, operation sequencing, starts, completions, downtime, OEE, and release handoffs. It composes with MRP, inventory, maintenance, quality, asset lifecycle, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `production_control`
- Mesh: `opsmfg`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `work_center`, `production_order`, `routing_step`,
  `production_schedule`, `dispatch_list`, `operation_confirmation`,
  `downtime_event`, `material_consumption`, `wip_inventory`,
  `labor_time_booking`, `machine_time_booking`, `quality_gate_result`,
  `production_completion_record`, `scrap_rework_event`, `oee_snapshot`,
  `throughput_forecast`, `production_exception_case`,
  `production_policy_screening`, `capacity_allocation`, `completion_proof`,
  `production_audit_entry`, `governed_model_evidence`, `production_rule`,
  `production_parameter`, and `production_configuration`
- Owned event tables: `production_control_appgen_outbox_event`,
  `production_control_appgen_inbox_event`, and
  `production_control_dead_letter_event`
- Consumed events: `PlannedOrderReleased`, `MaintenanceCompleted`
- Emitted events: `ProductionCompleted`, `AssetPlacedInService`, `DowntimeCaptured`
- External access rule: no shared MRP, inventory, maintenance, quality, or asset tables; use projections, APIs, and events only.

## Standard Table-Stakes Capabilities

1. Work center master capture with site, calendar, shift, capacity, efficiency, and status.
2. Routing step definition with sequence, work center, standard time, setup time, and quality gate.
3. Production order creation from planned-order projections.
4. Finite-capacity scheduling by site, work center, date, shift, and priority,
   persisted as owned `production_schedule` records.
5. Dispatch list generation and operation sequencing, persisted as owned
   `dispatch_list` records.
6. Production start, pause, resume, split, merge, and completion lifecycle.
7. Operation confirmation with good quantity, scrap quantity, labor hours, and
   machine hours, persisted as owned `operation_confirmation`,
   `labor_time_booking`, and `machine_time_booking` records.
8. Downtime event capture, classification, duration, asset projection, and OEE impact.
9. OEE, throughput, schedule adherence, yield, and cycle-time analytics.
10. Material readiness, consumption, WIP, and quality gate projection handling.
11. Maintenance completion projection handling.
12. Asset placed-in-service handoff where production creates commissioned equipment.
13. Production completion event generation for inventory and quality consumers.
14. Exception cases for capacity overload, missing material, quality hold,
    downtime, and late orders.
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
- Schema extensions may target only owned Production Control tables. The PBC
  can evolve all production master, schedule, dispatch, confirmation,
  material/WIP, time-booking, quality-gate, completion, scrap/rework, OEE,
  exception, proof, audit, governed-model, rule, parameter, and configuration
  tables; it must reject inventory, planning, maintenance, quality, asset,
  audit, identity, or shared platform tables.
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
material consumption, labor and machine time booking, downtime capture, quality
gate result capture, scrap/rework capture, operation confirmation, completion,
OEE snapshots, exception cases, capacity allocation, completion proofs, audit
entries, event inbox handling, and workbench reads. Each descriptor identifies
the owned table or consumed event
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

Generated schema evidence is part of the package contract.
`build_schema_contract` emits owned schema descriptors, generated migration
descriptors, generated model descriptors, and owned relationship evidence for
work centers, routings, production orders, finite schedules, dispatch lists,
operation confirmations, material consumption, WIP, labor and machine time,
quality gates, completion records, scrap/rework, OEE, forecasts, exceptions,
policy screenings, capacity allocation, proofs, audit entries, governed model
evidence, rules, parameters, configuration, projections, and AppGen-X runtime
tables. Those migration and model descriptors are validated before release
evidence is accepted.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- Production control workbench.
- Work center console.
- Routing editor.
- Production order board.
- Finite schedule board.
- Downtime console.
- Execution ledger for material consumption, labor time, machine time, and WIP.
- Quality and completion console for quality gates, scrap/rework, completion proofs, and audit entries.
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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `production_control`
- Mesh: `opsmfg`
- Datastore backend: `postgresql`

### Owned Tables

- `work_center`
- `production_order`
- `routing_step`
- `production_schedule`
- `dispatch_list`
- `operation_confirmation`
- `downtime_event`
- `material_consumption`
- `wip_inventory`
- `labor_time_booking`
- `machine_time_booking`
- `quality_gate_result`
- `production_completion_record`
- `scrap_rework_event`
- `oee_snapshot`
- `throughput_forecast`
- `production_exception_case`
- `production_policy_screening`
- `capacity_allocation`
- `completion_proof`
- `production_audit_entry`
- `governed_model_evidence`
- `production_rule`
- `production_parameter`
- `production_configuration`

### API Routes

- `POST /production/work-centers`
- `POST /production/orders`
- `POST /production/routing-steps`
- `POST /production/orders/{id}/schedule`
- `POST /production/operations/{id}/start`
- `POST /production/material-consumptions`
- `POST /production/labor-time`
- `POST /production/machine-time`
- `POST /production/downtime`
- `POST /production/quality-gates`
- `POST /production/scrap-rework`
- `POST /production/operations/{id}/confirm`
- `POST /production/orders/{id}/complete`
- `POST /production/oee-snapshots`
- `POST /production/exception-cases`
- `POST /production/capacity-allocations`
- `POST /production/completion-proofs`
- `POST /production/audit-entries`
- `POST /production/events/inbox`
- `POST /production/rules`
- `POST /production/parameters`
- `POST /production/configuration`
- `GET /production/workbench`
- `GET /production/schema-contract`
- `GET /production/service-contract`
- `GET /production/release-evidence`

### Emitted Events

- `ProductionCompleted`
- `AssetPlacedInService`
- `DowntimeCaptured`
- `MaterialConsumptionRecorded`
- `LaborTimeBooked`
- `MachineTimeBooked`
- `QualityGateRecorded`
- `ScrapReworkCaptured`

### Consumed Events

- `PlannedOrderReleased`
- `MaintenanceCompleted`

### UI Fragments

- `ProductionControlWorkbench`
- `WorkCenterConsole`
- `RoutingEditor`
- `ProductionOrderBoard`
- `FiniteScheduleBoard`
- `DowntimeConsole`
- `OeeDashboard`
- `ProductionRuleStudio`
- `ProductionParameterConsole`
- `ProductionConfigurationPanel`

### Permissions

- `production_control.audit`
- `production_control.complete`
- `production_control.configure`
- `production_control.event`
- `production_control.operate`
- `production_control.read`
- `production_control.schedule`

### Configuration Keys

- `PRODUCTION_CONTROL_DATABASE_URL`
- `PRODUCTION_CONTROL_EVENT_TOPIC`
- `PRODUCTION_CONTROL_RETRY_LIMIT`
- `PRODUCTION_CONTROL_DEFAULT_TIMEZONE`

### Standard Features

- `work_center_master`
- `routing_step_definition`
- `production_order_creation`
- `finite_capacity_scheduling`
- `dispatch_list`
- `operation_sequencing`
- `production_start`
- `operation_confirmation`
- `production_completion`
- `downtime_capture`
- `oee_calculation`
- `throughput_analytics`
- `schedule_adherence`
- `yield_tracking`
- `material_readiness_projection`
- `quality_gate_projection`
- `maintenance_projection`
- `asset_commissioning_handoff`
- `multi_site_isolation`
- `idempotent_handlers`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`

### Advanced Capabilities

- `event_sourced_production_lifecycle`
- `graph_relational_routing_work_center_topology`
- `multi_tenant_site_execution_isolation`
- `schema_evolution_resilient_production_schema`
- `probabilistic_downtime_yield_schedule_risk_scoring`
- `real_time_oee_execution_analytics`
- `counterfactual_dispatch_capacity_simulation`
- `temporal_throughput_downtime_forecasting`
- `autonomous_production_exception_resolution`
- `semantic_shop_floor_instruction_parsing`
- `predictive_schedule_quality_maintenance_risk`
- `self_healing_execution_route_selection`
- `zero_knowledge_completion_proof`
- `immutable_production_audit_trail`
- `dynamic_production_policy_screening`
- `automated_production_control_testing`
- `universal_api_async_streaming`
- `cross_system_production_federation`
- `mrp_inventory_quality_asset_integration`
- `decentralized_work_center_asset_identity`
- `chaos_engineered_shop_floor_tolerance`
- `quantum_resistant_production_authorization`
- `carbon_aware_production_scheduling`
- `algebraic_schedule_optimization`
- `mechanism_design_capacity_allocation`
- `information_theoretic_downtime_anomaly_detection`
- `temporal_production_exposure_stochastic_modeling`
- `distributed_systems_engineering`
- `probabilistic_ml_production_risk`
- `cryptographic_engineering`
- `mathematical_optimization`
- `production_mlops_governance`
- `standard_table_stakes_execution_records`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->
