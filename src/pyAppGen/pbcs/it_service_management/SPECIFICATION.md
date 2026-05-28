# IT Service Management PBC

## Purpose

The `it_service_management` PBC is a packaged business capability for Incidents, requests, changes, problems, configuration items, service levels, and IT operations controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `it_service_management`.
- Mesh: `platform`.
- Package directory: `src/pyAppGen/pbcs/it_service_management`.
- Runtime entrypoint: `it_service_management_runtime_capabilities()`.
- UI entrypoint: `it_service_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `it_service_management_it_incident`: owns it incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_service_request`: owns service request lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_change_request`: owns change request lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_problem_record`: owns problem record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_configuration_item`: owns configuration item lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_sla_clock`: owns sla clock lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_knowledge_article`: owns knowledge article lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_it_service_management_policy_rule`: owns it service management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_it_service_management_runtime_parameter`: owns it service management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_it_service_management_schema_extension`: owns it service management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_it_service_management_control_assertion`: owns it service management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `it_service_management_it_service_management_governed_model`: owns it service management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `it_service_management_appgen_outbox_event`, `it_service_management_appgen_inbox_event`, and `it_service_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /it-incidents', 'POST /service-requests', 'POST /change-requests', 'POST /problem-records', 'POST /configuration-items', 'GET /it-service-management-workbench').

## Executable Domain Operations

- `create_it_incident`: validates policy, writes owned `it_service_management_it_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_service_request`: validates policy, writes owned `it_service_management_service_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_change_request`: validates policy, writes owned `it_service_management_change_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_problem_record`: validates policy, writes owned `it_service_management_problem_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_configuration_item`: validates policy, writes owned `it_service_management_configuration_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_sla_clock`: validates policy, writes owned `it_service_management_sla_clock` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_knowledge_article`: validates policy, writes owned `it_service_management_knowledge_article` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_it_service_management_policy_rule`: validates policy, writes owned `it_service_management_it_service_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_it_service_management_runtime_parameter`: validates policy, writes owned `it_service_management_it_service_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_it_service_management_schema_extension`: validates policy, writes owned `it_service_management_it_service_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_it_service_management_control_assertion`: validates policy, writes owned `it_service_management_it_service_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_it_service_management_governed_model`: validates policy, writes owned `it_service_management_it_service_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_13`: validates policy, writes owned `it_service_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_14`: validates policy, writes owned `it_service_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_15`: validates policy, writes owned `it_service_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_16`: validates policy, writes owned `it_service_management_it_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_17`: validates policy, writes owned `it_service_management_service_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_it_service_management_18`: validates policy, writes owned `it_service_management_change_request` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for IT Service Management domain records.
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

Rules are first-class artifacts: ('it_incident_policy', 'service_request_policy', 'change_request_policy', 'problem_record_policy', 'configuration_item_policy', 'sla_clock_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /it-incidents', 'POST /service-requests', 'POST /change-requests', 'POST /problem-records', 'POST /configuration-items', 'GET /it-service-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `it_service_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ItServiceManagementCreated', 'ItServiceManagementUpdated', 'ItServiceManagementApproved', 'ItServiceManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('it incident board', 'service request board', 'change request board', 'problem record board', 'configuration item board', 'sla clock board', 'knowledge article board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `it_service_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: it_incident, service_request, change_request, problem_record, configuration_item, sla_clock, knowledge_article, it_service_management_policy_rule, it_service_management_runtime_parameter, it_service_management_schema_extension, it_service_management_control_assertion, it_service_management_governed_model
- operations: create_it_incident, record_service_request, review_change_request, approve_problem_record, simulate_configuration_item, create_sla_clock, record_knowledge_article, review_it_service_management_policy_rule, approve_it_service_management_runtime_parameter, simulate_it_service_management_schema_extension, create_it_service_management_control_assertion, record_it_service_management_governed_model, operate_it_service_management_13, operate_it_service_management_14, operate_it_service_management_15, operate_it_service_management_16, operate_it_service_management_17, operate_it_service_management_18
- emits: ItServiceManagementCreated, ItServiceManagementUpdated, ItServiceManagementApproved, ItServiceManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: it_incident_policy, service_request_policy, change_request_policy, problem_record_policy, configuration_item_policy, sla_clock_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ItServiceManagementWorkbench, ItServiceManagementDetail, ItServiceManagementAssistantPanel
- permissions: it_service_management.read, it_service_management.create, it_service_management.update, it_service_management.approve, it_service_management.admin
- configuration: IT_SERVICE_MANAGEMENT_DATABASE_URL, IT_SERVICE_MANAGEMENT_EVENT_TOPIC, IT_SERVICE_MANAGEMENT_RETRY_LIMIT, IT_SERVICE_MANAGEMENT_DEFAULT_POLICY
- standard_features: it_incident_management, it_service_management_workflow, it_service_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: it_service_management_event_sourced_operational_history, it_service_management_multi_tenant_policy_isolation, it_service_management_schema_evolution_resilience, it_service_management_autonomous_anomaly_detection, it_service_management_semantic_document_instruction_understanding, it_service_management_predictive_risk_scoring, it_service_management_counterfactual_scenario_simulation, it_service_management_cryptographic_audit_proofs, it_service_management_continuous_control_testing, it_service_management_carbon_and_sustainability_awareness, it_service_management_cross_pbc_event_federation, it_service_management_governed_ai_agent_execution
