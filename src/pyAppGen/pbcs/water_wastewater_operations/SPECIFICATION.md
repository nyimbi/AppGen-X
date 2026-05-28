# Water and Wastewater Operations PBC

## Purpose

The `water_wastewater_operations` PBC is a packaged business capability for Treatment plants, water quality, permits, assets, service interruptions, field work, and compliance reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `water_wastewater_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/water_wastewater_operations`.
- Runtime entrypoint: `water_wastewater_operations_runtime_capabilities()`.
- UI entrypoint: `water_wastewater_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `water_wastewater_operations_treatment_plant`: owns treatment plant lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_quality_sample`: owns water quality sample lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_permit_limit`: owns permit limit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_pump_asset`: owns pump asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_service_interruption`: owns service interruption lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_field_work_order`: owns field work order lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_compliance_sample`: owns compliance sample lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_wastewater_operations_policy_rule`: owns water wastewater operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_wastewater_operations_runtime_parameter`: owns water wastewater operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_wastewater_operations_schema_extension`: owns water wastewater operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_wastewater_operations_control_assertion`: owns water wastewater operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `water_wastewater_operations_water_wastewater_operations_governed_model`: owns water wastewater operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `water_wastewater_operations_appgen_outbox_event`, `water_wastewater_operations_appgen_inbox_event`, and `water_wastewater_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /treatment-plants', 'POST /water-quality-samples', 'POST /permit-limits', 'POST /pump-assets', 'POST /service-interruptions', 'GET /water-wastewater-operations-workbench').

## Executable Domain Operations

- `create_treatment_plant`: validates policy, writes owned `water_wastewater_operations_treatment_plant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_water_quality_sample`: validates policy, writes owned `water_wastewater_operations_water_quality_sample` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_permit_limit`: validates policy, writes owned `water_wastewater_operations_permit_limit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_pump_asset`: validates policy, writes owned `water_wastewater_operations_pump_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_service_interruption`: validates policy, writes owned `water_wastewater_operations_service_interruption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_field_work_order`: validates policy, writes owned `water_wastewater_operations_field_work_order` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_compliance_sample`: validates policy, writes owned `water_wastewater_operations_compliance_sample` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_water_wastewater_operations_policy_rule`: validates policy, writes owned `water_wastewater_operations_water_wastewater_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_water_wastewater_operations_runtime_parameter`: validates policy, writes owned `water_wastewater_operations_water_wastewater_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_water_wastewater_operations_schema_extension`: validates policy, writes owned `water_wastewater_operations_water_wastewater_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_water_wastewater_operations_control_assertion`: validates policy, writes owned `water_wastewater_operations_water_wastewater_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_water_wastewater_operations_governed_model`: validates policy, writes owned `water_wastewater_operations_water_wastewater_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_13`: validates policy, writes owned `water_wastewater_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_14`: validates policy, writes owned `water_wastewater_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_15`: validates policy, writes owned `water_wastewater_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_16`: validates policy, writes owned `water_wastewater_operations_treatment_plant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_17`: validates policy, writes owned `water_wastewater_operations_water_quality_sample` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_water_wastewater_operations_18`: validates policy, writes owned `water_wastewater_operations_permit_limit` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Water and Wastewater Operations domain records.
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

Rules are first-class artifacts: ('treatment_plant_policy', 'water_quality_sample_policy', 'permit_limit_policy', 'pump_asset_policy', 'service_interruption_policy', 'field_work_order_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /treatment-plants', 'POST /water-quality-samples', 'POST /permit-limits', 'POST /pump-assets', 'POST /service-interruptions', 'GET /water-wastewater-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `water_wastewater_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('WaterWastewaterOperationsCreated', 'WaterWastewaterOperationsUpdated', 'WaterWastewaterOperationsApproved', 'WaterWastewaterOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('treatment plant board', 'water quality sample board', 'permit limit board', 'pump asset board', 'service interruption board', 'field work order board', 'compliance sample board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `water_wastewater_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: treatment_plant, water_quality_sample, permit_limit, pump_asset, service_interruption, field_work_order, compliance_sample, water_wastewater_operations_policy_rule, water_wastewater_operations_runtime_parameter, water_wastewater_operations_schema_extension, water_wastewater_operations_control_assertion, water_wastewater_operations_governed_model
- operations: create_treatment_plant, record_water_quality_sample, review_permit_limit, approve_pump_asset, simulate_service_interruption, create_field_work_order, record_compliance_sample, review_water_wastewater_operations_policy_rule, approve_water_wastewater_operations_runtime_parameter, simulate_water_wastewater_operations_schema_extension, create_water_wastewater_operations_control_assertion, record_water_wastewater_operations_governed_model, operate_water_wastewater_operations_13, operate_water_wastewater_operations_14, operate_water_wastewater_operations_15, operate_water_wastewater_operations_16, operate_water_wastewater_operations_17, operate_water_wastewater_operations_18
- emits: WaterWastewaterOperationsCreated, WaterWastewaterOperationsUpdated, WaterWastewaterOperationsApproved, WaterWastewaterOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: treatment_plant_policy, water_quality_sample_policy, permit_limit_policy, pump_asset_policy, service_interruption_policy, field_work_order_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: WaterWastewaterOperationsWorkbench, WaterWastewaterOperationsDetail, WaterWastewaterOperationsAssistantPanel
- permissions: water_wastewater_operations.read, water_wastewater_operations.create, water_wastewater_operations.update, water_wastewater_operations.approve, water_wastewater_operations.admin
- configuration: WATER_WASTEWATER_OPERATIONS_DATABASE_URL, WATER_WASTEWATER_OPERATIONS_EVENT_TOPIC, WATER_WASTEWATER_OPERATIONS_RETRY_LIMIT, WATER_WASTEWATER_OPERATIONS_DEFAULT_POLICY
- standard_features: treatment_plant_management, water_wastewater_operations_workflow, water_wastewater_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: water_wastewater_operations_event_sourced_operational_history, water_wastewater_operations_multi_tenant_policy_isolation, water_wastewater_operations_schema_evolution_resilience, water_wastewater_operations_autonomous_anomaly_detection, water_wastewater_operations_semantic_document_instruction_understanding, water_wastewater_operations_predictive_risk_scoring, water_wastewater_operations_counterfactual_scenario_simulation, water_wastewater_operations_cryptographic_audit_proofs, water_wastewater_operations_continuous_control_testing, water_wastewater_operations_carbon_and_sustainability_awareness, water_wastewater_operations_cross_pbc_event_federation, water_wastewater_operations_governed_ai_agent_execution
