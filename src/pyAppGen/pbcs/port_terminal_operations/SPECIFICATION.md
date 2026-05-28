# Port Terminal Operations PBC

## Purpose

The `port_terminal_operations` PBC is a packaged business capability for Vessel calls, berths, yard moves, containers, equipment, customs handoffs, and terminal productivity. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `port_terminal_operations`.
- Mesh: `scl`.
- Package directory: `src/pyAppGen/pbcs/port_terminal_operations`.
- Runtime entrypoint: `port_terminal_operations_runtime_capabilities()`.
- UI entrypoint: `port_terminal_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `port_terminal_operations_vessel_call`: owns vessel call lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_berth_plan`: owns berth plan lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_container_move`: owns container move lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_yard_slot`: owns yard slot lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_gate_transaction`: owns gate transaction lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_terminal_equipment`: owns terminal equipment lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_customs_handoff`: owns customs handoff lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_port_terminal_operations_policy_rule`: owns port terminal operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_port_terminal_operations_runtime_parameter`: owns port terminal operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_port_terminal_operations_schema_extension`: owns port terminal operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_port_terminal_operations_control_assertion`: owns port terminal operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `port_terminal_operations_port_terminal_operations_governed_model`: owns port terminal operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `port_terminal_operations_appgen_outbox_event`, `port_terminal_operations_appgen_inbox_event`, and `port_terminal_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /vessel-calls', 'POST /berth-plans', 'POST /container-moves', 'POST /yard-slots', 'POST /gate-transactions', 'GET /port-terminal-operations-workbench').

## Executable Domain Operations

- `create_vessel_call`: validates policy, writes owned `port_terminal_operations_vessel_call` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_berth_plan`: validates policy, writes owned `port_terminal_operations_berth_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_container_move`: validates policy, writes owned `port_terminal_operations_container_move` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_yard_slot`: validates policy, writes owned `port_terminal_operations_yard_slot` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_gate_transaction`: validates policy, writes owned `port_terminal_operations_gate_transaction` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_terminal_equipment`: validates policy, writes owned `port_terminal_operations_terminal_equipment` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_customs_handoff`: validates policy, writes owned `port_terminal_operations_customs_handoff` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_port_terminal_operations_policy_rule`: validates policy, writes owned `port_terminal_operations_port_terminal_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_port_terminal_operations_runtime_parameter`: validates policy, writes owned `port_terminal_operations_port_terminal_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_port_terminal_operations_schema_extension`: validates policy, writes owned `port_terminal_operations_port_terminal_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_port_terminal_operations_control_assertion`: validates policy, writes owned `port_terminal_operations_port_terminal_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_port_terminal_operations_governed_model`: validates policy, writes owned `port_terminal_operations_port_terminal_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_13`: validates policy, writes owned `port_terminal_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_14`: validates policy, writes owned `port_terminal_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_15`: validates policy, writes owned `port_terminal_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_16`: validates policy, writes owned `port_terminal_operations_vessel_call` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_17`: validates policy, writes owned `port_terminal_operations_berth_plan` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_port_terminal_operations_18`: validates policy, writes owned `port_terminal_operations_container_move` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Port Terminal Operations domain records.
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

Rules are first-class artifacts: ('vessel_call_policy', 'berth_plan_policy', 'container_move_policy', 'yard_slot_policy', 'gate_transaction_policy', 'terminal_equipment_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /vessel-calls', 'POST /berth-plans', 'POST /container-moves', 'POST /yard-slots', 'POST /gate-transactions', 'GET /port-terminal-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `port_terminal_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('PortTerminalOperationsCreated', 'PortTerminalOperationsUpdated', 'PortTerminalOperationsApproved', 'PortTerminalOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('vessel call board', 'berth plan board', 'container move board', 'yard slot board', 'gate transaction board', 'terminal equipment board', 'customs handoff board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `port_terminal_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: vessel_call, berth_plan, container_move, yard_slot, gate_transaction, terminal_equipment, customs_handoff, port_terminal_operations_policy_rule, port_terminal_operations_runtime_parameter, port_terminal_operations_schema_extension, port_terminal_operations_control_assertion, port_terminal_operations_governed_model
- operations: create_vessel_call, record_berth_plan, review_container_move, approve_yard_slot, simulate_gate_transaction, create_terminal_equipment, record_customs_handoff, review_port_terminal_operations_policy_rule, approve_port_terminal_operations_runtime_parameter, simulate_port_terminal_operations_schema_extension, create_port_terminal_operations_control_assertion, record_port_terminal_operations_governed_model, operate_port_terminal_operations_13, operate_port_terminal_operations_14, operate_port_terminal_operations_15, operate_port_terminal_operations_16, operate_port_terminal_operations_17, operate_port_terminal_operations_18
- emits: PortTerminalOperationsCreated, PortTerminalOperationsUpdated, PortTerminalOperationsApproved, PortTerminalOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: vessel_call_policy, berth_plan_policy, container_move_policy, yard_slot_policy, gate_transaction_policy, terminal_equipment_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: PortTerminalOperationsWorkbench, PortTerminalOperationsDetail, PortTerminalOperationsAssistantPanel
- permissions: port_terminal_operations.read, port_terminal_operations.create, port_terminal_operations.update, port_terminal_operations.approve, port_terminal_operations.admin
- configuration: PORT_TERMINAL_OPERATIONS_DATABASE_URL, PORT_TERMINAL_OPERATIONS_EVENT_TOPIC, PORT_TERMINAL_OPERATIONS_RETRY_LIMIT, PORT_TERMINAL_OPERATIONS_DEFAULT_POLICY
- standard_features: vessel_call_management, port_terminal_operations_workflow, port_terminal_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: port_terminal_operations_event_sourced_operational_history, port_terminal_operations_multi_tenant_policy_isolation, port_terminal_operations_schema_evolution_resilience, port_terminal_operations_autonomous_anomaly_detection, port_terminal_operations_semantic_document_instruction_understanding, port_terminal_operations_predictive_risk_scoring, port_terminal_operations_counterfactual_scenario_simulation, port_terminal_operations_cryptographic_audit_proofs, port_terminal_operations_continuous_control_testing, port_terminal_operations_carbon_and_sustainability_awareness, port_terminal_operations_cross_pbc_event_federation, port_terminal_operations_governed_ai_agent_execution
