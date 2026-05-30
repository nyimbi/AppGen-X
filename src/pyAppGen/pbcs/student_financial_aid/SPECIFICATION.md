# Student Financial Aid PBC

## Purpose

The `student_financial_aid` package is an executable packaged business capability for aid-year setup, student aid profile intake, FAFSA/ISIR-equivalent application capture, dependency and verification review, satisfactory academic progress, cost-of-attendance budgeting, need analysis, award packaging, disbursement scheduling, refund and return controls, overaward handling, professional judgment, appeals, compliance, communications, and governed assistant previews. The package owns its schema, migration, models, services, API routes, AppGen-X event contract, handlers, workbench/UI metadata, permissions, configuration hooks, seed plan, tests, side-effect-free registration, and release evidence.

## Stable Identity

- PBC key: `student_financial_aid`
- Mesh: `finops`
- Package directory: `src/pyAppGen/pbcs/student_financial_aid`
- Runtime entrypoint: `student_financial_aid_runtime_capabilities()`
- Package registration entrypoint: `implementation_contract()`
- Event contract: AppGen-X only
- Allowed database backends: PostgreSQL, MySQL, MariaDB
- Stream engine picker: always hidden and forbidden

This PBC is intentionally self-contained. It does not write foreign or shared tables, and it does not require edits to global generation or language modules to function.

## Owned Table Boundary

The package owns the following database-backed artifacts and treats them as the only mutation targets for commands, routes, and assistant CRUD previews:

- `student_financial_aid_aid_year`
- `student_financial_aid_student_aid_profile`
- `student_financial_aid_aid_application`
- `student_financial_aid_dependency_review`
- `student_financial_aid_verification_item`
- `student_financial_aid_document_artifact`
- `student_financial_aid_sap_evaluation`
- `student_financial_aid_cost_of_attendance_budget`
- `student_financial_aid_need_analysis`
- `student_financial_aid_award_package`
- `student_financial_aid_award_line`
- `student_financial_aid_scholarship_resource`
- `student_financial_aid_grant_eligibility`
- `student_financial_aid_loan_offer`
- `student_financial_aid_work_study_plan`
- `student_financial_aid_disbursement_schedule`
- `student_financial_aid_refund_return_case`
- `student_financial_aid_overaward_case`
- `student_financial_aid_professional_judgment_case`
- `student_financial_aid_aid_appeal`
- `student_financial_aid_aid_compliance_obligation`
- `student_financial_aid_communication_log`
- `student_financial_aid_policy_rule`
- `student_financial_aid_runtime_parameter`
- `student_financial_aid_schema_extension`
- `student_financial_aid_control_assertion`
- `student_financial_aid_governed_model`
- `student_financial_aid_appgen_outbox_event`
- `student_financial_aid_appgen_inbox_event`
- `student_financial_aid_appgen_dead_letter_event`

Shared or foreign tables are explicitly out of scope. Cross-PBC collaboration is represented only through declared APIs, event consumption, or read-only projection dependencies.

## Schema, Migrations, and Models

`migrations/001_initial.sql` defines the complete owned schema. Every table uses a consistent owned-record envelope with identity, tenant boundary, aid-year reference, subject references, status, lifecycle stage, amount, currency, JSON payload, and timestamps. The schema contract and model contract are generated from the same owned table list in `slice_app.py`, so the migration, schema, service, and UI surfaces remain aligned.

The package-local model contract is intentionally simple. It exposes one model artifact per owned table and keeps field shapes stable for generation, audit, and smoke coverage. This is enough for database-backed contract artifacts and source ownership evidence without expanding into a shared ORM layer.

## Command and Query Services

The service surface exposes explicit command and query operations. Major commands include aid year setup, student aid profile creation, aid application intake, dependency and verification review, document registration, sap evaluation, cost-of-attendance capture, need analysis, award packaging, disbursement scheduling, refund and return review, professional judgment submission, appeal recording, compliance obligation tracking, and communication logging.

Each command stays inside the owned datastore plus outbox boundary. Queries expose workbench summaries and build workbench metadata from the same owned records. Service contracts describe operation kind, transaction boundary, event contract, and table scope. API route contracts map stable HTTP-style endpoints onto that same service surface.

## Events, Inbox/Outbox, Idempotency, and Retry

AppGen-X is the only event contract. The package emits:

- `StudentFinancialAidCreated`
- `StudentFinancialAidUpdated`
- `StudentFinancialAidApproved`
- `StudentFinancialAidExceptionOpened`

The package consumes:

- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

The handler layer requires idempotency keys, suppresses duplicates, and sends unexpected event types to the dead-letter table with retry metadata. This means event handling, outbox evidence, inbox evidence, dead-letter evidence, and retry posture are all visible to audits.

## Rules, Parameters, and Configuration

Rules are explicit compiled artifacts, not hidden behavior. The package defines policies for aid-year controls, dependency review, verification resolution, sap, need analysis, packaging, disbursement, return of funds, professional judgment, appeals, and compliance. Parameters such as workbench limits, verification deadlines, sap thresholds, loan caps, work-study caps, packaging buffers, and communication SLAs are bounded and editable through configuration contracts.

Configuration stays bounded as well. The package validates database backend selection against PostgreSQL, MySQL, and MariaDB only. It enforces the AppGen-X topic, never exposes a stream picker, and keeps side effects out of package discovery and metadata validation.

## UI, Workbench, Permissions, and Controls

The workbench is organized around real student-aid operations instead of placeholder boards. Navigation sections cover aid-year setup, intake and verification, need and packaging, disbursement and returns, appeals and compliance, agent assistance, and release evidence. Forms, wizards, and controls are all package-owned and aligned with the core workflows.

UI fragments include `StudentFinancialAidWorkbench`, `StudentFinancialAidDetail`, and `StudentFinancialAidAssistantPanel`. Permissions and RBAC are explicit: read, create, update, approve, admin, and operate. Controls include rule editors, parameter editors, an award matrix preview, a disbursement gate checklist, an event replay console, and an assistant mutation guard.

## Agent and Assistant Skills

The package contributes a governed assistant skill namespace. The assistant can guide users, read records, plan document changes, preview mutations, explain need analysis, and preview disbursement readiness. Document instruction intake is semantically aware of dependency, tax, sap, and appeal language, but it never mutates data directly. Instead it returns a mutation preview, candidate owned tables, extracted fields, and a requirement for human confirmation.

This means the package satisfies agent, assistant, chatbot, skill, document, datastore, CRUD, and mutation-preview requirements without expanding beyond owned boundaries.

## Side-Effect-Free Registration and Release Readiness

`register_pbc()`, `registration_plan()`, `package_metadata_manifest()`, and `validate_package_metadata()` keep discovery and registration side-effect free. The source package advertises its implementation directory, artifacts, docs, tests, capabilities, standard features, advanced features, and AppGen-X posture without mutating global registries during validation.

Release readiness is driven by three local audits:

- `pbc_source_artifact_contract`
- `pbc_implementation_release_audit`
- `pbc_generation_smoke_audit`

These audits confirm source artifact presence, owned schema and migration integrity, service and route coherence, event and handler posture, UI/workbench coverage, governed assistant previews, and generated model/route evidence.

## Standard and Advanced Capability Coverage

Standard capabilities include aid year setup, profile management, FAFSA/ISIR-equivalent intake, dependency review, verification tracking, document tracking, sap monitoring, cost-of-attendance budgeting, need analysis, award packaging, scholarship/grant/loan/work-study management, disbursement and return controls, professional judgment and appeals, compliance and communications, rules, parameters, configuration, workbench, permissions, seed data, and continuous release assurance.

Advanced capabilities include event-sourced operational history, multi-tenant policy isolation, schema evolution resilience, anomaly detection, semantic document understanding, predictive risk scoring, counterfactual packaging simulation, cryptographic audit proofs, continuous control testing, carbon awareness, cross-PBC federation through AppGen-X, and governed AI agent execution.

## Tests and Evidence

Focused tests cover schema, service, release evidence, package metadata, route dispatch, governance, event idempotency, the standalone slice app workflow bundle, and external runtime compatibility through `tests/test_pbc_student_financial_aid_runtime.py`. Seed planning is package-local. Release evidence and implementation status record the exact verification commands and outcomes.

## Manifest Traceability Appendix

Legacy catalog compatibility values retained for audit traceability:

- tables: aid_application, eligibility_review, award_package, verification_item, disbursement, sap_status, aid_compliance, student_financial_aid_policy_rule, student_financial_aid_runtime_parameter, student_financial_aid_schema_extension, student_financial_aid_control_assertion, student_financial_aid_governed_model
- apis: POST /aid-applications, POST /eligibility-reviews, POST /award-packages, POST /verification-items, POST /disbursements, GET /student-financial-aid-workbench
- emits: StudentFinancialAidCreated, StudentFinancialAidUpdated, StudentFinancialAidApproved, StudentFinancialAidExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- ui_fragments: StudentFinancialAidWorkbench, StudentFinancialAidDetail, StudentFinancialAidAssistantPanel
- permissions: student_financial_aid.read, student_financial_aid.create, student_financial_aid.update, student_financial_aid.approve, student_financial_aid.admin
- configuration: STUDENT_FINANCIAL_AID_DATABASE_URL, STUDENT_FINANCIAL_AID_EVENT_TOPIC, STUDENT_FINANCIAL_AID_RETRY_LIMIT, STUDENT_FINANCIAL_AID_DEFAULT_POLICY
- standard_features: aid_application_management, student_financial_aid_workflow, student_financial_aid_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: student_financial_aid_event_sourced_operational_history, student_financial_aid_multi_tenant_policy_isolation, student_financial_aid_schema_evolution_resilience, student_financial_aid_autonomous_anomaly_detection, student_financial_aid_semantic_document_instruction_understanding, student_financial_aid_predictive_risk_scoring, student_financial_aid_counterfactual_scenario_simulation, student_financial_aid_cryptographic_audit_proofs, student_financial_aid_continuous_control_testing, student_financial_aid_carbon_and_sustainability_awareness, student_financial_aid_cross_pbc_event_federation, student_financial_aid_governed_ai_agent_execution
