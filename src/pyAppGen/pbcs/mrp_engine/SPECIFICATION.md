# MRP Engine PBC Specification

## Purpose

`mrp_engine` owns material requirements planning for manufacturing: bill-of-material graph analysis, material demand, supply netting, capacity-aware planned orders, shortages, and release-ready procurement/production suggestions. It composes with inventory, order management, forecasting, procurement, production control, quality, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `mrp_engine`
- Mesh: `opsmfg`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `bill_of_material`, `material_demand`, `mrp_run`, `planned_order`
- Owned event tables: `mrp_engine_outbox`, `mrp_engine_inbox`, `mrp_engine_dead_letter`
- Consumed events: `InventoryReleased`, `OrderVerified`, `ForecastUpdated`
- Emitted events: `MaterialShortageDetected`, `PlannedOrderReleased`
- External access rule: no shared inventory, order, forecast, procurement, or production tables; use projections, APIs, and events only.

## Standard Table-Stakes Capabilities

1. Bill-of-material master capture with parent item, component item, quantity, scrap, effective dates, and revision status.
2. Multi-level BOM explosion and component dependency graph traversal.
3. Demand projection ingestion from verified orders and forecasts.
4. Inventory availability projection ingestion from inventory events.
5. Supply and demand netting by item, site, date, and planning bucket.
6. Safety stock, lot size, lead time, yield, scrap, and rounding parameter handling.
7. MRP run creation by tenant, site, horizon, bucket, planner, and scenario.
8. Shortage detection and root-cause evidence.
9. Planned production order generation.
10. Planned purchase suggestion generation.
11. Capacity-aware release readiness.
12. Pegging from demand to planned order and component shortages.
13. Exception messages for expedite, defer, cancel, reschedule, and substitute.
14. Scenario simulation and what-if planning.
15. Multi-tenant and multi-site isolation.
16. AppGen-X outbox/inbox idempotency.
17. Retry and dead-letter evidence.
18. RBAC descriptors for planner, production planner, procurement planner, auditor, and admin actions.
19. Configuration schema for runtime installation.
20. Rule engine for planning policy, item eligibility, shortage severity, substitution, release, and exception policies.
21. Parameter engine for horizon, bucket size, safety stock, lot size, lead time, and capacity thresholds.
22. Seed data for planning buckets, exception codes, lot-size policies, lead-time classes, and release statuses.
23. Package metadata, source registration, and release evidence.
24. Package-local workbench UI for BOMs, demand, MRP runs, planned orders, shortages, rules, parameters, and configuration.

## Advanced Capability Requirements

The runtime must prove deterministic evidence for:

- Event-sourced planning lifecycle and immutable audit trail.
- Graph-relational BOM topology and multi-level dependency traversal.
- Multi-tenant and multi-site planning isolation.
- Schema evolution for planning attributes.
- Probabilistic shortage, supplier, and capacity risk scoring.
- Real-time planning analytics and counterfactual planning-policy simulation.
- Demand, shortage, and inventory exposure forecasting.
- Autonomous planning exception recommendations.
- Semantic demand and BOM instruction parsing.
- Self-healing inventory/procurement/production route selection.
- Zero-knowledge supply availability proofs.
- Dynamic planning policy screening and automated controls.
- Universal API/event contracts and cross-system MRP federation.
- Inventory, order, forecast, procurement, and production integration through projections.
- Decentralized item/source identity verification.
- Resilience drills, crypto agility, and carbon-aware planning batch scheduling.
- Algebraic material allocation optimization and mechanism-design capacity allocation.
- Information-theoretic shortage anomaly detection.
- Stochastic material exposure modeling.
- Governed planning model registration with lineage, drift, and explainability controls.

## Rules, Parameters, And Configuration

The PBC must understand and execute:

- Configuration: database backend, event topic, retry limit, allowed sites, allowed order types, allowed procurement routes, allowed production routes, default planning bucket, and workbench limit.
- Parameters: planning horizon days, bucket size days, safety stock multiplier, lot size minimum, lead time days, capacity threshold, shortage severity threshold, and scrap factor.
- Rules: planning item eligibility, BOM revision eligibility, demand-source eligibility, shortage severity, substitution, release, and planner approval policies.

Rules are compiled into deterministic hashes, parameters are stored in owned runtime state, backend configuration rejects anything outside PostgreSQL, MySQL, or MariaDB, eventing remains bound to the AppGen-X event contract without user-facing stream-engine selection, and configuration gates BOM, demand, MRP run, planned order, and release operations.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- MRP workbench.
- BOM graph explorer.
- Demand console.
- MRP run control.
- Shortage board.
- Planned order board.
- Rule studio.
- Parameter console.
- Runtime configuration panel.

UI actions are RBAC-gated and bind only to owned tables, projections, and AppGen-X event surfaces.

## Release Evidence

Completion requires:

- Package-local specification, runtime, UI, and tests.
- `pbc_implementation_contract("mrp_engine")` returns an ok source package and advanced runtime.
- `pbc_implementation_release_audit(("mrp_engine",))` passes.
- `pbc_implemented_capability_audit(("mrp_engine",))` passes.
- Full 46-PBC generation smoke remains green.
