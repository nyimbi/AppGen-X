# Court Case Management PBC

## Purpose

The `court_case_management` PBC is the packaged business capability for trial-court intake and operations. It exists so a composed application can run court case intake, filing review, evidence lodging, hearings, docket chronology, orders, tasks, release evidence, and governed assistant workflows without leaning on shared foreign court tables. The package is intentionally side-effect-free at registration time and keeps discovery, registration, and runtime evidence inside the package boundary.

## Stable Identity

- PBC key: `court_case_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/court_case_management`.
- Runtime entrypoint: `court_case_management_runtime_capabilities()`.
- Standalone entrypoint: `CourtCaseManagementStandaloneApplication` in `standalone.py`.
- UI entrypoint: `court_case_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()` and `package_discovery_plan()`.
- Eventing standard: fixed AppGen-X outbox, inbox, and dead-letter contract.
- Supported ordinary backends: PostgreSQL, MySQL, and MariaDB.

## Owned Boundary, Schema, Migration, And Model Generation

Owned business tables include `court_case_management_court_case`, `court_case_management_filing`, `court_case_management_evidence_item`, `court_case_management_hearing`, `court_case_management_case_task`, `court_case_management_docket_entry`, `court_case_management_party`, `court_case_management_judgment`, and `court_case_management_court_order`. Governance and platform tables remain `court_case_management_court_case_management_policy_rule`, `court_case_management_court_case_management_runtime_parameter`, `court_case_management_court_case_management_schema_extension`, `court_case_management_court_case_management_control_assertion`, `court_case_management_court_case_management_governed_model`, `court_case_management_appgen_outbox_event`, `court_case_management_appgen_inbox_event`, and `court_case_management_appgen_dead_letter_event`.

Schema generation stays package-local. `runtime.py` materializes the schema contract, migration list, and model contract metadata. `migrations/001_initial.sql` is the materialized migration artifact. `models.py` exposes generated model contracts from the runtime schema contract. The package does not mutate shared or foreign tables; collaboration happens through API contracts, projections, and AppGen-X events.

## Service, API, Route, Command, And Query Surface

The service layer exposes command and query operations. Commands include case intake, party registration, filing intake, evidence intake, hearing scheduling, task creation and completion, order drafting, and order entry. Queries include workbench and case-detail views. `services.py` exposes both the contract service surface and a standalone service wrapper.

API and route evidence lives in `routes.py`. Key routes are `POST /court-cases`, `POST /filings`, `POST /evidence`, `POST /hearings`, `POST /tasks`, `POST /tasks/complete`, `POST /court-orders`, `POST /court-orders/enter`, `POST /docket-entrys`, `POST /partys`, and `GET /court-case-management-workbench`. The package distinguishes command paths from query paths and keeps route dispatch side-effect-free until an explicit standalone application instance executes the request.

## Events, Handlers, Outbox, Inbox, Dead-Letter, Idempotency, And Retry

The event contract is AppGen-X. Emitted events are `CourtCaseManagementCreated`, `CourtCaseManagementUpdated`, `CourtCaseManagementApproved`, and `CourtCaseManagementExceptionOpened`. Consumed events are `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`. The package records outbox, inbox, and dead-letter evidence. Handlers preserve idempotency, reject unexpected events into the dead-letter table, and retain retry policy evidence. This package treats idempotent event handling and retry evidence as first-class release requirements.

## UI, Workbench, Permissions, And RBAC

The UI includes `CourtCaseManagementWorkbench`, `CourtCaseManagementDetail`, and `CourtCaseManagementAssistantPanel`. The workbench organizes clerk deficiency queues, accepted filings, evidence review, chambers order review, courtroom calendar, pending tasks, restricted items, and open cases. The detail view provides a chronological timeline for filings, evidence, hearings, orders, tasks, and docket entries.

Permissions and RBAC are package-local. The standard permission set is `court_case_management.read`, `court_case_management.create`, `court_case_management.update`, `court_case_management.approve`, and `court_case_management.admin`. Controls enforce docket chronology, signed-order entry, evidence custody, judge and courtroom scheduling, task completion authority, and sealed-record access.

## Rules, Parameters, Configuration, And Governance

Rules, parameters, and configuration are explicit package artifacts. Rule evidence includes case-numbering, filing-deficiency, evidence, hearing, and task policy. Parameter evidence includes workbench limits, deficiency review windows, hearing buffers, and evidence review windows. Configuration includes `COURT_CASE_MANAGEMENT_DATABASE_URL`, `COURT_CASE_MANAGEMENT_EVENT_TOPIC`, `COURT_CASE_MANAGEMENT_RETRY_LIMIT`, and `COURT_CASE_MANAGEMENT_DEFAULT_POLICY`. Governance hooks live in `config.py`, `permissions.py`, and `seed_data.py`, and the package keeps validation, compile-rule, evaluate-rule, permission manifests, and seed plans executable.

## Agent, Assistant, Chatbot, Skill, Document, Instruction, CRUD, Datastore, And Mutation Surface

`agent.py` contributes governed assistant skills for filing triage, hearing preparation, and order follow-up. The assistant or chatbot surface accepts a document plus instruction, maps the request to a court-specific skill, and produces a governed CRUD datastore mutation preview. Mutations always require human confirmation. Document and instruction intake is constrained to package-owned tables, and foreign-table mutation attempts are rejected.

## Side-Effect-Free Registration, Discovery, Standard Capabilities, Advanced Capabilities, Release Evidence, Tests, And Seed Data

The package keeps self-registration, package metadata, and discovery side-effect-free. `implementation_contract()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` exist so tooling can register or discover the PBC without mutating external systems. Standard capabilities include workflow support, analytics, configuration schema, rule engine, parameter engine, owned schema migrations and models, AppGen-X outbox and inbox eventing, idempotent handlers, retry dead-letter evidence, permissions, seed data, workbench, agentic document instruction intake, governed datastore CRUD, AI agent task assistance, configuration workbench, continuous release assurance, single-PBC domain app, forms, wizards, and controls. Advanced capabilities include event sourced operational history, multi-tenant policy isolation, schema evolution resilience, autonomous anomaly detection, semantic document instruction understanding, predictive risk scoring, counterfactual scenario simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI agent execution.

Release evidence is bundled through `release_evidence.py`, `RELEASE_EVIDENCE.md`, focused standalone audits, package tests, and runtime smoke evidence. Seed data stays local to `seed_data.py` and is referenced explicitly in release evidence and validation.

## Manifest Traceability Appendix

- `tables`: `court_case`, `filing`, `hearing`, `docket_entry`, `party`, `judgment`, `court_order`, `court_case_management_policy_rule`, `court_case_management_runtime_parameter`, `court_case_management_schema_extension`, `court_case_management_control_assertion`, `court_case_management_governed_model`, `evidence_item`, `case_task`
- `apis`: `POST /court-cases`, `POST /filings`, `POST /hearings`, `POST /docket-entrys`, `POST /partys`, `GET /court-case-management-workbench`, `POST /evidence`, `POST /tasks`, `POST /tasks/complete`
- `emits`: `CourtCaseManagementCreated`, `CourtCaseManagementUpdated`, `CourtCaseManagementApproved`, `CourtCaseManagementExceptionOpened`
- `consumes`: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`
- `ui_fragments`: `CourtCaseManagementWorkbench`, `CourtCaseManagementDetail`, `CourtCaseManagementAssistantPanel`
- `permissions`: `court_case_management.read`, `court_case_management.create`, `court_case_management.update`, `court_case_management.approve`, `court_case_management.admin`
- `configuration`: `COURT_CASE_MANAGEMENT_DATABASE_URL`, `COURT_CASE_MANAGEMENT_EVENT_TOPIC`, `COURT_CASE_MANAGEMENT_RETRY_LIMIT`, `COURT_CASE_MANAGEMENT_DEFAULT_POLICY`
- `standard_features`: `court_case_management`, `court_case_management_workflow`, `court_case_management_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `owned_schema_migrations_models`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `permissions`, `seed_data`, `workbench`, `agentic_document_instruction_intake`, `governed_datastore_crud`, `ai_agent_task_assistance`, `configuration_workbench`, `continuous_release_assurance`, `single_pbc_domain_app`, `forms`, `wizards`, `controls`
- `advanced_capabilities`: `court_case_management_event_sourced_operational_history`, `court_case_management_multi_tenant_policy_isolation`, `court_case_management_schema_evolution_resilience`, `court_case_management_autonomous_anomaly_detection`, `court_case_management_semantic_document_instruction_understanding`, `court_case_management_predictive_risk_scoring`, `court_case_management_counterfactual_scenario_simulation`, `court_case_management_cryptographic_audit_proofs`, `court_case_management_continuous_control_testing`, `court_case_management_carbon_and_sustainability_awareness`, `court_case_management_cross_pbc_event_federation`, `court_case_management_governed_ai_agent_execution`
- `docs`: `README.md`, `implementation-plan.md`, `implementation-status.md`, `RELEASE_EVIDENCE.md`, `SPECIFICATION.md`
- `tests`: `tests/test_contract.py`, `tests/test_court_operations_app.py`, `tests/test_standalone.py`
