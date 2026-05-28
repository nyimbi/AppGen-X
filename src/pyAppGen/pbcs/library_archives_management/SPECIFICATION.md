# Library and Archives Management PBC

## Purpose

The `library_archives_management` PBC is a packaged business capability for Collections, circulation, cataloging, digitization, rights, preservation, and archival access. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `library_archives_management`.
- Mesh: `content`.
- Package directory: `src/pyAppGen/pbcs/library_archives_management`.
- Runtime entrypoint: `library_archives_management_runtime_capabilities()`.
- UI entrypoint: `library_archives_management_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `library_archives_management_collection_item`: owns collection item lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_catalog_record`: owns catalog record lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_circulation_loan`: owns circulation loan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_digitization_job`: owns digitization job lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_rights_statement`: owns rights statement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_preservation_action`: owns preservation action lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_archive_request`: owns archive request lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_library_archives_management_policy_rule`: owns library archives management policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_library_archives_management_runtime_parameter`: owns library archives management runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_library_archives_management_schema_extension`: owns library archives management schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_library_archives_management_control_assertion`: owns library archives management control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `library_archives_management_library_archives_management_governed_model`: owns library archives management governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `library_archives_management_appgen_outbox_event`, `library_archives_management_appgen_inbox_event`, and `library_archives_management_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /collection-items', 'POST /catalog-records', 'POST /circulation-loans', 'POST /digitization-jobs', 'POST /rights-statements', 'GET /library-archives-management-workbench').

## Executable Domain Operations

- `create_collection_item`: validates policy, writes owned `library_archives_management_collection_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_catalog_record`: validates policy, writes owned `library_archives_management_catalog_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_circulation_loan`: validates policy, writes owned `library_archives_management_circulation_loan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_digitization_job`: validates policy, writes owned `library_archives_management_digitization_job` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_rights_statement`: validates policy, writes owned `library_archives_management_rights_statement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_preservation_action`: validates policy, writes owned `library_archives_management_preservation_action` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_archive_request`: validates policy, writes owned `library_archives_management_archive_request` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_library_archives_management_policy_rule`: validates policy, writes owned `library_archives_management_library_archives_management_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_library_archives_management_runtime_parameter`: validates policy, writes owned `library_archives_management_library_archives_management_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_library_archives_management_schema_extension`: validates policy, writes owned `library_archives_management_library_archives_management_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_library_archives_management_control_assertion`: validates policy, writes owned `library_archives_management_library_archives_management_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_library_archives_management_governed_model`: validates policy, writes owned `library_archives_management_library_archives_management_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_13`: validates policy, writes owned `library_archives_management_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_14`: validates policy, writes owned `library_archives_management_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_15`: validates policy, writes owned `library_archives_management_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_16`: validates policy, writes owned `library_archives_management_collection_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_17`: validates policy, writes owned `library_archives_management_catalog_record` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_library_archives_management_18`: validates policy, writes owned `library_archives_management_circulation_loan` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Library and Archives Management domain records.
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

Rules are first-class artifacts: ('collection_item_policy', 'catalog_record_policy', 'circulation_loan_policy', 'digitization_job_policy', 'rights_statement_policy', 'preservation_action_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /collection-items', 'POST /catalog-records', 'POST /circulation-loans', 'POST /digitization-jobs', 'POST /rights-statements', 'GET /library-archives-management-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `library_archives_management_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('LibraryArchivesManagementCreated', 'LibraryArchivesManagementUpdated', 'LibraryArchivesManagementApproved', 'LibraryArchivesManagementExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('collection item board', 'catalog record board', 'circulation loan board', 'digitization job board', 'rights statement board', 'preservation action board', 'archive request board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `library_archives_management_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: collection_item, catalog_record, circulation_loan, digitization_job, rights_statement, preservation_action, archive_request, library_archives_management_policy_rule, library_archives_management_runtime_parameter, library_archives_management_schema_extension, library_archives_management_control_assertion, library_archives_management_governed_model
- operations: create_collection_item, record_catalog_record, review_circulation_loan, approve_digitization_job, simulate_rights_statement, create_preservation_action, record_archive_request, review_library_archives_management_policy_rule, approve_library_archives_management_runtime_parameter, simulate_library_archives_management_schema_extension, create_library_archives_management_control_assertion, record_library_archives_management_governed_model, operate_library_archives_management_13, operate_library_archives_management_14, operate_library_archives_management_15, operate_library_archives_management_16, operate_library_archives_management_17, operate_library_archives_management_18
- emits: LibraryArchivesManagementCreated, LibraryArchivesManagementUpdated, LibraryArchivesManagementApproved, LibraryArchivesManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: collection_item_policy, catalog_record_policy, circulation_loan_policy, digitization_job_policy, rights_statement_policy, preservation_action_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: LibraryArchivesManagementWorkbench, LibraryArchivesManagementDetail, LibraryArchivesManagementAssistantPanel
- permissions: library_archives_management.read, library_archives_management.create, library_archives_management.update, library_archives_management.approve, library_archives_management.admin
- configuration: LIBRARY_ARCHIVES_MANAGEMENT_DATABASE_URL, LIBRARY_ARCHIVES_MANAGEMENT_EVENT_TOPIC, LIBRARY_ARCHIVES_MANAGEMENT_RETRY_LIMIT, LIBRARY_ARCHIVES_MANAGEMENT_DEFAULT_POLICY
- standard_features: collection_item_management, library_archives_management_workflow, library_archives_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: library_archives_management_event_sourced_operational_history, library_archives_management_multi_tenant_policy_isolation, library_archives_management_schema_evolution_resilience, library_archives_management_autonomous_anomaly_detection, library_archives_management_semantic_document_instruction_understanding, library_archives_management_predictive_risk_scoring, library_archives_management_counterfactual_scenario_simulation, library_archives_management_cryptographic_audit_proofs, library_archives_management_continuous_control_testing, library_archives_management_carbon_and_sustainability_awareness, library_archives_management_cross_pbc_event_federation, library_archives_management_governed_ai_agent_execution
