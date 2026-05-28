# Media Production Management PBC

## Purpose

The `media_production_management` PBC is a packaged business capability for Productions, budgets, crews, locations, shoots, post-production, assets, and delivery milestones. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `media_production_management`.
- Mesh: `content`.
- Package directory: `src/pyAppGen/pbcs/media_production_management`.
- Runtime entrypoint: `media_production_management_runtime_capabilities()`.
- UI entrypoint: `media_production_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `media_production_management_production`: owns production lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_budget_line`: owns budget line lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_crew_booking`: owns crew booking lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_location_permit`: owns location permit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_shoot_day`: owns shoot day lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_post_production_task`: owns post production task lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_delivery_asset`: owns delivery asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_media_production_management_policy_rule`: owns media production management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_media_production_management_runtime_parameter`: owns media production management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_media_production_management_schema_extension`: owns media production management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_media_production_management_control_assertion`: owns media production management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `media_production_management_media_production_management_governed_model`: owns media production management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `media_production_management_appgen_outbox_event`, `media_production_management_appgen_inbox_event`, and `media_production_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /productions', 'POST /budget-lines', 'POST /crew-bookings', 'POST /location-permits', 'POST /shoot-days', 'GET /media-production-management-workbench').

## Executable Domain Operations

- `create_production`: validates policy, writes owned `media_production_management_production` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_budget_line`: validates policy, writes owned `media_production_management_budget_line` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_crew_booking`: validates policy, writes owned `media_production_management_crew_booking` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_location_permit`: validates policy, writes owned `media_production_management_location_permit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_shoot_day`: validates policy, writes owned `media_production_management_shoot_day` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_post_production_task`: validates policy, writes owned `media_production_management_post_production_task` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_delivery_asset`: validates policy, writes owned `media_production_management_delivery_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_media_production_management_policy_rule`: validates policy, writes owned `media_production_management_media_production_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_media_production_management_runtime_parameter`: validates policy, writes owned `media_production_management_media_production_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_media_production_management_schema_extension`: validates policy, writes owned `media_production_management_media_production_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_media_production_management_control_assertion`: validates policy, writes owned `media_production_management_media_production_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_media_production_management_governed_model`: validates policy, writes owned `media_production_management_media_production_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_13`: validates policy, writes owned `media_production_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_14`: validates policy, writes owned `media_production_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_15`: validates policy, writes owned `media_production_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_16`: validates policy, writes owned `media_production_management_production` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_17`: validates policy, writes owned `media_production_management_budget_line` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_media_production_management_18`: validates policy, writes owned `media_production_management_crew_booking` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Media Production Management domain records.
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

Rules are first-class artifacts: ('production_policy', 'budget_line_policy', 'crew_booking_policy', 'location_permit_policy', 'shoot_day_policy', 'post_production_task_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /productions', 'POST /budget-lines', 'POST /crew-bookings', 'POST /location-permits', 'POST /shoot-days', 'GET /media-production-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `media_production_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MediaProductionManagementCreated', 'MediaProductionManagementUpdated', 'MediaProductionManagementApproved', 'MediaProductionManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('production board', 'budget line board', 'crew booking board', 'location permit board', 'shoot day board', 'post production task board', 'delivery asset board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `media_production_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: production, budget_line, crew_booking, location_permit, shoot_day, post_production_task, delivery_asset, media_production_management_policy_rule, media_production_management_runtime_parameter, media_production_management_schema_extension, media_production_management_control_assertion, media_production_management_governed_model
- operations: create_production, record_budget_line, review_crew_booking, approve_location_permit, simulate_shoot_day, create_post_production_task, record_delivery_asset, review_media_production_management_policy_rule, approve_media_production_management_runtime_parameter, simulate_media_production_management_schema_extension, create_media_production_management_control_assertion, record_media_production_management_governed_model, operate_media_production_management_13, operate_media_production_management_14, operate_media_production_management_15, operate_media_production_management_16, operate_media_production_management_17, operate_media_production_management_18
- emits: MediaProductionManagementCreated, MediaProductionManagementUpdated, MediaProductionManagementApproved, MediaProductionManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: production_policy, budget_line_policy, crew_booking_policy, location_permit_policy, shoot_day_policy, post_production_task_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MediaProductionManagementWorkbench, MediaProductionManagementDetail, MediaProductionManagementAssistantPanel
- permissions: media_production_management.read, media_production_management.create, media_production_management.update, media_production_management.approve, media_production_management.admin
- configuration: MEDIA_PRODUCTION_MANAGEMENT_DATABASE_URL, MEDIA_PRODUCTION_MANAGEMENT_EVENT_TOPIC, MEDIA_PRODUCTION_MANAGEMENT_RETRY_LIMIT, MEDIA_PRODUCTION_MANAGEMENT_DEFAULT_POLICY
- standard_features: production_management, media_production_management_workflow, media_production_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: media_production_management_event_sourced_operational_history, media_production_management_multi_tenant_policy_isolation, media_production_management_schema_evolution_resilience, media_production_management_autonomous_anomaly_detection, media_production_management_semantic_document_instruction_understanding, media_production_management_predictive_risk_scoring, media_production_management_counterfactual_scenario_simulation, media_production_management_cryptographic_audit_proofs, media_production_management_continuous_control_testing, media_production_management_carbon_and_sustainability_awareness, media_production_management_cross_pbc_event_federation, media_production_management_governed_ai_agent_execution
