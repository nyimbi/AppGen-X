# Field Service Management PBC

## Purpose

The `field_service_management` PBC is a world-class packaged business capability for Owns work orders, dispatch, technicians, skills, appointments, parts, mobile execution, warranties, SLA performance, customer confirmations, and field-service intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `field_service_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `field_service_management_work_order`: owns work order lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_service_request`: owns service request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_service_appointment`: owns service appointment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_technician_profile`: owns technician profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_technician_skill`: owns technician skill lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_dispatch_plan`: owns dispatch plan lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_dispatch_assignment`: owns dispatch assignment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_service_part_requirement`: owns service part requirement lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_part_reservation`: owns part reservation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_mobile_work_log`: owns mobile work log lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_service_checklist`: owns service checklist lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_warranty_entitlement`: owns warranty entitlement lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_sla_commitment`: owns sla commitment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_sla_observation`: owns sla observation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_customer_confirmation`: owns customer confirmation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_repeat_visit_signal`: owns repeat visit signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_exception_case`: owns field exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_policy_rule`: owns field policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_runtime_parameter`: owns field runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_schema_extension`: owns field schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_control_assertion`: owns field control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_field_governed_model`: owns field governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `field_service_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `field_service_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `field_service_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for work orders: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_work_order`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `classify_service_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `schedule_appointment`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_technician`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_technician_skill`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_dispatch_plan`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_dispatch`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `reserve_service_part`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_mobile_work_log`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `complete_checklist`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `validate_warranty`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `measure_sla`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_customer_confirmation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `detect_repeat_visit`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_field_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_field_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_dispatch_disruption`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- AI dispatch optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- technician skill graph matching: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- parts shortage prediction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- mobile offline evidence capture: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- SLA breach simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- repeat-visit root-cause intelligence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- consented live workforce geospatial tracking: records current technician position, breadcrumb evidence, accuracy, capture source, geofence events, and privacy consent before any location mutation is accepted.
- constraint-aware route optimization and reoptimization: plans route stops and legs with priority, time-window, traffic, skill, tool, depot, and travel-buffer constraints, then emits AppGen-X route events for downstream projections.
- mobile task dependency orchestration: decomposes work orders into ordered mobile tasks with dependency checks, safety gates, offline rules, and conflict queues for field execution.
- job-tool calibration and custody validation: validates required job tools, tool availability, van stock, calibration status, custody, and reservation readiness before assignment.
- skill-location-tool assignment scoring: ranks candidate technicians by required skills, tool readiness, live location proximity, availability, and configurable assignment thresholds.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Workforce Tracking, Routing, Tasking, Tools, and Skills

The PBC now owns a complete field workforce execution surface rather than a generic dispatch placeholder.

- Live workforce tracking is represented by `field_service_management_technician_live_location`, `field_service_management_technician_location_breadcrumb`, `field_service_management_geofence_event`, and `field_service_management_location_privacy_consent`. Location updates require explicit privacy consent and record technician, tenant, latitude, longitude, accuracy, source, capture time, and AppGen-X event evidence.
- Technician availability is represented by `field_service_management_technician_availability` and `field_service_management_technician_home_base`, covering shift capacity, status, home/depot start points, and schedule windows.
- Routing is represented by `field_service_management_service_route_plan`, `field_service_management_service_route_stop`, `field_service_management_service_route_leg`, and `field_service_management_route_reoptimization`, covering stop ordering, route legs, ETA minutes, distance, traffic state, time windows, disruption reasons, blocked stops, and reoptimization constraints.
- Tasking is represented by `field_service_management_mobile_task_dependency` and `field_service_management_task_safety_gate`, covering task dependencies, safety prerequisites, offline execution flags, dependency blocking, and mobile conflict policies.
- Job-tool requirements are represented by `field_service_management_job_tool_requirement`, `field_service_management_tool_inventory`, `field_service_management_tool_calibration`, and `field_service_management_van_stock_position`, covering required tool classes, availability, calibration state, custody/readiness, and van-stock/depot readiness.
- Skill-based assignment is represented by `field_service_management_skill_assignment_score` and `field_service_management_assignment_constraint`, covering candidate ranking by skill match, required tools, location proximity, availability, explanation factors, and configurable minimum assignment score.
- UI surfaces include live workforce map, route optimizer, technician availability board, skill assignment console, job-tool requirement planner, tool calibration and custody console, task dependency board, and offline mobile conflict queue.
- Agent skills expose the same operations to the composed assistant: `track_technician_location`, `update_technician_availability`, `optimize_service_route`, `reoptimize_route_for_disruption`, `plan_mobile_task_dependencies`, `validate_job_tool_requirements`, `reserve_job_tools`, and `assign_by_skill_location_and_tools`.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `dispatch_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `skill_match_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `parts_reservation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `warranty_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `sla_escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `safety_checklist_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `sla_warning_minutes`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `travel_buffer_minutes`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `minimum_skill_score`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `part_shortage_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `repeat_visit_window_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `field_service_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `WorkOrderCreated`
- `AppointmentScheduled`
- `TechnicianDispatched`
- `PartReserved`
- `WorkOrderCompleted`
- `SlaRiskChanged`

Consumed events:

- `CustomerUpdated`
- `InventoryReserved`
- `PaymentCaptured`
- `PolicyChanged`

Handlers use idempotency keys of the form `field_service_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- field service workbench.
- dispatch board.
- technician schedule.
- parts reservation panel.
- mobile completion console.
- SLA risk board.
- warranty validation panel.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `field_service_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: work_order, service_request, service_appointment, technician_profile, technician_skill, dispatch_plan, dispatch_assignment, service_part_requirement, part_reservation, mobile_work_log, service_checklist, warranty_entitlement, sla_commitment, sla_observation, customer_confirmation, repeat_visit_signal, field_exception_case, field_policy_rule, field_runtime_parameter, field_schema_extension, field_control_assertion, field_governed_model
- operations: create_work_order, classify_service_request, schedule_appointment, register_technician, capture_technician_skill, build_dispatch_plan, assign_dispatch, reserve_service_part, record_mobile_work_log, complete_checklist, validate_warranty, measure_sla, capture_customer_confirmation, detect_repeat_visit, resolve_field_exception, compile_field_rule, simulate_dispatch_disruption
- emits: WorkOrderCreated, AppointmentScheduled, TechnicianDispatched, PartReserved, WorkOrderCompleted, SlaRiskChanged
- consumes: CustomerUpdated, InventoryReserved, PaymentCaptured, PolicyChanged
- rules: dispatch_policy, skill_match_policy, parts_reservation_policy, warranty_policy, sla_escalation_policy, safety_checklist_policy
- parameters: sla_warning_minutes, travel_buffer_minutes, minimum_skill_score, part_shortage_threshold, repeat_visit_window_days, workbench_limit
- advanced_capabilities: AI dispatch optimization, technician skill graph matching, parts shortage prediction, mobile offline evidence capture, SLA breach simulation, repeat-visit root-cause intelligence
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: field_work_order, dispatch_assignment, technician_profile, mobile_task, parts_usage, service_sla, service_history, customer_service_update
- apis: POST /field-work-orders, POST /dispatch-assignments, POST /mobile-tasks, POST /parts-usage, GET /field-service-workbench
- emits: FieldWorkOrderCreated, TechnicianDispatched, FieldTaskCompleted, ServiceSlaBreached
- consumes: ServiceTicketOpened, InventoryPositionUpdated, CustomerUpdated
- ui_fragments: FieldServiceManagementWorkbench, FieldServiceManagementDetail, FieldServiceManagementAssistantPanel
- permissions: field_service_management.read, field_service_management.create, field_service_management.update, field_service_management.approve, field_service_management.admin
- configuration: FIELD_SERVICE_MANAGEMENT_DATABASE_URL, FIELD_SERVICE_MANAGEMENT_EVENT_TOPIC, FIELD_SERVICE_MANAGEMENT_RETRY_LIMIT, FIELD_SERVICE_MANAGEMENT_DEFAULT_POLICY
- standard_features: field_work_order_management, field_service_management_workflow, field_service_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: field_service_management_event_sourced_operational_history, field_service_management_multi_tenant_policy_isolation, field_service_management_schema_evolution_resilience, field_service_management_autonomous_anomaly_detection, field_service_management_semantic_document_instruction_understanding, field_service_management_predictive_risk_scoring, field_service_management_counterfactual_scenario_simulation, field_service_management_cryptographic_audit_proofs, field_service_management_continuous_control_testing, field_service_management_carbon_and_sustainability_awareness, field_service_management_cross_pbc_event_federation, field_service_management_governed_ai_agent_execution
