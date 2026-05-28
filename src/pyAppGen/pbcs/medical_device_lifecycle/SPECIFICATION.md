# Medical Device Lifecycle PBC

## Purpose

The `medical_device_lifecycle` PBC is a packaged business capability for Medical device registry, maintenance, calibration, recalls, usage traceability, and regulatory evidence. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `medical_device_lifecycle`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/medical_device_lifecycle`.
- Runtime entrypoint: `medical_device_lifecycle_runtime_capabilities()`.
- UI entrypoint: `medical_device_lifecycle_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `medical_device_lifecycle_medical_device`: owns medical device lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_device_assignment`: owns device assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_calibration`: owns calibration lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_maintenance_event`: owns maintenance event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_recall_notice`: owns recall notice lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_usage_trace`: owns usage trace lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_regulatory_evidence`: owns regulatory evidence lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_medical_device_lifecycle_policy_rule`: owns medical device lifecycle policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_medical_device_lifecycle_runtime_parameter`: owns medical device lifecycle runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_medical_device_lifecycle_schema_extension`: owns medical device lifecycle schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_medical_device_lifecycle_control_assertion`: owns medical device lifecycle control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `medical_device_lifecycle_medical_device_lifecycle_governed_model`: owns medical device lifecycle governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `medical_device_lifecycle_appgen_outbox_event`, `medical_device_lifecycle_appgen_inbox_event`, and `medical_device_lifecycle_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /medical-devices', 'POST /device-assignments', 'POST /calibrations', 'POST /maintenance-events', 'POST /recall-notices', 'GET /medical-device-lifecycle-workbench').

## Executable Domain Operations

- `create_medical_device`: validates policy, writes owned `medical_device_lifecycle_medical_device` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_device_assignment`: validates policy, writes owned `medical_device_lifecycle_device_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_calibration`: validates policy, writes owned `medical_device_lifecycle_calibration` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_maintenance_event`: validates policy, writes owned `medical_device_lifecycle_maintenance_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_recall_notice`: validates policy, writes owned `medical_device_lifecycle_recall_notice` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_usage_trace`: validates policy, writes owned `medical_device_lifecycle_usage_trace` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_regulatory_evidence`: validates policy, writes owned `medical_device_lifecycle_regulatory_evidence` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_medical_device_lifecycle_policy_rule`: validates policy, writes owned `medical_device_lifecycle_medical_device_lifecycle_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_medical_device_lifecycle_runtime_parameter`: validates policy, writes owned `medical_device_lifecycle_medical_device_lifecycle_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_medical_device_lifecycle_schema_extension`: validates policy, writes owned `medical_device_lifecycle_medical_device_lifecycle_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_medical_device_lifecycle_control_assertion`: validates policy, writes owned `medical_device_lifecycle_medical_device_lifecycle_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_medical_device_lifecycle_governed_model`: validates policy, writes owned `medical_device_lifecycle_medical_device_lifecycle_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_13`: validates policy, writes owned `medical_device_lifecycle_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_14`: validates policy, writes owned `medical_device_lifecycle_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_15`: validates policy, writes owned `medical_device_lifecycle_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_16`: validates policy, writes owned `medical_device_lifecycle_medical_device` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_17`: validates policy, writes owned `medical_device_lifecycle_device_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_medical_device_lifecycle_18`: validates policy, writes owned `medical_device_lifecycle_calibration` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Medical Device Lifecycle domain records.
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

Rules are first-class artifacts: ('medical_device_policy', 'device_assignment_policy', 'calibration_policy', 'maintenance_event_policy', 'recall_notice_policy', 'usage_trace_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /medical-devices', 'POST /device-assignments', 'POST /calibrations', 'POST /maintenance-events', 'POST /recall-notices', 'GET /medical-device-lifecycle-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `medical_device_lifecycle_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MedicalDeviceLifecycleCreated', 'MedicalDeviceLifecycleUpdated', 'MedicalDeviceLifecycleApproved', 'MedicalDeviceLifecycleExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('medical device board', 'device assignment board', 'calibration board', 'maintenance event board', 'recall notice board', 'usage trace board', 'regulatory evidence board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `medical_device_lifecycle_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: medical_device, device_assignment, calibration, maintenance_event, recall_notice, usage_trace, regulatory_evidence, medical_device_lifecycle_policy_rule, medical_device_lifecycle_runtime_parameter, medical_device_lifecycle_schema_extension, medical_device_lifecycle_control_assertion, medical_device_lifecycle_governed_model
- operations: create_medical_device, record_device_assignment, review_calibration, approve_maintenance_event, simulate_recall_notice, create_usage_trace, record_regulatory_evidence, review_medical_device_lifecycle_policy_rule, approve_medical_device_lifecycle_runtime_parameter, simulate_medical_device_lifecycle_schema_extension, create_medical_device_lifecycle_control_assertion, record_medical_device_lifecycle_governed_model, operate_medical_device_lifecycle_13, operate_medical_device_lifecycle_14, operate_medical_device_lifecycle_15, operate_medical_device_lifecycle_16, operate_medical_device_lifecycle_17, operate_medical_device_lifecycle_18
- emits: MedicalDeviceLifecycleCreated, MedicalDeviceLifecycleUpdated, MedicalDeviceLifecycleApproved, MedicalDeviceLifecycleExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: medical_device_policy, device_assignment_policy, calibration_policy, maintenance_event_policy, recall_notice_policy, usage_trace_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MedicalDeviceLifecycleWorkbench, MedicalDeviceLifecycleDetail, MedicalDeviceLifecycleAssistantPanel
- permissions: medical_device_lifecycle.read, medical_device_lifecycle.create, medical_device_lifecycle.update, medical_device_lifecycle.approve, medical_device_lifecycle.admin
- configuration: MEDICAL_DEVICE_LIFECYCLE_DATABASE_URL, MEDICAL_DEVICE_LIFECYCLE_EVENT_TOPIC, MEDICAL_DEVICE_LIFECYCLE_RETRY_LIMIT, MEDICAL_DEVICE_LIFECYCLE_DEFAULT_POLICY
- standard_features: medical_device_management, medical_device_lifecycle_workflow, medical_device_lifecycle_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: medical_device_lifecycle_event_sourced_operational_history, medical_device_lifecycle_multi_tenant_policy_isolation, medical_device_lifecycle_schema_evolution_resilience, medical_device_lifecycle_autonomous_anomaly_detection, medical_device_lifecycle_semantic_document_instruction_understanding, medical_device_lifecycle_predictive_risk_scoring, medical_device_lifecycle_counterfactual_scenario_simulation, medical_device_lifecycle_cryptographic_audit_proofs, medical_device_lifecycle_continuous_control_testing, medical_device_lifecycle_carbon_and_sustainability_awareness, medical_device_lifecycle_cross_pbc_event_federation, medical_device_lifecycle_governed_ai_agent_execution
