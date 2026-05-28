# Nonprofit Program Impact PBC

## Purpose

The `nonprofit_program_impact` PBC is a packaged business capability for Programs, beneficiaries, outcomes, grants, services, restrictions, impact evidence, and donor reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `nonprofit_program_impact`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/nonprofit_program_impact`.
- Runtime entrypoint: `nonprofit_program_impact_runtime_capabilities()`.
- UI entrypoint: `nonprofit_program_impact_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `nonprofit_program_impact_program`: owns program lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_beneficiary`: owns beneficiary lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_service_episode`: owns service episode lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_outcome_measure`: owns outcome measure lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_grant_restriction`: owns grant restriction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_impact_evidence`: owns impact evidence lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_donor_report`: owns donor report lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_nonprofit_program_impact_policy_rule`: owns nonprofit program impact policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_nonprofit_program_impact_runtime_parameter`: owns nonprofit program impact runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_nonprofit_program_impact_schema_extension`: owns nonprofit program impact schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_nonprofit_program_impact_control_assertion`: owns nonprofit program impact control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `nonprofit_program_impact_nonprofit_program_impact_governed_model`: owns nonprofit program impact governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `nonprofit_program_impact_appgen_outbox_event`, `nonprofit_program_impact_appgen_inbox_event`, and `nonprofit_program_impact_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /programs', 'POST /beneficiarys', 'POST /service-episodes', 'POST /outcome-measures', 'POST /grant-restrictions', 'GET /nonprofit-program-impact-workbench').

## Executable Domain Operations

- `create_program`: validates policy, writes owned `nonprofit_program_impact_program` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_beneficiary`: validates policy, writes owned `nonprofit_program_impact_beneficiary` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_service_episode`: validates policy, writes owned `nonprofit_program_impact_service_episode` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_outcome_measure`: validates policy, writes owned `nonprofit_program_impact_outcome_measure` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_grant_restriction`: validates policy, writes owned `nonprofit_program_impact_grant_restriction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_impact_evidence`: validates policy, writes owned `nonprofit_program_impact_impact_evidence` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_donor_report`: validates policy, writes owned `nonprofit_program_impact_donor_report` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_nonprofit_program_impact_policy_rule`: validates policy, writes owned `nonprofit_program_impact_nonprofit_program_impact_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_nonprofit_program_impact_runtime_parameter`: validates policy, writes owned `nonprofit_program_impact_nonprofit_program_impact_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_nonprofit_program_impact_schema_extension`: validates policy, writes owned `nonprofit_program_impact_nonprofit_program_impact_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_nonprofit_program_impact_control_assertion`: validates policy, writes owned `nonprofit_program_impact_nonprofit_program_impact_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_nonprofit_program_impact_governed_model`: validates policy, writes owned `nonprofit_program_impact_nonprofit_program_impact_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_13`: validates policy, writes owned `nonprofit_program_impact_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_14`: validates policy, writes owned `nonprofit_program_impact_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_15`: validates policy, writes owned `nonprofit_program_impact_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_16`: validates policy, writes owned `nonprofit_program_impact_program` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_17`: validates policy, writes owned `nonprofit_program_impact_beneficiary` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_nonprofit_program_impact_18`: validates policy, writes owned `nonprofit_program_impact_service_episode` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Nonprofit Program Impact domain records.
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

Rules are first-class artifacts: ('program_policy', 'beneficiary_policy', 'service_episode_policy', 'outcome_measure_policy', 'grant_restriction_policy', 'impact_evidence_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /programs', 'POST /beneficiarys', 'POST /service-episodes', 'POST /outcome-measures', 'POST /grant-restrictions', 'GET /nonprofit-program-impact-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `nonprofit_program_impact_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('NonprofitProgramImpactCreated', 'NonprofitProgramImpactUpdated', 'NonprofitProgramImpactApproved', 'NonprofitProgramImpactExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('program board', 'beneficiary board', 'service episode board', 'outcome measure board', 'grant restriction board', 'impact evidence board', 'donor report board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `nonprofit_program_impact_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: program, beneficiary, service_episode, outcome_measure, grant_restriction, impact_evidence, donor_report, nonprofit_program_impact_policy_rule, nonprofit_program_impact_runtime_parameter, nonprofit_program_impact_schema_extension, nonprofit_program_impact_control_assertion, nonprofit_program_impact_governed_model
- operations: create_program, record_beneficiary, review_service_episode, approve_outcome_measure, simulate_grant_restriction, create_impact_evidence, record_donor_report, review_nonprofit_program_impact_policy_rule, approve_nonprofit_program_impact_runtime_parameter, simulate_nonprofit_program_impact_schema_extension, create_nonprofit_program_impact_control_assertion, record_nonprofit_program_impact_governed_model, operate_nonprofit_program_impact_13, operate_nonprofit_program_impact_14, operate_nonprofit_program_impact_15, operate_nonprofit_program_impact_16, operate_nonprofit_program_impact_17, operate_nonprofit_program_impact_18
- emits: NonprofitProgramImpactCreated, NonprofitProgramImpactUpdated, NonprofitProgramImpactApproved, NonprofitProgramImpactExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: program_policy, beneficiary_policy, service_episode_policy, outcome_measure_policy, grant_restriction_policy, impact_evidence_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: NonprofitProgramImpactWorkbench, NonprofitProgramImpactDetail, NonprofitProgramImpactAssistantPanel
- permissions: nonprofit_program_impact.read, nonprofit_program_impact.create, nonprofit_program_impact.update, nonprofit_program_impact.approve, nonprofit_program_impact.admin
- configuration: NONPROFIT_PROGRAM_IMPACT_DATABASE_URL, NONPROFIT_PROGRAM_IMPACT_EVENT_TOPIC, NONPROFIT_PROGRAM_IMPACT_RETRY_LIMIT, NONPROFIT_PROGRAM_IMPACT_DEFAULT_POLICY
- standard_features: program_management, nonprofit_program_impact_workflow, nonprofit_program_impact_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: nonprofit_program_impact_event_sourced_operational_history, nonprofit_program_impact_multi_tenant_policy_isolation, nonprofit_program_impact_schema_evolution_resilience, nonprofit_program_impact_autonomous_anomaly_detection, nonprofit_program_impact_semantic_document_instruction_understanding, nonprofit_program_impact_predictive_risk_scoring, nonprofit_program_impact_counterfactual_scenario_simulation, nonprofit_program_impact_cryptographic_audit_proofs, nonprofit_program_impact_continuous_control_testing, nonprofit_program_impact_carbon_and_sustainability_awareness, nonprofit_program_impact_cross_pbc_event_federation, nonprofit_program_impact_governed_ai_agent_execution
