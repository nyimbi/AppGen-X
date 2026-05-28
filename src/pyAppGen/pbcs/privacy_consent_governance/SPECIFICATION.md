# Privacy Consent Governance PBC Specification

## Stable Identity

The `privacy_consent_governance` pbc is a package-owned business capability in the `platform` mesh. It owns the implementation directory `src/pyAppGen/pbcs/privacy_consent_governance` and exposes a stable manifest, side-effect-free registration, discovery metadata, release evidence, and package-local tests. The PBC description is: Data subject rights, consent, retention policies, processing purposes, disclosure logs, impact assessments, and compliance evidence.

## Owned Boundary

The package owns its datastore boundary and does not mutate shared or foreign tables. All owned table names are generated under the `privacy_consent_governance_` prefix in schema contracts, models, migrations, service operation contracts, event handlers, UI workbench projections, and agent CRUD plans. Cross-PBC collaboration is represented through APIs, AppGen-X events, and read-only projections rather than shared table writes.

## Schema, Migration, and Models

The schema contract declares every owned table, field set, relationship, migration path, and model descriptor. The migration creates tables for PostgreSQL, MySQL, and MariaDB compatible backends. The model manifest proves that every runtime-owned table has a generated model and that relationships point only to owned tables. Schema extensions are governed by rule and parameter controls.

## Service, API, Command, and Query Contracts

The service layer separates command methods from read-only query methods. Commands use the owned datastore plus outbox transaction boundary. Queries read package projections without emitting events. API route contracts include idempotency keys, route metadata, validation evidence, and dispatch plans. The service contract exposes command, query, workbench, schema, release, configuration, parameter, and rule operations.

## Events and Handlers

Events use the AppGen-X contract with outbox, inbox, idempotency, retry, and dead-letter handling. The package emits typed domain events and consumes declared dependency events. Handlers are idempotent and retryable; unknown events are routed to the dead-letter table with retry evidence. Users do not select eventing engines or stream-engine pickers.

## UI, Workbench, Permissions, Rules, Parameters, and Configuration

The UI exposes workbench fragments for operations, records, rules, agent assistance, and configuration editing. Permissions and RBAC descriptors gate read, create, update, approve, and admin actions. Configuration schemas, rule manifests, parameter manifests, seed data, and governance smoke tests are package-local and executable.

## Agent, Chatbot, Skills, Documents, and CRUD

The PBC contributes first-class agent skills into the composed application single assistant under the `privacy_consent_governance_skills` namespace. The chatbot helps users accomplish tasks, accepts documents and instructions, proposes governed datastore CRUD mutations, rejects foreign table mutation, requires human confirmation for writes, and emits AppGen-X event plans. Skills are expressible in the DSL through composed assistant tool names.

## Standard and Advanced Capabilities

Standard capabilities cover table-stakes business operations, owned schema generation, service/API/event implementation, UI workbench coverage, configuration, rule, parameter, seed, permission, and release evidence. Advanced capabilities add event-sourced history, multi-tenant isolation, semantic document understanding, predictive scoring, counterfactual simulation, cryptographic audit proof, control testing, carbon awareness, cross-PBC event federation, and governed AI agent execution.

## Release, Tests, Seed, and Registration

Release evidence is materialized in `RELEASE_EVIDENCE.md` and `release_evidence.py`. Tests cover generated schema, service, release evidence, event contracts, handlers, agent chatbot skills, side-effect-free registration, service routes, configuration, permissions, and seed hooks. Registration is side-effect-free: `register_pbc`, `registration_plan`, `package_metadata_manifest`, `validate_package_metadata`, and `package_discovery_plan` return plans and metadata without mutating the catalog.

## Datastore and Event Policy

Ordinary datastore backends are limited to postgresql, mysql, and mariadb. Eventing is AppGen-X. The package includes outbox, inbox, dead-letter, retry, idempotent handler, and release-audit evidence without exposing stream-engine choices to users.

## Manifest Traceability Appendix

- tables: data_subject_profile, consent_record, processing_purpose, retention_policy, privacy_request, disclosure_log, privacy_impact_assessment, privacy_compliance_evidence
- apis: POST /privacy-requests, POST /consents, POST /processing-purposes, POST /retention-policies, GET /privacy-governance-workbench
- emits: ConsentRecorded, PrivacyRequestOpened, RetentionPolicyChanged, PrivacyAssessmentCompleted
- consumes: CustomerUpdated, AccessPolicyChanged, AuditProofGenerated
- ui_fragments: PrivacyConsentGovernanceWorkbench, PrivacyConsentGovernanceDetail, PrivacyConsentGovernanceAssistantPanel
- permissions: privacy_consent_governance.read, privacy_consent_governance.create, privacy_consent_governance.update, privacy_consent_governance.approve, privacy_consent_governance.admin
- configuration: PRIVACY_CONSENT_GOVERNANCE_DATABASE_URL, PRIVACY_CONSENT_GOVERNANCE_EVENT_TOPIC, PRIVACY_CONSENT_GOVERNANCE_RETRY_LIMIT, PRIVACY_CONSENT_GOVERNANCE_DEFAULT_POLICY
- standard_features: data_subject_profile_management, privacy_consent_governance_workflow, privacy_consent_governance_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud
- advanced_capabilities: privacy_consent_governance_event_sourced_operational_history, privacy_consent_governance_multi_tenant_policy_isolation, privacy_consent_governance_schema_evolution_resilience, privacy_consent_governance_autonomous_anomaly_detection, privacy_consent_governance_semantic_document_instruction_understanding, privacy_consent_governance_predictive_risk_scoring, privacy_consent_governance_counterfactual_scenario_simulation, privacy_consent_governance_cryptographic_audit_proofs, privacy_consent_governance_continuous_control_testing, privacy_consent_governance_carbon_and_sustainability_awareness, privacy_consent_governance_cross_pbc_event_federation, privacy_consent_governance_governed_ai_agent_execution

## Operational Rulebook and Advanced Execution Scenarios

The `privacy_consent_governance` package treats rules, parameters, and configuration as runtime-operational artifacts rather than static documentation. Domain teams can register policies for consent capture, purpose grants, data subject requests, privacy notices, processing records, retention decisions, and evidence packs; each policy is versioned, explainable, and evaluated before command execution. Parameters tune thresholds, approval tiers, retry limits, default ownership, workbench filters, agent confirmation gates, and exception severity without changing generated source. The same rulebook feeds API validation, service command guards, workbench indicators, agent recommendations, release evidence, and generated DSL metadata so composed applications preserve one consistent operating model.

Advanced execution scenarios prove that the PBC is useful beyond catalog presence. The runtime can simulate command impact, emit a governed outbox event, update only owned tables, and produce an evidence payload showing which rules fired, which parameters were read, which permissions were required, and which downstream dependencies receive API or event notifications. Exception flows explicitly route consent withdrawal, subject request deadlines, purpose conflicts, retention exceptions, and policy changes. The agent skill layer can translate uploaded instructions, emails, spreadsheets, policy notes, and document packets into proposed CRUD plans, but it never performs writes without the datastore boundary check and confirmation contract. These scenarios are included so generated applications can compose this PBC into a single assistant, expose professional UI workbenches, and audit every autonomous recommendation back to owned schema, service commands, event contracts, handlers, and release evidence.
