# Facilities and Space Management PBC

## Purpose

The `facilities_space_management` PBC is a world-class packaged business capability for Owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `facilities_space_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `facilities_space_management_facility_site`: owns facility site lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_floor`: owns facility floor lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_space_record`: owns space record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_space_type`: owns space type lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_occupancy_plan`: owns occupancy plan lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_occupancy_assignment`: owns occupancy assignment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_space_reservation`: owns space reservation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_move_request`: owns move request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_move_task`: owns move task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_maintenance_signal`: owns maintenance signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_space_availability_snapshot`: owns space availability snapshot lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_access_constraint`: owns access constraint lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_safety_inspection`: owns safety inspection lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_utilization_observation`: owns utilization observation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_capacity_plan`: owns capacity plan lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_exception_case`: owns facility exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_policy_rule`: owns facility policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_runtime_parameter`: owns facility runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_schema_extension`: owns facility schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_control_assertion`: owns facility control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_facility_governed_model`: owns facility governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `facilities_space_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `facilities_space_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `facilities_space_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for facilities: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_facility_site`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_floor`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_space_record`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `classify_space_type`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_occupancy_plan`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_occupant`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `reserve_space`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_move_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `complete_move_task`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_maintenance_signal`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_availability_snapshot`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_access_constraint`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_safety_inspection`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `observe_utilization`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_capacity_plan`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_facility_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_facility_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_space_demand`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- space demand forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- reservation conflict optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- occupancy scenario simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- safety-risk scoring: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- maintenance-aware availability: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- hybrid workplace recommendation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `space_reservation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `occupancy_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `move_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `maintenance_block_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `safety_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `capacity_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `reservation_horizon_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `occupancy_capacity_buffer`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `move_sla_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `utilization_warning_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `safety_review_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `facilities_space_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `FacilityCreated`
- `SpaceReserved`
- `MoveRequested`
- `MaintenanceSignalRecorded`
- `SafetyInspectionRecorded`
- `CapacityPlanPublished`

Consumed events:

- `EmployeeCreated`
- `WorkOrderCompleted`
- `AccessPolicyChanged`
- `PolicyChanged`

Handlers use idempotency keys of the form `facilities_space_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- facilities workbench.
- space map.
- reservation calendar.
- move board.
- maintenance block panel.
- safety inspection console.
- utilization analytics.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `facilities_space_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: facility_site, facility_floor, space_record, space_type, occupancy_plan, occupancy_assignment, space_reservation, move_request, move_task, maintenance_signal, space_availability_snapshot, access_constraint, safety_inspection, utilization_observation, capacity_plan, facility_exception_case, facility_policy_rule, facility_runtime_parameter, facility_schema_extension, facility_control_assertion, facility_governed_model
- operations: create_facility_site, define_floor, create_space_record, classify_space_type, create_occupancy_plan, assign_occupant, reserve_space, open_move_request, complete_move_task, record_maintenance_signal, publish_availability_snapshot, define_access_constraint, record_safety_inspection, observe_utilization, build_capacity_plan, resolve_facility_exception, compile_facility_rule, simulate_space_demand
- emits: FacilityCreated, SpaceReserved, MoveRequested, MaintenanceSignalRecorded, SafetyInspectionRecorded, CapacityPlanPublished
- consumes: EmployeeCreated, WorkOrderCompleted, AccessPolicyChanged, PolicyChanged
- rules: space_reservation_policy, occupancy_policy, move_policy, maintenance_block_policy, safety_policy, capacity_policy
- parameters: reservation_horizon_days, occupancy_capacity_buffer, move_sla_days, utilization_warning_percent, safety_review_days, workbench_limit
- advanced_capabilities: space demand forecasting, reservation conflict optimization, occupancy scenario simulation, safety-risk scoring, maintenance-aware availability, hybrid workplace recommendation
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: facility_site, building, room_space, occupancy_snapshot, space_reservation, maintenance_link, lease_metadata, space_plan
- apis: POST /facility-sites, POST /buildings, POST /spaces, POST /space-reservations, GET /facilities-workbench
- emits: SpaceReserved, OccupancyMeasured, SpacePlanApproved, FacilityMaintenanceLinked
- consumes: EmployeeProvisioned, MaintenanceCompleted, LeaseContractApproved
- ui_fragments: FacilitiesSpaceManagementWorkbench, FacilitiesSpaceManagementDetail, FacilitiesSpaceManagementAssistantPanel
- permissions: facilities_space_management.read, facilities_space_management.create, facilities_space_management.update, facilities_space_management.approve, facilities_space_management.admin
- configuration: FACILITIES_SPACE_MANAGEMENT_DATABASE_URL, FACILITIES_SPACE_MANAGEMENT_EVENT_TOPIC, FACILITIES_SPACE_MANAGEMENT_RETRY_LIMIT, FACILITIES_SPACE_MANAGEMENT_DEFAULT_POLICY
- standard_features: facility_site_management, facilities_space_management_workflow, facilities_space_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: facilities_space_management_event_sourced_operational_history, facilities_space_management_multi_tenant_policy_isolation, facilities_space_management_schema_evolution_resilience, facilities_space_management_autonomous_anomaly_detection, facilities_space_management_semantic_document_instruction_understanding, facilities_space_management_predictive_risk_scoring, facilities_space_management_counterfactual_scenario_simulation, facilities_space_management_cryptographic_audit_proofs, facilities_space_management_continuous_control_testing, facilities_space_management_carbon_and_sustainability_awareness, facilities_space_management_cross_pbc_event_federation, facilities_space_management_governed_ai_agent_execution
