# Reinsurance Management PBC

## Purpose

The `reinsurance_management` PBC is a packaged business capability for Treaties, facultative placements, cessions, recoverables, bordereaux, claims recoveries, and exposure. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `reinsurance_management`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/reinsurance_management`.
- Runtime entrypoint: `reinsurance_management_runtime_capabilities()`.
- UI entrypoint: `reinsurance_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `reinsurance_management_reinsurance_treaty`: owns reinsurance treaty lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_facultative_placement`: owns facultative placement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_cession`: owns cession lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_bordereau`: owns bordereau lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_recoverable`: owns recoverable lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_claim_recovery`: owns claim recovery lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_exposure_layer`: owns exposure layer lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_reinsurance_management_policy_rule`: owns reinsurance management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_reinsurance_management_runtime_parameter`: owns reinsurance management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_reinsurance_management_schema_extension`: owns reinsurance management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_reinsurance_management_control_assertion`: owns reinsurance management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `reinsurance_management_reinsurance_management_governed_model`: owns reinsurance management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `reinsurance_management_appgen_outbox_event`, `reinsurance_management_appgen_inbox_event`, and `reinsurance_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /reinsurance-treatys', 'POST /facultative-placements', 'POST /cessions', 'POST /bordereaus', 'POST /recoverables', 'GET /reinsurance-management-workbench').

## Executable Domain Operations

- `create_reinsurance_treaty`: validates policy, writes owned `reinsurance_management_reinsurance_treaty` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_facultative_placement`: validates policy, writes owned `reinsurance_management_facultative_placement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_cession`: validates policy, writes owned `reinsurance_management_cession` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_bordereau`: validates policy, writes owned `reinsurance_management_bordereau` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_recoverable`: validates policy, writes owned `reinsurance_management_recoverable` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_claim_recovery`: validates policy, writes owned `reinsurance_management_claim_recovery` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_exposure_layer`: validates policy, writes owned `reinsurance_management_exposure_layer` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_reinsurance_management_policy_rule`: validates policy, writes owned `reinsurance_management_reinsurance_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_reinsurance_management_runtime_parameter`: validates policy, writes owned `reinsurance_management_reinsurance_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_reinsurance_management_schema_extension`: validates policy, writes owned `reinsurance_management_reinsurance_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_reinsurance_management_control_assertion`: validates policy, writes owned `reinsurance_management_reinsurance_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_reinsurance_management_governed_model`: validates policy, writes owned `reinsurance_management_reinsurance_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_13`: validates policy, writes owned `reinsurance_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_14`: validates policy, writes owned `reinsurance_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_15`: validates policy, writes owned `reinsurance_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_16`: validates policy, writes owned `reinsurance_management_reinsurance_treaty` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_17`: validates policy, writes owned `reinsurance_management_facultative_placement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_reinsurance_management_18`: validates policy, writes owned `reinsurance_management_cession` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Reinsurance Management domain records.
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

Rules are first-class artifacts: ('reinsurance_treaty_policy', 'facultative_placement_policy', 'cession_policy', 'bordereau_policy', 'recoverable_policy', 'claim_recovery_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /reinsurance-treatys', 'POST /facultative-placements', 'POST /cessions', 'POST /bordereaus', 'POST /recoverables', 'GET /reinsurance-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `reinsurance_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ReinsuranceManagementCreated', 'ReinsuranceManagementUpdated', 'ReinsuranceManagementApproved', 'ReinsuranceManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('reinsurance treaty board', 'facultative placement board', 'cession board', 'bordereau board', 'recoverable board', 'claim recovery board', 'exposure layer board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `reinsurance_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: reinsurance_treaty, facultative_placement, cession, bordereau, recoverable, claim_recovery, exposure_layer, reinsurance_management_policy_rule, reinsurance_management_runtime_parameter, reinsurance_management_schema_extension, reinsurance_management_control_assertion, reinsurance_management_governed_model
- operations: create_reinsurance_treaty, record_facultative_placement, review_cession, approve_bordereau, simulate_recoverable, create_claim_recovery, record_exposure_layer, review_reinsurance_management_policy_rule, approve_reinsurance_management_runtime_parameter, simulate_reinsurance_management_schema_extension, create_reinsurance_management_control_assertion, record_reinsurance_management_governed_model, operate_reinsurance_management_13, operate_reinsurance_management_14, operate_reinsurance_management_15, operate_reinsurance_management_16, operate_reinsurance_management_17, operate_reinsurance_management_18
- emits: ReinsuranceManagementCreated, ReinsuranceManagementUpdated, ReinsuranceManagementApproved, ReinsuranceManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: reinsurance_treaty_policy, facultative_placement_policy, cession_policy, bordereau_policy, recoverable_policy, claim_recovery_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ReinsuranceManagementWorkbench, ReinsuranceManagementDetail, ReinsuranceManagementAssistantPanel
- permissions: reinsurance_management.read, reinsurance_management.create, reinsurance_management.update, reinsurance_management.approve, reinsurance_management.admin
- configuration: REINSURANCE_MANAGEMENT_DATABASE_URL, REINSURANCE_MANAGEMENT_EVENT_TOPIC, REINSURANCE_MANAGEMENT_RETRY_LIMIT, REINSURANCE_MANAGEMENT_DEFAULT_POLICY
- standard_features: reinsurance_treaty_management, reinsurance_management_workflow, reinsurance_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: reinsurance_management_event_sourced_operational_history, reinsurance_management_multi_tenant_policy_isolation, reinsurance_management_schema_evolution_resilience, reinsurance_management_autonomous_anomaly_detection, reinsurance_management_semantic_document_instruction_understanding, reinsurance_management_predictive_risk_scoring, reinsurance_management_counterfactual_scenario_simulation, reinsurance_management_cryptographic_audit_proofs, reinsurance_management_continuous_control_testing, reinsurance_management_carbon_and_sustainability_awareness, reinsurance_management_cross_pbc_event_federation, reinsurance_management_governed_ai_agent_execution
