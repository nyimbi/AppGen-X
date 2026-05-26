# Cross Border Trade PBC

`cross_border_trade` is the AppGen-X packaged business capability for
cross-border trade execution, including HS classification, landed-cost
calculation, denied-party and export-control screening, customs document
evidence, duties and taxes, broker and carrier handoffs, declarations,
compliance holds, and audit-proof release evidence. The package owns its
runtime behavior, schema descriptors, API descriptors, UI/workbench bindings,
rules, parameters, configuration, and focused verification.

## Stable Identity

- PBC key: `cross_border_trade`.
- Package directory: `src/pyAppGen/pbcs/cross_border_trade`.
- Runtime entrypoint: `cross_border_trade_runtime_capabilities()`.
- UI entrypoint: `cross_border_trade_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Required event topic: `appgen.cross_border_trade.events`.
- Eventing standard: fixed AppGen-X inbox/outbox contract only.
- User-facing eventing choice: forbidden.
- Stream-engine picker visibility: false.

## Owned Datastore Boundary

The package owns these operational trade tables:

- `hs_classification`.
- `landed_cost_quote`.
- `export_control_check`.
- `customs_declaration`.

The executable schema contract expands ownership to the package-local support
and evidence tables needed for a hardened complete-PBC slice:

- `denied_party_screening`.
- `trade_document_packet`.
- `broker_handoff`.
- `carrier_handoff`.
- `trade_compliance_hold`.
- `country_restriction_policy`.
- `trade_rule`.
- `trade_parameter`.
- `trade_configuration`.
- `trade_schema_extension`.
- `trade_audit_evidence`.
- `cross_border_trade_appgen_outbox_event`.
- `cross_border_trade_appgen_inbox_event`.
- `cross_border_trade_dead_letter_event`.

No shared ERP, customer, inventory, payment, shipment, customs broker, or
carrier tables are accessed directly. Cross-system context enters only through
declared events and read-only projections.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary cross-border trade surface expected from
a production package:

- HS classification with confidence scoring, keyword evidence, origin and
  destination validation, and review routing.
- Landed-cost quoting across goods value, shipping, duty, tax, insurance,
  broker fee, total landed amount, currency, and Incoterms.
- Denied-party screening evidence and export-control checks across counterparty
  risk, destination restrictions, license triggers, and review thresholds.
- Country restrictions and compliance-hold evidence for blocked destinations,
  missing documents, and restricted review outcomes.
- Customs declaration filing with document-packet completeness, broker route
  selection, broker handoff, carrier handoff, and declaration audit hashes.
- Duties and taxes captured as declaration evidence for audit review and
  customs filing support.
- Broker and carrier handoff evidence without shared-table coupling.
- Runtime configuration for database backend, event topic, retry limit,
  default currency, supported countries, supported Incoterms, and workbench
  limit.
- Parameter engine for classification thresholds, denied-party review
  thresholds, duty variance tolerance, de minimis value, broker-routing
  weights, carbon weight, forecast horizon, and workbench limit.
- Rule engine for classification policy, landed-cost policy, export-control
  policy, declaration policy, status, and compiled governance evidence.
- Owned-only schema extension support for trade tables.
- AppGen-X inbox, outbox, retry, idempotency, and dead-letter evidence.
- Package-local permissions for classify, quote, screen, declare, configure,
  event consume, and audit actions.
- Workbench/UI evidence for classifications, landed-cost quotes, export
  controls, declarations, rules, parameters, configuration, eventing, and
  dead-letter review.

## Advanced Capabilities

The runtime smoke and release evidence prove:

- Event-sourced trade lifecycle with immutable event hashes.
- Owned schema boundary enforcement with explicit violation reporting.
- Multi-tenant trade isolation in commands and workbench views.
- Schema-evolution-safe owned extensions.
- Graph-relational trade topology across classification, quote, screening,
  document packet, broker handoff, carrier handoff, and declaration.
- Counterfactual landed-cost simulation and mathematical optimization.
- Temporal duty/tax forecasting and stochastic exposure modeling.
- Autonomous trade exception-resolution evidence.
- Semantic trade-document parsing.
- Predictive export-control risk evidence.
- Carbon-aware broker routing and broker-allocation mechanism design.
- Cryptographic trade proofs, immutable audit evidence, and crypto agility.
- Governed-model evidence and policy-screening evidence.
- Chaos-tolerant AppGen-X event handling with duplicate, retry, and dead-letter
  evidence.

## Schema Contract

`build_schema_contract()` emits:

- Full table metadata for every owned operational, support, governance, and
  runtime event table.
- Relationship descriptors across classifications, quotes, screens,
  declarations, document packets, compliance holds, and handoffs.
- Generated migration descriptors at
  `pbcs/cross_border_trade/migrations/<nnn>_<table>.sql`.
- Generated model descriptors at
  `pbcs/cross_border_trade/models/<table>.py`.
- Runtime-table evidence for outbox, inbox, and dead-letter tables.
- Backend allowlist and required AppGen-X event-topic evidence.

## Service Contract

`build_service_contract()` exposes package-local command and query surfaces for:

- `configure_runtime`.
- `set_parameter`.
- `register_rule`.
- `register_schema_extension`.
- `receive_event`.
- `classify_product`.
- `quote_landed_cost`.
- `screen_export_control`.
- `file_customs_declaration`.
- `run_control_tests`.
- `build_api_contract`.
- `build_schema_contract`.
- `build_service_contract`.
- `build_release_evidence`.
- `build_workbench_view`.
- `verify_owned_table_boundary`.
- Advanced analytical helpers such as landed-cost simulation, duty/tax
  forecasting, trade-proof generation, policy screening, and anomaly
  detection.

The service contract declares AppGen-X eventing, owned mutation boundaries,
rules/parameters/configuration support, idempotent handlers, and zero shared
table dependencies.

## API Contract

`build_api_contract()` declares executable descriptors for:

- `POST /trade/classifications`.
- `POST /trade/landed-cost-quotes`.
- `POST /trade/export-control-checks`.
- `POST /trade/customs-declarations`.
- `POST /cross-border-trade/events/inbox`.
- `GET /trade/workbench`.
- `GET /trade/schema-contract`.
- `GET /trade/service-contract`.
- `GET /trade/release-evidence`.

Each route binds to owned tables only, carries permission requirements, and
declares emitted or consumed AppGen-X events where applicable.

## Events And Idempotency

Consumed event contracts:

- `OrderPlaced`.
- `InventoryReserved`.
- `PaymentCaptured`.
- `ShipmentDispatched`.

Emitted event contracts:

- `HSClassified`.
- `LandedCostQuoted`.
- `ExportControlCleared`.
- `CustomsDeclarationFiled`.

Handlers require event IDs and idempotency keys. Duplicate events are ignored
without double-applying state. Unsupported events first record retry evidence
and then dead-letter evidence once retry limits are exhausted.

## Permissions And UI Binding

`permissions_contract()` exposes:

- Permission descriptors for `cross_border_trade.classify`,
  `cross_border_trade.quote`, `cross_border_trade.screen`,
  `cross_border_trade.declare`, `cross_border_trade.event.consume`,
  `cross_border_trade.configure`, and `cross_border_trade.audit`.
- Role bundles for admin, operator, and auditor users.
- Policy controls for tenant scope, country/incoterm allowlists, idempotency,
  and shared-table prohibition.

`cross_border_trade_ui_contract()` and
`cross_border_trade_ui_binding_contract()` expose:

- Workbench route: `/workbench/pbcs/cross_border_trade`.
- Panels for classifications, landed cost, export controls, declarations,
  compliance holds, rules, parameters, configuration, eventing, and dead
  letters.
- Binding evidence for owned tables, runtime event tables, workbench route, and
  zero shared-table access.

## Release Evidence

`build_release_evidence()` aggregates:

- Schema contract evidence.
- Service contract evidence.
- API contract evidence.
- Permissions evidence.
- UI/workbench binding evidence.
- Duplicate inbox/idempotency evidence.
- Retry and dead-letter evidence.
- Runtime smoke evidence.

Focused tests cover the local completeness slice only and verify the package
exports the hardened contract surface through `implementation_contract()`.

## Seed And Release Evidence

Release evidence includes package-local seed data for trade lanes, customs
statuses, duty treatments, restricted-party decision classes, document types,
and landed-cost reason codes. Generated packages validate those seed
descriptors with schema, migration, model, service, route, event, handler, UI,
RBAC, configuration, and release contracts.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `cross_border_trade`
- Mesh: `commerce`
- Datastore backend: `None`

### Owned Tables

- `hs_classification`
- `landed_cost_quote`
- `export_control_check`
- `customs_declaration`

### API Routes

- `POST /landed-cost`
- `POST /export-checks`
- `POST /declarations`

### Emitted Events

- `CustomsDeclarationPrepared`
- `LandedCostCalculated`

### Consumed Events

- `ProductClassified`
- `OrderPriced`

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
