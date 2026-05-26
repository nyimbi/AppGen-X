# Inventory Positioning PBC Specification

## Purpose

`inventory_positioning` owns enterprise inventory truth: item masters,
attributes, substitutions, lots, serials, nodes, calendars, capacity,
positions, receipts, adjustments, reservations, allocations, releases, quality
holds, in-transit projections, traceability, backorders, replenishment,
reconciliation, policy screening, stock proofs, cross-node federation, carbon
fulfillment, competing channel allocation, anomaly signals, stock risk models,
rules, parameters, configuration, UI fragments, and release evidence.

The PBC integrates with order, warehouse, procurement, transportation, quality,
commerce, identity, schema, and audit capabilities only through declared APIs,
AppGen-X events, and read-only projections. It does not share stock tables with
other PBCs.

## Owned Datastore Boundary

The runtime owns these tables, with generated model and migration evidence for
each:

- `inventory_positioning_item`: item identity, SKU, UOM, tracking flags, and
  status.
- `inventory_positioning_item_attribute`: governed item attributes.
- `inventory_positioning_item_substitution`: substitute items and priority.
- `inventory_positioning_lot`: lot identity, expiry, status, and trace hash.
- `inventory_positioning_serial`: serial identity, lot, node, and status.
- `inventory_positioning_node`: warehouse, store, vendor, in-transit, virtual,
  and cross-dock node master.
- `inventory_positioning_node_calendar`: node working calendar and cutoffs.
- `inventory_positioning_node_capacity`: item/node capacity constraints.
- `inventory_positioning_node_identity`: decentralized node identity evidence.
- `inventory_positioning_inventory_position`: on-hand, reserved, quarantine,
  in-transit, and allocated quantities.
- `inventory_positioning_position_snapshot`: point-in-time position snapshot.
- `inventory_positioning_receipt`: receipt header.
- `inventory_positioning_receipt_line`: receipt line, item, lot, and quantity.
- `inventory_positioning_adjustment`: cycle count, shrink, damage, correction,
  or return adjustment.
- `inventory_positioning_cycle_count`: physical count and variance.
- `inventory_positioning_reservation`: order reservation and expiry.
- `inventory_positioning_allocation`: allocation header and state.
- `inventory_positioning_allocation_line`: node/lot allocation line.
- `inventory_positioning_allocation_expiry`: allocation TTL and release state.
- `inventory_positioning_quality_hold`: quarantine hold.
- `inventory_positioning_quality_release`: release evidence.
- `inventory_positioning_in_transit_projection`: expected in-transit stock.
- `inventory_positioning_traceability_event`: lot, serial, receipt, shipment,
  adjustment, and hold trace event.
- `inventory_positioning_backorder`: backorder demand.
- `inventory_positioning_replenishment_signal`: reorder signal.
- `inventory_positioning_replenishment_plan`: planned replenishment.
- `inventory_positioning_reconciliation`: ledger-to-physical reconciliation.
- `inventory_positioning_policy_screening`: node, lot, channel, and negative
  inventory screening.
- `inventory_positioning_stock_proof`: disclosure-minimized availability proof.
- `inventory_positioning_cross_node_federation`: external projection hash.
- `inventory_positioning_carbon_fulfillment`: carbon-aware node scheduling.
- `inventory_positioning_channel_allocation`: competing channel allocation.
- `inventory_positioning_anomaly_signal`: inventory anomaly evidence.
- `inventory_positioning_stock_risk_model`: stockout/spoilage risk model.
- `inventory_positioning_seed_data`: node type, status, UOM, and policy seeds.
- `inventory_positioning_schema_extension`: owned schema extension metadata.
- `inventory_positioning_control_assertion`: continuous control assertion.
- `inventory_positioning_governed_model`: regulated model governance.
- `inventory_positioning_rule`: executable inventory rule.
- `inventory_positioning_parameter`: bounded runtime parameter.
- `inventory_positioning_configuration`: database, AppGen-X topic, retry, and
  UOM configuration.
- `inventory_positioning_appgen_outbox_event`: emitted AppGen-X event.
- `inventory_positioning_appgen_inbox_event`: consumed AppGen-X event.
- `inventory_positioning_dead_letter_event`: exhausted retry evidence.

Supported ordinary backends are PostgreSQL, MySQL, and MariaDB.

## Standard Capabilities

The PBC implements item master, item attributes, substitutions, lots, serials,
node master, calendars, capacity, node identity, inventory positions, position
snapshots, goods receipts, receipt lines, inventory adjustments, cycle counts,
availability-to-promise, capable-to-promise inputs, reservations, allocation
creation, allocation lines, allocation release, reservation TTL, quality holds,
quality releases, in-transit projections, lot/serial traceability,
multi-node/multi-tenant isolation, substitution availability, backorders,
replenishment signals and plans, inventory reconciliation, AppGen-X outbox and
inbox, idempotent handlers, retry/dead-letter evidence, permissions,
configuration, rules, parameters, seed data, and workbench views.

## Advanced Capabilities

The runtime proves event-sourced inventory lifecycle, graph-relational item and
node topology, multi-tenant stock isolation, schema-on-read inventory
extensions, probabilistic availability projection, ATP/CTP convergence,
counterfactual allocation simulation, temporal stockout forecasting,
autonomous reconciliation, semantic inventory event parsing, stockout and
spoilage risk scoring, self-healing allocation routing, disclosure-minimized
stock proof, immutable traceability trail, dynamic policy screening,
continuous controls, universal API and AppGen-X events, cross-node federation,
warehouse/order/quality integration, decentralized node and lot identity,
resilience drills, crypto-agile authorization, carbon-aware fulfillment,
algebraic allocation optimization, mechanism-design channel allocation,
information-theoretic anomaly detection, stochastic stock exposure modeling,
partition-safe idempotency, probabilistic stock-risk governance,
cryptographic evidence, mathematical optimization, and inventory model
governance.

## Rules, Parameters, and Configuration

Configuration is validated by `inventory_positioning_configure_runtime`.
Required settings include `database_backend`, `event_topic`, `retry_limit`,
default UOM, precision, allowed statuses, reservation policy, and workbench
limits. The ordinary topic is fixed to `appgen.inventory.events`; user-facing
stream-engine selection is rejected.

Parameters are validated by `inventory_positioning_set_parameter`. Supported
parameters include `safety_stock_percent`, `partial_allocation_threshold`,
`reservation_ttl_minutes`, `reconciliation_tolerance_units`,
`stockout_risk_threshold`, and `workbench_limit`.

Rules are registered by `inventory_positioning_register_rule`. Rule scopes
include allocation priority, safety stock, ATP/CTP eligibility, lot
restrictions, expiration windows, quality release, substitutions, backorder,
node eligibility, channel protection, demand class prioritization, and
negative-inventory prevention.

Schema extensions are accepted only for Inventory-owned tables. Foreign table
extension attempts fail boundary validation.

## APIs

- `POST /inventory/items`
- `POST /inventory/nodes`
- `POST /inventory/receipts`
- `POST /inventory/adjustments`
- `GET /inventory/availability`
- `POST /inventory/allocations`
- `POST /inventory/allocations/{id}/release`
- `POST /inventory/quality-holds`
- `POST /inventory/events/inbox`
- `GET /inventory/workbench`

Declared external dependencies are APIs and projections only:

- `GET /identity/policies`
- `POST /audit/contract-events`
- `GET /schema/events`
- `order_demand_projection`
- `shipment_delivery_projection`
- `quality_release_projection`
- `purchase_receipt_projection`
- `demand_forecast_projection`
- `access_policy_projection`

## Events and Handlers

Emitted AppGen-X events:

- `ItemRegistered`
- `InventoryNodeRegistered`
- `GoodsReceiptPosted`
- `InventoryAdjusted`
- `InventoryAllocated`
- `InventoryReleased`
- `QualityHoldApplied`

Consumed AppGen-X events:

- `OrderVerified`
- `ShipmentDelivered`
- `QualityHoldReleased`
- `PurchaseReceiptPosted`
- `DemandForecastChanged`
- `AccessPolicyChanged`

Handlers are idempotent by event id, record inbox evidence, update owned
projections, retry failures according to configuration, and write terminal
failures to `inventory_positioning_dead_letter_event`.

## UI, Permissions, and Workbench

The UI exposes item master, item attributes, lot/serial traceability, node
master, node capacity, receipt, adjustment, availability, allocation, release,
quality hold, in-transit, substitution, backorder, replenishment,
reconciliation, anomaly, risk, rule, parameter, configuration, inbox/outbox,
dead-letter, and release evidence panels.

The permission contract covers read, master data, receive, adjust, allocate,
release, quality, replenish, reconcile, event handling, configuration, and
audit access.

## Package Metadata and Release Evidence

The package key is `inventory_positioning`. Package metadata advertises the
implementation directory, standard features, advanced capabilities, owned
tables, database allowlist, fixed event topic, emitted events, consumed events,
UI fragments, API contract, schema contract, service contract, permissions,
and release evidence.

Release readiness requires:

- `inventory_positioning_runtime_smoke()` returns `ok`.
- `implementation_contract()` includes runtime, UI, API, schema, service,
  permissions, topic, events, and release evidence contracts.
- `inventory_positioning_build_schema_contract()` proves all owned tables,
  models, relationships, migrations, backend allowlist, and no shared table
  access.
- `inventory_positioning_build_service_contract()` proves command and query
  services, transaction boundary, owned mutations, and declared dependencies.
- `inventory_positioning_build_release_evidence()` proves schema depth,
  migration coverage, service depth, AppGen-X API/event contract, permission
  coverage, backend allowlist, and shared-table isolation.
- Focused Inventory Positioning tests pass.
- The global PBC release audit, implementation release audit, implemented
  capability audit, and generation smoke audit pass for the implemented PBC
  set.
- Diff scans contain no banned legacy product or framework names.
