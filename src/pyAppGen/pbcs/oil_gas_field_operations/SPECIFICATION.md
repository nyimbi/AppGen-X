# Oil and Gas Field Operations PBC

## Purpose

The `oil_gas_field_operations` PBC is a packaged business capability for Wells, production, maintenance, field logistics, HSE, reserves, lifting costs, and operating events. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `oil_gas_field_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/oil_gas_field_operations`.
- Runtime entrypoint: `oil_gas_field_operations_runtime_capabilities()`.
- UI entrypoint: `oil_gas_field_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `oil_gas_field_operations_well`: owns well lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_production_reading`: owns production reading lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_field_ticket`: owns field ticket lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_workover_plan`: owns workover plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_hse_event`: owns hse event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_reserve_estimate`: owns reserve estimate lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_lifting_cost`: owns lifting cost lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_oil_gas_field_operations_policy_rule`: owns oil gas field operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_oil_gas_field_operations_runtime_parameter`: owns oil gas field operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_oil_gas_field_operations_schema_extension`: owns oil gas field operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_oil_gas_field_operations_control_assertion`: owns oil gas field operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `oil_gas_field_operations_oil_gas_field_operations_governed_model`: owns oil gas field operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `oil_gas_field_operations_appgen_outbox_event`, `oil_gas_field_operations_appgen_inbox_event`, and `oil_gas_field_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /wells', 'POST /production-readings', 'POST /field-tickets', 'POST /workover-plans', 'POST /hse-events', 'GET /oil-gas-field-operations-workbench').

## Executable Domain Operations

- `create_well`: validates policy, writes owned `oil_gas_field_operations_well` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_production_reading`: validates policy, writes owned `oil_gas_field_operations_production_reading` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_field_ticket`: validates policy, writes owned `oil_gas_field_operations_field_ticket` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_workover_plan`: validates policy, writes owned `oil_gas_field_operations_workover_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_hse_event`: validates policy, writes owned `oil_gas_field_operations_hse_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_reserve_estimate`: validates policy, writes owned `oil_gas_field_operations_reserve_estimate` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_lifting_cost`: validates policy, writes owned `oil_gas_field_operations_lifting_cost` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_oil_gas_field_operations_policy_rule`: validates policy, writes owned `oil_gas_field_operations_oil_gas_field_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_oil_gas_field_operations_runtime_parameter`: validates policy, writes owned `oil_gas_field_operations_oil_gas_field_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_oil_gas_field_operations_schema_extension`: validates policy, writes owned `oil_gas_field_operations_oil_gas_field_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_oil_gas_field_operations_control_assertion`: validates policy, writes owned `oil_gas_field_operations_oil_gas_field_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_oil_gas_field_operations_governed_model`: validates policy, writes owned `oil_gas_field_operations_oil_gas_field_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_13`: validates policy, writes owned `oil_gas_field_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_14`: validates policy, writes owned `oil_gas_field_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_15`: validates policy, writes owned `oil_gas_field_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_16`: validates policy, writes owned `oil_gas_field_operations_well` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_17`: validates policy, writes owned `oil_gas_field_operations_production_reading` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_oil_gas_field_operations_18`: validates policy, writes owned `oil_gas_field_operations_field_ticket` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Oil and Gas Field Operations domain records.
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

Rules are first-class artifacts: ('well_policy', 'production_reading_policy', 'field_ticket_policy', 'workover_plan_policy', 'hse_event_policy', 'reserve_estimate_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /wells', 'POST /production-readings', 'POST /field-tickets', 'POST /workover-plans', 'POST /hse-events', 'GET /oil-gas-field-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `oil_gas_field_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('OilGasFieldOperationsCreated', 'OilGasFieldOperationsUpdated', 'OilGasFieldOperationsApproved', 'OilGasFieldOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('well board', 'production reading board', 'field ticket board', 'workover plan board', 'hse event board', 'reserve estimate board', 'lifting cost board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `oil_gas_field_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: well, production_reading, field_ticket, workover_plan, hse_event, reserve_estimate, lifting_cost, oil_gas_field_operations_policy_rule, oil_gas_field_operations_runtime_parameter, oil_gas_field_operations_schema_extension, oil_gas_field_operations_control_assertion, oil_gas_field_operations_governed_model
- operations: create_well, record_production_reading, review_field_ticket, approve_workover_plan, simulate_hse_event, create_reserve_estimate, record_lifting_cost, review_oil_gas_field_operations_policy_rule, approve_oil_gas_field_operations_runtime_parameter, simulate_oil_gas_field_operations_schema_extension, create_oil_gas_field_operations_control_assertion, record_oil_gas_field_operations_governed_model, operate_oil_gas_field_operations_13, operate_oil_gas_field_operations_14, operate_oil_gas_field_operations_15, operate_oil_gas_field_operations_16, operate_oil_gas_field_operations_17, operate_oil_gas_field_operations_18
- emits: OilGasFieldOperationsCreated, OilGasFieldOperationsUpdated, OilGasFieldOperationsApproved, OilGasFieldOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: well_policy, production_reading_policy, field_ticket_policy, workover_plan_policy, hse_event_policy, reserve_estimate_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: OilGasFieldOperationsWorkbench, OilGasFieldOperationsDetail, OilGasFieldOperationsAssistantPanel
- permissions: oil_gas_field_operations.read, oil_gas_field_operations.create, oil_gas_field_operations.update, oil_gas_field_operations.approve, oil_gas_field_operations.admin
- configuration: OIL_GAS_FIELD_OPERATIONS_DATABASE_URL, OIL_GAS_FIELD_OPERATIONS_EVENT_TOPIC, OIL_GAS_FIELD_OPERATIONS_RETRY_LIMIT, OIL_GAS_FIELD_OPERATIONS_DEFAULT_POLICY
- standard_features: well_management, oil_gas_field_operations_workflow, oil_gas_field_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: oil_gas_field_operations_event_sourced_operational_history, oil_gas_field_operations_multi_tenant_policy_isolation, oil_gas_field_operations_schema_evolution_resilience, oil_gas_field_operations_autonomous_anomaly_detection, oil_gas_field_operations_semantic_document_instruction_understanding, oil_gas_field_operations_predictive_risk_scoring, oil_gas_field_operations_counterfactual_scenario_simulation, oil_gas_field_operations_cryptographic_audit_proofs, oil_gas_field_operations_continuous_control_testing, oil_gas_field_operations_carbon_and_sustainability_awareness, oil_gas_field_operations_cross_pbc_event_federation, oil_gas_field_operations_governed_ai_agent_execution
