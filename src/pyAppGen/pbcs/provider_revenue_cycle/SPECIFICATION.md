# Provider Revenue Cycle PBC

## Purpose

The `provider_revenue_cycle` PBC is a packaged business capability for Healthcare registration, charge capture, coding, claims, denials, payment posting, collections, and revenue integrity. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `provider_revenue_cycle`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/provider_revenue_cycle`.
- Runtime entrypoint: `provider_revenue_cycle_runtime_capabilities()`.
- UI entrypoint: `provider_revenue_cycle_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `provider_revenue_cycle_patient_account`: owns patient account lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_charge_capture`: owns charge capture lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_coding_workqueue`: owns coding workqueue lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_claim_batch`: owns claim batch lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_denial_case`: owns denial case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_payment_posting`: owns payment posting lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_collection_account`: owns collection account lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_provider_revenue_cycle_policy_rule`: owns provider revenue cycle policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_provider_revenue_cycle_runtime_parameter`: owns provider revenue cycle runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_provider_revenue_cycle_schema_extension`: owns provider revenue cycle schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_provider_revenue_cycle_control_assertion`: owns provider revenue cycle control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `provider_revenue_cycle_provider_revenue_cycle_governed_model`: owns provider revenue cycle governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `provider_revenue_cycle_appgen_outbox_event`, `provider_revenue_cycle_appgen_inbox_event`, and `provider_revenue_cycle_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /patient-accounts', 'POST /charge-captures', 'POST /coding-workqueues', 'POST /claim-batchs', 'POST /denial-cases', 'GET /provider-revenue-cycle-workbench').

## Executable Domain Operations

- `create_patient_account`: validates policy, writes owned `provider_revenue_cycle_patient_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_charge_capture`: validates policy, writes owned `provider_revenue_cycle_charge_capture` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_coding_workqueue`: validates policy, writes owned `provider_revenue_cycle_coding_workqueue` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_claim_batch`: validates policy, writes owned `provider_revenue_cycle_claim_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_denial_case`: validates policy, writes owned `provider_revenue_cycle_denial_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_payment_posting`: validates policy, writes owned `provider_revenue_cycle_payment_posting` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_collection_account`: validates policy, writes owned `provider_revenue_cycle_collection_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_provider_revenue_cycle_policy_rule`: validates policy, writes owned `provider_revenue_cycle_provider_revenue_cycle_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_provider_revenue_cycle_runtime_parameter`: validates policy, writes owned `provider_revenue_cycle_provider_revenue_cycle_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_provider_revenue_cycle_schema_extension`: validates policy, writes owned `provider_revenue_cycle_provider_revenue_cycle_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_provider_revenue_cycle_control_assertion`: validates policy, writes owned `provider_revenue_cycle_provider_revenue_cycle_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_provider_revenue_cycle_governed_model`: validates policy, writes owned `provider_revenue_cycle_provider_revenue_cycle_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_13`: validates policy, writes owned `provider_revenue_cycle_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_14`: validates policy, writes owned `provider_revenue_cycle_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_15`: validates policy, writes owned `provider_revenue_cycle_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_16`: validates policy, writes owned `provider_revenue_cycle_patient_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_17`: validates policy, writes owned `provider_revenue_cycle_charge_capture` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_provider_revenue_cycle_18`: validates policy, writes owned `provider_revenue_cycle_coding_workqueue` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Provider Revenue Cycle domain records.
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

Rules are first-class artifacts: ('patient_account_policy', 'charge_capture_policy', 'coding_workqueue_policy', 'claim_batch_policy', 'denial_case_policy', 'payment_posting_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /patient-accounts', 'POST /charge-captures', 'POST /coding-workqueues', 'POST /claim-batchs', 'POST /denial-cases', 'GET /provider-revenue-cycle-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `provider_revenue_cycle_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ProviderRevenueCycleCreated', 'ProviderRevenueCycleUpdated', 'ProviderRevenueCycleApproved', 'ProviderRevenueCycleExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('patient account board', 'charge capture board', 'coding workqueue board', 'claim batch board', 'denial case board', 'payment posting board', 'collection account board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `provider_revenue_cycle_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: patient_account, charge_capture, coding_workqueue, claim_batch, denial_case, payment_posting, collection_account, provider_revenue_cycle_policy_rule, provider_revenue_cycle_runtime_parameter, provider_revenue_cycle_schema_extension, provider_revenue_cycle_control_assertion, provider_revenue_cycle_governed_model
- operations: create_patient_account, record_charge_capture, review_coding_workqueue, approve_claim_batch, simulate_denial_case, create_payment_posting, record_collection_account, review_provider_revenue_cycle_policy_rule, approve_provider_revenue_cycle_runtime_parameter, simulate_provider_revenue_cycle_schema_extension, create_provider_revenue_cycle_control_assertion, record_provider_revenue_cycle_governed_model, operate_provider_revenue_cycle_13, operate_provider_revenue_cycle_14, operate_provider_revenue_cycle_15, operate_provider_revenue_cycle_16, operate_provider_revenue_cycle_17, operate_provider_revenue_cycle_18
- emits: ProviderRevenueCycleCreated, ProviderRevenueCycleUpdated, ProviderRevenueCycleApproved, ProviderRevenueCycleExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: patient_account_policy, charge_capture_policy, coding_workqueue_policy, claim_batch_policy, denial_case_policy, payment_posting_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ProviderRevenueCycleWorkbench, ProviderRevenueCycleDetail, ProviderRevenueCycleAssistantPanel
- permissions: provider_revenue_cycle.read, provider_revenue_cycle.create, provider_revenue_cycle.update, provider_revenue_cycle.approve, provider_revenue_cycle.admin
- configuration: PROVIDER_REVENUE_CYCLE_DATABASE_URL, PROVIDER_REVENUE_CYCLE_EVENT_TOPIC, PROVIDER_REVENUE_CYCLE_RETRY_LIMIT, PROVIDER_REVENUE_CYCLE_DEFAULT_POLICY
- standard_features: patient_account_management, provider_revenue_cycle_workflow, provider_revenue_cycle_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: provider_revenue_cycle_event_sourced_operational_history, provider_revenue_cycle_multi_tenant_policy_isolation, provider_revenue_cycle_schema_evolution_resilience, provider_revenue_cycle_autonomous_anomaly_detection, provider_revenue_cycle_semantic_document_instruction_understanding, provider_revenue_cycle_predictive_risk_scoring, provider_revenue_cycle_counterfactual_scenario_simulation, provider_revenue_cycle_cryptographic_audit_proofs, provider_revenue_cycle_continuous_control_testing, provider_revenue_cycle_carbon_and_sustainability_awareness, provider_revenue_cycle_cross_pbc_event_federation, provider_revenue_cycle_governed_ai_agent_execution
