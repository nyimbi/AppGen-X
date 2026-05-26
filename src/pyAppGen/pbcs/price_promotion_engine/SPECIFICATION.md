# Price Promotion Engine PBC

`price_promotion_engine` owns dynamic price decisions, promotions, loyalty tier price effects, and quote evidence for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, owned schema boundary, service commands, APIs, events, UI fragments, configuration, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `price_rule`, `promotion`, `loyalty_tier`, `price_decision`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.price_promotion.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Price rule catalog with currency, region, segment, cost, base price, and volume break controls.
- Promotion lifecycle with eligibility, stacking limits, exclusion rules, and redemption evidence.
- Loyalty tier management with tier discounts and customer-segment personalization.
- Price quote service with margin floor checks, demand forecast adjustment, counterfactual evidence, and decision audit proofs.
- Consumption of `CustomerSegmentUpdated` and `ForecastUpdated` with idempotent handlers.
- Emission of `PriceOptimized` and `PromotionApplied` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced pricing lifecycle and immutable decision trail.
- Probabilistic margin, elasticity, demand, and promotion risk scoring.
- Counterfactual promotion margin simulation and temporal price effectivity forecasting.
- Dynamic price policy screening and automated promotion control testing.
- Cross-system customer, forecast, and checkout federation through declared APIs/events only.
- Governed model evidence, cryptographic price decision proofs, and self-healing decision selection.

## UI

The workbench exposes price rule catalog, promotion designer, loyalty tier manager, price quote console, promotion stacking board, forecast signal panel, segment pricing panel, decision ledger, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
