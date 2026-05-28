# Actuarial Pricing and Reserving PBC

## Purpose

The `actuarial_pricing_reserving` PBC is a packaged business capability for Rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `actuarial_pricing_reserving`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/actuarial_pricing_reserving`.
- Runtime entrypoint: `actuarial_pricing_reserving_runtime_capabilities()`.
- UI entrypoint: `actuarial_pricing_reserving_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `actuarial_pricing_reserving_rating_model`: owns rating model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_assumption`: owns actuarial assumption lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_experience_study`: owns experience study lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_reserve_estimate`: owns reserve estimate lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_loss_triangle`: owns loss triangle lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_capital_scenario`: owns capital scenario lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_model_validation`: owns model validation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_pricing_reserving_policy_rule`: owns actuarial pricing reserving policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_pricing_reserving_runtime_parameter`: owns actuarial pricing reserving runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_pricing_reserving_schema_extension`: owns actuarial pricing reserving schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_pricing_reserving_control_assertion`: owns actuarial pricing reserving control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `actuarial_pricing_reserving_actuarial_pricing_reserving_governed_model`: owns actuarial pricing reserving governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `actuarial_pricing_reserving_appgen_outbox_event`, `actuarial_pricing_reserving_appgen_inbox_event`, and `actuarial_pricing_reserving_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /rating-models', 'POST /actuarial-assumptions', 'POST /experience-studys', 'POST /reserve-estimates', 'POST /loss-triangles', 'GET /actuarial-pricing-reserving-workbench').

## Executable Domain Operations

- `create_rating_model`: validates policy, writes owned `actuarial_pricing_reserving_rating_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_actuarial_assumption`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_assumption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_experience_study`: validates policy, writes owned `actuarial_pricing_reserving_experience_study` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_reserve_estimate`: validates policy, writes owned `actuarial_pricing_reserving_reserve_estimate` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_loss_triangle`: validates policy, writes owned `actuarial_pricing_reserving_loss_triangle` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_capital_scenario`: validates policy, writes owned `actuarial_pricing_reserving_capital_scenario` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_model_validation`: validates policy, writes owned `actuarial_pricing_reserving_model_validation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_actuarial_pricing_reserving_policy_rule`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_pricing_reserving_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_actuarial_pricing_reserving_runtime_parameter`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_pricing_reserving_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_actuarial_pricing_reserving_schema_extension`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_pricing_reserving_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_actuarial_pricing_reserving_control_assertion`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_pricing_reserving_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_actuarial_pricing_reserving_governed_model`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_pricing_reserving_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_13`: validates policy, writes owned `actuarial_pricing_reserving_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_14`: validates policy, writes owned `actuarial_pricing_reserving_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_15`: validates policy, writes owned `actuarial_pricing_reserving_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_16`: validates policy, writes owned `actuarial_pricing_reserving_rating_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_17`: validates policy, writes owned `actuarial_pricing_reserving_actuarial_assumption` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_actuarial_pricing_reserving_18`: validates policy, writes owned `actuarial_pricing_reserving_experience_study` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Actuarial Pricing and Reserving domain records.
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

Rules are first-class artifacts: ('rating_model_policy', 'actuarial_assumption_policy', 'experience_study_policy', 'reserve_estimate_policy', 'loss_triangle_policy', 'capital_scenario_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /rating-models', 'POST /actuarial-assumptions', 'POST /experience-studys', 'POST /reserve-estimates', 'POST /loss-triangles', 'GET /actuarial-pricing-reserving-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `actuarial_pricing_reserving_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ActuarialPricingReservingCreated', 'ActuarialPricingReservingUpdated', 'ActuarialPricingReservingApproved', 'ActuarialPricingReservingExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('rating model board', 'actuarial assumption board', 'experience study board', 'reserve estimate board', 'loss triangle board', 'capital scenario board', 'model validation board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `actuarial_pricing_reserving_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: rating_model, actuarial_assumption, experience_study, reserve_estimate, loss_triangle, capital_scenario, model_validation, actuarial_pricing_reserving_policy_rule, actuarial_pricing_reserving_runtime_parameter, actuarial_pricing_reserving_schema_extension, actuarial_pricing_reserving_control_assertion, actuarial_pricing_reserving_governed_model
- operations: create_rating_model, record_actuarial_assumption, review_experience_study, approve_reserve_estimate, simulate_loss_triangle, create_capital_scenario, record_model_validation, review_actuarial_pricing_reserving_policy_rule, approve_actuarial_pricing_reserving_runtime_parameter, simulate_actuarial_pricing_reserving_schema_extension, create_actuarial_pricing_reserving_control_assertion, record_actuarial_pricing_reserving_governed_model, operate_actuarial_pricing_reserving_13, operate_actuarial_pricing_reserving_14, operate_actuarial_pricing_reserving_15, operate_actuarial_pricing_reserving_16, operate_actuarial_pricing_reserving_17, operate_actuarial_pricing_reserving_18
- emits: ActuarialPricingReservingCreated, ActuarialPricingReservingUpdated, ActuarialPricingReservingApproved, ActuarialPricingReservingExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: rating_model_policy, actuarial_assumption_policy, experience_study_policy, reserve_estimate_policy, loss_triangle_policy, capital_scenario_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ActuarialPricingReservingWorkbench, ActuarialPricingReservingDetail, ActuarialPricingReservingAssistantPanel
- permissions: actuarial_pricing_reserving.read, actuarial_pricing_reserving.create, actuarial_pricing_reserving.update, actuarial_pricing_reserving.approve, actuarial_pricing_reserving.admin
- configuration: ACTUARIAL_PRICING_RESERVING_DATABASE_URL, ACTUARIAL_PRICING_RESERVING_EVENT_TOPIC, ACTUARIAL_PRICING_RESERVING_RETRY_LIMIT, ACTUARIAL_PRICING_RESERVING_DEFAULT_POLICY
- standard_features: rating_model_management, actuarial_pricing_reserving_workflow, actuarial_pricing_reserving_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: actuarial_pricing_reserving_event_sourced_operational_history, actuarial_pricing_reserving_multi_tenant_policy_isolation, actuarial_pricing_reserving_schema_evolution_resilience, actuarial_pricing_reserving_autonomous_anomaly_detection, actuarial_pricing_reserving_semantic_document_instruction_understanding, actuarial_pricing_reserving_predictive_risk_scoring, actuarial_pricing_reserving_counterfactual_scenario_simulation, actuarial_pricing_reserving_cryptographic_audit_proofs, actuarial_pricing_reserving_continuous_control_testing, actuarial_pricing_reserving_carbon_and_sustainability_awareness, actuarial_pricing_reserving_cross_pbc_event_federation, actuarial_pricing_reserving_governed_ai_agent_execution
