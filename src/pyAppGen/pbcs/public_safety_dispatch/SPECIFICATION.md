# Public Safety Dispatch PBC

## Purpose

The `public_safety_dispatch` PBC is a packaged business capability for Emergency calls, units, incidents, dispatch, mutual aid, response times, and public safety operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `public_safety_dispatch`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/public_safety_dispatch`.
- Runtime entrypoint: `public_safety_dispatch_runtime_capabilities()`.
- UI entrypoint: `public_safety_dispatch_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `public_safety_dispatch_emergency_call`: owns emergency call lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_response_unit`: owns response unit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_incident`: owns incident lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_dispatch_assignment`: owns dispatch assignment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_mutual_aid`: owns mutual aid lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_response_milestone`: owns response milestone lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_case_disposition`: owns case disposition lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_public_safety_dispatch_policy_rule`: owns public safety dispatch policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_public_safety_dispatch_runtime_parameter`: owns public safety dispatch runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_public_safety_dispatch_schema_extension`: owns public safety dispatch schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_public_safety_dispatch_control_assertion`: owns public safety dispatch control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `public_safety_dispatch_public_safety_dispatch_governed_model`: owns public safety dispatch governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `public_safety_dispatch_appgen_outbox_event`, `public_safety_dispatch_appgen_inbox_event`, and `public_safety_dispatch_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /emergency-calls', 'POST /response-units', 'POST /incidents', 'POST /dispatch-assignments', 'POST /mutual-aids', 'GET /public-safety-dispatch-workbench').

## Executable Domain Operations

- `create_emergency_call`: validates policy, writes owned `public_safety_dispatch_emergency_call` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_response_unit`: validates policy, writes owned `public_safety_dispatch_response_unit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_incident`: validates policy, writes owned `public_safety_dispatch_incident` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_dispatch_assignment`: validates policy, writes owned `public_safety_dispatch_dispatch_assignment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_mutual_aid`: validates policy, writes owned `public_safety_dispatch_mutual_aid` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_response_milestone`: validates policy, writes owned `public_safety_dispatch_response_milestone` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_case_disposition`: validates policy, writes owned `public_safety_dispatch_case_disposition` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_public_safety_dispatch_policy_rule`: validates policy, writes owned `public_safety_dispatch_public_safety_dispatch_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_public_safety_dispatch_runtime_parameter`: validates policy, writes owned `public_safety_dispatch_public_safety_dispatch_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_public_safety_dispatch_schema_extension`: validates policy, writes owned `public_safety_dispatch_public_safety_dispatch_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_public_safety_dispatch_control_assertion`: validates policy, writes owned `public_safety_dispatch_public_safety_dispatch_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_public_safety_dispatch_governed_model`: validates policy, writes owned `public_safety_dispatch_public_safety_dispatch_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_13`: validates policy, writes owned `public_safety_dispatch_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_14`: validates policy, writes owned `public_safety_dispatch_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_15`: validates policy, writes owned `public_safety_dispatch_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_16`: validates policy, writes owned `public_safety_dispatch_emergency_call` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_17`: validates policy, writes owned `public_safety_dispatch_response_unit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_public_safety_dispatch_18`: validates policy, writes owned `public_safety_dispatch_incident` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Public Safety Dispatch domain records.
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

Rules are first-class artifacts: ('emergency_call_policy', 'response_unit_policy', 'incident_policy', 'dispatch_assignment_policy', 'mutual_aid_policy', 'response_milestone_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /emergency-calls', 'POST /response-units', 'POST /incidents', 'POST /dispatch-assignments', 'POST /mutual-aids', 'GET /public-safety-dispatch-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `public_safety_dispatch_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PublicSafetyDispatchCreated', 'PublicSafetyDispatchUpdated', 'PublicSafetyDispatchApproved', 'PublicSafetyDispatchExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('emergency call board', 'response unit board', 'incident board', 'dispatch assignment board', 'mutual aid board', 'response milestone board', 'case disposition board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `public_safety_dispatch_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: emergency_call, response_unit, incident, dispatch_assignment, mutual_aid, response_milestone, case_disposition, public_safety_dispatch_policy_rule, public_safety_dispatch_runtime_parameter, public_safety_dispatch_schema_extension, public_safety_dispatch_control_assertion, public_safety_dispatch_governed_model
- operations: create_emergency_call, record_response_unit, review_incident, approve_dispatch_assignment, simulate_mutual_aid, create_response_milestone, record_case_disposition, review_public_safety_dispatch_policy_rule, approve_public_safety_dispatch_runtime_parameter, simulate_public_safety_dispatch_schema_extension, create_public_safety_dispatch_control_assertion, record_public_safety_dispatch_governed_model, operate_public_safety_dispatch_13, operate_public_safety_dispatch_14, operate_public_safety_dispatch_15, operate_public_safety_dispatch_16, operate_public_safety_dispatch_17, operate_public_safety_dispatch_18
- emits: PublicSafetyDispatchCreated, PublicSafetyDispatchUpdated, PublicSafetyDispatchApproved, PublicSafetyDispatchExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: emergency_call_policy, response_unit_policy, incident_policy, dispatch_assignment_policy, mutual_aid_policy, response_milestone_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PublicSafetyDispatchWorkbench, PublicSafetyDispatchDetail, PublicSafetyDispatchAssistantPanel
- permissions: public_safety_dispatch.read, public_safety_dispatch.create, public_safety_dispatch.update, public_safety_dispatch.approve, public_safety_dispatch.admin
- configuration: PUBLIC_SAFETY_DISPATCH_DATABASE_URL, PUBLIC_SAFETY_DISPATCH_EVENT_TOPIC, PUBLIC_SAFETY_DISPATCH_RETRY_LIMIT, PUBLIC_SAFETY_DISPATCH_DEFAULT_POLICY
- standard_features: emergency_call_management, public_safety_dispatch_workflow, public_safety_dispatch_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: public_safety_dispatch_event_sourced_operational_history, public_safety_dispatch_multi_tenant_policy_isolation, public_safety_dispatch_schema_evolution_resilience, public_safety_dispatch_autonomous_anomaly_detection, public_safety_dispatch_semantic_document_instruction_understanding, public_safety_dispatch_predictive_risk_scoring, public_safety_dispatch_counterfactual_scenario_simulation, public_safety_dispatch_cryptographic_audit_proofs, public_safety_dispatch_continuous_control_testing, public_safety_dispatch_carbon_and_sustainability_awareness, public_safety_dispatch_cross_pbc_event_federation, public_safety_dispatch_governed_ai_agent_execution
