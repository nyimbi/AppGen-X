# Education Student Lifecycle PBC

## Purpose

The `education_student_lifecycle` PBC is a packaged business capability for Admissions, enrollment, curriculum, advising, progression, assessment, credentials, and student outcomes. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `education_student_lifecycle`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/education_student_lifecycle`.
- Runtime entrypoint: `education_student_lifecycle_runtime_capabilities()`.
- UI entrypoint: `education_student_lifecycle_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `education_student_lifecycle_student_applicant`: owns student applicant lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_enrollment`: owns enrollment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_curriculum_plan`: owns curriculum plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_advising_case`: owns advising case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_course_attempt`: owns course attempt lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_assessment_result`: owns assessment result lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_credential`: owns credential lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_education_student_lifecycle_policy_rule`: owns education student lifecycle policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_education_student_lifecycle_runtime_parameter`: owns education student lifecycle runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_education_student_lifecycle_schema_extension`: owns education student lifecycle schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_education_student_lifecycle_control_assertion`: owns education student lifecycle control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `education_student_lifecycle_education_student_lifecycle_governed_model`: owns education student lifecycle governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `education_student_lifecycle_appgen_outbox_event`, `education_student_lifecycle_appgen_inbox_event`, and `education_student_lifecycle_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /student-applicants', 'POST /enrollments', 'POST /curriculum-plans', 'POST /advising-cases', 'POST /course-attempts', 'GET /education-student-lifecycle-workbench').

## Executable Domain Operations

- `create_student_applicant`: validates policy, writes owned `education_student_lifecycle_student_applicant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_enrollment`: validates policy, writes owned `education_student_lifecycle_enrollment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_curriculum_plan`: validates policy, writes owned `education_student_lifecycle_curriculum_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_advising_case`: validates policy, writes owned `education_student_lifecycle_advising_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_course_attempt`: validates policy, writes owned `education_student_lifecycle_course_attempt` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_assessment_result`: validates policy, writes owned `education_student_lifecycle_assessment_result` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_credential`: validates policy, writes owned `education_student_lifecycle_credential` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_education_student_lifecycle_policy_rule`: validates policy, writes owned `education_student_lifecycle_education_student_lifecycle_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_education_student_lifecycle_runtime_parameter`: validates policy, writes owned `education_student_lifecycle_education_student_lifecycle_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_education_student_lifecycle_schema_extension`: validates policy, writes owned `education_student_lifecycle_education_student_lifecycle_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_education_student_lifecycle_control_assertion`: validates policy, writes owned `education_student_lifecycle_education_student_lifecycle_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_education_student_lifecycle_governed_model`: validates policy, writes owned `education_student_lifecycle_education_student_lifecycle_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_13`: validates policy, writes owned `education_student_lifecycle_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_14`: validates policy, writes owned `education_student_lifecycle_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_15`: validates policy, writes owned `education_student_lifecycle_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_16`: validates policy, writes owned `education_student_lifecycle_student_applicant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_17`: validates policy, writes owned `education_student_lifecycle_enrollment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_education_student_lifecycle_18`: validates policy, writes owned `education_student_lifecycle_curriculum_plan` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Education Student Lifecycle domain records.
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

Rules are first-class artifacts: ('student_applicant_policy', 'enrollment_policy', 'curriculum_plan_policy', 'advising_case_policy', 'course_attempt_policy', 'assessment_result_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /student-applicants', 'POST /enrollments', 'POST /curriculum-plans', 'POST /advising-cases', 'POST /course-attempts', 'GET /education-student-lifecycle-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `education_student_lifecycle_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('EducationStudentLifecycleCreated', 'EducationStudentLifecycleUpdated', 'EducationStudentLifecycleApproved', 'EducationStudentLifecycleExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('student applicant board', 'enrollment board', 'curriculum plan board', 'advising case board', 'course attempt board', 'assessment result board', 'credential board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `education_student_lifecycle_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: student_applicant, enrollment, curriculum_plan, advising_case, course_attempt, assessment_result, credential, education_student_lifecycle_policy_rule, education_student_lifecycle_runtime_parameter, education_student_lifecycle_schema_extension, education_student_lifecycle_control_assertion, education_student_lifecycle_governed_model
- operations: create_student_applicant, record_enrollment, review_curriculum_plan, approve_advising_case, simulate_course_attempt, create_assessment_result, record_credential, review_education_student_lifecycle_policy_rule, approve_education_student_lifecycle_runtime_parameter, simulate_education_student_lifecycle_schema_extension, create_education_student_lifecycle_control_assertion, record_education_student_lifecycle_governed_model, operate_education_student_lifecycle_13, operate_education_student_lifecycle_14, operate_education_student_lifecycle_15, operate_education_student_lifecycle_16, operate_education_student_lifecycle_17, operate_education_student_lifecycle_18
- emits: EducationStudentLifecycleCreated, EducationStudentLifecycleUpdated, EducationStudentLifecycleApproved, EducationStudentLifecycleExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: student_applicant_policy, enrollment_policy, curriculum_plan_policy, advising_case_policy, course_attempt_policy, assessment_result_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: EducationStudentLifecycleWorkbench, EducationStudentLifecycleDetail, EducationStudentLifecycleAssistantPanel
- permissions: education_student_lifecycle.read, education_student_lifecycle.create, education_student_lifecycle.update, education_student_lifecycle.approve, education_student_lifecycle.admin
- configuration: EDUCATION_STUDENT_LIFECYCLE_DATABASE_URL, EDUCATION_STUDENT_LIFECYCLE_EVENT_TOPIC, EDUCATION_STUDENT_LIFECYCLE_RETRY_LIMIT, EDUCATION_STUDENT_LIFECYCLE_DEFAULT_POLICY
- standard_features: student_applicant_management, education_student_lifecycle_workflow, education_student_lifecycle_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: education_student_lifecycle_event_sourced_operational_history, education_student_lifecycle_multi_tenant_policy_isolation, education_student_lifecycle_schema_evolution_resilience, education_student_lifecycle_autonomous_anomaly_detection, education_student_lifecycle_semantic_document_instruction_understanding, education_student_lifecycle_predictive_risk_scoring, education_student_lifecycle_counterfactual_scenario_simulation, education_student_lifecycle_cryptographic_audit_proofs, education_student_lifecycle_continuous_control_testing, education_student_lifecycle_carbon_and_sustainability_awareness, education_student_lifecycle_cross_pbc_event_federation, education_student_lifecycle_governed_ai_agent_execution
