# Construction Contracts and Commercials PBC

## Purpose

The `construction_contracts_commercials` PBC is a packaged business capability for Construction contracts, pay applications, retainage, claims, variations, lien waivers, and commercial controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `construction_contracts_commercials`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/construction_contracts_commercials`.
- Runtime entrypoint: `construction_contracts_commercials_runtime_capabilities()`.
- UI entrypoint: `construction_contracts_commercials_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `construction_contracts_commercials_construction_contract`: owns construction contract lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_pay_application`: owns pay application lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_retainage`: owns retainage lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_variation_order`: owns variation order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_commercial_claim`: owns commercial claim lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_lien_waiver`: owns lien waiver lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_subcontract_package`: owns subcontract package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_construction_contracts_commercials_policy_rule`: owns construction contracts commercials policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_construction_contracts_commercials_runtime_parameter`: owns construction contracts commercials runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_construction_contracts_commercials_schema_extension`: owns construction contracts commercials schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_construction_contracts_commercials_control_assertion`: owns construction contracts commercials control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_contracts_commercials_construction_contracts_commercials_governed_model`: owns construction contracts commercials governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `construction_contracts_commercials_appgen_outbox_event`, `construction_contracts_commercials_appgen_inbox_event`, and `construction_contracts_commercials_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /construction-contracts', 'POST /pay-applications', 'POST /retainages', 'POST /variation-orders', 'POST /commercial-claims', 'GET /construction-contracts-commercials-workbench').

## Executable Domain Operations

- `create_construction_contract`: validates policy, writes owned `construction_contracts_commercials_construction_contract` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_pay_application`: validates policy, writes owned `construction_contracts_commercials_pay_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_retainage`: validates policy, writes owned `construction_contracts_commercials_retainage` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_variation_order`: validates policy, writes owned `construction_contracts_commercials_variation_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_commercial_claim`: validates policy, writes owned `construction_contracts_commercials_commercial_claim` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_lien_waiver`: validates policy, writes owned `construction_contracts_commercials_lien_waiver` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_subcontract_package`: validates policy, writes owned `construction_contracts_commercials_subcontract_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_construction_contracts_commercials_policy_rule`: validates policy, writes owned `construction_contracts_commercials_construction_contracts_commercials_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_construction_contracts_commercials_runtime_parameter`: validates policy, writes owned `construction_contracts_commercials_construction_contracts_commercials_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_construction_contracts_commercials_schema_extension`: validates policy, writes owned `construction_contracts_commercials_construction_contracts_commercials_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_construction_contracts_commercials_control_assertion`: validates policy, writes owned `construction_contracts_commercials_construction_contracts_commercials_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_construction_contracts_commercials_governed_model`: validates policy, writes owned `construction_contracts_commercials_construction_contracts_commercials_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_13`: validates policy, writes owned `construction_contracts_commercials_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_14`: validates policy, writes owned `construction_contracts_commercials_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_15`: validates policy, writes owned `construction_contracts_commercials_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_16`: validates policy, writes owned `construction_contracts_commercials_construction_contract` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_17`: validates policy, writes owned `construction_contracts_commercials_pay_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_contracts_commercials_18`: validates policy, writes owned `construction_contracts_commercials_retainage` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Construction Contracts and Commercials domain records.
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

Rules are first-class artifacts: ('construction_contract_policy', 'pay_application_policy', 'retainage_policy', 'variation_order_policy', 'commercial_claim_policy', 'lien_waiver_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /construction-contracts', 'POST /pay-applications', 'POST /retainages', 'POST /variation-orders', 'POST /commercial-claims', 'GET /construction-contracts-commercials-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `construction_contracts_commercials_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ConstructionContractsCommercialsCreated', 'ConstructionContractsCommercialsUpdated', 'ConstructionContractsCommercialsApproved', 'ConstructionContractsCommercialsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('construction contract board', 'pay application board', 'retainage board', 'variation order board', 'commercial claim board', 'lien waiver board', 'subcontract package board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `construction_contracts_commercials_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: construction_contract, pay_application, retainage, variation_order, commercial_claim, lien_waiver, subcontract_package, construction_contracts_commercials_policy_rule, construction_contracts_commercials_runtime_parameter, construction_contracts_commercials_schema_extension, construction_contracts_commercials_control_assertion, construction_contracts_commercials_governed_model
- operations: create_construction_contract, record_pay_application, review_retainage, approve_variation_order, simulate_commercial_claim, create_lien_waiver, record_subcontract_package, review_construction_contracts_commercials_policy_rule, approve_construction_contracts_commercials_runtime_parameter, simulate_construction_contracts_commercials_schema_extension, create_construction_contracts_commercials_control_assertion, record_construction_contracts_commercials_governed_model, operate_construction_contracts_commercials_13, operate_construction_contracts_commercials_14, operate_construction_contracts_commercials_15, operate_construction_contracts_commercials_16, operate_construction_contracts_commercials_17, operate_construction_contracts_commercials_18
- emits: ConstructionContractsCommercialsCreated, ConstructionContractsCommercialsUpdated, ConstructionContractsCommercialsApproved, ConstructionContractsCommercialsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: construction_contract_policy, pay_application_policy, retainage_policy, variation_order_policy, commercial_claim_policy, lien_waiver_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ConstructionContractsCommercialsWorkbench, ConstructionContractsCommercialsDetail, ConstructionContractsCommercialsAssistantPanel
- permissions: construction_contracts_commercials.read, construction_contracts_commercials.create, construction_contracts_commercials.update, construction_contracts_commercials.approve, construction_contracts_commercials.admin
- configuration: CONSTRUCTION_CONTRACTS_COMMERCIALS_DATABASE_URL, CONSTRUCTION_CONTRACTS_COMMERCIALS_EVENT_TOPIC, CONSTRUCTION_CONTRACTS_COMMERCIALS_RETRY_LIMIT, CONSTRUCTION_CONTRACTS_COMMERCIALS_DEFAULT_POLICY
- standard_features: construction_contract_management, construction_contracts_commercials_workflow, construction_contracts_commercials_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: construction_contracts_commercials_event_sourced_operational_history, construction_contracts_commercials_multi_tenant_policy_isolation, construction_contracts_commercials_schema_evolution_resilience, construction_contracts_commercials_autonomous_anomaly_detection, construction_contracts_commercials_semantic_document_instruction_understanding, construction_contracts_commercials_predictive_risk_scoring, construction_contracts_commercials_counterfactual_scenario_simulation, construction_contracts_commercials_cryptographic_audit_proofs, construction_contracts_commercials_continuous_control_testing, construction_contracts_commercials_carbon_and_sustainability_awareness, construction_contracts_commercials_cross_pbc_event_federation, construction_contracts_commercials_governed_ai_agent_execution
