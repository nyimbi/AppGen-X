# Insurance Claims and Policy PBC

## Purpose

The `insurance_claims_policy` PBC is a world-class packaged business capability for Owns policies, coverages, endorsements, premiums, claims, loss events, reserves, adjudication, settlements, recoveries, communications, and claims intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `insurance_claims_policy_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `insurance_claims_policy_insurance_policy`: owns insurance policy lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_policy_holder`: owns policy holder lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_policy_coverage`: owns policy coverage lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_policy_endorsement`: owns policy endorsement lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_premium_schedule`: owns premium schedule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_premium_payment`: owns premium payment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_record`: owns claim record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_loss_event`: owns loss event lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claimant`: owns claimant lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_document`: owns claim document lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_coverage_determination`: owns coverage determination lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_reserve`: owns claim reserve lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_reserve_change`: owns reserve change lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_adjudication`: owns claim adjudication lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_settlement_offer`: owns settlement offer lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_settlement_payment`: owns settlement payment lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_subrogation_recovery`: owns subrogation recovery lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_communication`: owns claim communication lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_fraud_indicator`: owns fraud indicator lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_claim_exception_case`: owns claim exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_insurance_policy_rule`: owns insurance policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_insurance_runtime_parameter`: owns insurance runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_insurance_schema_extension`: owns insurance schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_insurance_control_assertion`: owns insurance control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_insurance_governed_model`: owns insurance governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `insurance_claims_policy_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `insurance_claims_policy_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `insurance_claims_policy_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for policies: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_insurance_policy`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_policy_holder`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_policy_coverage`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_endorsement`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_premium_schedule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_premium_payment`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_claim`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_loss_event`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_claimant`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `attach_claim_document`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `determine_coverage`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `set_claim_reserve`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_reserve_change`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `adjudicate_claim`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_settlement_offer`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `execute_settlement_payment`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_subrogation_recovery`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `send_claim_communication`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_fraud_indicator`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_claim_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_insurance_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_loss_exposure`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- coverage reasoning engine: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- reserve adequacy forecasting: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- fraud signal fusion: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- loss exposure simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- settlement optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic claim evidence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `coverage_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `reserve_authority_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `settlement_approval_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `fraud_escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `premium_grace_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `recovery_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `reserve_review_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `settlement_authority_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `fraud_score_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `premium_grace_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `claim_sla_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `insurance_claims_policy_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `PolicyCreated`
- `CoverageDetermined`
- `ClaimOpened`
- `ReserveChanged`
- `ClaimAdjudicated`
- `SettlementPaid`

Consumed events:

- `PaymentCaptured`
- `CustomerUpdated`
- `FraudSignalRaised`
- `PolicyChanged`

Handlers use idempotency keys of the form `insurance_claims_policy:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- insurance workbench.
- policy coverage detail.
- claims queue.
- reserve console.
- adjudication board.
- settlement room.
- fraud and recovery panel.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `insurance_claims_policy_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: insurance_policy, policy_holder, policy_coverage, policy_endorsement, premium_schedule, premium_payment, claim_record, loss_event, claimant, claim_document, coverage_determination, claim_reserve, reserve_change, claim_adjudication, settlement_offer, settlement_payment, subrogation_recovery, claim_communication, fraud_indicator, claim_exception_case, insurance_policy_rule, insurance_runtime_parameter, insurance_schema_extension, insurance_control_assertion, insurance_governed_model
- operations: create_insurance_policy, register_policy_holder, define_policy_coverage, record_endorsement, create_premium_schedule, record_premium_payment, open_claim, record_loss_event, register_claimant, attach_claim_document, determine_coverage, set_claim_reserve, record_reserve_change, adjudicate_claim, create_settlement_offer, execute_settlement_payment, record_subrogation_recovery, send_claim_communication, score_fraud_indicator, resolve_claim_exception, compile_insurance_rule, simulate_loss_exposure
- emits: PolicyCreated, CoverageDetermined, ClaimOpened, ReserveChanged, ClaimAdjudicated, SettlementPaid
- consumes: PaymentCaptured, CustomerUpdated, FraudSignalRaised, PolicyChanged
- rules: coverage_policy, reserve_authority_policy, settlement_approval_policy, fraud_escalation_policy, premium_grace_policy, recovery_policy
- parameters: reserve_review_threshold, settlement_authority_limit, fraud_score_threshold, premium_grace_days, claim_sla_days, workbench_limit
- advanced_capabilities: coverage reasoning engine, reserve adequacy forecasting, fraud signal fusion, loss exposure simulation, settlement optimization, cryptographic claim evidence
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: insurance_policy, claim_intake, coverage_validation, claim_reserve, adjuster_assignment, claim_fraud_signal, claim_settlement, claim_audit_evidence
- apis: POST /insurance-policies, POST /claims, POST /coverage-validations, POST /claim-settlements, GET /insurance-workbench
- emits: ClaimOpened, CoverageValidated, ClaimReserveSet, ClaimSettled
- consumes: CustomerUpdated, PaymentCaptured, FraudRiskScored
- ui_fragments: InsuranceClaimsPolicyWorkbench, InsuranceClaimsPolicyDetail, InsuranceClaimsPolicyAssistantPanel
- permissions: insurance_claims_policy.read, insurance_claims_policy.create, insurance_claims_policy.update, insurance_claims_policy.approve, insurance_claims_policy.admin
- configuration: INSURANCE_CLAIMS_POLICY_DATABASE_URL, INSURANCE_CLAIMS_POLICY_EVENT_TOPIC, INSURANCE_CLAIMS_POLICY_RETRY_LIMIT, INSURANCE_CLAIMS_POLICY_DEFAULT_POLICY
- standard_features: insurance_policy_management, insurance_claims_policy_workflow, insurance_claims_policy_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: insurance_claims_policy_event_sourced_operational_history, insurance_claims_policy_multi_tenant_policy_isolation, insurance_claims_policy_schema_evolution_resilience, insurance_claims_policy_autonomous_anomaly_detection, insurance_claims_policy_semantic_document_instruction_understanding, insurance_claims_policy_predictive_risk_scoring, insurance_claims_policy_counterfactual_scenario_simulation, insurance_claims_policy_cryptographic_audit_proofs, insurance_claims_policy_continuous_control_testing, insurance_claims_policy_carbon_and_sustainability_awareness, insurance_claims_policy_cross_pbc_event_federation, insurance_claims_policy_governed_ai_agent_execution
