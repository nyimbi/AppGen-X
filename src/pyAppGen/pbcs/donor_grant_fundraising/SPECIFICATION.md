# Donor Grant and Fundraising PBC

## Purpose

The `donor_grant_fundraising` PBC is a packaged business capability for Donors, campaigns, pledges, restrictions, gifts, grant applications, stewardship, and impact reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `donor_grant_fundraising`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/donor_grant_fundraising`.
- Runtime entrypoint: `donor_grant_fundraising_runtime_capabilities()`.
- UI entrypoint: `donor_grant_fundraising_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `donor_grant_fundraising_donor`: owns donor lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_campaign`: owns campaign lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_pledge`: owns pledge lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_gift`: owns gift lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_restriction`: owns restriction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_grant_application`: owns grant application lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_stewardship_touchpoint`: owns stewardship touchpoint lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_donor_grant_fundraising_policy_rule`: owns donor grant fundraising policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_donor_grant_fundraising_runtime_parameter`: owns donor grant fundraising runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_donor_grant_fundraising_schema_extension`: owns donor grant fundraising schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_donor_grant_fundraising_control_assertion`: owns donor grant fundraising control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `donor_grant_fundraising_donor_grant_fundraising_governed_model`: owns donor grant fundraising governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `donor_grant_fundraising_appgen_outbox_event`, `donor_grant_fundraising_appgen_inbox_event`, and `donor_grant_fundraising_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /donors', 'POST /campaigns', 'POST /pledges', 'POST /gifts', 'POST /restrictions', 'GET /donor-grant-fundraising-workbench').

## Executable Domain Operations

- `create_donor`: validates policy, writes owned `donor_grant_fundraising_donor` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_campaign`: validates policy, writes owned `donor_grant_fundraising_campaign` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_pledge`: validates policy, writes owned `donor_grant_fundraising_pledge` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_gift`: validates policy, writes owned `donor_grant_fundraising_gift` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_restriction`: validates policy, writes owned `donor_grant_fundraising_restriction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_grant_application`: validates policy, writes owned `donor_grant_fundraising_grant_application` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_stewardship_touchpoint`: validates policy, writes owned `donor_grant_fundraising_stewardship_touchpoint` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_donor_grant_fundraising_policy_rule`: validates policy, writes owned `donor_grant_fundraising_donor_grant_fundraising_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_donor_grant_fundraising_runtime_parameter`: validates policy, writes owned `donor_grant_fundraising_donor_grant_fundraising_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_donor_grant_fundraising_schema_extension`: validates policy, writes owned `donor_grant_fundraising_donor_grant_fundraising_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_donor_grant_fundraising_control_assertion`: validates policy, writes owned `donor_grant_fundraising_donor_grant_fundraising_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_donor_grant_fundraising_governed_model`: validates policy, writes owned `donor_grant_fundraising_donor_grant_fundraising_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_13`: validates policy, writes owned `donor_grant_fundraising_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_14`: validates policy, writes owned `donor_grant_fundraising_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_15`: validates policy, writes owned `donor_grant_fundraising_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_16`: validates policy, writes owned `donor_grant_fundraising_donor` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_17`: validates policy, writes owned `donor_grant_fundraising_campaign` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_donor_grant_fundraising_18`: validates policy, writes owned `donor_grant_fundraising_pledge` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Donor Grant and Fundraising domain records.
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

Rules are first-class artifacts: ('donor_policy', 'campaign_policy', 'pledge_policy', 'gift_policy', 'restriction_policy', 'grant_application_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /donors', 'POST /campaigns', 'POST /pledges', 'POST /gifts', 'POST /restrictions', 'GET /donor-grant-fundraising-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `donor_grant_fundraising_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('DonorGrantFundraisingCreated', 'DonorGrantFundraisingUpdated', 'DonorGrantFundraisingApproved', 'DonorGrantFundraisingExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('donor board', 'campaign board', 'pledge board', 'gift board', 'restriction board', 'grant application board', 'stewardship touchpoint board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `donor_grant_fundraising_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: donor, campaign, pledge, gift, restriction, grant_application, stewardship_touchpoint, donor_grant_fundraising_policy_rule, donor_grant_fundraising_runtime_parameter, donor_grant_fundraising_schema_extension, donor_grant_fundraising_control_assertion, donor_grant_fundraising_governed_model
- operations: create_donor, record_campaign, review_pledge, approve_gift, simulate_restriction, create_grant_application, record_stewardship_touchpoint, review_donor_grant_fundraising_policy_rule, approve_donor_grant_fundraising_runtime_parameter, simulate_donor_grant_fundraising_schema_extension, create_donor_grant_fundraising_control_assertion, record_donor_grant_fundraising_governed_model, operate_donor_grant_fundraising_13, operate_donor_grant_fundraising_14, operate_donor_grant_fundraising_15, operate_donor_grant_fundraising_16, operate_donor_grant_fundraising_17, operate_donor_grant_fundraising_18
- emits: DonorGrantFundraisingCreated, DonorGrantFundraisingUpdated, DonorGrantFundraisingApproved, DonorGrantFundraisingExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: donor_policy, campaign_policy, pledge_policy, gift_policy, restriction_policy, grant_application_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: DonorGrantFundraisingWorkbench, DonorGrantFundraisingDetail, DonorGrantFundraisingAssistantPanel
- permissions: donor_grant_fundraising.read, donor_grant_fundraising.create, donor_grant_fundraising.update, donor_grant_fundraising.approve, donor_grant_fundraising.admin
- configuration: DONOR_GRANT_FUNDRAISING_DATABASE_URL, DONOR_GRANT_FUNDRAISING_EVENT_TOPIC, DONOR_GRANT_FUNDRAISING_RETRY_LIMIT, DONOR_GRANT_FUNDRAISING_DEFAULT_POLICY
- standard_features: donor_management, donor_grant_fundraising_workflow, donor_grant_fundraising_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: donor_grant_fundraising_event_sourced_operational_history, donor_grant_fundraising_multi_tenant_policy_isolation, donor_grant_fundraising_schema_evolution_resilience, donor_grant_fundraising_autonomous_anomaly_detection, donor_grant_fundraising_semantic_document_instruction_understanding, donor_grant_fundraising_predictive_risk_scoring, donor_grant_fundraising_counterfactual_scenario_simulation, donor_grant_fundraising_cryptographic_audit_proofs, donor_grant_fundraising_continuous_control_testing, donor_grant_fundraising_carbon_and_sustainability_awareness, donor_grant_fundraising_cross_pbc_event_federation, donor_grant_fundraising_governed_ai_agent_execution
