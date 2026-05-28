# Energy Grid Operations PBC

## Purpose

The `energy_grid_operations` PBC is a packaged business capability for Grid assets, load forecasts, switching, dispatch, outage state, reliability events, and grid operating constraints. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `energy_grid_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/energy_grid_operations`.
- Runtime entrypoint: `energy_grid_operations_runtime_capabilities()`.
- UI entrypoint: `energy_grid_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `energy_grid_operations_grid_asset`: owns grid asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_load_forecast`: owns load forecast lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_switching_order`: owns switching order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_dispatch_instruction`: owns dispatch instruction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_outage_event`: owns outage event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_reliability_constraint`: owns reliability constraint lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_grid_topology`: owns grid topology lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_energy_grid_operations_policy_rule`: owns energy grid operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_energy_grid_operations_runtime_parameter`: owns energy grid operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_energy_grid_operations_schema_extension`: owns energy grid operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_energy_grid_operations_control_assertion`: owns energy grid operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `energy_grid_operations_energy_grid_operations_governed_model`: owns energy grid operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `energy_grid_operations_appgen_outbox_event`, `energy_grid_operations_appgen_inbox_event`, and `energy_grid_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /grid-assets', 'POST /load-forecasts', 'POST /switching-orders', 'POST /dispatch-instructions', 'POST /outage-events', 'GET /energy-grid-operations-workbench').

## Executable Domain Operations

- `create_grid_asset`: validates policy, writes owned `energy_grid_operations_grid_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_load_forecast`: validates policy, writes owned `energy_grid_operations_load_forecast` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_switching_order`: validates policy, writes owned `energy_grid_operations_switching_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_dispatch_instruction`: validates policy, writes owned `energy_grid_operations_dispatch_instruction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_outage_event`: validates policy, writes owned `energy_grid_operations_outage_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_reliability_constraint`: validates policy, writes owned `energy_grid_operations_reliability_constraint` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_grid_topology`: validates policy, writes owned `energy_grid_operations_grid_topology` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_energy_grid_operations_policy_rule`: validates policy, writes owned `energy_grid_operations_energy_grid_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_energy_grid_operations_runtime_parameter`: validates policy, writes owned `energy_grid_operations_energy_grid_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_energy_grid_operations_schema_extension`: validates policy, writes owned `energy_grid_operations_energy_grid_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_energy_grid_operations_control_assertion`: validates policy, writes owned `energy_grid_operations_energy_grid_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_energy_grid_operations_governed_model`: validates policy, writes owned `energy_grid_operations_energy_grid_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_13`: validates policy, writes owned `energy_grid_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_14`: validates policy, writes owned `energy_grid_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_15`: validates policy, writes owned `energy_grid_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_16`: validates policy, writes owned `energy_grid_operations_grid_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_17`: validates policy, writes owned `energy_grid_operations_load_forecast` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_energy_grid_operations_18`: validates policy, writes owned `energy_grid_operations_switching_order` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Energy Grid Operations domain records.
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

Rules are first-class artifacts: ('grid_asset_policy', 'load_forecast_policy', 'switching_order_policy', 'dispatch_instruction_policy', 'outage_event_policy', 'reliability_constraint_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /grid-assets', 'POST /load-forecasts', 'POST /switching-orders', 'POST /dispatch-instructions', 'POST /outage-events', 'GET /energy-grid-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `energy_grid_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('EnergyGridOperationsCreated', 'EnergyGridOperationsUpdated', 'EnergyGridOperationsApproved', 'EnergyGridOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('grid asset board', 'load forecast board', 'switching order board', 'dispatch instruction board', 'outage event board', 'reliability constraint board', 'grid topology board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `energy_grid_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: grid_asset, load_forecast, switching_order, dispatch_instruction, outage_event, reliability_constraint, grid_topology, energy_grid_operations_policy_rule, energy_grid_operations_runtime_parameter, energy_grid_operations_schema_extension, energy_grid_operations_control_assertion, energy_grid_operations_governed_model
- operations: create_grid_asset, record_load_forecast, review_switching_order, approve_dispatch_instruction, simulate_outage_event, create_reliability_constraint, record_grid_topology, review_energy_grid_operations_policy_rule, approve_energy_grid_operations_runtime_parameter, simulate_energy_grid_operations_schema_extension, create_energy_grid_operations_control_assertion, record_energy_grid_operations_governed_model, operate_energy_grid_operations_13, operate_energy_grid_operations_14, operate_energy_grid_operations_15, operate_energy_grid_operations_16, operate_energy_grid_operations_17, operate_energy_grid_operations_18
- emits: EnergyGridOperationsCreated, EnergyGridOperationsUpdated, EnergyGridOperationsApproved, EnergyGridOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: grid_asset_policy, load_forecast_policy, switching_order_policy, dispatch_instruction_policy, outage_event_policy, reliability_constraint_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: EnergyGridOperationsWorkbench, EnergyGridOperationsDetail, EnergyGridOperationsAssistantPanel
- permissions: energy_grid_operations.read, energy_grid_operations.create, energy_grid_operations.update, energy_grid_operations.approve, energy_grid_operations.admin
- configuration: ENERGY_GRID_OPERATIONS_DATABASE_URL, ENERGY_GRID_OPERATIONS_EVENT_TOPIC, ENERGY_GRID_OPERATIONS_RETRY_LIMIT, ENERGY_GRID_OPERATIONS_DEFAULT_POLICY
- standard_features: grid_asset_management, energy_grid_operations_workflow, energy_grid_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: energy_grid_operations_event_sourced_operational_history, energy_grid_operations_multi_tenant_policy_isolation, energy_grid_operations_schema_evolution_resilience, energy_grid_operations_autonomous_anomaly_detection, energy_grid_operations_semantic_document_instruction_understanding, energy_grid_operations_predictive_risk_scoring, energy_grid_operations_counterfactual_scenario_simulation, energy_grid_operations_cryptographic_audit_proofs, energy_grid_operations_continuous_control_testing, energy_grid_operations_carbon_and_sustainability_awareness, energy_grid_operations_cross_pbc_event_federation, energy_grid_operations_governed_ai_agent_execution
