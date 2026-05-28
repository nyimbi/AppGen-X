# Data Product Catalog PBC

## Purpose

The `data_product_catalog` PBC is a world-class packaged business capability for Owns data products, ownership, contracts, schemas, quality, lineage, access, subscriptions, certifications, usage analytics, and productized data governance. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `data_product_catalog_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `data_product_catalog_data_product`: owns data product lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_owner`: owns data product owner lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_contract`: owns data contract lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_schema_version`: owns data schema version lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_quality_signal`: owns data quality signal lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_lineage_edge`: owns data lineage edge lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_access_request`: owns data access request lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_access_grant`: owns data access grant lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_subscription`: owns data subscription lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_certification`: owns data product certification lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_usage`: owns data product usage lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_sla`: owns data product sla lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_incident`: owns data product incident lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_change`: owns data product change lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_retention_policy`: owns data product retention policy lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_exception_case`: owns data product exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_policy_rule`: owns data product policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_runtime_parameter`: owns data product runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_schema_extension`: owns data product schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_control_assertion`: owns data product control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_data_product_governed_model`: owns data product governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `data_product_catalog_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `data_product_catalog_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `data_product_catalog_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for data products: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_data_product`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `assign_data_owner`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_data_contract`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_schema_version`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_quality_signal`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `map_lineage_edge`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `request_data_access`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `grant_data_access`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `subscribe_to_data_product`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `certify_data_product`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_usage`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_product_sla`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_product_incident`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_product_change`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_retention_policy`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_data_product_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_data_product_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_contract_change_impact`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- contract-aware data discovery: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- lineage impact simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- quality drift detection: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- AI data product steward: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- policy-aware access recommendation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic contract evidence: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `data_contract_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `quality_certification_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `access_approval_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `lineage_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `SLA_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `retention_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `quality_score_floor`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `access_review_days`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `schema_compatibility_level`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `usage_anomaly_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `sla_warning_minutes`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `data_product_catalog_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `DataProductCreated`
- `DataContractPublished`
- `DataQualityChanged`
- `DataAccessGranted`
- `DataProductCertified`
- `DataProductIncidentOpened`

Consumed events:

- `PolicyChanged`
- `AccessPolicyChanged`
- `SchemaAccepted`
- `AuditProofGenerated`

Handlers use idempotency keys of the form `data_product_catalog:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- data product catalog.
- contract studio.
- quality dashboard.
- lineage graph.
- access request queue.
- certification panel.
- usage analytics.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `data_product_catalog_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: data_product, data_product_owner, data_contract, data_schema_version, data_quality_signal, data_lineage_edge, data_access_request, data_access_grant, data_subscription, data_product_certification, data_product_usage, data_product_sla, data_product_incident, data_product_change, data_product_retention_policy, data_product_exception_case, data_product_policy_rule, data_product_runtime_parameter, data_product_schema_extension, data_product_control_assertion, data_product_governed_model
- operations: create_data_product, assign_data_owner, publish_data_contract, register_schema_version, record_quality_signal, map_lineage_edge, request_data_access, grant_data_access, subscribe_to_data_product, certify_data_product, record_usage, define_product_sla, open_product_incident, publish_product_change, define_retention_policy, resolve_data_product_exception, compile_data_product_rule, simulate_contract_change_impact
- emits: DataProductCreated, DataContractPublished, DataQualityChanged, DataAccessGranted, DataProductCertified, DataProductIncidentOpened
- consumes: PolicyChanged, AccessPolicyChanged, SchemaAccepted, AuditProofGenerated
- rules: data_contract_policy, quality_certification_policy, access_approval_policy, lineage_policy, SLA_policy, retention_policy
- parameters: quality_score_floor, access_review_days, schema_compatibility_level, usage_anomaly_threshold, sla_warning_minutes, workbench_limit
- advanced_capabilities: contract-aware data discovery, lineage impact simulation, quality drift detection, AI data product steward, policy-aware access recommendation, cryptographic contract evidence
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: data_product, data_product_owner, data_contract, data_quality_sla, lineage_edge, data_access_request, data_governance_rule, data_publication_workflow
- apis: POST /data-products, POST /data-contracts, POST /quality-slas, POST /access-requests, GET /data-product-catalog-workbench
- emits: DataProductPublished, DataContractChanged, DataAccessApproved, QualitySlaBreached
- consumes: SchemaPublished, PolicyChanged, SearchIndexRefreshed
- ui_fragments: DataProductCatalogWorkbench, DataProductCatalogDetail, DataProductCatalogAssistantPanel
- permissions: data_product_catalog.read, data_product_catalog.create, data_product_catalog.update, data_product_catalog.approve, data_product_catalog.admin
- configuration: DATA_PRODUCT_CATALOG_DATABASE_URL, DATA_PRODUCT_CATALOG_EVENT_TOPIC, DATA_PRODUCT_CATALOG_RETRY_LIMIT, DATA_PRODUCT_CATALOG_DEFAULT_POLICY
- standard_features: data_product_management, data_product_catalog_workflow, data_product_catalog_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: data_product_catalog_event_sourced_operational_history, data_product_catalog_multi_tenant_policy_isolation, data_product_catalog_schema_evolution_resilience, data_product_catalog_autonomous_anomaly_detection, data_product_catalog_semantic_document_instruction_understanding, data_product_catalog_predictive_risk_scoring, data_product_catalog_counterfactual_scenario_simulation, data_product_catalog_cryptographic_audit_proofs, data_product_catalog_continuous_control_testing, data_product_catalog_carbon_and_sustainability_awareness, data_product_catalog_cross_pbc_event_federation, data_product_catalog_governed_ai_agent_execution
