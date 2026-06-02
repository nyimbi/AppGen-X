# Donor Grant and Fundraising PBC

## Purpose

The `donor_grant_fundraising` PBC is a packaged business capability for donors, campaigns, pledges, restrictions, gifts, grant applications, stewardship, and impact reporting. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, release evidence, and a package-local standalone shell for one-PBC execution.

## Stable Identity

- PBC key: `donor_grant_fundraising`
- Mesh: `relationship`
- Package directory: `src/pyAppGen/pbcs/donor_grant_fundraising`
- Runtime entrypoint: `donor_grant_fundraising_runtime_capabilities()`
- Standalone entrypoint: `DonorGrantFundraisingStandaloneApplication`
- UI entrypoint: `donor_grant_fundraising_ui_contract()`
- Source registration entrypoint: `implementation_contract()`
- Allowed database backends: PostgreSQL, MySQL, and MariaDB
- Eventing standard: fixed AppGen-X outbox/inbox event contract
- User-facing stream-engine selector: forbidden and hidden

## Owned Datastore Boundary

Business tables:
- `donor_grant_fundraising_donor`
- `donor_grant_fundraising_campaign`
- `donor_grant_fundraising_pledge`
- `donor_grant_fundraising_gift`
- `donor_grant_fundraising_restriction`
- `donor_grant_fundraising_grant_application`
- `donor_grant_fundraising_stewardship_touchpoint`
- `donor_grant_fundraising_donor_relationship`
- `donor_grant_fundraising_proposal_workspace`
- `donor_grant_fundraising_acknowledgement`
- `donor_grant_fundraising_briefing_packet`
- `donor_grant_fundraising_opportunity_score`
- `donor_grant_fundraising_review_chain`
- `donor_grant_fundraising_budget_validation`

Governance tables:
- `donor_grant_fundraising_policy_rule`
- `donor_grant_fundraising_runtime_parameter`
- `donor_grant_fundraising_schema_extension`
- `donor_grant_fundraising_control_assertion`
- `donor_grant_fundraising_governed_model`

Runtime event tables:
- `donor_grant_fundraising_appgen_outbox_event`
- `donor_grant_fundraising_appgen_inbox_event`
- `donor_grant_fundraising_appgen_dead_letter_event`

The PBC never mutates foreign tables. Cross-PBC collaboration uses AppGen-X events or declared API contracts.

## Executable Domain Operations

- `create_donor`
- `advance_prospect_stage`
- `create_campaign`
- `create_pledge`
- `post_gift`
- `create_restriction`
- `manage_grant_application`
- `record_stewardship_touchpoint`
- `map_donor_relationship`
- `compose_proposal_workspace`
- `track_acknowledgement`
- `generate_briefing_packet`
- `score_fundraising_opportunity`
- `manage_review_chain`
- `validate_grant_budget`
- `review_policy_rule`
- `set_runtime_parameter`
- `register_schema_extension`
- `record_control_assertion`
- `register_governed_model`

Every command returns owned-table scope, emitted event evidence, idempotency metadata, rule decisions, parameter reads, and side-effect-free audit hashes in tests.

## Rules, Parameters, and Configuration

Rules are first-class artifacts: `donor_policy`, `campaign_policy`, `pledge_policy`, `gift_policy`, `restriction_policy`, `grant_application_policy`, `review_chain_policy`, and `budget_validation_policy`.

Parameters are bounded artifacts: `quality_score_floor`, `materiality_threshold`, `approval_sla_hours`, `risk_threshold`, `forecast_horizon_days`, and `workbench_limit`.

Configuration includes database backend, event topic, retry limit, default policy, workbench limit, and assistant confirmation requirements.

## Public APIs and Services

The package declares and dispatches these API contracts:
- `POST /donors`
- `POST /campaigns`
- `POST /pledges`
- `POST /gifts`
- `POST /restrictions`
- `POST /grant-applications`
- `POST /stewardship-touchpoints`
- `GET /donor-grant-fundraising-workbench`

The service layer executes runtime commands, standalone fundraising commands, and domain-depth operations without leaving the package boundary.

## Events and Handlers

Emitted events:
- `DonorGrantFundraisingCreated`
- `DonorGrantFundraisingUpdated`
- `DonorGrantFundraisingApproved`
- `DonorGrantFundraisingExceptionOpened`

Consumed events:
- `PolicyChanged`
- `CustomerUpdated`
- `SupplierQualified`

Handlers require idempotency keys, ignore duplicates, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

The workbench exposes queues for portfolio next actions, pledge exposure, acknowledgement backlog, grant deadline risk, proposal readiness, review blockers, budget validation failures, stewardship gaps, campaign performance, and exception backlog.

Forms, wizards, and controls cover donor profiles, prospect progression, campaigns, pledges, gifts, restrictions, grants, relationships, proposal workspaces, acknowledgements, review chains, and budget validation.

The assistant contributes proposal support, stewardship drafting, mutation preview, and operator guidance. All datastore mutations require human confirmation and remain constrained to owned tables.

## Standalone Shell

`standalone.py` provides a mutable package-local application shell that bootstraps configuration, registers default rules and parameters, seeds demo data, runs in-package domain commands, previews document-driven mutations, and renders a standalone workbench.

## Release Evidence and Tests

Release readiness proves schema, migration alignment, models, services, routes, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, standalone shell behavior, domain workflows, and package-local smoke tests.

## Advanced Capability Implementation Contract

The Donor Grant Fundraising PBC implements standard donor CRM, pledge, appeal, campaign, major-gift, institutional grant, restricted-fund, stewardship, receipt, and impact-reporting capabilities, plus advanced capabilities for propensity scoring, grant compliance reasoning, fraud and duplicate-gift anomaly detection, donor journey optimization, and governed AI assistance. Its owned tables remain inside the donor_grant_fundraising datastore and are exposed through generated schema, migration, and model artifacts only. Service command methods cover donor onboarding, pledge capture, campaign launch, grant application tracking, stewardship tasking, and receipt issuance; query methods cover portfolio, campaign, pipeline, compliance, and impact workbench views. API route contracts map those commands and queries to RBAC permissions, all using the AppGen-X event contract with outbox, inbox, idempotent handlers, retry policy, and dead-letter evidence. Configuration, rule, and parameter surfaces govern gift restrictions, acknowledgment deadlines, matching policies, grant eligibility, and stewardship SLAs. The chatbot skill surface can read donor documents and instructions, prepare side-effect-free CRUD mutation previews for owned datastore records, and join the composed application single agent through the donor_grant_fundraising_skills namespace. Package registration, package discovery, release evidence, seed data, and tests are side-effect-free and support PostgreSQL, MySQL, and MariaDB backends.
## Manifest Traceability Appendix

This appendix maps the executable manifest for `donor_grant_fundraising` to the implemented PBC package so release audits can verify that every declared surface is covered by the specification, code, UI, agent, tests, seed data, and AppGen-X integration evidence.

### tables
- `donor`
- `campaign`
- `pledge`
- `gift`
- `restriction`
- `grant_application`
- `stewardship_touchpoint`
- `donor_grant_fundraising_policy_rule`
- `donor_grant_fundraising_runtime_parameter`
- `donor_grant_fundraising_schema_extension`
- `donor_grant_fundraising_control_assertion`
- `donor_grant_fundraising_governed_model`

### apis
- `POST /donors`
- `POST /campaigns`
- `POST /pledges`
- `POST /gifts`
- `POST /restrictions`
- `GET /donor-grant-fundraising-workbench`

### emits
- `DonorGrantFundraisingCreated`
- `DonorGrantFundraisingUpdated`
- `DonorGrantFundraisingApproved`
- `DonorGrantFundraisingExceptionOpened`

### consumes
- `PolicyChanged`
- `CustomerUpdated`
- `SupplierQualified`

### ui_fragments
- `DonorGrantFundraisingWorkbench`
- `DonorGrantFundraisingDetail`
- `DonorGrantFundraisingAssistantPanel`

### permissions
- `donor_grant_fundraising.read`
- `donor_grant_fundraising.create`
- `donor_grant_fundraising.update`
- `donor_grant_fundraising.approve`
- `donor_grant_fundraising.admin`

### configuration
- `DONOR_GRANT_FUNDRAISING_DATABASE_URL`
- `DONOR_GRANT_FUNDRAISING_EVENT_TOPIC`
- `DONOR_GRANT_FUNDRAISING_RETRY_LIMIT`
- `DONOR_GRANT_FUNDRAISING_DEFAULT_POLICY`

### standard_features
- `donor_management`
- `donor_grant_fundraising_workflow`
- `donor_grant_fundraising_analytics`
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
- `donor_grant_fundraising_event_sourced_operational_history`
- `donor_grant_fundraising_multi_tenant_policy_isolation`
- `donor_grant_fundraising_schema_evolution_resilience`
- `donor_grant_fundraising_autonomous_anomaly_detection`
- `donor_grant_fundraising_semantic_document_instruction_understanding`
- `donor_grant_fundraising_predictive_risk_scoring`
- `donor_grant_fundraising_counterfactual_scenario_simulation`
- `donor_grant_fundraising_cryptographic_audit_proofs`
- `donor_grant_fundraising_continuous_control_testing`
- `donor_grant_fundraising_carbon_and_sustainability_awareness`
- `donor_grant_fundraising_cross_pbc_event_federation`
- `donor_grant_fundraising_governed_ai_agent_execution`

The listed tables are owned by the package datastore and are materialized by schema, migration, and model artifacts. The API routes implement service command and query contracts, the emitted and consumed events use AppGen-X outbox, inbox, idempotent retry, and dead-letter handlers, and the UI fragments expose forms, wizards, controls, configuration editors, RBAC permission gates, and agent/chatbot guidance. Configuration keys, standard features, and advanced capabilities are backed by rule, parameter, seed, package registration, discovery, and release evidence. Supported ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
