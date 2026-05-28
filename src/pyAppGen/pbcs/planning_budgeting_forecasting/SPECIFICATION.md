# Planning Budgeting and Forecasting PBC

## Purpose

The `planning_budgeting_forecasting` PBC is a world-class packaged business capability for Owns enterprise planning models, budgets, forecasts, scenarios, drivers, assumptions, allocations, approvals, variance explanations, and rolling forecast intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `planning_budgeting_forecasting_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `planning_budgeting_forecasting_planning_model`: owns planning model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_dimension`: owns planning dimension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_version`: owns planning version lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_budget_version`: owns budget version lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_budget_line`: owns budget line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_forecast_cycle`: owns forecast cycle lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_forecast_line`: owns forecast line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_driver_assumption`: owns driver assumption lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_driver_actual`: owns driver actual lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_allocation_rule`: owns allocation rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_allocation_run`: owns allocation run lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_scenario`: owns planning scenario lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_scenario_result`: owns scenario result lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_variance_analysis`: owns variance analysis lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_variance_commentary`: owns variance commentary lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_approval`: owns planning approval lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_task`: owns planning task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_rolling_forecast_snapshot`: owns rolling forecast snapshot lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_plan_lock`: owns plan lock lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_plan_import_batch`: owns plan import batch lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_exception_case`: owns planning exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_policy_rule`: owns planning policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_runtime_parameter`: owns planning runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_schema_extension`: owns planning schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_control_assertion`: owns planning control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_planning_governed_model`: owns planning governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `planning_budgeting_forecasting_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `planning_budgeting_forecasting_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `planning_budgeting_forecasting_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for plans: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_planning_model`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_dimension`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_budget_version`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_budget_line`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `start_forecast_cycle`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_forecast_line`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_driver_assumption`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `ingest_driver_actual`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_allocation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_scenario`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_scenario_result`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `analyze_variance`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `submit_plan_approval`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `lock_plan_version`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_rolling_forecast`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `import_plan_batch`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_planning_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_planning_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_assumption_shock`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- driver-based rolling forecasts: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- counterfactual scenario simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- AI variance explanation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous forecast freshness scoring: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic plan version proof: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- multi-tenant planning model isolation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `budget_approval_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `forecast_refresh_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `allocation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `scenario_governance_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `plan_lock_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `variance_commentary_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `variance_threshold_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `forecast_horizon_months`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `approval_amount_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `allocation_precision`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `scenario_count_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `planning_budgeting_forecasting_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `BudgetVersionOpened`
- `BudgetApproved`
- `ForecastPublished`
- `ScenarioModeled`
- `VarianceFlagged`
- `PlanningExceptionOpened`

Consumed events:

- `TrialBalanceCalculated`
- `RevenueRecognized`
- `DemandForecastPublished`
- `HeadcountChanged`

Handlers use idempotency keys of the form `planning_budgeting_forecasting:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- planning workbench.
- budget version grid.
- forecast cycle board.
- driver assumption studio.
- scenario simulation lab.
- variance commentary panel.
- approval queue.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `planning_budgeting_forecasting_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: planning_model, planning_dimension, planning_version, budget_version, budget_line, forecast_cycle, forecast_line, driver_assumption, driver_actual, allocation_rule, allocation_run, planning_scenario, scenario_result, variance_analysis, variance_commentary, planning_approval, planning_task, rolling_forecast_snapshot, plan_lock, plan_import_batch, planning_exception_case, planning_policy_rule, planning_runtime_parameter, planning_schema_extension, planning_control_assertion, planning_governed_model
- operations: create_planning_model, define_dimension, open_budget_version, capture_budget_line, start_forecast_cycle, capture_forecast_line, register_driver_assumption, ingest_driver_actual, run_allocation, create_scenario, calculate_scenario_result, analyze_variance, submit_plan_approval, lock_plan_version, publish_rolling_forecast, import_plan_batch, resolve_planning_exception, compile_planning_rule, simulate_assumption_shock
- emits: BudgetVersionOpened, BudgetApproved, ForecastPublished, ScenarioModeled, VarianceFlagged, PlanningExceptionOpened
- consumes: TrialBalanceCalculated, RevenueRecognized, DemandForecastPublished, HeadcountChanged
- rules: budget_approval_policy, forecast_refresh_policy, allocation_policy, scenario_governance_policy, plan_lock_policy, variance_commentary_policy
- parameters: variance_threshold_percent, forecast_horizon_months, approval_amount_limit, allocation_precision, scenario_count_limit, workbench_limit
- advanced_capabilities: driver-based rolling forecasts, counterfactual scenario simulation, AI variance explanation, continuous forecast freshness scoring, cryptographic plan version proof, multi-tenant planning model isolation
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: planning_model, budget_version, forecast_cycle, planning_scenario, driver_assumption, allocation_rule, variance_analysis, planning_approval
- apis: POST /plans, POST /budgets, POST /forecasts, POST /scenarios, POST /variance-analyses, GET /planning-workbench
- emits: BudgetApproved, ForecastPublished, ScenarioModeled, VarianceFlagged
- consumes: TrialBalanceCalculated, RevenueRecognized, DemandForecastPublished
- ui_fragments: PlanningBudgetingForecastingWorkbench, PlanningBudgetingForecastingDetail, PlanningBudgetingForecastingAssistantPanel
- permissions: planning_budgeting_forecasting.read, planning_budgeting_forecasting.create, planning_budgeting_forecasting.update, planning_budgeting_forecasting.approve, planning_budgeting_forecasting.admin
- configuration: PLANNING_BUDGETING_FORECASTING_DATABASE_URL, PLANNING_BUDGETING_FORECASTING_EVENT_TOPIC, PLANNING_BUDGETING_FORECASTING_RETRY_LIMIT, PLANNING_BUDGETING_FORECASTING_DEFAULT_POLICY
- standard_features: planning_model_management, planning_budgeting_forecasting_workflow, planning_budgeting_forecasting_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: planning_budgeting_forecasting_event_sourced_operational_history, planning_budgeting_forecasting_multi_tenant_policy_isolation, planning_budgeting_forecasting_schema_evolution_resilience, planning_budgeting_forecasting_autonomous_anomaly_detection, planning_budgeting_forecasting_semantic_document_instruction_understanding, planning_budgeting_forecasting_predictive_risk_scoring, planning_budgeting_forecasting_counterfactual_scenario_simulation, planning_budgeting_forecasting_cryptographic_audit_proofs, planning_budgeting_forecasting_continuous_control_testing, planning_budgeting_forecasting_carbon_and_sustainability_awareness, planning_budgeting_forecasting_cross_pbc_event_federation, planning_budgeting_forecasting_governed_ai_agent_execution
