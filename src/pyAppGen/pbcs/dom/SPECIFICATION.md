# Distributed Order Management PBC Specification

`dom` is the AppGen-X packaged business capability for distributed order
management: order capture, verification, pricing handoff, tax and customer
projection use, fraud screening, sourcing, allocation orchestration, fulfillment
planning, shipment confirmation projection, exception handling, and order
lifecycle visibility. The implementation is owned under
`src/pyAppGen/pbcs/dom/`.

## Owned Boundary

- **PBC key:** `dom`
- **Mesh:** `cx`
- **Owned tables:** `sales_order`, `order_line`, `order_status`,
  `customer_projection`, `tax_projection`, `fraud_screen`,
  `inventory_allocation_projection`, `payment_authorization_projection`,
  `fulfillment_plan`, `split_shipment`, `backorder`, `substitution`,
  `cancellation_request`, `shipment_projection`, `order_exception`,
  `route_selection`, `risk_score`, `policy_rule`, `dom_parameter`,
  `dom_configuration`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Fixed event topic:** `appgen.dom.events`
- **Emits:** `OrderCaptured`, `TaxProjectionApplied`, `FraudScreened`,
  `OrderVerified`, `OrderPriced`, `InventoryAllocationProjected`,
  `FulfillmentPlanCreated`, `OrderShipped`
- **Consumes:** `InventoryAllocated`, `TaxCalculated`, `CustomerUpdated`,
  `PaymentAuthorized`, `ShipmentDelivered`
- **Primary APIs:** `POST /orders`, `POST /allocation`,
  `GET /fulfillment-plans`
- **UI artifacts:** order orchestration workbench, verification queue,
  fulfillment-plan board, fraud review queue, exception console, policy editor

DOM owns order and fulfillment orchestration state. It references inventory,
tax, customer, payment, warehouse, and transportation facts through APIs,
events, and projections rather than shared tables.

The package must reject any configuration that exposes a user-facing stream
engine selector, alternate event transport, or custom eventing mode. Users can
configure business behavior, retention, retry limits, allowed channels, and
status policies; they cannot choose a stream engine or bypass the AppGen-X
event contract. Runtime, UI, API, and release evidence must all expose
`stream_engine_picker_visible: false`, `user_selectable_event_contract: false`,
the fixed topic, and the PostgreSQL/MySQL/MariaDB backend allowlist.

## Rules, Parameters, and Configuration

The runtime must execute order-management rules, parameters, and configuration:

- **Rules:** order validation, fraud threshold, customer status policy, payment
  hold policy, sourcing priority, split shipment eligibility, substitution,
  backorder, cancellation, promise-date, fulfillment route, tax-ready gating,
  and shipment confirmation requirements.
- **Parameters:** fraud threshold, max split shipments, allocation confidence
  threshold, partial fulfillment threshold, service-level weight, distance
  weight, margin weight, promise horizon, exception age threshold, and retry
  limit.
- **Configuration:** datastore backend, event topic, default currency, allowed
  order channels, allowed statuses, fulfillment calendars, sourcing regions,
  evidence retention, workbench limits, and tenant isolation.

The runtime exposes operations to configure the package, set parameters,
register rules, and apply them during order capture, verification, fraud
screening, sourcing, allocation, fulfillment planning, and shipping projection.

Rules compile into deterministic hashes so registration is auditable and can be
compared across tenants and release candidates. Parameters are deliberately
named and validated; unknown keys are rejected because operational policies must
not drift through ad hoc runtime metadata. Configuration is part of the release
surface: it binds the datastore family, the fixed AppGen-X event topic, retry
limits, default currency, allowed channels, allowed order statuses, workbench
limits, and tenant-safe evidence retention.

Schema extension is available only for DOM-owned tables. Extension field names
must be lowercase snake case so generated models, migrations, API descriptors,
and workbench forms remain portable across supported relational backends. Any
attempt to extend inventory, customer master, finance, warehouse, carrier, tax
authority, or payment-owned tables is a boundary violation; those relationships
must be modeled as consumed events, read APIs, or local projections.

## Standard Table-Stakes Capabilities

1. Sales order capture with customer, channel, currency, lines, requested
   service level, destination, and source references.
2. Order validation for required fields, supported channel, active customer,
   tax readiness, payment hold, and line integrity.
3. Fraud screening with score, reason codes, threshold policy, review decision,
   and explainable evidence.
4. Customer projection handling from `CustomerUpdated`.
5. Tax projection handling from `TaxCalculated`.
6. Price and charge summary with `OrderPriced` event emission.
7. Inventory allocation handoff and consumed allocation projection from
   `InventoryAllocated`.
8. Fulfillment plan creation with node choice, split shipment, source priority,
   promise date, and route references.
9. Backorder, partial fulfillment, cancellation, substitution, and exception
   handling.
10. Shipment projection and `OrderShipped` event emission.
11. Order lifecycle status transitions and idempotent event history.
12. Multi-channel, multi-tenant, and multi-entity order isolation.
13. Order orchestration workbench with open orders, fraud reviews, allocation
   gaps, fulfillment plans, exceptions, and shipped orders.
14. Retry, dead-letter, and idempotency evidence for consumed customer, tax, and
   inventory events.
15. Permissions and ABAC descriptors for create, verify, price, allocate, plan,
   cancel, ship, configure, and audit operations.
16. Configuration schema and seed data for channels, statuses, service levels,
   fulfillment policies, and default parameters.
17. Release-audit evidence for package ownership, manifests, schema, migrations,
   models, services, routes, events, handlers, UI, permissions, configuration,
   tests, registration metadata, and generation smoke.

18. Event inbox processing for allocation, tax, customer, payment, and shipment
    events, with duplicate detection by idempotency key.
19. Dead-letter records for unsupported or repeatedly failing consumed events,
    including event id, event type, tenant, attempt count, and reason.
20. Descriptor-level API metadata for each command, query, emitted event,
    consumed event, owned table, idempotency key, and required permission.
21. Permission descriptors for order create, verification, pricing,
    allocation, fulfillment planning, shipping, cancellation, event handling,
    configuration, and audit surfaces.
22. Workbench binding evidence proving that UI fragments bind to DOM-owned
    tables, the AppGen-X outbox, the AppGen-X inbox, the dead-letter table,
    fixed configuration, and RBAC permissions.

## Advanced Capabilities

1. Event-sourced order lifecycle.
2. Graph-relational order, customer, line, node, shipment, tax, and allocation
   topology.
3. Multi-tenant order isolation.
4. Schema-on-read order extensibility for channels, lines, payment, and
   fulfillment attributes.
5. Probabilistic fraud and allocation confidence.
6. Real-time order orchestration and analytics convergence.
7. Counterfactual sourcing and fulfillment simulation.
8. Temporal promise-date and demand impact forecasting.
9. Autonomous exception resolution recommendations.
10. Semantic order event and customer instruction parsing.
11. Predictive cancellation, fraud, and fulfillment-risk scoring.
12. Self-healing fulfillment route selection.
13. Zero-knowledge order verification proof.
14. Immutable order audit trail.
15. Dynamic order policy screening.
16. Automated order-control testing.
17. Universal API and async event contracts.
18. Cross-system order federation with inventory, tax, customer, warehouse,
    transportation, and finance packages.
19. Commerce and service-channel integration evidence.
20. Decentralized customer/order identity verification.
21. Chaos-engineered orchestration tolerance.
22. Crypto-agile order authorization.
23. Carbon-aware fulfillment planning.
24. Algebraic fulfillment optimization.
25. Mechanism-design allocation among channels or nodes.
26. Information-theoretic order anomaly detection.
27. Stochastic fulfillment exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML order-risk governance.
30. Cryptographic engineering for proofs and hash chains.
31. Mathematical optimization for sourcing, fulfillment, and split decisions.
32. Order MLOps governance with feature lineage, drift, and explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration execute and
influence order verification and fulfillment decisions; that order-owned state
stays inside the package boundary; that AppGen-X outbox events are idempotent;
that backend configuration rejects anything outside PostgreSQL, MySQL, or
MariaDB; that eventing remains bound to the AppGen-X event contract without
user-facing stream-engine selection; that package-local UI fragments expose
order capture, validation, customer/tax projection, fraud, verification,
pricing, allocation, fulfillment, split/backorder/cancellation, shipment,
exception, federation, rule, parameter, and configuration workbench surfaces;
and that all standard and advanced capabilities have testable release evidence.

The executable contract has the following package-local functions:

- `dom_configure_runtime` accepts only PostgreSQL, MySQL, or MariaDB and only
  the fixed `appgen.dom.events` topic. It records AppGen-X eventing metadata,
  owned tables, and hidden event selector evidence.
- `dom_register_schema_extension` accepts extensions for owned tables only and
  merges valid fields without deleting existing extensions.
- `dom_receive_event` is the only consumed-event entrypoint. It records every
  event in the inbox, projects supported events into local projection stores,
  suppresses processed duplicates, records retry evidence, and sends
  unsupported or repeatedly failing events to the dead-letter table.
- `dom_build_api_contract` returns descriptor-level routes rather than opaque
  strings. Each route declares its command/query, owned tables, emitted or
  consumed events, required permission, and idempotency key.
- `dom_permissions_contract` returns package-local permissions plus the
  action-to-permission map used by generated routes and UI fragments.
- `dom_verify_owned_table_boundary` proves that references are either owned
  tables, AppGen-X runtime tables, declared consumed events, declared API
  projections, or package-prefixed generated artifacts. Foreign shared table
  references are rejected.

## Event Handling Contract

DOM emits events only through the AppGen-X outbox. Outbox records carry the
event type, payload, and deterministic idempotency key. Consumed events arrive
through the AppGen-X inbox and are processed idempotently:

- `InventoryAllocated` updates inventory allocation projections.
- `TaxCalculated` updates tax calculation projections.
- `CustomerUpdated` updates customer profile projections.
- `PaymentAuthorized` updates payment authorization projections.
- `ShipmentDelivered` updates shipment delivery projections.

The handler never mutates another package's table. Projection keys come from the
event payload when present and otherwise fall back to event id, which keeps
replay deterministic. Unsupported events and simulated handler failures are
tracked with retry attempts until the configured retry limit is reached; then a
dead-letter entry is created. This evidence is surfaced to the workbench and to
release audit tests.

## UI and Workbench Contract

The package includes UI fragments because DOM is an operational PBC. Generated
applications must expose a workbench for capture, validation, verification,
pricing, allocation, fulfillment planning, exception handling, federation,
rules, parameters, and configuration. The UI contract binds fragments to owned
tables and AppGen-X runtime tables; it must not expose stream engine pickers.
The renderer computes visible actions from RBAC permissions, separates locked
actions, shows outbox/inbox/dead-letter counts, and carries configuration
binding evidence so generated apps can prove that the UI is attached to the
actual package runtime rather than a placeholder catalog entry.
