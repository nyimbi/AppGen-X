# Identity KYC AML Compliance PBC

## Purpose

`identity_kyc_aml_compliance` owns customer onboarding, identity proofing, beneficial ownership, sanctions and PEP screening, ongoing monitoring, suspicious activity escalation, and compliance decisioning. It remains standalone by owning its schema, migrations, runtime workflows, UI/assistant contracts, AppGen-X events, and release evidence inside this package.

## Core entities

- `identity_kyc_aml_compliance_kyc_profile`: onboarding classification, lifecycle status, risk tier, EDD flags, duplicate candidates, and next rescreen date.
- `identity_kyc_aml_compliance_identity_document`: document completeness, authenticity, expiry, liveness, and face-match evidence.
- `identity_kyc_aml_compliance_beneficial_owner`: threshold ownership, control-person roles, and screening requirements.
- `identity_kyc_aml_compliance_screening_hit`: sanctions, PEP, RCA, adverse media, and deny-list evidence with severity, confidence, and disposition.
- `identity_kyc_aml_compliance_monitoring_alert`: typology, severity, assignment, SLA, and triage state.
- `identity_kyc_aml_compliance_suspicious_activity_case`: escalated alert cases and suspicious activity handling.
- `identity_kyc_aml_compliance_compliance_review`: EDD packets, review outcomes, and risk score challenge lineage.

## Executable workflows

- Onboarding wizard: classification -> document capture -> screening -> beneficial ownership -> EDD packet -> approval gate.
- Rescreening cycle: risk-tier calendar plus event-driven follow-up from `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Monitoring escalation: alert triage -> case promotion boundary -> review evidence capture.
- Risk challenge flow: factor-based score explanation, challenge note, supervisor approval, and persisted review lineage.

## Rules and parameters

Rules include classification requirements, document completeness/authenticity, beneficial owner threshold policy, EDD triggers, periodic rescreening, alert-to-case promotion, and risk score challenge controls.

Parameters include threshold owner percentages, high-risk threshold percentages, rescreening cadences for low/medium/high risk, workbench limits, and high-risk geography lists.

## Public contracts

- APIs: `POST /kyc-profiles`, `POST /identity-documents`, `POST /beneficial-owners`, `POST /screening-hits`, `POST /monitoring-alerts`, `GET /identity-kyc-aml-compliance-workbench`
- Emitted events: `IdentityKycAmlComplianceCreated`, `IdentityKycAmlComplianceUpdated`, `IdentityKycAmlComplianceApproved`, `IdentityKycAmlComplianceExceptionOpened`
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- UI fragments: `IdentityKycAmlComplianceWorkbench`, `IdentityKycAmlComplianceDetail`, `IdentityKycAmlComplianceAssistantPanel`, `IdentityKycAmlComplianceOnboardingWizard`, `IdentityKycAmlComplianceReviewPacket`

## Guardrails

- No foreign-table writes.
- No stream-engine selector.
- Mutating assistant actions require confirmation.
- Approval requires document, screening, ownership, duplicate-resolution, and EDD gates to pass.

## Complete Implementation Contract

The Identity KYC AML Compliance PBC owns party identity, document verification, biometric proofing, sanctions screening, politically exposed person checks, adverse media review, beneficial ownership, customer risk rating, case investigation, SAR/STR workflow, audit proof, model governance, runtime parameter, policy rule, schema extension, and AppGen-X event tables. Schema, migration, and model artifacts are generated under the identity_kyc_aml_compliance prefix, and all service logic preserves the owned boundary without shared table mutation. Standard capabilities cover onboarding, document capture, identity resolution, screening, monitoring, risk scoring, EDD, investigation, regulatory filing, consent, retention, and evidence management. Advanced capabilities include graph-based entity resolution, explainable risk scoring, semantic document/instruction parsing, continuous sanctions monitoring, anomaly detection, counterfactual risk simulation, cryptographic audit proofs, privacy-preserving data minimization, and governed AI agent execution.

Service command methods create and update applicants, identity documents, verification sessions, screening hits, ownership graphs, cases, decisions, filings, rules, parameters, and configuration. Query methods expose workbench, risk, screening, case, filing, and release evidence views. API route contracts bind commands and queries to permission RBAC descriptors. Event handling uses AppGen-X outbox/inbox contracts, idempotency keys, retry policy, and dead-letter evidence. The UI exposes forms, wizards, controls, analyst queues, configuration editors, permission-aware actions, and model governance panels. The PBC chatbot provides skills for task guidance, document instruction intake, CRUD datastore mutation previews, and foreign-table rejection. Registration and discovery are side-effect-free, with package metadata, tests, seed data, and PostgreSQL, MySQL, and MariaDB backend policy.
## Manifest Traceability Appendix

This appendix maps the executable manifest for `identity_kyc_aml_compliance` to the implemented PBC package so release audits can verify that every declared surface is covered by the specification, code, UI, agent, tests, seed data, and AppGen-X integration evidence.

### tables
- `kyc_profile`
- `identity_document`
- `beneficial_owner`
- `screening_hit`
- `monitoring_alert`
- `suspicious_activity_case`
- `compliance_review`
- `identity_kyc_aml_compliance_policy_rule`
- `identity_kyc_aml_compliance_runtime_parameter`
- `identity_kyc_aml_compliance_schema_extension`
- `identity_kyc_aml_compliance_control_assertion`
- `identity_kyc_aml_compliance_governed_model`

### apis
- `POST /kyc-profiles`
- `POST /identity-documents`
- `POST /beneficial-owners`
- `POST /screening-hits`
- `POST /monitoring-alerts`
- `GET /identity-kyc-aml-compliance-workbench`

### emits
- `IdentityKycAmlComplianceCreated`
- `IdentityKycAmlComplianceUpdated`
- `IdentityKycAmlComplianceApproved`
- `IdentityKycAmlComplianceExceptionOpened`

### consumes
- `PolicyChanged`
- `AuditEventSealed`
- `OperationalKpiChanged`

### ui_fragments
- `IdentityKycAmlComplianceWorkbench`
- `IdentityKycAmlComplianceDetail`
- `IdentityKycAmlComplianceAssistantPanel`

### permissions
- `identity_kyc_aml_compliance.read`
- `identity_kyc_aml_compliance.create`
- `identity_kyc_aml_compliance.update`
- `identity_kyc_aml_compliance.approve`
- `identity_kyc_aml_compliance.admin`

### configuration
- `IDENTITY_KYC_AML_COMPLIANCE_DATABASE_URL`
- `IDENTITY_KYC_AML_COMPLIANCE_EVENT_TOPIC`
- `IDENTITY_KYC_AML_COMPLIANCE_RETRY_LIMIT`
- `IDENTITY_KYC_AML_COMPLIANCE_DEFAULT_POLICY`

### standard_features
- `kyc_profile_management`
- `identity_kyc_aml_compliance_workflow`
- `identity_kyc_aml_compliance_analytics`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `owned_schema_migrations_models`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `seed_data`
- `workbench`
- `agentic_document_instruction_intake`
- `governed_datastore_crud`
- `ai_agent_task_assistance`
- `configuration_workbench`
- `continuous_release_assurance`

### advanced_capabilities
- `identity_kyc_aml_compliance_event_sourced_operational_history`
- `identity_kyc_aml_compliance_multi_tenant_policy_isolation`
- `identity_kyc_aml_compliance_schema_evolution_resilience`
- `identity_kyc_aml_compliance_autonomous_anomaly_detection`
- `identity_kyc_aml_compliance_semantic_document_instruction_understanding`
- `identity_kyc_aml_compliance_predictive_risk_scoring`
- `identity_kyc_aml_compliance_counterfactual_scenario_simulation`
- `identity_kyc_aml_compliance_cryptographic_audit_proofs`
- `identity_kyc_aml_compliance_continuous_control_testing`
- `identity_kyc_aml_compliance_carbon_and_sustainability_awareness`
- `identity_kyc_aml_compliance_cross_pbc_event_federation`
- `identity_kyc_aml_compliance_governed_ai_agent_execution`

The listed tables are owned by the package datastore and are materialized by schema, migration, and model artifacts. The API routes implement service command and query contracts, the emitted and consumed events use AppGen-X outbox, inbox, idempotent retry, and dead-letter handlers, and the UI fragments expose forms, wizards, controls, configuration editors, RBAC permission gates, and agent/chatbot guidance. Configuration keys, standard features, and advanced capabilities are backed by rule, parameter, seed, package registration, discovery, and release evidence. Supported ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
