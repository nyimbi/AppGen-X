# Laboratory Information Management PBC

## Purpose

The `laboratory_information_management` PBC is a packaged business capability for Samples, tests, instruments, results, quality control, chain of custody, and laboratory workflows. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `laboratory_information_management`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/laboratory_information_management`.
- Runtime entrypoint: `laboratory_information_management_runtime_capabilities()`.
- UI entrypoint: `laboratory_information_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `laboratory_information_management_lab_sample`: owns lab sample lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_test_order`: owns test order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_instrument_run`: owns instrument run lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_result`: owns result lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_quality_control`: owns quality control lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_chain_custody`: owns chain custody lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_lab_batch`: owns lab batch lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_laboratory_information_management_policy_rule`: owns laboratory information management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_laboratory_information_management_runtime_parameter`: owns laboratory information management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_laboratory_information_management_schema_extension`: owns laboratory information management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_laboratory_information_management_control_assertion`: owns laboratory information management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `laboratory_information_management_laboratory_information_management_governed_model`: owns laboratory information management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `laboratory_information_management_appgen_outbox_event`, `laboratory_information_management_appgen_inbox_event`, and `laboratory_information_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /lab-samples', 'POST /test-orders', 'POST /instrument-runs', 'POST /results', 'POST /quality-controls', 'GET /laboratory-information-management-workbench').

## Executable Domain Operations

- `create_lab_sample`: validates policy, writes owned `laboratory_information_management_lab_sample` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_test_order`: validates policy, writes owned `laboratory_information_management_test_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_instrument_run`: validates policy, writes owned `laboratory_information_management_instrument_run` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_result`: validates policy, writes owned `laboratory_information_management_result` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_quality_control`: validates policy, writes owned `laboratory_information_management_quality_control` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_chain_custody`: validates policy, writes owned `laboratory_information_management_chain_custody` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_lab_batch`: validates policy, writes owned `laboratory_information_management_lab_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_laboratory_information_management_policy_rule`: validates policy, writes owned `laboratory_information_management_laboratory_information_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_laboratory_information_management_runtime_parameter`: validates policy, writes owned `laboratory_information_management_laboratory_information_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_laboratory_information_management_schema_extension`: validates policy, writes owned `laboratory_information_management_laboratory_information_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_laboratory_information_management_control_assertion`: validates policy, writes owned `laboratory_information_management_laboratory_information_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_laboratory_information_management_governed_model`: validates policy, writes owned `laboratory_information_management_laboratory_information_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_13`: validates policy, writes owned `laboratory_information_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_14`: validates policy, writes owned `laboratory_information_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_15`: validates policy, writes owned `laboratory_information_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_16`: validates policy, writes owned `laboratory_information_management_lab_sample` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_17`: validates policy, writes owned `laboratory_information_management_test_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_laboratory_information_management_18`: validates policy, writes owned `laboratory_information_management_instrument_run` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Laboratory Information Management domain records.
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

Rules are first-class artifacts: ('lab_sample_policy', 'test_order_policy', 'instrument_run_policy', 'result_policy', 'quality_control_policy', 'chain_custody_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /lab-samples', 'POST /test-orders', 'POST /instrument-runs', 'POST /results', 'POST /quality-controls', 'GET /laboratory-information-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `laboratory_information_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('LaboratoryInformationManagementCreated', 'LaboratoryInformationManagementUpdated', 'LaboratoryInformationManagementApproved', 'LaboratoryInformationManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('lab sample board', 'test order board', 'instrument run board', 'result board', 'quality control board', 'chain custody board', 'lab batch board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `laboratory_information_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: lab_sample, test_order, instrument_run, result, quality_control, chain_custody, lab_batch, laboratory_information_management_policy_rule, laboratory_information_management_runtime_parameter, laboratory_information_management_schema_extension, laboratory_information_management_control_assertion, laboratory_information_management_governed_model
- operations: create_lab_sample, record_test_order, review_instrument_run, approve_result, simulate_quality_control, create_chain_custody, record_lab_batch, review_laboratory_information_management_policy_rule, approve_laboratory_information_management_runtime_parameter, simulate_laboratory_information_management_schema_extension, create_laboratory_information_management_control_assertion, record_laboratory_information_management_governed_model, operate_laboratory_information_management_13, operate_laboratory_information_management_14, operate_laboratory_information_management_15, operate_laboratory_information_management_16, operate_laboratory_information_management_17, operate_laboratory_information_management_18
- emits: LaboratoryInformationManagementCreated, LaboratoryInformationManagementUpdated, LaboratoryInformationManagementApproved, LaboratoryInformationManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: lab_sample_policy, test_order_policy, instrument_run_policy, result_policy, quality_control_policy, chain_custody_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: LaboratoryInformationManagementWorkbench, LaboratoryInformationManagementDetail, LaboratoryInformationManagementAssistantPanel
- permissions: laboratory_information_management.read, laboratory_information_management.create, laboratory_information_management.update, laboratory_information_management.approve, laboratory_information_management.admin
- configuration: LABORATORY_INFORMATION_MANAGEMENT_DATABASE_URL, LABORATORY_INFORMATION_MANAGEMENT_EVENT_TOPIC, LABORATORY_INFORMATION_MANAGEMENT_RETRY_LIMIT, LABORATORY_INFORMATION_MANAGEMENT_DEFAULT_POLICY
- standard_features: lab_sample_management, laboratory_information_management_workflow, laboratory_information_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: laboratory_information_management_event_sourced_operational_history, laboratory_information_management_multi_tenant_policy_isolation, laboratory_information_management_schema_evolution_resilience, laboratory_information_management_autonomous_anomaly_detection, laboratory_information_management_semantic_document_instruction_understanding, laboratory_information_management_predictive_risk_scoring, laboratory_information_management_counterfactual_scenario_simulation, laboratory_information_management_cryptographic_audit_proofs, laboratory_information_management_continuous_control_testing, laboratory_information_management_carbon_and_sustainability_awareness, laboratory_information_management_cross_pbc_event_federation, laboratory_information_management_governed_ai_agent_execution
