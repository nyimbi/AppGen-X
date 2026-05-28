# Facility Energy Management PBC

## Purpose

The `facility_energy_management` PBC is a packaged business capability for Facility meters, loads, equipment schedules, demand response, optimization, tariffs, and energy performance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `facility_energy_management`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/facility_energy_management`.
- Runtime entrypoint: `facility_energy_management_runtime_capabilities()`.
- UI entrypoint: `facility_energy_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `facility_energy_management_energy_meter`: owns energy meter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_load_profile`: owns load profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_equipment_schedule`: owns equipment schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_demand_response_event`: owns demand response event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_energy_optimization`: owns energy optimization lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_tariff_signal`: owns tariff signal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_energy_baseline`: owns energy baseline lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_facility_energy_management_policy_rule`: owns facility energy management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_facility_energy_management_runtime_parameter`: owns facility energy management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_facility_energy_management_schema_extension`: owns facility energy management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_facility_energy_management_control_assertion`: owns facility energy management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `facility_energy_management_facility_energy_management_governed_model`: owns facility energy management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `facility_energy_management_appgen_outbox_event`, `facility_energy_management_appgen_inbox_event`, and `facility_energy_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /energy-meters', 'POST /load-profiles', 'POST /equipment-schedules', 'POST /demand-response-events', 'POST /energy-optimizations', 'GET /facility-energy-management-workbench').

## Executable Domain Operations

- `create_energy_meter`: validates policy, writes owned `facility_energy_management_energy_meter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_load_profile`: validates policy, writes owned `facility_energy_management_load_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_equipment_schedule`: validates policy, writes owned `facility_energy_management_equipment_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_demand_response_event`: validates policy, writes owned `facility_energy_management_demand_response_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_energy_optimization`: validates policy, writes owned `facility_energy_management_energy_optimization` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_tariff_signal`: validates policy, writes owned `facility_energy_management_tariff_signal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_energy_baseline`: validates policy, writes owned `facility_energy_management_energy_baseline` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_facility_energy_management_policy_rule`: validates policy, writes owned `facility_energy_management_facility_energy_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_facility_energy_management_runtime_parameter`: validates policy, writes owned `facility_energy_management_facility_energy_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_facility_energy_management_schema_extension`: validates policy, writes owned `facility_energy_management_facility_energy_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_facility_energy_management_control_assertion`: validates policy, writes owned `facility_energy_management_facility_energy_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_facility_energy_management_governed_model`: validates policy, writes owned `facility_energy_management_facility_energy_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_13`: validates policy, writes owned `facility_energy_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_14`: validates policy, writes owned `facility_energy_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_15`: validates policy, writes owned `facility_energy_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_16`: validates policy, writes owned `facility_energy_management_energy_meter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_17`: validates policy, writes owned `facility_energy_management_load_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_facility_energy_management_18`: validates policy, writes owned `facility_energy_management_equipment_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Facility Energy Management domain records.
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

Rules are first-class artifacts: ('energy_meter_policy', 'load_profile_policy', 'equipment_schedule_policy', 'demand_response_event_policy', 'energy_optimization_policy', 'tariff_signal_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /energy-meters', 'POST /load-profiles', 'POST /equipment-schedules', 'POST /demand-response-events', 'POST /energy-optimizations', 'GET /facility-energy-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `facility_energy_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('FacilityEnergyManagementCreated', 'FacilityEnergyManagementUpdated', 'FacilityEnergyManagementApproved', 'FacilityEnergyManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('energy meter board', 'load profile board', 'equipment schedule board', 'demand response event board', 'energy optimization board', 'tariff signal board', 'energy baseline board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `facility_energy_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: energy_meter, load_profile, equipment_schedule, demand_response_event, energy_optimization, tariff_signal, energy_baseline, facility_energy_management_policy_rule, facility_energy_management_runtime_parameter, facility_energy_management_schema_extension, facility_energy_management_control_assertion, facility_energy_management_governed_model
- operations: create_energy_meter, record_load_profile, review_equipment_schedule, approve_demand_response_event, simulate_energy_optimization, create_tariff_signal, record_energy_baseline, review_facility_energy_management_policy_rule, approve_facility_energy_management_runtime_parameter, simulate_facility_energy_management_schema_extension, create_facility_energy_management_control_assertion, record_facility_energy_management_governed_model, operate_facility_energy_management_13, operate_facility_energy_management_14, operate_facility_energy_management_15, operate_facility_energy_management_16, operate_facility_energy_management_17, operate_facility_energy_management_18
- emits: FacilityEnergyManagementCreated, FacilityEnergyManagementUpdated, FacilityEnergyManagementApproved, FacilityEnergyManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: energy_meter_policy, load_profile_policy, equipment_schedule_policy, demand_response_event_policy, energy_optimization_policy, tariff_signal_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: FacilityEnergyManagementWorkbench, FacilityEnergyManagementDetail, FacilityEnergyManagementAssistantPanel
- permissions: facility_energy_management.read, facility_energy_management.create, facility_energy_management.update, facility_energy_management.approve, facility_energy_management.admin
- configuration: FACILITY_ENERGY_MANAGEMENT_DATABASE_URL, FACILITY_ENERGY_MANAGEMENT_EVENT_TOPIC, FACILITY_ENERGY_MANAGEMENT_RETRY_LIMIT, FACILITY_ENERGY_MANAGEMENT_DEFAULT_POLICY
- standard_features: energy_meter_management, facility_energy_management_workflow, facility_energy_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: facility_energy_management_event_sourced_operational_history, facility_energy_management_multi_tenant_policy_isolation, facility_energy_management_schema_evolution_resilience, facility_energy_management_autonomous_anomaly_detection, facility_energy_management_semantic_document_instruction_understanding, facility_energy_management_predictive_risk_scoring, facility_energy_management_counterfactual_scenario_simulation, facility_energy_management_cryptographic_audit_proofs, facility_energy_management_continuous_control_testing, facility_energy_management_carbon_and_sustainability_awareness, facility_energy_management_cross_pbc_event_federation, facility_energy_management_governed_ai_agent_execution
