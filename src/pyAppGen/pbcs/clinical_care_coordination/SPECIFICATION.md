# Clinical Care Coordination PBC

## Purpose

The `clinical_care_coordination` PBC is a packaged business capability for Care plans, referrals, encounters, care teams, transitions, outcomes, and patient coordination workflows. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `clinical_care_coordination`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/clinical_care_coordination`.
- Runtime entrypoint: `clinical_care_coordination_runtime_capabilities()`.
- UI entrypoint: `clinical_care_coordination_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `clinical_care_coordination_patient_care_plan`: owns patient care plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_care_team`: owns care team lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_referral`: owns referral lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_encounter`: owns encounter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_care_gap`: owns care gap lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_transition_plan`: owns transition plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_outcome_measure`: owns outcome measure lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_clinical_care_coordination_policy_rule`: owns clinical care coordination policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_clinical_care_coordination_runtime_parameter`: owns clinical care coordination runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_clinical_care_coordination_schema_extension`: owns clinical care coordination schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_clinical_care_coordination_control_assertion`: owns clinical care coordination control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `clinical_care_coordination_clinical_care_coordination_governed_model`: owns clinical care coordination governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `clinical_care_coordination_appgen_outbox_event`, `clinical_care_coordination_appgen_inbox_event`, and `clinical_care_coordination_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /patient-care-plans', 'POST /care-teams', 'POST /referrals', 'POST /encounters', 'POST /care-gaps', 'GET /clinical-care-coordination-workbench').

## Executable Domain Operations

- `create_patient_care_plan`: validates policy, writes owned `clinical_care_coordination_patient_care_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_care_team`: validates policy, writes owned `clinical_care_coordination_care_team` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_referral`: validates policy, writes owned `clinical_care_coordination_referral` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_encounter`: validates policy, writes owned `clinical_care_coordination_encounter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_care_gap`: validates policy, writes owned `clinical_care_coordination_care_gap` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_transition_plan`: validates policy, writes owned `clinical_care_coordination_transition_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_outcome_measure`: validates policy, writes owned `clinical_care_coordination_outcome_measure` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_clinical_care_coordination_policy_rule`: validates policy, writes owned `clinical_care_coordination_clinical_care_coordination_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_clinical_care_coordination_runtime_parameter`: validates policy, writes owned `clinical_care_coordination_clinical_care_coordination_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_clinical_care_coordination_schema_extension`: validates policy, writes owned `clinical_care_coordination_clinical_care_coordination_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_clinical_care_coordination_control_assertion`: validates policy, writes owned `clinical_care_coordination_clinical_care_coordination_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_clinical_care_coordination_governed_model`: validates policy, writes owned `clinical_care_coordination_clinical_care_coordination_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_13`: validates policy, writes owned `clinical_care_coordination_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_14`: validates policy, writes owned `clinical_care_coordination_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_15`: validates policy, writes owned `clinical_care_coordination_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_16`: validates policy, writes owned `clinical_care_coordination_patient_care_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_17`: validates policy, writes owned `clinical_care_coordination_care_team` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_clinical_care_coordination_18`: validates policy, writes owned `clinical_care_coordination_referral` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Clinical Care Coordination domain records.
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

Rules are first-class artifacts: ('patient_care_plan_policy', 'care_team_policy', 'referral_policy', 'encounter_policy', 'care_gap_policy', 'transition_plan_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /patient-care-plans', 'POST /care-teams', 'POST /referrals', 'POST /encounters', 'POST /care-gaps', 'GET /clinical-care-coordination-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `clinical_care_coordination_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ClinicalCareCoordinationCreated', 'ClinicalCareCoordinationUpdated', 'ClinicalCareCoordinationApproved', 'ClinicalCareCoordinationExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('patient care plan board', 'care team board', 'referral board', 'encounter board', 'care gap board', 'transition plan board', 'outcome measure board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `clinical_care_coordination_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: patient_care_plan, care_team, referral, encounter, care_gap, transition_plan, outcome_measure, clinical_care_coordination_policy_rule, clinical_care_coordination_runtime_parameter, clinical_care_coordination_schema_extension, clinical_care_coordination_control_assertion, clinical_care_coordination_governed_model
- operations: create_patient_care_plan, record_care_team, review_referral, approve_encounter, simulate_care_gap, create_transition_plan, record_outcome_measure, review_clinical_care_coordination_policy_rule, approve_clinical_care_coordination_runtime_parameter, simulate_clinical_care_coordination_schema_extension, create_clinical_care_coordination_control_assertion, record_clinical_care_coordination_governed_model, operate_clinical_care_coordination_13, operate_clinical_care_coordination_14, operate_clinical_care_coordination_15, operate_clinical_care_coordination_16, operate_clinical_care_coordination_17, operate_clinical_care_coordination_18
- emits: ClinicalCareCoordinationCreated, ClinicalCareCoordinationUpdated, ClinicalCareCoordinationApproved, ClinicalCareCoordinationExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: patient_care_plan_policy, care_team_policy, referral_policy, encounter_policy, care_gap_policy, transition_plan_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ClinicalCareCoordinationWorkbench, ClinicalCareCoordinationDetail, ClinicalCareCoordinationAssistantPanel
- permissions: clinical_care_coordination.read, clinical_care_coordination.create, clinical_care_coordination.update, clinical_care_coordination.approve, clinical_care_coordination.admin
- configuration: CLINICAL_CARE_COORDINATION_DATABASE_URL, CLINICAL_CARE_COORDINATION_EVENT_TOPIC, CLINICAL_CARE_COORDINATION_RETRY_LIMIT, CLINICAL_CARE_COORDINATION_DEFAULT_POLICY
- standard_features: patient_care_plan_management, clinical_care_coordination_workflow, clinical_care_coordination_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: clinical_care_coordination_event_sourced_operational_history, clinical_care_coordination_multi_tenant_policy_isolation, clinical_care_coordination_schema_evolution_resilience, clinical_care_coordination_autonomous_anomaly_detection, clinical_care_coordination_semantic_document_instruction_understanding, clinical_care_coordination_predictive_risk_scoring, clinical_care_coordination_counterfactual_scenario_simulation, clinical_care_coordination_cryptographic_audit_proofs, clinical_care_coordination_continuous_control_testing, clinical_care_coordination_carbon_and_sustainability_awareness, clinical_care_coordination_cross_pbc_event_federation, clinical_care_coordination_governed_ai_agent_execution
