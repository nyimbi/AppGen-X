# Building Information Modeling Operations PBC

## Purpose

The `building_information_modeling_ops` PBC is a packaged business capability for BIM models, versions, clashes, assets, handover data, model governance, and digital twin operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `building_information_modeling_ops`.
- Mesh: `content`.
- Package directory: `src/pyAppGen/pbcs/building_information_modeling_ops`.
- Runtime entrypoint: `building_information_modeling_ops_runtime_capabilities()`.
- UI entrypoint: `building_information_modeling_ops_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `building_information_modeling_ops_bim_model`: owns bim model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_model_version`: owns model version lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_clash_issue`: owns clash issue lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_asset_object`: owns asset object lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_handover_package`: owns handover package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_model_review`: owns model review lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_digital_twin_link`: owns digital twin link lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_building_information_modeling_ops_policy_rule`: owns building information modeling ops policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_building_information_modeling_ops_runtime_parameter`: owns building information modeling ops runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_building_information_modeling_ops_schema_extension`: owns building information modeling ops schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_building_information_modeling_ops_control_assertion`: owns building information modeling ops control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `building_information_modeling_ops_building_information_modeling_ops_governed_model`: owns building information modeling ops governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `building_information_modeling_ops_appgen_outbox_event`, `building_information_modeling_ops_appgen_inbox_event`, and `building_information_modeling_ops_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /bim-models', 'POST /model-versions', 'POST /clash-issues', 'POST /asset-objects', 'POST /handover-packages', 'GET /building-information-modeling-ops-workbench').

## Executable Domain Operations

- `create_bim_model`: validates policy, writes owned `building_information_modeling_ops_bim_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_model_version`: validates policy, writes owned `building_information_modeling_ops_model_version` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_clash_issue`: validates policy, writes owned `building_information_modeling_ops_clash_issue` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_asset_object`: validates policy, writes owned `building_information_modeling_ops_asset_object` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_handover_package`: validates policy, writes owned `building_information_modeling_ops_handover_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_model_review`: validates policy, writes owned `building_information_modeling_ops_model_review` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_digital_twin_link`: validates policy, writes owned `building_information_modeling_ops_digital_twin_link` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_building_information_modeling_ops_policy_rule`: validates policy, writes owned `building_information_modeling_ops_building_information_modeling_ops_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_building_information_modeling_ops_runtime_parameter`: validates policy, writes owned `building_information_modeling_ops_building_information_modeling_ops_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_building_information_modeling_ops_schema_extension`: validates policy, writes owned `building_information_modeling_ops_building_information_modeling_ops_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_building_information_modeling_ops_control_assertion`: validates policy, writes owned `building_information_modeling_ops_building_information_modeling_ops_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_building_information_modeling_ops_governed_model`: validates policy, writes owned `building_information_modeling_ops_building_information_modeling_ops_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_13`: validates policy, writes owned `building_information_modeling_ops_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_14`: validates policy, writes owned `building_information_modeling_ops_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_15`: validates policy, writes owned `building_information_modeling_ops_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_16`: validates policy, writes owned `building_information_modeling_ops_bim_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_17`: validates policy, writes owned `building_information_modeling_ops_model_version` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_building_information_modeling_ops_18`: validates policy, writes owned `building_information_modeling_ops_clash_issue` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Building Information Modeling Operations domain records.
- Multi-tenant policy isolation with owned table boundaries.
- Schema evolution resilience through package-local schema extensions.
- Autonomous anomaly detection and specialist exception triage.
- Semantic document and instruction understanding for professional intake.
- Predictive risk scoring and confidence-ranked recommendations.
- Counterfactual scenario simulation for policy and operational choices.
- Cryptographic audit proofs for high-value records and decisions.
- Continuous control testing over domain lifecycle events.
- Carbon and sustainability awareness where operational decisions affect footprint.
- Cross-PBC event federation through AppGen-X only.
- Governed AI agent execution with human confirmation for mutations.

## Rules, Parameters, and Configuration

Rules are first-class artifacts: ('bim_model_policy', 'model_version_policy', 'clash_issue_policy', 'asset_object_policy', 'handover_package_policy', 'model_review_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /bim-models', 'POST /model-versions', 'POST /clash-issues', 'POST /asset-objects', 'POST /handover-packages', 'GET /building-information-modeling-ops-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `building_information_modeling_ops_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('BuildingInformationModelingOpsCreated', 'BuildingInformationModelingOpsUpdated', 'BuildingInformationModelingOpsApproved', 'BuildingInformationModelingOpsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('bim model board', 'model version board', 'clash issue board', 'asset object board', 'handover package board', 'model review board', 'digital twin link board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `building_information_modeling_ops_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: bim_model, model_version, clash_issue, asset_object, handover_package, model_review, digital_twin_link, building_information_modeling_ops_policy_rule, building_information_modeling_ops_runtime_parameter, building_information_modeling_ops_schema_extension, building_information_modeling_ops_control_assertion, building_information_modeling_ops_governed_model
- operations: create_bim_model, record_model_version, review_clash_issue, approve_asset_object, simulate_handover_package, create_model_review, record_digital_twin_link, review_building_information_modeling_ops_policy_rule, approve_building_information_modeling_ops_runtime_parameter, simulate_building_information_modeling_ops_schema_extension, create_building_information_modeling_ops_control_assertion, record_building_information_modeling_ops_governed_model, operate_building_information_modeling_ops_13, operate_building_information_modeling_ops_14, operate_building_information_modeling_ops_15, operate_building_information_modeling_ops_16, operate_building_information_modeling_ops_17, operate_building_information_modeling_ops_18
- emits: BuildingInformationModelingOpsCreated, BuildingInformationModelingOpsUpdated, BuildingInformationModelingOpsApproved, BuildingInformationModelingOpsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: bim_model_policy, model_version_policy, clash_issue_policy, asset_object_policy, handover_package_policy, model_review_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: BuildingInformationModelingOpsWorkbench, BuildingInformationModelingOpsDetail, BuildingInformationModelingOpsAssistantPanel
- permissions: building_information_modeling_ops.read, building_information_modeling_ops.create, building_information_modeling_ops.update, building_information_modeling_ops.approve, building_information_modeling_ops.admin
- configuration: BUILDING_INFORMATION_MODELING_OPS_DATABASE_URL, BUILDING_INFORMATION_MODELING_OPS_EVENT_TOPIC, BUILDING_INFORMATION_MODELING_OPS_RETRY_LIMIT, BUILDING_INFORMATION_MODELING_OPS_DEFAULT_POLICY
- standard_features: bim_model_management, building_information_modeling_ops_workflow, building_information_modeling_ops_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: building_information_modeling_ops_event_sourced_operational_history, building_information_modeling_ops_multi_tenant_policy_isolation, building_information_modeling_ops_schema_evolution_resilience, building_information_modeling_ops_autonomous_anomaly_detection, building_information_modeling_ops_semantic_document_instruction_understanding, building_information_modeling_ops_predictive_risk_scoring, building_information_modeling_ops_counterfactual_scenario_simulation, building_information_modeling_ops_cryptographic_audit_proofs, building_information_modeling_ops_continuous_control_testing, building_information_modeling_ops_carbon_and_sustainability_awareness, building_information_modeling_ops_cross_pbc_event_federation, building_information_modeling_ops_governed_ai_agent_execution
