# Transportation Management PBC Specification

`transportation_management` is the AppGen-X packaged business capability for
freight execution: shipment creation, carrier selection, route planning,
tendering, dispatch, tracking, ETA updates, inbound arrival, delivery,
exception handling, freight-cost governance, and transportation analytics. The
implementation is owned under `src/pyAppGen/pbcs/transportation_management/`.

## Owned Boundary

- **PBC key:** `transportation_management`
- **Mesh:** `scl`
- **Owned tables:** `shipment`, `shipment_line`, `shipment_party`,
  `shipment_reference`, `shipment_package`, `carrier`,
  `carrier_service_level`, `carrier_lane`, `carrier_contract`,
  `carrier_identity`, `freight_route`, `route_stop`, `route_leg`,
  `route_constraint`, `carrier_tender`, `carrier_tender_response`,
  `dispatch_confirmation`, `tracking_event`, `eta_snapshot`,
  `inbound_arrival`, `delivery_proof`, `delivery_exception`,
  `transportation_exception`, `freight_cost_accrual`,
  `freight_invoice_projection`, `cross_border_document`,
  `temperature_hazard_control`, `carrier_scorecard`,
  `carrier_risk_signal`, `carbon_distance_metric`,
  `packed_order_projection`, `purchase_order_projection`,
  `return_authorization_projection`, `inventory_transfer_projection`,
  `access_policy_projection`, `transportation_policy_screening`,
  `transportation_telematics_event`, `transportation_telematics_replay`,
  `transportation_delivery_proof_hash`, `transportation_audit_trace`,
  `transportation_federation_projection`,
  `transportation_carbon_route_selection`,
  `transportation_route_optimization`,
  `transportation_tender_allocation`,
  `transportation_tracking_anomaly_signal`,
  `transportation_transit_exposure_model`,
  `transportation_eta_cost_forecast`, `transportation_parsed_event`,
  `transportation_seed_data`, `transportation_schema_extension`,
  `transportation_control_assertion`, `transportation_governed_model`,
  `transportation_rule`, `transportation_parameter`,
  `transportation_configuration`,
  `transportation_management_appgen_outbox_event`,
  `transportation_management_appgen_inbox_event`, and
  `transportation_management_dead_letter_event`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only
- **Emits:** `CarrierRegistered`, `ShipmentCreated`, `CarrierSelected`,
  `FreightRoutePlanned`, `ShipmentDispatched`, `EtaUpdated`,
  `InboundArrived`, and `ShipmentDelivered`
- **Consumes:** `Packed`, `PurchaseOrderIssued`, `ReturnAuthorized`,
  `InventoryTransferRequested`, and `AccessPolicyChanged`
- **Primary APIs:** `POST /transportation/shipments`,
  `POST /transportation/carriers`,
  `POST /transportation/shipments/{id}/carrier-selection`,
  `POST /transportation/routes`,
  `POST /transportation/shipments/{id}/dispatch`,
  `POST /transportation/tracking-events`,
  `POST /transportation/shipments/{id}/arrival`,
  `POST /transportation/shipments/{id}/delivery`,
  `POST /transportation/events/inbox`, and `GET /transportation/workbench`
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
2. Shipment lines, parties, references, packages, weights, handling codes, and
   source-package projections.
3. Carrier master references with mode, service levels, lane coverage,
   contracts, cost, on-time performance, carbon profile, risk signals, and
   identity evidence.
4. Freight route planning with origin, destination, stops, legs, constraints,
   distance, mode,
   service level, appointment windows, and cost estimate.
5. Carrier selection and tendering with scorecard, eligibility, fallback,
   tender response, and
   award evidence.
6. Dispatch confirmation and shipment status progression.
7. Tracking event ingestion from telematics, carrier portal, EDI-style payloads,
   manual events, and warehouse dock events.
8. ETA calculation, confidence scoring, and `EtaUpdated` emission.
9. Inbound arrival and delivery confirmation with idempotent event emission.
10. Exception management for delay, damaged freight, missed appointment,
    missing
   proof, carrier rejection, and tracking silence.
11. Freight cost accrual, surcharge, accessorial, invoice projection, and
    variance projection.
12. Multi-stop, multi-leg, inbound, outbound, parcel, LTL, truckload, ocean, air,
    rail, and intermodal support.
13. Cross-border document and customs evidence references.
14. Temperature-controlled and hazardous-material handling controls.
15. Carrier performance scorecards and freight audit preparation.
16. Carbon, distance, utilization, and modal-shift analytics.
17. Local projections for packed orders, purchase orders, returns, inventory
    transfers, and access policies.
18. Consumed-event handlers for declared events with
    retry/dead-letter evidence.
19. AppGen-X outbox, inbox, retry, and dead-letter tables.
20. Multi-tenant and multi-entity transportation isolation.
21. Permissions and ABAC descriptors for plan, tender, dispatch, track, confirm,
    configure, and audit operations.
22. Configuration schema and seed data for modes, service levels, carriers,
    route statuses, and default parameters.
23. Workbench views for open shipments, tenders, late ETAs, exceptions,
    deliveries, carrier risk, and cost variance.
24. Schema-contract evidence for every owned table, including generated
    migration paths and model descriptors.
25. Service-contract evidence proving commands mutate only Transportation-owned
    tables and external state enters through declared APIs, events, or
    projections.
26. Release-audit evidence for package ownership, manifests, schema, migrations,
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
that backend configuration rejects anything outside PostgreSQL, MySQL, or
MariaDB; that eventing remains bound to the AppGen-X event contract without
user-facing stream-engine selection; that package-local UI fragments expose
shipment execution, carrier selection, tracking, ETA, delivery proof, exception,
freight-cost, carbon, rule, parameter, and configuration workbench surfaces; and
that every standard and advanced capability claim has testable release evidence.

## Package-Local Implementation Contract

The executable package exports the fixed transportation contract so generated
apps, audits, and package registries do not infer critical boundaries from
free-form documentation. `TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS`
is exactly PostgreSQL, MySQL, and MariaDB. `TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC`
is the fixed AppGen-X topic `appgen.transportation.events`. The configuration
operation rejects alternate topics and rejects user-selectable stream or
eventing fields such as stream-engine pickers, eventing mode selectors, and
transport overrides. That rejection is deliberate: ordinary PBC composition
chooses AppGen-X event semantics at the platform layer, while this package owns
only transportation behavior and its own inbox/outbox/dead-letter evidence.

Owned tables are declared as package metadata and as runtime evidence:
the owned table list above is the complete datastore boundary, including
operational shipment, carrier, route, tender, dispatch, tracking, proof, cost,
projection, policy, telematics, optimization, governance, configuration, and
AppGen-X runtime tables. Schema extensions must target only those tables
and field names must be stable lowercase identifiers. Extensions merge with
existing extension metadata so a package user can add telematics payloads,
appointment attributes, exception classifications, or proof metadata without
overwriting prior extension declarations.

`transportation_management_build_schema_contract()` emits generated schema
evidence for every owned table: fields, ownership, primary key evidence,
relationship descriptors, migration paths under
`pbcs/transportation_management/migrations/`, generated model class names,
allowed datastore backends, and `shared_table_access: false`.

`transportation_management_build_service_contract()` emits service evidence for
configuration, parameters, rules, schema extensions, event handling, carrier
registration, shipment creation, carrier selection, route planning, dispatch,
tracking, arrival, delivery, telematics routing, proofs, policy screening,
federation, identity, resilience, crypto epoch rotation, carbon-aware route
selection, route optimization, tender allocation, controls, and governed model
registration. Query services cover ETA, workbench, simulations, forecasts,
document/event parsing, risk scoring, exception recommendations, anomaly
detection, stochastic transit exposure, and boundary verification.

`transportation_management_build_release_evidence()` combines schema, service,
API, permission, backend, and shared-table checks into a blocking release gate.
A generated app must not mark Transportation complete unless this release
evidence returns `ok: true` with no blocking gaps.

The API contract is descriptor-level rather than a list of strings. Each route
declares its command or query, owned tables touched, event effects, required
permission, and idempotency key. It includes shipment creation, carrier master
maintenance, carrier selection, route planning, dispatch, tracking ingestion,
arrival confirmation, delivery confirmation, inbox handling, and the workbench
query. The contract explicitly states `shared_table_access: false`; integration
with warehouse, procurement, returns, inventory, identity, and audit packages is
through declared APIs, AppGen-X events, and local projections.

Inbound event handling is idempotent and side-effect bounded. Consumed events
are `Packed`, `PurchaseOrderIssued`, `ReturnAuthorized`,
`InventoryTransferRequested`, and `AccessPolicyChanged`. The handler writes an
inbox record, records handler attempts under an idempotency key, updates the
appropriate local projection, and returns duplicate evidence without appending
extra inbox rows after a processed event is replayed. Unsupported or simulated
failed events produce retry evidence until the configured retry limit is
reached, then move to the package-local dead-letter stream with a transportation
reason. The handler never writes to source-package tables.

The permissions contract covers read, master, plan, tender, dispatch, track,
confirm, event, configure, and audit permissions. Each command exposed by the
UI and API maps to a permission, including `receive_event`,
`register_schema_extension`, `configure_runtime`, and audit/control operations.
Workbench rendering exposes binding evidence for owned tables, the fixed
configuration, AppGen-X outbox, inbox, dead-letter tables, and RBAC permission
sets. This makes UI generation auditable: a generated transportation workbench
must show operational shipments and carriers, but it must also expose the event
contract, handler health, dead-letter counts, configuration lock, rules, and
parameters required to operate the package.

Boundary verification is executable. References are valid only when they are
owned transportation tables, consumed event names, package runtime event tables,
declared dependency APIs, declared local projections, or
`transportation_management_`-prefixed package artifacts. Foreign shared-table
references such as inventory balances or customer profiles are violations. This
keeps cross-PBC composition explicit and preserves the transport package as a
composable business capability rather than a shared database module.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `transportation_management`
- Mesh: `scl`
- Datastore backend: `None`

### Owned Tables

- `shipment`
- `shipment_line`
- `shipment_package`
- `carrier`
- `carrier_service_level`
- `carrier_lane`
- `freight_route`
- `route_stop`
- `route_leg`
- `carrier_tender`
- `dispatch_confirmation`
- `tracking_event`
- `eta_snapshot`
- `inbound_arrival`
- `delivery_proof`
- `freight_cost_accrual`
- `transportation_management_appgen_outbox_event`
- `transportation_management_appgen_inbox_event`
- `transportation_management_dead_letter_event`

### API Routes

- `POST /transportation/shipments`
- `POST /transportation/carriers`
- `POST /transportation/shipments/{id}/carrier-selection`
- `POST /transportation/routes`
- `POST /transportation/tracking-events`
- `POST /transportation/shipments/{id}/delivery`
- `GET /transportation/workbench`

### Emitted Events

- `CarrierRegistered`
- `ShipmentCreated`
- `CarrierSelected`
- `FreightRoutePlanned`
- `ShipmentDispatched`
- `EtaUpdated`
- `InboundArrived`
- `ShipmentDelivered`

### Consumed Events

- `Packed`
- `PurchaseOrderIssued`
- `ReturnAuthorized`
- `InventoryTransferRequested`
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

## Agent, Chatbot Skills, And Self-Registration Contract

The `transportation_management` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `transportation_management_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Transportation Management` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `transportation_management_shipment`, `transportation_management_shipment_line`, `transportation_management_shipment_package`, `transportation_management_carrier`, `transportation_management_carrier_service_level`, `transportation_management_carrier_lane`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `CarrierRegistered`, `ShipmentCreated`, `CarrierSelected`, `FreightRoutePlanned`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `transportation_management`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `transportation_management_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

