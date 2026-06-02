# Customer Success Management PBC

## Purpose

The `customer_success_management` PBC is a world-class packaged business capability for Owns customer success accounts, onboarding, touchpoints, adoption, health, playbooks, tasks, escalations, renewals, expansions, executive reviews, and churn-risk intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `customer_success_management_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `customer_success_management_customer_success_account`: owns customer success account lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_plan`: owns success plan lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_onboarding_milestone`: owns onboarding milestone lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_customer_touchpoint`: owns customer touchpoint lifecycle state, channel/outcome evidence, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_adoption_signal`: owns adoption signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_health_score`: owns health score lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_health_score_component`: owns health score component lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_playbook`: owns success playbook lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_playbook_task`: owns playbook task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_customer_escalation`: owns customer escalation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_renewal_motion`: owns renewal motion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_expansion_opportunity`: owns expansion opportunity lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_executive_business_review`: owns executive business review lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_customer_objective`: owns customer objective lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_customer_value_realization`: owns customer value realization lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_churn_risk_signal`: owns churn risk signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_exception_case`: owns success exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_policy_rule`: owns success policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_runtime_parameter`: owns success runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_schema_extension`: owns success schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_control_assertion`: owns success control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_success_governed_model`: owns success governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `customer_success_management_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `customer_success_management_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `customer_success_management_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for customer accounts: intake and creation, touchpoint capture, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_success_account`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_success_plan`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `track_onboarding_milestone`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_touchpoint`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `ingest_adoption_signal`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_health_score`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `explain_health_component`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `launch_playbook`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `complete_playbook_task`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_customer_escalation`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `start_renewal_motion`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `identify_expansion_opportunity`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `prepare_executive_review`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_customer_objective`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `measure_value_realization`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_churn_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_success_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_success_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_renewal_outcome`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- causal health scoring: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- AI playbook recommendation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- renewal outcome simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic account plan extraction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- value realization forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- customer journey graph intelligence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `health_score_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `playbook_trigger_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `renewal_risk_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `value_realization_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `expansion_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `churn_risk_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `onboarding_sla_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `health_warning_score`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `renewal_notice_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `playbook_task_sla_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `customer_success_management_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `SuccessAccountCreated`
- `CustomerTouchpointLogged`
- `HealthScoreChanged`
- `PlaybookLaunched`
- `CustomerEscalationOpened`
- `RenewalMotionStarted`
- `ChurnRiskChanged`

Consumed events:

- `CustomerUpdated`
- `SubscriptionActivated`
- `TicketClosed`
- `PaymentFailed`

Handlers use idempotency keys of the form `customer_success_management:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- customer success workbench.
- touchpoint timeline.
- health cockpit.
- onboarding tracker.
- playbook board.
- renewal room.
- executive review builder.
- churn risk panel.

The UI exposes operational queues, detail panels, touchpoint timelines, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `customer_success_management_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: customer_success_account, success_plan, onboarding_milestone, customer_touchpoint, adoption_signal, health_score, health_score_component, success_playbook, playbook_task, customer_escalation, renewal_motion, expansion_opportunity, executive_business_review, customer_objective, customer_value_realization, churn_risk_signal, success_exception_case, success_policy_rule, success_runtime_parameter, success_schema_extension, success_control_assertion, success_governed_model
- operations: create_success_account, create_success_plan, track_onboarding_milestone, record_touchpoint, ingest_adoption_signal, calculate_health_score, explain_health_component, launch_playbook, complete_playbook_task, open_customer_escalation, start_renewal_motion, identify_expansion_opportunity, prepare_executive_review, record_customer_objective, measure_value_realization, score_churn_risk, resolve_success_exception, compile_success_rule, simulate_renewal_outcome
- emits: SuccessAccountCreated, CustomerTouchpointLogged, HealthScoreChanged, PlaybookLaunched, CustomerEscalationOpened, RenewalMotionStarted, ChurnRiskChanged
- consumes: CustomerUpdated, SubscriptionActivated, TicketClosed, PaymentFailed
- rules: health_score_policy, playbook_trigger_policy, renewal_risk_policy, escalation_policy, value_realization_policy, expansion_policy
- parameters: churn_risk_threshold, onboarding_sla_days, health_warning_score, renewal_notice_days, playbook_task_sla_hours, workbench_limit
- advanced_capabilities: causal health scoring, AI playbook recommendation, renewal outcome simulation, semantic account plan extraction, value realization forecasting, customer journey graph intelligence
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: customer_success_account, customer_health_score, onboarding_plan, adoption_signal, renewal_plan, expansion_signal, success_playbook, churn_risk_case
- apis: POST /success-accounts, POST /health-scores, POST /onboarding-plans, POST /renewal-plans, GET /customer-success-workbench
- emits: CustomerHealthChanged, RenewalPlanCreated, ExpansionSignalDetected, ChurnRiskRaised
- consumes: CustomerUpdated, SubscriptionRenewed, ServiceTicketResolved
- ui_fragments: CustomerSuccessManagementWorkbench, CustomerSuccessManagementDetail, CustomerSuccessManagementAssistantPanel
- permissions: customer_success_management.read, customer_success_management.create, customer_success_management.update, customer_success_management.approve, customer_success_management.admin
- configuration: CUSTOMER_SUCCESS_MANAGEMENT_DATABASE_URL, CUSTOMER_SUCCESS_MANAGEMENT_EVENT_TOPIC, CUSTOMER_SUCCESS_MANAGEMENT_RETRY_LIMIT, CUSTOMER_SUCCESS_MANAGEMENT_DEFAULT_POLICY
- standard_features: customer_success_account_management, customer_success_management_workflow, customer_success_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: customer_success_management_event_sourced_operational_history, customer_success_management_multi_tenant_policy_isolation, customer_success_management_schema_evolution_resilience, customer_success_management_autonomous_anomaly_detection, customer_success_management_semantic_document_instruction_understanding, customer_success_management_predictive_risk_scoring, customer_success_management_counterfactual_scenario_simulation, customer_success_management_cryptographic_audit_proofs, customer_success_management_continuous_control_testing, customer_success_management_carbon_and_sustainability_awareness, customer_success_management_cross_pbc_event_federation, customer_success_management_governed_ai_agent_execution
