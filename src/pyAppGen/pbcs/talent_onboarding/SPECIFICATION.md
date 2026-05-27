# Talent Onboarding

Package-local implementation contract for the Talent Onboarding PBC. The package owns job requisitions, candidates, consents, interview and evaluation evidence, background checks, offers, onboarding tasks, provisioning handoffs, event evidence, rules, parameters, configuration, UI fragments, and release validation from requisition through day-one employee provisioning.

## Stable Identity

- PBC key: `talent_onboarding`.
- Mesh: people/HCM.
- Implementation directory: `src/pyAppGen/pbcs/talent_onboarding`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_talent_onboarding_runtime.py`.
- Event topic: `appgen.talent.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `job_requisition`
- `job_requisition_approval`
- `job_requisition_budget`
- `job_requisition_skill`
- `sourcing_campaign`
- `candidate_source`
- `candidate`
- `candidate_consent`
- `candidate_profile`
- `candidate_skill`
- `candidate_stage_history`
- `candidate_duplicate_check`
- `candidate_privacy_request`
- `interview_plan`
- `interview_panel`
- `interview_schedule`
- `interview_feedback`
- `evaluation_evidence`
- `candidate_scorecard`
- `background_check`
- `background_check_package`
- `background_check_adjudication`
- `adverse_action_notice`
- `offer`
- `offer_approval`
- `offer_acceptance`
- `compensation_projection`
- `onboarding_task`
- `onboarding_task_template`
- `onboarding_checklist`
- `equipment_request`
- `access_preload_projection`
- `welcome_notification_projection`
- `personnel_identity_projection`
- `payroll_worker_projection`
- `role_projection`
- `talent_policy_screening`
- `talent_audit_trace`
- `talent_candidate_proof`
- `talent_federation_projection`
- `talent_carbon_schedule_window`
- `talent_pipeline_optimization`
- `talent_interview_allocation`
- `talent_anomaly_signal`
- `talent_candidate_risk_model`
- `talent_hiring_forecast`
- `talent_parsed_instruction`
- `talent_seed_data`
- `talent_schema_extension`
- `talent_control_assertion`
- `talent_governed_model`
- `talent_rule`
- `talent_parameter`
- `talent_configuration`
- `talent_onboarding_appgen_outbox_event`
- `talent_onboarding_appgen_inbox_event`
- `talent_onboarding_dead_letter_event`

The PBC does not share personnel, payroll, access, notification, recruiting-provider, or audit tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed events: `RoleChanged`, `WorkerIdentityVerified`.
- API dependencies: `GET /roles`, `GET /identity-proofs`, `POST /access-preloads`, `POST /notifications`.
- Projections and handoffs: `personnel_identity_projection`, `access_preload_request`, `notification_welcome_sequence`, `payroll_worker_projection`, `role_projection`, and `audit_ledger_projection`.
- Emitted events: `EmployeeProvisioned`, `CandidateHired`.

## Standard Capabilities

- Job requisition creation, opening, pause/closure policy support, department, manager, location, budget, and headcount descriptors.
- Requisition approvals, budget evidence, required skills, sourcing campaigns, and candidate source tracking.
- Candidate capture with source, skills, country, match score, consent, identity, status, and stage.
- Consent management and privacy/retention policy evidence.
- Candidate profiles, skill evidence, stage history, duplicate checks, and candidate privacy requests.
- Candidate pipeline from application through screening, interview, offer, hired, rejection, withdrawal, and provisioning.
- Interview plan, panel, schedule, feedback, evaluation evidence, and candidate scorecard descriptors.
- Background check request, provider validation, result capture, confidence thresholding, adjudication, and adverse-action review evidence.
- Background check packages, adjudications, adverse-action notices, offer approvals, offer acceptance records, compensation projection, expiry policy, acceptance, decline, and blocked-offer evidence.
- Onboarding task generation by role, location, worker type, and jurisdiction.
- Task templates, onboarding checklists, equipment requests, task assignment, due date, completion, exception, and HR/manager review evidence.
- Employee provisioning handoffs for personnel identity, access preload, and welcome notifications.
- Candidate hire events for analytics and downstream workflows.
- Role and worker-identity projection handling through AppGen-X inbox events.
- Personnel identity, payroll worker, role, access preload, and welcome notification projections as package-local read models.
- Policy screening, audit trace, candidate proof, federation projection, carbon-aware scheduling, pipeline optimization, interview allocation, anomaly, risk, forecast, parsed instruction, control assertion, governed-model, seed, and schema-extension artifacts.
- Source-channel, cycle-time, conversion, hired, provisioned, and task-completion analytics.
- Multi-tenant and multi-entity isolation.
- AppGen-X inbox/outbox idempotency and dead-letter evidence.
- RBAC descriptors for requisition, candidate, offer, onboarding, event, configuration, and audit actions.
- Package-local workbench UI for requisitions, candidates, checks, offers, onboarding tasks, rules, parameters, configuration, and event evidence.

## Generated Schema, Services, And Release Evidence

`build_schema_contract` emits field definitions, relationships, migration paths
under `pbcs/talent_onboarding/migrations/`, generated model names, backend
allowlists, and `shared_table_access: false` for every owned table. The schema
contract covers requisitions, approvals, budgets, skills, sourcing, candidate
sources, candidate profiles, consents, skills, stage history, duplicate checks,
privacy requests, interview plans, panels, schedules, feedback, evaluations,
scorecards, background checks, adjudication, adverse action, offers, offer
approvals, acceptances, compensation projections, onboarding tasks, templates,
checklists, equipment, projections, policy screening, audit, proofs,
federation, carbon scheduling, optimization, allocation, anomaly, risk,
forecast, parsed instructions, seed data, extensions, controls, governed
models, rules, parameters, configuration, outbox, inbox, and dead-letter
artifacts.

`build_service_contract` declares the transaction boundary as the Talent
Onboarding owned datastore plus the AppGen-X outbox. Commands configure the
runtime, set parameters, register rules and schema extensions, receive events,
open requisitions, create candidates, move stages, record checks, extend and
accept offers, create and complete onboarding tasks, provision employees, route
screening/provisioning work, generate candidate proofs, screen policy, federate
talent views, verify identities, run resilience drills, rotate crypto epochs,
schedule carbon-aware interviews, optimize pipelines, allocate interviews, run
controls, and register governed models. Query methods cover workbench views,
hiring policy simulation, hiring-cycle forecasting, semantic instruction
parsing, candidate-risk scoring, exception recommendations, anomaly detection,
stochastic exposure, generated API/schema/release contracts, and boundary
verification.

`build_release_evidence` combines schema, service, API, and permissions
checks: owned schema depth, per-table migration coverage, command depth, fixed
AppGen-X eventing, key command permission coverage, backend allowlist, and no
shared-table access. A Talent Onboarding release is valid only when every check
passes and `blocking_gaps` is empty.

## Advanced Capabilities

- Event-sourced talent lifecycle with immutable hash-chain audit trail.
- Graph-relational hiring topology across requisitions, candidates, checks, offers, tasks, roles, and provisioning handoffs.
- Multi-tenant talent isolation and schema evolution through owned-table extensions.
- Probabilistic candidate-match, fraud, and compliance risk scoring.
- Real-time pipeline and onboarding analytics.
- Counterfactual hiring-policy simulation.
- Hiring demand and cycle-time forecasting.
- Autonomous candidate exception recommendations for missing consent, check review, and task overdue states.
- Semantic candidate instruction parsing.
- Predictive candidate attrition and compliance risk scoring.
- Self-healing screening and provisioning route selection.
- Zero-knowledge candidate eligibility proof generation.
- Dynamic talent policy screening by country and candidate state.
- Automated controls for configuration, rules, parameters, hired/provisioned consistency, and hash-chain integrity.
- Universal API and AppGen-X event contracts.
- Cross-system talent federation through personnel, access, payroll, notification, and audit projections.
- Decentralized candidate identity verification through DID-like evidence.
- Chaos-engineered screening and provisioning tolerance.
- Quantum-resistant authorization simulation through crypto-agile epoch rotation.
- Carbon-aware interview and onboarding scheduling.
- Algebraic pipeline optimization and mechanism-design interview allocation.
- Information-theoretic hiring anomaly detection.
- Temporal hiring exposure stochastic modeling.
- Governed talent model registration with feature lineage, drift, and explainability controls.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X event topic, retry limit, countries, candidate sources, background-check providers, task types, timezone, workbench limit, and stream-picker absence.
- `set_parameter` accepts only supported onboarding parameters.
- `register_rule` validates rule identity, tenant, status, and hiring-rule scope and stores deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles `RoleChanged` and `WorkerIdentityVerified`, records inbox evidence, schedules retries, and dead-letters exhausted failures.
- `create_job_requisition` owns requisition state and opening evidence.
- `create_candidate` owns candidate capture, consent validation, and match thresholding.
- `advance_candidate_stage` enforces allowed-stage policy.
- `record_background_check` validates provider, result, and confidence threshold.
- `extend_offer` and `accept_offer` own offer and acceptance state.
- `create_onboarding_task` and `complete_onboarding_task` own onboarding tasks.
- `provision_employee` emits `CandidateHired` and `EmployeeProvisioned` with downstream handoff evidence.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, dependency, and owned-table evidence.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /job-requisitions` maps to `create_job_requisition`.
- `POST /candidates` maps to `create_candidate`.
- `POST /candidates/{id}/stage` maps to `advance_candidate_stage`.
- `POST /background-checks` maps to `record_background_check`.
- `POST /offers` maps to `extend_offer`.
- `POST /onboarding/tasks` maps to `create_onboarding_task`.
- `POST /onboarding/provision` maps to `provision_employee`.
- `POST /talent/events/inbox` maps to `receive_event`.
- `GET /talent-workbench` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, and dependency evidence.

## Events And Handlers

Emitted events:

- `EmployeeProvisioned`
- `CandidateHired`

Consumed events:

- `RoleChanged`
- `WorkerIdentityVerified`

Handlers are idempotent by idempotency key or event type and event id. Duplicate processed events do not create duplicate state changes. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules cover job eligibility, worker type, allowed countries, required candidate consents, allowed pipeline stages, required check types, task templates, offer policy, onboarding policy, retention policy, provisioning eligibility, and status.

Parameters include:

- `minimum_match_score`
- `offer_expiry_days`
- `onboarding_sla_days`
- `maximum_active_requisitions_per_manager`
- `background_check_confidence_threshold`
- `retention_days`
- `candidate_review_sla_days`
- `interview_panel_size`
- `offer_approval_threshold`
- `workbench_limit`

Configuration includes database backend, event topic, retry limit, allowed countries, allowed candidate sources, allowed background-check providers, allowed task types, default timezone, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, allowed relational backends, hidden stream-engine picker evidence, non-selectable event-contract evidence, and owned tables.

## UI And Workbench

UI fragments:

- `TalentOnboardingWorkbench`
- `RequisitionConsole`
- `CandidatePipelineBoard`
- `BackgroundCheckReview`
- `OfferApprovalBoard`
- `OnboardingTaskBoard`
- `TalentRuleStudio`
- `TalentParameterConsole`
- `TalentConfigurationPanel`

The workbench exposes requisition, candidate, hired, provisioned, background-check, offer, task, inbox, outbox, dead-letter, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by requisition, candidate, offer, onboarding, event, configuration, and audit permissions.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, fixed AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, parameters, rules, schema extensions, event handling, requisitions, candidates, background checks, offers, tasks, provisioning, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, stream-picker configuration, unsupported parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `talent_onboarding`
- Mesh: `hcm`
- Datastore backend: `None`

### Owned Tables

- `job_requisition`
- `job_requisition_approval`
- `job_requisition_budget`
- `job_requisition_skill`
- `sourcing_campaign`
- `candidate_source`
- `candidate`
- `candidate_consent`
- `candidate_profile`
- `candidate_skill`
- `candidate_stage_history`
- `candidate_duplicate_check`
- `candidate_privacy_request`
- `interview_plan`
- `interview_panel`
- `interview_schedule`
- `interview_feedback`
- `evaluation_evidence`
- `candidate_scorecard`
- `background_check`
- `background_check_package`
- `background_check_adjudication`
- `adverse_action_notice`
- `offer`
- `offer_approval`
- `offer_acceptance`
- `compensation_projection`
- `onboarding_task`
- `onboarding_task_template`
- `onboarding_checklist`
- `equipment_request`
- `access_preload_projection`
- `welcome_notification_projection`
- `personnel_identity_projection`
- `payroll_worker_projection`
- `role_projection`
- `talent_policy_screening`
- `talent_audit_trace`
- `talent_candidate_proof`
- `talent_federation_projection`
- `talent_carbon_schedule_window`
- `talent_pipeline_optimization`
- `talent_interview_allocation`
- `talent_anomaly_signal`
- `talent_candidate_risk_model`
- `talent_hiring_forecast`
- `talent_parsed_instruction`
- `talent_seed_data`
- `talent_schema_extension`
- `talent_control_assertion`
- `talent_governed_model`
- `talent_rule`
- `talent_parameter`
- `talent_configuration`
- `talent_onboarding_appgen_outbox_event`
- `talent_onboarding_appgen_inbox_event`
- `talent_onboarding_dead_letter_event`

### API Routes

- `POST /job-requisitions`
- `POST /job-requisitions/{id}/approvals`
- `POST /candidates`
- `POST /candidates/{id}/stage`
- `POST /interviews`
- `POST /background-checks`
- `POST /offers`
- `POST /offers/{id}/acceptance`
- `POST /onboarding/tasks`
- `POST /onboarding/provision`
- `POST /talent/events/inbox`
- `POST /talent-rules`
- `POST /talent-parameters`
- `POST /talent-configuration`
- `GET /talent-workbench`

### Emitted Events

- `EmployeeProvisioned`
- `CandidateHired`

### Consumed Events

- `RoleChanged`
- `WorkerIdentityVerified`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `talent_onboarding` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `talent_onboarding_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Talent Acquisition and Onboarding` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `talent_onboarding_job_requisition`, `talent_onboarding_job_requisition_approval`, `talent_onboarding_job_requisition_budget`, `talent_onboarding_job_requisition_skill`, `talent_onboarding_sourcing_campaign`, `talent_onboarding_candidate_source`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `EmployeeProvisioned`, `CandidateHired`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `talent_onboarding`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `talent_onboarding_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

