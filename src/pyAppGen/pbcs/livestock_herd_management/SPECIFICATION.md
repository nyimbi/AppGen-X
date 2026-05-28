# Livestock Herd Management PBC

## Purpose

The `livestock_herd_management` PBC is a packaged business capability for Animals, health, breeding, feed, movements, treatments, compliance, and herd productivity. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `livestock_herd_management`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/livestock_herd_management`.
- Runtime entrypoint: `livestock_herd_management_runtime_capabilities()`.
- UI entrypoint: `livestock_herd_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `livestock_herd_management_animal`: owns animal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_herd_group`: owns herd group lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_health_event`: owns health event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_breeding_record`: owns breeding record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_feed_ration`: owns feed ration lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_movement_permit`: owns movement permit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_treatment`: owns treatment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_livestock_herd_management_policy_rule`: owns livestock herd management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_livestock_herd_management_runtime_parameter`: owns livestock herd management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_livestock_herd_management_schema_extension`: owns livestock herd management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_livestock_herd_management_control_assertion`: owns livestock herd management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `livestock_herd_management_livestock_herd_management_governed_model`: owns livestock herd management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `livestock_herd_management_appgen_outbox_event`, `livestock_herd_management_appgen_inbox_event`, and `livestock_herd_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /animals', 'POST /herd-groups', 'POST /health-events', 'POST /breeding-records', 'POST /feed-rations', 'GET /livestock-herd-management-workbench').

## Executable Domain Operations

- `create_animal`: validates policy, writes owned `livestock_herd_management_animal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_herd_group`: validates policy, writes owned `livestock_herd_management_herd_group` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_health_event`: validates policy, writes owned `livestock_herd_management_health_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_breeding_record`: validates policy, writes owned `livestock_herd_management_breeding_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_feed_ration`: validates policy, writes owned `livestock_herd_management_feed_ration` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_movement_permit`: validates policy, writes owned `livestock_herd_management_movement_permit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_treatment`: validates policy, writes owned `livestock_herd_management_treatment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_livestock_herd_management_policy_rule`: validates policy, writes owned `livestock_herd_management_livestock_herd_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_livestock_herd_management_runtime_parameter`: validates policy, writes owned `livestock_herd_management_livestock_herd_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_livestock_herd_management_schema_extension`: validates policy, writes owned `livestock_herd_management_livestock_herd_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_livestock_herd_management_control_assertion`: validates policy, writes owned `livestock_herd_management_livestock_herd_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_livestock_herd_management_governed_model`: validates policy, writes owned `livestock_herd_management_livestock_herd_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_13`: validates policy, writes owned `livestock_herd_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_14`: validates policy, writes owned `livestock_herd_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_15`: validates policy, writes owned `livestock_herd_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_16`: validates policy, writes owned `livestock_herd_management_animal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_17`: validates policy, writes owned `livestock_herd_management_herd_group` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_livestock_herd_management_18`: validates policy, writes owned `livestock_herd_management_health_event` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Livestock Herd Management domain records.
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

Rules are first-class artifacts: ('animal_policy', 'herd_group_policy', 'health_event_policy', 'breeding_record_policy', 'feed_ration_policy', 'movement_permit_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /animals', 'POST /herd-groups', 'POST /health-events', 'POST /breeding-records', 'POST /feed-rations', 'GET /livestock-herd-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `livestock_herd_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('LivestockHerdManagementCreated', 'LivestockHerdManagementUpdated', 'LivestockHerdManagementApproved', 'LivestockHerdManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('animal board', 'herd group board', 'health event board', 'breeding record board', 'feed ration board', 'movement permit board', 'treatment board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `livestock_herd_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: animal, herd_group, health_event, breeding_record, feed_ration, movement_permit, treatment, livestock_herd_management_policy_rule, livestock_herd_management_runtime_parameter, livestock_herd_management_schema_extension, livestock_herd_management_control_assertion, livestock_herd_management_governed_model
- operations: create_animal, record_herd_group, review_health_event, approve_breeding_record, simulate_feed_ration, create_movement_permit, record_treatment, review_livestock_herd_management_policy_rule, approve_livestock_herd_management_runtime_parameter, simulate_livestock_herd_management_schema_extension, create_livestock_herd_management_control_assertion, record_livestock_herd_management_governed_model, operate_livestock_herd_management_13, operate_livestock_herd_management_14, operate_livestock_herd_management_15, operate_livestock_herd_management_16, operate_livestock_herd_management_17, operate_livestock_herd_management_18
- emits: LivestockHerdManagementCreated, LivestockHerdManagementUpdated, LivestockHerdManagementApproved, LivestockHerdManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: animal_policy, herd_group_policy, health_event_policy, breeding_record_policy, feed_ration_policy, movement_permit_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: LivestockHerdManagementWorkbench, LivestockHerdManagementDetail, LivestockHerdManagementAssistantPanel
- permissions: livestock_herd_management.read, livestock_herd_management.create, livestock_herd_management.update, livestock_herd_management.approve, livestock_herd_management.admin
- configuration: LIVESTOCK_HERD_MANAGEMENT_DATABASE_URL, LIVESTOCK_HERD_MANAGEMENT_EVENT_TOPIC, LIVESTOCK_HERD_MANAGEMENT_RETRY_LIMIT, LIVESTOCK_HERD_MANAGEMENT_DEFAULT_POLICY
- standard_features: animal_management, livestock_herd_management_workflow, livestock_herd_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: livestock_herd_management_event_sourced_operational_history, livestock_herd_management_multi_tenant_policy_isolation, livestock_herd_management_schema_evolution_resilience, livestock_herd_management_autonomous_anomaly_detection, livestock_herd_management_semantic_document_instruction_understanding, livestock_herd_management_predictive_risk_scoring, livestock_herd_management_counterfactual_scenario_simulation, livestock_herd_management_cryptographic_audit_proofs, livestock_herd_management_continuous_control_testing, livestock_herd_management_carbon_and_sustainability_awareness, livestock_herd_management_cross_pbc_event_federation, livestock_herd_management_governed_ai_agent_execution
