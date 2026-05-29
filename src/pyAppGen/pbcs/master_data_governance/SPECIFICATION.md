# Master Data Governance PBC

## Purpose

The `master_data_governance` PBC is a world-class packaged business capability for Owns golden records, stewardship, matching, survivorship, hierarchies, quality rules, approvals, publication, and governed master-data lifecycle automation. It is designed as a composable AppGen-X package, not a thin catalog entry. The package owns its schema, migrations, models, services, APIs, event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks. It composes with other PBCs only through declared APIs, AppGen-X events, and read-only projections.

## Owned Datastore Boundary

The package owns the following operational tables, all under the `master_data_governance_` prefix. No operation mutates a foreign table, and every cross-PBC dependency is represented as an API dependency, an AppGen-X event, or a package-local projection.

- `master_data_governance_master_record`: owns master record lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_master_domain`: owns master domain lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_source_record_link`: owns source record link lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_match_candidate`: owns match candidate lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_match_decision`: owns match decision lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_survivorship_rule`: owns survivorship rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_survivorship_decision`: owns survivorship decision lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_golden_record_version`: owns golden record version lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_hierarchy_node`: owns hierarchy node lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_hierarchy_relationship`: owns hierarchy relationship lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_data_quality_rule`: owns data quality rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_data_quality_observation`: owns data quality observation lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_stewardship_task`: owns stewardship task lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_master_data_approval`: owns master data approval lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_publication_batch`: owns publication batch lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_publication_event`: owns publication event lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_master_exception_case`: owns master exception case lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_mdm_policy_rule`: owns mdm policy rule lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_mdm_runtime_parameter`: owns mdm runtime parameter lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_mdm_schema_extension`: owns mdm schema extension lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_mdm_control_assertion`: owns mdm control assertion lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_mdm_governed_model`: owns mdm governed model lifecycle state, evidence payloads, tenant boundary, status, versioning, and audit timestamps.
- `master_data_governance_appgen_outbox_event`: AppGen-X outbox for typed domain events.
- `master_data_governance_appgen_inbox_event`: AppGen-X inbox for idempotent consumed event handling.
- `master_data_governance_appgen_dead_letter_event`: dead-letter evidence for unknown or exhausted events.

Supported backing stores are PostgreSQL, MySQL, and MariaDB. Configuration rejects any user-facing stream engine selector and records AppGen-X as the ordinary event contract.

## Standard Table-Stakes Capabilities

The package implements the full table-stakes lifecycle for master records: intake and creation, identity and classification, operational state management, policy validation, approvals, exception handling, audit evidence, user workbenches, assistant-guided task execution, configuration, runtime parameters, rule compilation, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. The domain surface is intentionally broad enough for real enterprise use instead of only demonstrating a happy path.

## Executable Domain Operations

- `create_master_record`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `register_master_domain`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `link_source_record`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `generate_match_candidate`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `record_match_decision`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_survivorship_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `apply_survivorship`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_golden_version`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_hierarchy_node`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `link_hierarchy_relationship`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `define_quality_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `observe_data_quality`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `open_stewardship_task`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `approve_master_change`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `create_publication_batch`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `publish_master_event`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `resolve_master_exception`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `compile_mdm_rule`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.
- `simulate_survivorship_impact`: command/query implementation with validation, owned table writes or read-only projections, AppGen-X event planning, permissions, rule checks, and release evidence.

Each command is side-effect-free in package tests and returns the target owned table, emitted event, idempotency key, compiled rules, parameters read, permissions required, and evidence hash. Query operations are explicitly read-only and never publish events.

## Advanced Capabilities

- probabilistic entity resolution: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- explainable survivorship: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- hierarchy impact simulation: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- quality anomaly detection: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- stewardship workload optimization: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.
- cryptographic golden record proof: deterministic smoke evidence, governed model metadata where relevant, explainable output, and boundary-safe event/API collaboration.

Advanced execution is represented in `domain_depth_contract()`, `execute_domain_operation()`, package release evidence, and runtime capabilities. These functions are deterministic and can be used by generation smoke audits, external package validators, and composed application agents.

## Rules, Parameters, and Configuration

Rules are first-class runtime artifacts:

- `matching_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `survivorship_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `quality_threshold_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `stewardship_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `hierarchy_change_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.
- `publication_policy`: executable policy compiled with tenant, scope, status, hash, and side-effect-free evaluation.

Parameters are first-class runtime artifacts:

- `match_confidence_threshold`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `quality_score_floor`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `stewardship_sla_hours`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `publication_batch_size`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `hierarchy_depth_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.
- `workbench_limit`: bounded runtime parameter surfaced in configuration, service guards, workbench controls, and agent recommendations.

Configuration includes database backend, AppGen-X topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options. Rule compilation rejects event-engine picker fields before evaluation.

## Public APIs and Services

The service layer exposes package-local commands for the domain operations above and read-only query/workbench surfaces. APIs are generated from the same contract, preserving idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `master_data_governance_` tables plus the package AppGen-X outbox, inbox, and dead-letter tables.

## Events

Emitted events:

- `MasterRecordCreated`
- `MatchCandidateGenerated`
- `GoldenRecordPublished`
- `HierarchyChanged`
- `DataQualityChanged`
- `MasterDataPublished`

Consumed events:

- `CustomerUpdated`
- `SupplierQualified`
- `ProductPublished`
- `PolicyChanged`

Handlers use idempotency keys of the form `master_data_governance:<event_type>:<event_id>`, retry at least three times, and record dead-letter evidence with retry metadata. Unknown events do not mutate domain state.

## UI and Workbench

The package includes professional workbench surfaces:

- master data workbench.
- match review queue.
- survivorship studio.
- golden record detail.
- hierarchy manager.
- quality console.
- publication monitor.

The UI exposes operational queues, detail panels, rule and parameter editors, assistant panels, exception triage, analytics, and release-evidence status. Actions are permission-bound and grounded in owned state.

## AI Agent and Skills

The PBC contributes first-class skills to the composed application assistant under the `master_data_governance_skills` namespace. The agent can explain tasks, parse documents and instructions, recommend CRUD plans, validate owned-table boundaries, require human confirmation for writes, and produce event plans. It never writes foreign tables and exposes its competencies through DSL-visible composed assistant tool names.

## Release Evidence and Tests

Release readiness requires the package to prove schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry and dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent skill integration, and generation smoke readiness. Focused tests assert that the package has at least twenty owned domain tables, at least fifteen executable domain operations, at least six domain rules, at least six bounded parameters, AppGen-X eventing, and no shared-table mutation.

## Manifest Traceability Appendix

- tables: master_record, master_domain, source_record_link, match_candidate, match_decision, survivorship_rule, survivorship_decision, golden_record_version, hierarchy_node, hierarchy_relationship, data_quality_rule, data_quality_observation, stewardship_task, master_data_approval, publication_batch, publication_event, master_exception_case, mdm_policy_rule, mdm_runtime_parameter, mdm_schema_extension, mdm_control_assertion, mdm_governed_model
- operations: create_master_record, register_master_domain, link_source_record, generate_match_candidate, record_match_decision, define_survivorship_rule, apply_survivorship, publish_golden_version, create_hierarchy_node, link_hierarchy_relationship, define_quality_rule, observe_data_quality, open_stewardship_task, approve_master_change, create_publication_batch, publish_master_event, resolve_master_exception, compile_mdm_rule, simulate_survivorship_impact
- emits: MasterRecordCreated, MatchCandidateGenerated, GoldenRecordPublished, HierarchyChanged, DataQualityChanged, MasterDataPublished
- consumes: CustomerUpdated, SupplierQualified, ProductPublished, PolicyChanged
- rules: matching_policy, survivorship_policy, quality_threshold_policy, stewardship_policy, hierarchy_change_policy, publication_policy
- parameters: match_confidence_threshold, quality_score_floor, stewardship_sla_hours, publication_batch_size, hierarchy_depth_limit, workbench_limit
- advanced_capabilities: probabilistic entity resolution, explainable survivorship, hierarchy impact simulation, quality anomaly detection, stewardship workload optimization, cryptographic golden record proof
## Catalog Manifest Traceability Appendix

The following exact catalog values are retained so release audits can prove the deep domain implementation remains traceable to the stable public manifest.
- tables: master_record, golden_record, match_candidate, merge_decision, survivorship_rule, data_quality_rule, stewardship_task, downstream_sync_event
- apis: POST /master-records, POST /match-candidates, POST /merge-decisions, POST /stewardship-tasks, GET /master-data-workbench
- emits: GoldenRecordPublished, MergeDecisionApproved, StewardshipTaskOpened, MasterDataSynced
- consumes: CustomerUpdated, SupplierQualified, ProductPublished
- ui_fragments: MasterDataGovernanceWorkbench, MasterDataGovernanceDetail, MasterDataGovernanceAssistantPanel
- permissions: master_data_governance.read, master_data_governance.create, master_data_governance.update, master_data_governance.approve, master_data_governance.admin
- configuration: MASTER_DATA_GOVERNANCE_DATABASE_URL, MASTER_DATA_GOVERNANCE_EVENT_TOPIC, MASTER_DATA_GOVERNANCE_RETRY_LIMIT, MASTER_DATA_GOVERNANCE_DEFAULT_POLICY
- standard_features: master_record_management, master_data_governance_workflow, master_data_governance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: master_data_governance_event_sourced_operational_history, master_data_governance_multi_tenant_policy_isolation, master_data_governance_schema_evolution_resilience, master_data_governance_autonomous_anomaly_detection, master_data_governance_semantic_document_instruction_understanding, master_data_governance_predictive_risk_scoring, master_data_governance_counterfactual_scenario_simulation, master_data_governance_cryptographic_audit_proofs, master_data_governance_continuous_control_testing, master_data_governance_carbon_and_sustainability_awareness, master_data_governance_cross_pbc_event_federation, master_data_governance_governed_ai_agent_execution

## Standalone One-PBC App Surface

This package now ships a **standalone** executable slice in `standalone.py` that can run as a one-PBC app with package-local SQLite persistence for focused audits and smoke execution. The standalone surface includes:

- domain registry setup and stewardship ownership.
- golden records publication with lineage capture.
- survivorship policy definition and review.
- match/merge resolution with steward approval.
- stewardship workflow queues and task assignment.
- data quality rules and threshold governance.
- hierarchy management for governed relationships.
- reference data registration for controlled vocabularies.
- dedupe candidate handling and merge evidence.
- lineage evidence linking source records to golden records.
- policy approvals before sensitive publication actions.
- remediation queue management for quality exceptions.
- audit proof capture for release and operational attestations.

The package-local routes, forms, wizards, controls, seed bundle, AI planning surface, and release evidence all point to the same standalone implementation so source, release, and generation smoke audits can exercise the exact one-PBC app path.
