# Transportation Management PBC Specification

`transportation_management` is the AppGen-X packaged business capability for
freight execution: shipment creation, carrier selection, route planning,
tendering, dispatch, tracking, ETA updates, inbound arrival, delivery,
exception handling, freight-cost governance, and transportation analytics. The
implementation is owned under `src/pyAppGen/pbcs/transportation_management/`.

## Owned Boundary

- **PBC key:** `transportation_management`
- **Mesh:** `scl`
- **Owned tables:** `shipment`, `carrier`, `freight_route`, `tracking_event`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Emits:** `InboundArrived`, `ShipmentDelivered`, `EtaUpdated`
- **Consumes:** `Packed`, `PurchaseOrderIssued`
- **Primary APIs:** `POST /shipments`, `POST /carrier-selection`, `GET /eta`
- **UI artifacts:** transportation workbench, carrier selection board, route
  planner, tender monitor, tracking console, exception queue, policy editor

Transportation owns shipment execution and tracking state. Warehouse,
procurement, inventory, order, and finance packages interact through events,
APIs, and projections rather than shared transport tables.

## Rules, Parameters, and Configuration

The runtime must understand and apply executable transportation rules,
parameters, and configuration:

- **Rules:** carrier eligibility, service-level policy, hazardous-material
  restrictions, temperature-control requirements, preferred carrier, restricted
  carrier, lane policy, tender fallback, appointment window, consolidation,
  cross-border document requirements, and delivery proof policy.
- **Parameters:** maximum cost per mile, on-time weighting, carbon weighting,
  service-level weighting, tracking staleness limit, ETA confidence threshold,
  tender timeout, consolidation threshold, delay-risk threshold, and exception
  escalation window.
- **Configuration:** datastore backend, event topic, retry limit, default
  currency, units, allowed modes, telematics providers, label/evidence retention,
  route calendar, default timezone, and workbench limits.

The runtime exposes operations to configure the package, set parameters,
register rules, and apply them during carrier selection, route planning,
tendering, tracking, ETA calculation, exception handling, and delivery
confirmation.

## Standard Table-Stakes Capabilities

1. Shipment creation from packed order, purchase order, transfer, return, or
   inbound movement references.
2. Carrier master references with mode, service levels, lane coverage, cost,
   on-time performance, carbon profile, risk signals, and identity evidence.
3. Freight route planning with origin, destination, stops, distance, mode,
   service level, appointment windows, and cost estimate.
4. Carrier selection and tendering with scorecard, eligibility, fallback, and
   award evidence.
5. Dispatch confirmation and shipment status progression.
6. Tracking event ingestion from telematics, carrier portal, EDI-style payloads,
   manual events, and warehouse dock events.
7. ETA calculation, confidence scoring, and `EtaUpdated` emission.
8. Inbound arrival and delivery confirmation with idempotent event emission.
9. Exception management for delay, damaged freight, missed appointment, missing
   proof, carrier rejection, and tracking silence.
10. Freight cost accrual, surcharge, accessorial, and variance projection.
11. Multi-stop, multi-leg, inbound, outbound, parcel, LTL, truckload, ocean, air,
    rail, and intermodal support.
12. Cross-border document and customs evidence references.
13. Temperature-controlled and hazardous-material handling controls.
14. Carrier performance scorecards and freight audit preparation.
15. Carbon, distance, utilization, and modal-shift analytics.
16. Consumed-event handlers for `Packed` and `PurchaseOrderIssued` with
    retry/dead-letter evidence.
17. Multi-tenant and multi-entity transportation isolation.
18. Permissions and ABAC descriptors for plan, tender, dispatch, track, confirm,
    configure, and audit operations.
19. Configuration schema and seed data for modes, service levels, carriers,
    route statuses, and default parameters.
20. Workbench views for open shipments, tenders, late ETAs, exceptions,
    deliveries, carrier risk, and cost variance.
21. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## Advanced Capabilities

1. Event-sourced shipment lifecycle.
2. Graph-relational freight topology across carrier, shipment, lane, route,
   stop, dock, tracking, order, and supplier nodes.
3. Multi-tenant transportation isolation.
4. Schema-on-read transportation extensibility for carrier, lane, shipment, and
   tracking attributes.
5. Probabilistic ETA and delivery confidence.
6. Real-time freight execution and analytics convergence.
7. Counterfactual carrier and route simulation.
8. Temporal ETA, cost, and delay forecasting.
9. Autonomous transport exception resolution.
10. Semantic transport document and event parsing.
11. Predictive delay, damage, and carrier-risk scoring.
12. Self-healing carrier and telematics route selection.
13. Zero-knowledge delivery proof.
14. Immutable transportation traceability trail.
15. Dynamic transportation policy screening.
16. Automated transportation control testing.
17. Universal API and async event contracts.
18. Cross-system transportation federation with WMS, procurement, inventory,
    order, and finance packages.
19. Carrier network and telematics integration evidence.
20. Decentralized carrier identity verification.
21. Chaos-engineered carrier and telematics tolerance.
22. Crypto-agile transportation authorization.
23. Carbon-aware carrier and route selection.
24. Algebraic route and carrier optimization.
25. Mechanism-design carrier tender allocation.
26. Information-theoretic tracking anomaly detection.
27. Stochastic transit exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML transportation risk governance.
30. Cryptographic engineering for delivery proofs and trace hash chains.
31. Mathematical optimization for carrier, route, cost, and carbon objectives.
32. Transportation MLOps governance with feature lineage, drift, and
    explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration execute and
influence carrier selection and ETA decisions; that transportation-owned state
stays inside the package boundary; that AppGen-X outbox events are idempotent;
and that every standard and advanced capability claim has testable release
evidence.
