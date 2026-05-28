# Legal Matter Management PBC

## Purpose

The `legal_matter_management` PBC is a world-class packaged business capability for Owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `legal_matter_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `legal_matter_management_legal_matter`: owns legal matter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_party`: owns matter party lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_counsel`: owns matter counsel lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_budget`: owns matter budget lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_budget_line`: owns matter budget line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_legal_hold`: owns legal hold lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_hold_custodian`: owns hold custodian lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_deadline`: owns matter deadline lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_filing_record`: owns filing record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_document`: owns matter document lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_document_privilege_review`: owns document privilege review lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_outside_counsel_invoice`: owns outside counsel invoice lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_task`: owns matter task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_risk_assessment`: owns matter risk assessment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_settlement_offer`: owns settlement offer lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_outcome`: owns matter outcome lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_exception_case`: owns matter exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_policy_rule`: owns matter policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_runtime_parameter`: owns matter runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_schema_extension`: owns matter schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_control_assertion`: owns matter control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_matter_governed_model`: owns matter governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `legal_matter_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `legal_matter_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `legal_matter_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for legal matters: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `open_legal_matter`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_matter_party`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_counsel`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_matter_budget`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_budget_line`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `issue_legal_hold`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_hold_custodian`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_matter_deadline`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_filing`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `attach_matter_document`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `review_document_privilege`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `ingest_counsel_invoice`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_matter_task`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_matter_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_settlement_offer`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `close_matter_outcome`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_matter_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_matter_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_case_exposure`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- legal deadline risk prediction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic document privilege triage: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- case exposure simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- outside counsel spend intelligence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic hold evidence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- policy-aware settlement routing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `matter_intake_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `hold_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `deadline_escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `privilege_review_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `budget_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `settlement_approval_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `deadline_warning_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `budget_warning_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `privilege_review_sla_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `settlement_approval_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `hold_review_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `legal_matter_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `LegalMatterOpened`
- `LegalHoldIssued`
- `MatterDeadlineTracked`
- `FilingRecorded`
- `MatterRiskChanged`
- `MatterClosed`

Consumed events:

- `SupplierQualified`
- `InvoiceCaptured`
- `PolicyChanged`
- `AuditProofGenerated`

Handlers use idempotency keys of the form `legal_matter_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- legal matter workbench.
- matter timeline.
- legal hold console.
- deadline calendar.
- document privilege queue.
- counsel invoice review.
- risk and exposure panel.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `legal_matter_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: legal_matter, matter_party, matter_counsel, matter_budget, matter_budget_line, legal_hold, hold_custodian, matter_deadline, filing_record, matter_document, document_privilege_review, outside_counsel_invoice, matter_task, matter_risk_assessment, settlement_offer, matter_outcome, matter_exception_case, matter_policy_rule, matter_runtime_parameter, matter_schema_extension, matter_control_assertion, matter_governed_model
- operations: open_legal_matter, register_matter_party, assign_counsel, create_matter_budget, capture_budget_line, issue_legal_hold, register_hold_custodian, track_matter_deadline, record_filing, attach_matter_document, review_document_privilege, ingest_counsel_invoice, create_matter_task, score_matter_risk, record_settlement_offer, close_matter_outcome, resolve_matter_exception, compile_matter_rule, simulate_case_exposure
- emits: LegalMatterOpened, LegalHoldIssued, MatterDeadlineTracked, FilingRecorded, MatterRiskChanged, MatterClosed
- consumes: SupplierQualified, InvoiceCaptured, PolicyChanged, AuditProofGenerated
- rules: matter_intake_policy, hold_policy, deadline_escalation_policy, privilege_review_policy, budget_policy, settlement_approval_policy
- parameters: deadline_warning_days, budget_warning_percent, privilege_review_sla_hours, settlement_approval_limit, hold_review_days, workbench_limit
- advanced_capabilities: legal deadline risk prediction, semantic document privilege triage, case exposure simulation, outside counsel spend intelligence, cryptographic hold evidence, policy-aware settlement routing
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: legal_matter, outside_counsel, matter_budget, matter_document, legal_deadline, legal_hold, counsel_invoice, matter_outcome
- apis: POST /legal-matters, POST /outside-counsel, POST /matter-budgets, POST /legal-holds, GET /legal-matter-workbench
- emits: LegalMatterOpened, LegalHoldIssued, MatterBudgetApproved, CounselInvoiceReviewed
- consumes: ContractApproved, InvoiceApproved, RiskAssessed
- ui_fragments: LegalMatterManagementWorkbench, LegalMatterManagementDetail, LegalMatterManagementAssistantPanel
- permissions: legal_matter_management.read, legal_matter_management.create, legal_matter_management.update, legal_matter_management.approve, legal_matter_management.admin
- configuration: LEGAL_MATTER_MANAGEMENT_DATABASE_URL, LEGAL_MATTER_MANAGEMENT_EVENT_TOPIC, LEGAL_MATTER_MANAGEMENT_RETRY_LIMIT, LEGAL_MATTER_MANAGEMENT_DEFAULT_POLICY
- standard_features: legal_matter_management, legal_matter_management_workflow, legal_matter_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: legal_matter_management_event_sourced_operational_history, legal_matter_management_multi_tenant_policy_isolation, legal_matter_management_schema_evolution_resilience, legal_matter_management_autonomous_anomaly_detection, legal_matter_management_semantic_document_instruction_understanding, legal_matter_management_predictive_risk_scoring, legal_matter_management_counterfactual_scenario_simulation, legal_matter_management_cryptographic_audit_proofs, legal_matter_management_continuous_control_testing, legal_matter_management_carbon_and_sustainability_awareness, legal_matter_management_cross_pbc_event_federation, legal_matter_management_governed_ai_agent_execution
