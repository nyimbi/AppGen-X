# Airport Operations Management PBC

## Purpose

The `airport_operations_management` PBC is a packaged business capability for Gates, stands, slots, turnaround, baggage, passenger flows, disruptions, and airport coordination. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `airport_operations_management`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/airport_operations_management`.
- Runtime entrypoint: `airport_operations_management_runtime_capabilities()`.
- UI entrypoint: `airport_operations_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `airport_operations_management_gate_assignment`: owns gate assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_stand_allocation`: owns stand allocation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_slot`: owns slot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_turndown_task`: owns turndown task lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_baggage_belt`: owns baggage belt lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_passenger_flow`: owns passenger flow lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_disruption`: owns airport disruption lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_operations_management_policy_rule`: owns airport operations management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_operations_management_runtime_parameter`: owns airport operations management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_operations_management_schema_extension`: owns airport operations management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_operations_management_control_assertion`: owns airport operations management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airport_operations_management_airport_operations_management_governed_model`: owns airport operations management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `airport_operations_management_appgen_outbox_event`, `airport_operations_management_appgen_inbox_event`, and `airport_operations_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /gate-assignments', 'POST /stand-allocations', 'POST /slots', 'POST /turndown-tasks', 'POST /baggage-belts', 'GET /airport-operations-management-workbench').

## Executable Domain Operations

- `create_gate_assignment`: validates policy, writes owned `airport_operations_management_gate_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_stand_allocation`: validates policy, writes owned `airport_operations_management_stand_allocation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_slot`: validates policy, writes owned `airport_operations_management_slot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_turndown_task`: validates policy, writes owned `airport_operations_management_turndown_task` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_baggage_belt`: validates policy, writes owned `airport_operations_management_baggage_belt` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_passenger_flow`: validates policy, writes owned `airport_operations_management_passenger_flow` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_airport_disruption`: validates policy, writes owned `airport_operations_management_airport_disruption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_airport_operations_management_policy_rule`: validates policy, writes owned `airport_operations_management_airport_operations_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_airport_operations_management_runtime_parameter`: validates policy, writes owned `airport_operations_management_airport_operations_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_airport_operations_management_schema_extension`: validates policy, writes owned `airport_operations_management_airport_operations_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_airport_operations_management_control_assertion`: validates policy, writes owned `airport_operations_management_airport_operations_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_airport_operations_management_governed_model`: validates policy, writes owned `airport_operations_management_airport_operations_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_13`: validates policy, writes owned `airport_operations_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_14`: validates policy, writes owned `airport_operations_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_15`: validates policy, writes owned `airport_operations_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_16`: validates policy, writes owned `airport_operations_management_gate_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_17`: validates policy, writes owned `airport_operations_management_stand_allocation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airport_operations_management_18`: validates policy, writes owned `airport_operations_management_slot` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Airport Operations Management domain records.
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

Rules are first-class artifacts: ('gate_assignment_policy', 'stand_allocation_policy', 'slot_policy', 'turndown_task_policy', 'baggage_belt_policy', 'passenger_flow_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /gate-assignments', 'POST /stand-allocations', 'POST /slots', 'POST /turndown-tasks', 'POST /baggage-belts', 'GET /airport-operations-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `airport_operations_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AirportOperationsManagementCreated', 'AirportOperationsManagementUpdated', 'AirportOperationsManagementApproved', 'AirportOperationsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('gate assignment board', 'stand allocation board', 'slot board', 'turndown task board', 'baggage belt board', 'passenger flow board', 'airport disruption board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `airport_operations_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: gate_assignment, stand_allocation, slot, turndown_task, baggage_belt, passenger_flow, airport_disruption, airport_operations_management_policy_rule, airport_operations_management_runtime_parameter, airport_operations_management_schema_extension, airport_operations_management_control_assertion, airport_operations_management_governed_model
- operations: create_gate_assignment, record_stand_allocation, review_slot, approve_turndown_task, simulate_baggage_belt, create_passenger_flow, record_airport_disruption, review_airport_operations_management_policy_rule, approve_airport_operations_management_runtime_parameter, simulate_airport_operations_management_schema_extension, create_airport_operations_management_control_assertion, record_airport_operations_management_governed_model, operate_airport_operations_management_13, operate_airport_operations_management_14, operate_airport_operations_management_15, operate_airport_operations_management_16, operate_airport_operations_management_17, operate_airport_operations_management_18
- emits: AirportOperationsManagementCreated, AirportOperationsManagementUpdated, AirportOperationsManagementApproved, AirportOperationsManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: gate_assignment_policy, stand_allocation_policy, slot_policy, turndown_task_policy, baggage_belt_policy, passenger_flow_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AirportOperationsManagementWorkbench, AirportOperationsManagementDetail, AirportOperationsManagementAssistantPanel
- permissions: airport_operations_management.read, airport_operations_management.create, airport_operations_management.update, airport_operations_management.approve, airport_operations_management.admin
- configuration: AIRPORT_OPERATIONS_MANAGEMENT_DATABASE_URL, AIRPORT_OPERATIONS_MANAGEMENT_EVENT_TOPIC, AIRPORT_OPERATIONS_MANAGEMENT_RETRY_LIMIT, AIRPORT_OPERATIONS_MANAGEMENT_DEFAULT_POLICY
- standard_features: gate_assignment_management, airport_operations_management_workflow, airport_operations_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: airport_operations_management_event_sourced_operational_history, airport_operations_management_multi_tenant_policy_isolation, airport_operations_management_schema_evolution_resilience, airport_operations_management_autonomous_anomaly_detection, airport_operations_management_semantic_document_instruction_understanding, airport_operations_management_predictive_risk_scoring, airport_operations_management_counterfactual_scenario_simulation, airport_operations_management_cryptographic_audit_proofs, airport_operations_management_continuous_control_testing, airport_operations_management_carbon_and_sustainability_awareness, airport_operations_management_cross_pbc_event_federation, airport_operations_management_governed_ai_agent_execution
