# MRP Engine PBC Specification

## Purpose

`mrp_engine` is the package-local Material Requirements Planning capability for AppGen-X manufacturing applications. It owns the planning graph that turns demand, supply projections, bill-of-material structure, site policy, capacity signals, lead times, lot sizing, safety stock, scrap, yield, and release rules into executable planned production orders and planned purchase suggestions. The package must work as a composable PBC: it has its own schema boundary, runtime services, API descriptors, event contracts, handlers, UI fragments, configuration model, rules, parameters, tests, and release evidence.

The PBC does not own inventory balances, customer orders, supplier masters, production execution, quality inspection, or audit ledgers. It composes with those domains only through AppGen-X APIs, AppGen-X events, and package-owned projections. Cross-PBC dependency data is copied into MRP-owned projection tables or in-memory runtime projections; no shared table access is part of the contract.

## Package Boundary

- PBC key: `mrp_engine`
- Mesh assignment: `opsmfg`
- Implementation directory: `src/pyAppGen/pbcs/mrp_engine`
- Ordinary datastore backends: PostgreSQL, MySQL, or MariaDB only
- Required event contract: AppGen-X
- Fixed event topic: `appgen.mrp.events`
- User-facing stream-engine picker: forbidden
- Owned runtime event tables: `mrp_engine_appgen_outbox_event`, `mrp_engine_appgen_inbox_event`, `mrp_engine_dead_letter_event`

Owned tables are:

- `bill_of_material`
- `bom_revision`
- `bom_component`
- `bom_alternate`
- `bom_substitution_rule`
- `item_planning_profile`
- `item_source_rule`
- `material_demand`
- `demand_projection_line`
- `demand_forecast_snapshot`
- `sales_order_demand_projection`
- `safety_stock_policy`
- `inventory_projection`
- `inventory_lot_projection`
- `inventory_reservation_projection`
- `quality_hold_projection`
- `capacity_projection`
- `capacity_bucket`
- `work_center_capacity_projection`
- `supplier_lead_time_projection`
- `production_capacity_projection`
- `mrp_run`
- `mrp_run_item`
- `mrp_run_bucket`
- `mrp_scenario`
- `mrp_plan_version`
- `planned_order`
- `planned_order_component`
- `planned_purchase_suggestion`
- `planned_production_order`
- `planned_transfer_order`
- `material_shortage`
- `shortage_pegging`
- `supply_demand_pegging`
- `planning_exception`
- `exception_resolution_plan`
- `release_route`
- `planning_policy_screening`
- `planning_audit_trace`
- `supply_availability_proof`
- `mrp_federation_projection`
- `carbon_planning_window`
- `material_allocation_optimization`
- `capacity_allocation`
- `shortage_anomaly_signal`
- `material_risk_model`
- `shortage_forecast`
- `planning_parsed_instruction`
- `mrp_seed_data`
- `mrp_schema_extension`
- `mrp_control_assertion`
- `mrp_governed_model`
- `mrp_rule`
- `mrp_parameter`
- `mrp_configuration`
- `mrp_engine_appgen_outbox_event`
- `mrp_engine_appgen_inbox_event`
- `mrp_engine_dead_letter_event`

Allowed dependency projections are inventory release, verified order, forecast, production capacity, quality hold, and supplier lead-time projections. These are MRP-owned representations sourced from declared APIs or events, not foreign tables.

## Standard Table-Stakes Capabilities

The PBC must cover the baseline functionality expected from a production MRP engine:

1. Bill-of-material master capture for parent item, component item, component quantity, revision, site, status, and scrap percent.
2. BOM revision eligibility and release-state checking through rule policy.
3. BOM explosion from finished goods into required component quantities.
4. Demand projection ingestion from verified orders and forecasts.
5. Inventory projection ingestion from released inventory availability signals.
6. Supply and demand netting by tenant, site, item, quantity, and planning run.
7. Safety stock multiplier, lot-size minimum, lead-time days, capacity threshold, and shortage-severity parameters.
8. MRP run creation by tenant, site, horizon, scenario, and planner.
9. Shortage detection with total shortage, per-item shortage, pegged demand, and severity scoring.
10. Planned purchase suggestion generation for externally procured components.
11. Planned production order generation for internally made or assembled components.
12. Release of planned orders into downstream procurement or production routes.
13. Pegging from planned order back to demand and BOM requirement.
14. Exception recommendations for shortage, capacity, and quality-hold cases.
15. Scenario simulation for counterfactual demand and planning-policy changes.
16. Multi-tenant and multi-site isolation in runtime views and commands.
17. Idempotent event handlers with inbox records and handled-event keys.
18. Retry evidence and dead-letter evidence for failed or unsupported events.
19. RBAC descriptors for master data, planning, release, event handling, configuration, and audit actions.
20. Configuration schema and validation for backend, event topic, retry limit, sites, routes, buckets, and workbench limits.
21. Rule engine for planning, shortage, substitution, release, capacity, and exception policies.
22. Parameter engine for numeric planning controls.
23. Schema-extension registration limited to MRP-owned tables.
24. Seed-ready descriptors for buckets, exception codes, release routes, lot-size policies, and lead-time classes.
25. Workbench UI fragments for BOMs, demand, MRP runs, shortages, planned orders, rules, parameters, and configuration.
26. API route descriptors for each command and query with owned-table, event, idempotency, and permission metadata.

## Advanced Capability Contract

The runtime must provide deterministic evidence for the advanced MRP feature set:

- Event-sourced planning lifecycle with immutable planning event hashes.
- Graph-relational BOM topology suitable for traversal and future multi-level expansion.
- Multi-tenant and multi-site planning isolation.
- Schema-on-read extension points for owned planning tables.
- Probabilistic shortage, quality, and capacity risk scoring.
- Real-time workbench analytics over current runtime state.
- Counterfactual planning-policy simulation.
- Temporal demand, shortage, and inventory exposure forecasting.
- Autonomous exception-resolution recommendations.
- Semantic parsing of planning instructions.
- Predictive material, capacity, and compliance-risk screening.
- Self-healing route selection for procurement, production, and outbox fallback paths.
- Zero-disclosure supply availability proof generation from permitted public claims.
- Immutable control trail validation through event hash-chain checks.
- Dynamic policy screening for restricted sites and blocked runs.
- Automated control tests for configuration, rules, parameters, planned-order correctness, and event integrity.
- Universal AppGen-X API and event descriptors.
- Cross-system plan federation through declared APIs and projections.
- Decentralized item and source identity verification.
- Chaos-style resilience drills for projection delay and downstream API timeout scenarios.
- Crypto-agility evidence for planning authorization epochs.
- Carbon-aware planning batch scheduling.
- Algebraic material allocation optimization.
- Mechanism-design capacity allocation.
- Information-theoretic shortage anomaly detection.
- Stochastic material exposure modeling.
- Governed planning model registration with feature lineage, drift threshold, and explainability requirements.

## Runtime Configuration

`mrp_engine_configure_runtime` is the installation gate. It must reject any database backend outside PostgreSQL, MySQL, and MariaDB. It must reject any event topic other than `appgen.mrp.events`. It must reject user-facing eventing or stream-engine fields such as `stream_engine`, `stream_engine_picker`, `eventing_mode`, `event_transport`, or `user_eventing_choice`. A successful configuration writes:

- `event_contract: AppGen-X`
- `allowed_database_backends`
- `stream_engine_picker_visible: False`
- `user_selectable_event_contract: False`
- `owned_tables`

This makes ordinary eventing non-negotiable and prevents generated apps from exposing implementation choices that would break the AppGen-X event contract.

## Rules And Parameters

Rules are registered with `rule_id`, tenant, status, and either `scope` or `rule_type`. The runtime compiles a deterministic hash over each rule, marks active rules as enabled, and uses rule attributes to decide BOM eligibility, demand-source eligibility, allowed sites, release routes, substitutions, and exception behavior.

Parameters are limited to known planning controls: planning horizon, bucket size, safety-stock multiplier, lot-size minimum, lead-time days, capacity threshold, shortage-severity threshold, scrap factor, planner approval threshold, and workbench limit. Unknown parameters are rejected so configuration cannot smuggle unsupported behavior into the runtime.

## Event Contract And Handlers

Emitted events:

- `BomRegistered`
- `DemandProjectionIngested`
- `InventoryProjectionIngested`
- `MrpRunStarted`
- `MaterialShortageDetected`
- `PlannedOrderReleased`

Consumed events:

- `InventoryReleased`
- `OrderVerified`
- `ForecastUpdated`
- `ProductionCapacityChanged`
- `QualityHoldReleased`
- `SupplierLeadTimeUpdated`

`mrp_engine_receive_event` is idempotent. It builds a deterministic idempotency key from the incoming event when one is not provided. Processed events are stored in `handled_events`; duplicate processed deliveries return without adding inbox records or changing projections. Supported events are projected into package-owned projection stores. Unsupported events and simulated failures create retry evidence until the configured retry limit is reached, then append dead-letter records with failure reason `unsupported_or_failed_mrp_event`.

## API And Permission Contract

`mrp_engine_build_api_contract` returns descriptor routes, not unstructured route strings. Each descriptor identifies the route, command or query, owned tables touched, emitted or consumed event types, required permission, and idempotency key. The contract explicitly states:

- `shared_table_access: False`
- `event_contract: AppGen-X`
- `stream_engine_picker_visible: False`
- `database_backends: ("postgresql", "mysql", "mariadb")`
- owned tables and event contracts from package constants

`mrp_engine_permissions_contract` defines read, master, plan, release, event, configure, and audit permissions. Every command exposed by the API contract and workbench has a corresponding action-permission mapping.

## Generated Schema, Services, And Release Evidence

`mrp_engine_build_schema_contract` produces executable generation descriptors for every owned table. The descriptor includes table fields, primary keys, parent-child relationships, package-local model paths, and migration paths in `pbcs/mrp_engine/migrations/{sequence}_{table}.sql`. The schema contract rejects shared-table access and limits MRP schema names to the package-owned prefixes used by the runtime.

`mrp_engine_build_service_contract` exposes command methods for configuration, rules, parameters, schema extension, inbox handling, BOM registration, demand and inventory projection ingestion, MRP runs, BOM explosion, material plan calculation, planned-order release, supply routing, proofs, screening, federation, identity checks, resilience drills, crypto epoch rotation, carbon-aware batching, allocation optimization, control tests, governed models, and boundary verification. Query methods cover workbench views, simulations, forecasts, parsing, risk scoring, exception recommendations, anomaly detection, stochastic exposure modeling, and descriptor builders.

`mrp_engine_build_release_evidence` is the package-local release gate. It proves schema depth, one migration descriptor per owned table, service command depth, AppGen-X-only API/eventing, permission coverage for core commands, backend allowlist compliance, and no shared table access.

## UI And Workbench Contract

`ui.py` exposes package-local fragments:

- `MrpEngineWorkbench`
- `BomGraphExplorer`
- `DemandConsole`
- `MrpRunControl`
- `ShortageBoard`
- `PlannedOrderBoard`
- `MrpRuleStudio`
- `MrpParameterConsole`
- `MrpConfigurationPanel`

The UI contract binds fragments to owned tables, projections, and AppGen-X event surfaces. It exposes outbox, inbox, and dead-letter status as visible operational evidence. The configuration editor exposes the fixed AppGen-X topic and allowed backend list while keeping the stream-engine picker hidden. `mrp_engine_render_workbench` filters visible actions by RBAC permissions and reports owned-table, configuration, outbox, inbox, and dead-letter binding evidence.

## Boundary Verification

`mrp_engine_verify_owned_table_boundary` proves that a generated or composed MRP package references only MRP-owned tables, MRP runtime event tables, declared AppGen-X consumed events, declared dependency APIs, declared dependency projections, or `mrp_engine_`-prefixed package-local artifacts. It reports violations for foreign operational tables such as inventory balances or customer profile data.

## Release Evidence

The package is complete only when:

- Runtime, UI, exports, specification, and focused tests live in the package directory or focused test file.
- `mrp_engine_runtime_smoke()` passes every standard and advanced capability check.
- `pbc_implementation_contract("mrp_engine")` exposes source package, runtime, UI, API, permissions, owned tables, and allowed database backends.
- `pbc_implementation_release_audit(("mrp_engine",))` passes.
- `pbc_implemented_capability_audit(("mrp_engine",))` passes.
- Focused tests prove domain workflows, rules, parameters, configuration, UI binding, schema ownership, AppGen-X event handling, retry/dead-letter behavior, API/RBAC descriptors, and owned-table boundary enforcement.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `mrp_engine`
- Mesh: `opsmfg`
- Datastore backend: `None`

### Owned Tables

- `bill_of_material`
- `bom_revision`
- `bom_component`
- `item_planning_profile`
- `material_demand`
- `inventory_projection`
- `capacity_projection`
- `mrp_run`
- `mrp_run_item`
- `planned_order`
- `planned_purchase_suggestion`
- `planned_production_order`
- `material_shortage`
- `shortage_pegging`
- `planning_exception`
- `mrp_rule`
- `mrp_parameter`
- `mrp_configuration`

### API Routes

- `POST /mrp/boms`
- `POST /mrp/demand-projections`
- `POST /mrp/inventory-projections`
- `POST /mrp/runs`
- `POST /mrp/runs/{id}/calculate`
- `POST /mrp/planned-orders/{id}/release`
- `POST /mrp/events/inbox`
- `GET /mrp/workbench`

### Emitted Events

- `BomRegistered`
- `DemandProjectionIngested`
- `InventoryProjectionIngested`
- `MrpRunStarted`
- `MaterialShortageDetected`
- `PlannedOrderReleased`

### Consumed Events

- `InventoryReleased`
- `OrderVerified`
- `ForecastUpdated`
- `ProductionCapacityChanged`
- `QualityHoldReleased`
- `SupplierLeadTimeUpdated`

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
