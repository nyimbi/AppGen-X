# Insurance Policy Administration PBC

## Purpose

The `policy_administration_insurance` PBC is a packaged business capability for Insurance policy lifecycle, endorsements, renewals, cancellations, billing status, coverage changes, and documents. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `policy_administration_insurance`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/policy_administration_insurance`.
- Runtime entrypoint: `policy_administration_insurance_runtime_capabilities()`.
- UI entrypoint: `policy_administration_insurance_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `policy_administration_insurance_insurance_policy`: owns insurance policy lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_coverage_item`: owns coverage item lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_endorsement`: owns endorsement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_renewal_notice`: owns renewal notice lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_cancellation_event`: owns cancellation event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_billing_status`: owns billing status lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_document`: owns policy document lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_administration_insurance_policy_rule`: owns policy administration insurance policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_administration_insurance_runtime_parameter`: owns policy administration insurance runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_administration_insurance_schema_extension`: owns policy administration insurance schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_administration_insurance_control_assertion`: owns policy administration insurance control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `policy_administration_insurance_policy_administration_insurance_governed_model`: owns policy administration insurance governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `policy_administration_insurance_appgen_outbox_event`, `policy_administration_insurance_appgen_inbox_event`, and `policy_administration_insurance_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /insurance-policys', 'POST /coverage-items', 'POST /endorsements', 'POST /renewal-notices', 'POST /cancellation-events', 'GET /policy-administration-insurance-workbench').

## Executable Domain Operations

- `create_insurance_policy`: validates policy, writes owned `policy_administration_insurance_insurance_policy` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_coverage_item`: validates policy, writes owned `policy_administration_insurance_coverage_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_endorsement`: validates policy, writes owned `policy_administration_insurance_endorsement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_renewal_notice`: validates policy, writes owned `policy_administration_insurance_renewal_notice` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_cancellation_event`: validates policy, writes owned `policy_administration_insurance_cancellation_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_billing_status`: validates policy, writes owned `policy_administration_insurance_billing_status` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_policy_document`: validates policy, writes owned `policy_administration_insurance_policy_document` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_policy_administration_insurance_policy_rule`: validates policy, writes owned `policy_administration_insurance_policy_administration_insurance_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_policy_administration_insurance_runtime_parameter`: validates policy, writes owned `policy_administration_insurance_policy_administration_insurance_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_policy_administration_insurance_schema_extension`: validates policy, writes owned `policy_administration_insurance_policy_administration_insurance_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_policy_administration_insurance_control_assertion`: validates policy, writes owned `policy_administration_insurance_policy_administration_insurance_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_policy_administration_insurance_governed_model`: validates policy, writes owned `policy_administration_insurance_policy_administration_insurance_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_13`: validates policy, writes owned `policy_administration_insurance_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_14`: validates policy, writes owned `policy_administration_insurance_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_15`: validates policy, writes owned `policy_administration_insurance_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_16`: validates policy, writes owned `policy_administration_insurance_insurance_policy` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_17`: validates policy, writes owned `policy_administration_insurance_coverage_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_policy_administration_insurance_18`: validates policy, writes owned `policy_administration_insurance_endorsement` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Insurance Policy Administration domain records.
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

Rules are first-class artifacts: ('insurance_policy_policy', 'coverage_item_policy', 'endorsement_policy', 'renewal_notice_policy', 'cancellation_event_policy', 'billing_status_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /insurance-policys', 'POST /coverage-items', 'POST /endorsements', 'POST /renewal-notices', 'POST /cancellation-events', 'GET /policy-administration-insurance-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `policy_administration_insurance_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PolicyAdministrationInsuranceCreated', 'PolicyAdministrationInsuranceUpdated', 'PolicyAdministrationInsuranceApproved', 'PolicyAdministrationInsuranceExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('insurance policy board', 'coverage item board', 'endorsement board', 'renewal notice board', 'cancellation event board', 'billing status board', 'policy document board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `policy_administration_insurance_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: insurance_policy, coverage_item, endorsement, renewal_notice, cancellation_event, billing_status, policy_document, policy_administration_insurance_policy_rule, policy_administration_insurance_runtime_parameter, policy_administration_insurance_schema_extension, policy_administration_insurance_control_assertion, policy_administration_insurance_governed_model
- operations: create_insurance_policy, record_coverage_item, review_endorsement, approve_renewal_notice, simulate_cancellation_event, create_billing_status, record_policy_document, review_policy_administration_insurance_policy_rule, approve_policy_administration_insurance_runtime_parameter, simulate_policy_administration_insurance_schema_extension, create_policy_administration_insurance_control_assertion, record_policy_administration_insurance_governed_model, operate_policy_administration_insurance_13, operate_policy_administration_insurance_14, operate_policy_administration_insurance_15, operate_policy_administration_insurance_16, operate_policy_administration_insurance_17, operate_policy_administration_insurance_18
- emits: PolicyAdministrationInsuranceCreated, PolicyAdministrationInsuranceUpdated, PolicyAdministrationInsuranceApproved, PolicyAdministrationInsuranceExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: insurance_policy_policy, coverage_item_policy, endorsement_policy, renewal_notice_policy, cancellation_event_policy, billing_status_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PolicyAdministrationInsuranceWorkbench, PolicyAdministrationInsuranceDetail, PolicyAdministrationInsuranceAssistantPanel
- permissions: policy_administration_insurance.read, policy_administration_insurance.create, policy_administration_insurance.update, policy_administration_insurance.approve, policy_administration_insurance.admin
- configuration: POLICY_ADMINISTRATION_INSURANCE_DATABASE_URL, POLICY_ADMINISTRATION_INSURANCE_EVENT_TOPIC, POLICY_ADMINISTRATION_INSURANCE_RETRY_LIMIT, POLICY_ADMINISTRATION_INSURANCE_DEFAULT_POLICY
- standard_features: insurance_policy_management, policy_administration_insurance_workflow, policy_administration_insurance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: policy_administration_insurance_event_sourced_operational_history, policy_administration_insurance_multi_tenant_policy_isolation, policy_administration_insurance_schema_evolution_resilience, policy_administration_insurance_autonomous_anomaly_detection, policy_administration_insurance_semantic_document_instruction_understanding, policy_administration_insurance_predictive_risk_scoring, policy_administration_insurance_counterfactual_scenario_simulation, policy_administration_insurance_cryptographic_audit_proofs, policy_administration_insurance_continuous_control_testing, policy_administration_insurance_carbon_and_sustainability_awareness, policy_administration_insurance_cross_pbc_event_federation, policy_administration_insurance_governed_ai_agent_execution
