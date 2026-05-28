# Construction Project Controls PBC

## Purpose

The `construction_project_controls` PBC is a packaged business capability for Construction budgets, schedules, RFIs, submittals, change events, field progress, and site risk controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `construction_project_controls`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/construction_project_controls`.
- Runtime entrypoint: `construction_project_controls_runtime_capabilities()`.
- UI entrypoint: `construction_project_controls_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `construction_project_controls_construction_project`: owns construction project lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_work_package`: owns work package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_rfi`: owns rfi lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_submittal`: owns submittal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_site_progress`: owns site progress lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_change_event`: owns change event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_schedule_risk`: owns schedule risk lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_construction_project_controls_policy_rule`: owns construction project controls policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_construction_project_controls_runtime_parameter`: owns construction project controls runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_construction_project_controls_schema_extension`: owns construction project controls schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_construction_project_controls_control_assertion`: owns construction project controls control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `construction_project_controls_construction_project_controls_governed_model`: owns construction project controls governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `construction_project_controls_appgen_outbox_event`, `construction_project_controls_appgen_inbox_event`, and `construction_project_controls_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /construction-projects', 'POST /work-packages', 'POST /rfis', 'POST /submittals', 'POST /site-progresss', 'GET /construction-project-controls-workbench').

## Executable Domain Operations

- `create_construction_project`: validates policy, writes owned `construction_project_controls_construction_project` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_work_package`: validates policy, writes owned `construction_project_controls_work_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_rfi`: validates policy, writes owned `construction_project_controls_rfi` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_submittal`: validates policy, writes owned `construction_project_controls_submittal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_site_progress`: validates policy, writes owned `construction_project_controls_site_progress` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_change_event`: validates policy, writes owned `construction_project_controls_change_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_schedule_risk`: validates policy, writes owned `construction_project_controls_schedule_risk` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_construction_project_controls_policy_rule`: validates policy, writes owned `construction_project_controls_construction_project_controls_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_construction_project_controls_runtime_parameter`: validates policy, writes owned `construction_project_controls_construction_project_controls_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_construction_project_controls_schema_extension`: validates policy, writes owned `construction_project_controls_construction_project_controls_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_construction_project_controls_control_assertion`: validates policy, writes owned `construction_project_controls_construction_project_controls_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_construction_project_controls_governed_model`: validates policy, writes owned `construction_project_controls_construction_project_controls_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_13`: validates policy, writes owned `construction_project_controls_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_14`: validates policy, writes owned `construction_project_controls_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_15`: validates policy, writes owned `construction_project_controls_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_16`: validates policy, writes owned `construction_project_controls_construction_project` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_17`: validates policy, writes owned `construction_project_controls_work_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_construction_project_controls_18`: validates policy, writes owned `construction_project_controls_rfi` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Construction Project Controls domain records.
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

Rules are first-class artifacts: ('construction_project_policy', 'work_package_policy', 'rfi_policy', 'submittal_policy', 'site_progress_policy', 'change_event_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /construction-projects', 'POST /work-packages', 'POST /rfis', 'POST /submittals', 'POST /site-progresss', 'GET /construction-project-controls-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `construction_project_controls_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ConstructionProjectControlsCreated', 'ConstructionProjectControlsUpdated', 'ConstructionProjectControlsApproved', 'ConstructionProjectControlsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('construction project board', 'work package board', 'rfi board', 'submittal board', 'site progress board', 'change event board', 'schedule risk board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `construction_project_controls_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: construction_project, work_package, rfi, submittal, site_progress, change_event, schedule_risk, construction_project_controls_policy_rule, construction_project_controls_runtime_parameter, construction_project_controls_schema_extension, construction_project_controls_control_assertion, construction_project_controls_governed_model
- operations: create_construction_project, record_work_package, review_rfi, approve_submittal, simulate_site_progress, create_change_event, record_schedule_risk, review_construction_project_controls_policy_rule, approve_construction_project_controls_runtime_parameter, simulate_construction_project_controls_schema_extension, create_construction_project_controls_control_assertion, record_construction_project_controls_governed_model, operate_construction_project_controls_13, operate_construction_project_controls_14, operate_construction_project_controls_15, operate_construction_project_controls_16, operate_construction_project_controls_17, operate_construction_project_controls_18
- emits: ConstructionProjectControlsCreated, ConstructionProjectControlsUpdated, ConstructionProjectControlsApproved, ConstructionProjectControlsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: construction_project_policy, work_package_policy, rfi_policy, submittal_policy, site_progress_policy, change_event_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ConstructionProjectControlsWorkbench, ConstructionProjectControlsDetail, ConstructionProjectControlsAssistantPanel
- permissions: construction_project_controls.read, construction_project_controls.create, construction_project_controls.update, construction_project_controls.approve, construction_project_controls.admin
- configuration: CONSTRUCTION_PROJECT_CONTROLS_DATABASE_URL, CONSTRUCTION_PROJECT_CONTROLS_EVENT_TOPIC, CONSTRUCTION_PROJECT_CONTROLS_RETRY_LIMIT, CONSTRUCTION_PROJECT_CONTROLS_DEFAULT_POLICY
- standard_features: construction_project_management, construction_project_controls_workflow, construction_project_controls_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: construction_project_controls_event_sourced_operational_history, construction_project_controls_multi_tenant_policy_isolation, construction_project_controls_schema_evolution_resilience, construction_project_controls_autonomous_anomaly_detection, construction_project_controls_semantic_document_instruction_understanding, construction_project_controls_predictive_risk_scoring, construction_project_controls_counterfactual_scenario_simulation, construction_project_controls_cryptographic_audit_proofs, construction_project_controls_continuous_control_testing, construction_project_controls_carbon_and_sustainability_awareness, construction_project_controls_cross_pbc_event_federation, construction_project_controls_governed_ai_agent_execution
