# Notifications PBC

`notifications` owns omnichannel communication orchestration for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, owned schema boundary, service commands, APIs, events, UI fragments, configuration, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `notification_template`, `delivery_channel`, `message_delivery`, `preference_snapshot`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.notifications.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Template management with required variables, localization, rendering, and audit proofs.
- Delivery channel registry for email, SMS, push, chat, provider health, cost, and failover.
- Preference snapshot projection from `PreferenceChanged` events.
- Trigger handling for `SlaBreached` and `WorkflowCompleted` events.
- Consent-aware message sending, channel routing, delivery attempts, status evidence, and failure handling.
- Emission of `MessageDelivered` and `MessageFailed` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced message lifecycle and immutable delivery audit trail.
- Probabilistic delivery, recipient-fatigue, channel-health, and urgency risk scoring.
- Counterfactual channel selection simulation and temporal delivery-window forecasting evidence.
- Autonomous delivery exception resolution and semantic message instruction understanding.
- Dynamic consent policy screening and automated communication control testing.
- Cross-system preference, workflow, and service federation through declared APIs/events only.
- Governed model evidence, cryptographic delivery proofs, and self-healing channel route selection.

## UI

The workbench exposes template designer, delivery channel console, message composer, preference snapshot panel, delivery status board, channel routing board, consent policy panel, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
