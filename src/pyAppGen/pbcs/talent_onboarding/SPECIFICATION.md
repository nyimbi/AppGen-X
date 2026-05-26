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
- `candidate`
- `candidate_consent`
- `interview_plan`
- `evaluation_evidence`
- `background_check`
- `offer`
- `onboarding_task`
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
- Candidate capture with source, skills, country, match score, consent, identity, status, and stage.
- Consent management and privacy/retention policy evidence.
- Candidate pipeline from application through screening, interview, offer, hired, rejection, withdrawal, and provisioning.
- Interview plan and evaluation evidence descriptors.
- Background check request, provider validation, result capture, confidence thresholding, adjudication, and adverse-action review evidence.
- Offer creation, compensation projection, expiry policy, acceptance, decline, and blocked-offer evidence.
- Onboarding task generation by role, location, worker type, and jurisdiction.
- Task assignment, due date, completion, exception, and HR/manager review evidence.
- Employee provisioning handoffs for personnel identity, access preload, and welcome notifications.
- Candidate hire events for analytics and downstream workflows.
- Role and worker-identity projection handling through AppGen-X inbox events.
- Source-channel, cycle-time, conversion, hired, provisioned, and task-completion analytics.
- Multi-tenant and multi-entity isolation.
- AppGen-X inbox/outbox idempotency and dead-letter evidence.
- RBAC descriptors for requisition, candidate, offer, onboarding, event, configuration, and audit actions.
- Package-local workbench UI for requisitions, candidates, checks, offers, onboarding tasks, rules, parameters, configuration, and event evidence.

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
