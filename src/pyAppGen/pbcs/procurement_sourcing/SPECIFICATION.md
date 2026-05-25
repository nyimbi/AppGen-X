# Procurement and Strategic Sourcing PBC Specification

`procurement_sourcing` is the AppGen-X packaged business capability for
source-to-order execution: purchase requisitions, sourcing events, RFQs,
supplier scoring, contract awards, purchase orders, approvals, compliance,
vendor performance, and supply-risk governance. The implementation lives under
`src/pyAppGen/pbcs/procurement_sourcing/`.

## Owned Boundary

- **PBC key:** `procurement_sourcing`
- **Mesh:** `scl`
- **Owned tables:** `purchase_requisition`, `rfq`, `vendor_contract`,
  `purchase_order`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Emits:** `PurchaseOrderIssued`, `SupplierSelected`
- **Consumes:** `MaterialShortageDetected`, `VendorPerformanceUpdated`
- **Primary APIs:** `POST /requisitions`, `POST /rfqs`,
  `POST /purchase-orders`
- **UI artifacts:** sourcing workbench, requisition queue, RFQ monitor,
  supplier scorecard, contract award board, purchase-order console, policy
  editor

Procurement owns source-to-order records. AP, inventory, manufacturing, and
supplier relationship packages interact through APIs/events/projections, not
shared procurement tables.

## Rules, Parameters, and Configuration

Every generated procurement package must understand and execute business rules,
runtime parameters, and configuration:

- **Rules:** requisition approval thresholds, preferred supplier, category
  policy, diversity/sustainability weighting, restricted supplier screening,
  budget control, split-award eligibility, emergency sourcing, contract
  precedence, PO tolerance, and three-way-match handoff requirements.
- **Parameters:** approval limit, RFQ response window, minimum bid count,
  supplier risk threshold, score weights, price variance tolerance, lead-time
  tolerance, contract renewal horizon, emergency premium, and award confidence.
- **Configuration:** datastore backend, event topic, retry limit, default
  currency, allowed categories, authority matrix, sourcing calendar, retention,
  evidence policy, and workbench limits.

The runtime exposes operations to configure the PBC, set parameters, register
rules, and apply them during requisition approval, RFQ evaluation, supplier
selection, contract award, and purchase-order issuance.

## Standard Table-Stakes Capabilities

1. Purchase requisition creation, validation, enrichment, approval routing, and
   budget/policy checks.
2. Category, commodity, cost center, project, and legal entity references.
3. Supplier registration references, preferred supplier policy, and supplier
   performance projections.
4. RFQ creation, supplier invitation, response capture, bid normalization, and
   response-window controls.
5. Supplier scoring across price, lead time, risk, quality, performance,
   sustainability, diversity, and compliance dimensions.
6. Award recommendation, split award, negotiation summary, and award approval.
7. Contract creation with price, term, renewal, service-level, compliance, and
   evidence metadata.
8. Purchase order creation, line validation, tolerance checks, contract binding,
   approval status, and idempotent event emission.
9. Blanket PO, planned PO, emergency PO, service PO, and direct/indirect spend
   support.
10. Change order and cancellation control.
11. Supplier risk and compliance screening.
12. Spend analytics, savings calculation, and budget commitment projection.
13. Contract renewal, expiry, and obligation monitoring.
14. Material shortage and supplier performance consumed-event handling with
    retry/dead-letter evidence.
15. Multi-tenant and multi-entity procurement isolation.
16. Permissions and ABAC descriptors for request, approve, source, award,
    contract, order, configure, and audit operations.
17. Configuration schema and seed data for categories, award methods, approval
    levels, currencies, and default parameters.
18. Workbench views for open requisitions, active RFQs, pending awards, PO
    backlog, supplier risks, contract renewals, and sourcing exceptions.
19. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## Advanced Capabilities

1. Event-sourced source-to-order lifecycle.
2. Graph-relational supplier, category, contract, RFQ, PO, and risk topology.
3. Multi-tenant procurement isolation.
4. Schema-on-read procurement extensibility for categories, evidence, bids, and
   contracts.
5. Probabilistic supplier award confidence.
6. Real-time sourcing and spend analytics convergence.
7. Counterfactual sourcing strategy simulation.
8. Temporal price, lead-time, and supply-risk forecasting.
9. Autonomous supplier selection and negotiation recommendations.
10. Semantic requisition, quote, and contract parsing.
11. Predictive supplier disruption and compliance risk.
12. Self-healing PO route selection with retry/dead-letter evidence.
13. Zero-knowledge supplier compliance proof.
14. Immutable procurement audit trail.
15. Dynamic policy screening for restricted suppliers, budget, category, and
    tolerance violations.
16. Automated procurement control testing.
17. Universal API and async event contracts.
18. Cross-system procurement federation with AP, inventory, manufacturing, and
    supplier systems.
19. Supplier network integration evidence.
20. Decentralized supplier identity verification.
21. Chaos-engineered supplier and PO route tolerance.
22. Crypto-agile procurement authorization.
23. Carbon-aware sourcing and fulfillment selection.
24. Algebraic sourcing award optimization.
25. Mechanism-design RFQ and auction allocation.
26. Information-theoretic bid anomaly detection.
27. Stochastic supply exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML supplier risk governance.
30. Cryptographic engineering for supplier proofs and hash chains.
31. Mathematical optimization for award and PO routing.
32. Procurement MLOps governance with feature lineage, drift, and explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration execute and
affect procurement decisions; that requisitions, RFQs, contracts, and POs stay
inside the package boundary; that AppGen-X outbox events are idempotent; and
that all standard and advanced capability claims have testable release evidence.
