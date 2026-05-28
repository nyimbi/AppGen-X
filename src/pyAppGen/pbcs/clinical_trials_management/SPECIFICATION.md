# Clinical Trials Management PBC

## Purpose

The `clinical_trials_management` PBC is a packaged business capability for Protocols, trial sites, subjects, consent, visits, adverse events, monitoring, and trial data operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `clinical_trials_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/clinical_trials_management`.
- Runtime entrypoint: `clinical_trials_management_runtime_capabilities()`.
- UI entrypoint: `clinical_trials_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `clinical_trials_management_trial_protocol`: owns trial protocol lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_study_site`: owns study site lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_subject`: owns subject lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_consent_record`: owns consent record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_visit_schedule`: owns visit schedule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_adverse_event`: owns adverse event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_monitoring_finding`: owns monitoring finding lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_clinical_trials_management_policy_rule`: owns clinical trials management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_clinical_trials_management_runtime_parameter`: owns clinical trials management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_clinical_trials_management_schema_extension`: owns clinical trials management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_clinical_trials_management_control_assertion`: owns clinical trials management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_trials_management_clinical_trials_management_governed_model`: owns clinical trials management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `clinical_trials_management_appgen_outbox_event`, `clinical_trials_management_appgen_inbox_event`, and `clinical_trials_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /trial-protocols', 'POST /study-sites', 'POST /subjects', 'POST /consent-records', 'POST /visit-schedules', 'GET /clinical-trials-management-workbench').

## Executable Domain Operations

- `create_trial_protocol`: validates policy, writes owned `clinical_trials_management_trial_protocol` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_study_site`: validates policy, writes owned `clinical_trials_management_study_site` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_subject`: validates policy, writes owned `clinical_trials_management_subject` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_consent_record`: validates policy, writes owned `clinical_trials_management_consent_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_visit_schedule`: validates policy, writes owned `clinical_trials_management_visit_schedule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_adverse_event`: validates policy, writes owned `clinical_trials_management_adverse_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_monitoring_finding`: validates policy, writes owned `clinical_trials_management_monitoring_finding` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_clinical_trials_management_policy_rule`: validates policy, writes owned `clinical_trials_management_clinical_trials_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_clinical_trials_management_runtime_parameter`: validates policy, writes owned `clinical_trials_management_clinical_trials_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_clinical_trials_management_schema_extension`: validates policy, writes owned `clinical_trials_management_clinical_trials_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_clinical_trials_management_control_assertion`: validates policy, writes owned `clinical_trials_management_clinical_trials_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_clinical_trials_management_governed_model`: validates policy, writes owned `clinical_trials_management_clinical_trials_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_13`: validates policy, writes owned `clinical_trials_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_14`: validates policy, writes owned `clinical_trials_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_15`: validates policy, writes owned `clinical_trials_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_16`: validates policy, writes owned `clinical_trials_management_trial_protocol` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_17`: validates policy, writes owned `clinical_trials_management_study_site` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_trials_management_18`: validates policy, writes owned `clinical_trials_management_subject` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Clinical Trials Management domain records.
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

Rules are first-class artifacts: ('trial_protocol_policy', 'study_site_policy', 'subject_policy', 'consent_record_policy', 'visit_schedule_policy', 'adverse_event_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /trial-protocols', 'POST /study-sites', 'POST /subjects', 'POST /consent-records', 'POST /visit-schedules', 'GET /clinical-trials-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `clinical_trials_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ClinicalTrialsManagementCreated', 'ClinicalTrialsManagementUpdated', 'ClinicalTrialsManagementApproved', 'ClinicalTrialsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('trial protocol board', 'study site board', 'subject board', 'consent record board', 'visit schedule board', 'adverse event board', 'monitoring finding board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `clinical_trials_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: trial_protocol, study_site, subject, consent_record, visit_schedule, adverse_event, monitoring_finding, clinical_trials_management_policy_rule, clinical_trials_management_runtime_parameter, clinical_trials_management_schema_extension, clinical_trials_management_control_assertion, clinical_trials_management_governed_model
- operations: create_trial_protocol, record_study_site, review_subject, approve_consent_record, simulate_visit_schedule, create_adverse_event, record_monitoring_finding, review_clinical_trials_management_policy_rule, approve_clinical_trials_management_runtime_parameter, simulate_clinical_trials_management_schema_extension, create_clinical_trials_management_control_assertion, record_clinical_trials_management_governed_model, operate_clinical_trials_management_13, operate_clinical_trials_management_14, operate_clinical_trials_management_15, operate_clinical_trials_management_16, operate_clinical_trials_management_17, operate_clinical_trials_management_18
- emits: ClinicalTrialsManagementCreated, ClinicalTrialsManagementUpdated, ClinicalTrialsManagementApproved, ClinicalTrialsManagementExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: trial_protocol_policy, study_site_policy, subject_policy, consent_record_policy, visit_schedule_policy, adverse_event_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ClinicalTrialsManagementWorkbench, ClinicalTrialsManagementDetail, ClinicalTrialsManagementAssistantPanel
- permissions: clinical_trials_management.read, clinical_trials_management.create, clinical_trials_management.update, clinical_trials_management.approve, clinical_trials_management.admin
- configuration: CLINICAL_TRIALS_MANAGEMENT_DATABASE_URL, CLINICAL_TRIALS_MANAGEMENT_EVENT_TOPIC, CLINICAL_TRIALS_MANAGEMENT_RETRY_LIMIT, CLINICAL_TRIALS_MANAGEMENT_DEFAULT_POLICY
- standard_features: trial_protocol_management, clinical_trials_management_workflow, clinical_trials_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: clinical_trials_management_event_sourced_operational_history, clinical_trials_management_multi_tenant_policy_isolation, clinical_trials_management_schema_evolution_resilience, clinical_trials_management_autonomous_anomaly_detection, clinical_trials_management_semantic_document_instruction_understanding, clinical_trials_management_predictive_risk_scoring, clinical_trials_management_counterfactual_scenario_simulation, clinical_trials_management_cryptographic_audit_proofs, clinical_trials_management_continuous_control_testing, clinical_trials_management_carbon_and_sustainability_awareness, clinical_trials_management_cross_pbc_event_federation, clinical_trials_management_governed_ai_agent_execution
