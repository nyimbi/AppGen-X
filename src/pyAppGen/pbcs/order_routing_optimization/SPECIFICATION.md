# Order Routing Optimization

Package-local implementation contract for the Order Routing Optimization PBC. The package owns fulfillment-routing policy, route candidates, capacity snapshots, routing decisions, node reservations, event evidence, rules, parameters, configuration, UI fragments, and release validation for optimized enterprise order routing.

## Stable Identity

- PBC key: `order_routing_optimization`.
- Implementation directory: `src/pyAppGen/pbcs/order_routing_optimization`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_order_routing_optimization_runtime.py`.
- Event topic: `appgen.order-routing.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `routing_rule`
- `route_candidate`
- `capacity_snapshot`
- `routing_decision`
- `node_reservation`
- `routing_parameter`
- `routing_configuration`
- `order_routing_optimization_appgen_outbox_event`
- `order_routing_optimization_appgen_inbox_event`
- `order_routing_optimization_dead_letter_event`

The PBC does not share order, inventory, tax, WMS, DOM, carrier, or checkout tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed AppGen-X events: `OrderVerified`, `AvailabilityProjected`, `TaxCalculated`.
- API dependencies: `POST /orders/verify`, `GET /availability-projections`, `GET /tax-calculations`, `GET /inventory-nodes`, `GET /wms-capacity`.
- Projections: `order_projection`, `availability_projection`, `tax_projection`, `inventory_projection`, `wms_capacity_projection`, and `dom_projection`.
- Emitted events: `FulfillmentRouteSelected` and `NodeCapacityReserved`.

## Standard Capabilities

- Routing rule management with eligible nodes, preferred nodes, region constraints, split policy, substitution mode, and capacity floors.
- Route candidate intake with node, region, order, inventory source, cost, SLA, risk, carbon, split, substitution, and graph-topology evidence.
- Capacity snapshot intake with available, reserved, available-to-promise, and forecast-gap calculations.
- Event intake for verified orders, availability projections, and tax quotes.
- Routing decision selection across candidate score, cost, SLA, capacity, risk, carbon, split policy, and substitution policy.
- Node reservation with hold duration and capacity decrement.
- Split-shipment routing when single-node capacity cannot satisfy the request and policy allows it.
- Substitution eligibility enforcement.
- Tenant isolation for rules, events, candidates, decisions, reservations, and workbench views.
- AppGen-X outbox/inbox records with idempotent handler keys.
- Retry and dead-letter evidence for failed event handling.
- Configuration schema, bounded parameter engine, compiled rule engine, seed runtime state, RBAC descriptors, API routes, and workbench fragments.

## Advanced Capabilities

- Event-sourced routing lifecycle with immutable hash-chain audit evidence.
- Graph-relational fulfillment topology across order, region, nodes, candidates, decisions, rules, and reservations.
- Probabilistic SLA, cost, capacity, risk, and carbon scoring.
- Counterfactual routing simulation for alternative nodes.
- Temporal capacity forecasting from capacity and demand paths.
- Autonomous routing exception recommendations for capacity shortfall, tax mismatch, carrier disruption, and inventory drift.
- Semantic route-request parsing for natural-language order, region, units, SLA, and split hints.
- Predictive fulfillment-risk scoring from stockout, tax variance, exception, and capacity-volatility signals.
- Self-healing route selection when selected nodes become unavailable.
- Cryptographic routing proof generation for selective disclosure.
- Dynamic routing policy screening for blocked nodes and carbon budgets.
- Continuous control tests for configuration, rules, parameters, event-contract safety, dead-letter backlog, and hash-chain integrity.
- Cross-system federation through order, inventory, tax, WMS, and DOM projections.
- Chaos-tolerant outbox replay for availability, tax, and worker-restart failures.
- Crypto-agile epoch rotation.
- Carbon-aware route scheduling.
- Mathematical route-network optimization.
- Auction-style capacity clearing across nodes.
- Routing anomaly detection with entropy evidence.
- Stochastic routing exposure modeling.
- Governed model registration with regulated and explainability evidence.
- Distributed-systems idempotency evidence on emitted reservation events.

## Runtime Services

- `configure_runtime` validates required configuration fields, exact AppGen-X event topic, backend, retry limit, supported regions, split policies, substitution modes, topology systems, timezone, and workbench limit.
- `set_parameter` accepts only supported bounded numeric routing parameters.
- `register_rule` validates routing-policy fields and stores deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table extensions with valid field identifiers.
- `handle_event` idempotently processes consumed events, records inbox evidence, schedules retries, and dead-letters exhausted failures.
- `ingest_capacity_snapshot` owns capacity projection and available-to-promise calculation.
- `upsert_route_candidate` owns route-candidate projection and tax/capacity scoring inputs.
- `route_orders` selects or splits fulfillment routes using rules, parameters, candidate scores, and capacity.
- `reserve_node_capacity` owns node reservations and capacity decrement.
- `build_api_contract` emits descriptor-level API, event, permission, dependency, and owned-table metadata.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational counts and release evidence.

## API Contract

- `POST /route-orders` maps to `route_orders`.
- `GET /route-candidates` maps to `build_workbench_view`.
- `POST /capacity` maps to `ingest_capacity_snapshot`.
- `POST /route-candidates` maps to `upsert_route_candidate`.
- `POST /order-routing/events/inbox` maps to `handle_event`.
- `GET /routing-workbench` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, and declared dependency evidence.

## Events And Handlers

Emitted events:

- `FulfillmentRouteSelected`
- `NodeCapacityReserved`

Consumed events:

- `OrderVerified`
- `AvailabilityProjected`
- `TaxCalculated`

Handlers are idempotent by event type and event id. Duplicate processed events do not append additional inbox entries. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules require:

- `rule_id`
- `tenant`
- `rule_type`
- `regions`
- `eligible_nodes`
- `capacity_floor`
- `split_policy`
- `substitution_mode`
- `status`

Parameters include:

- `cost_weight`
- `sla_weight`
- `capacity_weight`
- `risk_weight`
- `carbon_weight`
- `reservation_hold_minutes`
- `forecast_horizon_hours`
- `max_split_count`
- `simulation_sample_size`
- `confidence_floor`

Configuration includes backend, event topic, retry limit, default currency, supported regions, split policies, substitution modes, topology systems, default timezone, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, hidden stream-engine picker evidence, non-selectable event-contract evidence, and supported configuration fields.

## UI And Workbench

UI fragments:

- `OrderRoutingWorkbench`
- `RoutingRuleStudio`
- `RouteCandidateGrid`
- `CapacitySnapshotBoard`
- `RoutingDecisionLedger`
- `ReservationConsole`
- `CounterfactualSimulationLab`
- `RoutingInboxMonitor`
- `RoutingParameterConsole`
- `RoutingConfigurationPanel`
- `RoutingPolicyScreeningPanel`
- `RoutingAuditTrailView`

The workbench exposes route candidate, capacity, decision, split, reservation, inbox, outbox, dead-letter, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by route, capacity, event, configuration, and audit permissions.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, parameters, rules, schema extensions, event handling, capacity, candidates, decisions, reservations, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, unsupported configuration fields, unsupported parameters, out-of-range parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.
