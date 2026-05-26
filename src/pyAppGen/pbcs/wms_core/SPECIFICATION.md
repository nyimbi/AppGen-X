# Warehouse Management Core PBC Specification

`wms_core` is the AppGen-X packaged business capability for warehouse execution:
receiving, putaway, replenishment, picking, packing, staging, shipping,
cross-docking, cycle count, and edge-workflow orchestration. The package owns
its implementation under `src/pyAppGen/pbcs/wms_core/`.

## Owned Boundary

- **PBC key:** `wms_core`
- **Mesh:** `scl`
- **Owned tables:** `warehouse`, `bin_location`, `pick_wave`, `pack_task`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Emits:** `Picked`, `Packed`, `GoodsReceiptPosted`, `OrderShipped`
- **Consumes:** `InventoryAllocated`, `InboundArrived`
- **Primary APIs:** `POST /putaway`, `POST /pick-waves`, `POST /pack-tasks`
- **UI artifacts:** warehouse execution workbench, dock door board, putaway
  queue, wave monitor, pack station view, exception queue, rule editor

The package owns warehouse execution state. Inventory ownership remains in
`inventory_positioning`; WMS references inventory through allocation and receipt
events only.

## Rules, Parameters, and Configuration

The runtime must understand and apply executable warehouse rules, parameters,
and configuration:

- **Rules:** putaway zone selection, bin capacity, hazardous/temperature
  compatibility, pick method, wave grouping, replenishment trigger, pack
  material selection, carrier staging, cross-dock eligibility, labor priority,
  and exception escalation.
- **Parameters:** bin capacity tolerance, pick-wave size, pick path weighting,
  partial pick threshold, pack weight limit, replenishment minimum, dock dwell
  target, labor productivity target, scan tolerance, and anomaly threshold.
- **Configuration:** datastore backend, event topic, retry limit, default
  warehouse timezone, allowed bin statuses, pack station limits, label format,
  edge-device mode, and workbench limits.

The PBC exposes operations to configure runtime behavior, set parameters,
register rules, and apply them during putaway, wave planning, picking, packing,
and shipping.

## Standard Table-Stakes Capabilities

1. Warehouse master data with zones, dock doors, pack stations, calendars, and
   edge-device modes.
2. Bin/location master data with capacity, status, zone, temperature, hazard,
   and pick-path coordinates.
3. Inbound receipt and dock-door registration from `InboundArrived` events.
4. Putaway task creation and confirmation using bin-eligibility rules.
5. Replenishment task recommendation from minimum stock and forward-pick
   thresholds.
6. Inventory allocation consumption from `InventoryAllocated` events without
   shared stock tables.
7. Pick wave planning with grouping, path sequencing, labor assignment, and
   partial-pick handling.
8. Pick task execution with scan validation, substitutions, short picks, and
   exception capture.
9. Pack task creation with cartonization, material selection, weight checks, and
   label evidence.
10. Staging and ship confirmation with carrier route, dock door, and order
    shipment event evidence.
11. Cross-dock flow from inbound to outbound staging.
12. Cycle count and location audit workflows.
13. Warehouse exception management for damaged goods, missing stock, blocked
    bins, short picks, and failed labels.
14. Labor task prioritization and productivity metrics.
15. Edge-device command replay for scanners, printers, scales, conveyors, and
    sortation events.
16. Multi-tenant and multi-warehouse isolation.
17. Retry, dead-letter, and idempotency evidence for consumed allocation and
    inbound events.
18. Permissions and ABAC descriptors for receive, putaway, pick, pack, ship,
    count, configure, and audit operations.
19. Configuration schema and seed data for warehouse types, bin statuses, pick
    methods, pack materials, and default parameters.
20. Workbench views for dock backlog, putaway tasks, waves, pack tasks, ship
    queue, exceptions, and labor load.
21. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## Advanced Capabilities

1. Event-sourced warehouse execution lifecycle.
2. Graph-relational warehouse topology across warehouse, zone, bin, dock,
   station, task, wave, order, and operator nodes.
3. Multi-tenant warehouse isolation.
4. Schema-on-read warehouse extensibility for bin, task, device, and carton
   attributes.
5. Probabilistic putaway and pick completion estimates.
6. Real-time warehouse execution and operational analytics convergence.
7. Counterfactual wave and labor simulation.
8. Temporal throughput and dock-dwell forecasting.
9. Autonomous pick/pack exception resolution recommendations.
10. Semantic warehouse document and scan parsing.
11. Predictive congestion, damage, and short-pick risk.
12. Self-healing edge route selection for scanners, printers, and conveyors.
13. Zero-knowledge shipment proof.
14. Immutable warehouse traceability trail.
15. Dynamic policy screening for restricted bins, hazard conflicts, temperature
    violations, and blocked carriers.
16. Automated warehouse control testing.
17. Universal API and async event contracts.
18. Cross-system warehouse federation with inventory, transportation, quality,
    and order packages.
19. Edge-device network integration evidence.
20. Decentralized warehouse and operator identity verification.
21. Chaos-engineered edge and dock tolerance.
22. Crypto-agile warehouse authorization.
23. Carbon-aware wave and carrier staging.
24. Algebraic pick-path and wave optimization.
25. Mechanism-design labor/task allocation.
26. Information-theoretic warehouse anomaly detection.
27. Stochastic throughput exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML warehouse risk governance.
30. Cryptographic engineering for proofs and trace hash chains.
31. Mathematical optimization for pick waves, pack flow, and staging.
32. Warehouse MLOps governance with feature lineage, drift, and explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration are executable
and influence task decisions, that runtime configuration rejects unsupported
backends while exposing only the AppGen-X event contract, that package-local UI
fragments cover master data, inbound, putaway, picking, packing, shipping,
exceptions, labor, edge-device replay, rules, parameters, and configuration,
that WMS-owned state stays inside the package boundary, that AppGen-X outbox
events are idempotent, and that every standard and advanced capability has
testable release evidence.
