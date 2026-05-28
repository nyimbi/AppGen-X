# Gaming and Casino Operations PBC

## Purpose

The `gaming_casino_operations` PBC is a packaged business capability for Players, tables, slots, compliance, responsible gaming, loyalty, payouts, and gaming floor operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `gaming_casino_operations`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/gaming_casino_operations`.
- Runtime entrypoint: `gaming_casino_operations_runtime_capabilities()`.
- UI entrypoint: `gaming_casino_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `gaming_casino_operations_player_profile`: owns player profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_table_game`: owns table game lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_slot_machine`: owns slot machine lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_wager_session`: owns wager session lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_payout`: owns payout lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_responsible_gaming_case`: owns responsible gaming case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_compliance`: owns gaming compliance lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_casino_operations_policy_rule`: owns gaming casino operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_casino_operations_runtime_parameter`: owns gaming casino operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_casino_operations_schema_extension`: owns gaming casino operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_casino_operations_control_assertion`: owns gaming casino operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `gaming_casino_operations_gaming_casino_operations_governed_model`: owns gaming casino operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `gaming_casino_operations_appgen_outbox_event`, `gaming_casino_operations_appgen_inbox_event`, and `gaming_casino_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /player-profiles', 'POST /table-games', 'POST /slot-machines', 'POST /wager-sessions', 'POST /payouts', 'GET /gaming-casino-operations-workbench').

## Executable Domain Operations

- `create_player_profile`: validates policy, writes owned `gaming_casino_operations_player_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_table_game`: validates policy, writes owned `gaming_casino_operations_table_game` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_slot_machine`: validates policy, writes owned `gaming_casino_operations_slot_machine` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_wager_session`: validates policy, writes owned `gaming_casino_operations_wager_session` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_payout`: validates policy, writes owned `gaming_casino_operations_payout` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_responsible_gaming_case`: validates policy, writes owned `gaming_casino_operations_responsible_gaming_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_gaming_compliance`: validates policy, writes owned `gaming_casino_operations_gaming_compliance` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_gaming_casino_operations_policy_rule`: validates policy, writes owned `gaming_casino_operations_gaming_casino_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_gaming_casino_operations_runtime_parameter`: validates policy, writes owned `gaming_casino_operations_gaming_casino_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_gaming_casino_operations_schema_extension`: validates policy, writes owned `gaming_casino_operations_gaming_casino_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_gaming_casino_operations_control_assertion`: validates policy, writes owned `gaming_casino_operations_gaming_casino_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_gaming_casino_operations_governed_model`: validates policy, writes owned `gaming_casino_operations_gaming_casino_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_13`: validates policy, writes owned `gaming_casino_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_14`: validates policy, writes owned `gaming_casino_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_15`: validates policy, writes owned `gaming_casino_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_16`: validates policy, writes owned `gaming_casino_operations_player_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_17`: validates policy, writes owned `gaming_casino_operations_table_game` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_gaming_casino_operations_18`: validates policy, writes owned `gaming_casino_operations_slot_machine` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Gaming and Casino Operations domain records.
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

Rules are first-class artifacts: ('player_profile_policy', 'table_game_policy', 'slot_machine_policy', 'wager_session_policy', 'payout_policy', 'responsible_gaming_case_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /player-profiles', 'POST /table-games', 'POST /slot-machines', 'POST /wager-sessions', 'POST /payouts', 'GET /gaming-casino-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `gaming_casino_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('GamingCasinoOperationsCreated', 'GamingCasinoOperationsUpdated', 'GamingCasinoOperationsApproved', 'GamingCasinoOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('player profile board', 'table game board', 'slot machine board', 'wager session board', 'payout board', 'responsible gaming case board', 'gaming compliance board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `gaming_casino_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: player_profile, table_game, slot_machine, wager_session, payout, responsible_gaming_case, gaming_compliance, gaming_casino_operations_policy_rule, gaming_casino_operations_runtime_parameter, gaming_casino_operations_schema_extension, gaming_casino_operations_control_assertion, gaming_casino_operations_governed_model
- operations: create_player_profile, record_table_game, review_slot_machine, approve_wager_session, simulate_payout, create_responsible_gaming_case, record_gaming_compliance, review_gaming_casino_operations_policy_rule, approve_gaming_casino_operations_runtime_parameter, simulate_gaming_casino_operations_schema_extension, create_gaming_casino_operations_control_assertion, record_gaming_casino_operations_governed_model, operate_gaming_casino_operations_13, operate_gaming_casino_operations_14, operate_gaming_casino_operations_15, operate_gaming_casino_operations_16, operate_gaming_casino_operations_17, operate_gaming_casino_operations_18
- emits: GamingCasinoOperationsCreated, GamingCasinoOperationsUpdated, GamingCasinoOperationsApproved, GamingCasinoOperationsExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: player_profile_policy, table_game_policy, slot_machine_policy, wager_session_policy, payout_policy, responsible_gaming_case_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: GamingCasinoOperationsWorkbench, GamingCasinoOperationsDetail, GamingCasinoOperationsAssistantPanel
- permissions: gaming_casino_operations.read, gaming_casino_operations.create, gaming_casino_operations.update, gaming_casino_operations.approve, gaming_casino_operations.admin
- configuration: GAMING_CASINO_OPERATIONS_DATABASE_URL, GAMING_CASINO_OPERATIONS_EVENT_TOPIC, GAMING_CASINO_OPERATIONS_RETRY_LIMIT, GAMING_CASINO_OPERATIONS_DEFAULT_POLICY
- standard_features: player_profile_management, gaming_casino_operations_workflow, gaming_casino_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: gaming_casino_operations_event_sourced_operational_history, gaming_casino_operations_multi_tenant_policy_isolation, gaming_casino_operations_schema_evolution_resilience, gaming_casino_operations_autonomous_anomaly_detection, gaming_casino_operations_semantic_document_instruction_understanding, gaming_casino_operations_predictive_risk_scoring, gaming_casino_operations_counterfactual_scenario_simulation, gaming_casino_operations_cryptographic_audit_proofs, gaming_casino_operations_continuous_control_testing, gaming_casino_operations_carbon_and_sustainability_awareness, gaming_casino_operations_cross_pbc_event_federation, gaming_casino_operations_governed_ai_agent_execution
