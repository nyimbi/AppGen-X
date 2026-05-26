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
- **Owned tables:** `sales_order`, `order_line`, `fulfillment_plan`,
  `fraud_screen`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Emits:** `OrderVerified`, `OrderPriced`, `OrderShipped`
- **Consumes:** `InventoryAllocated`, `TaxCalculated`, `CustomerUpdated`
- **Primary APIs:** `POST /orders`, `POST /allocation`,
  `GET /fulfillment-plans`
- **UI artifacts:** order orchestration workbench, verification queue,
  fulfillment-plan board, fraud review queue, exception console, policy editor

DOM owns order and fulfillment orchestration state. It references inventory,
tax, customer, payment, warehouse, and transportation facts through APIs,
events, and projections rather than shared tables.

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
