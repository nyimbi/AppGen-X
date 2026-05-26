# Lead Opportunity PBC

`lead_opportunity` owns revenue pipeline intake, qualification, account hierarchy, opportunity execution, activity history, and forecast evidence for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, owned schema boundary, service commands, APIs, events, UI fragments, configuration, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `lead`, `opportunity`, `account_hierarchy`, `sales_activity`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.lead_opportunity.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Lead capture, deduplication, scoring, qualification, and nurture routing.
- Account hierarchy management with parent-child account structure and owner assignment.
- Opportunity creation from qualified leads, stage advancement, win capture, and pipeline rollup.
- Sales activity timeline with sentiment, next-best-action, and immutable activity evidence.
- Customer segment projection handling through idempotent `CustomerSegmentUpdated` handlers.
- Emission of `LeadQualified`, `OpportunityWon`, and `CustomerUpdated` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced revenue lifecycle and immutable pipeline audit trail.
- Probabilistic win likelihood, deal slippage, and forecast confidence scoring.
- Counterfactual deal-velocity simulation and temporal pipeline forecasting.
- Autonomous next-best-action generation and semantic interaction understanding evidence.
- Dynamic sales policy screening and automated revenue control testing.
- Cross-system customer, segment, and billing federation through declared APIs/events only.
- Governed model evidence, cryptographic pipeline proofs, and self-healing assignment evidence.

## UI

The workbench exposes lead inbox, account hierarchy map, qualification board, opportunity pipeline, sales activity timeline, forecast rollup, next-best-action panel, customer segment projection panel, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
