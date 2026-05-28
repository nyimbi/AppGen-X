# Court Case Management PBC

## Purpose

The `court_case_management` PBC is a packaged business capability for Filings, hearings, dockets, parties, judgments, orders, calendars, and court operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `court_case_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/court_case_management`.
- Runtime entrypoint: `court_case_management_runtime_capabilities()`.
- UI entrypoint: `court_case_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `court_case_management_court_case`: owns court case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_filing`: owns filing lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_hearing`: owns hearing lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_docket_entry`: owns docket entry lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_party`: owns party lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_judgment`: owns judgment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_order`: owns court order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_case_management_policy_rule`: owns court case management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_case_management_runtime_parameter`: owns court case management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_case_management_schema_extension`: owns court case management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_case_management_control_assertion`: owns court case management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `court_case_management_court_case_management_governed_model`: owns court case management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `court_case_management_appgen_outbox_event`, `court_case_management_appgen_inbox_event`, and `court_case_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /court-cases', 'POST /filings', 'POST /hearings', 'POST /docket-entrys', 'POST /partys', 'GET /court-case-management-workbench').

## Executable Domain Operations

- `create_court_case`: validates policy, writes owned `court_case_management_court_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_filing`: validates policy, writes owned `court_case_management_filing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_hearing`: validates policy, writes owned `court_case_management_hearing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_docket_entry`: validates policy, writes owned `court_case_management_docket_entry` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_party`: validates policy, writes owned `court_case_management_party` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_judgment`: validates policy, writes owned `court_case_management_judgment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_court_order`: validates policy, writes owned `court_case_management_court_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_court_case_management_policy_rule`: validates policy, writes owned `court_case_management_court_case_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_court_case_management_runtime_parameter`: validates policy, writes owned `court_case_management_court_case_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_court_case_management_schema_extension`: validates policy, writes owned `court_case_management_court_case_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_court_case_management_control_assertion`: validates policy, writes owned `court_case_management_court_case_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_court_case_management_governed_model`: validates policy, writes owned `court_case_management_court_case_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_13`: validates policy, writes owned `court_case_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_14`: validates policy, writes owned `court_case_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_15`: validates policy, writes owned `court_case_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_16`: validates policy, writes owned `court_case_management_court_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_17`: validates policy, writes owned `court_case_management_filing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_court_case_management_18`: validates policy, writes owned `court_case_management_hearing` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Court Case Management domain records.
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

Rules are first-class artifacts: ('court_case_policy', 'filing_policy', 'hearing_policy', 'docket_entry_policy', 'party_policy', 'judgment_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /court-cases', 'POST /filings', 'POST /hearings', 'POST /docket-entrys', 'POST /partys', 'GET /court-case-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `court_case_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('CourtCaseManagementCreated', 'CourtCaseManagementUpdated', 'CourtCaseManagementApproved', 'CourtCaseManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('court case board', 'filing board', 'hearing board', 'docket entry board', 'party board', 'judgment board', 'court order board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `court_case_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: court_case, filing, hearing, docket_entry, party, judgment, court_order, court_case_management_policy_rule, court_case_management_runtime_parameter, court_case_management_schema_extension, court_case_management_control_assertion, court_case_management_governed_model
- operations: create_court_case, record_filing, review_hearing, approve_docket_entry, simulate_party, create_judgment, record_court_order, review_court_case_management_policy_rule, approve_court_case_management_runtime_parameter, simulate_court_case_management_schema_extension, create_court_case_management_control_assertion, record_court_case_management_governed_model, operate_court_case_management_13, operate_court_case_management_14, operate_court_case_management_15, operate_court_case_management_16, operate_court_case_management_17, operate_court_case_management_18
- emits: CourtCaseManagementCreated, CourtCaseManagementUpdated, CourtCaseManagementApproved, CourtCaseManagementExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: court_case_policy, filing_policy, hearing_policy, docket_entry_policy, party_policy, judgment_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: CourtCaseManagementWorkbench, CourtCaseManagementDetail, CourtCaseManagementAssistantPanel
- permissions: court_case_management.read, court_case_management.create, court_case_management.update, court_case_management.approve, court_case_management.admin
- configuration: COURT_CASE_MANAGEMENT_DATABASE_URL, COURT_CASE_MANAGEMENT_EVENT_TOPIC, COURT_CASE_MANAGEMENT_RETRY_LIMIT, COURT_CASE_MANAGEMENT_DEFAULT_POLICY
- standard_features: court_case_management, court_case_management_workflow, court_case_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: court_case_management_event_sourced_operational_history, court_case_management_multi_tenant_policy_isolation, court_case_management_schema_evolution_resilience, court_case_management_autonomous_anomaly_detection, court_case_management_semantic_document_instruction_understanding, court_case_management_predictive_risk_scoring, court_case_management_counterfactual_scenario_simulation, court_case_management_cryptographic_audit_proofs, court_case_management_continuous_control_testing, court_case_management_carbon_and_sustainability_awareness, court_case_management_cross_pbc_event_federation, court_case_management_governed_ai_agent_execution
