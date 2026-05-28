# Public Sector Tax Administration PBC

## Purpose

The `tax_administration_public_sector` PBC is a packaged business capability for Taxpayer accounts, filings, assessments, audits, collections, appeals, and public revenue administration. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `tax_administration_public_sector`.
- Mesh: `finops`.
- Package directory: `src/pyAppGen/pbcs/tax_administration_public_sector`.
- Runtime entrypoint: `tax_administration_public_sector_runtime_capabilities()`.
- UI entrypoint: `tax_administration_public_sector_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `tax_administration_public_sector_taxpayer_account`: owns taxpayer account lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_filing`: owns tax filing lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_assessment`: owns assessment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_audit_case`: owns audit case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_collection_action`: owns collection action lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_appeal`: owns appeal lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_notice`: owns tax notice lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_administration_public_sector_policy_rule`: owns tax administration public sector policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_administration_public_sector_runtime_parameter`: owns tax administration public sector runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_administration_public_sector_schema_extension`: owns tax administration public sector schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_administration_public_sector_control_assertion`: owns tax administration public sector control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `tax_administration_public_sector_tax_administration_public_sector_governed_model`: owns tax administration public sector governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `tax_administration_public_sector_appgen_outbox_event`, `tax_administration_public_sector_appgen_inbox_event`, and `tax_administration_public_sector_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /taxpayer-accounts', 'POST /tax-filings', 'POST /assessments', 'POST /audit-cases', 'POST /collection-actions', 'GET /tax-administration-public-sector-workbench').

## Executable Domain Operations

- `create_taxpayer_account`: validates policy, writes owned `tax_administration_public_sector_taxpayer_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_tax_filing`: validates policy, writes owned `tax_administration_public_sector_tax_filing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_assessment`: validates policy, writes owned `tax_administration_public_sector_assessment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_audit_case`: validates policy, writes owned `tax_administration_public_sector_audit_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_collection_action`: validates policy, writes owned `tax_administration_public_sector_collection_action` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_appeal`: validates policy, writes owned `tax_administration_public_sector_appeal` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_tax_notice`: validates policy, writes owned `tax_administration_public_sector_tax_notice` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_tax_administration_public_sector_policy_rule`: validates policy, writes owned `tax_administration_public_sector_tax_administration_public_sector_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_tax_administration_public_sector_runtime_parameter`: validates policy, writes owned `tax_administration_public_sector_tax_administration_public_sector_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_tax_administration_public_sector_schema_extension`: validates policy, writes owned `tax_administration_public_sector_tax_administration_public_sector_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_tax_administration_public_sector_control_assertion`: validates policy, writes owned `tax_administration_public_sector_tax_administration_public_sector_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_tax_administration_public_sector_governed_model`: validates policy, writes owned `tax_administration_public_sector_tax_administration_public_sector_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_13`: validates policy, writes owned `tax_administration_public_sector_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_14`: validates policy, writes owned `tax_administration_public_sector_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_15`: validates policy, writes owned `tax_administration_public_sector_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_16`: validates policy, writes owned `tax_administration_public_sector_taxpayer_account` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_17`: validates policy, writes owned `tax_administration_public_sector_tax_filing` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_tax_administration_public_sector_18`: validates policy, writes owned `tax_administration_public_sector_assessment` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Public Sector Tax Administration domain records.
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

Rules are first-class artifacts: ('taxpayer_account_policy', 'tax_filing_policy', 'assessment_policy', 'audit_case_policy', 'collection_action_policy', 'appeal_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /taxpayer-accounts', 'POST /tax-filings', 'POST /assessments', 'POST /audit-cases', 'POST /collection-actions', 'GET /tax-administration-public-sector-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `tax_administration_public_sector_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('TaxAdministrationPublicSectorCreated', 'TaxAdministrationPublicSectorUpdated', 'TaxAdministrationPublicSectorApproved', 'TaxAdministrationPublicSectorExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('taxpayer account board', 'tax filing board', 'assessment board', 'audit case board', 'collection action board', 'appeal board', 'tax notice board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `tax_administration_public_sector_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: taxpayer_account, tax_filing, assessment, audit_case, collection_action, appeal, tax_notice, tax_administration_public_sector_policy_rule, tax_administration_public_sector_runtime_parameter, tax_administration_public_sector_schema_extension, tax_administration_public_sector_control_assertion, tax_administration_public_sector_governed_model
- operations: create_taxpayer_account, record_tax_filing, review_assessment, approve_audit_case, simulate_collection_action, create_appeal, record_tax_notice, review_tax_administration_public_sector_policy_rule, approve_tax_administration_public_sector_runtime_parameter, simulate_tax_administration_public_sector_schema_extension, create_tax_administration_public_sector_control_assertion, record_tax_administration_public_sector_governed_model, operate_tax_administration_public_sector_13, operate_tax_administration_public_sector_14, operate_tax_administration_public_sector_15, operate_tax_administration_public_sector_16, operate_tax_administration_public_sector_17, operate_tax_administration_public_sector_18
- emits: TaxAdministrationPublicSectorCreated, TaxAdministrationPublicSectorUpdated, TaxAdministrationPublicSectorApproved, TaxAdministrationPublicSectorExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: taxpayer_account_policy, tax_filing_policy, assessment_policy, audit_case_policy, collection_action_policy, appeal_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: TaxAdministrationPublicSectorWorkbench, TaxAdministrationPublicSectorDetail, TaxAdministrationPublicSectorAssistantPanel
- permissions: tax_administration_public_sector.read, tax_administration_public_sector.create, tax_administration_public_sector.update, tax_administration_public_sector.approve, tax_administration_public_sector.admin
- configuration: TAX_ADMINISTRATION_PUBLIC_SECTOR_DATABASE_URL, TAX_ADMINISTRATION_PUBLIC_SECTOR_EVENT_TOPIC, TAX_ADMINISTRATION_PUBLIC_SECTOR_RETRY_LIMIT, TAX_ADMINISTRATION_PUBLIC_SECTOR_DEFAULT_POLICY
- standard_features: taxpayer_account_management, tax_administration_public_sector_workflow, tax_administration_public_sector_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: tax_administration_public_sector_event_sourced_operational_history, tax_administration_public_sector_multi_tenant_policy_isolation, tax_administration_public_sector_schema_evolution_resilience, tax_administration_public_sector_autonomous_anomaly_detection, tax_administration_public_sector_semantic_document_instruction_understanding, tax_administration_public_sector_predictive_risk_scoring, tax_administration_public_sector_counterfactual_scenario_simulation, tax_administration_public_sector_cryptographic_audit_proofs, tax_administration_public_sector_continuous_control_testing, tax_administration_public_sector_carbon_and_sustainability_awareness, tax_administration_public_sector_cross_pbc_event_federation, tax_administration_public_sector_governed_ai_agent_execution
