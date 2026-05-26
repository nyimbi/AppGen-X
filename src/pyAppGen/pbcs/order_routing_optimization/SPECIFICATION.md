# Order Routing Optimization Specification

Package-local runtime slice for `order_routing_optimization`.

## Scope

Distributed order routing and optimization for enterprise order flow, including:

- Routing rules, route candidates, capacity snapshots, routing decisions, and node reservations.
- Cost, SLA, capacity, risk, and carbon-aware scoring.
- Split-shipment policy, substitution eligibility, tenant isolation, and workbench visibility.
- AppGen-X inbox/outbox eventing with idempotent handlers plus retry and dead-letter evidence.
- Fixed permissions, bounded configuration and parameter surfaces, deterministic rule compilation evidence, and focused runtime/UI tests.

## Catalog Contract

- Tables: `routing_rule`, `route_candidate`, `capacity_snapshot`, `routing_decision`
- APIs: `POST /route-orders`, `GET /route-candidates`, `POST /capacity`
- Emits: `FulfillmentRouteSelected`, `NodeCapacityReserved`
- Consumes: `OrderVerified`, `AvailabilityProjected`, `TaxCalculated`

## Runtime Invariants

- Database backends are restricted to PostgreSQL, MySQL, and MariaDB.
- `event_topic` is required and treated as an AppGen-X contract binding.
- Stream-engine selection is not user visible and the event contract is not user selectable.
- Only the declared configuration fields and parameter keys are accepted.
- Rules must provide all required fields and always compile to deterministic hash evidence.
- Workbench and UI render output must expose configuration, rule, and parameter binding evidence.

## Supported Configuration

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

## Supported Parameters

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

## Required Rule Fields

- `rule_id`
- `tenant`
- `rule_type`
- `regions`
- `eligible_nodes`
- `capacity_floor`
- `split_policy`
- `substitution_mode`
- `status`

## Advanced Runtime Coverage

The runtime smoke path covers:

- Event-sourced routing lifecycle and immutable audit trail
- Graph-relational fulfillment topology
- Probabilistic SLA/cost/capacity scoring
- Counterfactual routing simulation
- Temporal capacity forecasting
- Autonomous exception resolution
- Semantic request parsing
- Predictive fulfillment risk
- Self-healing route selection
- Cryptographic routing proof and crypto agility
- Dynamic policy screening and automated control testing
- Cross-system order/inventory/tax federation
- Chaos tolerance and distributed systems evidence
- Carbon-aware routing and mathematical optimization
- Allocation and auction-style capacity clearing
- Routing anomaly detection and stochastic exposure modeling
- Governed ML model evidence

## Workbench Surface

The workbench exposes:

- Route candidate, capacity, decision, split, reservation, inbox, outbox, and dead-letter counts
- Configuration binding evidence with fixed AppGen-X event contract metadata
- Rule compilation evidence with deterministic hashes
- Parameter binding evidence with supported vs active keys
