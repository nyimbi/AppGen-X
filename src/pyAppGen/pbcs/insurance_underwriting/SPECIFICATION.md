# Insurance Underwriting PBC Specification

## Purpose

The `insurance_underwriting` package is a packaged business capability for underwriting intake, risk profiling, rating evidence, quote generation, authority-governed underwriting decisions, bind readiness, exclusions, configuration, rules, parameters, AppGen-X event evidence, package registration, and assistant-led underwriting workflows. The package is intentionally split into two aligned surfaces: a source-package contract used by repo-level PBC discovery and audits, and a package-local standalone app slice used to execute the underwriting lifecycle inside this directory. The PBC owns underwriting submissions, risk profiles, rating factors, quotes, underwriting decisions, bind packages, exclusions, governed rules, runtime parameters, schema extensions, control assertions, governed model metadata, and AppGen-X outbox, inbox, and dead-letter evidence.

## Stable Identity

- PBC key: `insurance_underwriting`.
- Package directory: `src/pyAppGen/pbcs/insurance_underwriting`.
- Runtime entrypoint: `insurance_underwriting_runtime_capabilities()`.
- UI entrypoint: `insurance_underwriting_ui_contract()`.
- Standalone entrypoint: `insurance_underwriting_standalone_app_contract()`.
- Self-registration entrypoint: `implementation_contract()` with side-effect-free discovery helpers and register plans.
- Allowed deployment datastore backends: PostgreSQL, MySQL, and MariaDB.
- Package-local execution datastore: sqlite for standalone development and verification only.
- Event contract: AppGen-X outbox/inbox/dead-letter with idempotent retry handling.
- Stream engine picker visibility: forbidden and hidden.

## Owned Boundary

Owned business tables are `insurance_underwriting_underwriting_submission`, `insurance_underwriting_risk_profile`, `insurance_underwriting_rating_factor`, `insurance_underwriting_quote`, `insurance_underwriting_underwriting_decision`, `insurance_underwriting_bind_package`, `insurance_underwriting_exclusion`, `insurance_underwriting_insurance_underwriting_policy_rule`, `insurance_underwriting_insurance_underwriting_runtime_parameter`, `insurance_underwriting_insurance_underwriting_schema_extension`, `insurance_underwriting_insurance_underwriting_control_assertion`, and `insurance_underwriting_insurance_underwriting_governed_model`. Owned runtime event tables are `insurance_underwriting_appgen_outbox_event`, `insurance_underwriting_appgen_inbox_event`, and `insurance_underwriting_appgen_dead_letter_event`.

The package does not mutate shared or foreign policy, claims, actuarial, broker, or accounting tables. Cross-PBC dependencies are represented only through declared APIs, consumed AppGen-X events, or package-local projections captured in owned tables. This owned boundary is enforced by schema generation, runtime boundary checks, governed CRUD plans, and release evidence.

## Schema, Migration, and Model Generation

Schema generation is materialized in `models.py`, `schema_contract.py`, and `migrations/001_initial.sql`. Every owned table has a model contract, an owned migration entry, and package-local sqlite execution support. Migration alignment checks verify that the migration file contains each owned table definition, and release evidence links schema, migration, model, and owned-boundary metadata together. The package exposes source-package schema contracts for repo audits and a standalone model contract for local execution.

## Service and API Contract

Source-package service contracts remain command and query oriented: `command_underwriting_submission`, `command_risk_profile`, `command_rating_factor`, `command_quote`, `command_underwriting_decision`, and `query_workbench`. Public API route contracts cover `POST /underwriting-submissions`, `POST /risk-profiles`, `POST /rating-factors`, `POST /quotes`, `POST /underwriting-decisions`, and `GET /insurance-underwriting-workbench`.

The standalone service adds executable command methods for create submission, build risk profile, review rating factor, generate quote, issue underwriting decision, assemble bind package, record exclusion, register rule, set parameter, receive event, and workflow execution. The standalone query surface supports workbench, detail, and timeline reads. Command and query contracts are separated, route validation checks idempotency requirements, and service execution stays inside owned datastore plus outbox boundaries.

## Events, Handlers, Retry, and Dead-Letter

Emitted AppGen-X events are `InsuranceUnderwritingCreated`, `InsuranceUnderwritingUpdated`, `InsuranceUnderwritingApproved`, and `InsuranceUnderwritingExceptionOpened`. Consumed AppGen-X events are `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`. Event envelopes capture event IDs, aggregate IDs, topics, occurred timestamps, payloads, and idempotency keys.

Handlers are idempotent, require an idempotency key, and route unsupported events to the dead-letter table with retry evidence. Retry policy is exponential with at least five attempts. Inbox capture creates control assertions so release evidence can prove event ingestion, retry, and dead-letter coverage.

## UI, Workbench, Permissions, and RBAC

The UI contract exposes `InsuranceUnderwritingWorkbench`, `InsuranceUnderwritingDetail`, `InsuranceUnderwritingAssistantPanel`, `SubmissionDetailPanel`, `ReferralQueueBoard`, `QuoteScenarioDesk`, `BindReadinessBoard`, `UnderwriterAssistantPanel`, `GovernanceStudio`, and `ReleaseEvidencePanel`. The workbench includes summary cards, referral queues, quote scenario comparisons, subjectivity checklist controls, and event operations console views.

Forms, wizards, and controls cover submission intake, risk profile construction, rating review, quote scenarios, underwriting decision review, bind readiness, exclusion capture, rule editing, parameter tuning, and event inbox operations. RBAC and permission evidence are materialized through action permissions, role maps, authority limits, approval checks, and configuration editor controls.

## Rules, Parameters, Configuration, and Seed Data

Rules are first-class artifacts: `submission_completeness_gate`, `risk_appetite_screening`, `rating_override_control`, `authority_matrix`, and `bind_readiness`. Parameters are bounded artifacts: `quality_score_floor`, `risk_threshold`, `quote_validity_days`, `auto_bind_limit`, `referral_sla_hours`, and `max_override_delta_pct`. Configuration schema covers database backend, event topic, workbench limit, appetite mode, default authority level, and assistant citation requirements.

Seed data includes starter underwriting rules, runtime parameters, and a default sample submission payload. Configuration schema, rule compilation, parameter edits, and seed evidence are all referenced by release readiness checks.

## Agent, Assistant, Chatbot Skills, and Mutations

The package contributes an underwriting assistant, chatbot, and skill surface with submission summary, risk profile explanation, referral memo drafting, quote scenario comparison, bind readiness review, document instruction intake, governed datastore CRUD, and workbench navigation. Document and instruction plans infer forms, wizards, candidate routes, and owned tables from underwriting documents such as applications, loss runs, or inspection reports.

All assistant mutations require a preview, owned-boundary validation, permission checks, and human confirmation. Governed CRUD planning explicitly references datastore mutation boundaries, assistant controls, and event audit plans.

## Self-Registration, Standard Features, Advanced Runtime, Release, and Tests

The package preserves side-effect-free self-registration through `register_pbc()`, `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()`. Standard features include underwriting submission management, insurance underwriting workflow, insurance underwriting analytics, configuration schema, rule engine, parameter engine, owned schema migrations models, AppGen-X outbox/inbox eventing, idempotent handlers, retry dead-letter evidence, permissions, seed data, workbench, agentic document instruction intake, governed datastore CRUD, AI agent task assistance, configuration workbench, standalone package-local app, and continuous release assurance.

Advanced capabilities include insurance underwriting event sourced operational history, multi-tenant policy isolation, schema evolution resilience, autonomous anomaly detection, semantic document instruction understanding, predictive risk scoring, counterfactual scenario simulation, cryptographic audit proofs, continuous control testing, carbon and sustainability awareness, cross-PBC event federation, and governed AI agent execution. Release evidence ties together schema, service, API, event, handler, UI, agent, governance, seed, documentation, and standalone app smoke results. Focused tests cover schema/service/release evidence, event contracts, registration, routes, governance hooks, idempotent handlers, incomplete-submission rejection, standalone lifecycle execution, and package smoke execution.

## Manifest Traceability Appendix

- tables: underwriting_submission, risk_profile, rating_factor, quote, underwriting_decision, bind_package, exclusion, insurance_underwriting_policy_rule, insurance_underwriting_runtime_parameter, insurance_underwriting_schema_extension, insurance_underwriting_control_assertion, insurance_underwriting_governed_model
- apis: POST /underwriting-submissions, POST /risk-profiles, POST /rating-factors, POST /quotes, POST /underwriting-decisions, GET /insurance-underwriting-workbench
- emits: InsuranceUnderwritingCreated, InsuranceUnderwritingUpdated, InsuranceUnderwritingApproved, InsuranceUnderwritingExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- ui_fragments: InsuranceUnderwritingWorkbench, InsuranceUnderwritingDetail, InsuranceUnderwritingAssistantPanel, SubmissionDetailPanel, ReferralQueueBoard, QuoteScenarioDesk, BindReadinessBoard, UnderwriterAssistantPanel
- permissions: insurance_underwriting.read, insurance_underwriting.create, insurance_underwriting.update, insurance_underwriting.approve, insurance_underwriting.admin, insurance_underwriting.submission.write, insurance_underwriting.quote.write, insurance_underwriting.decision.approve, insurance_underwriting.bind.approve
- configuration: INSURANCE_UNDERWRITING_DATABASE_URL, INSURANCE_UNDERWRITING_EVENT_TOPIC, INSURANCE_UNDERWRITING_RETRY_LIMIT, INSURANCE_UNDERWRITING_DEFAULT_POLICY, INSURANCE_UNDERWRITING_WORKBENCH_LIMIT, INSURANCE_UNDERWRITING_DEFAULT_AUTHORITY_LEVEL
- standard_features: underwriting_submission_management, insurance_underwriting_workflow, insurance_underwriting_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, standalone_package_local_app, continuous_release_assurance
- advanced_capabilities: insurance_underwriting_event_sourced_operational_history, insurance_underwriting_multi_tenant_policy_isolation, insurance_underwriting_schema_evolution_resilience, insurance_underwriting_autonomous_anomaly_detection, insurance_underwriting_semantic_document_instruction_understanding, insurance_underwriting_predictive_risk_scoring, insurance_underwriting_counterfactual_scenario_simulation, insurance_underwriting_cryptographic_audit_proofs, insurance_underwriting_continuous_control_testing, insurance_underwriting_carbon_and_sustainability_awareness, insurance_underwriting_cross_pbc_event_federation, insurance_underwriting_governed_ai_agent_execution
