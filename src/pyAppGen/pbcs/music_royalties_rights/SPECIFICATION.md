# Music Royalties and Rights PBC

## Purpose

The `music_royalties_rights` PBC is a packaged business capability for Works, recordings, splits, licenses, statements, usage, royalty payments, and rights disputes. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `music_royalties_rights`.
- Mesh: `content`.
- Package directory: `src/pyAppGen/pbcs/music_royalties_rights`.
- Runtime entrypoint: `music_royalties_rights_runtime_capabilities()`.
- UI entrypoint: `music_royalties_rights_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `music_royalties_rights_musical_work`: owns musical work lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_recording`: owns recording lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_rights_split`: owns rights split lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_license`: owns license lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_usage_report`: owns usage report lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_royalty_statement`: owns royalty statement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_rights_dispute`: owns rights dispute lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_music_royalties_rights_policy_rule`: owns music royalties rights policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_music_royalties_rights_runtime_parameter`: owns music royalties rights runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_music_royalties_rights_schema_extension`: owns music royalties rights schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_music_royalties_rights_control_assertion`: owns music royalties rights control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `music_royalties_rights_music_royalties_rights_governed_model`: owns music royalties rights governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `music_royalties_rights_appgen_outbox_event`, `music_royalties_rights_appgen_inbox_event`, and `music_royalties_rights_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /musical-works', 'POST /recordings', 'POST /rights-splits', 'POST /licenses', 'POST /usage-reports', 'GET /music-royalties-rights-workbench').

## Executable Domain Operations

- `create_musical_work`: validates policy, writes owned `music_royalties_rights_musical_work` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_recording`: validates policy, writes owned `music_royalties_rights_recording` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_rights_split`: validates policy, writes owned `music_royalties_rights_rights_split` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_license`: validates policy, writes owned `music_royalties_rights_license` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_usage_report`: validates policy, writes owned `music_royalties_rights_usage_report` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_royalty_statement`: validates policy, writes owned `music_royalties_rights_royalty_statement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_rights_dispute`: validates policy, writes owned `music_royalties_rights_rights_dispute` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_music_royalties_rights_policy_rule`: validates policy, writes owned `music_royalties_rights_music_royalties_rights_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_music_royalties_rights_runtime_parameter`: validates policy, writes owned `music_royalties_rights_music_royalties_rights_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_music_royalties_rights_schema_extension`: validates policy, writes owned `music_royalties_rights_music_royalties_rights_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_music_royalties_rights_control_assertion`: validates policy, writes owned `music_royalties_rights_music_royalties_rights_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_music_royalties_rights_governed_model`: validates policy, writes owned `music_royalties_rights_music_royalties_rights_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_13`: validates policy, writes owned `music_royalties_rights_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_14`: validates policy, writes owned `music_royalties_rights_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_15`: validates policy, writes owned `music_royalties_rights_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_16`: validates policy, writes owned `music_royalties_rights_musical_work` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_17`: validates policy, writes owned `music_royalties_rights_recording` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_music_royalties_rights_18`: validates policy, writes owned `music_royalties_rights_rights_split` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Music Royalties and Rights domain records.
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

Rules are first-class artifacts: ('musical_work_policy', 'recording_policy', 'rights_split_policy', 'license_policy', 'usage_report_policy', 'royalty_statement_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /musical-works', 'POST /recordings', 'POST /rights-splits', 'POST /licenses', 'POST /usage-reports', 'GET /music-royalties-rights-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `music_royalties_rights_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MusicRoyaltiesRightsCreated', 'MusicRoyaltiesRightsUpdated', 'MusicRoyaltiesRightsApproved', 'MusicRoyaltiesRightsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('musical work board', 'recording board', 'rights split board', 'license board', 'usage report board', 'royalty statement board', 'rights dispute board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `music_royalties_rights_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: musical_work, recording, rights_split, license, usage_report, royalty_statement, rights_dispute, music_royalties_rights_policy_rule, music_royalties_rights_runtime_parameter, music_royalties_rights_schema_extension, music_royalties_rights_control_assertion, music_royalties_rights_governed_model
- operations: create_musical_work, record_recording, review_rights_split, approve_license, simulate_usage_report, create_royalty_statement, record_rights_dispute, review_music_royalties_rights_policy_rule, approve_music_royalties_rights_runtime_parameter, simulate_music_royalties_rights_schema_extension, create_music_royalties_rights_control_assertion, record_music_royalties_rights_governed_model, operate_music_royalties_rights_13, operate_music_royalties_rights_14, operate_music_royalties_rights_15, operate_music_royalties_rights_16, operate_music_royalties_rights_17, operate_music_royalties_rights_18
- emits: MusicRoyaltiesRightsCreated, MusicRoyaltiesRightsUpdated, MusicRoyaltiesRightsApproved, MusicRoyaltiesRightsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: musical_work_policy, recording_policy, rights_split_policy, license_policy, usage_report_policy, royalty_statement_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MusicRoyaltiesRightsWorkbench, MusicRoyaltiesRightsDetail, MusicRoyaltiesRightsAssistantPanel
- permissions: music_royalties_rights.read, music_royalties_rights.create, music_royalties_rights.update, music_royalties_rights.approve, music_royalties_rights.admin
- configuration: MUSIC_ROYALTIES_RIGHTS_DATABASE_URL, MUSIC_ROYALTIES_RIGHTS_EVENT_TOPIC, MUSIC_ROYALTIES_RIGHTS_RETRY_LIMIT, MUSIC_ROYALTIES_RIGHTS_DEFAULT_POLICY
- standard_features: musical_work_management, music_royalties_rights_workflow, music_royalties_rights_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: music_royalties_rights_event_sourced_operational_history, music_royalties_rights_multi_tenant_policy_isolation, music_royalties_rights_schema_evolution_resilience, music_royalties_rights_autonomous_anomaly_detection, music_royalties_rights_semantic_document_instruction_understanding, music_royalties_rights_predictive_risk_scoring, music_royalties_rights_counterfactual_scenario_simulation, music_royalties_rights_cryptographic_audit_proofs, music_royalties_rights_continuous_control_testing, music_royalties_rights_carbon_and_sustainability_awareness, music_royalties_rights_cross_pbc_event_federation, music_royalties_rights_governed_ai_agent_execution
