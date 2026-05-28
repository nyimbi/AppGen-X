# Environment Health and Safety PBC

## Purpose

The `environment_health_safety` PBC is a packaged business capability for EHS incidents, inspections, permits, hazards, corrective actions, training, audits, and compliance evidence. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `environment_health_safety`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/environment_health_safety`.
- Runtime entrypoint: `environment_health_safety_runtime_capabilities()`.
- UI entrypoint: `environment_health_safety_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `environment_health_safety_ehs_incident`: owns ehs incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_hazard`: owns hazard lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_inspection`: owns inspection lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_permit`: owns permit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_corrective_action`: owns corrective action lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_safety_training`: owns safety training lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_audit_finding`: owns audit finding lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_environment_health_safety_policy_rule`: owns environment health safety policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_environment_health_safety_runtime_parameter`: owns environment health safety runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_environment_health_safety_schema_extension`: owns environment health safety schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_environment_health_safety_control_assertion`: owns environment health safety control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `environment_health_safety_environment_health_safety_governed_model`: owns environment health safety governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `environment_health_safety_appgen_outbox_event`, `environment_health_safety_appgen_inbox_event`, and `environment_health_safety_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /ehs-incidents', 'POST /hazards', 'POST /inspections', 'POST /permits', 'POST /corrective-actions', 'GET /environment-health-safety-workbench').

## Executable Domain Operations

- `create_ehs_incident`: validates policy, writes owned `environment_health_safety_ehs_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_hazard`: validates policy, writes owned `environment_health_safety_hazard` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_inspection`: validates policy, writes owned `environment_health_safety_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_permit`: validates policy, writes owned `environment_health_safety_permit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_corrective_action`: validates policy, writes owned `environment_health_safety_corrective_action` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_safety_training`: validates policy, writes owned `environment_health_safety_safety_training` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_audit_finding`: validates policy, writes owned `environment_health_safety_audit_finding` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_environment_health_safety_policy_rule`: validates policy, writes owned `environment_health_safety_environment_health_safety_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_environment_health_safety_runtime_parameter`: validates policy, writes owned `environment_health_safety_environment_health_safety_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_environment_health_safety_schema_extension`: validates policy, writes owned `environment_health_safety_environment_health_safety_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_environment_health_safety_control_assertion`: validates policy, writes owned `environment_health_safety_environment_health_safety_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_environment_health_safety_governed_model`: validates policy, writes owned `environment_health_safety_environment_health_safety_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_13`: validates policy, writes owned `environment_health_safety_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_14`: validates policy, writes owned `environment_health_safety_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_15`: validates policy, writes owned `environment_health_safety_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_16`: validates policy, writes owned `environment_health_safety_ehs_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_17`: validates policy, writes owned `environment_health_safety_hazard` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_environment_health_safety_18`: validates policy, writes owned `environment_health_safety_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Environment Health and Safety domain records.
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

Rules are first-class artifacts: ('ehs_incident_policy', 'hazard_policy', 'inspection_policy', 'permit_policy', 'corrective_action_policy', 'safety_training_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /ehs-incidents', 'POST /hazards', 'POST /inspections', 'POST /permits', 'POST /corrective-actions', 'GET /environment-health-safety-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `environment_health_safety_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('EnvironmentHealthSafetyCreated', 'EnvironmentHealthSafetyUpdated', 'EnvironmentHealthSafetyApproved', 'EnvironmentHealthSafetyExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('ehs incident board', 'hazard board', 'inspection board', 'permit board', 'corrective action board', 'safety training board', 'audit finding board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `environment_health_safety_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: ehs_incident, hazard, inspection, permit, corrective_action, safety_training, audit_finding, environment_health_safety_policy_rule, environment_health_safety_runtime_parameter, environment_health_safety_schema_extension, environment_health_safety_control_assertion, environment_health_safety_governed_model
- operations: create_ehs_incident, record_hazard, review_inspection, approve_permit, simulate_corrective_action, create_safety_training, record_audit_finding, review_environment_health_safety_policy_rule, approve_environment_health_safety_runtime_parameter, simulate_environment_health_safety_schema_extension, create_environment_health_safety_control_assertion, record_environment_health_safety_governed_model, operate_environment_health_safety_13, operate_environment_health_safety_14, operate_environment_health_safety_15, operate_environment_health_safety_16, operate_environment_health_safety_17, operate_environment_health_safety_18
- emits: EnvironmentHealthSafetyCreated, EnvironmentHealthSafetyUpdated, EnvironmentHealthSafetyApproved, EnvironmentHealthSafetyExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: ehs_incident_policy, hazard_policy, inspection_policy, permit_policy, corrective_action_policy, safety_training_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: EnvironmentHealthSafetyWorkbench, EnvironmentHealthSafetyDetail, EnvironmentHealthSafetyAssistantPanel
- permissions: environment_health_safety.read, environment_health_safety.create, environment_health_safety.update, environment_health_safety.approve, environment_health_safety.admin
- configuration: ENVIRONMENT_HEALTH_SAFETY_DATABASE_URL, ENVIRONMENT_HEALTH_SAFETY_EVENT_TOPIC, ENVIRONMENT_HEALTH_SAFETY_RETRY_LIMIT, ENVIRONMENT_HEALTH_SAFETY_DEFAULT_POLICY
- standard_features: ehs_incident_management, environment_health_safety_workflow, environment_health_safety_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: environment_health_safety_event_sourced_operational_history, environment_health_safety_multi_tenant_policy_isolation, environment_health_safety_schema_evolution_resilience, environment_health_safety_autonomous_anomaly_detection, environment_health_safety_semantic_document_instruction_understanding, environment_health_safety_predictive_risk_scoring, environment_health_safety_counterfactual_scenario_simulation, environment_health_safety_cryptographic_audit_proofs, environment_health_safety_continuous_control_testing, environment_health_safety_carbon_and_sustainability_awareness, environment_health_safety_cross_pbc_event_federation, environment_health_safety_governed_ai_agent_execution
