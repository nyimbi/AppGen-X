# CDP Segmentation PBC

`cdp_segmentation` owns customer event ingestion, profile properties, segment definitions, real-time membership evaluation, and activation evidence for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, owned schema boundary, service commands, APIs, events, UI fragments, configuration, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `customer_event`, `segment_definition`, `segment_membership`, `profile_property`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.cdp_segmentation.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Customer event ingestion for profile, payment, shipment, and engagement events.
- Profile property stitching, identity-key evidence, consent policy, and enrichment.
- Segment definition management with compiled criteria and activation policies.
- Real-time membership evaluation, membership scoring, and segment activation.
- Idempotent consumption of `CustomerUpdated`, `PaymentCaptured`, and `OrderShipped`.
- Emission of `CustomerSegmentUpdated` and `ProfileEnriched` through the AppGen-X outbox.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced profile lifecycle and immutable profile audit trail.
- Probabilistic affinity, consent, lifecycle, and membership scoring.
- Counterfactual segment-membership simulation and temporal audience forecasting evidence.
- Autonomous audience exception resolution and semantic segment-rule understanding.
- Dynamic consent policy screening and automated data-quality control testing.
- Cross-system customer, payment, and order federation through declared APIs/events only.
- Governed model evidence, cryptographic profile proofs, and self-healing profile merge evidence.

## UI

The workbench exposes customer event stream, profile property panel, segment definition builder, membership evaluation board, activation console, consent policy panel, identity stitching panel, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
