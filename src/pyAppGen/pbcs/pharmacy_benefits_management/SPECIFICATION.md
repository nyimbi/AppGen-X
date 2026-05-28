# Pharmacy Benefits Management PBC

## Purpose

The `pharmacy_benefits_management` PBC is a packaged business capability for Formulary, prior authorization, pharmacy network, claims, rebates, utilization controls, and medication affordability. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `pharmacy_benefits_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/pharmacy_benefits_management`.
- Runtime entrypoint: `pharmacy_benefits_management_runtime_capabilities()`.
- UI entrypoint: `pharmacy_benefits_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `pharmacy_benefits_management_formulary`: owns formulary lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_drug_coverage_rule`: owns drug coverage rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_prior_authorization`: owns prior authorization lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_claim`: owns pharmacy claim lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_rebate_contract`: owns rebate contract lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_utilization_review`: owns utilization review lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_network`: owns pharmacy network lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_benefits_management_policy_rule`: owns pharmacy benefits management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_benefits_management_runtime_parameter`: owns pharmacy benefits management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_benefits_management_schema_extension`: owns pharmacy benefits management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_benefits_management_control_assertion`: owns pharmacy benefits management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharmacy_benefits_management_pharmacy_benefits_management_governed_model`: owns pharmacy benefits management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `pharmacy_benefits_management_appgen_outbox_event`, `pharmacy_benefits_management_appgen_inbox_event`, and `pharmacy_benefits_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /formularys', 'POST /drug-coverage-rules', 'POST /prior-authorizations', 'POST /pharmacy-claims', 'POST /rebate-contracts', 'GET /pharmacy-benefits-management-workbench').

## Executable Domain Operations

- `create_formulary`: validates policy, writes owned `pharmacy_benefits_management_formulary` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_drug_coverage_rule`: validates policy, writes owned `pharmacy_benefits_management_drug_coverage_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_prior_authorization`: validates policy, writes owned `pharmacy_benefits_management_prior_authorization` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_pharmacy_claim`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_claim` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_rebate_contract`: validates policy, writes owned `pharmacy_benefits_management_rebate_contract` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_utilization_review`: validates policy, writes owned `pharmacy_benefits_management_utilization_review` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_pharmacy_network`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_network` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_pharmacy_benefits_management_policy_rule`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_benefits_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_pharmacy_benefits_management_runtime_parameter`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_benefits_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_pharmacy_benefits_management_schema_extension`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_benefits_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_pharmacy_benefits_management_control_assertion`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_benefits_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_pharmacy_benefits_management_governed_model`: validates policy, writes owned `pharmacy_benefits_management_pharmacy_benefits_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_13`: validates policy, writes owned `pharmacy_benefits_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_14`: validates policy, writes owned `pharmacy_benefits_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_15`: validates policy, writes owned `pharmacy_benefits_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_16`: validates policy, writes owned `pharmacy_benefits_management_formulary` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_17`: validates policy, writes owned `pharmacy_benefits_management_drug_coverage_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharmacy_benefits_management_18`: validates policy, writes owned `pharmacy_benefits_management_prior_authorization` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Pharmacy Benefits Management domain records.
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

Rules are first-class artifacts: ('formulary_policy', 'drug_coverage_rule_policy', 'prior_authorization_policy', 'pharmacy_claim_policy', 'rebate_contract_policy', 'utilization_review_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /formularys', 'POST /drug-coverage-rules', 'POST /prior-authorizations', 'POST /pharmacy-claims', 'POST /rebate-contracts', 'GET /pharmacy-benefits-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `pharmacy_benefits_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PharmacyBenefitsManagementCreated', 'PharmacyBenefitsManagementUpdated', 'PharmacyBenefitsManagementApproved', 'PharmacyBenefitsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('formulary board', 'drug coverage rule board', 'prior authorization board', 'pharmacy claim board', 'rebate contract board', 'utilization review board', 'pharmacy network board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `pharmacy_benefits_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: formulary, drug_coverage_rule, prior_authorization, pharmacy_claim, rebate_contract, utilization_review, pharmacy_network, pharmacy_benefits_management_policy_rule, pharmacy_benefits_management_runtime_parameter, pharmacy_benefits_management_schema_extension, pharmacy_benefits_management_control_assertion, pharmacy_benefits_management_governed_model
- operations: create_formulary, record_drug_coverage_rule, review_prior_authorization, approve_pharmacy_claim, simulate_rebate_contract, create_utilization_review, record_pharmacy_network, review_pharmacy_benefits_management_policy_rule, approve_pharmacy_benefits_management_runtime_parameter, simulate_pharmacy_benefits_management_schema_extension, create_pharmacy_benefits_management_control_assertion, record_pharmacy_benefits_management_governed_model, operate_pharmacy_benefits_management_13, operate_pharmacy_benefits_management_14, operate_pharmacy_benefits_management_15, operate_pharmacy_benefits_management_16, operate_pharmacy_benefits_management_17, operate_pharmacy_benefits_management_18
- emits: PharmacyBenefitsManagementCreated, PharmacyBenefitsManagementUpdated, PharmacyBenefitsManagementApproved, PharmacyBenefitsManagementExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: formulary_policy, drug_coverage_rule_policy, prior_authorization_policy, pharmacy_claim_policy, rebate_contract_policy, utilization_review_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PharmacyBenefitsManagementWorkbench, PharmacyBenefitsManagementDetail, PharmacyBenefitsManagementAssistantPanel
- permissions: pharmacy_benefits_management.read, pharmacy_benefits_management.create, pharmacy_benefits_management.update, pharmacy_benefits_management.approve, pharmacy_benefits_management.admin
- configuration: PHARMACY_BENEFITS_MANAGEMENT_DATABASE_URL, PHARMACY_BENEFITS_MANAGEMENT_EVENT_TOPIC, PHARMACY_BENEFITS_MANAGEMENT_RETRY_LIMIT, PHARMACY_BENEFITS_MANAGEMENT_DEFAULT_POLICY
- standard_features: formulary_management, pharmacy_benefits_management_workflow, pharmacy_benefits_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: pharmacy_benefits_management_event_sourced_operational_history, pharmacy_benefits_management_multi_tenant_policy_isolation, pharmacy_benefits_management_schema_evolution_resilience, pharmacy_benefits_management_autonomous_anomaly_detection, pharmacy_benefits_management_semantic_document_instruction_understanding, pharmacy_benefits_management_predictive_risk_scoring, pharmacy_benefits_management_counterfactual_scenario_simulation, pharmacy_benefits_management_cryptographic_audit_proofs, pharmacy_benefits_management_continuous_control_testing, pharmacy_benefits_management_carbon_and_sustainability_awareness, pharmacy_benefits_management_cross_pbc_event_federation, pharmacy_benefits_management_governed_ai_agent_execution
