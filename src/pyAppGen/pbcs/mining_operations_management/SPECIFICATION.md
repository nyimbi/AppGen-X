# Mining Operations Management PBC

## Purpose

The `mining_operations_management` PBC is a packaged business capability for Mine plans, extraction, haulage, fleet, ore quality, safety, stockpiles, and rehabilitation operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `mining_operations_management`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/mining_operations_management`.
- Runtime entrypoint: `mining_operations_management_runtime_capabilities()`.
- UI entrypoint: `mining_operations_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `mining_operations_management_mine_plan`: owns mine plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_pit_block`: owns pit block lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_extraction_shift`: owns extraction shift lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_haulage_cycle`: owns haulage cycle lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_fleet_asset`: owns fleet asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_ore_quality`: owns ore quality lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_stockpile`: owns stockpile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_mining_operations_management_policy_rule`: owns mining operations management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_mining_operations_management_runtime_parameter`: owns mining operations management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_mining_operations_management_schema_extension`: owns mining operations management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_mining_operations_management_control_assertion`: owns mining operations management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_operations_management_mining_operations_management_governed_model`: owns mining operations management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `mining_operations_management_appgen_outbox_event`, `mining_operations_management_appgen_inbox_event`, and `mining_operations_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /mine-plans', 'POST /pit-blocks', 'POST /extraction-shifts', 'POST /haulage-cycles', 'POST /fleet-assets', 'GET /mining-operations-management-workbench').

## Executable Domain Operations

- `create_mine_plan`: validates policy, writes owned `mining_operations_management_mine_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_pit_block`: validates policy, writes owned `mining_operations_management_pit_block` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_extraction_shift`: validates policy, writes owned `mining_operations_management_extraction_shift` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_haulage_cycle`: validates policy, writes owned `mining_operations_management_haulage_cycle` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_fleet_asset`: validates policy, writes owned `mining_operations_management_fleet_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_ore_quality`: validates policy, writes owned `mining_operations_management_ore_quality` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_stockpile`: validates policy, writes owned `mining_operations_management_stockpile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_mining_operations_management_policy_rule`: validates policy, writes owned `mining_operations_management_mining_operations_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_mining_operations_management_runtime_parameter`: validates policy, writes owned `mining_operations_management_mining_operations_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_mining_operations_management_schema_extension`: validates policy, writes owned `mining_operations_management_mining_operations_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_mining_operations_management_control_assertion`: validates policy, writes owned `mining_operations_management_mining_operations_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_mining_operations_management_governed_model`: validates policy, writes owned `mining_operations_management_mining_operations_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_13`: validates policy, writes owned `mining_operations_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_14`: validates policy, writes owned `mining_operations_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_15`: validates policy, writes owned `mining_operations_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_16`: validates policy, writes owned `mining_operations_management_mine_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_17`: validates policy, writes owned `mining_operations_management_pit_block` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_operations_management_18`: validates policy, writes owned `mining_operations_management_extraction_shift` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Mining Operations Management domain records.
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

Rules are first-class artifacts: ('mine_plan_policy', 'pit_block_policy', 'extraction_shift_policy', 'haulage_cycle_policy', 'fleet_asset_policy', 'ore_quality_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /mine-plans', 'POST /pit-blocks', 'POST /extraction-shifts', 'POST /haulage-cycles', 'POST /fleet-assets', 'GET /mining-operations-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `mining_operations_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MiningOperationsManagementCreated', 'MiningOperationsManagementUpdated', 'MiningOperationsManagementApproved', 'MiningOperationsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('mine plan board', 'pit block board', 'extraction shift board', 'haulage cycle board', 'fleet asset board', 'ore quality board', 'stockpile board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `mining_operations_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: mine_plan, pit_block, extraction_shift, haulage_cycle, fleet_asset, ore_quality, stockpile, mining_operations_management_policy_rule, mining_operations_management_runtime_parameter, mining_operations_management_schema_extension, mining_operations_management_control_assertion, mining_operations_management_governed_model
- operations: create_mine_plan, record_pit_block, review_extraction_shift, approve_haulage_cycle, simulate_fleet_asset, create_ore_quality, record_stockpile, review_mining_operations_management_policy_rule, approve_mining_operations_management_runtime_parameter, simulate_mining_operations_management_schema_extension, create_mining_operations_management_control_assertion, record_mining_operations_management_governed_model, operate_mining_operations_management_13, operate_mining_operations_management_14, operate_mining_operations_management_15, operate_mining_operations_management_16, operate_mining_operations_management_17, operate_mining_operations_management_18
- emits: MiningOperationsManagementCreated, MiningOperationsManagementUpdated, MiningOperationsManagementApproved, MiningOperationsManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: mine_plan_policy, pit_block_policy, extraction_shift_policy, haulage_cycle_policy, fleet_asset_policy, ore_quality_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MiningOperationsManagementWorkbench, MiningOperationsManagementDetail, MiningOperationsManagementAssistantPanel
- permissions: mining_operations_management.read, mining_operations_management.create, mining_operations_management.update, mining_operations_management.approve, mining_operations_management.admin
- configuration: MINING_OPERATIONS_MANAGEMENT_DATABASE_URL, MINING_OPERATIONS_MANAGEMENT_EVENT_TOPIC, MINING_OPERATIONS_MANAGEMENT_RETRY_LIMIT, MINING_OPERATIONS_MANAGEMENT_DEFAULT_POLICY
- standard_features: mine_plan_management, mining_operations_management_workflow, mining_operations_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: mining_operations_management_event_sourced_operational_history, mining_operations_management_multi_tenant_policy_isolation, mining_operations_management_schema_evolution_resilience, mining_operations_management_autonomous_anomaly_detection, mining_operations_management_semantic_document_instruction_understanding, mining_operations_management_predictive_risk_scoring, mining_operations_management_counterfactual_scenario_simulation, mining_operations_management_cryptographic_audit_proofs, mining_operations_management_continuous_control_testing, mining_operations_management_carbon_and_sustainability_awareness, mining_operations_management_cross_pbc_event_federation, mining_operations_management_governed_ai_agent_execution
