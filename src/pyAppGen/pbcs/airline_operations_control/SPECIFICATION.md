# Airline Operations Control PBC

## Purpose

The `airline_operations_control` PBC is a packaged business capability for Fleet rotations, crew legality, disruptions, passenger reaccommodation, operational control, and recovery planning. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `airline_operations_control`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/airline_operations_control`.
- Runtime entrypoint: `airline_operations_control_runtime_capabilities()`.
- UI entrypoint: `airline_operations_control_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `airline_operations_control_flight_leg`: owns flight leg lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_aircraft_rotation`: owns aircraft rotation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_crew_pairing`: owns crew pairing lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_disruption_event`: owns disruption event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_reaccommodation_plan`: owns reaccommodation plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_operations_decision`: owns operations decision lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_delay_code`: owns delay code lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_airline_operations_control_policy_rule`: owns airline operations control policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_airline_operations_control_runtime_parameter`: owns airline operations control runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_airline_operations_control_schema_extension`: owns airline operations control schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_airline_operations_control_control_assertion`: owns airline operations control control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `airline_operations_control_airline_operations_control_governed_model`: owns airline operations control governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `airline_operations_control_appgen_outbox_event`, `airline_operations_control_appgen_inbox_event`, and `airline_operations_control_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /flight-legs', 'POST /aircraft-rotations', 'POST /crew-pairings', 'POST /disruption-events', 'POST /reaccommodation-plans', 'GET /airline-operations-control-workbench').

## Executable Domain Operations

- `create_flight_leg`: validates policy, writes owned `airline_operations_control_flight_leg` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_aircraft_rotation`: validates policy, writes owned `airline_operations_control_aircraft_rotation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_crew_pairing`: validates policy, writes owned `airline_operations_control_crew_pairing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_disruption_event`: validates policy, writes owned `airline_operations_control_disruption_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_reaccommodation_plan`: validates policy, writes owned `airline_operations_control_reaccommodation_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_operations_decision`: validates policy, writes owned `airline_operations_control_operations_decision` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_delay_code`: validates policy, writes owned `airline_operations_control_delay_code` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_airline_operations_control_policy_rule`: validates policy, writes owned `airline_operations_control_airline_operations_control_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_airline_operations_control_runtime_parameter`: validates policy, writes owned `airline_operations_control_airline_operations_control_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_airline_operations_control_schema_extension`: validates policy, writes owned `airline_operations_control_airline_operations_control_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_airline_operations_control_control_assertion`: validates policy, writes owned `airline_operations_control_airline_operations_control_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_airline_operations_control_governed_model`: validates policy, writes owned `airline_operations_control_airline_operations_control_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_13`: validates policy, writes owned `airline_operations_control_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_14`: validates policy, writes owned `airline_operations_control_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_15`: validates policy, writes owned `airline_operations_control_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_16`: validates policy, writes owned `airline_operations_control_flight_leg` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_17`: validates policy, writes owned `airline_operations_control_aircraft_rotation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_airline_operations_control_18`: validates policy, writes owned `airline_operations_control_crew_pairing` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Airline Operations Control domain records.
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

Rules are first-class artifacts: ('flight_leg_policy', 'aircraft_rotation_policy', 'crew_pairing_policy', 'disruption_event_policy', 'reaccommodation_plan_policy', 'operations_decision_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /flight-legs', 'POST /aircraft-rotations', 'POST /crew-pairings', 'POST /disruption-events', 'POST /reaccommodation-plans', 'GET /airline-operations-control-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `airline_operations_control_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AirlineOperationsControlCreated', 'AirlineOperationsControlUpdated', 'AirlineOperationsControlApproved', 'AirlineOperationsControlExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('flight leg board', 'aircraft rotation board', 'crew pairing board', 'disruption event board', 'reaccommodation plan board', 'operations decision board', 'delay code board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `airline_operations_control_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: flight_leg, aircraft_rotation, crew_pairing, disruption_event, reaccommodation_plan, operations_decision, delay_code, airline_operations_control_policy_rule, airline_operations_control_runtime_parameter, airline_operations_control_schema_extension, airline_operations_control_control_assertion, airline_operations_control_governed_model
- operations: create_flight_leg, record_aircraft_rotation, review_crew_pairing, approve_disruption_event, simulate_reaccommodation_plan, create_operations_decision, record_delay_code, review_airline_operations_control_policy_rule, approve_airline_operations_control_runtime_parameter, simulate_airline_operations_control_schema_extension, create_airline_operations_control_control_assertion, record_airline_operations_control_governed_model, operate_airline_operations_control_13, operate_airline_operations_control_14, operate_airline_operations_control_15, operate_airline_operations_control_16, operate_airline_operations_control_17, operate_airline_operations_control_18
- emits: AirlineOperationsControlCreated, AirlineOperationsControlUpdated, AirlineOperationsControlApproved, AirlineOperationsControlExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: flight_leg_policy, aircraft_rotation_policy, crew_pairing_policy, disruption_event_policy, reaccommodation_plan_policy, operations_decision_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AirlineOperationsControlWorkbench, AirlineOperationsControlDetail, AirlineOperationsControlAssistantPanel
- permissions: airline_operations_control.read, airline_operations_control.create, airline_operations_control.update, airline_operations_control.approve, airline_operations_control.admin
- configuration: AIRLINE_OPERATIONS_CONTROL_DATABASE_URL, AIRLINE_OPERATIONS_CONTROL_EVENT_TOPIC, AIRLINE_OPERATIONS_CONTROL_RETRY_LIMIT, AIRLINE_OPERATIONS_CONTROL_DEFAULT_POLICY
- standard_features: flight_leg_management, airline_operations_control_workflow, airline_operations_control_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: airline_operations_control_event_sourced_operational_history, airline_operations_control_multi_tenant_policy_isolation, airline_operations_control_schema_evolution_resilience, airline_operations_control_autonomous_anomaly_detection, airline_operations_control_semantic_document_instruction_understanding, airline_operations_control_predictive_risk_scoring, airline_operations_control_counterfactual_scenario_simulation, airline_operations_control_cryptographic_audit_proofs, airline_operations_control_continuous_control_testing, airline_operations_control_carbon_and_sustainability_awareness, airline_operations_control_cross_pbc_event_federation, airline_operations_control_governed_ai_agent_execution
