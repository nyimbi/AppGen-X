# Food Safety Quality Compliance PBC

## Purpose

The `food_safety_quality_compliance` PBC is a packaged business capability for HACCP plans, inspections, nonconformance, recalls, supplier audits, food quality, and regulatory evidence. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `food_safety_quality_compliance`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/food_safety_quality_compliance`.
- Runtime entrypoint: `food_safety_quality_compliance_runtime_capabilities()`.
- UI entrypoint: `food_safety_quality_compliance_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `food_safety_quality_compliance_haccp_plan`: owns haccp plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_critical_control_point`: owns critical control point lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_inspection`: owns inspection lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_nonconformance`: owns nonconformance lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_recall_event`: owns recall event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_supplier_audit`: owns supplier audit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_quality_hold`: owns quality hold lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_food_safety_quality_compliance_policy_rule`: owns food safety quality compliance policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter`: owns food safety quality compliance runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_food_safety_quality_compliance_schema_extension`: owns food safety quality compliance schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_food_safety_quality_compliance_control_assertion`: owns food safety quality compliance control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `food_safety_quality_compliance_food_safety_quality_compliance_governed_model`: owns food safety quality compliance governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `food_safety_quality_compliance_appgen_outbox_event`, `food_safety_quality_compliance_appgen_inbox_event`, and `food_safety_quality_compliance_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /haccp-plans', 'POST /critical-control-points', 'POST /inspections', 'POST /nonconformances', 'POST /recall-events', 'GET /food-safety-quality-compliance-workbench').

## Executable Domain Operations

- `create_haccp_plan`: validates policy, writes owned `food_safety_quality_compliance_haccp_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_critical_control_point`: validates policy, writes owned `food_safety_quality_compliance_critical_control_point` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_inspection`: validates policy, writes owned `food_safety_quality_compliance_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_nonconformance`: validates policy, writes owned `food_safety_quality_compliance_nonconformance` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_recall_event`: validates policy, writes owned `food_safety_quality_compliance_recall_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_supplier_audit`: validates policy, writes owned `food_safety_quality_compliance_supplier_audit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_quality_hold`: validates policy, writes owned `food_safety_quality_compliance_quality_hold` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_food_safety_quality_compliance_policy_rule`: validates policy, writes owned `food_safety_quality_compliance_food_safety_quality_compliance_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_food_safety_quality_compliance_runtime_parameter`: validates policy, writes owned `food_safety_quality_compliance_food_safety_quality_compliance_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_food_safety_quality_compliance_schema_extension`: validates policy, writes owned `food_safety_quality_compliance_food_safety_quality_compliance_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_food_safety_quality_compliance_control_assertion`: validates policy, writes owned `food_safety_quality_compliance_food_safety_quality_compliance_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_food_safety_quality_compliance_governed_model`: validates policy, writes owned `food_safety_quality_compliance_food_safety_quality_compliance_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_13`: validates policy, writes owned `food_safety_quality_compliance_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_14`: validates policy, writes owned `food_safety_quality_compliance_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_15`: validates policy, writes owned `food_safety_quality_compliance_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_16`: validates policy, writes owned `food_safety_quality_compliance_haccp_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_17`: validates policy, writes owned `food_safety_quality_compliance_critical_control_point` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_food_safety_quality_compliance_18`: validates policy, writes owned `food_safety_quality_compliance_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Food Safety Quality Compliance domain records.
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

Rules are first-class artifacts: ('haccp_plan_policy', 'critical_control_point_policy', 'inspection_policy', 'nonconformance_policy', 'recall_event_policy', 'supplier_audit_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /haccp-plans', 'POST /critical-control-points', 'POST /inspections', 'POST /nonconformances', 'POST /recall-events', 'GET /food-safety-quality-compliance-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `food_safety_quality_compliance_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('FoodSafetyQualityComplianceCreated', 'FoodSafetyQualityComplianceUpdated', 'FoodSafetyQualityComplianceApproved', 'FoodSafetyQualityComplianceExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('haccp plan board', 'critical control point board', 'inspection board', 'nonconformance board', 'recall event board', 'supplier audit board', 'quality hold board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `food_safety_quality_compliance_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: haccp_plan, critical_control_point, inspection, nonconformance, recall_event, supplier_audit, quality_hold, food_safety_quality_compliance_policy_rule, food_safety_quality_compliance_runtime_parameter, food_safety_quality_compliance_schema_extension, food_safety_quality_compliance_control_assertion, food_safety_quality_compliance_governed_model
- operations: create_haccp_plan, record_critical_control_point, review_inspection, approve_nonconformance, simulate_recall_event, create_supplier_audit, record_quality_hold, review_food_safety_quality_compliance_policy_rule, approve_food_safety_quality_compliance_runtime_parameter, simulate_food_safety_quality_compliance_schema_extension, create_food_safety_quality_compliance_control_assertion, record_food_safety_quality_compliance_governed_model, operate_food_safety_quality_compliance_13, operate_food_safety_quality_compliance_14, operate_food_safety_quality_compliance_15, operate_food_safety_quality_compliance_16, operate_food_safety_quality_compliance_17, operate_food_safety_quality_compliance_18
- emits: FoodSafetyQualityComplianceCreated, FoodSafetyQualityComplianceUpdated, FoodSafetyQualityComplianceApproved, FoodSafetyQualityComplianceExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: haccp_plan_policy, critical_control_point_policy, inspection_policy, nonconformance_policy, recall_event_policy, supplier_audit_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: FoodSafetyQualityComplianceWorkbench, FoodSafetyQualityComplianceDetail, FoodSafetyQualityComplianceAssistantPanel
- permissions: food_safety_quality_compliance.read, food_safety_quality_compliance.create, food_safety_quality_compliance.update, food_safety_quality_compliance.approve, food_safety_quality_compliance.admin
- configuration: FOOD_SAFETY_QUALITY_COMPLIANCE_DATABASE_URL, FOOD_SAFETY_QUALITY_COMPLIANCE_EVENT_TOPIC, FOOD_SAFETY_QUALITY_COMPLIANCE_RETRY_LIMIT, FOOD_SAFETY_QUALITY_COMPLIANCE_DEFAULT_POLICY
- standard_features: haccp_plan_management, food_safety_quality_compliance_workflow, food_safety_quality_compliance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: food_safety_quality_compliance_event_sourced_operational_history, food_safety_quality_compliance_multi_tenant_policy_isolation, food_safety_quality_compliance_schema_evolution_resilience, food_safety_quality_compliance_autonomous_anomaly_detection, food_safety_quality_compliance_semantic_document_instruction_understanding, food_safety_quality_compliance_predictive_risk_scoring, food_safety_quality_compliance_counterfactual_scenario_simulation, food_safety_quality_compliance_cryptographic_audit_proofs, food_safety_quality_compliance_continuous_control_testing, food_safety_quality_compliance_carbon_and_sustainability_awareness, food_safety_quality_compliance_cross_pbc_event_federation, food_safety_quality_compliance_governed_ai_agent_execution
