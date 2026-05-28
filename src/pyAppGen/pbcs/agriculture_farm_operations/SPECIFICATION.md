# Agriculture Farm Operations PBC

## Purpose

The `agriculture_farm_operations` PBC is a packaged business capability for Fields, crops, inputs, equipment, irrigation, harvest, yield, certifications, and farm compliance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `agriculture_farm_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/agriculture_farm_operations`.
- Runtime entrypoint: `agriculture_farm_operations_runtime_capabilities()`.
- UI entrypoint: `agriculture_farm_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `agriculture_farm_operations_field`: owns field lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_crop_plan`: owns crop plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_input_application`: owns input application lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_irrigation_event`: owns irrigation event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_equipment_use`: owns equipment use lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_harvest_lot`: owns harvest lot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_yield_observation`: owns yield observation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_agriculture_farm_operations_policy_rule`: owns agriculture farm operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_agriculture_farm_operations_runtime_parameter`: owns agriculture farm operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_agriculture_farm_operations_schema_extension`: owns agriculture farm operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_agriculture_farm_operations_control_assertion`: owns agriculture farm operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agriculture_farm_operations_agriculture_farm_operations_governed_model`: owns agriculture farm operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `agriculture_farm_operations_appgen_outbox_event`, `agriculture_farm_operations_appgen_inbox_event`, and `agriculture_farm_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /fields', 'POST /crop-plans', 'POST /input-applications', 'POST /irrigation-events', 'POST /equipment-uses', 'GET /agriculture-farm-operations-workbench').

## Executable Domain Operations

- `create_field`: validates policy, writes owned `agriculture_farm_operations_field` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_crop_plan`: validates policy, writes owned `agriculture_farm_operations_crop_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_input_application`: validates policy, writes owned `agriculture_farm_operations_input_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_irrigation_event`: validates policy, writes owned `agriculture_farm_operations_irrigation_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_equipment_use`: validates policy, writes owned `agriculture_farm_operations_equipment_use` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_harvest_lot`: validates policy, writes owned `agriculture_farm_operations_harvest_lot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_yield_observation`: validates policy, writes owned `agriculture_farm_operations_yield_observation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_agriculture_farm_operations_policy_rule`: validates policy, writes owned `agriculture_farm_operations_agriculture_farm_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_agriculture_farm_operations_runtime_parameter`: validates policy, writes owned `agriculture_farm_operations_agriculture_farm_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_agriculture_farm_operations_schema_extension`: validates policy, writes owned `agriculture_farm_operations_agriculture_farm_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_agriculture_farm_operations_control_assertion`: validates policy, writes owned `agriculture_farm_operations_agriculture_farm_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_agriculture_farm_operations_governed_model`: validates policy, writes owned `agriculture_farm_operations_agriculture_farm_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_13`: validates policy, writes owned `agriculture_farm_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_14`: validates policy, writes owned `agriculture_farm_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_15`: validates policy, writes owned `agriculture_farm_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_16`: validates policy, writes owned `agriculture_farm_operations_field` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_17`: validates policy, writes owned `agriculture_farm_operations_crop_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agriculture_farm_operations_18`: validates policy, writes owned `agriculture_farm_operations_input_application` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Agriculture Farm Operations domain records.
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

Rules are first-class artifacts: ('field_policy', 'crop_plan_policy', 'input_application_policy', 'irrigation_event_policy', 'equipment_use_policy', 'harvest_lot_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /fields', 'POST /crop-plans', 'POST /input-applications', 'POST /irrigation-events', 'POST /equipment-uses', 'GET /agriculture-farm-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `agriculture_farm_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AgricultureFarmOperationsCreated', 'AgricultureFarmOperationsUpdated', 'AgricultureFarmOperationsApproved', 'AgricultureFarmOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('field board', 'crop plan board', 'input application board', 'irrigation event board', 'equipment use board', 'harvest lot board', 'yield observation board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `agriculture_farm_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: field, crop_plan, input_application, irrigation_event, equipment_use, harvest_lot, yield_observation, agriculture_farm_operations_policy_rule, agriculture_farm_operations_runtime_parameter, agriculture_farm_operations_schema_extension, agriculture_farm_operations_control_assertion, agriculture_farm_operations_governed_model
- operations: create_field, record_crop_plan, review_input_application, approve_irrigation_event, simulate_equipment_use, create_harvest_lot, record_yield_observation, review_agriculture_farm_operations_policy_rule, approve_agriculture_farm_operations_runtime_parameter, simulate_agriculture_farm_operations_schema_extension, create_agriculture_farm_operations_control_assertion, record_agriculture_farm_operations_governed_model, operate_agriculture_farm_operations_13, operate_agriculture_farm_operations_14, operate_agriculture_farm_operations_15, operate_agriculture_farm_operations_16, operate_agriculture_farm_operations_17, operate_agriculture_farm_operations_18
- emits: AgricultureFarmOperationsCreated, AgricultureFarmOperationsUpdated, AgricultureFarmOperationsApproved, AgricultureFarmOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: field_policy, crop_plan_policy, input_application_policy, irrigation_event_policy, equipment_use_policy, harvest_lot_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AgricultureFarmOperationsWorkbench, AgricultureFarmOperationsDetail, AgricultureFarmOperationsAssistantPanel
- permissions: agriculture_farm_operations.read, agriculture_farm_operations.create, agriculture_farm_operations.update, agriculture_farm_operations.approve, agriculture_farm_operations.admin
- configuration: AGRICULTURE_FARM_OPERATIONS_DATABASE_URL, AGRICULTURE_FARM_OPERATIONS_EVENT_TOPIC, AGRICULTURE_FARM_OPERATIONS_RETRY_LIMIT, AGRICULTURE_FARM_OPERATIONS_DEFAULT_POLICY
- standard_features: field_management, agriculture_farm_operations_workflow, agriculture_farm_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: agriculture_farm_operations_event_sourced_operational_history, agriculture_farm_operations_multi_tenant_policy_isolation, agriculture_farm_operations_schema_evolution_resilience, agriculture_farm_operations_autonomous_anomaly_detection, agriculture_farm_operations_semantic_document_instruction_understanding, agriculture_farm_operations_predictive_risk_scoring, agriculture_farm_operations_counterfactual_scenario_simulation, agriculture_farm_operations_cryptographic_audit_proofs, agriculture_farm_operations_continuous_control_testing, agriculture_farm_operations_carbon_and_sustainability_awareness, agriculture_farm_operations_cross_pbc_event_federation, agriculture_farm_operations_governed_ai_agent_execution
