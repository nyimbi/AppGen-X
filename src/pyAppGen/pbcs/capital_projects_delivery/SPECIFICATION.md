# Capital Projects Delivery PBC

## Purpose

The `capital_projects_delivery` PBC is a packaged business capability for Megaproject governance, EPC packages, permits, progress, commissioning, risk, and capital delivery controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `capital_projects_delivery`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/capital_projects_delivery`.
- Runtime entrypoint: `capital_projects_delivery_runtime_capabilities()`.
- UI entrypoint: `capital_projects_delivery_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `capital_projects_delivery_capital_project`: owns capital project lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_epc_package`: owns epc package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_permit_milestone`: owns permit milestone lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_progress_measurement`: owns progress measurement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_commissioning_system`: owns commissioning system lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_project_risk`: owns project risk lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_turnover_package`: owns turnover package lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_capital_projects_delivery_policy_rule`: owns capital projects delivery policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_capital_projects_delivery_runtime_parameter`: owns capital projects delivery runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_capital_projects_delivery_schema_extension`: owns capital projects delivery schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_capital_projects_delivery_control_assertion`: owns capital projects delivery control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `capital_projects_delivery_capital_projects_delivery_governed_model`: owns capital projects delivery governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `capital_projects_delivery_appgen_outbox_event`, `capital_projects_delivery_appgen_inbox_event`, and `capital_projects_delivery_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /capital-projects', 'POST /epc-packages', 'POST /permit-milestones', 'POST /progress-measurements', 'POST /commissioning-systems', 'GET /capital-projects-delivery-workbench').

## Executable Domain Operations

- `create_capital_project`: validates policy, writes owned `capital_projects_delivery_capital_project` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_epc_package`: validates policy, writes owned `capital_projects_delivery_epc_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_permit_milestone`: validates policy, writes owned `capital_projects_delivery_permit_milestone` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_progress_measurement`: validates policy, writes owned `capital_projects_delivery_progress_measurement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_commissioning_system`: validates policy, writes owned `capital_projects_delivery_commissioning_system` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_project_risk`: validates policy, writes owned `capital_projects_delivery_project_risk` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_turnover_package`: validates policy, writes owned `capital_projects_delivery_turnover_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_capital_projects_delivery_policy_rule`: validates policy, writes owned `capital_projects_delivery_capital_projects_delivery_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_capital_projects_delivery_runtime_parameter`: validates policy, writes owned `capital_projects_delivery_capital_projects_delivery_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_capital_projects_delivery_schema_extension`: validates policy, writes owned `capital_projects_delivery_capital_projects_delivery_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_capital_projects_delivery_control_assertion`: validates policy, writes owned `capital_projects_delivery_capital_projects_delivery_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_capital_projects_delivery_governed_model`: validates policy, writes owned `capital_projects_delivery_capital_projects_delivery_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_13`: validates policy, writes owned `capital_projects_delivery_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_14`: validates policy, writes owned `capital_projects_delivery_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_15`: validates policy, writes owned `capital_projects_delivery_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_16`: validates policy, writes owned `capital_projects_delivery_capital_project` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_17`: validates policy, writes owned `capital_projects_delivery_epc_package` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_capital_projects_delivery_18`: validates policy, writes owned `capital_projects_delivery_permit_milestone` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Capital Projects Delivery domain records.
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

Rules are first-class artifacts: ('capital_project_policy', 'epc_package_policy', 'permit_milestone_policy', 'progress_measurement_policy', 'commissioning_system_policy', 'project_risk_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /capital-projects', 'POST /epc-packages', 'POST /permit-milestones', 'POST /progress-measurements', 'POST /commissioning-systems', 'GET /capital-projects-delivery-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `capital_projects_delivery_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('CapitalProjectsDeliveryCreated', 'CapitalProjectsDeliveryUpdated', 'CapitalProjectsDeliveryApproved', 'CapitalProjectsDeliveryExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('capital project board', 'epc package board', 'permit milestone board', 'progress measurement board', 'commissioning system board', 'project risk board', 'turnover package board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `capital_projects_delivery_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: capital_project, epc_package, permit_milestone, progress_measurement, commissioning_system, project_risk, turnover_package, capital_projects_delivery_policy_rule, capital_projects_delivery_runtime_parameter, capital_projects_delivery_schema_extension, capital_projects_delivery_control_assertion, capital_projects_delivery_governed_model
- operations: create_capital_project, record_epc_package, review_permit_milestone, approve_progress_measurement, simulate_commissioning_system, create_project_risk, record_turnover_package, review_capital_projects_delivery_policy_rule, approve_capital_projects_delivery_runtime_parameter, simulate_capital_projects_delivery_schema_extension, create_capital_projects_delivery_control_assertion, record_capital_projects_delivery_governed_model, operate_capital_projects_delivery_13, operate_capital_projects_delivery_14, operate_capital_projects_delivery_15, operate_capital_projects_delivery_16, operate_capital_projects_delivery_17, operate_capital_projects_delivery_18
- emits: CapitalProjectsDeliveryCreated, CapitalProjectsDeliveryUpdated, CapitalProjectsDeliveryApproved, CapitalProjectsDeliveryExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: capital_project_policy, epc_package_policy, permit_milestone_policy, progress_measurement_policy, commissioning_system_policy, project_risk_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: CapitalProjectsDeliveryWorkbench, CapitalProjectsDeliveryDetail, CapitalProjectsDeliveryAssistantPanel
- permissions: capital_projects_delivery.read, capital_projects_delivery.create, capital_projects_delivery.update, capital_projects_delivery.approve, capital_projects_delivery.admin
- configuration: CAPITAL_PROJECTS_DELIVERY_DATABASE_URL, CAPITAL_PROJECTS_DELIVERY_EVENT_TOPIC, CAPITAL_PROJECTS_DELIVERY_RETRY_LIMIT, CAPITAL_PROJECTS_DELIVERY_DEFAULT_POLICY
- standard_features: capital_project_management, capital_projects_delivery_workflow, capital_projects_delivery_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: capital_projects_delivery_event_sourced_operational_history, capital_projects_delivery_multi_tenant_policy_isolation, capital_projects_delivery_schema_evolution_resilience, capital_projects_delivery_autonomous_anomaly_detection, capital_projects_delivery_semantic_document_instruction_understanding, capital_projects_delivery_predictive_risk_scoring, capital_projects_delivery_counterfactual_scenario_simulation, capital_projects_delivery_cryptographic_audit_proofs, capital_projects_delivery_continuous_control_testing, capital_projects_delivery_carbon_and_sustainability_awareness, capital_projects_delivery_cross_pbc_event_federation, capital_projects_delivery_governed_ai_agent_execution
