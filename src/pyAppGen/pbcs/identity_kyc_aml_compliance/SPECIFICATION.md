# Identity KYC AML Compliance PBC

## Purpose

The `identity_kyc_aml_compliance` PBC is a packaged business capability for Customer onboarding, identity proofing, beneficial ownership, screening, transaction monitoring, suspicious activity, and compliance cases. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `identity_kyc_aml_compliance`.
- Mesh: `platform`.
- Package directory: `src/pyAppGen/pbcs/identity_kyc_aml_compliance`.
- Runtime entrypoint: `identity_kyc_aml_compliance_runtime_capabilities()`.
- UI entrypoint: `identity_kyc_aml_compliance_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `identity_kyc_aml_compliance_kyc_profile`: owns kyc profile lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_document`: owns identity document lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_beneficial_owner`: owns beneficial owner lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_screening_hit`: owns screening hit lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_monitoring_alert`: owns monitoring alert lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_suspicious_activity_case`: owns suspicious activity case lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_compliance_review`: owns compliance review lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_kyc_aml_compliance_policy_rule`: owns identity kyc aml compliance policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_kyc_aml_compliance_runtime_parameter`: owns identity kyc aml compliance runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_kyc_aml_compliance_schema_extension`: owns identity kyc aml compliance schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_kyc_aml_compliance_control_assertion`: owns identity kyc aml compliance control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `identity_kyc_aml_compliance_identity_kyc_aml_compliance_governed_model`: owns identity kyc aml compliance governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `identity_kyc_aml_compliance_appgen_outbox_event`, `identity_kyc_aml_compliance_appgen_inbox_event`, and `identity_kyc_aml_compliance_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /kyc-profiles', 'POST /identity-documents', 'POST /beneficial-owners', 'POST /screening-hits', 'POST /monitoring-alerts', 'GET /identity-kyc-aml-compliance-workbench').

## Executable Domain Operations

- `create_kyc_profile`: validates policy, writes owned `identity_kyc_aml_compliance_kyc_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_identity_document`: validates policy, writes owned `identity_kyc_aml_compliance_identity_document` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_beneficial_owner`: validates policy, writes owned `identity_kyc_aml_compliance_beneficial_owner` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_screening_hit`: validates policy, writes owned `identity_kyc_aml_compliance_screening_hit` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_monitoring_alert`: validates policy, writes owned `identity_kyc_aml_compliance_monitoring_alert` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_suspicious_activity_case`: validates policy, writes owned `identity_kyc_aml_compliance_suspicious_activity_case` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_compliance_review`: validates policy, writes owned `identity_kyc_aml_compliance_compliance_review` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_identity_kyc_aml_compliance_policy_rule`: validates policy, writes owned `identity_kyc_aml_compliance_identity_kyc_aml_compliance_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_identity_kyc_aml_compliance_runtime_parameter`: validates policy, writes owned `identity_kyc_aml_compliance_identity_kyc_aml_compliance_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_identity_kyc_aml_compliance_schema_extension`: validates policy, writes owned `identity_kyc_aml_compliance_identity_kyc_aml_compliance_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_identity_kyc_aml_compliance_control_assertion`: validates policy, writes owned `identity_kyc_aml_compliance_identity_kyc_aml_compliance_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_identity_kyc_aml_compliance_governed_model`: validates policy, writes owned `identity_kyc_aml_compliance_identity_kyc_aml_compliance_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_13`: validates policy, writes owned `identity_kyc_aml_compliance_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_14`: validates policy, writes owned `identity_kyc_aml_compliance_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_15`: validates policy, writes owned `identity_kyc_aml_compliance_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_16`: validates policy, writes owned `identity_kyc_aml_compliance_kyc_profile` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_17`: validates policy, writes owned `identity_kyc_aml_compliance_identity_document` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_identity_kyc_aml_compliance_18`: validates policy, writes owned `identity_kyc_aml_compliance_beneficial_owner` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Identity KYC AML Compliance domain records.
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

Rules are first-class artifacts: ('kyc_profile_policy', 'identity_document_policy', 'beneficial_owner_policy', 'screening_hit_policy', 'monitoring_alert_policy', 'suspicious_activity_case_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /kyc-profiles', 'POST /identity-documents', 'POST /beneficial-owners', 'POST /screening-hits', 'POST /monitoring-alerts', 'GET /identity-kyc-aml-compliance-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `identity_kyc_aml_compliance_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('IdentityKycAmlComplianceCreated', 'IdentityKycAmlComplianceUpdated', 'IdentityKycAmlComplianceApproved', 'IdentityKycAmlComplianceExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('kyc profile board', 'identity document board', 'beneficial owner board', 'screening hit board', 'monitoring alert board', 'suspicious activity case board', 'compliance review board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `identity_kyc_aml_compliance_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: kyc_profile, identity_document, beneficial_owner, screening_hit, monitoring_alert, suspicious_activity_case, compliance_review, identity_kyc_aml_compliance_policy_rule, identity_kyc_aml_compliance_runtime_parameter, identity_kyc_aml_compliance_schema_extension, identity_kyc_aml_compliance_control_assertion, identity_kyc_aml_compliance_governed_model
- operations: create_kyc_profile, record_identity_document, review_beneficial_owner, approve_screening_hit, simulate_monitoring_alert, create_suspicious_activity_case, record_compliance_review, review_identity_kyc_aml_compliance_policy_rule, approve_identity_kyc_aml_compliance_runtime_parameter, simulate_identity_kyc_aml_compliance_schema_extension, create_identity_kyc_aml_compliance_control_assertion, record_identity_kyc_aml_compliance_governed_model, operate_identity_kyc_aml_compliance_13, operate_identity_kyc_aml_compliance_14, operate_identity_kyc_aml_compliance_15, operate_identity_kyc_aml_compliance_16, operate_identity_kyc_aml_compliance_17, operate_identity_kyc_aml_compliance_18
- emits: IdentityKycAmlComplianceCreated, IdentityKycAmlComplianceUpdated, IdentityKycAmlComplianceApproved, IdentityKycAmlComplianceExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: kyc_profile_policy, identity_document_policy, beneficial_owner_policy, screening_hit_policy, monitoring_alert_policy, suspicious_activity_case_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: IdentityKycAmlComplianceWorkbench, IdentityKycAmlComplianceDetail, IdentityKycAmlComplianceAssistantPanel
- permissions: identity_kyc_aml_compliance.read, identity_kyc_aml_compliance.create, identity_kyc_aml_compliance.update, identity_kyc_aml_compliance.approve, identity_kyc_aml_compliance.admin
- configuration: IDENTITY_KYC_AML_COMPLIANCE_DATABASE_URL, IDENTITY_KYC_AML_COMPLIANCE_EVENT_TOPIC, IDENTITY_KYC_AML_COMPLIANCE_RETRY_LIMIT, IDENTITY_KYC_AML_COMPLIANCE_DEFAULT_POLICY
- standard_features: kyc_profile_management, identity_kyc_aml_compliance_workflow, identity_kyc_aml_compliance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: identity_kyc_aml_compliance_event_sourced_operational_history, identity_kyc_aml_compliance_multi_tenant_policy_isolation, identity_kyc_aml_compliance_schema_evolution_resilience, identity_kyc_aml_compliance_autonomous_anomaly_detection, identity_kyc_aml_compliance_semantic_document_instruction_understanding, identity_kyc_aml_compliance_predictive_risk_scoring, identity_kyc_aml_compliance_counterfactual_scenario_simulation, identity_kyc_aml_compliance_cryptographic_audit_proofs, identity_kyc_aml_compliance_continuous_control_testing, identity_kyc_aml_compliance_carbon_and_sustainability_awareness, identity_kyc_aml_compliance_cross_pbc_event_federation, identity_kyc_aml_compliance_governed_ai_agent_execution
