# Mining Safety and Permits PBC

## Purpose

The `mining_safety_permits` PBC is a packaged business capability for Mine permits, shifts, blasts, inspections, incidents, safety controls, and regulatory evidence. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `mining_safety_permits`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/mining_safety_permits`.
- Runtime entrypoint: `mining_safety_permits_runtime_capabilities()`.
- UI entrypoint: `mining_safety_permits_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `mining_safety_permits_mine_permit`: owns mine permit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_shift_roster`: owns shift roster lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_blast_plan`: owns blast plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_safety_inspection`: owns safety inspection lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_incident_report`: owns incident report lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_regulatory_submission`: owns regulatory submission lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_control_action`: owns control action lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_mining_safety_permits_policy_rule`: owns mining safety permits policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_mining_safety_permits_runtime_parameter`: owns mining safety permits runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_mining_safety_permits_schema_extension`: owns mining safety permits schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_mining_safety_permits_control_assertion`: owns mining safety permits control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `mining_safety_permits_mining_safety_permits_governed_model`: owns mining safety permits governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `mining_safety_permits_appgen_outbox_event`, `mining_safety_permits_appgen_inbox_event`, and `mining_safety_permits_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /mine-permits', 'POST /shift-rosters', 'POST /blast-plans', 'POST /safety-inspections', 'POST /incident-reports', 'GET /mining-safety-permits-workbench').

## Executable Domain Operations

- `create_mine_permit`: validates policy, writes owned `mining_safety_permits_mine_permit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_shift_roster`: validates policy, writes owned `mining_safety_permits_shift_roster` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_blast_plan`: validates policy, writes owned `mining_safety_permits_blast_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_safety_inspection`: validates policy, writes owned `mining_safety_permits_safety_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_incident_report`: validates policy, writes owned `mining_safety_permits_incident_report` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_regulatory_submission`: validates policy, writes owned `mining_safety_permits_regulatory_submission` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_control_action`: validates policy, writes owned `mining_safety_permits_control_action` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_mining_safety_permits_policy_rule`: validates policy, writes owned `mining_safety_permits_mining_safety_permits_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_mining_safety_permits_runtime_parameter`: validates policy, writes owned `mining_safety_permits_mining_safety_permits_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_mining_safety_permits_schema_extension`: validates policy, writes owned `mining_safety_permits_mining_safety_permits_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_mining_safety_permits_control_assertion`: validates policy, writes owned `mining_safety_permits_mining_safety_permits_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_mining_safety_permits_governed_model`: validates policy, writes owned `mining_safety_permits_mining_safety_permits_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_13`: validates policy, writes owned `mining_safety_permits_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_14`: validates policy, writes owned `mining_safety_permits_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_15`: validates policy, writes owned `mining_safety_permits_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_16`: validates policy, writes owned `mining_safety_permits_mine_permit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_17`: validates policy, writes owned `mining_safety_permits_shift_roster` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_mining_safety_permits_18`: validates policy, writes owned `mining_safety_permits_blast_plan` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Mining Safety and Permits domain records.
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

Rules are first-class artifacts: ('mine_permit_policy', 'shift_roster_policy', 'blast_plan_policy', 'safety_inspection_policy', 'incident_report_policy', 'regulatory_submission_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /mine-permits', 'POST /shift-rosters', 'POST /blast-plans', 'POST /safety-inspections', 'POST /incident-reports', 'GET /mining-safety-permits-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `mining_safety_permits_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MiningSafetyPermitsCreated', 'MiningSafetyPermitsUpdated', 'MiningSafetyPermitsApproved', 'MiningSafetyPermitsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('mine permit board', 'shift roster board', 'blast plan board', 'safety inspection board', 'incident report board', 'regulatory submission board', 'control action board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `mining_safety_permits_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: mine_permit, shift_roster, blast_plan, safety_inspection, incident_report, regulatory_submission, control_action, mining_safety_permits_policy_rule, mining_safety_permits_runtime_parameter, mining_safety_permits_schema_extension, mining_safety_permits_control_assertion, mining_safety_permits_governed_model
- operations: create_mine_permit, record_shift_roster, review_blast_plan, approve_safety_inspection, simulate_incident_report, create_regulatory_submission, record_control_action, review_mining_safety_permits_policy_rule, approve_mining_safety_permits_runtime_parameter, simulate_mining_safety_permits_schema_extension, create_mining_safety_permits_control_assertion, record_mining_safety_permits_governed_model, operate_mining_safety_permits_13, operate_mining_safety_permits_14, operate_mining_safety_permits_15, operate_mining_safety_permits_16, operate_mining_safety_permits_17, operate_mining_safety_permits_18
- emits: MiningSafetyPermitsCreated, MiningSafetyPermitsUpdated, MiningSafetyPermitsApproved, MiningSafetyPermitsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: mine_permit_policy, shift_roster_policy, blast_plan_policy, safety_inspection_policy, incident_report_policy, regulatory_submission_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MiningSafetyPermitsWorkbench, MiningSafetyPermitsDetail, MiningSafetyPermitsAssistantPanel
- permissions: mining_safety_permits.read, mining_safety_permits.create, mining_safety_permits.update, mining_safety_permits.approve, mining_safety_permits.admin
- configuration: MINING_SAFETY_PERMITS_DATABASE_URL, MINING_SAFETY_PERMITS_EVENT_TOPIC, MINING_SAFETY_PERMITS_RETRY_LIMIT, MINING_SAFETY_PERMITS_DEFAULT_POLICY
- standard_features: mine_permit_management, mining_safety_permits_workflow, mining_safety_permits_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: mining_safety_permits_event_sourced_operational_history, mining_safety_permits_multi_tenant_policy_isolation, mining_safety_permits_schema_evolution_resilience, mining_safety_permits_autonomous_anomaly_detection, mining_safety_permits_semantic_document_instruction_understanding, mining_safety_permits_predictive_risk_scoring, mining_safety_permits_counterfactual_scenario_simulation, mining_safety_permits_cryptographic_audit_proofs, mining_safety_permits_continuous_control_testing, mining_safety_permits_carbon_and_sustainability_awareness, mining_safety_permits_cross_pbc_event_federation, mining_safety_permits_governed_ai_agent_execution
