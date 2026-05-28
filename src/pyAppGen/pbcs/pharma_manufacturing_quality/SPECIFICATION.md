# Pharma Manufacturing Quality PBC

## Purpose

The `pharma_manufacturing_quality` PBC is a packaged business capability for Batch records, validation, deviations, CAPA, release, serialization, and regulated manufacturing quality. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `pharma_manufacturing_quality`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/pharma_manufacturing_quality`.
- Runtime entrypoint: `pharma_manufacturing_quality_runtime_capabilities()`.
- UI entrypoint: `pharma_manufacturing_quality_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `pharma_manufacturing_quality_pharma_batch`: owns pharma batch lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_master_batch_record`: owns master batch record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_validation_protocol`: owns validation protocol lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_deviation`: owns deviation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_capa`: owns capa lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_quality_release`: owns quality release lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_serialization_event`: owns serialization event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_pharma_manufacturing_quality_policy_rule`: owns pharma manufacturing quality policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_pharma_manufacturing_quality_runtime_parameter`: owns pharma manufacturing quality runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_pharma_manufacturing_quality_schema_extension`: owns pharma manufacturing quality schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_pharma_manufacturing_quality_control_assertion`: owns pharma manufacturing quality control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `pharma_manufacturing_quality_pharma_manufacturing_quality_governed_model`: owns pharma manufacturing quality governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `pharma_manufacturing_quality_appgen_outbox_event`, `pharma_manufacturing_quality_appgen_inbox_event`, and `pharma_manufacturing_quality_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /pharma-batchs', 'POST /master-batch-records', 'POST /validation-protocols', 'POST /deviations', 'POST /capas', 'GET /pharma-manufacturing-quality-workbench').

## Executable Domain Operations

- `create_pharma_batch`: validates policy, writes owned `pharma_manufacturing_quality_pharma_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_master_batch_record`: validates policy, writes owned `pharma_manufacturing_quality_master_batch_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_validation_protocol`: validates policy, writes owned `pharma_manufacturing_quality_validation_protocol` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_deviation`: validates policy, writes owned `pharma_manufacturing_quality_deviation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_capa`: validates policy, writes owned `pharma_manufacturing_quality_capa` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_quality_release`: validates policy, writes owned `pharma_manufacturing_quality_quality_release` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_serialization_event`: validates policy, writes owned `pharma_manufacturing_quality_serialization_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_pharma_manufacturing_quality_policy_rule`: validates policy, writes owned `pharma_manufacturing_quality_pharma_manufacturing_quality_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_pharma_manufacturing_quality_runtime_parameter`: validates policy, writes owned `pharma_manufacturing_quality_pharma_manufacturing_quality_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_pharma_manufacturing_quality_schema_extension`: validates policy, writes owned `pharma_manufacturing_quality_pharma_manufacturing_quality_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_pharma_manufacturing_quality_control_assertion`: validates policy, writes owned `pharma_manufacturing_quality_pharma_manufacturing_quality_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_pharma_manufacturing_quality_governed_model`: validates policy, writes owned `pharma_manufacturing_quality_pharma_manufacturing_quality_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_13`: validates policy, writes owned `pharma_manufacturing_quality_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_14`: validates policy, writes owned `pharma_manufacturing_quality_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_15`: validates policy, writes owned `pharma_manufacturing_quality_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_16`: validates policy, writes owned `pharma_manufacturing_quality_pharma_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_17`: validates policy, writes owned `pharma_manufacturing_quality_master_batch_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_pharma_manufacturing_quality_18`: validates policy, writes owned `pharma_manufacturing_quality_validation_protocol` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Pharma Manufacturing Quality domain records.
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

Rules are first-class artifacts: ('pharma_batch_policy', 'master_batch_record_policy', 'validation_protocol_policy', 'deviation_policy', 'capa_policy', 'quality_release_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /pharma-batchs', 'POST /master-batch-records', 'POST /validation-protocols', 'POST /deviations', 'POST /capas', 'GET /pharma-manufacturing-quality-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `pharma_manufacturing_quality_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PharmaManufacturingQualityCreated', 'PharmaManufacturingQualityUpdated', 'PharmaManufacturingQualityApproved', 'PharmaManufacturingQualityExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('pharma batch board', 'master batch record board', 'validation protocol board', 'deviation board', 'capa board', 'quality release board', 'serialization event board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `pharma_manufacturing_quality_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: pharma_batch, master_batch_record, validation_protocol, deviation, capa, quality_release, serialization_event, pharma_manufacturing_quality_policy_rule, pharma_manufacturing_quality_runtime_parameter, pharma_manufacturing_quality_schema_extension, pharma_manufacturing_quality_control_assertion, pharma_manufacturing_quality_governed_model
- operations: create_pharma_batch, record_master_batch_record, review_validation_protocol, approve_deviation, simulate_capa, create_quality_release, record_serialization_event, review_pharma_manufacturing_quality_policy_rule, approve_pharma_manufacturing_quality_runtime_parameter, simulate_pharma_manufacturing_quality_schema_extension, create_pharma_manufacturing_quality_control_assertion, record_pharma_manufacturing_quality_governed_model, operate_pharma_manufacturing_quality_13, operate_pharma_manufacturing_quality_14, operate_pharma_manufacturing_quality_15, operate_pharma_manufacturing_quality_16, operate_pharma_manufacturing_quality_17, operate_pharma_manufacturing_quality_18
- emits: PharmaManufacturingQualityCreated, PharmaManufacturingQualityUpdated, PharmaManufacturingQualityApproved, PharmaManufacturingQualityExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: pharma_batch_policy, master_batch_record_policy, validation_protocol_policy, deviation_policy, capa_policy, quality_release_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PharmaManufacturingQualityWorkbench, PharmaManufacturingQualityDetail, PharmaManufacturingQualityAssistantPanel
- permissions: pharma_manufacturing_quality.read, pharma_manufacturing_quality.create, pharma_manufacturing_quality.update, pharma_manufacturing_quality.approve, pharma_manufacturing_quality.admin
- configuration: PHARMA_MANUFACTURING_QUALITY_DATABASE_URL, PHARMA_MANUFACTURING_QUALITY_EVENT_TOPIC, PHARMA_MANUFACTURING_QUALITY_RETRY_LIMIT, PHARMA_MANUFACTURING_QUALITY_DEFAULT_POLICY
- standard_features: pharma_batch_management, pharma_manufacturing_quality_workflow, pharma_manufacturing_quality_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: pharma_manufacturing_quality_event_sourced_operational_history, pharma_manufacturing_quality_multi_tenant_policy_isolation, pharma_manufacturing_quality_schema_evolution_resilience, pharma_manufacturing_quality_autonomous_anomaly_detection, pharma_manufacturing_quality_semantic_document_instruction_understanding, pharma_manufacturing_quality_predictive_risk_scoring, pharma_manufacturing_quality_counterfactual_scenario_simulation, pharma_manufacturing_quality_cryptographic_audit_proofs, pharma_manufacturing_quality_continuous_control_testing, pharma_manufacturing_quality_carbon_and_sustainability_awareness, pharma_manufacturing_quality_cross_pbc_event_federation, pharma_manufacturing_quality_governed_ai_agent_execution
