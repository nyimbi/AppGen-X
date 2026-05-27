# Checkout Processing

Package-local implementation contract for the Checkout Processing PBC. The package owns cart, session, promotion, handoff, risk, rule, parameter, configuration, inbox, outbox, and workbench evidence for checkout orchestration.

## Stable Identity

- PBC key: `checkout_processing`.
- Implementation directory: `src/pyAppGen/pbcs/checkout_processing`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_checkout_processing_runtime.py`.
- AppGen-X event topic: `appgen.checkout.events`.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not part of this PBC.

## Owned Datastore Boundary

The PBC owns these tables and generated artifacts:

- `cart`
- `cart_line`
- `checkout_session`
- `promotion_redemption`
- `checkout_pricing_handoff`
- `checkout_tax_handoff`
- `checkout_inventory_reservation_handoff`
- `checkout_payment_intent_handoff`
- `checkout_risk_screen`
- `checkout_address_validation`
- `checkout_rule`
- `checkout_parameter`
- `checkout_configuration`
- `checkout_processing_appgen_outbox_event`
- `checkout_processing_appgen_inbox_event`
- `checkout_processing_dead_letter_event`

Cross-PBC access is represented through declared APIs, events, or projections:

- Product and price projections consumed from `ProductPublished` and `PriceOptimized`.
- Tax quote projection consumed from `TaxCalculated`.
- Inventory reservation API dependency for reservation handoff.
- Payment intent API dependency for payment orchestration handoff.
- Optional customer projection for checkout personalization.
- No shared table reads or writes are allowed.

## Standard Capabilities

- Cart creation, currency/channel capture, tenant isolation, TTL parameter support, and immutable `CartOpened` events.
- Cart line management with product snapshot and price projection binding.
- Promotion redemption with compiled rule evidence, discount caps, campaign metadata, and deterministic idempotency.
- Address and shipping option validation using configured options and tenant rule policy.
- Checkout session lifecycle from initiated through ready, blocked, and completed states.
- Pricing, tax, inventory, payment, and risk handoff records under checkout-owned tables.
- Explicit inventory confirmation before order completion, recorded on the
  owned inventory reservation handoff.
- Fraud and checkout-risk scoring with clear, review, and block decisions.
- Payment intent creation, authorization, and capture using allowed methods and
  configured capture policy.
- Checkout completion with total verification, emitted completion event, and order handoff payload.
- AppGen-X inbox/outbox records with idempotency keys, retry attempts, and dead-letter evidence.
- Rule, parameter, and configuration engines with compiled hashes and explicit supported fields.
- Seed data for shipping options and payment methods.
- Workbench views for carts, sessions, promotions, eventing, rules, parameters, and configuration.
- Permissions for cart, checkout, pricing, promotion, inventory, payment, risk, event consumption, configuration, and audit actions.

## Advanced Capabilities

- Event-sourced checkout lifecycle with hash-chained events and projection rebuild evidence.
- Graph-relational cart topology evidence for cart, line, customer, payment, inventory, and session relationships.
- Multi-tenant isolation checks across carts, lines, sessions, rules, events, and workbench views.
- Schema extension for owned tables with validated field identifiers.
- Probabilistic conversion scoring and probabilistic checkout-risk scoring.
- Counterfactual promotion and fulfillment simulation.
- Temporal abandonment forecasting.
- Autonomous exception resolution for tax, inventory, payment, and risk failures.
- Semantic instruction parsing for coupons, shipping preference, and route preference.
- Predictive checkout risk scoring over behavioral and device inputs.
- Self-healing route selection across payment or checkout rails.
- Cryptographic checkout proof generation for selective disclosure.
- Immutable checkout audit trail and continuous control tests.
- Dynamic checkout policy screening for restricted destinations and blocked sessions.
- Cross-system checkout federation through projections and API references.
- Chaos-tolerant operation drills with retry and dead-letter topics.
- Crypto agility through rotatable signing epochs.
- Carbon-aware fulfillment option selection.
- Mathematical checkout path optimization and promotion allocation.
- Checkout anomaly detection with entropy evidence.
- Stochastic exposure modeling for checkout value-at-risk.
- Governed model registration with evidence URI, drift, and quality thresholds.

## Runtime Services

- `configure_runtime` validates backend, event topic, retry limit, currency, shipping options, payment methods, and stream-picker absence.
- `set_parameter` accepts only supported checkout parameters.
- `register_rule` compiles promotion, shipping, risk, and payment policy into stable evidence.
- `register_schema_extension` allows zero-downtime metadata only on owned tables.
- `receive_event` consumes AppGen-X events idempotently and dead-letters unsupported or malformed events.
- `create_cart` and `add_cart_line` own cart projection creation and recalculation.
- `apply_coupon` owns promotion redemption and discount evidence.
- `validate_shipping_address` owns address and shipping validation evidence.
- `open_checkout_session` creates checkout sessions and order handoff identifiers.
- `apply_pricing_handoff`, `apply_tax_handoff`, `reserve_inventory_handoff`, `screen_risk`, and `create_payment_intent` own checkout handoff records without sharing foreign tables.
- `confirm_inventory_reservation` changes the checkout-owned inventory handoff
  from reserved to confirmed.
- `authorize_payment_intent` and `capture_payment_intent` advance the owned
  payment handoff before completion.
- `complete_checkout` emits a completion event after pricing, tax, confirmed
  inventory, captured payment, and risk readiness.
- `build_api_contract` emits descriptor-level API metadata.
- `build_schema_contract` emits owned schema, relationships, model, and migration evidence for every owned checkout table, including AppGen-X inbox/outbox/dead-letter tables.
- `build_service_contract` emits command and query surface evidence for checkout orchestration and advanced analytics helpers.
- `build_release_evidence` combines schema, service, API, permission, and UI/workbench binding evidence into one package-local release contract.
- `permissions_contract` maps commands to action permissions.
- `verify_owned_table_boundary` rejects undeclared foreign table references.

## API Contract

- `POST /carts` maps to `create_cart`.
- `POST /cart-lines` maps to `add_cart_line`.
- `POST /coupons` maps to `apply_coupon`.
- `POST /checkout` maps to `open_checkout_session`.
- `POST /checkout/pricing` maps to `apply_pricing_handoff`.
- `POST /checkout/tax` maps to `apply_tax_handoff`.
- `POST /checkout/reservations` maps to `reserve_inventory_handoff`.
- `POST /checkout/reservations/confirmations` maps to `confirm_inventory_reservation`.
- `POST /checkout/risk` maps to `screen_risk`.
- `POST /checkout/payment-intents` maps to `create_payment_intent`.
- `POST /checkout/payment-intents/authorizations` maps to `authorize_payment_intent`.
- `POST /checkout/payment-intents/captures` maps to `capture_payment_intent`.
- `POST /checkout/completions` maps to `complete_checkout`.
- `POST /checkout-processing/events/inbox` maps to `receive_event`.
- `GET /checkout-workbench` maps to `build_workbench_view`.
- `GET /checkout/schema-contract` maps to `build_schema_contract`.
- `GET /checkout/service-contract` maps to `build_service_contract`.
- `GET /checkout/release-evidence` maps to `build_release_evidence`.

Every route descriptor states owned tables, required permission, idempotency key, emitted events, consumed events, and declared API or projection dependencies where applicable.

## Events

Emitted events:

- `OrderPriced`
- `CheckoutCompleted`

Consumed events:

- `ProductPublished`
- `PriceOptimized`
- `TaxCalculated`

Inbox handling is idempotent through event or semantic idempotency keys. Unsupported event types and missing-tenant payloads produce dead-letter records with retry evidence.

## Rules, Parameters, And Configuration

Rules require:

- `rule_id`
- `tenant`
- `scope`
- `status`
- `promotion_policy`
- `shipping_policy`
- `risk_policy`
- `payment_policy`

Parameters include cart TTL, session TTL, risk thresholds, retry attempts, promotion cap, shipping and carbon weights, abandonment horizon, route switch threshold, and workbench limit.

Configuration includes database backend, event topic, retry limit, default currency, default country, shipping options, payment methods, and workbench limit. The runtime records `event_contract: AppGen-X`, supported databases, and `user_eventing_choice: False`.

## UI And Workbench

Workbench fragments include:

- `CheckoutWorkbench`
- `CartConsole`
- `CartLineConsole`
- `CheckoutSessionConsole`
- `PromotionRedemptionStudio`
- `PricingTaxHandoffPanel`
- `InventoryReservationPanel`
- `PaymentIntentPanel`
- `RiskDecisionConsole`
- `AddressValidationPanel`
- `ShippingOptionMatrix`
- `CheckoutExceptionBoard`
- `CheckoutFederationView`
- `CheckoutRuleStudio`
- `CheckoutParameterConsole`
- `CheckoutConfigurationPanel`
- `InboxOutboxMonitor`

The workbench exposes only actions permitted by the principal and binds to owned data, declared projections, pricing/tax/inventory/payment handoff evidence, outbox, inbox, dead-letter, rule, parameter, configuration, and package-local contract evidence.

## Release Evidence

The focused test suite proves:

- Runtime smoke checks cover every standard and advanced capability key.
- The package declares owned tables, descriptor-level APIs, owned schema contract, service contract, and release evidence contract.
- Rules, parameters, configuration, schema extensions, and UI contracts are executable.
- Checkout flow completes across cart, coupon, address, session, pricing, tax, inventory, risk, payment, completion, outbox, and workbench steps.
- API contracts use fixed AppGen-X eventing and allowed relational backends only.
- Retry-first inbox handling produces retry evidence before dead-letter evidence, and dead-letter records stay package-owned.
- Boundary validation accepts owned tables and declared dependencies, then rejects direct foreign-table references.
- Invalid backend, wrong event topic, stream picker fields, unsupported parameters, invalid rules, unsupported events, and non-owned schema extensions fail.

## Read-Only Workbench Query Surface

- `GET /checkout-processing-workbench` maps to `query_checkout_processing_workbench` and exposes a read-only workbench/query contract for this command-heavy PBC.
- The query route has read-table scope only, emits no outbox event, requires no idempotency key, and remains inside the PBC-owned datastore boundary.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `checkout_processing`
- Mesh: `commerce`
- Datastore backend: `None`

### Owned Tables

- `cart`
- `cart_line`
- `checkout_session`
- `promotion_redemption`

### API Routes

- `POST /carts`
- `POST /checkout`
- `POST /coupons`

### Emitted Events

- `OrderPriced`
- `CheckoutCompleted`

### Consumed Events

- `ProductPublished`
- `PriceOptimized`
- `TaxCalculated`

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
