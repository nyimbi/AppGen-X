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
  `order_note`, `order_hold`, `order_promise`, `order_channel_context`,
  `order_payment_projection`, `customer_projection`,
  `customer_identity_projection`, `tax_projection`, `fraud_screen`,
  `fraud_signal`, `order_verification`, `order_price_component`,
  `order_discount_projection`, `inventory_allocation_projection`,
  `inventory_node_projection`, `payment_authorization_projection`,
  `fulfillment_plan`, `fulfillment_plan_line`,
  `fulfillment_node_candidate`, `fulfillment_reservation_projection`,
  `split_shipment`, `backorder`, `substitution`,
  `cancellation_request`, `shipment_projection`,
  `shipment_status_projection`, `order_exception`, `route_selection`,
  `risk_score`, `promise_demand_forecast`,
  `fulfillment_policy_simulation`, `fulfillment_route_replay`,
  `order_verification_proof`, `order_policy_screening`,
  `order_audit_trace`, `order_federation_projection`,
  `order_carbon_fulfillment`, `order_fulfillment_optimization`,
  `order_node_allocation`, `order_anomaly_signal`,
  `order_fulfillment_exposure_model`, `order_parsed_event`,
  `order_seed_data`, `dom_schema_extension`, `dom_control_assertion`,
  `dom_governed_model`, `policy_rule`, `dom_parameter`,
  `dom_configuration`, `dom_appgen_outbox_event`, `dom_appgen_inbox_event`,
  and `dom_dead_letter_event`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Fixed event topic:** `appgen.dom.events`
- **Emits:** `OrderCaptured`, `TaxProjectionApplied`, `FraudScreened`,
  `OrderVerified`, `OrderPriced`, `InventoryAllocationProjected`,
  `FulfillmentPlanCreated`, `OrderShipped`
- **Consumes:** `InventoryAllocated`, `TaxCalculated`, `CustomerUpdated`,
  `PaymentAuthorized`, `ShipmentDelivered`
- **Primary APIs:** `POST /dom/orders`,
  `POST /dom/orders/{id}/tax-projection`,
  `POST /dom/orders/{id}/fraud-screen`, `POST /dom/orders/{id}/verify`,
  `POST /dom/orders/{id}/price`, `POST /dom/orders/{id}/allocation`,
  `POST /dom/fulfillment-plans`, `POST /dom/shipments`,
  `POST /dom/events/inbox`, and `GET /dom/workbench`
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
2. Order notes, holds, promise dates, channel context, and payment projection
   evidence.
3. Order validation for required fields, supported channel, active customer,
   tax readiness, payment hold, and line integrity.
4. Fraud screening with signals, score, reason codes, threshold policy, review
   decision,
   and explainable evidence.
5. Customer and customer identity projection handling from `CustomerUpdated`.
6. Tax projection handling from `TaxCalculated`.
7. Price component, discount projection, and charge summary with `OrderPriced`
   event emission.
8. Inventory allocation and inventory node handoff projection from
   `InventoryAllocated`.
9. Fulfillment plan creation with plan lines, node candidates, reservations,
   split shipment, source priority, promise date, and route references.
10. Backorder, partial fulfillment, cancellation, substitution, and exception
   handling.
11. Shipment and shipment-status projection and `OrderShipped` event emission.
12. Order lifecycle status transitions and idempotent event history.
13. Promise-demand forecasting, fulfillment simulation, route replay, and
    order policy screening.
14. Order verification proof, audit trail, federation projection, carbon-aware
    fulfillment, optimization, node allocation, anomaly detection, and
    stochastic fulfillment exposure.
15. AppGen-X outbox, inbox, retry, and dead-letter tables.
16. Multi-channel, multi-tenant, and multi-entity order isolation.
17. Order orchestration workbench with open orders, fraud reviews, allocation
   gaps, fulfillment plans, exceptions, and shipped orders.
18. Retry, dead-letter, and idempotency evidence for consumed customer, tax, and
   inventory events.
19. Permissions and ABAC descriptors for create, verify, price, allocate, plan,
   cancel, ship, configure, and audit operations.
20. Configuration schema and seed data for channels, statuses, service levels,
   fulfillment policies, and default parameters.
21. Schema-contract evidence for every owned table, including generated
    migration paths and model descriptors.
22. Service-contract evidence proving commands mutate only DOM-owned tables and
    external state enters through declared APIs, events, or projections.
23. Release-audit evidence for package ownership, manifests, schema, migrations,
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
- `dom_build_schema_contract` returns generated schema evidence for every
  owned table, including fields, relationships, generated migration paths,
  generated model descriptors, backend allowlists, and no shared-table access.
- `dom_build_service_contract` returns service command/query evidence,
  transaction boundary, mutates-only table set, declared API dependencies,
  consumed events, package-local projections, and no shared-table dependencies.
- `dom_build_release_evidence` combines schema, service, API, permission,
  backend, and shared-table checks into a blocking release gate.
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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `dom`
- Mesh: `cx`
- Datastore backend: `None`

### Owned Tables

- `sales_order`
- `order_line`
- `order_status`
- `order_promise`
- `customer_projection`
- `tax_projection`
- `fraud_screen`
- `order_verification`
- `order_price_component`
- `inventory_allocation_projection`
- `payment_authorization_projection`
- `fulfillment_plan`
- `fulfillment_plan_line`
- `fulfillment_node_candidate`
- `split_shipment`
- `backorder`
- `substitution`
- `shipment_projection`
- `dom_appgen_outbox_event`
- `dom_appgen_inbox_event`
- `dom_dead_letter_event`

### API Routes

- `POST /dom/orders`
- `POST /dom/orders/{id}/verify`
- `POST /dom/orders/{id}/price`
- `POST /dom/orders/{id}/allocation`
- `POST /dom/fulfillment-plans`
- `POST /dom/shipments`
- `GET /dom/workbench`

### Emitted Events

- `OrderCaptured`
- `TaxProjectionApplied`
- `FraudScreened`
- `OrderVerified`
- `OrderPriced`
- `InventoryAllocationProjected`
- `FulfillmentPlanCreated`
- `OrderShipped`

### Consumed Events

- `InventoryAllocated`
- `TaxCalculated`
- `CustomerUpdated`
- `PaymentAuthorized`
- `ShipmentDelivered`

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
