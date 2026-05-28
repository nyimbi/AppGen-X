# Utility Outage Restoration PBC

## Purpose

The `utility_outage_restoration` PBC is a packaged business capability for Outage detection, switching, crew dispatch, restoration estimates, customer impact, and reliability reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `utility_outage_restoration`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/utility_outage_restoration`.
- Runtime entrypoint: `utility_outage_restoration_runtime_capabilities()`.
- UI entrypoint: `utility_outage_restoration_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `utility_outage_restoration_outage_incident`: owns outage incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_device_interruption`: owns device interruption lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_switching_step`: owns switching step lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_crew_assignment`: owns crew assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_restoration_estimate`: owns restoration estimate lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_customer_impact`: owns customer impact lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_reliability_metric`: owns reliability metric lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_utility_outage_restoration_policy_rule`: owns utility outage restoration policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_utility_outage_restoration_runtime_parameter`: owns utility outage restoration runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_utility_outage_restoration_schema_extension`: owns utility outage restoration schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_utility_outage_restoration_control_assertion`: owns utility outage restoration control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `utility_outage_restoration_utility_outage_restoration_governed_model`: owns utility outage restoration governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `utility_outage_restoration_appgen_outbox_event`, `utility_outage_restoration_appgen_inbox_event`, and `utility_outage_restoration_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /outage-incidents', 'POST /device-interruptions', 'POST /switching-steps', 'POST /crew-assignments', 'POST /restoration-estimates', 'GET /utility-outage-restoration-workbench').

## Executable Domain Operations

- `create_outage_incident`: validates policy, writes owned `utility_outage_restoration_outage_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_device_interruption`: validates policy, writes owned `utility_outage_restoration_device_interruption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_switching_step`: validates policy, writes owned `utility_outage_restoration_switching_step` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_crew_assignment`: validates policy, writes owned `utility_outage_restoration_crew_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_restoration_estimate`: validates policy, writes owned `utility_outage_restoration_restoration_estimate` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_customer_impact`: validates policy, writes owned `utility_outage_restoration_customer_impact` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_reliability_metric`: validates policy, writes owned `utility_outage_restoration_reliability_metric` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_utility_outage_restoration_policy_rule`: validates policy, writes owned `utility_outage_restoration_utility_outage_restoration_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_utility_outage_restoration_runtime_parameter`: validates policy, writes owned `utility_outage_restoration_utility_outage_restoration_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_utility_outage_restoration_schema_extension`: validates policy, writes owned `utility_outage_restoration_utility_outage_restoration_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_utility_outage_restoration_control_assertion`: validates policy, writes owned `utility_outage_restoration_utility_outage_restoration_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_utility_outage_restoration_governed_model`: validates policy, writes owned `utility_outage_restoration_utility_outage_restoration_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_13`: validates policy, writes owned `utility_outage_restoration_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_14`: validates policy, writes owned `utility_outage_restoration_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_15`: validates policy, writes owned `utility_outage_restoration_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_16`: validates policy, writes owned `utility_outage_restoration_outage_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_17`: validates policy, writes owned `utility_outage_restoration_device_interruption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_utility_outage_restoration_18`: validates policy, writes owned `utility_outage_restoration_switching_step` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Utility Outage Restoration domain records.
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

Rules are first-class artifacts: ('outage_incident_policy', 'device_interruption_policy', 'switching_step_policy', 'crew_assignment_policy', 'restoration_estimate_policy', 'customer_impact_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /outage-incidents', 'POST /device-interruptions', 'POST /switching-steps', 'POST /crew-assignments', 'POST /restoration-estimates', 'GET /utility-outage-restoration-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `utility_outage_restoration_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('UtilityOutageRestorationCreated', 'UtilityOutageRestorationUpdated', 'UtilityOutageRestorationApproved', 'UtilityOutageRestorationExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('outage incident board', 'device interruption board', 'switching step board', 'crew assignment board', 'restoration estimate board', 'customer impact board', 'reliability metric board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `utility_outage_restoration_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: outage_incident, device_interruption, switching_step, crew_assignment, restoration_estimate, customer_impact, reliability_metric, utility_outage_restoration_policy_rule, utility_outage_restoration_runtime_parameter, utility_outage_restoration_schema_extension, utility_outage_restoration_control_assertion, utility_outage_restoration_governed_model
- operations: create_outage_incident, record_device_interruption, review_switching_step, approve_crew_assignment, simulate_restoration_estimate, create_customer_impact, record_reliability_metric, review_utility_outage_restoration_policy_rule, approve_utility_outage_restoration_runtime_parameter, simulate_utility_outage_restoration_schema_extension, create_utility_outage_restoration_control_assertion, record_utility_outage_restoration_governed_model, operate_utility_outage_restoration_13, operate_utility_outage_restoration_14, operate_utility_outage_restoration_15, operate_utility_outage_restoration_16, operate_utility_outage_restoration_17, operate_utility_outage_restoration_18
- emits: UtilityOutageRestorationCreated, UtilityOutageRestorationUpdated, UtilityOutageRestorationApproved, UtilityOutageRestorationExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: outage_incident_policy, device_interruption_policy, switching_step_policy, crew_assignment_policy, restoration_estimate_policy, customer_impact_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: UtilityOutageRestorationWorkbench, UtilityOutageRestorationDetail, UtilityOutageRestorationAssistantPanel
- permissions: utility_outage_restoration.read, utility_outage_restoration.create, utility_outage_restoration.update, utility_outage_restoration.approve, utility_outage_restoration.admin
- configuration: UTILITY_OUTAGE_RESTORATION_DATABASE_URL, UTILITY_OUTAGE_RESTORATION_EVENT_TOPIC, UTILITY_OUTAGE_RESTORATION_RETRY_LIMIT, UTILITY_OUTAGE_RESTORATION_DEFAULT_POLICY
- standard_features: outage_incident_management, utility_outage_restoration_workflow, utility_outage_restoration_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: utility_outage_restoration_event_sourced_operational_history, utility_outage_restoration_multi_tenant_policy_isolation, utility_outage_restoration_schema_evolution_resilience, utility_outage_restoration_autonomous_anomaly_detection, utility_outage_restoration_semantic_document_instruction_understanding, utility_outage_restoration_predictive_risk_scoring, utility_outage_restoration_counterfactual_scenario_simulation, utility_outage_restoration_cryptographic_audit_proofs, utility_outage_restoration_continuous_control_testing, utility_outage_restoration_carbon_and_sustainability_awareness, utility_outage_restoration_cross_pbc_event_federation, utility_outage_restoration_governed_ai_agent_execution
