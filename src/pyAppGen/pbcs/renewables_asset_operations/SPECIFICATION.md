# Renewables Asset Operations PBC

## Purpose

The `renewables_asset_operations` PBC is a packaged business capability for Solar and wind assets, generation, curtailment, maintenance, PPAs, availability, and renewable performance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `renewables_asset_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/renewables_asset_operations`.
- Runtime entrypoint: `renewables_asset_operations_runtime_capabilities()`.
- UI entrypoint: `renewables_asset_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `renewables_asset_operations_renewable_asset`: owns renewable asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_generation_reading`: owns generation reading lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_curtailment_event`: owns curtailment event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_availability_record`: owns availability record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_ppa_obligation`: owns ppa obligation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_maintenance_work`: owns maintenance work lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_performance_ratio`: owns performance ratio lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_renewables_asset_operations_policy_rule`: owns renewables asset operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_renewables_asset_operations_runtime_parameter`: owns renewables asset operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_renewables_asset_operations_schema_extension`: owns renewables asset operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_renewables_asset_operations_control_assertion`: owns renewables asset operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `renewables_asset_operations_renewables_asset_operations_governed_model`: owns renewables asset operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `renewables_asset_operations_appgen_outbox_event`, `renewables_asset_operations_appgen_inbox_event`, and `renewables_asset_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /renewable-assets', 'POST /generation-readings', 'POST /curtailment-events', 'POST /availability-records', 'POST /ppa-obligations', 'GET /renewables-asset-operations-workbench').

## Executable Domain Operations

- `create_renewable_asset`: validates policy, writes owned `renewables_asset_operations_renewable_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_generation_reading`: validates policy, writes owned `renewables_asset_operations_generation_reading` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_curtailment_event`: validates policy, writes owned `renewables_asset_operations_curtailment_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_availability_record`: validates policy, writes owned `renewables_asset_operations_availability_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_ppa_obligation`: validates policy, writes owned `renewables_asset_operations_ppa_obligation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_maintenance_work`: validates policy, writes owned `renewables_asset_operations_maintenance_work` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_performance_ratio`: validates policy, writes owned `renewables_asset_operations_performance_ratio` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_renewables_asset_operations_policy_rule`: validates policy, writes owned `renewables_asset_operations_renewables_asset_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_renewables_asset_operations_runtime_parameter`: validates policy, writes owned `renewables_asset_operations_renewables_asset_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_renewables_asset_operations_schema_extension`: validates policy, writes owned `renewables_asset_operations_renewables_asset_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_renewables_asset_operations_control_assertion`: validates policy, writes owned `renewables_asset_operations_renewables_asset_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_renewables_asset_operations_governed_model`: validates policy, writes owned `renewables_asset_operations_renewables_asset_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_13`: validates policy, writes owned `renewables_asset_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_14`: validates policy, writes owned `renewables_asset_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_15`: validates policy, writes owned `renewables_asset_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_16`: validates policy, writes owned `renewables_asset_operations_renewable_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_17`: validates policy, writes owned `renewables_asset_operations_generation_reading` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_renewables_asset_operations_18`: validates policy, writes owned `renewables_asset_operations_curtailment_event` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Renewables Asset Operations domain records.
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

Rules are first-class artifacts: ('renewable_asset_policy', 'generation_reading_policy', 'curtailment_event_policy', 'availability_record_policy', 'ppa_obligation_policy', 'maintenance_work_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /renewable-assets', 'POST /generation-readings', 'POST /curtailment-events', 'POST /availability-records', 'POST /ppa-obligations', 'GET /renewables-asset-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `renewables_asset_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('RenewablesAssetOperationsCreated', 'RenewablesAssetOperationsUpdated', 'RenewablesAssetOperationsApproved', 'RenewablesAssetOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('renewable asset board', 'generation reading board', 'curtailment event board', 'availability record board', 'ppa obligation board', 'maintenance work board', 'performance ratio board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `renewables_asset_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: renewable_asset, generation_reading, curtailment_event, availability_record, ppa_obligation, maintenance_work, performance_ratio, renewables_asset_operations_policy_rule, renewables_asset_operations_runtime_parameter, renewables_asset_operations_schema_extension, renewables_asset_operations_control_assertion, renewables_asset_operations_governed_model
- operations: create_renewable_asset, record_generation_reading, review_curtailment_event, approve_availability_record, simulate_ppa_obligation, create_maintenance_work, record_performance_ratio, review_renewables_asset_operations_policy_rule, approve_renewables_asset_operations_runtime_parameter, simulate_renewables_asset_operations_schema_extension, create_renewables_asset_operations_control_assertion, record_renewables_asset_operations_governed_model, operate_renewables_asset_operations_13, operate_renewables_asset_operations_14, operate_renewables_asset_operations_15, operate_renewables_asset_operations_16, operate_renewables_asset_operations_17, operate_renewables_asset_operations_18
- emits: RenewablesAssetOperationsCreated, RenewablesAssetOperationsUpdated, RenewablesAssetOperationsApproved, RenewablesAssetOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: renewable_asset_policy, generation_reading_policy, curtailment_event_policy, availability_record_policy, ppa_obligation_policy, maintenance_work_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: RenewablesAssetOperationsWorkbench, RenewablesAssetOperationsDetail, RenewablesAssetOperationsAssistantPanel
- permissions: renewables_asset_operations.read, renewables_asset_operations.create, renewables_asset_operations.update, renewables_asset_operations.approve, renewables_asset_operations.admin
- configuration: RENEWABLES_ASSET_OPERATIONS_DATABASE_URL, RENEWABLES_ASSET_OPERATIONS_EVENT_TOPIC, RENEWABLES_ASSET_OPERATIONS_RETRY_LIMIT, RENEWABLES_ASSET_OPERATIONS_DEFAULT_POLICY
- standard_features: renewable_asset_management, renewables_asset_operations_workflow, renewables_asset_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: renewables_asset_operations_event_sourced_operational_history, renewables_asset_operations_multi_tenant_policy_isolation, renewables_asset_operations_schema_evolution_resilience, renewables_asset_operations_autonomous_anomaly_detection, renewables_asset_operations_semantic_document_instruction_understanding, renewables_asset_operations_predictive_risk_scoring, renewables_asset_operations_counterfactual_scenario_simulation, renewables_asset_operations_cryptographic_audit_proofs, renewables_asset_operations_continuous_control_testing, renewables_asset_operations_carbon_and_sustainability_awareness, renewables_asset_operations_cross_pbc_event_federation, renewables_asset_operations_governed_ai_agent_execution
