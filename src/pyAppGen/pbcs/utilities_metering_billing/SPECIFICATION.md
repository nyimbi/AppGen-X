# Utilities Metering and Billing PBC

## Purpose

The `utilities_metering_billing` PBC is a packaged business capability for Meter reads, usage validation, tariffs, service orders, bills, adjustments, collections, and customer utility billing. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `utilities_metering_billing`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/utilities_metering_billing`.
- Runtime entrypoint: `utilities_metering_billing_runtime_capabilities()`.
- UI entrypoint: `utilities_metering_billing_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `utilities_metering_billing_meter_read`: owns meter read lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_usage_interval`: owns usage interval lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_tariff`: owns tariff lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_service_order`: owns service order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utility_bill`: owns utility bill lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_billing_adjustment`: owns billing adjustment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_customer_meter_account`: owns customer meter account lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utilities_metering_billing_policy_rule`: owns utilities metering billing policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utilities_metering_billing_runtime_parameter`: owns utilities metering billing runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utilities_metering_billing_schema_extension`: owns utilities metering billing schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utilities_metering_billing_control_assertion`: owns utilities metering billing control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utilities_metering_billing_utilities_metering_billing_governed_model`: owns utilities metering billing governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `utilities_metering_billing_appgen_outbox_event`, `utilities_metering_billing_appgen_inbox_event`, and `utilities_metering_billing_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /meter-reads', 'POST /usage-intervals', 'POST /tariffs', 'POST /service-orders', 'POST /utility-bills', 'GET /utilities-metering-billing-workbench').

## Executable Domain Operations

- `create_meter_read`: validates policy, writes owned `utilities_metering_billing_meter_read` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_usage_interval`: validates policy, writes owned `utilities_metering_billing_usage_interval` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_tariff`: validates policy, writes owned `utilities_metering_billing_tariff` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_service_order`: validates policy, writes owned `utilities_metering_billing_service_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_utility_bill`: validates policy, writes owned `utilities_metering_billing_utility_bill` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_billing_adjustment`: validates policy, writes owned `utilities_metering_billing_billing_adjustment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_customer_meter_account`: validates policy, writes owned `utilities_metering_billing_customer_meter_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_utilities_metering_billing_policy_rule`: validates policy, writes owned `utilities_metering_billing_utilities_metering_billing_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_utilities_metering_billing_runtime_parameter`: validates policy, writes owned `utilities_metering_billing_utilities_metering_billing_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_utilities_metering_billing_schema_extension`: validates policy, writes owned `utilities_metering_billing_utilities_metering_billing_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_utilities_metering_billing_control_assertion`: validates policy, writes owned `utilities_metering_billing_utilities_metering_billing_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_utilities_metering_billing_governed_model`: validates policy, writes owned `utilities_metering_billing_utilities_metering_billing_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_13`: validates policy, writes owned `utilities_metering_billing_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_14`: validates policy, writes owned `utilities_metering_billing_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_15`: validates policy, writes owned `utilities_metering_billing_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_16`: validates policy, writes owned `utilities_metering_billing_meter_read` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_17`: validates policy, writes owned `utilities_metering_billing_usage_interval` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utilities_metering_billing_18`: validates policy, writes owned `utilities_metering_billing_tariff` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Utilities Metering and Billing domain records.
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

Rules are first-class artifacts: ('meter_read_policy', 'usage_interval_policy', 'tariff_policy', 'service_order_policy', 'utility_bill_policy', 'billing_adjustment_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /meter-reads', 'POST /usage-intervals', 'POST /tariffs', 'POST /service-orders', 'POST /utility-bills', 'GET /utilities-metering-billing-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `utilities_metering_billing_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('UtilitiesMeteringBillingCreated', 'UtilitiesMeteringBillingUpdated', 'UtilitiesMeteringBillingApproved', 'UtilitiesMeteringBillingExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('meter read board', 'usage interval board', 'tariff board', 'service order board', 'utility bill board', 'billing adjustment board', 'customer meter account board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `utilities_metering_billing_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: meter_read, usage_interval, tariff, service_order, utility_bill, billing_adjustment, customer_meter_account, utilities_metering_billing_policy_rule, utilities_metering_billing_runtime_parameter, utilities_metering_billing_schema_extension, utilities_metering_billing_control_assertion, utilities_metering_billing_governed_model
- operations: create_meter_read, record_usage_interval, review_tariff, approve_service_order, simulate_utility_bill, create_billing_adjustment, record_customer_meter_account, review_utilities_metering_billing_policy_rule, approve_utilities_metering_billing_runtime_parameter, simulate_utilities_metering_billing_schema_extension, create_utilities_metering_billing_control_assertion, record_utilities_metering_billing_governed_model, operate_utilities_metering_billing_13, operate_utilities_metering_billing_14, operate_utilities_metering_billing_15, operate_utilities_metering_billing_16, operate_utilities_metering_billing_17, operate_utilities_metering_billing_18
- emits: UtilitiesMeteringBillingCreated, UtilitiesMeteringBillingUpdated, UtilitiesMeteringBillingApproved, UtilitiesMeteringBillingExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: meter_read_policy, usage_interval_policy, tariff_policy, service_order_policy, utility_bill_policy, billing_adjustment_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: UtilitiesMeteringBillingWorkbench, UtilitiesMeteringBillingDetail, UtilitiesMeteringBillingAssistantPanel
- permissions: utilities_metering_billing.read, utilities_metering_billing.create, utilities_metering_billing.update, utilities_metering_billing.approve, utilities_metering_billing.admin
- configuration: UTILITIES_METERING_BILLING_DATABASE_URL, UTILITIES_METERING_BILLING_EVENT_TOPIC, UTILITIES_METERING_BILLING_RETRY_LIMIT, UTILITIES_METERING_BILLING_DEFAULT_POLICY
- standard_features: meter_read_management, utilities_metering_billing_workflow, utilities_metering_billing_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: utilities_metering_billing_event_sourced_operational_history, utilities_metering_billing_multi_tenant_policy_isolation, utilities_metering_billing_schema_evolution_resilience, utilities_metering_billing_autonomous_anomaly_detection, utilities_metering_billing_semantic_document_instruction_understanding, utilities_metering_billing_predictive_risk_scoring, utilities_metering_billing_counterfactual_scenario_simulation, utilities_metering_billing_cryptographic_audit_proofs, utilities_metering_billing_continuous_control_testing, utilities_metering_billing_carbon_and_sustainability_awareness, utilities_metering_billing_cross_pbc_event_federation, utilities_metering_billing_governed_ai_agent_execution
