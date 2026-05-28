# Lease Lending and Equipment Finance PBC

## Purpose

The `lease_lending_equipment_finance` PBC is a packaged business capability for Equipment leases, assets, schedules, residuals, buyouts, repossession, and finance servicing. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `lease_lending_equipment_finance`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/lease_lending_equipment_finance`.
- Runtime entrypoint: `lease_lending_equipment_finance_runtime_capabilities()`.
- UI entrypoint: `lease_lending_equipment_finance_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `lease_lending_equipment_finance_equipment_lease`: owns equipment lease lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_leased_asset`: owns leased asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_payment_schedule`: owns payment schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_residual_value`: owns residual value lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_buyout_quote`: owns buyout quote lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_repo_case`: owns repo case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_servicing_event`: owns lease servicing event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_lending_equipment_finance_policy_rule`: owns lease lending equipment finance policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_lending_equipment_finance_runtime_parameter`: owns lease lending equipment finance runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_lending_equipment_finance_schema_extension`: owns lease lending equipment finance schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_lending_equipment_finance_control_assertion`: owns lease lending equipment finance control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `lease_lending_equipment_finance_lease_lending_equipment_finance_governed_model`: owns lease lending equipment finance governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `lease_lending_equipment_finance_appgen_outbox_event`, `lease_lending_equipment_finance_appgen_inbox_event`, and `lease_lending_equipment_finance_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /equipment-leases', 'POST /leased-assets', 'POST /payment-schedules', 'POST /residual-values', 'POST /buyout-quotes', 'GET /lease-lending-equipment-finance-workbench').

## Executable Domain Operations

- `create_equipment_lease`: validates policy, writes owned `lease_lending_equipment_finance_equipment_lease` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_leased_asset`: validates policy, writes owned `lease_lending_equipment_finance_leased_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_payment_schedule`: validates policy, writes owned `lease_lending_equipment_finance_payment_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_residual_value`: validates policy, writes owned `lease_lending_equipment_finance_residual_value` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_buyout_quote`: validates policy, writes owned `lease_lending_equipment_finance_buyout_quote` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_repo_case`: validates policy, writes owned `lease_lending_equipment_finance_repo_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_lease_servicing_event`: validates policy, writes owned `lease_lending_equipment_finance_lease_servicing_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_lease_lending_equipment_finance_policy_rule`: validates policy, writes owned `lease_lending_equipment_finance_lease_lending_equipment_finance_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_lease_lending_equipment_finance_runtime_parameter`: validates policy, writes owned `lease_lending_equipment_finance_lease_lending_equipment_finance_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_lease_lending_equipment_finance_schema_extension`: validates policy, writes owned `lease_lending_equipment_finance_lease_lending_equipment_finance_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_lease_lending_equipment_finance_control_assertion`: validates policy, writes owned `lease_lending_equipment_finance_lease_lending_equipment_finance_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_lease_lending_equipment_finance_governed_model`: validates policy, writes owned `lease_lending_equipment_finance_lease_lending_equipment_finance_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_13`: validates policy, writes owned `lease_lending_equipment_finance_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_14`: validates policy, writes owned `lease_lending_equipment_finance_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_15`: validates policy, writes owned `lease_lending_equipment_finance_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_16`: validates policy, writes owned `lease_lending_equipment_finance_equipment_lease` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_17`: validates policy, writes owned `lease_lending_equipment_finance_leased_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_lease_lending_equipment_finance_18`: validates policy, writes owned `lease_lending_equipment_finance_payment_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Lease Lending and Equipment Finance domain records.
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

Rules are first-class artifacts: ('equipment_lease_policy', 'leased_asset_policy', 'payment_schedule_policy', 'residual_value_policy', 'buyout_quote_policy', 'repo_case_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /equipment-leases', 'POST /leased-assets', 'POST /payment-schedules', 'POST /residual-values', 'POST /buyout-quotes', 'GET /lease-lending-equipment-finance-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `lease_lending_equipment_finance_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('LeaseLendingEquipmentFinanceCreated', 'LeaseLendingEquipmentFinanceUpdated', 'LeaseLendingEquipmentFinanceApproved', 'LeaseLendingEquipmentFinanceExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('equipment lease board', 'leased asset board', 'payment schedule board', 'residual value board', 'buyout quote board', 'repo case board', 'lease servicing event board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `lease_lending_equipment_finance_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: equipment_lease, leased_asset, payment_schedule, residual_value, buyout_quote, repo_case, lease_servicing_event, lease_lending_equipment_finance_policy_rule, lease_lending_equipment_finance_runtime_parameter, lease_lending_equipment_finance_schema_extension, lease_lending_equipment_finance_control_assertion, lease_lending_equipment_finance_governed_model
- operations: create_equipment_lease, record_leased_asset, review_payment_schedule, approve_residual_value, simulate_buyout_quote, create_repo_case, record_lease_servicing_event, review_lease_lending_equipment_finance_policy_rule, approve_lease_lending_equipment_finance_runtime_parameter, simulate_lease_lending_equipment_finance_schema_extension, create_lease_lending_equipment_finance_control_assertion, record_lease_lending_equipment_finance_governed_model, operate_lease_lending_equipment_finance_13, operate_lease_lending_equipment_finance_14, operate_lease_lending_equipment_finance_15, operate_lease_lending_equipment_finance_16, operate_lease_lending_equipment_finance_17, operate_lease_lending_equipment_finance_18
- emits: LeaseLendingEquipmentFinanceCreated, LeaseLendingEquipmentFinanceUpdated, LeaseLendingEquipmentFinanceApproved, LeaseLendingEquipmentFinanceExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: equipment_lease_policy, leased_asset_policy, payment_schedule_policy, residual_value_policy, buyout_quote_policy, repo_case_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: LeaseLendingEquipmentFinanceWorkbench, LeaseLendingEquipmentFinanceDetail, LeaseLendingEquipmentFinanceAssistantPanel
- permissions: lease_lending_equipment_finance.read, lease_lending_equipment_finance.create, lease_lending_equipment_finance.update, lease_lending_equipment_finance.approve, lease_lending_equipment_finance.admin
- configuration: LEASE_LENDING_EQUIPMENT_FINANCE_DATABASE_URL, LEASE_LENDING_EQUIPMENT_FINANCE_EVENT_TOPIC, LEASE_LENDING_EQUIPMENT_FINANCE_RETRY_LIMIT, LEASE_LENDING_EQUIPMENT_FINANCE_DEFAULT_POLICY
- standard_features: equipment_lease_management, lease_lending_equipment_finance_workflow, lease_lending_equipment_finance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: lease_lending_equipment_finance_event_sourced_operational_history, lease_lending_equipment_finance_multi_tenant_policy_isolation, lease_lending_equipment_finance_schema_evolution_resilience, lease_lending_equipment_finance_autonomous_anomaly_detection, lease_lending_equipment_finance_semantic_document_instruction_understanding, lease_lending_equipment_finance_predictive_risk_scoring, lease_lending_equipment_finance_counterfactual_scenario_simulation, lease_lending_equipment_finance_cryptographic_audit_proofs, lease_lending_equipment_finance_continuous_control_testing, lease_lending_equipment_finance_carbon_and_sustainability_awareness, lease_lending_equipment_finance_cross_pbc_event_federation, lease_lending_equipment_finance_governed_ai_agent_execution
