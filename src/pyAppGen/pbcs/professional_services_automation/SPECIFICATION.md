# Professional Services Automation PBC

## Purpose

The `professional_services_automation` PBC is a world-class packaged business capability for Owns services engagements, statements of work, staffing, skills, time, milestones, delivery risks, project financials, billing readiness, utilization, and margin controls. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `professional_services_automation_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `professional_services_automation_engagement`: owns engagement lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_statement_of_work`: owns statement of work lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_engagement_role`: owns engagement role lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_consultant_skill_profile`: owns consultant skill profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_staffing_request`: owns staffing request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_staffing_assignment`: owns staffing assignment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_time_entry`: owns time entry lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_expense_link`: owns expense link lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_milestone`: owns milestone lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_deliverable`: owns deliverable lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_billing_schedule`: owns billing schedule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_billing_readiness_check`: owns billing readiness check lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_utilization_snapshot`: owns utilization snapshot lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_margin_forecast`: owns margin forecast lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_delivery_risk`: owns delivery risk lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_client_acceptance`: owns client acceptance lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_engagement_exception_case`: owns engagement exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_psa_policy_rule`: owns psa policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_psa_runtime_parameter`: owns psa runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_psa_schema_extension`: owns psa schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_psa_control_assertion`: owns psa control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_psa_governed_model`: owns psa governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `professional_services_automation_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `professional_services_automation_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `professional_services_automation_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for engagements: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_engagement`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_statement_of_work`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_engagement_role`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_skill_profile`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_staffing_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_staff`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_time_entry`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `link_expense`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_milestone`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `submit_deliverable`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_billing_schedule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_billing_readiness`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_utilization`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `forecast_margin`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_delivery_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_client_acceptance`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_engagement_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_psa_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_margin_leakage`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- skills-based staffing optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- margin leakage prediction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic statement-of-work extraction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- billing readiness controls: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- delivery-risk simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- consultant utilization forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `staffing_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `time_entry_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `billing_readiness_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `margin_threshold_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `milestone_acceptance_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `utilization_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `target_utilization_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `minimum_margin_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `time_submission_sla_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `billing_cutoff_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `risk_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `professional_services_automation_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `EngagementCreated`
- `StaffingAssigned`
- `TimeEntryCaptured`
- `MilestoneCompleted`
- `BillingReady`
- `DeliveryRiskChanged`

Consumed events:

- `EmployeeCreated`
- `ExpenseApproved`
- `InvoiceIssued`
- `PolicyChanged`

Handlers use idempotency keys of the form `professional_services_automation:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- engagement workbench.
- staffing board.
- time and expense console.
- milestone tracker.
- billing readiness queue.
- utilization cockpit.
- margin risk panel.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `professional_services_automation_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: engagement, statement_of_work, engagement_role, consultant_skill_profile, staffing_request, staffing_assignment, time_entry, expense_link, milestone, deliverable, billing_schedule, billing_readiness_check, utilization_snapshot, margin_forecast, delivery_risk, client_acceptance, engagement_exception_case, psa_policy_rule, psa_runtime_parameter, psa_schema_extension, psa_control_assertion, psa_governed_model
- operations: create_engagement, register_statement_of_work, define_engagement_role, record_skill_profile, open_staffing_request, assign_staff, capture_time_entry, link_expense, track_milestone, submit_deliverable, create_billing_schedule, run_billing_readiness, calculate_utilization, forecast_margin, score_delivery_risk, record_client_acceptance, resolve_engagement_exception, compile_psa_rule, simulate_margin_leakage
- emits: EngagementCreated, StaffingAssigned, TimeEntryCaptured, MilestoneCompleted, BillingReady, DeliveryRiskChanged
- consumes: EmployeeCreated, ExpenseApproved, InvoiceIssued, PolicyChanged
- rules: staffing_policy, time_entry_policy, billing_readiness_policy, margin_threshold_policy, milestone_acceptance_policy, utilization_policy
- parameters: target_utilization_percent, minimum_margin_percent, time_submission_sla_hours, billing_cutoff_days, risk_threshold, workbench_limit
- advanced_capabilities: skills-based staffing optimization, margin leakage prediction, semantic statement-of-work extraction, billing readiness controls, delivery-risk simulation, consultant utilization forecasting
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: client_engagement, statement_of_work, engagement_staffing, delivery_milestone, billable_time_entry, billing_milestone, utilization_snapshot, engagement_margin
- apis: POST /engagements, POST /statements-of-work, POST /staffing, POST /billing-milestones, GET /services-automation-workbench
- emits: EngagementOpened, BillingMilestoneReady, UtilizationMeasured, EngagementMarginUpdated
- consumes: ContractApproved, TimeSubmitted, InvoiceIssued
- ui_fragments: ProfessionalServicesAutomationWorkbench, ProfessionalServicesAutomationDetail, ProfessionalServicesAutomationAssistantPanel
- permissions: professional_services_automation.read, professional_services_automation.create, professional_services_automation.update, professional_services_automation.approve, professional_services_automation.admin
- configuration: PROFESSIONAL_SERVICES_AUTOMATION_DATABASE_URL, PROFESSIONAL_SERVICES_AUTOMATION_EVENT_TOPIC, PROFESSIONAL_SERVICES_AUTOMATION_RETRY_LIMIT, PROFESSIONAL_SERVICES_AUTOMATION_DEFAULT_POLICY
- standard_features: client_engagement_management, professional_services_automation_workflow, professional_services_automation_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: professional_services_automation_event_sourced_operational_history, professional_services_automation_multi_tenant_policy_isolation, professional_services_automation_schema_evolution_resilience, professional_services_automation_autonomous_anomaly_detection, professional_services_automation_semantic_document_instruction_understanding, professional_services_automation_predictive_risk_scoring, professional_services_automation_counterfactual_scenario_simulation, professional_services_automation_cryptographic_audit_proofs, professional_services_automation_continuous_control_testing, professional_services_automation_carbon_and_sustainability_awareness, professional_services_automation_cross_pbc_event_federation, professional_services_automation_governed_ai_agent_execution
