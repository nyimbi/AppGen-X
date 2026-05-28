# Smart City Mobility Operations PBC

## Purpose

The `smart_city_mobility_operations` PBC is a packaged business capability for Transit, parking, traffic signals, incidents, curb management, multimodal services, and city mobility analytics. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `smart_city_mobility_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/smart_city_mobility_operations`.
- Runtime entrypoint: `smart_city_mobility_operations_runtime_capabilities()`.
- UI entrypoint: `smart_city_mobility_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `smart_city_mobility_operations_transit_service`: owns transit service lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_parking_asset`: owns parking asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_signal_plan`: owns signal plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_traffic_incident`: owns traffic incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_curb_allocation`: owns curb allocation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_mobility_sensor`: owns mobility sensor lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_service_disruption`: owns service disruption lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_smart_city_mobility_operations_policy_rule`: owns smart city mobility operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_smart_city_mobility_operations_runtime_parameter`: owns smart city mobility operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_smart_city_mobility_operations_schema_extension`: owns smart city mobility operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_smart_city_mobility_operations_control_assertion`: owns smart city mobility operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `smart_city_mobility_operations_smart_city_mobility_operations_governed_model`: owns smart city mobility operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `smart_city_mobility_operations_appgen_outbox_event`, `smart_city_mobility_operations_appgen_inbox_event`, and `smart_city_mobility_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /transit-services', 'POST /parking-assets', 'POST /signal-plans', 'POST /traffic-incidents', 'POST /curb-allocations', 'GET /smart-city-mobility-operations-workbench').

## Executable Domain Operations

- `create_transit_service`: validates policy, writes owned `smart_city_mobility_operations_transit_service` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_parking_asset`: validates policy, writes owned `smart_city_mobility_operations_parking_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_signal_plan`: validates policy, writes owned `smart_city_mobility_operations_signal_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_traffic_incident`: validates policy, writes owned `smart_city_mobility_operations_traffic_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_curb_allocation`: validates policy, writes owned `smart_city_mobility_operations_curb_allocation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_mobility_sensor`: validates policy, writes owned `smart_city_mobility_operations_mobility_sensor` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_service_disruption`: validates policy, writes owned `smart_city_mobility_operations_service_disruption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_smart_city_mobility_operations_policy_rule`: validates policy, writes owned `smart_city_mobility_operations_smart_city_mobility_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_smart_city_mobility_operations_runtime_parameter`: validates policy, writes owned `smart_city_mobility_operations_smart_city_mobility_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_smart_city_mobility_operations_schema_extension`: validates policy, writes owned `smart_city_mobility_operations_smart_city_mobility_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_smart_city_mobility_operations_control_assertion`: validates policy, writes owned `smart_city_mobility_operations_smart_city_mobility_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_smart_city_mobility_operations_governed_model`: validates policy, writes owned `smart_city_mobility_operations_smart_city_mobility_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_13`: validates policy, writes owned `smart_city_mobility_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_14`: validates policy, writes owned `smart_city_mobility_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_15`: validates policy, writes owned `smart_city_mobility_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_16`: validates policy, writes owned `smart_city_mobility_operations_transit_service` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_17`: validates policy, writes owned `smart_city_mobility_operations_parking_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_smart_city_mobility_operations_18`: validates policy, writes owned `smart_city_mobility_operations_signal_plan` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Smart City Mobility Operations domain records.
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

Rules are first-class artifacts: ('transit_service_policy', 'parking_asset_policy', 'signal_plan_policy', 'traffic_incident_policy', 'curb_allocation_policy', 'mobility_sensor_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /transit-services', 'POST /parking-assets', 'POST /signal-plans', 'POST /traffic-incidents', 'POST /curb-allocations', 'GET /smart-city-mobility-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `smart_city_mobility_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('SmartCityMobilityOperationsCreated', 'SmartCityMobilityOperationsUpdated', 'SmartCityMobilityOperationsApproved', 'SmartCityMobilityOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('transit service board', 'parking asset board', 'signal plan board', 'traffic incident board', 'curb allocation board', 'mobility sensor board', 'service disruption board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `smart_city_mobility_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: transit_service, parking_asset, signal_plan, traffic_incident, curb_allocation, mobility_sensor, service_disruption, smart_city_mobility_operations_policy_rule, smart_city_mobility_operations_runtime_parameter, smart_city_mobility_operations_schema_extension, smart_city_mobility_operations_control_assertion, smart_city_mobility_operations_governed_model
- operations: create_transit_service, record_parking_asset, review_signal_plan, approve_traffic_incident, simulate_curb_allocation, create_mobility_sensor, record_service_disruption, review_smart_city_mobility_operations_policy_rule, approve_smart_city_mobility_operations_runtime_parameter, simulate_smart_city_mobility_operations_schema_extension, create_smart_city_mobility_operations_control_assertion, record_smart_city_mobility_operations_governed_model, operate_smart_city_mobility_operations_13, operate_smart_city_mobility_operations_14, operate_smart_city_mobility_operations_15, operate_smart_city_mobility_operations_16, operate_smart_city_mobility_operations_17, operate_smart_city_mobility_operations_18
- emits: SmartCityMobilityOperationsCreated, SmartCityMobilityOperationsUpdated, SmartCityMobilityOperationsApproved, SmartCityMobilityOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: transit_service_policy, parking_asset_policy, signal_plan_policy, traffic_incident_policy, curb_allocation_policy, mobility_sensor_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: SmartCityMobilityOperationsWorkbench, SmartCityMobilityOperationsDetail, SmartCityMobilityOperationsAssistantPanel
- permissions: smart_city_mobility_operations.read, smart_city_mobility_operations.create, smart_city_mobility_operations.update, smart_city_mobility_operations.approve, smart_city_mobility_operations.admin
- configuration: SMART_CITY_MOBILITY_OPERATIONS_DATABASE_URL, SMART_CITY_MOBILITY_OPERATIONS_EVENT_TOPIC, SMART_CITY_MOBILITY_OPERATIONS_RETRY_LIMIT, SMART_CITY_MOBILITY_OPERATIONS_DEFAULT_POLICY
- standard_features: transit_service_management, smart_city_mobility_operations_workflow, smart_city_mobility_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: smart_city_mobility_operations_event_sourced_operational_history, smart_city_mobility_operations_multi_tenant_policy_isolation, smart_city_mobility_operations_schema_evolution_resilience, smart_city_mobility_operations_autonomous_anomaly_detection, smart_city_mobility_operations_semantic_document_instruction_understanding, smart_city_mobility_operations_predictive_risk_scoring, smart_city_mobility_operations_counterfactual_scenario_simulation, smart_city_mobility_operations_cryptographic_audit_proofs, smart_city_mobility_operations_continuous_control_testing, smart_city_mobility_operations_carbon_and_sustainability_awareness, smart_city_mobility_operations_cross_pbc_event_federation, smart_city_mobility_operations_governed_ai_agent_execution
