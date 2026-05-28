# Project Portfolio Management PBC

## Purpose

The `project_portfolio_management` PBC is a world-class packaged business capability for Owns initiative intake, business cases, portfolio scoring, prioritization, stage gates, dependencies, resources, benefits, risks, and executive portfolio governance. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `project_portfolio_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `project_portfolio_management_portfolio_item`: owns portfolio item lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_program`: owns portfolio program lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_business_case`: owns business case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_score`: owns portfolio score lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_prioritization_run`: owns prioritization run lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_stage_gate`: owns stage gate lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_gate_decision`: owns gate decision lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_project_dependency`: owns project dependency lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_resource_demand`: owns resource demand lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_resource_assignment`: owns resource assignment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_benefit_hypothesis`: owns benefit hypothesis lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_benefit_realization`: owns benefit realization lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_risk`: owns portfolio risk lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_issue`: owns portfolio issue lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_change_request`: owns change request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_financial_snapshot`: owns portfolio financial snapshot lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_exception_case`: owns portfolio exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_policy_rule`: owns portfolio policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_runtime_parameter`: owns portfolio runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_schema_extension`: owns portfolio schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_control_assertion`: owns portfolio control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_portfolio_governed_model`: owns portfolio governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `project_portfolio_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `project_portfolio_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `project_portfolio_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for portfolio items: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `intake_portfolio_item`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_business_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_portfolio_item`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_prioritization`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_stage_gate`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_gate_decision`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `map_dependency`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `forecast_resource_demand`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_resource`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_benefit_hypothesis`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `measure_benefit_realization`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_portfolio_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_portfolio_issue`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `process_change_request`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_financial_snapshot`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_portfolio_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_portfolio_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_portfolio_tradeoff`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- optimization-based prioritization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- counterfactual portfolio tradeoffs: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- dependency graph risk propagation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- benefit realization forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous governance controls: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- AI-assisted business case critique: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `intake_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `scoring_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `stage_gate_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `resource_capacity_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `benefit_tracking_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `change_control_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `minimum_score_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `capacity_buffer_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `gate_warning_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `benefit_materiality_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `change_approval_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `project_portfolio_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `PortfolioItemIntaked`
- `BusinessCaseApproved`
- `PrioritizationPublished`
- `GateDecisionRecorded`
- `BenefitRealizationMeasured`
- `PortfolioExceptionOpened`

Consumed events:

- `BudgetApproved`
- `EmployeeCreated`
- `RiskAssessed`
- `PolicyChanged`

Handlers use idempotency keys of the form `project_portfolio_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- portfolio workbench.
- intake funnel.
- business case canvas.
- prioritization board.
- stage gate console.
- dependency map.
- benefits tracker.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `project_portfolio_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: portfolio_item, portfolio_program, business_case, portfolio_score, prioritization_run, stage_gate, gate_decision, project_dependency, resource_demand, resource_assignment, benefit_hypothesis, benefit_realization, portfolio_risk, portfolio_issue, change_request, portfolio_financial_snapshot, portfolio_exception_case, portfolio_policy_rule, portfolio_runtime_parameter, portfolio_schema_extension, portfolio_control_assertion, portfolio_governed_model
- operations: intake_portfolio_item, create_business_case, score_portfolio_item, run_prioritization, define_stage_gate, record_gate_decision, map_dependency, forecast_resource_demand, assign_resource, define_benefit_hypothesis, measure_benefit_realization, record_portfolio_risk, open_portfolio_issue, process_change_request, publish_financial_snapshot, resolve_portfolio_exception, compile_portfolio_rule, simulate_portfolio_tradeoff
- emits: PortfolioItemIntaked, BusinessCaseApproved, PrioritizationPublished, GateDecisionRecorded, BenefitRealizationMeasured, PortfolioExceptionOpened
- consumes: BudgetApproved, EmployeeCreated, RiskAssessed, PolicyChanged
- rules: intake_policy, scoring_policy, stage_gate_policy, resource_capacity_policy, benefit_tracking_policy, change_control_policy
- parameters: minimum_score_threshold, capacity_buffer_percent, gate_warning_days, benefit_materiality_threshold, change_approval_limit, workbench_limit
- advanced_capabilities: optimization-based prioritization, counterfactual portfolio tradeoffs, dependency graph risk propagation, benefit realization forecasting, continuous governance controls, AI-assisted business case critique
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: portfolio, program, project, project_milestone, project_budget, resource_assignment, project_risk, benefit_realization
- apis: POST /portfolios, POST /programs, POST /projects, POST /milestones, POST /benefits, GET /portfolio-workbench
- emits: ProjectApproved, MilestoneCompleted, ProjectRiskRaised, BenefitRealized
- consumes: BudgetApproved, EmployeeProvisioned, ProcurementApproved
- ui_fragments: ProjectPortfolioManagementWorkbench, ProjectPortfolioManagementDetail, ProjectPortfolioManagementAssistantPanel
- permissions: project_portfolio_management.read, project_portfolio_management.create, project_portfolio_management.update, project_portfolio_management.approve, project_portfolio_management.admin
- configuration: PROJECT_PORTFOLIO_MANAGEMENT_DATABASE_URL, PROJECT_PORTFOLIO_MANAGEMENT_EVENT_TOPIC, PROJECT_PORTFOLIO_MANAGEMENT_RETRY_LIMIT, PROJECT_PORTFOLIO_MANAGEMENT_DEFAULT_POLICY
- standard_features: portfolio_management, project_portfolio_management_workflow, project_portfolio_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: project_portfolio_management_event_sourced_operational_history, project_portfolio_management_multi_tenant_policy_isolation, project_portfolio_management_schema_evolution_resilience, project_portfolio_management_autonomous_anomaly_detection, project_portfolio_management_semantic_document_instruction_understanding, project_portfolio_management_predictive_risk_scoring, project_portfolio_management_counterfactual_scenario_simulation, project_portfolio_management_cryptographic_audit_proofs, project_portfolio_management_continuous_control_testing, project_portfolio_management_carbon_and_sustainability_awareness, project_portfolio_management_cross_pbc_event_federation, project_portfolio_management_governed_ai_agent_execution
