# Humanitarian Relief Operations PBC

## Purpose

The `humanitarian_relief_operations` PBC is a packaged business capability for Needs assessment, aid distribution, logistics, protection, field partners, donor reporting, and relief accountability. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `humanitarian_relief_operations`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/humanitarian_relief_operations`.
- Runtime entrypoint: `humanitarian_relief_operations_runtime_capabilities()`.
- UI entrypoint: `humanitarian_relief_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `humanitarian_relief_operations_needs_assessment`: owns needs assessment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_aid_item`: owns aid item lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_distribution_event`: owns distribution event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_field_partner`: owns field partner lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_protection_case`: owns protection case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_relief_shipment`: owns relief shipment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_donor_accountability`: owns donor accountability lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_humanitarian_relief_operations_policy_rule`: owns humanitarian relief operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_humanitarian_relief_operations_runtime_parameter`: owns humanitarian relief operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_humanitarian_relief_operations_schema_extension`: owns humanitarian relief operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_humanitarian_relief_operations_control_assertion`: owns humanitarian relief operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `humanitarian_relief_operations_humanitarian_relief_operations_governed_model`: owns humanitarian relief operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `humanitarian_relief_operations_appgen_outbox_event`, `humanitarian_relief_operations_appgen_inbox_event`, and `humanitarian_relief_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /needs-assessments', 'POST /aid-items', 'POST /distribution-events', 'POST /field-partners', 'POST /protection-cases', 'GET /humanitarian-relief-operations-workbench').

## Executable Domain Operations

- `create_needs_assessment`: validates policy, writes owned `humanitarian_relief_operations_needs_assessment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_aid_item`: validates policy, writes owned `humanitarian_relief_operations_aid_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_distribution_event`: validates policy, writes owned `humanitarian_relief_operations_distribution_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_field_partner`: validates policy, writes owned `humanitarian_relief_operations_field_partner` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_protection_case`: validates policy, writes owned `humanitarian_relief_operations_protection_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_relief_shipment`: validates policy, writes owned `humanitarian_relief_operations_relief_shipment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_donor_accountability`: validates policy, writes owned `humanitarian_relief_operations_donor_accountability` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_humanitarian_relief_operations_policy_rule`: validates policy, writes owned `humanitarian_relief_operations_humanitarian_relief_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_humanitarian_relief_operations_runtime_parameter`: validates policy, writes owned `humanitarian_relief_operations_humanitarian_relief_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_humanitarian_relief_operations_schema_extension`: validates policy, writes owned `humanitarian_relief_operations_humanitarian_relief_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_humanitarian_relief_operations_control_assertion`: validates policy, writes owned `humanitarian_relief_operations_humanitarian_relief_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_humanitarian_relief_operations_governed_model`: validates policy, writes owned `humanitarian_relief_operations_humanitarian_relief_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_13`: validates policy, writes owned `humanitarian_relief_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_14`: validates policy, writes owned `humanitarian_relief_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_15`: validates policy, writes owned `humanitarian_relief_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_16`: validates policy, writes owned `humanitarian_relief_operations_needs_assessment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_17`: validates policy, writes owned `humanitarian_relief_operations_aid_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_humanitarian_relief_operations_18`: validates policy, writes owned `humanitarian_relief_operations_distribution_event` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Humanitarian Relief Operations domain records.
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

Rules are first-class artifacts: ('needs_assessment_policy', 'aid_item_policy', 'distribution_event_policy', 'field_partner_policy', 'protection_case_policy', 'relief_shipment_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /needs-assessments', 'POST /aid-items', 'POST /distribution-events', 'POST /field-partners', 'POST /protection-cases', 'GET /humanitarian-relief-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `humanitarian_relief_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('HumanitarianReliefOperationsCreated', 'HumanitarianReliefOperationsUpdated', 'HumanitarianReliefOperationsApproved', 'HumanitarianReliefOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('needs assessment board', 'aid item board', 'distribution event board', 'field partner board', 'protection case board', 'relief shipment board', 'donor accountability board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `humanitarian_relief_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: needs_assessment, aid_item, distribution_event, field_partner, protection_case, relief_shipment, donor_accountability, humanitarian_relief_operations_policy_rule, humanitarian_relief_operations_runtime_parameter, humanitarian_relief_operations_schema_extension, humanitarian_relief_operations_control_assertion, humanitarian_relief_operations_governed_model
- operations: create_needs_assessment, record_aid_item, review_distribution_event, approve_field_partner, simulate_protection_case, create_relief_shipment, record_donor_accountability, review_humanitarian_relief_operations_policy_rule, approve_humanitarian_relief_operations_runtime_parameter, simulate_humanitarian_relief_operations_schema_extension, create_humanitarian_relief_operations_control_assertion, record_humanitarian_relief_operations_governed_model, operate_humanitarian_relief_operations_13, operate_humanitarian_relief_operations_14, operate_humanitarian_relief_operations_15, operate_humanitarian_relief_operations_16, operate_humanitarian_relief_operations_17, operate_humanitarian_relief_operations_18
- emits: HumanitarianReliefOperationsCreated, HumanitarianReliefOperationsUpdated, HumanitarianReliefOperationsApproved, HumanitarianReliefOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: needs_assessment_policy, aid_item_policy, distribution_event_policy, field_partner_policy, protection_case_policy, relief_shipment_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: HumanitarianReliefOperationsWorkbench, HumanitarianReliefOperationsDetail, HumanitarianReliefOperationsAssistantPanel
- permissions: humanitarian_relief_operations.read, humanitarian_relief_operations.create, humanitarian_relief_operations.update, humanitarian_relief_operations.approve, humanitarian_relief_operations.admin
- configuration: HUMANITARIAN_RELIEF_OPERATIONS_DATABASE_URL, HUMANITARIAN_RELIEF_OPERATIONS_EVENT_TOPIC, HUMANITARIAN_RELIEF_OPERATIONS_RETRY_LIMIT, HUMANITARIAN_RELIEF_OPERATIONS_DEFAULT_POLICY
- standard_features: needs_assessment_management, humanitarian_relief_operations_workflow, humanitarian_relief_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: humanitarian_relief_operations_event_sourced_operational_history, humanitarian_relief_operations_multi_tenant_policy_isolation, humanitarian_relief_operations_schema_evolution_resilience, humanitarian_relief_operations_autonomous_anomaly_detection, humanitarian_relief_operations_semantic_document_instruction_understanding, humanitarian_relief_operations_predictive_risk_scoring, humanitarian_relief_operations_counterfactual_scenario_simulation, humanitarian_relief_operations_cryptographic_audit_proofs, humanitarian_relief_operations_continuous_control_testing, humanitarian_relief_operations_carbon_and_sustainability_awareness, humanitarian_relief_operations_cross_pbc_event_federation, humanitarian_relief_operations_governed_ai_agent_execution
