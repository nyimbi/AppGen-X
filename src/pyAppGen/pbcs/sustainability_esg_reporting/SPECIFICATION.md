# Sustainability ESG Reporting PBC

## Purpose

The `sustainability_esg_reporting` PBC is a world-class packaged business capability for Owns ESG metrics, activity data, emissions factors, calculations, targets, supplier inputs, assurance evidence, disclosure packs, and sustainability reporting controls. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `sustainability_esg_reporting_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `sustainability_esg_reporting_esg_metric`: owns esg metric lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_activity_record`: owns esg activity record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_emissions_factor`: owns emissions factor lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_emissions_calculation`: owns emissions calculation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_scope_boundary`: owns scope boundary lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_supplier_esg_input`: owns supplier esg input lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_sustainability_target`: owns sustainability target lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_target_progress`: owns target progress lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_framework_mapping`: owns framework mapping lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_disclosure_packet`: owns disclosure packet lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_assurance_evidence`: owns assurance evidence lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_assurance_exception`: owns assurance exception lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_data_quality_check`: owns data quality check lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_carbon_offset_record`: owns carbon offset record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_climate_risk_scenario`: owns climate risk scenario lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_exception_case`: owns esg exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_policy_rule`: owns esg policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_runtime_parameter`: owns esg runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_schema_extension`: owns esg schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_control_assertion`: owns esg control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_esg_governed_model`: owns esg governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `sustainability_esg_reporting_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `sustainability_esg_reporting_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `sustainability_esg_reporting_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for ESG metrics: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `define_esg_metric`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `capture_activity_record`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_emissions_factor`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `calculate_emissions`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_scope_boundary`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `ingest_supplier_esg_input`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_sustainability_target`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `measure_target_progress`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `map_reporting_framework`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `build_disclosure_packet`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `attach_assurance_evidence`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_assurance_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `run_data_quality_check`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_carbon_offset`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_climate_risk`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_esg_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_esg_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_emissions_reduction`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- carbon calculation lineage: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- supplier ESG confidence scoring: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- climate scenario simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- assurance anomaly detection: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- framework semantic mapping: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic disclosure proof: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `emissions_factor_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `scope_boundary_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `assurance_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `target_tracking_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `framework_mapping_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `data_quality_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `quality_score_floor`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `target_warning_percent`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `factor_expiry_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `assurance_sample_rate`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `materiality_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `sustainability_esg_reporting_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `EsgMetricDefined`
- `ActivityRecordCaptured`
- `EmissionsCalculated`
- `TargetProgressMeasured`
- `DisclosurePacketBuilt`
- `AssuranceExceptionOpened`

Consumed events:

- `SupplierQualified`
- `ShipmentDelivered`
- `EnergyUsageRecorded`
- `PolicyChanged`

Handlers use idempotency keys of the form `sustainability_esg_reporting:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- ESG reporting workbench.
- activity data inbox.
- emissions calculator.
- target tracker.
- framework mapping studio.
- assurance evidence room.
- disclosure builder.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `sustainability_esg_reporting_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: esg_metric, esg_activity_record, emissions_factor, emissions_calculation, scope_boundary, supplier_esg_input, sustainability_target, target_progress, framework_mapping, disclosure_packet, assurance_evidence, assurance_exception, data_quality_check, carbon_offset_record, climate_risk_scenario, esg_exception_case, esg_policy_rule, esg_runtime_parameter, esg_schema_extension, esg_control_assertion, esg_governed_model
- operations: define_esg_metric, capture_activity_record, register_emissions_factor, calculate_emissions, define_scope_boundary, ingest_supplier_esg_input, create_sustainability_target, measure_target_progress, map_reporting_framework, build_disclosure_packet, attach_assurance_evidence, open_assurance_exception, run_data_quality_check, record_carbon_offset, simulate_climate_risk, resolve_esg_exception, compile_esg_rule, simulate_emissions_reduction
- emits: EsgMetricDefined, ActivityRecordCaptured, EmissionsCalculated, TargetProgressMeasured, DisclosurePacketBuilt, AssuranceExceptionOpened
- consumes: SupplierQualified, ShipmentDelivered, EnergyUsageRecorded, PolicyChanged
- rules: emissions_factor_policy, scope_boundary_policy, assurance_policy, target_tracking_policy, framework_mapping_policy, data_quality_policy
- parameters: quality_score_floor, target_warning_percent, factor_expiry_days, assurance_sample_rate, materiality_threshold, workbench_limit
- advanced_capabilities: carbon calculation lineage, supplier ESG confidence scoring, climate scenario simulation, assurance anomaly detection, framework semantic mapping, cryptographic disclosure proof
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: emissions_factor, activity_data, carbon_ledger_entry, esg_metric, supplier_disclosure, assurance_evidence, sustainability_report, regulatory_submission
- apis: POST /emissions-factors, POST /activity-data, POST /carbon-ledger, POST /sustainability-reports, GET /esg-workbench
- emits: CarbonLedgerPosted, EsgMetricPublished, SustainabilityReportFiled, SupplierDisclosureReceived
- consumes: SupplierQualified, TravelBooked, AssetPlacedInService
- ui_fragments: SustainabilityEsgReportingWorkbench, SustainabilityEsgReportingDetail, SustainabilityEsgReportingAssistantPanel
- permissions: sustainability_esg_reporting.read, sustainability_esg_reporting.create, sustainability_esg_reporting.update, sustainability_esg_reporting.approve, sustainability_esg_reporting.admin
- configuration: SUSTAINABILITY_ESG_REPORTING_DATABASE_URL, SUSTAINABILITY_ESG_REPORTING_EVENT_TOPIC, SUSTAINABILITY_ESG_REPORTING_RETRY_LIMIT, SUSTAINABILITY_ESG_REPORTING_DEFAULT_POLICY
- standard_features: emissions_factor_management, sustainability_esg_reporting_workflow, sustainability_esg_reporting_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: sustainability_esg_reporting_event_sourced_operational_history, sustainability_esg_reporting_multi_tenant_policy_isolation, sustainability_esg_reporting_schema_evolution_resilience, sustainability_esg_reporting_autonomous_anomaly_detection, sustainability_esg_reporting_semantic_document_instruction_understanding, sustainability_esg_reporting_predictive_risk_scoring, sustainability_esg_reporting_counterfactual_scenario_simulation, sustainability_esg_reporting_cryptographic_audit_proofs, sustainability_esg_reporting_continuous_control_testing, sustainability_esg_reporting_carbon_and_sustainability_awareness, sustainability_esg_reporting_cross_pbc_event_federation, sustainability_esg_reporting_governed_ai_agent_execution
