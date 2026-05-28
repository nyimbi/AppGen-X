# Vendor and Supplier 360 PBC

## Purpose

The `vendor_supplier_360` PBC is a world-class packaged business capability for Owns supplier master data, onboarding, qualification, sites, contacts, tax and bank credentials, certifications, diversity and sustainability evidence, risk, performance, segmentation, relationship planning, and supplier intelligence. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `vendor_supplier_360_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `vendor_supplier_360_supplier_profile`: owns supplier profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_site`: owns supplier site lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_contact`: owns supplier contact lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_identity_proof`: owns supplier identity proof lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_beneficial_owner`: owns supplier beneficial owner lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_tax_profile`: owns supplier tax profile lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_bank_validation`: owns supplier bank validation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_payment_preference`: owns supplier payment preference lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_certification`: owns supplier certification lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_diversity_attribute`: owns supplier diversity attribute lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_esg_disclosure`: owns supplier esg disclosure lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_sanctions_screening`: owns supplier sanctions screening lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_risk_signal`: owns supplier risk signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_quality_incident`: owns supplier quality incident lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_delivery_performance`: owns supplier delivery performance lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_scorecard`: owns supplier scorecard lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_segmentation`: owns supplier segmentation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_onboarding_case`: owns supplier onboarding case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_qualification_decision`: owns supplier qualification decision lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_contract_reference`: owns supplier contract reference lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_spend_snapshot`: owns supplier spend snapshot lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_concentration_exposure`: owns supplier concentration exposure lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_action_plan`: owns supplier action plan lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_exception_case`: owns supplier exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_policy_rule`: owns supplier policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_runtime_parameter`: owns supplier runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_schema_extension`: owns supplier schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_control_assertion`: owns supplier control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_supplier_governed_model`: owns supplier governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `vendor_supplier_360_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `vendor_supplier_360_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `vendor_supplier_360_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for suppliers: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_supplier_profile`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `validate_supplier_identity`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_supplier_site`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_tax_profile`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `validate_bank_account`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_certification`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `screen_sanctions`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_esg_disclosure`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `score_supplier_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `qualify_supplier`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `segment_supplier`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_quality_incident`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `update_delivery_performance`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_scorecard`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `detect_concentration_exposure`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_onboarding_case`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `approve_supplier`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_supplier_action_plan`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_supplier_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_supplier_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_supplier_failure_impact`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- supplier graph intelligence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- counterfactual supplier disruption simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- semantic document onboarding: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- continuous certification control testing: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic credential proof: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- risk-aware sourcing recommendation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `qualification_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `bank_validation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `certification_expiry_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `sanctions_escalation_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `concentration_limit_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `performance_scorecard_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `risk_review_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `certification_warning_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `concentration_limit_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `minimum_delivery_score`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `bank_validation_ttl_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `vendor_supplier_360_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `SupplierProfileCreated`
- `SupplierBankValidated`
- `SupplierQualified`
- `SupplierRiskChanged`
- `SupplierScorecardPublished`
- `SupplierExceptionOpened`

Consumed events:

- `PurchaseOrderCreated`
- `PaymentRejected`
- `CompliancePolicyChanged`
- `QualityIncidentRecorded`

Handlers use idempotency keys of the form `vendor_supplier_360:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- supplier 360 workbench.
- onboarding case board.
- bank and tax validation panel.
- certification tracker.
- risk and sanctions console.
- scorecard cockpit.
- relationship action planner.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `vendor_supplier_360_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: supplier_profile, supplier_site, supplier_contact, supplier_identity_proof, supplier_beneficial_owner, supplier_tax_profile, supplier_bank_validation, supplier_payment_preference, supplier_certification, supplier_diversity_attribute, supplier_esg_disclosure, supplier_sanctions_screening, supplier_risk_signal, supplier_quality_incident, supplier_delivery_performance, supplier_scorecard, supplier_segmentation, supplier_onboarding_case, supplier_qualification_decision, supplier_contract_reference, supplier_spend_snapshot, supplier_concentration_exposure, supplier_action_plan, supplier_exception_case, supplier_policy_rule, supplier_runtime_parameter, supplier_schema_extension, supplier_control_assertion, supplier_governed_model
- operations: create_supplier_profile, validate_supplier_identity, register_supplier_site, capture_tax_profile, validate_bank_account, capture_certification, screen_sanctions, record_esg_disclosure, score_supplier_risk, qualify_supplier, segment_supplier, record_quality_incident, update_delivery_performance, calculate_scorecard, detect_concentration_exposure, open_onboarding_case, approve_supplier, create_supplier_action_plan, resolve_supplier_exception, compile_supplier_rule, simulate_supplier_failure_impact
- emits: SupplierProfileCreated, SupplierBankValidated, SupplierQualified, SupplierRiskChanged, SupplierScorecardPublished, SupplierExceptionOpened
- consumes: PurchaseOrderCreated, PaymentRejected, CompliancePolicyChanged, QualityIncidentRecorded
- rules: qualification_policy, bank_validation_policy, certification_expiry_policy, sanctions_escalation_policy, concentration_limit_policy, performance_scorecard_policy
- parameters: risk_review_threshold, certification_warning_days, concentration_limit_percent, minimum_delivery_score, bank_validation_ttl_days, workbench_limit
- advanced_capabilities: supplier graph intelligence, counterfactual supplier disruption simulation, semantic document onboarding, continuous certification control testing, cryptographic credential proof, risk-aware sourcing recommendation
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: supplier_profile, supplier_site, supplier_certification, supplier_bank_validation, supplier_risk_signal, supplier_esg_disclosure, supplier_scorecard, supplier_onboarding_case
- apis: POST /suppliers, POST /suppliers/{id}/sites, POST /suppliers/{id}/certifications, POST /suppliers/{id}/bank-validations, GET /supplier-360-workbench
- emits: SupplierQualified, SupplierRiskChanged, SupplierBankValidated, SupplierOnboarded
- consumes: PurchaseOrderCreated, PaymentRejected, CompliancePolicyChanged
- ui_fragments: VendorSupplier360Workbench, VendorSupplier360Detail, VendorSupplier360AssistantPanel
- permissions: vendor_supplier_360.read, vendor_supplier_360.create, vendor_supplier_360.update, vendor_supplier_360.approve, vendor_supplier_360.admin
- configuration: VENDOR_SUPPLIER_360_DATABASE_URL, VENDOR_SUPPLIER_360_EVENT_TOPIC, VENDOR_SUPPLIER_360_RETRY_LIMIT, VENDOR_SUPPLIER_360_DEFAULT_POLICY
- standard_features: supplier_profile_management, vendor_supplier_360_workflow, vendor_supplier_360_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: vendor_supplier_360_event_sourced_operational_history, vendor_supplier_360_multi_tenant_policy_isolation, vendor_supplier_360_schema_evolution_resilience, vendor_supplier_360_autonomous_anomaly_detection, vendor_supplier_360_semantic_document_instruction_understanding, vendor_supplier_360_predictive_risk_scoring, vendor_supplier_360_counterfactual_scenario_simulation, vendor_supplier_360_cryptographic_audit_proofs, vendor_supplier_360_continuous_control_testing, vendor_supplier_360_carbon_and_sustainability_awareness, vendor_supplier_360_cross_pbc_event_federation, vendor_supplier_360_governed_ai_agent_execution
