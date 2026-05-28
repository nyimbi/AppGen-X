# Lending Origination and Servicing PBC

## Purpose

The `lending_origination_servicing` PBC is a packaged business capability for Loan applications, underwriting, offers, disbursement, repayment, servicing, collections, and covenant monitoring. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `lending_origination_servicing`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/lending_origination_servicing`.
- Runtime entrypoint: `lending_origination_servicing_runtime_capabilities()`.
- UI entrypoint: `lending_origination_servicing_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `lending_origination_servicing_loan_application`: owns loan application lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_borrower_profile`: owns borrower profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_underwriting_decision`: owns underwriting decision lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_loan_offer`: owns loan offer lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_disbursement`: owns disbursement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_repayment_schedule`: owns repayment schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_servicing_case`: owns servicing case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_lending_origination_servicing_policy_rule`: owns lending origination servicing policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_lending_origination_servicing_runtime_parameter`: owns lending origination servicing runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_lending_origination_servicing_schema_extension`: owns lending origination servicing schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_lending_origination_servicing_control_assertion`: owns lending origination servicing control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lending_origination_servicing_lending_origination_servicing_governed_model`: owns lending origination servicing governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `lending_origination_servicing_appgen_outbox_event`, `lending_origination_servicing_appgen_inbox_event`, and `lending_origination_servicing_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /loan-applications', 'POST /borrower-profiles', 'POST /underwriting-decisions', 'POST /loan-offers', 'POST /disbursements', 'GET /lending-origination-servicing-workbench').

## Executable Domain Operations

- `create_loan_application`: validates policy, writes owned `lending_origination_servicing_loan_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_borrower_profile`: validates policy, writes owned `lending_origination_servicing_borrower_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_underwriting_decision`: validates policy, writes owned `lending_origination_servicing_underwriting_decision` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_loan_offer`: validates policy, writes owned `lending_origination_servicing_loan_offer` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_disbursement`: validates policy, writes owned `lending_origination_servicing_disbursement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_repayment_schedule`: validates policy, writes owned `lending_origination_servicing_repayment_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_servicing_case`: validates policy, writes owned `lending_origination_servicing_servicing_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_lending_origination_servicing_policy_rule`: validates policy, writes owned `lending_origination_servicing_lending_origination_servicing_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_lending_origination_servicing_runtime_parameter`: validates policy, writes owned `lending_origination_servicing_lending_origination_servicing_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_lending_origination_servicing_schema_extension`: validates policy, writes owned `lending_origination_servicing_lending_origination_servicing_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_lending_origination_servicing_control_assertion`: validates policy, writes owned `lending_origination_servicing_lending_origination_servicing_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_lending_origination_servicing_governed_model`: validates policy, writes owned `lending_origination_servicing_lending_origination_servicing_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_13`: validates policy, writes owned `lending_origination_servicing_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_14`: validates policy, writes owned `lending_origination_servicing_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_15`: validates policy, writes owned `lending_origination_servicing_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_16`: validates policy, writes owned `lending_origination_servicing_loan_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_17`: validates policy, writes owned `lending_origination_servicing_borrower_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lending_origination_servicing_18`: validates policy, writes owned `lending_origination_servicing_underwriting_decision` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Lending Origination and Servicing domain records.
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

Rules are first-class artifacts: ('loan_application_policy', 'borrower_profile_policy', 'underwriting_decision_policy', 'loan_offer_policy', 'disbursement_policy', 'repayment_schedule_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /loan-applications', 'POST /borrower-profiles', 'POST /underwriting-decisions', 'POST /loan-offers', 'POST /disbursements', 'GET /lending-origination-servicing-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `lending_origination_servicing_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('LendingOriginationServicingCreated', 'LendingOriginationServicingUpdated', 'LendingOriginationServicingApproved', 'LendingOriginationServicingExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('loan application board', 'borrower profile board', 'underwriting decision board', 'loan offer board', 'disbursement board', 'repayment schedule board', 'servicing case board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `lending_origination_servicing_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: loan_application, borrower_profile, underwriting_decision, loan_offer, disbursement, repayment_schedule, servicing_case, lending_origination_servicing_policy_rule, lending_origination_servicing_runtime_parameter, lending_origination_servicing_schema_extension, lending_origination_servicing_control_assertion, lending_origination_servicing_governed_model
- operations: create_loan_application, record_borrower_profile, review_underwriting_decision, approve_loan_offer, simulate_disbursement, create_repayment_schedule, record_servicing_case, review_lending_origination_servicing_policy_rule, approve_lending_origination_servicing_runtime_parameter, simulate_lending_origination_servicing_schema_extension, create_lending_origination_servicing_control_assertion, record_lending_origination_servicing_governed_model, operate_lending_origination_servicing_13, operate_lending_origination_servicing_14, operate_lending_origination_servicing_15, operate_lending_origination_servicing_16, operate_lending_origination_servicing_17, operate_lending_origination_servicing_18
- emits: LendingOriginationServicingCreated, LendingOriginationServicingUpdated, LendingOriginationServicingApproved, LendingOriginationServicingExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: loan_application_policy, borrower_profile_policy, underwriting_decision_policy, loan_offer_policy, disbursement_policy, repayment_schedule_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: LendingOriginationServicingWorkbench, LendingOriginationServicingDetail, LendingOriginationServicingAssistantPanel
- permissions: lending_origination_servicing.read, lending_origination_servicing.create, lending_origination_servicing.update, lending_origination_servicing.approve, lending_origination_servicing.admin
- configuration: LENDING_ORIGINATION_SERVICING_DATABASE_URL, LENDING_ORIGINATION_SERVICING_EVENT_TOPIC, LENDING_ORIGINATION_SERVICING_RETRY_LIMIT, LENDING_ORIGINATION_SERVICING_DEFAULT_POLICY
- standard_features: loan_application_management, lending_origination_servicing_workflow, lending_origination_servicing_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: lending_origination_servicing_event_sourced_operational_history, lending_origination_servicing_multi_tenant_policy_isolation, lending_origination_servicing_schema_evolution_resilience, lending_origination_servicing_autonomous_anomaly_detection, lending_origination_servicing_semantic_document_instruction_understanding, lending_origination_servicing_predictive_risk_scoring, lending_origination_servicing_counterfactual_scenario_simulation, lending_origination_servicing_cryptographic_audit_proofs, lending_origination_servicing_continuous_control_testing, lending_origination_servicing_carbon_and_sustainability_awareness, lending_origination_servicing_cross_pbc_event_federation, lending_origination_servicing_governed_ai_agent_execution
