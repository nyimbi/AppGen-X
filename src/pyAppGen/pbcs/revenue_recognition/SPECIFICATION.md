# Revenue Recognition PBC

## Purpose

The `revenue_recognition` PBC is a world-class packaged business capability for Owns revenue contracts, performance obligations, transaction price allocation, modifications, satisfaction events, schedules, holds, adjustments, disclosures, and close-ready revenue evidence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `revenue_recognition_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `revenue_recognition_revenue_contract`: owns revenue contract lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_contract_line`: owns contract line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_performance_obligation`: owns performance obligation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_obligation_satisfaction_event`: owns obligation satisfaction event lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_transaction_price_allocation`: owns transaction price allocation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_variable_consideration_estimate`: owns variable consideration estimate lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_schedule`: owns revenue schedule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_schedule_line`: owns revenue schedule line lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_deferral`: owns revenue deferral lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_entry`: owns revenue recognition entry lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_contract_modification`: owns contract modification lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_standalone_selling_price`: owns standalone selling price lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_hold`: owns revenue hold lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_adjustment`: owns revenue adjustment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_disclosure_packet`: owns disclosure packet lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_close_readiness_check`: owns close readiness check lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_exception_case`: owns revenue exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_policy_rule`: owns revenue policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_runtime_parameter`: owns revenue runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_schema_extension`: owns revenue schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_control_assertion`: owns revenue control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_revenue_governed_model`: owns revenue governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `revenue_recognition_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `revenue_recognition_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `revenue_recognition_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for revenue contracts: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_revenue_contract`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `identify_obligations`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `estimate_variable_consideration`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `allocate_transaction_price`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_satisfaction_event`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `generate_revenue_schedule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `post_recognition_entry`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_deferral`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `process_contract_modification`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `apply_revenue_hold`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_revenue_adjustment`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_disclosure_packet`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_close_readiness_check`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_revenue_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_revenue_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_modification_impact`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- probabilistic variable consideration: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- contract-modification counterfactuals: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous close controls: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic contract obligation extraction: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic recognition proof: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- policy-versioned accounting logic: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `obligation_identification_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `allocation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `variable_consideration_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `revenue_hold_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `close_readiness_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `disclosure_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `materiality_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `variable_consideration_confidence`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `recognition_window_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `close_cutoff_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `disclosure_precision`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `revenue_recognition_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `RevenueContractCreated`
- `PerformanceObligationIdentified`
- `RevenueScheduled`
- `RevenueRecognized`
- `RevenueHoldApplied`
- `DisclosurePacketGenerated`

Consumed events:

- `OrderCompleted`
- `SubscriptionActivated`
- `InvoiceIssued`
- `PolicyChanged`

Handlers use idempotency keys of the form `revenue_recognition:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- revenue contract workbench.
- obligation map.
- allocation board.
- schedule calendar.
- hold and exception queue.
- close readiness console.
- disclosure evidence room.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `revenue_recognition_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: revenue_contract, contract_line, performance_obligation, obligation_satisfaction_event, transaction_price_allocation, variable_consideration_estimate, revenue_schedule, revenue_schedule_line, revenue_deferral, revenue_recognition_entry, contract_modification, standalone_selling_price, revenue_hold, revenue_adjustment, disclosure_packet, close_readiness_check, revenue_exception_case, revenue_policy_rule, revenue_runtime_parameter, revenue_schema_extension, revenue_control_assertion, revenue_governed_model
- operations: create_revenue_contract, identify_obligations, estimate_variable_consideration, allocate_transaction_price, record_satisfaction_event, generate_revenue_schedule, post_recognition_entry, create_deferral, process_contract_modification, apply_revenue_hold, record_revenue_adjustment, build_disclosure_packet, run_close_readiness_check, resolve_revenue_exception, compile_revenue_rule, simulate_modification_impact
- emits: RevenueContractCreated, PerformanceObligationIdentified, RevenueScheduled, RevenueRecognized, RevenueHoldApplied, DisclosurePacketGenerated
- consumes: OrderCompleted, SubscriptionActivated, InvoiceIssued, PolicyChanged
- rules: obligation_identification_policy, allocation_policy, variable_consideration_policy, revenue_hold_policy, close_readiness_policy, disclosure_policy
- parameters: materiality_threshold, variable_consideration_confidence, recognition_window_days, close_cutoff_hours, disclosure_precision, workbench_limit
- advanced_capabilities: probabilistic variable consideration, contract-modification counterfactuals, continuous close controls, semantic contract obligation extraction, cryptographic recognition proof, policy-versioned accounting logic
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: revenue_contract, performance_obligation, transaction_price_allocation, contract_modification, revenue_schedule, revenue_event, compliance_evidence, recognition_policy
- apis: POST /revenue-contracts, POST /performance-obligations, POST /revenue-schedules, POST /recognition-runs, GET /revenue-recognition-workbench
- emits: RevenueRecognized, RevenueScheduleCreated, RecognitionPolicyChanged, ContractModificationAssessed
- consumes: ContractApproved, InvoiceIssued, PaymentCaptured
- ui_fragments: RevenueRecognitionWorkbench, RevenueRecognitionDetail, RevenueRecognitionAssistantPanel
- permissions: revenue_recognition.read, revenue_recognition.create, revenue_recognition.update, revenue_recognition.approve, revenue_recognition.admin
- configuration: REVENUE_RECOGNITION_DATABASE_URL, REVENUE_RECOGNITION_EVENT_TOPIC, REVENUE_RECOGNITION_RETRY_LIMIT, REVENUE_RECOGNITION_DEFAULT_POLICY
- standard_features: revenue_contract_management, revenue_recognition_workflow, revenue_recognition_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: revenue_recognition_event_sourced_operational_history, revenue_recognition_multi_tenant_policy_isolation, revenue_recognition_schema_evolution_resilience, revenue_recognition_autonomous_anomaly_detection, revenue_recognition_semantic_document_instruction_understanding, revenue_recognition_predictive_risk_scoring, revenue_recognition_counterfactual_scenario_simulation, revenue_recognition_cryptographic_audit_proofs, revenue_recognition_continuous_control_testing, revenue_recognition_carbon_and_sustainability_awareness, revenue_recognition_cross_pbc_event_federation, revenue_recognition_governed_ai_agent_execution
