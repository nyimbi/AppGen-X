# Checkout Processing

Package-local runtime slice for headless cart and checkout processing.

## Scope

- Owns `cart`, `cart_line`, `checkout_session`, and `promotion_redemption`.
- Exposes the catalog contract APIs: `POST /carts`, `POST /checkout`, `POST /coupons`.
- Emits `OrderPriced` and `CheckoutCompleted`.
- Consumes `ProductPublished`, `PriceOptimized`, and `TaxCalculated`.

## Runtime Surface

- Configuration is restricted to PostgreSQL, MySQL, or MariaDB.
- Eventing is fixed to the AppGen-X topic `appgen.checkout.events`.
- User-facing stream-engine or eventing mode selection is disallowed.
- Parameters are bounded to an explicit supported set.
- Rules require deterministic compiled hash and compiled evidence.

## Functional Coverage

- Cart creation and line management.
- Promotion redemption with deterministic evidence.
- Checkout session lifecycle and immutable event history.
- Pricing, tax, inventory reservation, payment intent, and fraud/risk handoffs.
- Address and shipping option validation with tenant isolation.
- Inbox/outbox eventing, idempotent handling, retry and dead-letter evidence.
- Workbench/UI evidence for configuration, rule, and parameter bindings.

## Advanced Coverage

- Event-sourced checkout lifecycle.
- Graph-relational cart/session topology.
- Conversion and risk scoring.
- Counterfactual promotion and fulfillment simulation.
- Abandonment forecasting.
- Autonomous exception resolution.
- Semantic checkout instruction parsing.
- Self-healing route selection.
- Cryptographic checkout proof and immutable audit trail.
- Dynamic policy screening and automated control testing.
- Cross-system federation across product, pricing, tax, payment, and inventory.
- Chaos tolerance, crypto agility, carbon-aware option selection, mathematical optimization, promotion allocation, anomaly detection, stochastic exposure modeling, and governed ML evidence.
