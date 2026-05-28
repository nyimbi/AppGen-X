# Capital Markets Trading Operations PBC

## Purpose

The `capital_markets_trading_ops` PBC is a packaged business capability for Trade orders, executions, allocations, confirmations, settlement, breaks, positions, and trading operations controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `capital_markets_trading_ops`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/capital_markets_trading_ops`.
- Runtime entrypoint: `capital_markets_trading_ops_runtime_capabilities()`.
- UI entrypoint: `capital_markets_trading_ops_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `capital_markets_trading_ops_trade_order`: owns trade order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_execution`: owns execution lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_allocation`: owns allocation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_confirmation`: owns confirmation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_settlement_instruction`: owns settlement instruction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_trade_break`: owns trade break lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_position_snapshot`: owns position snapshot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_capital_markets_trading_ops_policy_rule`: owns capital markets trading ops policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter`: owns capital markets trading ops runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_capital_markets_trading_ops_schema_extension`: owns capital markets trading ops schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_capital_markets_trading_ops_control_assertion`: owns capital markets trading ops control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_markets_trading_ops_capital_markets_trading_ops_governed_model`: owns capital markets trading ops governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `capital_markets_trading_ops_appgen_outbox_event`, `capital_markets_trading_ops_appgen_inbox_event`, and `capital_markets_trading_ops_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /trade-orders', 'POST /executions', 'POST /allocations', 'POST /confirmations', 'POST /settlement-instructions', 'GET /capital-markets-trading-ops-workbench').

## Executable Domain Operations

- `create_trade_order`: validates policy, writes owned `capital_markets_trading_ops_trade_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_execution`: validates policy, writes owned `capital_markets_trading_ops_execution` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_allocation`: validates policy, writes owned `capital_markets_trading_ops_allocation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_confirmation`: validates policy, writes owned `capital_markets_trading_ops_confirmation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_settlement_instruction`: validates policy, writes owned `capital_markets_trading_ops_settlement_instruction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_trade_break`: validates policy, writes owned `capital_markets_trading_ops_trade_break` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_position_snapshot`: validates policy, writes owned `capital_markets_trading_ops_position_snapshot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_capital_markets_trading_ops_policy_rule`: validates policy, writes owned `capital_markets_trading_ops_capital_markets_trading_ops_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_capital_markets_trading_ops_runtime_parameter`: validates policy, writes owned `capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_capital_markets_trading_ops_schema_extension`: validates policy, writes owned `capital_markets_trading_ops_capital_markets_trading_ops_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_capital_markets_trading_ops_control_assertion`: validates policy, writes owned `capital_markets_trading_ops_capital_markets_trading_ops_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_capital_markets_trading_ops_governed_model`: validates policy, writes owned `capital_markets_trading_ops_capital_markets_trading_ops_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_13`: validates policy, writes owned `capital_markets_trading_ops_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_14`: validates policy, writes owned `capital_markets_trading_ops_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_15`: validates policy, writes owned `capital_markets_trading_ops_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_16`: validates policy, writes owned `capital_markets_trading_ops_trade_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_17`: validates policy, writes owned `capital_markets_trading_ops_execution` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_markets_trading_ops_18`: validates policy, writes owned `capital_markets_trading_ops_allocation` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Capital Markets Trading Operations domain records.
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

Rules are first-class artifacts: ('trade_order_policy', 'execution_policy', 'allocation_policy', 'confirmation_policy', 'settlement_instruction_policy', 'trade_break_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /trade-orders', 'POST /executions', 'POST /allocations', 'POST /confirmations', 'POST /settlement-instructions', 'GET /capital-markets-trading-ops-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `capital_markets_trading_ops_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('CapitalMarketsTradingOpsCreated', 'CapitalMarketsTradingOpsUpdated', 'CapitalMarketsTradingOpsApproved', 'CapitalMarketsTradingOpsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('trade order board', 'execution board', 'allocation board', 'confirmation board', 'settlement instruction board', 'trade break board', 'position snapshot board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `capital_markets_trading_ops_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: trade_order, execution, allocation, confirmation, settlement_instruction, trade_break, position_snapshot, capital_markets_trading_ops_policy_rule, capital_markets_trading_ops_runtime_parameter, capital_markets_trading_ops_schema_extension, capital_markets_trading_ops_control_assertion, capital_markets_trading_ops_governed_model
- operations: create_trade_order, record_execution, review_allocation, approve_confirmation, simulate_settlement_instruction, create_trade_break, record_position_snapshot, review_capital_markets_trading_ops_policy_rule, approve_capital_markets_trading_ops_runtime_parameter, simulate_capital_markets_trading_ops_schema_extension, create_capital_markets_trading_ops_control_assertion, record_capital_markets_trading_ops_governed_model, operate_capital_markets_trading_ops_13, operate_capital_markets_trading_ops_14, operate_capital_markets_trading_ops_15, operate_capital_markets_trading_ops_16, operate_capital_markets_trading_ops_17, operate_capital_markets_trading_ops_18
- emits: CapitalMarketsTradingOpsCreated, CapitalMarketsTradingOpsUpdated, CapitalMarketsTradingOpsApproved, CapitalMarketsTradingOpsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: trade_order_policy, execution_policy, allocation_policy, confirmation_policy, settlement_instruction_policy, trade_break_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: CapitalMarketsTradingOpsWorkbench, CapitalMarketsTradingOpsDetail, CapitalMarketsTradingOpsAssistantPanel
- permissions: capital_markets_trading_ops.read, capital_markets_trading_ops.create, capital_markets_trading_ops.update, capital_markets_trading_ops.approve, capital_markets_trading_ops.admin
- configuration: CAPITAL_MARKETS_TRADING_OPS_DATABASE_URL, CAPITAL_MARKETS_TRADING_OPS_EVENT_TOPIC, CAPITAL_MARKETS_TRADING_OPS_RETRY_LIMIT, CAPITAL_MARKETS_TRADING_OPS_DEFAULT_POLICY
- standard_features: trade_order_management, capital_markets_trading_ops_workflow, capital_markets_trading_ops_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: capital_markets_trading_ops_event_sourced_operational_history, capital_markets_trading_ops_multi_tenant_policy_isolation, capital_markets_trading_ops_schema_evolution_resilience, capital_markets_trading_ops_autonomous_anomaly_detection, capital_markets_trading_ops_semantic_document_instruction_understanding, capital_markets_trading_ops_predictive_risk_scoring, capital_markets_trading_ops_counterfactual_scenario_simulation, capital_markets_trading_ops_cryptographic_audit_proofs, capital_markets_trading_ops_continuous_control_testing, capital_markets_trading_ops_carbon_and_sustainability_awareness, capital_markets_trading_ops_cross_pbc_event_federation, capital_markets_trading_ops_governed_ai_agent_execution
