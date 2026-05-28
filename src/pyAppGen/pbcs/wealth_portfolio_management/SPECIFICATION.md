# Wealth Portfolio Management PBC

## Purpose

The `wealth_portfolio_management` PBC is a packaged business capability for Client portfolios, mandates, suitability, rebalancing, performance, fees, and advisory controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `wealth_portfolio_management`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/wealth_portfolio_management`.
- Runtime entrypoint: `wealth_portfolio_management_runtime_capabilities()`.
- UI entrypoint: `wealth_portfolio_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `wealth_portfolio_management_client_portfolio`: owns client portfolio lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_investment_mandate`: owns investment mandate lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_suitability_profile`: owns suitability profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_rebalance_order`: owns rebalance order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_performance_snapshot`: owns performance snapshot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_fee_schedule`: owns fee schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_advisory_review`: owns advisory review lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_wealth_portfolio_management_policy_rule`: owns wealth portfolio management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_wealth_portfolio_management_runtime_parameter`: owns wealth portfolio management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_wealth_portfolio_management_schema_extension`: owns wealth portfolio management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_wealth_portfolio_management_control_assertion`: owns wealth portfolio management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `wealth_portfolio_management_wealth_portfolio_management_governed_model`: owns wealth portfolio management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `wealth_portfolio_management_appgen_outbox_event`, `wealth_portfolio_management_appgen_inbox_event`, and `wealth_portfolio_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /client-portfolios', 'POST /investment-mandates', 'POST /suitability-profiles', 'POST /rebalance-orders', 'POST /performance-snapshots', 'GET /wealth-portfolio-management-workbench').

## Executable Domain Operations

- `create_client_portfolio`: validates policy, writes owned `wealth_portfolio_management_client_portfolio` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_investment_mandate`: validates policy, writes owned `wealth_portfolio_management_investment_mandate` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_suitability_profile`: validates policy, writes owned `wealth_portfolio_management_suitability_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_rebalance_order`: validates policy, writes owned `wealth_portfolio_management_rebalance_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_performance_snapshot`: validates policy, writes owned `wealth_portfolio_management_performance_snapshot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_fee_schedule`: validates policy, writes owned `wealth_portfolio_management_fee_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_advisory_review`: validates policy, writes owned `wealth_portfolio_management_advisory_review` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_wealth_portfolio_management_policy_rule`: validates policy, writes owned `wealth_portfolio_management_wealth_portfolio_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_wealth_portfolio_management_runtime_parameter`: validates policy, writes owned `wealth_portfolio_management_wealth_portfolio_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_wealth_portfolio_management_schema_extension`: validates policy, writes owned `wealth_portfolio_management_wealth_portfolio_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_wealth_portfolio_management_control_assertion`: validates policy, writes owned `wealth_portfolio_management_wealth_portfolio_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_wealth_portfolio_management_governed_model`: validates policy, writes owned `wealth_portfolio_management_wealth_portfolio_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_13`: validates policy, writes owned `wealth_portfolio_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_14`: validates policy, writes owned `wealth_portfolio_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_15`: validates policy, writes owned `wealth_portfolio_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_16`: validates policy, writes owned `wealth_portfolio_management_client_portfolio` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_17`: validates policy, writes owned `wealth_portfolio_management_investment_mandate` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_wealth_portfolio_management_18`: validates policy, writes owned `wealth_portfolio_management_suitability_profile` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Wealth Portfolio Management domain records.
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

Rules are first-class artifacts: ('client_portfolio_policy', 'investment_mandate_policy', 'suitability_profile_policy', 'rebalance_order_policy', 'performance_snapshot_policy', 'fee_schedule_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /client-portfolios', 'POST /investment-mandates', 'POST /suitability-profiles', 'POST /rebalance-orders', 'POST /performance-snapshots', 'GET /wealth-portfolio-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `wealth_portfolio_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('WealthPortfolioManagementCreated', 'WealthPortfolioManagementUpdated', 'WealthPortfolioManagementApproved', 'WealthPortfolioManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('client portfolio board', 'investment mandate board', 'suitability profile board', 'rebalance order board', 'performance snapshot board', 'fee schedule board', 'advisory review board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `wealth_portfolio_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: client_portfolio, investment_mandate, suitability_profile, rebalance_order, performance_snapshot, fee_schedule, advisory_review, wealth_portfolio_management_policy_rule, wealth_portfolio_management_runtime_parameter, wealth_portfolio_management_schema_extension, wealth_portfolio_management_control_assertion, wealth_portfolio_management_governed_model
- operations: create_client_portfolio, record_investment_mandate, review_suitability_profile, approve_rebalance_order, simulate_performance_snapshot, create_fee_schedule, record_advisory_review, review_wealth_portfolio_management_policy_rule, approve_wealth_portfolio_management_runtime_parameter, simulate_wealth_portfolio_management_schema_extension, create_wealth_portfolio_management_control_assertion, record_wealth_portfolio_management_governed_model, operate_wealth_portfolio_management_13, operate_wealth_portfolio_management_14, operate_wealth_portfolio_management_15, operate_wealth_portfolio_management_16, operate_wealth_portfolio_management_17, operate_wealth_portfolio_management_18
- emits: WealthPortfolioManagementCreated, WealthPortfolioManagementUpdated, WealthPortfolioManagementApproved, WealthPortfolioManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: client_portfolio_policy, investment_mandate_policy, suitability_profile_policy, rebalance_order_policy, performance_snapshot_policy, fee_schedule_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: WealthPortfolioManagementWorkbench, WealthPortfolioManagementDetail, WealthPortfolioManagementAssistantPanel
- permissions: wealth_portfolio_management.read, wealth_portfolio_management.create, wealth_portfolio_management.update, wealth_portfolio_management.approve, wealth_portfolio_management.admin
- configuration: WEALTH_PORTFOLIO_MANAGEMENT_DATABASE_URL, WEALTH_PORTFOLIO_MANAGEMENT_EVENT_TOPIC, WEALTH_PORTFOLIO_MANAGEMENT_RETRY_LIMIT, WEALTH_PORTFOLIO_MANAGEMENT_DEFAULT_POLICY
- standard_features: client_portfolio_management, wealth_portfolio_management_workflow, wealth_portfolio_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: wealth_portfolio_management_event_sourced_operational_history, wealth_portfolio_management_multi_tenant_policy_isolation, wealth_portfolio_management_schema_evolution_resilience, wealth_portfolio_management_autonomous_anomaly_detection, wealth_portfolio_management_semantic_document_instruction_understanding, wealth_portfolio_management_predictive_risk_scoring, wealth_portfolio_management_counterfactual_scenario_simulation, wealth_portfolio_management_cryptographic_audit_proofs, wealth_portfolio_management_continuous_control_testing, wealth_portfolio_management_carbon_and_sustainability_awareness, wealth_portfolio_management_cross_pbc_event_federation, wealth_portfolio_management_governed_ai_agent_execution
