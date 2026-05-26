# Global Inventory Visibility PBC Specification

`global_inventory_visibility` is the AppGen-X packaged business capability for
federated, multi-location inventory visibility. The implementation is owned
under `src/pyAppGen/pbcs/global_inventory_visibility/` and must remain
side-effect free at import time.

## Owned Boundary

- **PBC key:** `global_inventory_visibility`
- **Mesh:** `commerce`
- **Implementation directory:** `src/pyAppGen/pbcs/global_inventory_visibility`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Fixed event contract:** AppGen-X only
- **Fixed event topic:** `appgen.global_inventory_visibility.events`
- **User-facing eventing choice:** not allowed
- **Shared table access:** not allowed

The package owns all runtime behavior, schema descriptors, release evidence, UI
contracts, and workbench binding evidence for global inventory visibility. It
may depend on external projections and APIs, but it may not read or write
shared tables directly.

## Owned Tables

The package-local schema contract covers the full owned surface:

- `inventory_pool`
- `supply_node`
- `availability_snapshot`
- `inventory_projection`
- `available_to_promise_projection`
- `capable_to_promise_projection`
- `channel_projection`
- `supply_signal`
- `demand_signal`
- `inventory_reservation`
- `inventory_allocation`
- `inventory_adjustment`
- `inventory_reconciliation`
- `inventory_exception`
- `freshness_sla_evidence`
- `inventory_federation_projection`
- `inventory_audit_trace`
- `inventory_control_assertion`
- `inventory_schema_extension`
- `inventory_rule`
- `inventory_parameter`
- `inventory_configuration`
- `inventory_governed_model`
- `global_inventory_visibility_appgen_outbox_event`
- `global_inventory_visibility_appgen_inbox_event`
- `global_inventory_visibility_dead_letter_event`

`build_schema_contract()` emits field descriptors, relationship descriptors,
generated migration descriptors, generated model descriptors, runtime-table
descriptors, datastore allowlists, and the required event topic.

## Standard Table-Stakes Coverage

The package must cover the standard inventory-visibility baseline:

1. Multi-location inventory pools and supply nodes.
2. Availability snapshots with on-hand, reserved, allocated, in-transit,
   freshness, and staleness evidence.
3. ATP and CTP projections.
4. Reservation visibility and channel projections.
5. Supply and demand signal evidence.
6. Inventory reconciliation and adjustment evidence.
7. Exception handling and remediation guidance.
8. Freshness/SLA evidence and stale-snapshot detection.
9. Federation across warehouse, transportation, planning, and channel views.
10. AppGen-X outbox/inbox/dead-letter evidence with idempotent consumed-event
    handling.
11. Rules, bounded parameters, configuration, permissions, API descriptors, and
    workbench/UI binding evidence.

## Advanced Runtime Coverage

The runtime exposes advanced capability evidence for:

1. Event-sourced availability projections.
2. Graph-relational supply topology.
3. Multi-tenant pool isolation.
4. Schema-evolution resilience.
5. Probabilistic freshness and confidence scoring.
6. Real-time ATP convergence.
7. Counterfactual allocation simulation.
8. Temporal availability forecasting.
9. Autonomous exception resolution.
10. Semantic availability query parsing.
11. Predictive stockout risk.
12. Self-healing projection routing.
13. Cryptographic availability proof.
14. Immutable audit trails.
15. Dynamic policy screening.
16. Automated control testing.
17. Cross-system federation.
18. Reservation/allocation visibility integration.
19. Supply identity verification.
20. Chaos-tolerant projection processing.
21. Crypto-agile authorization evidence.
22. Carbon-aware sourcing windows.
23. Allocation optimization and competing-pool allocation.
24. Inventory anomaly detection and stochastic exposure evidence.
25. Governed model evidence.
26. Temporal freshness/staleness modeling.
27. In-transit network visibility.
28. Deterministic rule-compilation evidence.

## Runtime Builders

The package-local completeness surface is exposed through
`__init__.implementation_contract()` and must include:

- `api_contract`
- `schema_contract`
- `service_contract`
- `release_evidence_contract`
- `permissions_contract`
- `ui_contract`
- `advanced_runtime`

### `build_schema_contract()`

This builder proves the owned schema shape. It emits:

- One table descriptor per owned table.
- One migration descriptor per owned table.
- One model descriptor per owned table.
- Relationship descriptors linking pools, nodes, projections, signals,
  reservations, reconciliation evidence, exception evidence, freshness/SLA
  evidence, and federation evidence.
- Runtime-table descriptors for outbox, inbox, and dead-letter evidence.
- The datastore allowlist and fixed AppGen-X event topic.

### `build_service_contract()`

This builder proves the service boundary. It emits:

- Standard command/query method lists for runtime configuration, rule and
  parameter management, pool/node/snapshot registration, projection, ATP/CTP,
  reservation handling, consumed-event ingestion, exception resolution,
  federation, control testing, release builders, and advanced evidence helpers.
- The transaction boundary
  `global_inventory_visibility_owned_datastore_plus_appgen_outbox`.
- Idempotent handler evidence for `ingest_event`.
- Retry/dead-letter evidence tied to owned AppGen-X inbox/outbox/dead-letter
  tables.
- Eventing metadata that fixes AppGen-X as the only event contract and disables
  any stream-engine or alternate event-contract picker.
- Declared external dependencies limited to APIs and projection feeds only.

### `build_release_evidence()`

This builder combines schema, service, API, permissions, UI, workbench, and
boundary evidence. It must prove:

- Owned schema depth and per-table migration coverage.
- Service command depth and idempotent handler evidence.
- Fixed AppGen-X event contract and required event topic.
- Audit permissions for schema/service/release evidence queries.
- UI binding evidence for runtime tables and no shared-table access.
- Workbench binding evidence for configuration, rule, parameter, and runtime
  event-table surfaces.
- Backend allowlist conformance and no shared-table access.

## API Contract

`build_api_contract()` emits structured route descriptors, not just route names.
The descriptors cover:

- `PUT /inventory/configuration`
- `POST /inventory/parameters`
- `POST /inventory/rules`
- `POST /inventory/pools`
- `POST /inventory/supply-nodes`
- `POST /inventory/snapshots`
- `POST /inventory/projections`
- `POST /inventory/reservations`
- `POST /inventory/events/inbox`
- `GET /inventory/availability`
- `GET /inventory/workbench`
- `GET /inventory/schema-contract`
- `GET /inventory/service-contract`
- `GET /inventory/release-evidence`

Each route descriptor carries owned-table evidence, required permission,
AppGen-X contract metadata, the fixed event topic, and a shared-table-access
flag set to `False`.

## Event Contract

The package consumes AppGen-X inventory-adjacent events and emits AppGen-X
inventory-visibility events. Event evidence must remain package-local:

- Outbox table: `global_inventory_visibility_appgen_outbox_event`
- Inbox table: `global_inventory_visibility_appgen_inbox_event`
- Dead-letter table: `global_inventory_visibility_dead_letter_event`
- Consumed events are processed idempotently by `ingest_event`.
- Duplicate consumed events return `duplicate: True` without mutating state.
- Retry evidence is recorded in `retry_evidence`.
- Retry exhaustion writes dead-letter evidence with
  `reason == "retry_limit_exceeded"`.

## Rules, Parameters, and Configuration

The runtime must support deterministic rule compilation, bounded parameters, and
fixed configuration:

- **Rules:** allocation policy, node preference, freshness floors,
  safety-stock overrides, projection routing, reservation controls, exception
  resolution, and governance screening.
- **Parameters:** safety-stock percent, freshness half-life, availability
  confidence floor, reservation TTL, projection horizon, stockout risk
  threshold, staleness SLA, carbon-cost weight, federation lag tolerance, and
  workbench limit.
- **Configuration:** datastore backend, fixed AppGen-X event topic, retry
  limit, default currency, projection horizon, staleness SLA, workbench limit,
  and tenant isolation.

Unsupported parameters, unsupported datastores, missing required rule fields,
and any attempt to expose user-facing eventing or stream-engine choices are
rejected.

## UI and Workbench Binding Evidence

The UI contract and rendered workbench must expose explicit binding evidence for:

- Owned tables and runtime tables.
- Outbox, inbox, and dead-letter surfaces.
- Configuration, rules, and parameters.
- RBAC action bindings.
- AppGen-X event contract and required event topic.
- Available ATP/CTP, channel projection count, freshness evidence, and
  dead-letter counts.

## Verification and Release Criteria

The completeness slice is acceptable only when:

1. `global_inventory_visibility_runtime_smoke()` returns `ok: True`.
2. `implementation_contract()` includes schema, service, and release-evidence
   contracts in addition to API, UI, permissions, advanced runtime, owned
   tables, runtime tables, allowed datastores, event topic, and emitted/consumed
   event contracts.
3. Focused runtime tests prove configuration, rule/parameter binding, pool and
   node registration, snapshot/projection/reservation flow, ATP/CTP evidence,
   channel projections, supply/demand signals, idempotent inbox behavior,
   retry/dead-letter evidence, API descriptors, permissions, schema/service
   builders, release evidence, and workbench/UI binding evidence.
4. `python -m py_compile` succeeds for the owned Python files.
5. Focused `pytest` for `tests/test_pbc_global_inventory_visibility_runtime.py`
   passes.

## Seed And Release Evidence

Release evidence includes package-local seed data for inventory status codes,
availability bands, source-system classes, freshness thresholds, and exception
reasons. Generated applications validate those seed descriptors together with
owned schema, migration, model, service, route, event, handler, UI, RBAC,
configuration, and release contracts.
