# Travel Management PBC

## Purpose

The `travel_management` PBC is a world-class packaged business capability for Owns trip requests, travel policy, booking intents, itineraries, approvals, duty-of-care, disruptions, unused tickets, settlement, and traveler assistance. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `travel_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `travel_management_trip_request`: owns trip request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_traveler_profile`: owns traveler profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_policy`: owns travel policy lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_approval_task`: owns travel approval task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_booking_intent`: owns booking intent lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_air_booking`: owns air booking lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_hotel_booking`: owns hotel booking lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_ground_booking`: owns ground booking lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_itinerary_item`: owns itinerary item lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_duty_of_care_alert`: owns duty of care alert lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_disruption`: owns travel disruption lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_unused_ticket`: owns unused ticket lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_expense_link`: owns travel expense link lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_risk_assessment`: owns travel risk assessment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_supplier_offer`: owns travel supplier offer lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_exception_case`: owns travel exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_policy_rule`: owns travel policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_runtime_parameter`: owns travel runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_schema_extension`: owns travel schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_control_assertion`: owns travel control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_travel_governed_model`: owns travel governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `travel_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `travel_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `travel_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for trips: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_trip_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `validate_travel_policy`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `route_travel_approval`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_booking_intent`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_air_booking`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_hotel_booking`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_ground_booking`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_itinerary`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `screen_duty_of_care`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_travel_disruption`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_unused_ticket`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `link_travel_expense`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_travel_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compare_supplier_offer`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_travel_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_travel_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_disruption_impact`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- traveler-aware policy guidance: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- disruption counterfactual routing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic itinerary ingestion: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- duty-of-care risk intelligence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- unused-ticket optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- carbon-aware booking comparison: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `travel_approval_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `fare_class_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `hotel_rate_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `duty_of_care_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `unused_ticket_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `disruption_escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `advance_booking_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `hotel_rate_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `risk_alert_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `unused_ticket_warning_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `approval_amount_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `travel_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `TripRequested`
- `TravelApproved`
- `ItineraryBuilt`
- `DutyOfCareAlertOpened`
- `TravelDisruptionOpened`
- `UnusedTicketRecorded`

Consumed events:

- `EmployeeCreated`
- `ExpenseReportCreated`
- `PolicyChanged`
- `PaymentExecuted`

Handlers use idempotency keys of the form `travel_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- travel workbench.
- trip request board.
- booking intent console.
- itinerary timeline.
- duty of care map.
- disruption queue.
- unused ticket panel.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `travel_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: trip_request, traveler_profile, travel_policy, travel_approval_task, booking_intent, air_booking, hotel_booking, ground_booking, itinerary_item, duty_of_care_alert, travel_disruption, unused_ticket, travel_expense_link, travel_risk_assessment, travel_supplier_offer, travel_exception_case, travel_policy_rule, travel_runtime_parameter, travel_schema_extension, travel_control_assertion, travel_governed_model
- operations: create_trip_request, validate_travel_policy, route_travel_approval, create_booking_intent, record_air_booking, record_hotel_booking, record_ground_booking, build_itinerary, screen_duty_of_care, open_travel_disruption, track_unused_ticket, link_travel_expense, score_travel_risk, compare_supplier_offer, resolve_travel_exception, compile_travel_rule, simulate_disruption_impact
- emits: TripRequested, TravelApproved, ItineraryBuilt, DutyOfCareAlertOpened, TravelDisruptionOpened, UnusedTicketRecorded
- consumes: EmployeeCreated, ExpenseReportCreated, PolicyChanged, PaymentExecuted
- rules: travel_approval_policy, fare_class_policy, hotel_rate_policy, duty_of_care_policy, unused_ticket_policy, disruption_escalation_policy
- parameters: advance_booking_days, hotel_rate_limit, risk_alert_threshold, unused_ticket_warning_days, approval_amount_limit, workbench_limit
- advanced_capabilities: traveler-aware policy guidance, disruption counterfactual routing, semantic itinerary ingestion, duty-of-care risk intelligence, unused-ticket optimization, carbon-aware booking comparison
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: travel_request, travel_booking, travel_itinerary, travel_policy_check, duty_of_care_alert, supplier_travel_feed, travel_expense_handoff, travel_carbon_record
- apis: POST /travel-requests, POST /travel-bookings, POST /itineraries, POST /policy-checks, GET /travel-workbench
- emits: TravelApproved, TravelBooked, DutyOfCareAlerted, TravelExpenseHandedOff
- consumes: EmployeeProvisioned, ExpenseApproved, SupplierQualified
- ui_fragments: TravelManagementWorkbench, TravelManagementDetail, TravelManagementAssistantPanel
- permissions: travel_management.read, travel_management.create, travel_management.update, travel_management.approve, travel_management.admin
- configuration: TRAVEL_MANAGEMENT_DATABASE_URL, TRAVEL_MANAGEMENT_EVENT_TOPIC, TRAVEL_MANAGEMENT_RETRY_LIMIT, TRAVEL_MANAGEMENT_DEFAULT_POLICY
- standard_features: travel_request_management, travel_management_workflow, travel_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: travel_management_event_sourced_operational_history, travel_management_multi_tenant_policy_isolation, travel_management_schema_evolution_resilience, travel_management_autonomous_anomaly_detection, travel_management_semantic_document_instruction_understanding, travel_management_predictive_risk_scoring, travel_management_counterfactual_scenario_simulation, travel_management_cryptographic_audit_proofs, travel_management_continuous_control_testing, travel_management_carbon_and_sustainability_awareness, travel_management_cross_pbc_event_federation, travel_management_governed_ai_agent_execution
