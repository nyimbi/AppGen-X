# Procurement and Strategic Sourcing PBC Specification

`procurement_sourcing` is the AppGen-X packaged business capability for
source-to-order execution: purchase requisitions, sourcing events, RFQs,
supplier scoring, contract awards, purchase orders, approvals, compliance,
vendor performance, and supply-risk governance. The implementation lives under
`src/pyAppGen/pbcs/procurement_sourcing/`.

## Owned Boundary

- **PBC key:** `procurement_sourcing`
- **Mesh:** `scl`
- **Owned tables:** `procurement_sourcing_purchase_requisition`,
  `procurement_sourcing_purchase_requisition_line`,
  `procurement_sourcing_requisition_approval`,
  `procurement_sourcing_requisition_budget_check`,
  `procurement_sourcing_category_strategy`,
  `procurement_sourcing_category_policy`,
  `procurement_sourcing_supplier_profile`,
  `procurement_sourcing_supplier_identity`,
  `procurement_sourcing_supplier_site`,
  `procurement_sourcing_supplier_qualification`,
  `procurement_sourcing_supplier_risk_signal`,
  `procurement_sourcing_preferred_supplier_policy`,
  `procurement_sourcing_rfq`, `procurement_sourcing_rfq_line`,
  `procurement_sourcing_supplier_invitation`,
  `procurement_sourcing_supplier_bid`,
  `procurement_sourcing_supplier_bid_line`,
  `procurement_sourcing_bid_normalization`,
  `procurement_sourcing_supplier_scorecard`,
  `procurement_sourcing_supplier_award`,
  `procurement_sourcing_split_award`,
  `procurement_sourcing_vendor_contract`,
  `procurement_sourcing_contract_clause`,
  `procurement_sourcing_contract_compliance_obligation`,
  `procurement_sourcing_contract_renewal`,
  `procurement_sourcing_purchase_order`,
  `procurement_sourcing_purchase_order_line`,
  `procurement_sourcing_change_order`,
  `procurement_sourcing_po_tolerance_check`,
  `procurement_sourcing_payment_terms`,
  `procurement_sourcing_material_shortage_projection`,
  `procurement_sourcing_vendor_performance_projection`,
  `procurement_sourcing_budget_projection`,
  `procurement_sourcing_supplier_risk_projection`,
  `procurement_sourcing_contract_compliance_projection`,
  `procurement_sourcing_access_policy_projection`,
  `procurement_sourcing_policy_screening`,
  `procurement_sourcing_purchase_order_route`,
  `procurement_sourcing_supplier_compliance_proof`,
  `procurement_sourcing_audit_trace`,
  `procurement_sourcing_federation_projection`,
  `procurement_sourcing_carbon_sourcing_selection`,
  `procurement_sourcing_award_optimization`,
  `procurement_sourcing_rfq_mechanism_allocation`,
  `procurement_sourcing_bid_anomaly_signal`,
  `procurement_sourcing_supply_exposure_model`,
  `procurement_sourcing_price_lead_time_forecast`,
  `procurement_sourcing_sourcing_strategy_simulation`,
  `procurement_sourcing_parsed_document`,
  `procurement_sourcing_seed_data`,
  `procurement_sourcing_schema_extension`,
  `procurement_sourcing_control_assertion`,
  `procurement_sourcing_governed_model`,
  `procurement_sourcing_rule`, `procurement_sourcing_parameter`,
  `procurement_sourcing_configuration`,
  `procurement_sourcing_appgen_outbox_event`,
  `procurement_sourcing_appgen_inbox_event`, and
  `procurement_sourcing_dead_letter_event`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Fixed event topic:** `appgen.procurement_sourcing.events`
- **Emits:** `PurchaseRequisitionCreated`,
  `PurchaseRequisitionApproved`, `RfqCreated`, `SupplierBidCaptured`,
  `SupplierSelected`, `VendorContractCreated`, `PurchaseOrderIssued`
- **Consumes:** `MaterialShortageDetected`, `VendorPerformanceUpdated`,
  `BudgetChanged`, `SupplierRiskChanged`, `ContractComplianceChanged`,
  `AccessPolicyChanged`
- **Primary APIs:** `POST /procurement/requisitions`,
  `POST /procurement/requisitions/{id}/approve`,
  `POST /procurement/rfqs`, `POST /procurement/rfqs/{id}/bids`,
  `POST /procurement/rfqs/{id}/score`, `POST /procurement/awards`,
  `POST /procurement/contracts`, `POST /procurement/purchase-orders`,
  `POST /procurement/events/inbox`, and `GET /procurement/workbench`
- **UI artifacts:** sourcing workbench, requisition queue, RFQ monitor,
  supplier scorecard, contract award board, purchase-order console, policy
  editor

Procurement owns source-to-order records. AP, inventory, manufacturing, and
supplier relationship packages interact through APIs/events/projections, not
shared procurement tables.

The package also owns its AppGen-X runtime tables:
`procurement_sourcing_appgen_outbox_event`,
`procurement_sourcing_appgen_inbox_event`, and
`procurement_sourcing_dead_letter_event`. Any dependency on material
availability, supplier performance, budget, compliance, access policy, schema,
identity, or audit data is represented through declared events, API calls, or
package-local projections such as `material_shortage_projection` and
`budget_projection`. The runtime boundary verifier rejects references to
foreign tables and accepts only owned tables, runtime event tables, declared
consumed event names, declared API projections, and declared platform APIs.

The package exports schema, service, and release-evidence contracts from
`pyAppGen.pbcs.procurement_sourcing`. Package discovery must load the module
without mutating state; registration output is a side-effect-free plan that
contains owned tables, generated migration paths, generated model descriptors,
service command/query descriptors, route descriptors, event contracts, UI
fragments, permissions, configuration schema, consumed and emitted events, and
the AppGen-X topic.

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

Configuration is executable, not descriptive. `configure_runtime` accepts only
PostgreSQL, MySQL, or MariaDB; requires the fixed AppGen-X topic
`appgen.procurement_sourcing.events`; stores the AppGen-X event contract name;
records owned tables; and marks the stream-engine picker as hidden and
non-selectable. User-facing stream-engine fields are invalid input because
ordinary PBCs do not expose event transport choice. `set_parameter` accepts only
known procurement parameters. `register_rule` compiles active procurement rules
with a deterministic hash. `register_schema_extension` can extend only
Procurement Sourcing owned tables and rejects invalid field names.

## Standard Table-Stakes Capabilities

1. Purchase requisition creation, validation, enrichment, approval routing, and
   budget/policy checks.
2. Purchase requisition lines, cost center, project, legal entity, category,
   item, quantity, due-date, and currency validation.
3. Category strategy, category policy, commodity references, and preferred
   source methods.
4. Supplier profile, site, qualification, identity, risk signal, and preferred
   supplier policy.
5. RFQ creation, RFQ lines, supplier invitation, response capture, bid
   normalization, and
   response-window controls.
6. Supplier scoring across price, lead time, risk, quality, performance,
   sustainability, diversity, and compliance dimensions.
7. Award recommendation, split award, negotiation summary, and award approval.
8. Contract creation with price, term, clauses, renewal, service-level,
   compliance obligations, and
   evidence metadata.
9. Purchase order creation, line validation, tolerance checks, contract binding,
   approval status, and idempotent event emission.
10. Blanket PO, planned PO, emergency PO, service PO, and direct/indirect spend
   support.
11. Change order, cancellation control, and payment terms.
12. Supplier risk, restricted supplier, and compliance screening.
13. Spend analytics, savings calculation, and budget commitment projection.
14. Contract renewal, expiry, and obligation monitoring.
15. Material shortage and supplier performance consumed-event handling with
    retry/dead-letter evidence.
16. Local projections for material shortage, supplier performance, budget,
    supplier risk, contract compliance, and access policy events.
17. AppGen-X outbox, inbox, retry, and dead-letter tables.
18. Multi-tenant and multi-entity procurement isolation.
19. Permissions and ABAC descriptors for request, approve, source, award,
    contract, order, configure, and audit operations.
20. Configuration schema and seed data for categories, award methods, approval
    levels, currencies, and default parameters.
21. Workbench views for open requisitions, active RFQs, pending awards, PO
    backlog, supplier risks, contract renewals, and sourcing exceptions.
22. Schema-contract evidence for every owned table, including generated
    migration paths and model descriptors.
23. Service-contract evidence proving commands mutate only Procurement-owned
    tables and external state enters through declared APIs, events, or
    projections.
24. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## API, Handler, and UI Contract

Procurement Sourcing exposes descriptor-level route contracts rather than loose
route strings. Each route declares its command or query, owned table access,
emitted events, required permission, and idempotency key. The route set covers
requisition creation and approval, RFQ creation, bid capture, supplier scoring,
award selection, contract creation, purchase order issuance, event inbox
handling, and workbench read models. The API contract declares no shared table
access, fixed AppGen-X eventing, the required event topic, async event names,
and the allowed database backends.

The package includes an idempotent `receive_event` handler for all consumed
events. The handler writes an inbox entry, derives a deterministic idempotency
key, ignores duplicate processed events, projects supported events into
package-local read models, records retry evidence for failed or unsupported
events, and moves messages to the package dead-letter table after the runtime
retry limit is exhausted. Material shortages update sourcing demand
projections; supplier performance and risk events update supplier projections;
budget and contract compliance events update award and release-gate
projections; access policy events update local authorization projections. These
projections inform sourcing decisions while keeping the source tables in their
own PBCs.

Permissions are action-level. Requesters can create requisitions, approvers can
approve, sourcing users can create RFQs and score bids, bid users can capture
responses, award users can select suppliers, contract users can create contract
records, order users can issue POs, event users can run the inbox handler,
configuration users can manage rules, parameters, runtime configuration, and
schema extensions, and audit users can view control evidence. The UI contract
binds these permissions to workbench actions and exposes procurement panels for
requisitions, approvals, budget policy, suppliers, RFQs, invitations, bid
capture, normalization, scoring, awards, contracts, renewals, purchase orders,
risk, spend, rules, parameters, and configuration. UI binding evidence includes
owned tables, outbox, inbox, dead-letter tables, hidden stream picker, fixed
topic, AppGen-X contract, and no shared table access.

## Generated Schema, Models, and Services

`procurement_sourcing_build_schema_contract()` emits generated schema evidence
for every Procurement-owned table: field names, ownership, primary-key
evidence, relationship descriptors, migration paths under
`pbcs/procurement_sourcing/migrations/`, generated model class names, allowed
datastore backends, and `shared_table_access: false`.

`procurement_sourcing_build_service_contract()` emits service evidence for
configuration, parameters, rules, schema extensions, event handling,
requisition creation, approval, RFQ creation, bid capture, supplier scoring,
supplier award, contract creation, PO issuance, policy screening, PO routing,
compliance proofs, federation, identity verification, resilience drills,
crypto epoch rotation, carbon-aware sourcing, award optimization, RFQ
allocation, controls, and governed model registration. Query services cover
the workbench, bid anomaly detection, stochastic supply exposure, price and
lead-time forecasts, sourcing strategy simulation, document parsing, supplier
risk scoring, and boundary verification. The service contract declares the
transaction boundary as the Procurement-owned datastore plus AppGen-X outbox
and lists only declared APIs, consumed events, and projections as external
dependencies.

`procurement_sourcing_build_release_evidence()` combines schema, service, API,
permission, backend, and shared-table checks into the release gate. A generated
app must not mark Procurement complete unless this release evidence returns
`ok: true` with no blocking gaps.

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
affect procurement decisions; that runtime configuration rejects unsupported
backends while exposing only the AppGen-X event contract; that package-local UI
fragments cover requisitions, approval, budget policy, suppliers, RFQs,
invitations, bid capture, scoring, awards, contracts, renewals, purchase orders,
risk, spend analytics, rules, parameters, and configuration; that requisitions,
RFQs, contracts, and POs stay inside the package boundary; that AppGen-X outbox
events are idempotent; that AppGen-X inbox events are idempotent, retryable,
projected, and dead-lettered; that descriptor APIs and RBAC contracts are
exported from the package; that package metadata declares owned tables and
allowed backends; and that all standard and advanced capability claims have
testable release evidence.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `procurement_sourcing`
- Mesh: `scl`
- Datastore backend: `None`

### Owned Tables

- `procurement_sourcing_purchase_requisition`
- `procurement_sourcing_purchase_requisition_line`
- `procurement_sourcing_requisition_approval`
- `procurement_sourcing_category_strategy`
- `procurement_sourcing_supplier_profile`
- `procurement_sourcing_supplier_qualification`
- `procurement_sourcing_rfq`
- `procurement_sourcing_rfq_line`
- `procurement_sourcing_supplier_invitation`
- `procurement_sourcing_supplier_bid`
- `procurement_sourcing_supplier_scorecard`
- `procurement_sourcing_supplier_award`
- `procurement_sourcing_vendor_contract`
- `procurement_sourcing_purchase_order`
- `procurement_sourcing_purchase_order_line`
- `procurement_sourcing_appgen_outbox_event`
- `procurement_sourcing_appgen_inbox_event`
- `procurement_sourcing_dead_letter_event`

### API Routes

- `POST /procurement/requisitions`
- `POST /procurement/rfqs`
- `POST /procurement/rfqs/{id}/bids`
- `POST /procurement/awards`
- `POST /procurement/contracts`
- `POST /procurement/purchase-orders`
- `GET /procurement/workbench`

### Emitted Events

- `PurchaseRequisitionCreated`
- `PurchaseRequisitionApproved`
- `RfqCreated`
- `SupplierBidCaptured`
- `SupplierSelected`
- `VendorContractCreated`
- `PurchaseOrderIssued`

### Consumed Events

- `MaterialShortageDetected`
- `VendorPerformanceUpdated`
- `BudgetChanged`
- `SupplierRiskChanged`
- `ContractComplianceChanged`
- `AccessPolicyChanged`

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
