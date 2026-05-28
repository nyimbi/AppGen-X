# Real Estate Property Management PBC

## Purpose

The `real_estate_property_management` PBC is a packaged business capability for Properties, leases, tenants, rent, maintenance, inspections, deposits, and property compliance. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `real_estate_property_management`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/real_estate_property_management`.
- Runtime entrypoint: `real_estate_property_management_runtime_capabilities()`.
- UI entrypoint: `real_estate_property_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `real_estate_property_management_property`: owns property lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_tenant`: owns tenant lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_lease`: owns lease lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_rent_charge`: owns rent charge lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_maintenance_request`: owns maintenance request lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_inspection`: owns inspection lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_security_deposit`: owns security deposit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_real_estate_property_management_policy_rule`: owns real estate property management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_real_estate_property_management_runtime_parameter`: owns real estate property management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_real_estate_property_management_schema_extension`: owns real estate property management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_real_estate_property_management_control_assertion`: owns real estate property management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `real_estate_property_management_real_estate_property_management_governed_model`: owns real estate property management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `real_estate_property_management_appgen_outbox_event`, `real_estate_property_management_appgen_inbox_event`, and `real_estate_property_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /propertys', 'POST /tenants', 'POST /leases', 'POST /rent-charges', 'POST /maintenance-requests', 'GET /real-estate-property-management-workbench').

## Executable Domain Operations

- `create_property`: validates policy, writes owned `real_estate_property_management_property` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_tenant`: validates policy, writes owned `real_estate_property_management_tenant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_lease`: validates policy, writes owned `real_estate_property_management_lease` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_rent_charge`: validates policy, writes owned `real_estate_property_management_rent_charge` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_maintenance_request`: validates policy, writes owned `real_estate_property_management_maintenance_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_inspection`: validates policy, writes owned `real_estate_property_management_inspection` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_security_deposit`: validates policy, writes owned `real_estate_property_management_security_deposit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_real_estate_property_management_policy_rule`: validates policy, writes owned `real_estate_property_management_real_estate_property_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_real_estate_property_management_runtime_parameter`: validates policy, writes owned `real_estate_property_management_real_estate_property_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_real_estate_property_management_schema_extension`: validates policy, writes owned `real_estate_property_management_real_estate_property_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_real_estate_property_management_control_assertion`: validates policy, writes owned `real_estate_property_management_real_estate_property_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_real_estate_property_management_governed_model`: validates policy, writes owned `real_estate_property_management_real_estate_property_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_13`: validates policy, writes owned `real_estate_property_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_14`: validates policy, writes owned `real_estate_property_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_15`: validates policy, writes owned `real_estate_property_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_16`: validates policy, writes owned `real_estate_property_management_property` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_17`: validates policy, writes owned `real_estate_property_management_tenant` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_real_estate_property_management_18`: validates policy, writes owned `real_estate_property_management_lease` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Real Estate Property Management domain records.
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

Rules are first-class artifacts: ('property_policy', 'tenant_policy', 'lease_policy', 'rent_charge_policy', 'maintenance_request_policy', 'inspection_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /propertys', 'POST /tenants', 'POST /leases', 'POST /rent-charges', 'POST /maintenance-requests', 'GET /real-estate-property-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `real_estate_property_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('RealEstatePropertyManagementCreated', 'RealEstatePropertyManagementUpdated', 'RealEstatePropertyManagementApproved', 'RealEstatePropertyManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('property board', 'tenant board', 'lease board', 'rent charge board', 'maintenance request board', 'inspection board', 'security deposit board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `real_estate_property_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: property, tenant, lease, rent_charge, maintenance_request, inspection, security_deposit, real_estate_property_management_policy_rule, real_estate_property_management_runtime_parameter, real_estate_property_management_schema_extension, real_estate_property_management_control_assertion, real_estate_property_management_governed_model
- operations: create_property, record_tenant, review_lease, approve_rent_charge, simulate_maintenance_request, create_inspection, record_security_deposit, review_real_estate_property_management_policy_rule, approve_real_estate_property_management_runtime_parameter, simulate_real_estate_property_management_schema_extension, create_real_estate_property_management_control_assertion, record_real_estate_property_management_governed_model, operate_real_estate_property_management_13, operate_real_estate_property_management_14, operate_real_estate_property_management_15, operate_real_estate_property_management_16, operate_real_estate_property_management_17, operate_real_estate_property_management_18
- emits: RealEstatePropertyManagementCreated, RealEstatePropertyManagementUpdated, RealEstatePropertyManagementApproved, RealEstatePropertyManagementExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: property_policy, tenant_policy, lease_policy, rent_charge_policy, maintenance_request_policy, inspection_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: RealEstatePropertyManagementWorkbench, RealEstatePropertyManagementDetail, RealEstatePropertyManagementAssistantPanel
- permissions: real_estate_property_management.read, real_estate_property_management.create, real_estate_property_management.update, real_estate_property_management.approve, real_estate_property_management.admin
- configuration: REAL_ESTATE_PROPERTY_MANAGEMENT_DATABASE_URL, REAL_ESTATE_PROPERTY_MANAGEMENT_EVENT_TOPIC, REAL_ESTATE_PROPERTY_MANAGEMENT_RETRY_LIMIT, REAL_ESTATE_PROPERTY_MANAGEMENT_DEFAULT_POLICY
- standard_features: property_management, real_estate_property_management_workflow, real_estate_property_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: real_estate_property_management_event_sourced_operational_history, real_estate_property_management_multi_tenant_policy_isolation, real_estate_property_management_schema_evolution_resilience, real_estate_property_management_autonomous_anomaly_detection, real_estate_property_management_semantic_document_instruction_understanding, real_estate_property_management_predictive_risk_scoring, real_estate_property_management_counterfactual_scenario_simulation, real_estate_property_management_cryptographic_audit_proofs, real_estate_property_management_continuous_control_testing, real_estate_property_management_carbon_and_sustainability_awareness, real_estate_property_management_cross_pbc_event_federation, real_estate_property_management_governed_ai_agent_execution
