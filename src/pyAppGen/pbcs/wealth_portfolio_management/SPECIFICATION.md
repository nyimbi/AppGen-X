# Wealth Portfolio Management PBC

## Purpose

`wealth_portfolio_management` is a package-local packaged business capability for advisor-led household portfolio management. The package owns the portfolio lifecycle inside its boundary: household and client profile capture, investment mandate and investment policy statement maintenance, suitability and risk readiness, portfolio drift monitoring, tax-aware rebalance proposal authoring, fee and performance evidence, advisor review workflows, document readiness, and compliance surveillance. The package is designed for AppGen-X composition, so every workflow is expressed as source-controlled schema, services, routes, UI fragments, governed agent skills, tests, and release evidence rather than hidden runtime magic.

## Stable Identity

- PBC key: `wealth_portfolio_management`
- Label: `Wealth Portfolio Management`
- Mesh: `finops`
- Package directory: `src/pyAppGen/pbcs/wealth_portfolio_management`
- Runtime entrypoint: `wealth_portfolio_management_runtime_capabilities()`
- UI entrypoint: `wealth_portfolio_management_ui_contract()`
- Standalone entrypoint: `wealth_portfolio_management_standalone_app_contract()`
- Side-effect-free package registration: `register_pbc()`, `registration_plan()`, `package_metadata_manifest()`, and `package_discovery_plan()`

The package keeps one stable identity across source audit, package discovery, generation smoke, and standalone workbench execution. The source registration entrypoints are intentionally side-effect free so repository audits can prove package discovery without mutating any catalog or shared runtime state.

## Owned Boundary And Datastore Policy

Deployment-facing ownership stays on package-local tables prefixed with `wealth_portfolio_management_`. The source package contract owns `wealth_portfolio_management_client_portfolio`, `wealth_portfolio_management_investment_mandate`, `wealth_portfolio_management_suitability_profile`, `wealth_portfolio_management_rebalance_order`, `wealth_portfolio_management_performance_snapshot`, `wealth_portfolio_management_fee_schedule`, `wealth_portfolio_management_advisory_review`, `wealth_portfolio_management_wealth_portfolio_management_policy_rule`, `wealth_portfolio_management_wealth_portfolio_management_runtime_parameter`, `wealth_portfolio_management_wealth_portfolio_management_schema_extension`, `wealth_portfolio_management_wealth_portfolio_management_control_assertion`, and `wealth_portfolio_management_wealth_portfolio_management_governed_model`, plus the AppGen-X outbox, inbox, and dead-letter tables.

No foreign or shared table is mutated. External client mastering, custody books, security mastering, and execution systems are represented only through declared APIs, AppGen-X events, or package-local projections. The package explicitly supports PostgreSQL, MySQL, and MariaDB for deployment. The standalone execution harness uses sqlite only inside the package directory for focused tests and smoke evidence; it does not change the deployment datastore policy.

## Schema, Migrations, And Models

The source package materializes owned schema through `migrations/001_initial.sql`, `schema_contract.py`, and `models.py`. Source-owned records intentionally keep a common envelope with `id`, `tenant`, `code`, `status`, `version`, `payload`, `created_at`, and `updated_at` so the package can hold wealth-specific detail without leaking across bounded contexts. Rich wealth detail is stored inside the payload envelope for household goals, IPS settings, benchmark history, risk data, holdings, tax lots, drift, fee projections, review evidence, and compliance findings.

The standalone sqlite harness deepens that source contract by materializing executable local tables for document packages and surveillance alerts in addition to the owned business tables and AppGen-X event evidence. This keeps the generated source package compact while still giving the PBC a usable one-package workbench.

## Services, APIs, And Commands

The source service surface preserves deterministic contract evidence for `configure_runtime`, `set_parameter`, `register_rule`, `command_client_portfolio`, and the wealth-specific domain operation set. The standalone service layer adds executable workflows that an advisor workbench can actually run:

- create household and client portfolio records
- capture investment policy and mandate evidence
- record suitability and risk-capacity evidence
- record fee schedule projections
- ingest document packages and missing-document evidence
- generate tax-aware trade proposals from model drift, restrictions, and cash needs
- record performance snapshots
- record advisor review outcomes
- run compliance surveillance over suitability, drift, cash needs, documents, and review state

Public APIs remain `POST /client-portfolios`, `POST /investment-mandates`, `POST /suitability-profiles`, `POST /rebalance-orders`, `POST /performance-snapshots`, and `GET /wealth-portfolio-management-workbench`. The package-local standalone workbench adds internal execution routes under `/app/wealth-portfolio-management/...` for onboarding, rebalancing, surveillance, and detail views.

## Eventing, Handlers, And Retry

AppGen-X is the only eventing contract. Emitted events are `WealthPortfolioManagementCreated`, `WealthPortfolioManagementUpdated`, `WealthPortfolioManagementApproved`, and `WealthPortfolioManagementExceptionOpened`. Consumed events are `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`. Unknown inbound events are routed to `wealth_portfolio_management_appgen_dead_letter_event`, known inbound events are recorded in `wealth_portfolio_management_appgen_inbox_event`, and all outbound operational activity is recorded in `wealth_portfolio_management_appgen_outbox_event`.

The package hides all stream-engine selectors. No stream-engine picker is exposed in configuration, services, UI, routes, or agent surfaces. The event contract is fixed to AppGen-X with idempotency keys, retry evidence, and dead-letter handling.

## Rules, Parameters, Configuration, And Seed Data

Rule and parameter handling are first-class source artifacts. Rules cover client portfolio policy, investment policy statement policy, suitability profile policy, restriction policy, cash needs policy, tax lot policy, and advisor review policy. Parameters cover drift tolerance, cash buffer months, tax budget limits, review cycle days, wash-sale window days, and workbench limits.

Configuration is represented by `WEALTH_PORTFOLIO_MANAGEMENT_DATABASE_URL`, `WEALTH_PORTFOLIO_MANAGEMENT_EVENT_TOPIC`, `WEALTH_PORTFOLIO_MANAGEMENT_RETRY_LIMIT`, and `WEALTH_PORTFOLIO_MANAGEMENT_DEFAULT_POLICY`. Seed hooks remain package-local and side-effect free so release audits can validate the existence of seed plans without mutating real state.

## UI, Workbench, Permissions, And Agent Skills

UI fragments remain `WealthPortfolioManagementWorkbench`, `WealthPortfolioManagementDetail`, and `WealthPortfolioManagementAssistantPanel`. The standalone workbench blueprint adds explicit forms, wizards, and controls for household onboarding, goal and risk capture, investment policy statements, trade proposal approval, advisor review, tax-aware rebalancing, cash planning, document collection, surveillance, drift heatmaps, restriction matrices, tax-lot grids, fee projection cards, document checklists, and a governed AI assistant panel.

Permissions are `wealth_portfolio_management.read`, `wealth_portfolio_management.create`, `wealth_portfolio_management.update`, `wealth_portfolio_management.approve`, and `wealth_portfolio_management.admin`. The package chatbot exposes `governed_datastore_crud` and document-instruction intake with confirmation-gated mutation skills. Every mutation-oriented skill requires confirmation before it can lead to a write path, and every CRUD preview validates that the target table stays inside the `wealth_portfolio_management_` boundary.

## Standard And Advanced Capabilities

Standard features include `client_portfolio_management`, `wealth_portfolio_management_workflow`, `wealth_portfolio_management_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `owned_schema_migrations_models`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `permissions`, `seed_data`, `workbench`, `agentic_document_instruction_intake`, `governed_datastore_crud`, `ai_agent_task_assistance`, `configuration_workbench`, and `continuous_release_assurance`.

Advanced capabilities include `wealth_portfolio_management_event_sourced_operational_history`, `wealth_portfolio_management_multi_tenant_policy_isolation`, `wealth_portfolio_management_schema_evolution_resilience`, `wealth_portfolio_management_autonomous_anomaly_detection`, `wealth_portfolio_management_semantic_document_instruction_understanding`, `wealth_portfolio_management_predictive_risk_scoring`, `wealth_portfolio_management_counterfactual_scenario_simulation`, `wealth_portfolio_management_cryptographic_audit_proofs`, `wealth_portfolio_management_continuous_control_testing`, `wealth_portfolio_management_carbon_and_sustainability_awareness`, `wealth_portfolio_management_cross_pbc_event_federation`, and `wealth_portfolio_management_governed_ai_agent_execution`.

## Release Evidence And Tests

Release readiness is package-local and explicit. The package proves source artifacts, schema, migrations, models, service contracts, route contracts, event contracts, handlers, permissions, configuration, rules, parameters, seed hooks, agent capability evidence, documentation, standalone app smoke, and repository audit compatibility. Focused tests cover source package contracts plus the standalone wealth workflow end to end. Release evidence is surfaced through `RELEASE_EVIDENCE.md`, `release_evidence.py`, `tests/test_contract.py`, and `tests/test_standalone.py`.

## Manifest Traceability Appendix

- tables: client_portfolio, investment_mandate, suitability_profile, rebalance_order, performance_snapshot, fee_schedule, advisory_review, wealth_portfolio_management_policy_rule, wealth_portfolio_management_runtime_parameter, wealth_portfolio_management_schema_extension, wealth_portfolio_management_control_assertion, wealth_portfolio_management_governed_model
- apis: POST /client-portfolios, POST /investment-mandates, POST /suitability-profiles, POST /rebalance-orders, POST /performance-snapshots, GET /wealth-portfolio-management-workbench
- emits: WealthPortfolioManagementCreated, WealthPortfolioManagementUpdated, WealthPortfolioManagementApproved, WealthPortfolioManagementExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- ui_fragments: WealthPortfolioManagementWorkbench, WealthPortfolioManagementDetail, WealthPortfolioManagementAssistantPanel
- permissions: wealth_portfolio_management.read, wealth_portfolio_management.create, wealth_portfolio_management.update, wealth_portfolio_management.approve, wealth_portfolio_management.admin
- configuration: WEALTH_PORTFOLIO_MANAGEMENT_DATABASE_URL, WEALTH_PORTFOLIO_MANAGEMENT_EVENT_TOPIC, WEALTH_PORTFOLIO_MANAGEMENT_RETRY_LIMIT, WEALTH_PORTFOLIO_MANAGEMENT_DEFAULT_POLICY
- standard_features: client_portfolio_management, wealth_portfolio_management_workflow, wealth_portfolio_management_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: wealth_portfolio_management_event_sourced_operational_history, wealth_portfolio_management_multi_tenant_policy_isolation, wealth_portfolio_management_schema_evolution_resilience, wealth_portfolio_management_autonomous_anomaly_detection, wealth_portfolio_management_semantic_document_instruction_understanding, wealth_portfolio_management_predictive_risk_scoring, wealth_portfolio_management_counterfactual_scenario_simulation, wealth_portfolio_management_cryptographic_audit_proofs, wealth_portfolio_management_continuous_control_testing, wealth_portfolio_management_carbon_and_sustainability_awareness, wealth_portfolio_management_cross_pbc_event_federation, wealth_portfolio_management_governed_ai_agent_execution
