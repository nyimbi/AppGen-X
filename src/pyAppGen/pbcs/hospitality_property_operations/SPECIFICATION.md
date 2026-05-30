# Hospitality Property Operations PBC

## Purpose

`hospitality_property_operations` is the package-local operating core for hotel room readiness, reservations, guest stays, housekeeping dispatch, guest request recovery, occupancy projection, and rate-plan readiness. The source package remains side-effect-free for discovery and registration, while the standalone slice inside this directory provides executable command and query flows for local validation. The design is intentionally strict about the owned datastore boundary: the PBC owns hotel operating tables and AppGen-X event tables, and it collaborates with adjacent PBCs only through declared API routes, AppGen-X events, and package-local projections. No shared or foreign table mutation is allowed.

## Stable Identity

- PBC key: `hospitality_property_operations`
- Package directory: `src/pyAppGen/pbcs/hospitality_property_operations`
- Runtime entrypoint: `hospitality_property_operations_runtime_capabilities()`
- Standalone entrypoint: `hospitality_property_operations_standalone_app_contract()`
- Source registration entrypoints: `register_pbc()`, `registration_plan()`, `package_metadata_manifest()`, `package_discovery_plan()`
- Database backends for the owned contract: PostgreSQL, MySQL, MariaDB
- Local execution harness: sqlite only and package-local
- Eventing standard: AppGen-X outbox, inbox, dead-letter, idempotent handler, and retry contract
- User-visible stream engine picker: forbidden and hidden

## Owned Boundary and Schema Materialization

The owned schema, model metadata, and migration are aligned in `models.py`, `runtime.py`, and `migrations/001_initial.sql`. The package owns the following business tables and no others:

- `hospitality_property_operations_room_inventory`
- `hospitality_property_operations_reservation`
- `hospitality_property_operations_guest_stay`
- `hospitality_property_operations_housekeeping_task`
- `hospitality_property_operations_guest_request`
- `hospitality_property_operations_occupancy_snapshot`
- `hospitality_property_operations_rate_plan`
- `hospitality_property_operations_hospitality_property_operations_policy_rule`
- `hospitality_property_operations_hospitality_property_operations_runtime_parameter`
- `hospitality_property_operations_hospitality_property_operations_schema_extension`
- `hospitality_property_operations_hospitality_property_operations_control_assertion`
- `hospitality_property_operations_hospitality_property_operations_governed_model`

The package also owns the AppGen-X runtime event tables `hospitality_property_operations_appgen_outbox_event`, `hospitality_property_operations_appgen_inbox_event`, and `hospitality_property_operations_appgen_dead_letter_event`. Migration DDL is materialized, model metadata is materialized, and the source package exposes a schema contract that remains side-effect-free for discovery and register flows.

## Service, API, Command, and Query Surface

The source-package service layer exposes command and query contracts. Commands cover runtime configuration, room-inventory command intake, reservation intake, guest-stay intake, housekeeping-task intake, and guest-request intake. Queries expose the workbench summary surface. The standalone slice adds executable command routes and query routes for room detail, shift handover, occupancy capture, and rate-plan updates.

Source APIs:

- `POST /room-inventorys`
- `POST /reservations`
- `POST /guest-stays`
- `POST /housekeeping-tasks`
- `POST /guest-requests`
- `GET /hospitality-property-operations-workbench`

Standalone local routes:

- `POST /app/hospitality-property-operations/rooms`
- `POST /app/hospitality-property-operations/reservations`
- `POST /app/hospitality-property-operations/stays/check-in`
- `POST /app/hospitality-property-operations/stays/check-out`
- `POST /app/hospitality-property-operations/stays/move`
- `POST /app/hospitality-property-operations/housekeeping-tasks`
- `POST /app/hospitality-property-operations/housekeeping-tasks/complete`
- `POST /app/hospitality-property-operations/guest-requests`
- `POST /app/hospitality-property-operations/guest-requests/resolve`
- `POST /app/hospitality-property-operations/occupancy-snapshots`
- `POST /app/hospitality-property-operations/rate-plans`
- `GET /app/hospitality-property-operations/workbench`
- `GET /app/hospitality-property-operations/rooms/detail`
- `GET /app/hospitality-property-operations/shift-handover`

## Events, Inbox, Outbox, Idempotent Handlers, and Retry

The package uses AppGen-X eventing only. Emitted standalone domain events are `RoomInventoryAdjusted`, `ReservationBooked`, `GuestCheckedIn`, `HousekeepingTaskCompleted`, `GuestRequestRecovered`, `OccupancySnapshotCaptured`, `RatePlanAdjusted`, and `ShiftHandoverPrepared`. Consumed events are `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`. The handler surface is idempotent, the inbox stores idempotency keys, retries are configured, and unsupported events route to the dead-letter table for recovery evidence.

Compatibility traceability also preserves the source-package legacy emitted lifecycle markers used by broader AppGen cataloging: `HospitalityPropertyOperationsCreated`, `HospitalityPropertyOperationsUpdated`, `HospitalityPropertyOperationsApproved`, and `HospitalityPropertyOperationsExceptionOpened`.

## UI, Workbench, Permissions, and RBAC

The UI contract exposes the exact fragments `HospitalityPropertyOperationsWorkbench`, `HospitalityPropertyOperationsDetail`, and `HospitalityPropertyOperationsAssistantPanel`. The workbench renders arrival, in-house, departure, room-ready, exception, and service-recovery lanes. Room detail renders sellable-state evidence, housekeeping history, guest requests, active stay state, and the event timeline.

RBAC and permission coverage are explicit. The package includes `hospitality_property_operations.read`, `hospitality_property_operations.create`, `hospitality_property_operations.update`, `hospitality_property_operations.approve`, and `hospitality_property_operations.admin`. The standalone surface maps forms and controls to role-aware permissions for front office, housekeeping supervisor, revenue manager, approver, and auditor roles.

## Rules, Parameters, Configuration, and Governance

Rules are first-class and executable. The package defines `room_sellable_state`, `accessible_assignment_guard`, `reservation_guarantee_cutoff`, `overbooking_limit`, `late_checkout_approval`, and `guest_request_sla`. Parameters are bounded and executable: `turn_time_minutes`, `inspection_delay_minutes`, `arrival_rush_threshold`, `same_day_turn_limit`, `oversell_threshold`, `late_night_escalation_minutes`, and `workbench_limit`.

Configuration is explicit and validated. The source package recognizes `HOSPITALITY_PROPERTY_OPERATIONS_DATABASE_URL`, `HOSPITALITY_PROPERTY_OPERATIONS_EVENT_TOPIC`, `HOSPITALITY_PROPERTY_OPERATIONS_RETRY_LIMIT`, and `HOSPITALITY_PROPERTY_OPERATIONS_DEFAULT_POLICY`. The standalone governance surface also validates a workbench limit and keeps configuration side-effect-free until execution time.

## Agent, Assistant, Chatbot, Skills, and Document Intake

The assistant and chatbot surface is package-local and route-aware. The package contributes skills for arrival pickup triage, service recovery, revenue control, and shift handover. The agent surface supports document and instruction parsing, governed datastore CRUD planning, mutation previews, workflow recommendation, and handover summaries. Every mutation-oriented plan requires human confirmation. CRUD and datastore plans are limited to owned tables only.

## Workflows and Domain Depth

The PBC exposes four core workflows:

1. `arrival_turnaround` for booking, housekeeping, release, and check-in.
2. `service_recovery` for guest-request handling, room moves, and confirmation.
3. `revenue_control` for occupancy, rate fences, and operational exception review.
4. `shift_handover` for unresolved arrivals, blocked rooms, and service recovery packets.

These workflows are modeled as explicit command sequences and executable query-backed views. The source package remains side-effect-free for discovery, while the standalone slice executes real local flows for tests and release evidence.

## Standard and Advanced Capabilities

Standard capabilities include room_inventory_management, hospitality_property_operations_workflow, hospitality_property_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, and continuous_release_assurance.

Advanced capabilities include hospitality_property_operations_event_sourced_operational_history, hospitality_property_operations_multi_tenant_policy_isolation, hospitality_property_operations_schema_evolution_resilience, hospitality_property_operations_autonomous_anomaly_detection, hospitality_property_operations_semantic_document_instruction_understanding, hospitality_property_operations_predictive_risk_scoring, hospitality_property_operations_counterfactual_scenario_simulation, hospitality_property_operations_cryptographic_audit_proofs, hospitality_property_operations_continuous_control_testing, hospitality_property_operations_carbon_and_sustainability_awareness, hospitality_property_operations_cross_pbc_event_federation, and hospitality_property_operations_governed_ai_agent_execution.

## Release, Tests, Seed Data, and Side-Effect-Free Discovery

Release evidence is package-local and executable. It checks schema, service, API, event, handler, UI, agent, governance, documentation, and standalone-app execution. Seed data is materialized for core room, rate, and parameter rows. Tests cover source-package contracts and standalone flows. Package discovery, registration, and metadata generation are explicitly side-effect-free and exist to support self-registration without mutating the broader repo state.

## Manifest Traceability Appendix

- tables: room_inventory, reservation, guest_stay, housekeeping_task, guest_request, occupancy_snapshot, rate_plan, hospitality_property_operations_policy_rule, hospitality_property_operations_runtime_parameter, hospitality_property_operations_schema_extension, hospitality_property_operations_control_assertion, hospitality_property_operations_governed_model
- apis: POST /room-inventorys, POST /reservations, POST /guest-stays, POST /housekeeping-tasks, POST /guest-requests, GET /hospitality-property-operations-workbench
- emits: HospitalityPropertyOperationsCreated, HospitalityPropertyOperationsUpdated, HospitalityPropertyOperationsApproved, HospitalityPropertyOperationsExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- ui_fragments: HospitalityPropertyOperationsWorkbench, HospitalityPropertyOperationsDetail, HospitalityPropertyOperationsAssistantPanel
- permissions: hospitality_property_operations.read, hospitality_property_operations.create, hospitality_property_operations.update, hospitality_property_operations.approve, hospitality_property_operations.admin
- configuration: HOSPITALITY_PROPERTY_OPERATIONS_DATABASE_URL, HOSPITALITY_PROPERTY_OPERATIONS_EVENT_TOPIC, HOSPITALITY_PROPERTY_OPERATIONS_RETRY_LIMIT, HOSPITALITY_PROPERTY_OPERATIONS_DEFAULT_POLICY
- standard_features: room_inventory_management, hospitality_property_operations_workflow, hospitality_property_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: hospitality_property_operations_event_sourced_operational_history, hospitality_property_operations_multi_tenant_policy_isolation, hospitality_property_operations_schema_evolution_resilience, hospitality_property_operations_autonomous_anomaly_detection, hospitality_property_operations_semantic_document_instruction_understanding, hospitality_property_operations_predictive_risk_scoring, hospitality_property_operations_counterfactual_scenario_simulation, hospitality_property_operations_cryptographic_audit_proofs, hospitality_property_operations_continuous_control_testing, hospitality_property_operations_carbon_and_sustainability_awareness, hospitality_property_operations_cross_pbc_event_federation, hospitality_property_operations_governed_ai_agent_execution
