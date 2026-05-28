# Advertising Campaign Operations PBC

## Purpose

The `advertising_campaign_operations` PBC is a packaged business capability for Campaigns, budgets, audiences, placements, creative approvals, performance, billing, and optimization. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `advertising_campaign_operations`.
- Mesh: `relationship`.
- Package directory: `src/pyAppGen/pbcs/advertising_campaign_operations`.
- Runtime entrypoint: `advertising_campaign_operations_runtime_capabilities()`.
- UI entrypoint: `advertising_campaign_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `advertising_campaign_operations_ad_campaign`: owns ad campaign lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_audience_segment`: owns audience segment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_media_placement`: owns media placement lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_creative_asset`: owns creative asset lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_campaign_budget`: owns campaign budget lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_performance_result`: owns performance result lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_billing_event`: owns billing event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_advertising_campaign_operations_policy_rule`: owns advertising campaign operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_advertising_campaign_operations_runtime_parameter`: owns advertising campaign operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_advertising_campaign_operations_schema_extension`: owns advertising campaign operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_advertising_campaign_operations_control_assertion`: owns advertising campaign operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `advertising_campaign_operations_advertising_campaign_operations_governed_model`: owns advertising campaign operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `advertising_campaign_operations_appgen_outbox_event`, `advertising_campaign_operations_appgen_inbox_event`, and `advertising_campaign_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified') and API contracts ('POST /ad-campaigns', 'POST /audience-segments', 'POST /media-placements', 'POST /creative-assets', 'POST /campaign-budgets', 'GET /advertising-campaign-operations-workbench').

## Executable Domain Operations

- `create_ad_campaign`: validates policy, writes owned `advertising_campaign_operations_ad_campaign` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_audience_segment`: validates policy, writes owned `advertising_campaign_operations_audience_segment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_media_placement`: validates policy, writes owned `advertising_campaign_operations_media_placement` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_creative_asset`: validates policy, writes owned `advertising_campaign_operations_creative_asset` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_campaign_budget`: validates policy, writes owned `advertising_campaign_operations_campaign_budget` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_performance_result`: validates policy, writes owned `advertising_campaign_operations_performance_result` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_billing_event`: validates policy, writes owned `advertising_campaign_operations_billing_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_advertising_campaign_operations_policy_rule`: validates policy, writes owned `advertising_campaign_operations_advertising_campaign_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_advertising_campaign_operations_runtime_parameter`: validates policy, writes owned `advertising_campaign_operations_advertising_campaign_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_advertising_campaign_operations_schema_extension`: validates policy, writes owned `advertising_campaign_operations_advertising_campaign_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_advertising_campaign_operations_control_assertion`: validates policy, writes owned `advertising_campaign_operations_advertising_campaign_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_advertising_campaign_operations_governed_model`: validates policy, writes owned `advertising_campaign_operations_advertising_campaign_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_13`: validates policy, writes owned `advertising_campaign_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_14`: validates policy, writes owned `advertising_campaign_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_15`: validates policy, writes owned `advertising_campaign_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_16`: validates policy, writes owned `advertising_campaign_operations_ad_campaign` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_17`: validates policy, writes owned `advertising_campaign_operations_audience_segment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_advertising_campaign_operations_18`: validates policy, writes owned `advertising_campaign_operations_media_placement` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Advertising Campaign Operations domain records.
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

Rules are first-class artifacts: ('ad_campaign_policy', 'audience_segment_policy', 'media_placement_policy', 'creative_asset_policy', 'campaign_budget_policy', 'performance_result_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /ad-campaigns', 'POST /audience-segments', 'POST /media-placements', 'POST /creative-assets', 'POST /campaign-budgets', 'GET /advertising-campaign-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `advertising_campaign_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AdvertisingCampaignOperationsCreated', 'AdvertisingCampaignOperationsUpdated', 'AdvertisingCampaignOperationsApproved', 'AdvertisingCampaignOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('ad campaign board', 'audience segment board', 'media placement board', 'creative asset board', 'campaign budget board', 'performance result board', 'billing event board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `advertising_campaign_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: ad_campaign, audience_segment, media_placement, creative_asset, campaign_budget, performance_result, billing_event, advertising_campaign_operations_policy_rule, advertising_campaign_operations_runtime_parameter, advertising_campaign_operations_schema_extension, advertising_campaign_operations_control_assertion, advertising_campaign_operations_governed_model
- operations: create_ad_campaign, record_audience_segment, review_media_placement, approve_creative_asset, simulate_campaign_budget, create_performance_result, record_billing_event, review_advertising_campaign_operations_policy_rule, approve_advertising_campaign_operations_runtime_parameter, simulate_advertising_campaign_operations_schema_extension, create_advertising_campaign_operations_control_assertion, record_advertising_campaign_operations_governed_model, operate_advertising_campaign_operations_13, operate_advertising_campaign_operations_14, operate_advertising_campaign_operations_15, operate_advertising_campaign_operations_16, operate_advertising_campaign_operations_17, operate_advertising_campaign_operations_18
- emits: AdvertisingCampaignOperationsCreated, AdvertisingCampaignOperationsUpdated, AdvertisingCampaignOperationsApproved, AdvertisingCampaignOperationsExceptionOpened
- consumes: PolicyChanged, CustomerUpdated, SupplierQualified
- rules: ad_campaign_policy, audience_segment_policy, media_placement_policy, creative_asset_policy, campaign_budget_policy, performance_result_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AdvertisingCampaignOperationsWorkbench, AdvertisingCampaignOperationsDetail, AdvertisingCampaignOperationsAssistantPanel
- permissions: advertising_campaign_operations.read, advertising_campaign_operations.create, advertising_campaign_operations.update, advertising_campaign_operations.approve, advertising_campaign_operations.admin
- configuration: ADVERTISING_CAMPAIGN_OPERATIONS_DATABASE_URL, ADVERTISING_CAMPAIGN_OPERATIONS_EVENT_TOPIC, ADVERTISING_CAMPAIGN_OPERATIONS_RETRY_LIMIT, ADVERTISING_CAMPAIGN_OPERATIONS_DEFAULT_POLICY
- standard_features: ad_campaign_management, advertising_campaign_operations_workflow, advertising_campaign_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: advertising_campaign_operations_event_sourced_operational_history, advertising_campaign_operations_multi_tenant_policy_isolation, advertising_campaign_operations_schema_evolution_resilience, advertising_campaign_operations_autonomous_anomaly_detection, advertising_campaign_operations_semantic_document_instruction_understanding, advertising_campaign_operations_predictive_risk_scoring, advertising_campaign_operations_counterfactual_scenario_simulation, advertising_campaign_operations_cryptographic_audit_proofs, advertising_campaign_operations_continuous_control_testing, advertising_campaign_operations_carbon_and_sustainability_awareness, advertising_campaign_operations_cross_pbc_event_federation, advertising_campaign_operations_governed_ai_agent_execution
