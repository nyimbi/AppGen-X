# Hotel Revenue Management PBC

## Purpose

The `hotel_revenue_management` PBC is a packaged business capability for Room inventory, rates, channels, demand forecasts, overbooking, yield, and hotel revenue controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `hotel_revenue_management`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/hotel_revenue_management`.
- Runtime entrypoint: `hotel_revenue_management_runtime_capabilities()`.
- UI entrypoint: `hotel_revenue_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `hotel_revenue_management_room_type`: owns room type lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_rate_plan`: owns rate plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_channel_inventory`: owns channel inventory lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_demand_forecast`: owns demand forecast lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_overbooking_policy`: owns overbooking policy lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_yield_decision`: owns yield decision lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_revenue_snapshot`: owns revenue snapshot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_hotel_revenue_management_policy_rule`: owns hotel revenue management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_hotel_revenue_management_runtime_parameter`: owns hotel revenue management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_hotel_revenue_management_schema_extension`: owns hotel revenue management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_hotel_revenue_management_control_assertion`: owns hotel revenue management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hotel_revenue_management_hotel_revenue_management_governed_model`: owns hotel revenue management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `hotel_revenue_management_appgen_outbox_event`, `hotel_revenue_management_appgen_inbox_event`, and `hotel_revenue_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /room-types', 'POST /rate-plans', 'POST /channel-inventorys', 'POST /demand-forecasts', 'POST /overbooking-policys', 'GET /hotel-revenue-management-workbench').

## Executable Domain Operations

- `create_room_type`: validates policy, writes owned `hotel_revenue_management_room_type` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_rate_plan`: validates policy, writes owned `hotel_revenue_management_rate_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_channel_inventory`: validates policy, writes owned `hotel_revenue_management_channel_inventory` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_demand_forecast`: validates policy, writes owned `hotel_revenue_management_demand_forecast` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_overbooking_policy`: validates policy, writes owned `hotel_revenue_management_overbooking_policy` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_yield_decision`: validates policy, writes owned `hotel_revenue_management_yield_decision` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_revenue_snapshot`: validates policy, writes owned `hotel_revenue_management_revenue_snapshot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_hotel_revenue_management_policy_rule`: validates policy, writes owned `hotel_revenue_management_hotel_revenue_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_hotel_revenue_management_runtime_parameter`: validates policy, writes owned `hotel_revenue_management_hotel_revenue_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_hotel_revenue_management_schema_extension`: validates policy, writes owned `hotel_revenue_management_hotel_revenue_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_hotel_revenue_management_control_assertion`: validates policy, writes owned `hotel_revenue_management_hotel_revenue_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_hotel_revenue_management_governed_model`: validates policy, writes owned `hotel_revenue_management_hotel_revenue_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_13`: validates policy, writes owned `hotel_revenue_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_14`: validates policy, writes owned `hotel_revenue_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_15`: validates policy, writes owned `hotel_revenue_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_16`: validates policy, writes owned `hotel_revenue_management_room_type` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_17`: validates policy, writes owned `hotel_revenue_management_rate_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hotel_revenue_management_18`: validates policy, writes owned `hotel_revenue_management_channel_inventory` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Hotel Revenue Management domain records.
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

Rules are first-class artifacts: ('room_type_policy', 'rate_plan_policy', 'channel_inventory_policy', 'demand_forecast_policy', 'overbooking_policy_policy', 'yield_decision_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /room-types', 'POST /rate-plans', 'POST /channel-inventorys', 'POST /demand-forecasts', 'POST /overbooking-policys', 'GET /hotel-revenue-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `hotel_revenue_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('HotelRevenueManagementCreated', 'HotelRevenueManagementUpdated', 'HotelRevenueManagementApproved', 'HotelRevenueManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('room type board', 'rate plan board', 'channel inventory board', 'demand forecast board', 'overbooking policy board', 'yield decision board', 'revenue snapshot board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `hotel_revenue_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: room_type, rate_plan, channel_inventory, demand_forecast, overbooking_policy, yield_decision, revenue_snapshot, hotel_revenue_management_policy_rule, hotel_revenue_management_runtime_parameter, hotel_revenue_management_schema_extension, hotel_revenue_management_control_assertion, hotel_revenue_management_governed_model
- operations: create_room_type, record_rate_plan, review_channel_inventory, approve_demand_forecast, simulate_overbooking_policy, create_yield_decision, record_revenue_snapshot, review_hotel_revenue_management_policy_rule, approve_hotel_revenue_management_runtime_parameter, simulate_hotel_revenue_management_schema_extension, create_hotel_revenue_management_control_assertion, record_hotel_revenue_management_governed_model, operate_hotel_revenue_management_13, operate_hotel_revenue_management_14, operate_hotel_revenue_management_15, operate_hotel_revenue_management_16, operate_hotel_revenue_management_17, operate_hotel_revenue_management_18
- emits: HotelRevenueManagementCreated, HotelRevenueManagementUpdated, HotelRevenueManagementApproved, HotelRevenueManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: room_type_policy, rate_plan_policy, channel_inventory_policy, demand_forecast_policy, overbooking_policy_policy, yield_decision_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: HotelRevenueManagementWorkbench, HotelRevenueManagementDetail, HotelRevenueManagementAssistantPanel
- permissions: hotel_revenue_management.read, hotel_revenue_management.create, hotel_revenue_management.update, hotel_revenue_management.approve, hotel_revenue_management.admin
- configuration: HOTEL_REVENUE_MANAGEMENT_DATABASE_URL, HOTEL_REVENUE_MANAGEMENT_EVENT_TOPIC, HOTEL_REVENUE_MANAGEMENT_RETRY_LIMIT, HOTEL_REVENUE_MANAGEMENT_DEFAULT_POLICY
- standard_features: room_type_management, hotel_revenue_management_workflow, hotel_revenue_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: hotel_revenue_management_event_sourced_operational_history, hotel_revenue_management_multi_tenant_policy_isolation, hotel_revenue_management_schema_evolution_resilience, hotel_revenue_management_autonomous_anomaly_detection, hotel_revenue_management_semantic_document_instruction_understanding, hotel_revenue_management_predictive_risk_scoring, hotel_revenue_management_counterfactual_scenario_simulation, hotel_revenue_management_cryptographic_audit_proofs, hotel_revenue_management_continuous_control_testing, hotel_revenue_management_carbon_and_sustainability_awareness, hotel_revenue_management_cross_pbc_event_federation, hotel_revenue_management_governed_ai_agent_execution
