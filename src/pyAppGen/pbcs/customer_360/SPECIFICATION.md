# Customer 360 and Engagement Registry PBC Specification

## Scope

`customer_360` owns the unified customer profile and engagement registry for
AppGen-X composable applications. It manages customer identities, profile
attributes, account/contact relationships, consent, communication preferences,
touchpoints, engagement events, customer timelines, lifecycle state, loyalty and
service signals, segmentation projections, merge/unmerge evidence, privacy
controls, rules, parameters, configuration, and UI workbench fragments.

The PBC composes with order management, billing, service, loyalty, marketing,
notifications, identity, audit, and analytics PBCs through APIs, AppGen-X
events, and read-model projections only. It does not share tables with those
PBCs.

## Owned Boundary

Owned tables:

- `customer_profile`
- `customer_identity`
- `customer_relationship`
- `engagement_event`
- `communication_preference`
- `touchpoint`
- `consent_record`
- `customer_timeline`
- `customer_segment_projection`
- `profile_merge_case`
- `customer_rule`
- `customer_parameter`
- `customer_configuration`
- `customer_outbox`
- `customer_inbox`
- `customer_dead_letter`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing
uses the AppGen-X outbox/inbox event contract.

## Standard Capabilities

- Customer profile creation, lifecycle state, demographic/firmographic
  attributes, account/contact modeling, and tenant isolation.
- Identity resolution across email, phone, external IDs, device IDs, loyalty IDs,
  and verified credentials.
- Duplicate detection, merge case management, survivorship rules, and
  privacy-safe unmerge evidence.
- Consent, communication preferences, lawful basis, channel opt-in/opt-out,
  jurisdictional privacy controls, and preference-change events.
- Touchpoint capture across web, mobile, call center, store, email, service,
  order, payment, and support channels.
- Engagement event ingestion, channel history, customer timeline projection,
  recency/frequency/value metrics, sentiment, and churn/propensity signals.
- Customer read models for commerce, service, loyalty, notifications,
  segmentation, analytics, and audit consumers.
- Rules, parameters, configuration schema, permissions, seed data, idempotent
  handlers, retry/dead-letter evidence, and UI workbench fragments.

## Advanced Capabilities

- Event-sourced customer profile lifecycle with immutable hash-chained history.
- Graph-relational customer topology across identities, relationships,
  touchpoints, preferences, consents, segments, orders, payments, and service
  signals.
- Multi-tenant customer isolation with independently configurable rules,
  parameters, consent policies, and crypto epochs.
- Schema evolution through governed profile and preference extension
  registration.
- Probabilistic identity, churn, consent, and engagement risk scoring.
- Real-time profile analytics over timeline, RFM, consent, preference, and
  engagement health.
- Counterfactual preference, segmentation, and engagement simulation.
- Temporal customer value, churn, and engagement forecasting.
- Autonomous customer-data exception recommendation with auditable rationale.
- Semantic customer instruction parsing for contact-center and marketing text.
- Predictive customer health risk scoring and self-healing customer event route
  selection.
- Cryptographic customer-proof generation, immutable audit trails, dynamic
  privacy policy screening, and continuous control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  customer identity, resilience drills, crypto agility, carbon-aware customer
  processing, mathematical segment optimization, channel allocation, anomaly
  detection, stochastic customer exposure modeling, and governed customer models.

## APIs

- `POST /profiles`
- `POST /identities`
- `POST /relationships`
- `POST /preferences`
- `POST /consents`
- `POST /touchpoints`
- `POST /engagement-events`
- `POST /profile-merge-cases`
- `GET /customer-timeline`
- `GET /customer-read-models`
- `POST /customer-rules`
- `POST /customer-parameters`
- `POST /customer-configuration`

## Events

Emitted:

- `CustomerUpdated`
- `CustomerIdentityLinked`
- `PreferenceChanged`
- `ConsentRecorded`
- `TouchpointCaptured`
- `CustomerSegmentUpdated`

Consumed:

- `InvoiceIssued`
- `PaymentCaptured`
- `OrderVerified`
- `ServiceTicketClosed`
- `LoyaltyRewardEarned`
- `CandidateHired`

Handlers are idempotent through `customer_360:<EventType>:<event_id>` keys,
retry through the AppGen-X outbox adapter, and route exhausted failures to
`customer_360.dead_letter`.

## UI

The package exports a workbench UI contract with fragments for profile registry,
identity resolution, preference and consent management, touchpoint capture,
timeline analytics, relationship graph, merge review, segment projections,
rules, parameters, and configuration.
