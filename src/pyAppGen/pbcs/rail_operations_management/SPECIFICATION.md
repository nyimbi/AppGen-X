# Rail Operations Management PBC

## Purpose

The `rail_operations_management` PBC is a packaged business capability for Train plans, consists, track windows, yards, crews, incidents, and rail service performance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `rail_operations_management`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/rail_operations_management`.
- Runtime entrypoint: `rail_operations_management_runtime_capabilities()`.
- UI entrypoint: `rail_operations_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `rail_operations_management_train_plan`: owns train plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_consist`: owns consist lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_track_window`: owns track window lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_yard_move`: owns yard move lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_crew_assignment`: owns crew assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_incident`: owns rail incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_service_performance`: owns service performance lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_operations_management_policy_rule`: owns rail operations management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_operations_management_runtime_parameter`: owns rail operations management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_operations_management_schema_extension`: owns rail operations management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_operations_management_control_assertion`: owns rail operations management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `rail_operations_management_rail_operations_management_governed_model`: owns rail operations management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `rail_operations_management_appgen_outbox_event`, `rail_operations_management_appgen_inbox_event`, and `rail_operations_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /train-plans', 'POST /consists', 'POST /track-windows', 'POST /yard-moves', 'POST /crew-assignments', 'GET /rail-operations-management-workbench').

## Executable Domain Operations

- `create_train_plan`: validates policy, writes owned `rail_operations_management_train_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_consist`: validates policy, writes owned `rail_operations_management_consist` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_track_window`: validates policy, writes owned `rail_operations_management_track_window` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_yard_move`: validates policy, writes owned `rail_operations_management_yard_move` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_crew_assignment`: validates policy, writes owned `rail_operations_management_crew_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_rail_incident`: validates policy, writes owned `rail_operations_management_rail_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_service_performance`: validates policy, writes owned `rail_operations_management_service_performance` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_rail_operations_management_policy_rule`: validates policy, writes owned `rail_operations_management_rail_operations_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_rail_operations_management_runtime_parameter`: validates policy, writes owned `rail_operations_management_rail_operations_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_rail_operations_management_schema_extension`: validates policy, writes owned `rail_operations_management_rail_operations_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_rail_operations_management_control_assertion`: validates policy, writes owned `rail_operations_management_rail_operations_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_rail_operations_management_governed_model`: validates policy, writes owned `rail_operations_management_rail_operations_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_13`: validates policy, writes owned `rail_operations_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_14`: validates policy, writes owned `rail_operations_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_15`: validates policy, writes owned `rail_operations_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_16`: validates policy, writes owned `rail_operations_management_train_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_17`: validates policy, writes owned `rail_operations_management_consist` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_rail_operations_management_18`: validates policy, writes owned `rail_operations_management_track_window` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Rail Operations Management domain records.
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

Rules are first-class artifacts: ('train_plan_policy', 'consist_policy', 'track_window_policy', 'yard_move_policy', 'crew_assignment_policy', 'rail_incident_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /train-plans', 'POST /consists', 'POST /track-windows', 'POST /yard-moves', 'POST /crew-assignments', 'GET /rail-operations-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `rail_operations_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('RailOperationsManagementCreated', 'RailOperationsManagementUpdated', 'RailOperationsManagementApproved', 'RailOperationsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('train plan board', 'consist board', 'track window board', 'yard move board', 'crew assignment board', 'rail incident board', 'service performance board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `rail_operations_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: train_plan, consist, track_window, yard_move, crew_assignment, rail_incident, service_performance, rail_operations_management_policy_rule, rail_operations_management_runtime_parameter, rail_operations_management_schema_extension, rail_operations_management_control_assertion, rail_operations_management_governed_model
- operations: create_train_plan, record_consist, review_track_window, approve_yard_move, simulate_crew_assignment, create_rail_incident, record_service_performance, review_rail_operations_management_policy_rule, approve_rail_operations_management_runtime_parameter, simulate_rail_operations_management_schema_extension, create_rail_operations_management_control_assertion, record_rail_operations_management_governed_model, operate_rail_operations_management_13, operate_rail_operations_management_14, operate_rail_operations_management_15, operate_rail_operations_management_16, operate_rail_operations_management_17, operate_rail_operations_management_18
- emits: RailOperationsManagementCreated, RailOperationsManagementUpdated, RailOperationsManagementApproved, RailOperationsManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: train_plan_policy, consist_policy, track_window_policy, yard_move_policy, crew_assignment_policy, rail_incident_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: RailOperationsManagementWorkbench, RailOperationsManagementDetail, RailOperationsManagementAssistantPanel
- permissions: rail_operations_management.read, rail_operations_management.create, rail_operations_management.update, rail_operations_management.approve, rail_operations_management.admin
- configuration: RAIL_OPERATIONS_MANAGEMENT_DATABASE_URL, RAIL_OPERATIONS_MANAGEMENT_EVENT_TOPIC, RAIL_OPERATIONS_MANAGEMENT_RETRY_LIMIT, RAIL_OPERATIONS_MANAGEMENT_DEFAULT_POLICY
- standard_features: train_plan_management, rail_operations_management_workflow, rail_operations_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: rail_operations_management_event_sourced_operational_history, rail_operations_management_multi_tenant_policy_isolation, rail_operations_management_schema_evolution_resilience, rail_operations_management_autonomous_anomaly_detection, rail_operations_management_semantic_document_instruction_understanding, rail_operations_management_predictive_risk_scoring, rail_operations_management_counterfactual_scenario_simulation, rail_operations_management_cryptographic_audit_proofs, rail_operations_management_continuous_control_testing, rail_operations_management_carbon_and_sustainability_awareness, rail_operations_management_cross_pbc_event_federation, rail_operations_management_governed_ai_agent_execution
