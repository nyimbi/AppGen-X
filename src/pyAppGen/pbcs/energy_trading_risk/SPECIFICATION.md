# Energy Trading and Risk PBC

## Purpose

The `energy_trading_risk` PBC is a packaged business capability for Energy contracts, positions, nominations, settlement, mark-to-market, exposure, and risk limits. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `energy_trading_risk`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/energy_trading_risk`.
- Runtime entrypoint: `energy_trading_risk_runtime_capabilities()`.
- UI entrypoint: `energy_trading_risk_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `energy_trading_risk_energy_contract`: owns energy contract lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_trade_position`: owns trade position lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_nomination`: owns nomination lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_schedule`: owns schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_settlement`: owns settlement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_exposure_limit`: owns exposure limit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_market_price_curve`: owns market price curve lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_energy_trading_risk_policy_rule`: owns energy trading risk policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_energy_trading_risk_runtime_parameter`: owns energy trading risk runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_energy_trading_risk_schema_extension`: owns energy trading risk schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_energy_trading_risk_control_assertion`: owns energy trading risk control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_trading_risk_energy_trading_risk_governed_model`: owns energy trading risk governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `energy_trading_risk_appgen_outbox_event`, `energy_trading_risk_appgen_inbox_event`, and `energy_trading_risk_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /energy-contracts', 'POST /trade-positions', 'POST /nominations', 'POST /schedules', 'POST /settlements', 'GET /energy-trading-risk-workbench').

## Executable Domain Operations

- `create_energy_contract`: validates policy, writes owned `energy_trading_risk_energy_contract` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_trade_position`: validates policy, writes owned `energy_trading_risk_trade_position` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_nomination`: validates policy, writes owned `energy_trading_risk_nomination` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_schedule`: validates policy, writes owned `energy_trading_risk_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_settlement`: validates policy, writes owned `energy_trading_risk_settlement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_exposure_limit`: validates policy, writes owned `energy_trading_risk_exposure_limit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_market_price_curve`: validates policy, writes owned `energy_trading_risk_market_price_curve` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_energy_trading_risk_policy_rule`: validates policy, writes owned `energy_trading_risk_energy_trading_risk_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_energy_trading_risk_runtime_parameter`: validates policy, writes owned `energy_trading_risk_energy_trading_risk_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_energy_trading_risk_schema_extension`: validates policy, writes owned `energy_trading_risk_energy_trading_risk_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_energy_trading_risk_control_assertion`: validates policy, writes owned `energy_trading_risk_energy_trading_risk_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_energy_trading_risk_governed_model`: validates policy, writes owned `energy_trading_risk_energy_trading_risk_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_13`: validates policy, writes owned `energy_trading_risk_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_14`: validates policy, writes owned `energy_trading_risk_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_15`: validates policy, writes owned `energy_trading_risk_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_16`: validates policy, writes owned `energy_trading_risk_energy_contract` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_17`: validates policy, writes owned `energy_trading_risk_trade_position` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_trading_risk_18`: validates policy, writes owned `energy_trading_risk_nomination` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Energy Trading and Risk domain records.
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

Rules are first-class artifacts: ('energy_contract_policy', 'trade_position_policy', 'nomination_policy', 'schedule_policy', 'settlement_policy', 'exposure_limit_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /energy-contracts', 'POST /trade-positions', 'POST /nominations', 'POST /schedules', 'POST /settlements', 'GET /energy-trading-risk-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `energy_trading_risk_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('EnergyTradingRiskCreated', 'EnergyTradingRiskUpdated', 'EnergyTradingRiskApproved', 'EnergyTradingRiskExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('energy contract board', 'trade position board', 'nomination board', 'schedule board', 'settlement board', 'exposure limit board', 'market price curve board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `energy_trading_risk_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: energy_contract, trade_position, nomination, schedule, settlement, exposure_limit, market_price_curve, energy_trading_risk_policy_rule, energy_trading_risk_runtime_parameter, energy_trading_risk_schema_extension, energy_trading_risk_control_assertion, energy_trading_risk_governed_model
- operations: create_energy_contract, record_trade_position, review_nomination, approve_schedule, simulate_settlement, create_exposure_limit, record_market_price_curve, review_energy_trading_risk_policy_rule, approve_energy_trading_risk_runtime_parameter, simulate_energy_trading_risk_schema_extension, create_energy_trading_risk_control_assertion, record_energy_trading_risk_governed_model, operate_energy_trading_risk_13, operate_energy_trading_risk_14, operate_energy_trading_risk_15, operate_energy_trading_risk_16, operate_energy_trading_risk_17, operate_energy_trading_risk_18
- emits: EnergyTradingRiskCreated, EnergyTradingRiskUpdated, EnergyTradingRiskApproved, EnergyTradingRiskExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: energy_contract_policy, trade_position_policy, nomination_policy, schedule_policy, settlement_policy, exposure_limit_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: EnergyTradingRiskWorkbench, EnergyTradingRiskDetail, EnergyTradingRiskAssistantPanel
- permissions: energy_trading_risk.read, energy_trading_risk.create, energy_trading_risk.update, energy_trading_risk.approve, energy_trading_risk.admin
- configuration: ENERGY_TRADING_RISK_DATABASE_URL, ENERGY_TRADING_RISK_EVENT_TOPIC, ENERGY_TRADING_RISK_RETRY_LIMIT, ENERGY_TRADING_RISK_DEFAULT_POLICY
- standard_features: energy_contract_management, energy_trading_risk_workflow, energy_trading_risk_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: energy_trading_risk_event_sourced_operational_history, energy_trading_risk_multi_tenant_policy_isolation, energy_trading_risk_schema_evolution_resilience, energy_trading_risk_autonomous_anomaly_detection, energy_trading_risk_semantic_document_instruction_understanding, energy_trading_risk_predictive_risk_scoring, energy_trading_risk_counterfactual_scenario_simulation, energy_trading_risk_cryptographic_audit_proofs, energy_trading_risk_continuous_control_testing, energy_trading_risk_carbon_and_sustainability_awareness, energy_trading_risk_cross_pbc_event_federation, energy_trading_risk_governed_ai_agent_execution
