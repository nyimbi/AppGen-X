# Subscription Billing PBC

`subscription_billing` owns recurring-revenue subscription operations for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, schema boundary, service commands, API/event contracts, UI fragments, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `subscription`, `usage_meter`, `billing_schedule`, `dunning_notice`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.subscription.events`; no user-facing stream-engine selection.

## Runtime Capabilities

- Plan catalog and rate schedule registration.
- Subscription activation, renewal, review, and lifecycle evidence.
- Usage metering, optimized usage rates, invoice approval, deferred-revenue handoff, tax handoff, and entitlement handoff.
- Dunning notices with retry/dead-letter evidence.
- Configurable rule, parameter, and schema-extension engines.
- Idempotent handlers for `PaymentCaptured` and `PriceOptimized`.
- Advanced runtime evidence for event sourcing, tenant isolation, probabilistic risk scoring, counterfactual proration, governed model evidence, cryptographic audit proofs, policy enforcement, and chaos-tolerant AppGen-X eventing.

## UI

The workbench exposes subscription registry, plan designer, usage console, invoice approval, renewal console, dunning board, entitlement handoff, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
