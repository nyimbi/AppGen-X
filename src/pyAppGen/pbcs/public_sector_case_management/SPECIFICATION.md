# Public Sector Case Management PBC

## Purpose

The `public_sector_case_management` PBC is a packaged business capability for Citizen cases, eligibility, benefits, inspections, notices, appeals, service levels, and public outcomes. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `public_sector_case_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/public_sector_case_management`.
- Runtime entrypoint: `public_sector_case_management_runtime_capabilities()`.
- UI entrypoint: `public_sector_case_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `public_sector_case_management_citizen_case`: owns citizen case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_eligibility_determination`: owns eligibility determination lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_benefit_decision`: owns benefit decision lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_inspection`: owns inspection lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_notice`: owns notice lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_appeal`: owns appeal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_service_outcome`: owns service outcome lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_public_sector_case_management_policy_rule`: owns public sector case management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_public_sector_case_management_runtime_parameter`: owns public sector case management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_public_sector_case_management_schema_extension`: owns public sector case management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_public_sector_case_management_control_assertion`: owns public sector case management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_sector_case_management_public_sector_case_management_governed_model`: owns public sector case management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `public_sector_case_management_appgen_outbox_event`, `public_sector_case_management_appgen_inbox_event`, and `public_sector_case_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /citizen-cases', 'POST /eligibility-determinations', 'POST /benefit-decisions', 'POST /inspections', 'POST /notices', 'GET /public-sector-case-management-workbench').

## Executable Domain Operations

- `create_citizen_case`: validates policy, writes owned `public_sector_case_management_citizen_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_eligibility_determination`: validates policy, writes owned `public_sector_case_management_eligibility_determination` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_benefit_decision`: validates policy, writes owned `public_sector_case_management_benefit_decision` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_inspection`: validates policy, writes owned `public_sector_case_management_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_notice`: validates policy, writes owned `public_sector_case_management_notice` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_appeal`: validates policy, writes owned `public_sector_case_management_appeal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_service_outcome`: validates policy, writes owned `public_sector_case_management_service_outcome` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_public_sector_case_management_policy_rule`: validates policy, writes owned `public_sector_case_management_public_sector_case_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_public_sector_case_management_runtime_parameter`: validates policy, writes owned `public_sector_case_management_public_sector_case_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_public_sector_case_management_schema_extension`: validates policy, writes owned `public_sector_case_management_public_sector_case_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_public_sector_case_management_control_assertion`: validates policy, writes owned `public_sector_case_management_public_sector_case_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_public_sector_case_management_governed_model`: validates policy, writes owned `public_sector_case_management_public_sector_case_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_13`: validates policy, writes owned `public_sector_case_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_14`: validates policy, writes owned `public_sector_case_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_15`: validates policy, writes owned `public_sector_case_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_16`: validates policy, writes owned `public_sector_case_management_citizen_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_17`: validates policy, writes owned `public_sector_case_management_eligibility_determination` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_sector_case_management_18`: validates policy, writes owned `public_sector_case_management_benefit_decision` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Public Sector Case Management domain records.
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

Rules are first-class artifacts: ('citizen_case_policy', 'eligibility_determination_policy', 'benefit_decision_policy', 'inspection_policy', 'notice_policy', 'appeal_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /citizen-cases', 'POST /eligibility-determinations', 'POST /benefit-decisions', 'POST /inspections', 'POST /notices', 'GET /public-sector-case-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `public_sector_case_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PublicSectorCaseManagementCreated', 'PublicSectorCaseManagementUpdated', 'PublicSectorCaseManagementApproved', 'PublicSectorCaseManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('citizen case board', 'eligibility determination board', 'benefit decision board', 'inspection board', 'notice board', 'appeal board', 'service outcome board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `public_sector_case_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: citizen_case, eligibility_determination, benefit_decision, inspection, notice, appeal, service_outcome, public_sector_case_management_policy_rule, public_sector_case_management_runtime_parameter, public_sector_case_management_schema_extension, public_sector_case_management_control_assertion, public_sector_case_management_governed_model
- operations: create_citizen_case, record_eligibility_determination, review_benefit_decision, approve_inspection, simulate_notice, create_appeal, record_service_outcome, review_public_sector_case_management_policy_rule, approve_public_sector_case_management_runtime_parameter, simulate_public_sector_case_management_schema_extension, create_public_sector_case_management_control_assertion, record_public_sector_case_management_governed_model, operate_public_sector_case_management_13, operate_public_sector_case_management_14, operate_public_sector_case_management_15, operate_public_sector_case_management_16, operate_public_sector_case_management_17, operate_public_sector_case_management_18
- emits: PublicSectorCaseManagementCreated, PublicSectorCaseManagementUpdated, PublicSectorCaseManagementApproved, PublicSectorCaseManagementExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: citizen_case_policy, eligibility_determination_policy, benefit_decision_policy, inspection_policy, notice_policy, appeal_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PublicSectorCaseManagementWorkbench, PublicSectorCaseManagementDetail, PublicSectorCaseManagementAssistantPanel
- permissions: public_sector_case_management.read, public_sector_case_management.create, public_sector_case_management.update, public_sector_case_management.approve, public_sector_case_management.admin
- configuration: PUBLIC_SECTOR_CASE_MANAGEMENT_DATABASE_URL, PUBLIC_SECTOR_CASE_MANAGEMENT_EVENT_TOPIC, PUBLIC_SECTOR_CASE_MANAGEMENT_RETRY_LIMIT, PUBLIC_SECTOR_CASE_MANAGEMENT_DEFAULT_POLICY
- standard_features: citizen_case_management, public_sector_case_management_workflow, public_sector_case_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: public_sector_case_management_event_sourced_operational_history, public_sector_case_management_multi_tenant_policy_isolation, public_sector_case_management_schema_evolution_resilience, public_sector_case_management_autonomous_anomaly_detection, public_sector_case_management_semantic_document_instruction_understanding, public_sector_case_management_predictive_risk_scoring, public_sector_case_management_counterfactual_scenario_simulation, public_sector_case_management_cryptographic_audit_proofs, public_sector_case_management_continuous_control_testing, public_sector_case_management_carbon_and_sustainability_awareness, public_sector_case_management_cross_pbc_event_federation, public_sector_case_management_governed_ai_agent_execution
