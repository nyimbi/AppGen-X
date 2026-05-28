# Research Grants Management PBC

## Purpose

The `research_grants_management` PBC is a packaged business capability for Research proposals, awards, budgets, compliance, milestones, subawards, effort, and sponsor reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `research_grants_management`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/research_grants_management`.
- Runtime entrypoint: `research_grants_management_runtime_capabilities()`.
- UI entrypoint: `research_grants_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `research_grants_management_grant_proposal`: owns grant proposal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_award`: owns research award lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_sponsor_budget`: owns sponsor budget lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_compliance_requirement`: owns compliance requirement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_subaward`: owns subaward lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_milestone_report`: owns milestone report lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_effort_certification`: owns effort certification lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_grants_management_policy_rule`: owns research grants management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_grants_management_runtime_parameter`: owns research grants management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_grants_management_schema_extension`: owns research grants management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_grants_management_control_assertion`: owns research grants management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `research_grants_management_research_grants_management_governed_model`: owns research grants management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `research_grants_management_appgen_outbox_event`, `research_grants_management_appgen_inbox_event`, and `research_grants_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /grant-proposals', 'POST /research-awards', 'POST /sponsor-budgets', 'POST /compliance-requirements', 'POST /subawards', 'GET /research-grants-management-workbench').

## Executable Domain Operations

- `create_grant_proposal`: validates policy, writes owned `research_grants_management_grant_proposal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_research_award`: validates policy, writes owned `research_grants_management_research_award` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_sponsor_budget`: validates policy, writes owned `research_grants_management_sponsor_budget` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_compliance_requirement`: validates policy, writes owned `research_grants_management_compliance_requirement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_subaward`: validates policy, writes owned `research_grants_management_subaward` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_milestone_report`: validates policy, writes owned `research_grants_management_milestone_report` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_effort_certification`: validates policy, writes owned `research_grants_management_effort_certification` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_research_grants_management_policy_rule`: validates policy, writes owned `research_grants_management_research_grants_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_research_grants_management_runtime_parameter`: validates policy, writes owned `research_grants_management_research_grants_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_research_grants_management_schema_extension`: validates policy, writes owned `research_grants_management_research_grants_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_research_grants_management_control_assertion`: validates policy, writes owned `research_grants_management_research_grants_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_research_grants_management_governed_model`: validates policy, writes owned `research_grants_management_research_grants_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_13`: validates policy, writes owned `research_grants_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_14`: validates policy, writes owned `research_grants_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_15`: validates policy, writes owned `research_grants_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_16`: validates policy, writes owned `research_grants_management_grant_proposal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_17`: validates policy, writes owned `research_grants_management_research_award` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_research_grants_management_18`: validates policy, writes owned `research_grants_management_sponsor_budget` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Research Grants Management domain records.
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

Rules are first-class artifacts: ('grant_proposal_policy', 'research_award_policy', 'sponsor_budget_policy', 'compliance_requirement_policy', 'subaward_policy', 'milestone_report_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /grant-proposals', 'POST /research-awards', 'POST /sponsor-budgets', 'POST /compliance-requirements', 'POST /subawards', 'GET /research-grants-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `research_grants_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('ResearchGrantsManagementCreated', 'ResearchGrantsManagementUpdated', 'ResearchGrantsManagementApproved', 'ResearchGrantsManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('grant proposal board', 'research award board', 'sponsor budget board', 'compliance requirement board', 'subaward board', 'milestone report board', 'effort certification board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `research_grants_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: grant_proposal, research_award, sponsor_budget, compliance_requirement, subaward, milestone_report, effort_certification, research_grants_management_policy_rule, research_grants_management_runtime_parameter, research_grants_management_schema_extension, research_grants_management_control_assertion, research_grants_management_governed_model
- operations: create_grant_proposal, record_research_award, review_sponsor_budget, approve_compliance_requirement, simulate_subaward, create_milestone_report, record_effort_certification, review_research_grants_management_policy_rule, approve_research_grants_management_runtime_parameter, simulate_research_grants_management_schema_extension, create_research_grants_management_control_assertion, record_research_grants_management_governed_model, operate_research_grants_management_13, operate_research_grants_management_14, operate_research_grants_management_15, operate_research_grants_management_16, operate_research_grants_management_17, operate_research_grants_management_18
- emits: ResearchGrantsManagementCreated, ResearchGrantsManagementUpdated, ResearchGrantsManagementApproved, ResearchGrantsManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: grant_proposal_policy, research_award_policy, sponsor_budget_policy, compliance_requirement_policy, subaward_policy, milestone_report_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: ResearchGrantsManagementWorkbench, ResearchGrantsManagementDetail, ResearchGrantsManagementAssistantPanel
- permissions: research_grants_management.read, research_grants_management.create, research_grants_management.update, research_grants_management.approve, research_grants_management.admin
- configuration: RESEARCH_GRANTS_MANAGEMENT_DATABASE_URL, RESEARCH_GRANTS_MANAGEMENT_EVENT_TOPIC, RESEARCH_GRANTS_MANAGEMENT_RETRY_LIMIT, RESEARCH_GRANTS_MANAGEMENT_DEFAULT_POLICY
- standard_features: grant_proposal_management, research_grants_management_workflow, research_grants_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: research_grants_management_event_sourced_operational_history, research_grants_management_multi_tenant_policy_isolation, research_grants_management_schema_evolution_resilience, research_grants_management_autonomous_anomaly_detection, research_grants_management_semantic_document_instruction_understanding, research_grants_management_predictive_risk_scoring, research_grants_management_counterfactual_scenario_simulation, research_grants_management_cryptographic_audit_proofs, research_grants_management_continuous_control_testing, research_grants_management_carbon_and_sustainability_awareness, research_grants_management_cross_pbc_event_federation, research_grants_management_governed_ai_agent_execution
