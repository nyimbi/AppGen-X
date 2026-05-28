# Aviation Maintenance and Repair PBC

## Purpose

The `aviation_maintenance_repair` PBC is a packaged business capability for Aircraft maintenance, components, work cards, compliance, airworthiness, deferred defects, and MRO operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `aviation_maintenance_repair`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/aviation_maintenance_repair`.
- Runtime entrypoint: `aviation_maintenance_repair_runtime_capabilities()`.
- UI entrypoint: `aviation_maintenance_repair_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `aviation_maintenance_repair_aircraft`: owns aircraft lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_component`: owns component lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_work_card`: owns work card lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_maintenance_visit`: owns maintenance visit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_airworthiness_directive`: owns airworthiness directive lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_deferred_defect`: owns deferred defect lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_compliance_release`: owns compliance release lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_aviation_maintenance_repair_policy_rule`: owns aviation maintenance repair policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_aviation_maintenance_repair_runtime_parameter`: owns aviation maintenance repair runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_aviation_maintenance_repair_schema_extension`: owns aviation maintenance repair schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_aviation_maintenance_repair_control_assertion`: owns aviation maintenance repair control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `aviation_maintenance_repair_aviation_maintenance_repair_governed_model`: owns aviation maintenance repair governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `aviation_maintenance_repair_appgen_outbox_event`, `aviation_maintenance_repair_appgen_inbox_event`, and `aviation_maintenance_repair_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /aircrafts', 'POST /components', 'POST /work-cards', 'POST /maintenance-visits', 'POST /airworthiness-directives', 'GET /aviation-maintenance-repair-workbench').

## Executable Domain Operations

- `create_aircraft`: validates policy, writes owned `aviation_maintenance_repair_aircraft` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_component`: validates policy, writes owned `aviation_maintenance_repair_component` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_work_card`: validates policy, writes owned `aviation_maintenance_repair_work_card` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_maintenance_visit`: validates policy, writes owned `aviation_maintenance_repair_maintenance_visit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_airworthiness_directive`: validates policy, writes owned `aviation_maintenance_repair_airworthiness_directive` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_deferred_defect`: validates policy, writes owned `aviation_maintenance_repair_deferred_defect` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_compliance_release`: validates policy, writes owned `aviation_maintenance_repair_compliance_release` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_aviation_maintenance_repair_policy_rule`: validates policy, writes owned `aviation_maintenance_repair_aviation_maintenance_repair_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_aviation_maintenance_repair_runtime_parameter`: validates policy, writes owned `aviation_maintenance_repair_aviation_maintenance_repair_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_aviation_maintenance_repair_schema_extension`: validates policy, writes owned `aviation_maintenance_repair_aviation_maintenance_repair_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_aviation_maintenance_repair_control_assertion`: validates policy, writes owned `aviation_maintenance_repair_aviation_maintenance_repair_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_aviation_maintenance_repair_governed_model`: validates policy, writes owned `aviation_maintenance_repair_aviation_maintenance_repair_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_13`: validates policy, writes owned `aviation_maintenance_repair_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_14`: validates policy, writes owned `aviation_maintenance_repair_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_15`: validates policy, writes owned `aviation_maintenance_repair_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_16`: validates policy, writes owned `aviation_maintenance_repair_aircraft` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_17`: validates policy, writes owned `aviation_maintenance_repair_component` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_aviation_maintenance_repair_18`: validates policy, writes owned `aviation_maintenance_repair_work_card` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Aviation Maintenance and Repair domain records.
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

Rules are first-class artifacts: ('aircraft_policy', 'component_policy', 'work_card_policy', 'maintenance_visit_policy', 'airworthiness_directive_policy', 'deferred_defect_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /aircrafts', 'POST /components', 'POST /work-cards', 'POST /maintenance-visits', 'POST /airworthiness-directives', 'GET /aviation-maintenance-repair-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `aviation_maintenance_repair_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AviationMaintenanceRepairCreated', 'AviationMaintenanceRepairUpdated', 'AviationMaintenanceRepairApproved', 'AviationMaintenanceRepairExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('aircraft board', 'component board', 'work card board', 'maintenance visit board', 'airworthiness directive board', 'deferred defect board', 'compliance release board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `aviation_maintenance_repair_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: aircraft, component, work_card, maintenance_visit, airworthiness_directive, deferred_defect, compliance_release, aviation_maintenance_repair_policy_rule, aviation_maintenance_repair_runtime_parameter, aviation_maintenance_repair_schema_extension, aviation_maintenance_repair_control_assertion, aviation_maintenance_repair_governed_model
- operations: create_aircraft, record_component, review_work_card, approve_maintenance_visit, simulate_airworthiness_directive, create_deferred_defect, record_compliance_release, review_aviation_maintenance_repair_policy_rule, approve_aviation_maintenance_repair_runtime_parameter, simulate_aviation_maintenance_repair_schema_extension, create_aviation_maintenance_repair_control_assertion, record_aviation_maintenance_repair_governed_model, operate_aviation_maintenance_repair_13, operate_aviation_maintenance_repair_14, operate_aviation_maintenance_repair_15, operate_aviation_maintenance_repair_16, operate_aviation_maintenance_repair_17, operate_aviation_maintenance_repair_18
- emits: AviationMaintenanceRepairCreated, AviationMaintenanceRepairUpdated, AviationMaintenanceRepairApproved, AviationMaintenanceRepairExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: aircraft_policy, component_policy, work_card_policy, maintenance_visit_policy, airworthiness_directive_policy, deferred_defect_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AviationMaintenanceRepairWorkbench, AviationMaintenanceRepairDetail, AviationMaintenanceRepairAssistantPanel
- permissions: aviation_maintenance_repair.read, aviation_maintenance_repair.create, aviation_maintenance_repair.update, aviation_maintenance_repair.approve, aviation_maintenance_repair.admin
- configuration: AVIATION_MAINTENANCE_REPAIR_DATABASE_URL, AVIATION_MAINTENANCE_REPAIR_EVENT_TOPIC, AVIATION_MAINTENANCE_REPAIR_RETRY_LIMIT, AVIATION_MAINTENANCE_REPAIR_DEFAULT_POLICY
- standard_features: aircraft_management, aviation_maintenance_repair_workflow, aviation_maintenance_repair_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: aviation_maintenance_repair_event_sourced_operational_history, aviation_maintenance_repair_multi_tenant_policy_isolation, aviation_maintenance_repair_schema_evolution_resilience, aviation_maintenance_repair_autonomous_anomaly_detection, aviation_maintenance_repair_semantic_document_instruction_understanding, aviation_maintenance_repair_predictive_risk_scoring, aviation_maintenance_repair_counterfactual_scenario_simulation, aviation_maintenance_repair_cryptographic_audit_proofs, aviation_maintenance_repair_continuous_control_testing, aviation_maintenance_repair_carbon_and_sustainability_awareness, aviation_maintenance_repair_cross_pbc_event_federation, aviation_maintenance_repair_governed_ai_agent_execution
