# Agriculture Supply Chain Traceability PBC

## Purpose

The `agri_supply_chain_traceability` PBC is a packaged business capability for Farm lots, inputs, certifications, storage, transport, recalls, provenance, and food traceability. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `agri_supply_chain_traceability`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/agri_supply_chain_traceability`.
- Runtime entrypoint: `agri_supply_chain_traceability_runtime_capabilities()`.
- UI entrypoint: `agri_supply_chain_traceability_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `agri_supply_chain_traceability_farm_lot`: owns farm lot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_input_batch`: owns input batch lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_certification`: owns certification lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_storage_event`: owns storage event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_transport_leg`: owns transport leg lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_recall_link`: owns recall link lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_provenance_proof`: owns provenance proof lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule`: owns agri supply chain traceability policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter`: owns agri supply chain traceability runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension`: owns agri supply chain traceability schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion`: owns agri supply chain traceability control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model`: owns agri supply chain traceability governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `agri_supply_chain_traceability_appgen_outbox_event`, `agri_supply_chain_traceability_appgen_inbox_event`, and `agri_supply_chain_traceability_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /farm-lots', 'POST /input-batchs', 'POST /certifications', 'POST /storage-events', 'POST /transport-legs', 'GET /agri-supply-chain-traceability-workbench').

## Executable Domain Operations

- `create_farm_lot`: validates policy, writes owned `agri_supply_chain_traceability_farm_lot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_input_batch`: validates policy, writes owned `agri_supply_chain_traceability_input_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_certification`: validates policy, writes owned `agri_supply_chain_traceability_certification` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_storage_event`: validates policy, writes owned `agri_supply_chain_traceability_storage_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_transport_leg`: validates policy, writes owned `agri_supply_chain_traceability_transport_leg` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_recall_link`: validates policy, writes owned `agri_supply_chain_traceability_recall_link` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_provenance_proof`: validates policy, writes owned `agri_supply_chain_traceability_provenance_proof` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_agri_supply_chain_traceability_policy_rule`: validates policy, writes owned `agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_agri_supply_chain_traceability_runtime_parameter`: validates policy, writes owned `agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_agri_supply_chain_traceability_schema_extension`: validates policy, writes owned `agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_agri_supply_chain_traceability_control_assertion`: validates policy, writes owned `agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_agri_supply_chain_traceability_governed_model`: validates policy, writes owned `agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_13`: validates policy, writes owned `agri_supply_chain_traceability_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_14`: validates policy, writes owned `agri_supply_chain_traceability_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_15`: validates policy, writes owned `agri_supply_chain_traceability_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_16`: validates policy, writes owned `agri_supply_chain_traceability_farm_lot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_17`: validates policy, writes owned `agri_supply_chain_traceability_input_batch` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_agri_supply_chain_traceability_18`: validates policy, writes owned `agri_supply_chain_traceability_certification` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Agriculture Supply Chain Traceability domain records.
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

Rules are first-class artifacts: ('farm_lot_policy', 'input_batch_policy', 'certification_policy', 'storage_event_policy', 'transport_leg_policy', 'recall_link_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /farm-lots', 'POST /input-batchs', 'POST /certifications', 'POST /storage-events', 'POST /transport-legs', 'GET /agri-supply-chain-traceability-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `agri_supply_chain_traceability_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('AgriSupplyChainTraceabilityCreated', 'AgriSupplyChainTraceabilityUpdated', 'AgriSupplyChainTraceabilityApproved', 'AgriSupplyChainTraceabilityExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('farm lot board', 'input batch board', 'certification board', 'storage event board', 'transport leg board', 'recall link board', 'provenance proof board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `agri_supply_chain_traceability_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: farm_lot, input_batch, certification, storage_event, transport_leg, recall_link, provenance_proof, agri_supply_chain_traceability_policy_rule, agri_supply_chain_traceability_runtime_parameter, agri_supply_chain_traceability_schema_extension, agri_supply_chain_traceability_control_assertion, agri_supply_chain_traceability_governed_model
- operations: create_farm_lot, record_input_batch, review_certification, approve_storage_event, simulate_transport_leg, create_recall_link, record_provenance_proof, review_agri_supply_chain_traceability_policy_rule, approve_agri_supply_chain_traceability_runtime_parameter, simulate_agri_supply_chain_traceability_schema_extension, create_agri_supply_chain_traceability_control_assertion, record_agri_supply_chain_traceability_governed_model, operate_agri_supply_chain_traceability_13, operate_agri_supply_chain_traceability_14, operate_agri_supply_chain_traceability_15, operate_agri_supply_chain_traceability_16, operate_agri_supply_chain_traceability_17, operate_agri_supply_chain_traceability_18
- emits: AgriSupplyChainTraceabilityCreated, AgriSupplyChainTraceabilityUpdated, AgriSupplyChainTraceabilityApproved, AgriSupplyChainTraceabilityExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: farm_lot_policy, input_batch_policy, certification_policy, storage_event_policy, transport_leg_policy, recall_link_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: AgriSupplyChainTraceabilityWorkbench, AgriSupplyChainTraceabilityDetail, AgriSupplyChainTraceabilityAssistantPanel
- permissions: agri_supply_chain_traceability.read, agri_supply_chain_traceability.create, agri_supply_chain_traceability.update, agri_supply_chain_traceability.approve, agri_supply_chain_traceability.admin
- configuration: AGRI_SUPPLY_CHAIN_TRACEABILITY_DATABASE_URL, AGRI_SUPPLY_CHAIN_TRACEABILITY_EVENT_TOPIC, AGRI_SUPPLY_CHAIN_TRACEABILITY_RETRY_LIMIT, AGRI_SUPPLY_CHAIN_TRACEABILITY_DEFAULT_POLICY
- standard_features: farm_lot_management, agri_supply_chain_traceability_workflow, agri_supply_chain_traceability_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: agri_supply_chain_traceability_event_sourced_operational_history, agri_supply_chain_traceability_multi_tenant_policy_isolation, agri_supply_chain_traceability_schema_evolution_resilience, agri_supply_chain_traceability_autonomous_anomaly_detection, agri_supply_chain_traceability_semantic_document_instruction_understanding, agri_supply_chain_traceability_predictive_risk_scoring, agri_supply_chain_traceability_counterfactual_scenario_simulation, agri_supply_chain_traceability_cryptographic_audit_proofs, agri_supply_chain_traceability_continuous_control_testing, agri_supply_chain_traceability_carbon_and_sustainability_awareness, agri_supply_chain_traceability_cross_pbc_event_federation, agri_supply_chain_traceability_governed_ai_agent_execution
