# Price Promotion Engine PBC

`price_promotion_engine` is the AppGen-X packaged business capability for
dynamic price decisions, promotion design, loyalty-tier price effects, margin
controls, customer-segment pricing, forecast-aware quote optimization, and
promotion application evidence. It is a complete package-local implementation
with owned schema, runtime services, API descriptors, AppGen-X events,
idempotent handlers, rules, parameters, configuration, UI fragments, package
metadata, tests, and release evidence.

## Stable Identity

- PBC key: `price_promotion_engine`.
- Mesh: commerce.
- Package directory: `src/pyAppGen/pbcs/price_promotion_engine`.
- Runtime entrypoint: `price_promotion_engine_runtime_capabilities()`.
- UI entrypoint: `price_promotion_engine_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.price_promotion.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `price_rule`: tenant, SKU, region, currency, base price, cost, eligible
  segments, volume breaks, status, margin, and audit proof.
- `promotion`: tenant, code, discount percent, segment/region/currency
  eligibility, stackability, status, and audit proof.
- `loyalty_tier`: tenant, tier identity, rank, discount percent, status, and
  audit proof.
- `price_decision`: quote decision, customer, SKU, region, currency, quantity,
  selected promotions, loyalty tier, base and optimized price, extended price,
  margin, risk score, counterfactuals, status, applied promotions, and audit
  proof.

No customer, forecast, checkout, order, product, inventory, or finance tables
are shared or directly accessed. External context arrives through declared
AppGen-X events and API projections only:

- Consumed events: `CustomerSegmentUpdated` and `ForecastUpdated`.
- API projections: `customer_segment_projection`, `forecast_projection`, and
  `checkout_projection`.
- Runtime event tables are PBC-local:
  `price_promotion_engine_appgen_outbox_event`,
  `price_promotion_engine_appgen_inbox_event`, and
  `price_promotion_engine_dead_letter_event`.

The owned-boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer_segment`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary pricing and promotion capabilities
expected from a production commerce package:

- Price-rule catalog with tenant, SKU, region, currency, base price, cost,
  margin, eligible segments, volume breaks, status, and audit evidence.
- Promotion lifecycle with code, discount, segment/region/currency eligibility,
  stackability, status, exclusion-ready policy evidence, and audit proof.
- Loyalty-tier price effects with rank, discount percent, status, and
  tier-specific quote adjustments.
- Runtime configuration for database backend, event topic, retry limit,
  default currency, supported currencies, supported regions, pricing calendars,
  timezone, decision mode, and workbench limit.
- Parameter engine for margin floor, promotion stack limit, elasticity weight,
  forecast weight, segment weight, loyalty weight, risk review threshold,
  discount ceiling, decision TTL, and workbench limit.
- Rule engine for tenant, scope, allowed currencies, allowed regions, allowed
  segments, promotion policy, margin policy, status, compiled hash, and
  policy-engine evidence.
- Schema extension for owned price and promotion tables only, with versioned
  migration evidence.
- Idempotent AppGen-X handlers for `CustomerSegmentUpdated` and
  `ForecastUpdated`.
- Price quote service that selects active price rules, validates segment policy,
  calculates volume, promotion, and loyalty discounts, applies forecast
  adjustment, enforces discount ceilings, computes margin and risk, produces
  counterfactuals, and stores an owned decision.
- Promotion application service that validates eligibility and records applied
  promotions on the owned decision.
- `PriceOptimized` and `PromotionApplied` AppGen-X outbox emissions with retry
  policy and audit hash.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for price rules, promotions, loyalty tiers, decisions,
  approved decisions, average margin, rules, parameters, configuration, outbox,
  and dead letters.
- UI fragments for price-rule catalog, promotion designer, loyalty-tier manager,
  quote console, stacking board, forecast signals, segment pricing, decision
  ledger, rule studio, parameter console, configuration, outbox, and dead
  letters.
- Permission/RBAC descriptors for price, promotion, quote, event,
  configuration, and audit actions.
- Seed data for pricing calendars and promotion types.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for a modern
pricing PBC:

- Event-sourced pricing lifecycle with immutable state-event hashes.
- Owned pricing schema boundary enforcement with explicit violation evidence.
- Multi-tenant pricing isolation across rules, promotions, tiers, decisions,
  and UI views.
- Schema-evolution-safe price decision extensions.
- Dynamic price rule management with margin and volume-break controls.
- Promotion design with stack limits and eligibility filtering.
- Loyalty-tier price personalization.
- Forecast-aware quote optimization.
- Customer-segment pricing projections through declared events only.
- Probabilistic margin and promotion risk scoring.
- Counterfactual promotion margin simulation.
- Temporal decision TTL and pricing-calendar configuration.
- Dynamic price policy screening through compiled rules and parameters.
- Automated promotion control testing via smoke checks and release audits.
- Self-healing decision selection by deterministic active-rule choice and risk
  review routing.
- Cryptographic price decision proofs for rules, promotions, tiers, quotes, and
  outbox events.
- Immutable decision audit trail.
- Cross-system customer, forecast, and checkout federation through declared
  APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed pricing-model evidence through schema extensions and decision
  feature payloads.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_price_rule(command)`.
- `register_promotion(command)`.
- `register_loyalty_tier(command)`.
- `receive_event(event, simulate_failure=False)`.
- `quote_price(command)`.
- `apply_promotion(decision_id, promotion_id)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /price-rules` runs `register_price_rule`, writes `price_rule`,
  requires `price_promotion_engine.price.write`, and is idempotent by
  `price_rule_id`.
- `POST /promotions` runs `register_promotion`, writes `promotion`, requires
  `price_promotion_engine.promotion.write`, and is idempotent by
  `promotion_id`.
- `POST /loyalty-tiers` runs `register_loyalty_tier`, writes `loyalty_tier`,
  requires `price_promotion_engine.promotion.write`, and is idempotent by
  `tier_id`.
- `POST /price-quotes` runs `quote_price`, writes `price_decision`, requires
  `price_promotion_engine.quote`, emits `PriceOptimized`, and is idempotent by
  `decision_id`.
- `POST /promotion-applications` runs `apply_promotion`, updates
  `price_decision`, requires `price_promotion_engine.quote`, emits
  `PromotionApplied`, and is idempotent by `decision_id:promotion_id`.
- `POST /price-promotion/events/inbox` runs `receive_event`, consumes declared
  AppGen-X events, requires `price_promotion_engine.event.consume`, and is
  idempotent by `event_id`.
- `GET /price-decisions` queries `build_workbench_view`, reads only owned Price
  Promotion state, and requires `price_promotion_engine.audit`.

The catalog-facing route set remains `POST /price-quotes`, `POST /promotions`,
and `GET /price-decisions`.

## Events And Handlers

Consumed events:

- `CustomerSegmentUpdated`.
- `ForecastUpdated`.

Emitted events:

- `PriceOptimized`.
- `PromotionApplied`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, store customer-segment and forecast projections in package-local
state, and send simulated failures to the dead-letter evidence queue. Users
never choose a stream engine.

## UI And Workbench

The UI contract exposes:

- `PricePromotionWorkbench`.
- `PriceRuleCatalog`.
- `PromotionDesigner`.
- `LoyaltyTierManager`.
- `PriceQuoteConsole`.
- `PromotionStackingBoard`.
- `ForecastSignalPanel`.
- `SegmentPricingPanel`.
- `PriceDecisionLedger`.
- `PriceRuleStudio`.
- `PriceParameterConsole`.
- `PriceConfigurationPanel`.
- `PriceEventOutbox`.
- `PriceDeadLetterQueue`.

Rendered workbench output includes tenant-filtered price-rule, promotion,
loyalty-tier, decision, outbox, and dead-letter counts; visible and locked
actions from RBAC permissions; configuration/rule/parameter state; and
owned-table binding evidence.

## Release Evidence

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, price-rule, promotion,
  loyalty-tier, event handling, quote, promotion application, outbox emission,
  UI rendering, API descriptors, RBAC descriptors, and workbench evidence
  execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
