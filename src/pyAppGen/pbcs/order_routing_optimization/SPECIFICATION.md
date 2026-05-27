# Order Routing Optimization

Package-local implementation contract for the Order Routing Optimization PBC. The package owns order-routing plans, node topology and services, routing constraints and costs, delivery promises, split-shipment evidence, inventory/transport/service inputs, route simulation and optimization evidence, approvals, feedback, AppGen-X event evidence, UI/workbench bindings, and package-local release validation for optimized enterprise order routing.

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

Owned tables and generated descriptors:

- `routing_plan`
- `routing_plan_leg`
- `routing_node`
- `routing_node_calendar`
- `routing_node_service`
- `routing_node_capacity`
- `routing_constraint`
- `routing_cost_component`
- `routing_promise`
- `split_shipment`
- `split_shipment_leg`
- `inventory_input_projection`
- `transport_input_projection`
- `service_input_projection`
- `route_candidate`
- `capacity_snapshot`
- `routing_decision`
- `node_reservation`
- `route_simulation`
- `route_simulation_scenario`
- `optimization_run`
- `optimization_candidate`
- `routing_exception`
- `exception_resolution`
- `routing_approval`
- `routing_feedback`
- `routing_policy_screening`
- `routing_audit_trace`
- `routing_federation_projection`
- `routing_carbon_schedule`
- `routing_network_optimization`
- `routing_capacity_allocation`
- `routing_anomaly_signal`
- `routing_exposure_model`
- `routing_forecast`
- `routing_parsed_request`
- `routing_seed_data`
- `routing_schema_extension`
- `routing_control_assertion`
- `routing_governed_model`
- `routing_rule`
- `routing_parameter`
- `routing_configuration`
- `order_routing_optimization_appgen_outbox_event`
- `order_routing_optimization_appgen_inbox_event`
- `order_routing_optimization_dead_letter_event`

The package does not share checkout, order, inventory, tax, transportation, WMS, DOM, approval, or feedback tables. Cross-PBC integration is represented only by declared APIs, AppGen-X events, or read-only projections:

- Consumed AppGen-X events: `OrderVerified`, `AvailabilityProjected`, `TaxCalculated`.
- Emitted AppGen-X events: `FulfillmentRouteSelected`, `NodeCapacityReserved`.
- API dependencies: `POST /orders/verify`, `GET /availability-projections`, `GET /tax-calculations`, `GET /inventory-nodes`, `GET /wms-capacity`, `GET /transport-service-options`, `GET /delivery-promises`, `POST /routing-approvals`, and `POST /routing-feedback`.
- Projection dependencies: `order_projection`, `availability_projection`, `tax_projection`, `inventory_projection`, `wms_capacity_projection`, `dom_projection`, `transport_service_projection`, `delivery_promise_projection`, `approval_policy_projection`, and `feedback_signal_projection`.

## Standard Capabilities

- Routing-plan ownership for decision headers and plan legs.
- Routing-node, calendar, service, and capacity evidence.
- Routing-rule and routing-constraint management with deterministic compiled hashes.
- Route-candidate intake with region, cost, SLA, risk, carbon, split, and substitution evidence.
- Capacity snapshots with available-to-promise calculation and reservation decrement.
- Routing-cost and delivery-promise evidence per selected decision.
- Split-shipment evidence when a request is fulfilled across multiple nodes.
- Inventory, transport, and service inputs recorded from event and candidate intake.
- Routing decisions and node reservations with tenant isolation.
- AppGen-X outbox, inbox, retry, and dead-letter evidence.
- Idempotent event handling keyed by consumed event type and event id.
- Configuration schema, bounded parameter engine, package-local API descriptors, RBAC descriptors, and workbench fragments.
- Package-local `build_schema_contract()`, `build_service_contract()`, and `build_release_evidence()` exported through `__init__.implementation_contract()`.

## Advanced Capabilities

- Event-sourced routing lifecycle with immutable hash-chain audit evidence.
- Graph-relational routing topology across orders, regions, nodes, plans, constraints, candidates, decisions, promises, and reservations.
- Probabilistic cost, SLA, capacity, risk, and carbon scoring.
- Counterfactual route simulation for alternate nodes.
- Forecasting of future available capacity and saturation risk.
- Autonomous routing exception resolution recommendations.
- Natural-language route-request parsing.
- Predictive fulfillment-risk scoring.
- Self-healing route selection when nodes become unavailable.
- Cryptographic routing proof generation for selective disclosure.
- Dynamic routing policy screening for blocked nodes and carbon budgets.
- Carbon-aware scheduling, network optimization, and auction-style capacity allocation evidence.
- Routing anomaly detection and stochastic exposure modeling.
- Governed model registration with explainability and lineage evidence.
- Package-local release evidence combining schema, service, API, permissions, workbench, and eventing proofs.

## Schema Contract

`build_schema_contract()` emits:

- An owned-table contract covering all package-owned runtime and metadata tables.
- Field descriptors for plans, legs, nodes, constraints, costs, promises, splits, inputs, simulations, optimization runs, exceptions, approvals, feedback, rules, parameters, configuration, and AppGen-X evidence.
- Relationship descriptors connecting plans to legs, nodes to calendars/services/capacity, rules to constraints, decisions to costs/promises/reservations/approvals/feedback, simulations to scenarios, optimization runs to candidates, and exceptions to resolutions.
- Generated migration descriptors at `pbcs/order_routing_optimization/migrations/<nnn>_<table>.sql`.
- Generated model descriptors with package-local class names and field ownership evidence.
- Back-end allowlist evidence and explicit `shared_table_access: false`.

## Service Contract

`build_service_contract()` declares the transaction boundary as the Order Routing Optimization owned datastore plus the AppGen-X outbox.

Command methods include:

- `configure_runtime`
- `set_parameter`
- `register_rule`
- `register_schema_extension`
- `handle_event`
- `ingest_capacity_snapshot`
- `upsert_route_candidate`
- `route_orders`
- `reserve_node_capacity`
- `simulate_counterfactual`
- `forecast_capacity`
- `recommend_exception_resolution`
- `parse_route_request`
- `score_fulfillment_risk`
- `self_heal_route_selection`
- `generate_routing_proof`
- `screen_policy`
- `run_control_tests`
- `federate_routing_view`
- `run_resilience_drill`
- `rotate_crypto_epoch`
- `schedule_carbon_aware_route`
- `optimize_route_network`
- `clear_capacity_auction`
- `detect_routing_anomaly`
- `model_stochastic_exposure`
- `register_governed_model`

Query methods include:

- `build_workbench_view`
- `build_api_contract`
- `build_schema_contract`
- `build_service_contract`
- `build_release_evidence`
- `verify_owned_table_boundary`

The service contract also records owned-only mutation boundaries and declared external API, event, and projection dependencies with no shared-table access.

## Runtime Services

- `configure_runtime` validates all required configuration fields, exact AppGen-X event topic, relational backend, retry limit, supported regions, split policies, substitution modes, topology systems, timezone, and workbench limit.
- `set_parameter` accepts only supported bounded numeric routing parameters.
- `register_rule` validates rule fields and emits compiled routing-constraint evidence.
- `register_schema_extension` allows extensions only for package-owned tables and valid field identifiers.
- `handle_event` idempotently consumes `OrderVerified`, `AvailabilityProjected`, and `TaxCalculated`, updates order/inventory/service inputs, records inbox evidence, and preserves retry/dead-letter evidence.
- `ingest_capacity_snapshot` records capacity and routing-node evidence.
- `upsert_route_candidate` records route candidates plus transport/service input evidence.
- `route_orders` selects a standard route or split route, records plans, costs, promises, optimization runs, approvals, feedback, and node reservations, and emits AppGen-X outbox events.
- `reserve_node_capacity` decrements available-to-promise capacity and emits `NodeCapacityReserved`.
- `simulate_counterfactual`, `forecast_capacity`, `optimize_route_network`, and `clear_capacity_auction` provide advanced optimization evidence.
- `recommend_exception_resolution`, `screen_policy`, `detect_routing_anomaly`, `model_stochastic_exposure`, and `register_governed_model` provide hardened operational evidence.

## API Contract

`build_api_contract()` exposes descriptor-level API evidence:

- `POST /route-orders` maps to `route_orders`.
- `GET /route-candidates` maps to `build_workbench_view`.
- `POST /capacity` maps to `ingest_capacity_snapshot`.
- `POST /route-candidates` maps to `upsert_route_candidate`.
- `POST /order-routing/events/inbox` maps to `handle_event`.
- `GET /routing-workbench` maps to `build_workbench_view`.
- `POST /routing-simulations` maps to `simulate_counterfactual`.
- `POST /routing-optimizations` maps to `optimize_route_network`.
- `POST /routing-policy-screening` maps to `screen_policy`.
- `GET /routing-federation` maps to `federate_routing_view`.
- `POST /routing-proof` maps to `generate_routing_proof`.

Every route descriptor includes owned tables, command or query binding, emitted or consumed event metadata where applicable, required permission, and declared dependency evidence.

## Events And Handlers

Emitted events:

- `FulfillmentRouteSelected`
- `NodeCapacityReserved`

Consumed events:

- `OrderVerified`
- `AvailabilityProjected`
- `TaxCalculated`

Handler expectations:

- AppGen-X event topic is fixed to `appgen.order-routing.events`.
- Duplicate processed events do not append duplicate inbox or projection records.
- Retry evidence is recorded until `retry_limit` is reached.
- Exhausted failures create dead-letter evidence in the package-owned dead-letter table contract.

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

Parameters:

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

Configuration:

- `database_backend`
- `event_topic`
- `retry_limit`
- `default_currency`
- `supported_regions`
- `supported_split_policies`
- `supported_substitution_modes`
- `topology_systems`
- `default_timezone`
- `workbench_limit`

Configuration evidence also records `event_contract: AppGen-X`, locked event-contract visibility, hidden stream-engine picker evidence, emitted and consumed event types, and owned-table binding evidence.

## Permissions

`permissions_contract()` exposes action-level RBAC evidence with package-local permissions:

- `order_routing_optimization.read`
- `order_routing_optimization.route`
- `order_routing_optimization.capacity`
- `order_routing_optimization.configure`
- `order_routing_optimization.audit`
- `order_routing_optimization.event`

Action bindings cover standard order-routing operations plus advanced contract builders:

- `route_orders`, `reserve_node_capacity`, `optimize_route_network`, `clear_capacity_auction`, and `schedule_carbon_aware_route`.
- `ingest_capacity_snapshot` and `upsert_route_candidate`.
- `handle_event`.
- `configure_runtime`, `set_parameter`, `register_rule`, and `register_schema_extension`.
- `simulate_counterfactual`, `recommend_exception_resolution`, `score_fulfillment_risk`, `generate_routing_proof`, `screen_policy`, `run_control_tests`, `run_resilience_drill`, `rotate_crypto_epoch`, `detect_routing_anomaly`, `model_stochastic_exposure`, `register_governed_model`, `build_workbench_view`, `build_schema_contract`, `build_service_contract`, and `build_release_evidence`.

## UI And Workbench

UI fragments include:

- `OrderRoutingWorkbench`
- `RoutingNodeTopologyMap`
- `RoutingRuleStudio`
- `RouteCandidateGrid`
- `CapacitySnapshotBoard`
- `RoutingDecisionLedger`
- `RoutingPromiseBoard`
- `SplitShipmentStudio`
- `ReservationConsole`
- `CounterfactualSimulationLab`
- `RoutingOptimizationWorkbench`
- `RoutingExceptionConsole`
- `RoutingApprovalQueue`
- `RoutingFeedbackLedger`
- `RoutingInboxMonitor`
- `RoutingParameterConsole`
- `RoutingConfigurationPanel`
- `RoutingPolicyScreeningPanel`
- `RoutingAuditTrailView`

Workbench evidence includes:

- Counts for plans, nodes, constraints, costs, promises, split shipments, inventory/transport/service inputs, candidates, capacity snapshots, decisions, reservations, simulations, optimization runs, exceptions, approvals, feedback, inbox entries, outbox entries, and dead-letter entries.
- Configuration binding evidence with AppGen-X lock metadata.
- Rule and parameter binding evidence.
- Event surface evidence for emitted/consumed event types and fixed topic.
- Owned-table, outbox-table, inbox-table, and dead-letter-table evidence.

## Release Evidence

`build_release_evidence()` combines:

- `build_schema_contract()`
- `build_service_contract()`
- `build_api_contract()`
- `permissions_contract()`
- Runtime smoke state
- Workbench binding evidence
- UI contract evidence

Release checks prove:

- Owned schema depth and migration-per-owned-table coverage.
- Service command depth for standard and advanced routing capabilities.
- Fixed AppGen-X event contract and hidden stream-engine picker evidence.
- Permission coverage for core routing and contract-builder operations.
- Owned-only datastore boundaries.
- Idempotent inbox/outbox/dead-letter evidence through package-owned table bindings.

## Focused Validation

The focused package test covers:

- Runtime smoke against every declared advanced capability key.
- `implementation_contract()` exposure of schema, service, release, API, permissions, UI, event topic, emitted events, and consumed events.
- Positive schema/service/release evidence with expanded owned tables and generated migration/model descriptors.
- Configuration, parameters, rules, schema extensions, event handling, capacity, candidates, routing decisions, promises, approvals, feedback, workbench binding evidence, and UI rendering.
- Invalid backends, unsupported configuration fields, unsupported parameters, out-of-range parameters, non-owned schema extensions, duplicate event handling, retries, and dead letters.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `order_routing_optimization`
- Mesh: `commerce`
- Datastore backend: `None`

### Owned Tables

- `routing_rule`
- `route_candidate`
- `capacity_snapshot`
- `routing_decision`

### API Routes

- `POST /route-orders`
- `GET /route-candidates`
- `POST /capacity`

### Emitted Events

- `FulfillmentRouteSelected`
- `NodeCapacityReserved`

### Consumed Events

- `OrderVerified`
- `AvailabilityProjected`
- `TaxCalculated`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `order_routing_optimization` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `order_routing_optimization_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Distributed Order Routing and Optimization` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `order_routing_optimization_routing_rule`, `order_routing_optimization_route_candidate`, `order_routing_optimization_capacity_snapshot`, `order_routing_optimization_routing_decision`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `FulfillmentRouteSelected`, `NodeCapacityReserved`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `order_routing_optimization`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `order_routing_optimization_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

