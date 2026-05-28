# Hospitality Property Operations PBC

## Purpose

The `hospitality_property_operations` PBC is a packaged business capability for Rooms, reservations, housekeeping, guest service, occupancy, revenue controls, and property operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `hospitality_property_operations`.
- Mesh: `cx`.
- Package directory: `src/pyAppGen/pbcs/hospitality_property_operations`.
- Runtime entrypoint: `hospitality_property_operations_runtime_capabilities()`.
- UI entrypoint: `hospitality_property_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `hospitality_property_operations_room_inventory`: owns room inventory lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_reservation`: owns reservation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_guest_stay`: owns guest stay lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_housekeeping_task`: owns housekeeping task lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_guest_request`: owns guest request lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_occupancy_snapshot`: owns occupancy snapshot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_rate_plan`: owns rate plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_hospitality_property_operations_policy_rule`: owns hospitality property operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_hospitality_property_operations_runtime_parameter`: owns hospitality property operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_hospitality_property_operations_schema_extension`: owns hospitality property operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_hospitality_property_operations_control_assertion`: owns hospitality property operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `hospitality_property_operations_hospitality_property_operations_governed_model`: owns hospitality property operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `hospitality_property_operations_appgen_outbox_event`, `hospitality_property_operations_appgen_inbox_event`, and `hospitality_property_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /room-inventorys', 'POST /reservations', 'POST /guest-stays', 'POST /housekeeping-tasks', 'POST /guest-requests', 'GET /hospitality-property-operations-workbench').

## Executable Domain Operations

- `create_room_inventory`: validates policy, writes owned `hospitality_property_operations_room_inventory` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_reservation`: validates policy, writes owned `hospitality_property_operations_reservation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_guest_stay`: validates policy, writes owned `hospitality_property_operations_guest_stay` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_housekeeping_task`: validates policy, writes owned `hospitality_property_operations_housekeeping_task` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_guest_request`: validates policy, writes owned `hospitality_property_operations_guest_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_occupancy_snapshot`: validates policy, writes owned `hospitality_property_operations_occupancy_snapshot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_rate_plan`: validates policy, writes owned `hospitality_property_operations_rate_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_hospitality_property_operations_policy_rule`: validates policy, writes owned `hospitality_property_operations_hospitality_property_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_hospitality_property_operations_runtime_parameter`: validates policy, writes owned `hospitality_property_operations_hospitality_property_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_hospitality_property_operations_schema_extension`: validates policy, writes owned `hospitality_property_operations_hospitality_property_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_hospitality_property_operations_control_assertion`: validates policy, writes owned `hospitality_property_operations_hospitality_property_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_hospitality_property_operations_governed_model`: validates policy, writes owned `hospitality_property_operations_hospitality_property_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_13`: validates policy, writes owned `hospitality_property_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_14`: validates policy, writes owned `hospitality_property_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_15`: validates policy, writes owned `hospitality_property_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_16`: validates policy, writes owned `hospitality_property_operations_room_inventory` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_17`: validates policy, writes owned `hospitality_property_operations_reservation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_hospitality_property_operations_18`: validates policy, writes owned `hospitality_property_operations_guest_stay` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Hospitality Property Operations domain records.
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

Rules are first-class artifacts: ('room_inventory_policy', 'reservation_policy', 'guest_stay_policy', 'housekeeping_task_policy', 'guest_request_policy', 'occupancy_snapshot_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /room-inventorys', 'POST /reservations', 'POST /guest-stays', 'POST /housekeeping-tasks', 'POST /guest-requests', 'GET /hospitality-property-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `hospitality_property_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('HospitalityPropertyOperationsCreated', 'HospitalityPropertyOperationsUpdated', 'HospitalityPropertyOperationsApproved', 'HospitalityPropertyOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('room inventory board', 'reservation board', 'guest stay board', 'housekeeping task board', 'guest request board', 'occupancy snapshot board', 'rate plan board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `hospitality_property_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: room_inventory, reservation, guest_stay, housekeeping_task, guest_request, occupancy_snapshot, rate_plan, hospitality_property_operations_policy_rule, hospitality_property_operations_runtime_parameter, hospitality_property_operations_schema_extension, hospitality_property_operations_control_assertion, hospitality_property_operations_governed_model
- operations: create_room_inventory, record_reservation, review_guest_stay, approve_housekeeping_task, simulate_guest_request, create_occupancy_snapshot, record_rate_plan, review_hospitality_property_operations_policy_rule, approve_hospitality_property_operations_runtime_parameter, simulate_hospitality_property_operations_schema_extension, create_hospitality_property_operations_control_assertion, record_hospitality_property_operations_governed_model, operate_hospitality_property_operations_13, operate_hospitality_property_operations_14, operate_hospitality_property_operations_15, operate_hospitality_property_operations_16, operate_hospitality_property_operations_17, operate_hospitality_property_operations_18
- emits: HospitalityPropertyOperationsCreated, HospitalityPropertyOperationsUpdated, HospitalityPropertyOperationsApproved, HospitalityPropertyOperationsExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: room_inventory_policy, reservation_policy, guest_stay_policy, housekeeping_task_policy, guest_request_policy, occupancy_snapshot_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: HospitalityPropertyOperationsWorkbench, HospitalityPropertyOperationsDetail, HospitalityPropertyOperationsAssistantPanel
- permissions: hospitality_property_operations.read, hospitality_property_operations.create, hospitality_property_operations.update, hospitality_property_operations.approve, hospitality_property_operations.admin
- configuration: HOSPITALITY_PROPERTY_OPERATIONS_DATABASE_URL, HOSPITALITY_PROPERTY_OPERATIONS_EVENT_TOPIC, HOSPITALITY_PROPERTY_OPERATIONS_RETRY_LIMIT, HOSPITALITY_PROPERTY_OPERATIONS_DEFAULT_POLICY
- standard_features: room_inventory_management, hospitality_property_operations_workflow, hospitality_property_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: hospitality_property_operations_event_sourced_operational_history, hospitality_property_operations_multi_tenant_policy_isolation, hospitality_property_operations_schema_evolution_resilience, hospitality_property_operations_autonomous_anomaly_detection, hospitality_property_operations_semantic_document_instruction_understanding, hospitality_property_operations_predictive_risk_scoring, hospitality_property_operations_counterfactual_scenario_simulation, hospitality_property_operations_cryptographic_audit_proofs, hospitality_property_operations_continuous_control_testing, hospitality_property_operations_carbon_and_sustainability_awareness, hospitality_property_operations_cross_pbc_event_federation, hospitality_property_operations_governed_ai_agent_execution
