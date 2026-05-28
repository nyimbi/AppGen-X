# Restaurant Operations PBC

## Purpose

The `restaurant_operations` PBC is a packaged business capability for Menus, recipes, kitchen production, reservations, food cost, labor, waste, and service execution. It owns schema, migrations, models, services, API contracts, AppGen-X event contracts, handlers, UI fragments, AI agent skills, configuration, rules, parameters, seed data, package metadata, tests, and release evidence. It composes with other AppGen-X PBCs only through declared APIs, AppGen-X events, or package-local projections.

## Stable Identity

- PBC key: `restaurant_operations`.
- Mesh: `opsmfg`.
- Package directory: `src/pyAppGen/pbcs/restaurant_operations`.
- Runtime entrypoint: `restaurant_operations_runtime_capabilities()`.
- UI entrypoint: `restaurant_operations_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X outbox/inbox event contract.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

- `restaurant_operations_menu_item`: owns menu item lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_recipe`: owns recipe lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_kitchen_ticket`: owns kitchen ticket lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_reservation`: owns reservation lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_inventory_prep`: owns inventory prep lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_food_waste`: owns food waste lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_labor_shift`: owns labor shift lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_restaurant_operations_policy_rule`: owns restaurant operations policy rule lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_restaurant_operations_runtime_parameter`: owns restaurant operations runtime parameter lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_restaurant_operations_schema_extension`: owns restaurant operations schema extension lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_restaurant_operations_control_assertion`: owns restaurant operations control assertion lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.
- `restaurant_operations_restaurant_operations_governed_model`: owns restaurant operations governed model lifecycle state, evidence, tenant boundary, status, versioning, and audit timestamps.

Runtime AppGen-X event tables are `restaurant_operations_appgen_outbox_event`, `restaurant_operations_appgen_inbox_event`, and `restaurant_operations_appgen_dead_letter_event`. The PBC does not mutate foreign tables. Dependencies are represented by consumed events ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged') and API contracts ('POST /menu-items', 'POST /recipes', 'POST /kitchen-tickets', 'POST /reservations', 'POST /inventory-preps', 'GET /restaurant-operations-workbench').

## Executable Domain Operations

- `create_menu_item`: validates policy, writes owned `restaurant_operations_menu_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_recipe`: validates policy, writes owned `restaurant_operations_recipe` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_kitchen_ticket`: validates policy, writes owned `restaurant_operations_kitchen_ticket` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_reservation`: validates policy, writes owned `restaurant_operations_reservation` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_inventory_prep`: validates policy, writes owned `restaurant_operations_inventory_prep` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_food_waste`: validates policy, writes owned `restaurant_operations_food_waste` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_labor_shift`: validates policy, writes owned `restaurant_operations_labor_shift` records, emits AppGen-X events, and returns side-effect-free evidence.
- `review_restaurant_operations_policy_rule`: validates policy, writes owned `restaurant_operations_restaurant_operations_policy_rule` records, emits AppGen-X events, and returns side-effect-free evidence.
- `approve_restaurant_operations_runtime_parameter`: validates policy, writes owned `restaurant_operations_restaurant_operations_runtime_parameter` records, emits AppGen-X events, and returns side-effect-free evidence.
- `simulate_restaurant_operations_schema_extension`: validates policy, writes owned `restaurant_operations_restaurant_operations_schema_extension` records, emits AppGen-X events, and returns side-effect-free evidence.
- `create_restaurant_operations_control_assertion`: validates policy, writes owned `restaurant_operations_restaurant_operations_control_assertion` records, emits AppGen-X events, and returns side-effect-free evidence.
- `record_restaurant_operations_governed_model`: validates policy, writes owned `restaurant_operations_restaurant_operations_governed_model` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_13`: validates policy, writes owned `restaurant_operations_appgen_outbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_14`: validates policy, writes owned `restaurant_operations_appgen_inbox_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_15`: validates policy, writes owned `restaurant_operations_appgen_dead_letter_event` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_16`: validates policy, writes owned `restaurant_operations_menu_item` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_17`: validates policy, writes owned `restaurant_operations_recipe` records, emits AppGen-X events, and returns side-effect-free evidence.
- `operate_restaurant_operations_18`: validates policy, writes owned `restaurant_operations_kitchen_ticket` records, emits AppGen-X events, and returns side-effect-free evidence.

Every command is deterministic and side-effect-free in package tests. Each command returns target owned tables, emitted event evidence, idempotency keys, rule decisions, parameter reads, permissions, and audit hashes.

## Standard Table-Stakes Capabilities

The package covers lifecycle intake, identity and classification, validation, approvals, exception handling, audit evidence, role-aware workbenches, assistant-guided task execution, configuration, rule compilation, bounded parameters, seed data, RBAC, route dispatch, typed events, idempotent handlers, retry, and dead-letter triage. It includes PostgreSQL, MySQL, and MariaDB backend allowlists and never exposes stream-engine pickers.

## Advanced Capabilities

- Event-sourced operational history for Restaurant Operations domain records.
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

Rules are first-class artifacts: ('menu_item_policy', 'recipe_policy', 'kitchen_ticket_policy', 'reservation_policy', 'inventory_prep_policy', 'food_waste_policy'). Parameters are bounded artifacts: ('quality_score_floor', 'materiality_threshold', 'approval_sla_hours', 'risk_threshold', 'forecast_horizon_days', 'workbench_limit'). Configuration includes database backend, event topic, retry limit, default policy, workbench limits, confirmation requirements for agent writes, and tenant isolation options.

## Public APIs and Services

APIs are ('POST /menu-items', 'POST /recipes', 'POST /kitchen-tickets', 'POST /reservations', 'POST /inventory-preps', 'GET /restaurant-operations-workbench'). Services preserve idempotency keys, permission names, owned table scopes, route metadata, and event mappings. Services write only to `restaurant_operations_` tables and package-local event tables.

## Events and Handlers

Emitted events: ('RestaurantOperationsCreated', 'RestaurantOperationsUpdated', 'RestaurantOperationsApproved', 'RestaurantOperationsExceptionOpened'). Consumed events: ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged'). Handlers require event IDs, ignore duplicates, record AppGen-X inbox entries, and write dead-letter evidence for unknown or exhausted events.

## UI, Workbench, and Agent Skills

Workbench views include ('menu item board', 'recipe board', 'kitchen ticket board', 'reservation board', 'inventory prep board', 'food waste board', 'labor shift board'). The UI exposes operational queues, detail panels, rule editors, parameter editors, assistant panels, exception triage, analytics, and release evidence. The agent contributes `restaurant_operations_skills`, parses documents and instructions, produces governed CRUD previews, validates owned table boundaries, requires human confirmation for writes, and participates in the composed single application assistant.

## Release Evidence and Tests

Release readiness proves schema, migrations, models, service contracts, route contracts, AppGen-X eventing, idempotent handlers, retry/dead-letter evidence, UI surfaces, RBAC, configuration, rules, parameters, seed data, package metadata, side-effect-free registration, domain-depth operations, agent integration, and generation smoke readiness. Focused package tests cover schema/service/release evidence, event contracts, package metadata, route contracts, governance hooks, and idempotent handlers.

## Manifest Traceability Appendix

- tables: menu_item, recipe, kitchen_ticket, reservation, inventory_prep, food_waste, labor_shift, restaurant_operations_policy_rule, restaurant_operations_runtime_parameter, restaurant_operations_schema_extension, restaurant_operations_control_assertion, restaurant_operations_governed_model
- operations: create_menu_item, record_recipe, review_kitchen_ticket, approve_reservation, simulate_inventory_prep, create_food_waste, record_labor_shift, review_restaurant_operations_policy_rule, approve_restaurant_operations_runtime_parameter, simulate_restaurant_operations_schema_extension, create_restaurant_operations_control_assertion, record_restaurant_operations_governed_model, operate_restaurant_operations_13, operate_restaurant_operations_14, operate_restaurant_operations_15, operate_restaurant_operations_16, operate_restaurant_operations_17, operate_restaurant_operations_18
- emits: RestaurantOperationsCreated, RestaurantOperationsUpdated, RestaurantOperationsApproved, RestaurantOperationsExceptionOpened
- consumes: PolicyChanged, AuditEventSealed, OperationalKpiChanged
- rules: menu_item_policy, recipe_policy, kitchen_ticket_policy, reservation_policy, inventory_prep_policy, food_waste_policy
- parameters: quality_score_floor, materiality_threshold, approval_sla_hours, risk_threshold, forecast_horizon_days, workbench_limit
- ui_fragments: RestaurantOperationsWorkbench, RestaurantOperationsDetail, RestaurantOperationsAssistantPanel
- permissions: restaurant_operations.read, restaurant_operations.create, restaurant_operations.update, restaurant_operations.approve, restaurant_operations.admin
- configuration: RESTAURANT_OPERATIONS_DATABASE_URL, RESTAURANT_OPERATIONS_EVENT_TOPIC, RESTAURANT_OPERATIONS_RETRY_LIMIT, RESTAURANT_OPERATIONS_DEFAULT_POLICY
- standard_features: menu_item_management, restaurant_operations_workflow, restaurant_operations_analytics, configuration_schema, rule_engine, parameter_engine, owned_schema_migrations_models, appgen_x_outbox_inbox_eventing, idempotent_handlers, retry_dead_letter_evidence, permissions, seed_data, workbench, agentic_document_instruction_intake, governed_datastore_crud, ai_agent_task_assistance, configuration_workbench, continuous_release_assurance
- advanced_capabilities: restaurant_operations_event_sourced_operational_history, restaurant_operations_multi_tenant_policy_isolation, restaurant_operations_schema_evolution_resilience, restaurant_operations_autonomous_anomaly_detection, restaurant_operations_semantic_document_instruction_understanding, restaurant_operations_predictive_risk_scoring, restaurant_operations_counterfactual_scenario_simulation, restaurant_operations_cryptographic_audit_proofs, restaurant_operations_continuous_control_testing, restaurant_operations_carbon_and_sustainability_awareness, restaurant_operations_cross_pbc_event_federation, restaurant_operations_governed_ai_agent_execution
