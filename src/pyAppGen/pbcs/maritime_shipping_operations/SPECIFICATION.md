# Maritime Shipping Operations PBC

## Purpose

The `maritime_shipping_operations` PBC is a packaged business capability for Voyages, vessels, cargo, charter parties, port calls, demurrage, bunkers, and marine operations. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `maritime_shipping_operations`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/maritime_shipping_operations`.
- Runtime entrypoint: `maritime_shipping_operations_runtime_capabilities()`.
- UI entrypoint: `maritime_shipping_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `maritime_shipping_operations_voyage`: owns voyage lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_vessel`: owns vessel lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_cargo_booking`: owns cargo booking lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_charter_party`: owns charter party lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_port_call`: owns port call lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_demurrage_claim`: owns demurrage claim lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_bunker_event`: owns bunker event lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_maritime_shipping_operations_policy_rule`: owns maritime shipping operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_maritime_shipping_operations_runtime_parameter`: owns maritime shipping operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_maritime_shipping_operations_schema_extension`: owns maritime shipping operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_maritime_shipping_operations_control_assertion`: owns maritime shipping operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `maritime_shipping_operations_maritime_shipping_operations_governed_model`: owns maritime shipping operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `maritime_shipping_operations_appgen_outbox_event`, `maritime_shipping_operations_appgen_inbox_event`, and `maritime_shipping_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /voyages', 'POST /vessels', 'POST /cargo-bookings', 'POST /charter-partys', 'POST /port-calls', 'GET /maritime-shipping-operations-workbench').

## Executable Domain Operations

- `create_voyage`: validates policy, writes owned `maritime_shipping_operations_voyage` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_vessel`: validates policy, writes owned `maritime_shipping_operations_vessel` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_cargo_booking`: validates policy, writes owned `maritime_shipping_operations_cargo_booking` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_charter_party`: validates policy, writes owned `maritime_shipping_operations_charter_party` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_port_call`: validates policy, writes owned `maritime_shipping_operations_port_call` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_demurrage_claim`: validates policy, writes owned `maritime_shipping_operations_demurrage_claim` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_bunker_event`: validates policy, writes owned `maritime_shipping_operations_bunker_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_maritime_shipping_operations_policy_rule`: validates policy, writes owned `maritime_shipping_operations_maritime_shipping_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_maritime_shipping_operations_runtime_parameter`: validates policy, writes owned `maritime_shipping_operations_maritime_shipping_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_maritime_shipping_operations_schema_extension`: validates policy, writes owned `maritime_shipping_operations_maritime_shipping_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_maritime_shipping_operations_control_assertion`: validates policy, writes owned `maritime_shipping_operations_maritime_shipping_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_maritime_shipping_operations_governed_model`: validates policy, writes owned `maritime_shipping_operations_maritime_shipping_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_13`: validates policy, writes owned `maritime_shipping_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_14`: validates policy, writes owned `maritime_shipping_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_15`: validates policy, writes owned `maritime_shipping_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_16`: validates policy, writes owned `maritime_shipping_operations_voyage` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_17`: validates policy, writes owned `maritime_shipping_operations_vessel` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_maritime_shipping_operations_18`: validates policy, writes owned `maritime_shipping_operations_cargo_booking` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Maritime Shipping Operations domain records.
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

Rules are first-class artifacts: ('voyage_policy', 'vessel_policy', 'cargo_booking_policy', 'charter_party_policy', 'port_call_policy', 'demurrage_claim_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /voyages', 'POST /vessels', 'POST /cargo-bookings', 'POST /charter-partys', 'POST /port-calls', 'GET /maritime-shipping-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `maritime_shipping_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('MaritimeShippingOperationsCreated', 'MaritimeShippingOperationsUpdated', 'MaritimeShippingOperationsApproved', 'MaritimeShippingOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('voyage board', 'vessel board', 'cargo booking board', 'charter party board', 'port call board', 'demurrage claim board', 'bunker event board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `maritime_shipping_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: voyage, vessel, cargo_booking, charter_party, port_call, demurrage_claim, bunker_event, maritime_shipping_operations_policy_rule, maritime_shipping_operations_runtime_parameter, maritime_shipping_operations_schema_extension, maritime_shipping_operations_control_assertion, maritime_shipping_operations_governed_model
- operations: create_voyage, record_vessel, review_cargo_booking, approve_charter_party, simulate_port_call, create_demurrage_claim, record_bunker_event, review_maritime_shipping_operations_policy_rule, approve_maritime_shipping_operations_runtime_parameter, simulate_maritime_shipping_operations_schema_extension, create_maritime_shipping_operations_control_assertion, record_maritime_shipping_operations_governed_model, operate_maritime_shipping_operations_13, operate_maritime_shipping_operations_14, operate_maritime_shipping_operations_15, operate_maritime_shipping_operations_16, operate_maritime_shipping_operations_17, operate_maritime_shipping_operations_18
- emits: MaritimeShippingOperationsCreated, MaritimeShippingOperationsUpdated, MaritimeShippingOperationsApproved, MaritimeShippingOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: voyage_policy, vessel_policy, cargo_booking_policy, charter_party_policy, port_call_policy, demurrage_claim_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: MaritimeShippingOperationsWorkbench, MaritimeShippingOperationsDetail, MaritimeShippingOperationsAssistantPanel
- permissions: maritime_shipping_operations.read, maritime_shipping_operations.create, maritime_shipping_operations.update, maritime_shipping_operations.approve, maritime_shipping_operations.admin
- configuration: MARITIME_SHIPPING_OPERATIONS_DATABASE_URL, MARITIME_SHIPPING_OPERATIONS_EVENT_TOPIC, MARITIME_SHIPPING_OPERATIONS_RETRY_LIMIT, MARITIME_SHIPPING_OPERATIONS_DEFAULT_POLICY
- standard_features: voyage_management, maritime_shipping_operations_workflow, maritime_shipping_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: maritime_shipping_operations_event_sourced_operational_history, maritime_shipping_operations_multi_tenant_policy_isolation, maritime_shipping_operations_schema_evolution_resilience, maritime_shipping_operations_autonomous_anomaly_detection, maritime_shipping_operations_semantic_document_instruction_understanding, maritime_shipping_operations_predictive_risk_scoring, maritime_shipping_operations_counterfactual_scenario_simulation, maritime_shipping_operations_cryptographic_audit_proofs, maritime_shipping_operations_continuous_control_testing, maritime_shipping_operations_carbon_and_sustainability_awareness, maritime_shipping_operations_cross_pbc_event_federation, maritime_shipping_operations_governed_ai_agent_execution
