# Cross Border Trade PBC

`cross_border_trade` is the AppGen-X packaged business capability for
cross-border product classification, landed-cost calculation, export-control
screening, customs declaration execution, and trade-governance evidence. It is
a complete package-local implementation with owned schema, runtime services,
descriptor contracts, AppGen-X events, idempotent handlers, rules, parameters,
configuration, UI fragments, tests, and release evidence.

## Stable Identity

- PBC key: `cross_border_trade`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/cross_border_trade`.
- Runtime entrypoint: `cross_border_trade_runtime_capabilities()`.
- UI entrypoint: `cross_border_trade_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.cross_border_trade.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `hs_classification`: tenant, product, description, origin, destination,
  confidence, review status, evidence hash, and classification facts.
- `landed_cost_quote`: tenant, order, classification, incoterm, origin,
  destination, duty/tax inputs, landed total, currency, and evidence hash.
- `export_control_check`: tenant, order, classification, counterparties,
  destination risk, decision, review status, and evidence hash.
- `customs_declaration`: tenant, order, quote, export-control check,
  documents, broker route, filing status, topology degree, and evidence hash.

No ERP, customer, inventory, payment, shipment, broker, or customs gateway
tables are shared or directly accessed. External context arrives only through
declared AppGen-X events and API projections:

- Consumed events: `OrderPlaced`, `InventoryReserved`, `PaymentCaptured`, and
  `ShipmentDispatched`.
- API projections: `order_projection`, `inventory_projection`,
  `payment_projection`, and `logistics_projection`.
- Runtime event tables are PBC-local:
  `cross_border_trade_appgen_outbox_event`,
  `cross_border_trade_appgen_inbox_event`, and
  `cross_border_trade_dead_letter_event`.

The owned-boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local runtime event tables. It rejects direct
foreign references such as `customer_master`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary cross-border trade capabilities expected
from a production package:

- Runtime configuration for database backend, event topic, retry limit,
  default currency, supported countries, supported incoterms, and workbench
  limit.
- Parameter engine for classification confidence, restricted-party review,
  duty variance tolerance, de minimis value, broker routing weights, forecast
  horizon, and workbench limit.
- Rule engine for tenant, scope, classification policy, landed-cost policy,
  export-control policy, declaration policy, compiled hash, and governance
  evidence.
- Schema extension support for owned trade tables only, with migration evidence
  and projection rebuild status.
- Idempotent AppGen-X handlers for order, inventory, payment, and shipment
  events.
- HS classification with confidence scoring, keyword-based review routing, and
  immutable evidence hashes.
- Landed-cost quote generation across goods value, shipping, duty, tax,
  insurance, broker fee, incoterm, and currency.
- Export-control screening for destination risk, restricted-party review,
  license triggers, and blocked destinations.
- Customs declaration filing with required-document validation, broker route
  selection, and declaration status evidence.
- Retry and dead-letter evidence for unsupported or exhausted consumed-event
  handling.
- Workbench views for classifications, quotes, export-control checks,
  declarations, rules, parameters, configuration, outbox, inbox, and dead
  letters.
- UI fragments for classification, landed cost, export controls, declarations,
  broker submission, document evidence, topology, exposure, exceptions, rules,
  parameters, configuration, eventing, and dead letters.
- Permission/RBAC descriptors for trade execution, event consumption,
  configuration, and audit actions.
- Seed data for incoterms, broker candidates, and owned-table bindings.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for a modern
trade-governance PBC:

- Event-sourced trade lifecycle with immutable state-event hashes.
- Owned trade schema boundary enforcement with explicit violation evidence.
- Multi-tenant trade isolation across classifications, quotes, checks,
  declarations, and workbench views.
- Schema-evolution-safe declaration extensions for owned trade tables.
- Graph-relational trade topology across order, classification, quote,
  export-control check, broker route, and declaration.
- Counterfactual landed-cost simulation and mathematical landed-cost
  optimization.
- Temporal duty/tax forecasting and stochastic trade exposure modeling.
- Autonomous trade exception resolution evidence.
- Semantic trade-document parsing for order, SKU, origin, destination, and
  incoterm extraction.
- Predictive export-control risk scoring and governed model evidence.
- Dynamic trade-policy screening and automated trade-control testing.
- Cross-system order, inventory, payment, and logistics federation through
  declared projections only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence and permissions governance evidence.
- Carbon-aware broker routing, broker-allocation mechanism design, crypto
  agility, cryptographic trade proofs, and immutable audit trail evidence.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(parameter_name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(entity, fields)`.
- `receive_event(event)`.
- `classify_product(command)`.
- `quote_landed_cost(command)`.
- `screen_export_control(command)`.
- `file_customs_declaration(command)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /trade/classifications` runs `classify_product`, writes
  `hs_classification`, emits `HSClassified`, requires
  `cross_border_trade.classify`, and is idempotent by `classification_id`.
- `POST /trade/landed-cost-quotes` runs `quote_landed_cost`, writes
  `landed_cost_quote`, emits `LandedCostQuoted`, requires
  `cross_border_trade.quote`, and is idempotent by `quote_id`.
- `POST /trade/export-control-checks` runs `screen_export_control`, writes
  `export_control_check`, emits `ExportControlCleared`, requires
  `cross_border_trade.screen`, and is idempotent by `check_id`.
- `POST /trade/customs-declarations` runs `file_customs_declaration`, writes
  `customs_declaration`, emits `CustomsDeclarationFiled`, requires
  `cross_border_trade.declare`, and is idempotent by `declaration_id`.
- `POST /cross-border-trade/events/inbox` runs `receive_event`, consumes
  declared AppGen-X events, requires `cross_border_trade.event.consume`, and
  is idempotent by `event_id`.
- `GET /trade/workbench` queries `build_workbench_view`, reads only owned
  Cross Border Trade state, and requires `cross_border_trade.audit`.

The catalog-facing route set remains `POST /trade/classifications`,
`POST /trade/customs-declarations`, and `GET /trade/workbench`.

## Events And Handlers

Consumed events:

- `OrderPlaced`.
- `InventoryReserved`.
- `PaymentCaptured`.
- `ShipmentDispatched`.

Emitted events:

- `HSClassified`.
- `LandedCostQuoted`.
- `ExportControlCleared`.
- `CustomsDeclarationFiled`.

Handlers require event IDs and idempotency keys, reject unsupported event
types, dead-letter exhausted retries, record inbox evidence, and translate
external order/inventory/payment/shipment payloads into owned trade context.
Users never choose a stream engine.

## UI And Workbench

The UI contract exposes:

- Cross Border Trade workbench.
- HS classification console.
- Landed-cost quote workbench.
- Export-control screening panel.
- Customs declaration console.
- Broker submission board.
- Trade document evidence panel.
- Trade topology graph.
- Duty/tax exposure panel.
- Trade exception resolution board.
- Trade rule studio.
- Trade parameter console.
- Trade configuration panel.
- Trade eventing monitor.
- Trade dead-letter queue.

Rendered workbench output includes tenant-filtered classification, quote,
export-control, declaration, outbox, inbox, and dead-letter counts; visible
and locked actions from RBAC permissions; configuration/rule/parameter state;
and owned-table binding evidence including local AppGen-X runtime event tables.

## Release Evidence

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, event-handling,
  classification, landed-cost quote, export-control screen, customs
  declaration, outbox emission, UI rendering, API descriptors, RBAC
  descriptors, and workbench evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid event topics, forbidden eventing-choice
  fields, invalid parameters, non-owned schema extensions, and unsupported
  event types are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
