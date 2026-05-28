# Healthcare Claims Adjudication PBC

## Purpose

The `claims_adjudication_healthcare` PBC is a packaged business capability for Healthcare claim intake, coding validation, benefit rules, denials, appeals, payment integrity, and payer adjudication. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `claims_adjudication_healthcare`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/claims_adjudication_healthcare`.
- Runtime entrypoint: `claims_adjudication_healthcare_runtime_capabilities()`.
- UI entrypoint: `claims_adjudication_healthcare_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `claims_adjudication_healthcare_health_claim`: owns health claim lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claim_line`: owns claim line lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_coding_review`: owns coding review lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_benefit_rule`: owns benefit rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_denial`: owns denial lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_appeal`: owns appeal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_payment_determination`: owns payment determination lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claims_adjudication_healthcare_policy_rule`: owns claims adjudication healthcare policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claims_adjudication_healthcare_runtime_parameter`: owns claims adjudication healthcare runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claims_adjudication_healthcare_schema_extension`: owns claims adjudication healthcare schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claims_adjudication_healthcare_control_assertion`: owns claims adjudication healthcare control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `claims_adjudication_healthcare_claims_adjudication_healthcare_governed_model`: owns claims adjudication healthcare governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `claims_adjudication_healthcare_appgen_outbox_event`, `claims_adjudication_healthcare_appgen_inbox_event`, and `claims_adjudication_healthcare_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /health-claims', 'POST /claim-lines', 'POST /coding-reviews', 'POST /benefit-rules', 'POST /denials', 'GET /claims-adjudication-healthcare-workbench').

## Executable Domain Operations

- `create_health_claim`: validates policy, writes owned `claims_adjudication_healthcare_health_claim` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_claim_line`: validates policy, writes owned `claims_adjudication_healthcare_claim_line` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_coding_review`: validates policy, writes owned `claims_adjudication_healthcare_coding_review` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_benefit_rule`: validates policy, writes owned `claims_adjudication_healthcare_benefit_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_denial`: validates policy, writes owned `claims_adjudication_healthcare_denial` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_appeal`: validates policy, writes owned `claims_adjudication_healthcare_appeal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_payment_determination`: validates policy, writes owned `claims_adjudication_healthcare_payment_determination` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_claims_adjudication_healthcare_policy_rule`: validates policy, writes owned `claims_adjudication_healthcare_claims_adjudication_healthcare_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_claims_adjudication_healthcare_runtime_parameter`: validates policy, writes owned `claims_adjudication_healthcare_claims_adjudication_healthcare_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_claims_adjudication_healthcare_schema_extension`: validates policy, writes owned `claims_adjudication_healthcare_claims_adjudication_healthcare_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_claims_adjudication_healthcare_control_assertion`: validates policy, writes owned `claims_adjudication_healthcare_claims_adjudication_healthcare_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_claims_adjudication_healthcare_governed_model`: validates policy, writes owned `claims_adjudication_healthcare_claims_adjudication_healthcare_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_13`: validates policy, writes owned `claims_adjudication_healthcare_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_14`: validates policy, writes owned `claims_adjudication_healthcare_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_15`: validates policy, writes owned `claims_adjudication_healthcare_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_16`: validates policy, writes owned `claims_adjudication_healthcare_health_claim` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_17`: validates policy, writes owned `claims_adjudication_healthcare_claim_line` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_claims_adjudication_healthcare_18`: validates policy, writes owned `claims_adjudication_healthcare_coding_review` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Healthcare Claims Adjudication domain records.
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

Rules are first-class artifacts: ('health_claim_policy', 'claim_line_policy', 'coding_review_policy', 'benefit_rule_policy', 'denial_policy', 'appeal_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /health-claims', 'POST /claim-lines', 'POST /coding-reviews', 'POST /benefit-rules', 'POST /denials', 'GET /claims-adjudication-healthcare-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `claims_adjudication_healthcare_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ClaimsAdjudicationHealthcareCreated', 'ClaimsAdjudicationHealthcareUpdated', 'ClaimsAdjudicationHealthcareApproved', 'ClaimsAdjudicationHealthcareExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('health claim board', 'claim line board', 'coding review board', 'benefit rule board', 'denial board', 'appeal board', 'payment determination board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `claims_adjudication_healthcare_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: health_claim, claim_line, coding_review, benefit_rule, denial, appeal, payment_determination, claims_adjudication_healthcare_policy_rule, claims_adjudication_healthcare_runtime_parameter, claims_adjudication_healthcare_schema_extension, claims_adjudication_healthcare_control_assertion, claims_adjudication_healthcare_governed_model
- operations: create_health_claim, record_claim_line, review_coding_review, approve_benefit_rule, simulate_denial, create_appeal, record_payment_determination, review_claims_adjudication_healthcare_policy_rule, approve_claims_adjudication_healthcare_runtime_parameter, simulate_claims_adjudication_healthcare_schema_extension, create_claims_adjudication_healthcare_control_assertion, record_claims_adjudication_healthcare_governed_model, operate_claims_adjudication_healthcare_13, operate_claims_adjudication_healthcare_14, operate_claims_adjudication_healthcare_15, operate_claims_adjudication_healthcare_16, operate_claims_adjudication_healthcare_17, operate_claims_adjudication_healthcare_18
- emits: ClaimsAdjudicationHealthcareCreated, ClaimsAdjudicationHealthcareUpdated, ClaimsAdjudicationHealthcareApproved, ClaimsAdjudicationHealthcareExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: health_claim_policy, claim_line_policy, coding_review_policy, benefit_rule_policy, denial_policy, appeal_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ClaimsAdjudicationHealthcareWorkbench, ClaimsAdjudicationHealthcareDetail, ClaimsAdjudicationHealthcareAssistantPanel
- permissions: claims_adjudication_healthcare.read, claims_adjudication_healthcare.create, claims_adjudication_healthcare.update, claims_adjudication_healthcare.approve, claims_adjudication_healthcare.admin
- configuration: CLAIMS_ADJUDICATION_HEALTHCARE_DATABASE_URL, CLAIMS_ADJUDICATION_HEALTHCARE_EVENT_TOPIC, CLAIMS_ADJUDICATION_HEALTHCARE_RETRY_LIMIT, CLAIMS_ADJUDICATION_HEALTHCARE_DEFAULT_POLICY
- standard_features: health_claim_management, claims_adjudication_healthcare_workflow, claims_adjudication_healthcare_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: claims_adjudication_healthcare_event_sourced_operational_history, claims_adjudication_healthcare_multi_tenant_policy_isolation, claims_adjudication_healthcare_schema_evolution_resilience, claims_adjudication_healthcare_autonomous_anomaly_detection, claims_adjudication_healthcare_semantic_document_instruction_understanding, claims_adjudication_healthcare_predictive_risk_scoring, claims_adjudication_healthcare_counterfactual_scenario_simulation, claims_adjudication_healthcare_cryptographic_audit_proofs, claims_adjudication_healthcare_continuous_control_testing, claims_adjudication_healthcare_carbon_and_sustainability_awareness, claims_adjudication_healthcare_cross_pbc_event_federation, claims_adjudication_healthcare_governed_ai_agent_execution
