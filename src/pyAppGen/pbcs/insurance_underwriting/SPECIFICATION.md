# Insurance Underwriting PBC

## Purpose

The `insurance_underwriting` PBC is a packaged business capability for Risk submissions, rating, quote generation, underwriting decisions, bind packages, exclusions, and referral workflows. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `insurance_underwriting`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/insurance_underwriting`.
- Runtime entrypoint: `insurance_underwriting_runtime_capabilities()`.
- UI entrypoint: `insurance_underwriting_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `insurance_underwriting_underwriting_submission`: owns underwriting submission lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_risk_profile`: owns risk profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_rating_factor`: owns rating factor lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_quote`: owns quote lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_underwriting_decision`: owns underwriting decision lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_bind_package`: owns bind package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_exclusion`: owns exclusion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_insurance_underwriting_policy_rule`: owns insurance underwriting policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_insurance_underwriting_runtime_parameter`: owns insurance underwriting runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_insurance_underwriting_schema_extension`: owns insurance underwriting schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_insurance_underwriting_control_assertion`: owns insurance underwriting control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `insurance_underwriting_insurance_underwriting_governed_model`: owns insurance underwriting governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `insurance_underwriting_appgen_outbox_event`, `insurance_underwriting_appgen_inbox_event`, and `insurance_underwriting_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /underwriting-submissions', 'POST /risk-profiles', 'POST /rating-factors', 'POST /quotes', 'POST /underwriting-decisions', 'GET /insurance-underwriting-workbench').

## Executable Domain Operations

- `create_underwriting_submission`: validates policy, writes owned `insurance_underwriting_underwriting_submission` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_risk_profile`: validates policy, writes owned `insurance_underwriting_risk_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_rating_factor`: validates policy, writes owned `insurance_underwriting_rating_factor` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_quote`: validates policy, writes owned `insurance_underwriting_quote` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_underwriting_decision`: validates policy, writes owned `insurance_underwriting_underwriting_decision` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_bind_package`: validates policy, writes owned `insurance_underwriting_bind_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_exclusion`: validates policy, writes owned `insurance_underwriting_exclusion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_insurance_underwriting_policy_rule`: validates policy, writes owned `insurance_underwriting_insurance_underwriting_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_insurance_underwriting_runtime_parameter`: validates policy, writes owned `insurance_underwriting_insurance_underwriting_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_insurance_underwriting_schema_extension`: validates policy, writes owned `insurance_underwriting_insurance_underwriting_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_insurance_underwriting_control_assertion`: validates policy, writes owned `insurance_underwriting_insurance_underwriting_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_insurance_underwriting_governed_model`: validates policy, writes owned `insurance_underwriting_insurance_underwriting_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_13`: validates policy, writes owned `insurance_underwriting_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_14`: validates policy, writes owned `insurance_underwriting_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_15`: validates policy, writes owned `insurance_underwriting_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_16`: validates policy, writes owned `insurance_underwriting_underwriting_submission` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_17`: validates policy, writes owned `insurance_underwriting_risk_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_insurance_underwriting_18`: validates policy, writes owned `insurance_underwriting_rating_factor` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Insurance Underwriting domain records.
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

Rules are first-class artifacts: ('underwriting_submission_policy', 'risk_profile_policy', 'rating_factor_policy', 'quote_policy', 'underwriting_decision_policy', 'bind_package_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /underwriting-submissions', 'POST /risk-profiles', 'POST /rating-factors', 'POST /quotes', 'POST /underwriting-decisions', 'GET /insurance-underwriting-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `insurance_underwriting_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('InsuranceUnderwritingCreated', 'InsuranceUnderwritingUpdated', 'InsuranceUnderwritingApproved', 'InsuranceUnderwritingExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('underwriting submission board', 'risk profile board', 'rating factor board', 'quote board', 'underwriting decision board', 'bind package board', 'exclusion board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `insurance_underwriting_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: underwriting_submission, risk_profile, rating_factor, quote, underwriting_decision, bind_package, exclusion, insurance_underwriting_policy_rule, insurance_underwriting_runtime_parameter, insurance_underwriting_schema_extension, insurance_underwriting_control_assertion, insurance_underwriting_governed_model
- operations: create_underwriting_submission, record_risk_profile, review_rating_factor, approve_quote, simulate_underwriting_decision, create_bind_package, record_exclusion, review_insurance_underwriting_policy_rule, approve_insurance_underwriting_runtime_parameter, simulate_insurance_underwriting_schema_extension, create_insurance_underwriting_control_assertion, record_insurance_underwriting_governed_model, operate_insurance_underwriting_13, operate_insurance_underwriting_14, operate_insurance_underwriting_15, operate_insurance_underwriting_16, operate_insurance_underwriting_17, operate_insurance_underwriting_18
- emits: InsuranceUnderwritingCreated, InsuranceUnderwritingUpdated, InsuranceUnderwritingApproved, InsuranceUnderwritingExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: underwriting_submission_policy, risk_profile_policy, rating_factor_policy, quote_policy, underwriting_decision_policy, bind_package_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: InsuranceUnderwritingWorkbench, InsuranceUnderwritingDetail, InsuranceUnderwritingAssistantPanel
- permissions: insurance_underwriting.read, insurance_underwriting.create, insurance_underwriting.update, insurance_underwriting.approve, insurance_underwriting.admin
- configuration: INSURANCE_UNDERWRITING_DATABASE_URL, INSURANCE_UNDERWRITING_EVENT_TOPIC, INSURANCE_UNDERWRITING_RETRY_LIMIT, INSURANCE_UNDERWRITING_DEFAULT_POLICY
- standard_features: underwriting_submission_management, insurance_underwriting_workflow, insurance_underwriting_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: insurance_underwriting_event_sourced_operational_history, insurance_underwriting_multi_tenant_policy_isolation, insurance_underwriting_schema_evolution_resilience, insurance_underwriting_autonomous_anomaly_detection, insurance_underwriting_semantic_document_instruction_understanding, insurance_underwriting_predictive_risk_scoring, insurance_underwriting_counterfactual_scenario_simulation, insurance_underwriting_cryptographic_audit_proofs, insurance_underwriting_continuous_control_testing, insurance_underwriting_carbon_and_sustainability_awareness, insurance_underwriting_cross_pbc_event_federation, insurance_underwriting_governed_ai_agent_execution
