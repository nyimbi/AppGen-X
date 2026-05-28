# Grant and Fund Accounting PBC

## Purpose

The `grant_fund_accounting` PBC is a world-class packaged business capability for Owns grant awards, fund restrictions, budgets, allowable costs, draws, match requirements, reporting milestones, compliance evidence, and funder-ready accounting controls. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `grant_fund_accounting_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `grant_fund_accounting_grant_award`: owns grant award lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_fund`: owns grant fund lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_fund_restriction`: owns fund restriction lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_budget`: owns grant budget lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_budget_line`: owns grant budget line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_allowable_cost_rule`: owns allowable cost rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_cost_transaction`: owns grant cost transaction lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_cost_allocation`: owns cost allocation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_drawdown_request`: owns drawdown request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_drawdown_receipt`: owns drawdown receipt lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_match_requirement`: owns match requirement lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_match_contribution`: owns match contribution lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_funder_report`: owns funder report lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_reporting_milestone`: owns reporting milestone lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_compliance_evidence`: owns compliance evidence lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_closeout`: owns grant closeout lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_exception_case`: owns grant exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_policy_rule`: owns grant policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_runtime_parameter`: owns grant runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_schema_extension`: owns grant schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_control_assertion`: owns grant control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_grant_governed_model`: owns grant governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `grant_fund_accounting_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `grant_fund_accounting_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `grant_fund_accounting_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for grant awards: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_grant_award`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_fund_restriction`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_grant_budget`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_budget_line`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_allowable_cost_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_grant_cost`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_cost_allocation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `prepare_drawdown_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_drawdown_receipt`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_match_requirement`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_match_contribution`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_funder_report`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_reporting_milestone`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `attach_compliance_evidence`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `close_grant`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_grant_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_grant_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_funding_shortfall`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- restriction-aware cost validation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- drawdown cash simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic award document extraction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous funder compliance testing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic evidence packet: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- multi-funder portfolio forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `allowable_cost_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `drawdown_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `match_requirement_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `reporting_deadline_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `fund_restriction_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `closeout_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `drawdown_lead_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `match_warning_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `reporting_warning_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `cost_materiality_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `retention_years`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `grant_fund_accounting_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `GrantAwardCreated`
- `GrantBudgetApproved`
- `GrantCostRecorded`
- `DrawdownRequested`
- `FunderReportSubmitted`
- `GrantExceptionOpened`

Consumed events:

- `JournalPosted`
- `PaymentExecuted`
- `PolicyChanged`
- `AuditProofGenerated`

Handlers use idempotency keys of the form `grant_fund_accounting:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- grant accounting workbench.
- fund restriction ledger.
- budget control board.
- drawdown console.
- match tracker.
- funder report room.
- closeout checklist.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `grant_fund_accounting_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: grant_award, grant_fund, fund_restriction, grant_budget, grant_budget_line, allowable_cost_rule, grant_cost_transaction, cost_allocation, drawdown_request, drawdown_receipt, match_requirement, match_contribution, funder_report, reporting_milestone, compliance_evidence, grant_closeout, grant_exception_case, grant_policy_rule, grant_runtime_parameter, grant_schema_extension, grant_control_assertion, grant_governed_model
- operations: create_grant_award, define_fund_restriction, open_grant_budget, capture_budget_line, register_allowable_cost_rule, record_grant_cost, run_cost_allocation, prepare_drawdown_request, record_drawdown_receipt, track_match_requirement, record_match_contribution, build_funder_report, track_reporting_milestone, attach_compliance_evidence, close_grant, resolve_grant_exception, compile_grant_rule, simulate_funding_shortfall
- emits: GrantAwardCreated, GrantBudgetApproved, GrantCostRecorded, DrawdownRequested, FunderReportSubmitted, GrantExceptionOpened
- consumes: JournalPosted, PaymentExecuted, PolicyChanged, AuditProofGenerated
- rules: allowable_cost_policy, drawdown_policy, match_requirement_policy, reporting_deadline_policy, fund_restriction_policy, closeout_policy
- parameters: drawdown_lead_days, match_warning_threshold, reporting_warning_days, cost_materiality_threshold, retention_years, workbench_limit
- advanced_capabilities: restriction-aware cost validation, drawdown cash simulation, semantic award document extraction, continuous funder compliance testing, cryptographic evidence packet, multi-funder portfolio forecasting
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: grant_award, fund_restriction, grant_budget, donor_rule, allowable_cost, reimbursement_claim, grant_compliance_report, fund_audit_trail
- apis: POST /grant-awards, POST /fund-restrictions, POST /grant-budgets, POST /reimbursement-claims, GET /grant-fund-workbench
- emits: GrantAwarded, ReimbursementClaimPrepared, FundRestrictionApplied, GrantComplianceReported
- consumes: JournalPosted, ExpenseApproved, PaymentCaptured
- ui_fragments: GrantFundAccountingWorkbench, GrantFundAccountingDetail, GrantFundAccountingAssistantPanel
- permissions: grant_fund_accounting.read, grant_fund_accounting.create, grant_fund_accounting.update, grant_fund_accounting.approve, grant_fund_accounting.admin
- configuration: GRANT_FUND_ACCOUNTING_DATABASE_URL, GRANT_FUND_ACCOUNTING_EVENT_TOPIC, GRANT_FUND_ACCOUNTING_RETRY_LIMIT, GRANT_FUND_ACCOUNTING_DEFAULT_POLICY
- standard_features: grant_award_management, grant_fund_accounting_workflow, grant_fund_accounting_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: grant_fund_accounting_event_sourced_operational_history, grant_fund_accounting_multi_tenant_policy_isolation, grant_fund_accounting_schema_evolution_resilience, grant_fund_accounting_autonomous_anomaly_detection, grant_fund_accounting_semantic_document_instruction_understanding, grant_fund_accounting_predictive_risk_scoring, grant_fund_accounting_counterfactual_scenario_simulation, grant_fund_accounting_cryptographic_audit_proofs, grant_fund_accounting_continuous_control_testing, grant_fund_accounting_carbon_and_sustainability_awareness, grant_fund_accounting_cross_pbc_event_federation, grant_fund_accounting_governed_ai_agent_execution
