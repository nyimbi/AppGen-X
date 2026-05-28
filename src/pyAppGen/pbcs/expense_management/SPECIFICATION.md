# Expense Management PBC

## Purpose

The `expense_management` PBC is a world-class packaged business capability for Owns expense reports, card transactions, receipts, policy validation, approvals, reimbursements, audit sampling, spend controls, and employee spend intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `expense_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `expense_management_expense_report`: owns expense report lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_line`: owns expense line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_receipt_artifact`: owns receipt artifact lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_card_transaction`: owns card transaction lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_merchant_profile`: owns merchant profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_policy`: owns expense policy lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_policy_violation`: owns policy violation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_approval_task`: owns expense approval task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_reimbursement_batch`: owns reimbursement batch lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_reimbursement_payment`: owns reimbursement payment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_cash_advance`: owns cash advance lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_mileage_claim`: owns mileage claim lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_per_diem_claim`: owns per diem claim lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_audit_sample`: owns expense audit sample lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_duplicate_expense_signal`: owns duplicate expense signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_exception_case`: owns expense exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_policy_rule`: owns expense policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_runtime_parameter`: owns expense runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_schema_extension`: owns expense schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_control_assertion`: owns expense control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_expense_governed_model`: owns expense governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `expense_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `expense_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `expense_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for expense reports: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_expense_report`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_expense_line`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `attach_receipt`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `ingest_card_transaction`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `match_card_receipt`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `validate_expense_policy`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_policy_violation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `route_expense_approval`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `approve_expense_report`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_reimbursement_batch`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `execute_reimbursement`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_cash_advance`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_mileage`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_per_diem`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `sample_expense_audit`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `detect_duplicate_expense`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_expense_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_expense_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- semantic receipt extraction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- probabilistic duplicate detection: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- counterfactual policy coaching: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous spend control testing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- risk-based audit sampling: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- carbon-aware travel expense insights: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `receipt_required_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `merchant_category_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `approval_limit_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `duplicate_detection_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `reimbursement_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `audit_sampling_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `receipt_required_amount`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `auto_approval_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `duplicate_similarity_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `mileage_rate`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `audit_sample_rate`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `expense_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `ExpenseReportCreated`
- `ExpensePolicyViolationOpened`
- `ExpenseApproved`
- `ReimbursementScheduled`
- `ExpenseAuditSampled`
- `DuplicateExpenseDetected`

Consumed events:

- `EmployeeCreated`
- `CardTransactionPosted`
- `PaymentExecuted`
- `PolicyChanged`

Handlers use idempotency keys of the form `expense_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- expense workbench.
- receipt inbox.
- policy violation queue.
- approval board.
- reimbursement console.
- audit sampling panel.
- employee spend analytics.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `expense_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: expense_report, expense_line, receipt_artifact, card_transaction, merchant_profile, expense_policy, policy_violation, expense_approval_task, reimbursement_batch, reimbursement_payment, cash_advance, mileage_claim, per_diem_claim, expense_audit_sample, duplicate_expense_signal, expense_exception_case, expense_policy_rule, expense_runtime_parameter, expense_schema_extension, expense_control_assertion, expense_governed_model
- operations: create_expense_report, capture_expense_line, attach_receipt, ingest_card_transaction, match_card_receipt, validate_expense_policy, open_policy_violation, route_expense_approval, approve_expense_report, create_reimbursement_batch, execute_reimbursement, record_cash_advance, calculate_mileage, calculate_per_diem, sample_expense_audit, detect_duplicate_expense, resolve_expense_exception, compile_expense_rule
- emits: ExpenseReportCreated, ExpensePolicyViolationOpened, ExpenseApproved, ReimbursementScheduled, ExpenseAuditSampled, DuplicateExpenseDetected
- consumes: EmployeeCreated, CardTransactionPosted, PaymentExecuted, PolicyChanged
- rules: receipt_required_policy, merchant_category_policy, approval_limit_policy, duplicate_detection_policy, reimbursement_policy, audit_sampling_policy
- parameters: receipt_required_amount, auto_approval_limit, duplicate_similarity_threshold, mileage_rate, audit_sample_rate, workbench_limit
- advanced_capabilities: semantic receipt extraction, probabilistic duplicate detection, counterfactual policy coaching, continuous spend control testing, risk-based audit sampling, carbon-aware travel expense insights
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: expense_report, expense_line, receipt_document, corporate_card_feed, expense_policy, expense_approval, reimbursement_batch, expense_fraud_signal
- apis: POST /expense-reports, POST /expense-lines, POST /receipt-documents, POST /expense-approvals, GET /expense-workbench
- emits: ExpenseApproved, ExpenseRejected, ReimbursementPrepared, ExpenseFraudFlagged
- consumes: EmployeeProvisioned, PaymentCaptured, AccessPolicyChanged
- ui_fragments: ExpenseManagementWorkbench, ExpenseManagementDetail, ExpenseManagementAssistantPanel
- permissions: expense_management.read, expense_management.create, expense_management.update, expense_management.approve, expense_management.admin
- configuration: EXPENSE_MANAGEMENT_DATABASE_URL, EXPENSE_MANAGEMENT_EVENT_TOPIC, EXPENSE_MANAGEMENT_RETRY_LIMIT, EXPENSE_MANAGEMENT_DEFAULT_POLICY
- standard_features: expense_report_management, expense_management_workflow, expense_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: expense_management_event_sourced_operational_history, expense_management_multi_tenant_policy_isolation, expense_management_schema_evolution_resilience, expense_management_autonomous_anomaly_detection, expense_management_semantic_document_instruction_understanding, expense_management_predictive_risk_scoring, expense_management_counterfactual_scenario_simulation, expense_management_cryptographic_audit_proofs, expense_management_continuous_control_testing, expense_management_carbon_and_sustainability_awareness, expense_management_cross_pbc_event_federation, expense_management_governed_ai_agent_execution
