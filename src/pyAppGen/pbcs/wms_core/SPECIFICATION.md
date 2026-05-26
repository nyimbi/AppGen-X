# Warehouse Management Core PBC Specification

`wms_core` is the AppGen-X packaged business capability for warehouse execution:
receiving, putaway, replenishment, picking, packing, staging, shipping,
cross-docking, cycle count, and edge-workflow orchestration. The package owns
its implementation under `src/pyAppGen/pbcs/wms_core/`.

## Owned Boundary

- **PBC key:** `wms_core`
- **Mesh:** `scl`
- **Owned tables:** `warehouse`, `bin_location`, `inbound_receipt`,
  `dock_door`, `putaway_task`, `replenishment_task`, `pick_wave`,
  `pick_task`, `pack_task`, `carton`, `label_evidence`, `staging_lane`,
  `shipment_confirmation`, `cross_dock_flow`, `cycle_count`,
  `warehouse_exception`, `labor_task`, `edge_device_command`, `wms_rule`,
  `wms_parameter`, and `wms_configuration`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only, fixed to
  `appgen.wms.events`
- **Emits:** `WarehouseRegistered`, `BinRegistered`, `GoodsReceiptPosted`,
  `PutawayTaskCreated`, `PutawayConfirmed`, `PickWaveReleased`, `Picked`,
  `PackTaskCreated`, `Packed`, and `OrderShipped`
- **Consumes:** `InventoryAllocated`, `InboundArrived`,
  `QualityHoldReleased`, `CarrierBooked`, and `AccessPolicyChanged`
- **Primary APIs:** `POST /wms/warehouses`, `POST /wms/bins`,
  `POST /wms/inbound`, `POST /wms/putaway`, `POST /wms/pick-waves`,
  `POST /wms/picks/{id}/execute`, `POST /wms/pack-tasks`,
  `POST /wms/shipments`, `POST /wms/events/inbox`, and
  `GET /wms/workbench`
- **UI artifacts:** warehouse execution workbench, dock door board, putaway
  queue, wave monitor, pack station view, exception queue, rule editor

The package owns warehouse execution state. Inventory ownership remains in
`inventory_positioning`; WMS references inventory through allocation and receipt
events only. Carrier status, quality release, and access policy state are
represented as projections from declared events or APIs, never through shared
tables. Package-level boundary verification must accept owned tables,
AppGen-X runtime event tables, declared consumed events, and named projections;
it must reject references such as `inventory_balance` or customer/account tables
unless those references are represented by a declared API or event projection.

## Package Metadata and Registration

The package exports a stable `PBC_KEY`, implementation contract, capability
catalog, API descriptor, permission descriptor, UI contract, owned table list,
database backend allowlist, emitted event list, and consumed event list from
the package directory. Package discovery can load `pyAppGen.pbcs.wms_core`
without causing side effects. The implementation contract is a read-only
registration plan: it describes the source package, runtime capability proof,
UI fragments, API descriptors, RBAC descriptors, owned tables, and datastore
constraints without mutating application state.

Generated applications must include WMS-owned schema, migrations, models,
services, routes, event contracts, handlers, and workbench fragments derived
from this package. The package does not offer a stream-engine picker or a
user-selectable eventing mode; the only user-visible eventing contract is the
AppGen-X outbox/inbox contract with retry and dead-letter evidence.

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

Runtime configuration must reject unsupported database backends, any topic other
than `appgen.wms.events`, and fields that attempt to expose a user stream-engine
or eventing picker. Configuration evidence stored in state must include
`event_contract: AppGen-X`, the backend allowlist, `stream_engine_picker_visible:
false`, `user_selectable_event_contract: false`, and the owned table list.

Schema extensions are allowed only on WMS-owned tables. Extensions are
schema-on-read metadata used by generated migrations and models; they must use
lowercase snake-case field names and merge with any existing extension metadata
for the same table. Attempts to extend inventory, transportation, quality,
identity, customer, finance, or other external tables are package-boundary
violations.

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

## Event Handling and Reliability

`wms_core` maintains an AppGen-X outbox for domain events it emits and an inbox
for declared events it consumes. Consumed events are handled idempotently through
an idempotency key derived from the incoming event type and event identifier
unless a caller supplies an explicit idempotency key. Duplicate processed events
return the original handler evidence and do not append another inbox entry.

Supported consumed events are projected into package-owned read models:

- `InventoryAllocated` becomes an inventory-allocation projection used by wave
  release and picking decisions.
- `InboundArrived` becomes an inbound-arrival projection used by receiving and
  dock-door visibility.
- `QualityHoldReleased` becomes a quality-hold projection used by putaway and
  pick eligibility.
- `CarrierBooked` becomes a carrier-booking projection used by staging and ship
  confirmation.
- `AccessPolicyChanged` becomes an access-policy projection used by dynamic
  policy screening and workbench authorization evidence.

Unsupported or failed consumed events create retry evidence until the configured
retry limit is reached; then they move to the WMS dead-letter surface with a
reason and immutable handler evidence. Generated applications must expose
outbox, inbox, retry, and dead-letter state through package-local models and
workbench fragments.

## API, RBAC, and Workbench Binding

Every API descriptor declares its route, command or query, owned tables touched,
emitted or consumed events, required permission, and idempotency key basis. The
API contract declares `shared_table_access: false`, the AppGen-X event contract,
allowed database backends, owned tables, and generated configuration variables.

The permission contract includes read, master-data, receiving, putaway, picking,
packing, shipping, cycle-count, edge-device, event, configure, and audit
permissions. Each command and query maps to exactly one permission so generated
apps can enforce RBAC and ABAC rules consistently across service methods, API
routes, event handlers, and UI actions.

The UI contract binds fragments to WMS-owned tables and runtime surfaces:
warehouse master, bins, receipts, putaway tasks, pick waves, picks, pack tasks,
shipments, rules, parameters, configuration, AppGen-X outbox, inbox, and
dead-letter tables. The workbench render contract reports visible and locked
actions from RBAC, counts outbox/inbox/dead-letter records, and includes binding
evidence proving that configuration and events use the package-local AppGen-X
contract.

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
