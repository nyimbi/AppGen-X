# Fleet and Mobility Operations PBC

## Purpose

The `fleet_mobility_operations` PBC is a packaged business capability for Vehicles, drivers, telematics, routing, maintenance, utilization, fuel, safety, and fleet compliance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `fleet_mobility_operations`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/fleet_mobility_operations`.
- Runtime entrypoint: `fleet_mobility_operations_runtime_capabilities()`.
- UI entrypoint: `fleet_mobility_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `fleet_mobility_operations_vehicle`: owns vehicle lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_driver_assignment`: owns driver assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_telematics_event`: owns telematics event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_route_plan`: owns route plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fuel_transaction`: owns fuel transaction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_maintenance_schedule`: owns maintenance schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_safety_event`: owns safety event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fleet_mobility_operations_policy_rule`: owns fleet mobility operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fleet_mobility_operations_runtime_parameter`: owns fleet mobility operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fleet_mobility_operations_schema_extension`: owns fleet mobility operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fleet_mobility_operations_control_assertion`: owns fleet mobility operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `fleet_mobility_operations_fleet_mobility_operations_governed_model`: owns fleet mobility operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `fleet_mobility_operations_appgen_outbox_event`, `fleet_mobility_operations_appgen_inbox_event`, and `fleet_mobility_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /vehicles', 'POST /driver-assignments', 'POST /telematics-events', 'POST /route-plans', 'POST /fuel-transactions', 'GET /fleet-mobility-operations-workbench').

## Executable Domain Operations

- `create_vehicle`: validates policy, writes owned `fleet_mobility_operations_vehicle` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_driver_assignment`: validates policy, writes owned `fleet_mobility_operations_driver_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_telematics_event`: validates policy, writes owned `fleet_mobility_operations_telematics_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_route_plan`: validates policy, writes owned `fleet_mobility_operations_route_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_fuel_transaction`: validates policy, writes owned `fleet_mobility_operations_fuel_transaction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_maintenance_schedule`: validates policy, writes owned `fleet_mobility_operations_maintenance_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_safety_event`: validates policy, writes owned `fleet_mobility_operations_safety_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_fleet_mobility_operations_policy_rule`: validates policy, writes owned `fleet_mobility_operations_fleet_mobility_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_fleet_mobility_operations_runtime_parameter`: validates policy, writes owned `fleet_mobility_operations_fleet_mobility_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_fleet_mobility_operations_schema_extension`: validates policy, writes owned `fleet_mobility_operations_fleet_mobility_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_fleet_mobility_operations_control_assertion`: validates policy, writes owned `fleet_mobility_operations_fleet_mobility_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_fleet_mobility_operations_governed_model`: validates policy, writes owned `fleet_mobility_operations_fleet_mobility_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_13`: validates policy, writes owned `fleet_mobility_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_14`: validates policy, writes owned `fleet_mobility_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_15`: validates policy, writes owned `fleet_mobility_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_16`: validates policy, writes owned `fleet_mobility_operations_vehicle` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_17`: validates policy, writes owned `fleet_mobility_operations_driver_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_fleet_mobility_operations_18`: validates policy, writes owned `fleet_mobility_operations_telematics_event` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Fleet and Mobility Operations domain records.
- Multi-tenant policy isolation with owned table boundaries.
- Schema evolution resilience through package-local schema extensions.
- Autonomous anomaly detection and specialist exception triage.
- Semantic document and instruction understanding for professional intake.
- Predictive risk scoring and confidence-ranked recommendations.
- Counterfactual scenario simulation for policy and operational choices.
- Cryptographic audit proofs for high-value records and decisions.
- Continuous control testing over domain lifecycle events.
- Carbon and sustainability awareness where operational decisions affect footprint.
- Cross-PBC event federation through AppGen-X only.
- Governed AI agent execution with human confirmation for mutations.

## Rules, Parameters, and Configuration

Rules are first-class artifacts: ('vehicle_policy', 'driver_assignment_policy', 'telematics_event_policy', 'route_plan_policy', 'fuel_transaction_policy', 'maintenance_schedule_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /vehicles', 'POST /driver-assignments', 'POST /telematics-events', 'POST /route-plans', 'POST /fuel-transactions', 'GET /fleet-mobility-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `fleet_mobility_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('FleetMobilityOperationsCreated', 'FleetMobilityOperationsUpdated', 'FleetMobilityOperationsApproved', 'FleetMobilityOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('vehicle board', 'driver assignment board', 'telematics event board', 'route plan board', 'fuel transaction board', 'maintenance schedule board', 'safety event board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `fleet_mobility_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: vehicle, driver_assignment, telematics_event, route_plan, fuel_transaction, maintenance_schedule, safety_event, fleet_mobility_operations_policy_rule, fleet_mobility_operations_runtime_parameter, fleet_mobility_operations_schema_extension, fleet_mobility_operations_control_assertion, fleet_mobility_operations_governed_model
- operations: create_vehicle, record_driver_assignment, review_telematics_event, approve_route_plan, simulate_fuel_transaction, create_maintenance_schedule, record_safety_event, review_fleet_mobility_operations_policy_rule, approve_fleet_mobility_operations_runtime_parameter, simulate_fleet_mobility_operations_schema_extension, create_fleet_mobility_operations_control_assertion, record_fleet_mobility_operations_governed_model, operate_fleet_mobility_operations_13, operate_fleet_mobility_operations_14, operate_fleet_mobility_operations_15, operate_fleet_mobility_operations_16, operate_fleet_mobility_operations_17, operate_fleet_mobility_operations_18
- emits: FleetMobilityOperationsCreated, FleetMobilityOperationsUpdated, FleetMobilityOperationsApproved, FleetMobilityOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: vehicle_policy, driver_assignment_policy, telematics_event_policy, route_plan_policy, fuel_transaction_policy, maintenance_schedule_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: FleetMobilityOperationsWorkbench, FleetMobilityOperationsDetail, FleetMobilityOperationsAssistantPanel
- permissions: fleet_mobility_operations.read, fleet_mobility_operations.create, fleet_mobility_operations.update, fleet_mobility_operations.approve, fleet_mobility_operations.admin
- configuration: FLEET_MOBILITY_OPERATIONS_DATABASE_URL, FLEET_MOBILITY_OPERATIONS_EVENT_TOPIC, FLEET_MOBILITY_OPERATIONS_RETRY_LIMIT, FLEET_MOBILITY_OPERATIONS_DEFAULT_POLICY
- standard_features: vehicle_management, fleet_mobility_operations_workflow, fleet_mobility_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: fleet_mobility_operations_event_sourced_operational_history, fleet_mobility_operations_multi_tenant_policy_isolation, fleet_mobility_operations_schema_evolution_resilience, fleet_mobility_operations_autonomous_anomaly_detection, fleet_mobility_operations_semantic_document_instruction_understanding, fleet_mobility_operations_predictive_risk_scoring, fleet_mobility_operations_counterfactual_scenario_simulation, fleet_mobility_operations_cryptographic_audit_proofs, fleet_mobility_operations_continuous_control_testing, fleet_mobility_operations_carbon_and_sustainability_awareness, fleet_mobility_operations_cross_pbc_event_federation, fleet_mobility_operations_governed_ai_agent_execution
