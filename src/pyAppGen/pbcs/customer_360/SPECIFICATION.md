# Customer 360 and Engagement Registry PBC Specification

## Scope

`customer_360` owns the unified customer profile and engagement registry for
AppGen-X composable applications. It manages customer identities, profile
attributes, account and contact relationships, consent, communication
preferences, touchpoints, engagement events, customer timelines, lifecycle
state, loyalty and service signals, segmentation projections, merge evidence,
privacy controls, rules, parameters, configuration, and workbench fragments.

The PBC composes with order management, billing, service, loyalty,
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

Runtime event tables:

- `customer_360_appgen_outbox_event`
- `customer_360_appgen_inbox_event`
- `customer_360_dead_letter_event`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Runtime
configuration requires the fixed AppGen-X event topic
`appgen.customer.events`, exposes `visible_event_contracts: ("AppGen-X",)`,
and keeps `stream_engine_picker_visible: false`. Any user-facing stream-engine
picker, alternate event transport selector, or other event-contract override is
rejected.

## Standard Capabilities

- Customer profile creation, lifecycle state, demographic and firmographic
  attributes, account and contact modeling, and tenant isolation.
- Identity resolution across email, phone, external IDs, device IDs, loyalty
  IDs, and verified credentials.
- Duplicate detection, merge case management, survivorship rules, and
  privacy-safe merge evidence.
- Consent, communication preferences, lawful basis, channel opt-in and opt-out,
  jurisdictional privacy controls, and preference-change events.
- Touchpoint capture across web, mobile, store, email, service, order,
  payment, and support channels.
- Engagement event ingestion, channel history, customer timeline projection,
  recency, frequency, and value metrics, sentiment, and churn signals.
- Customer read models for commerce, billing, service, loyalty, notification,
  segmentation, analytics, and audit consumers.
- Rules, parameters, configuration schema, AppGen-X inbox and outbox evidence,
  idempotent handlers, retry and dead-letter evidence, permissions, owned-table
  boundary enforcement, and workbench fragments.

## Advanced Capabilities

- Event-sourced customer profile lifecycle with immutable hash-chained history.
- Graph-relational customer topology across identities, relationships,
  touchpoints, preferences, consents, segments, and service signals.
- Multi-tenant customer isolation with independently configurable rules,
  parameters, consent policies, and crypto epochs.
- Schema evolution through governed profile and preference extension
  registration limited to owned tables.
- Probabilistic identity, churn, consent, and engagement scoring.
- Real-time profile analytics over timeline, RFM, consent, preference, and
  engagement health.
- Counterfactual preference, segmentation, and engagement simulation.
- Temporal customer value, churn, and engagement forecasting.
- Autonomous customer-data exception recommendation with auditable rationale.
- Semantic customer instruction parsing for contact-center and marketing text.
- Predictive customer health scoring and self-healing customer event route
  selection.
- Cryptographic customer-proof generation, immutable audit trails, dynamic
  privacy policy screening, and continuous control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  customer identity, resilience drills, crypto agility, carbon-aware customer
  processing, mathematical segment optimization, channel allocation, anomaly
  detection, stochastic customer exposure modeling, and governed customer
  models.

## Configuration, Rules, and Parameters

Configuration requires:

- `database_backend`
- `event_topic`
- `retry_limit`
- `allowed_channels`
- `allowed_regions`
- `allowed_identity_types`
- `default_timezone`
- `workbench_limit`

Supported parameters are:

- `identity_match_threshold`
- `churn_risk_threshold`
- `engagement_decay_days`
- `minimum_consent_confidence`
- `timeline_limit`
- `retention_days`
- `workbench_limit`

Rules require:

- `rule_id`
- `tenant`
- `rule_type`
- `allowed_channels`
- `required_consents`
- `status`

Rules compile into deterministic hashes and emit compiled evidence containing
the required field set and resolved scope. This evidence is surfaced through the
runtime workbench and UI contract.

## APIs, Events, and Handlers

The descriptor API contract exposes command routes for creating customer
profiles, linking identities, recording consents, setting preferences,
capturing touchpoints, ingesting engagement events, opening and resolving merge
cases, and receiving AppGen-X inbox events. Query routes expose the customer
timeline and read-model surface. Every route is a descriptor with a command or
query, owned table, and permission.

The API contract declares:

- `event_contract: AppGen-X`
- `required_event_topic: appgen.customer.events`
- `stream_engine_picker_visible: false`
- `user_selectable_event_contract: false`
- `shared_table_access: false`
- owned tables, runtime tables, supported database backends, emitted events,
  consumed events, and declared dependency projections and API reads

Emitted events are:

- `CustomerUpdated`
- `CustomerIdentityLinked`
- `PreferenceChanged`
- `ConsentRecorded`
- `TouchpointCaptured`
- `CustomerSegmentUpdated`
- `ProfileMergeCaseOpened`
- `ProfileMergeResolved`

Consumed events are:

- `InvoiceIssued`
- `PaymentCaptured`
- `OrderVerified`
- `ServiceTicketClosed`
- `LoyaltyRewardEarned`
- `CandidateHired`

`receive_event` uses `event_id` or the supplied idempotency key to maintain
exactly-once handler evidence in the inbox. Processed events update package
local projection buckets only. Unsupported or failed events append retry
evidence until the configured retry limit is reached, then move to the package
dead-letter table with preserved handler evidence.

## Permissions and UI Contract

The permissions contract maps actions to AppGen-X permissions such as:

- `customer_360.read`
- `customer_360.profile`
- `customer_360.consent`
- `customer_360.engage`
- `customer_360.merge`
- `customer_360.configure`
- `customer_360.event`
- `customer_360.audit`

Roles include admin, analyst, operator, and auditor. ABAC attributes include
tenant, region, profile ID, channel, and lifecycle state. Policy controls
declare shared-table access forbidden and the stream-engine picker hidden.

The package-local UI contract exposes the customer workbench, profile registry,
identity resolution panel, consent and preference center, touchpoint capture
console, engagement timeline, relationship graph, merge review, segment
dashboard, rule studio, parameter console, and configuration panel.

Workbench and render evidence include:

- visible and locked actions
- configuration binding details including AppGen-X and the hidden stream picker
- compiled rule evidence
- supported and active parameters
- owned tables and runtime event table bindings
- outbox, inbox, and dead-letter counts

## Boundary and Release Evidence

`register_schema_extension` accepts only owned tables. Foreign tables raise an
owned-table validation error, while malformed field names return structured
validation evidence.

`verify_owned_table_boundary` accepts only:

- package-owned business tables
- package runtime event tables
- declared consumed event types
- declared dependency projections
- declared dependency API routes
- names prefixed with `customer_360_`

Foreign tables are reported as violations. This proves cross-PBC integration
through APIs, projections, and AppGen-X events rather than shared datastore
access.

The package implementation contract exports package metadata for:

- owned tables
- allowed database backends
- required event topic
- emitted and consumed events
- descriptor API contract
- permissions contract
- boundary contract
- UI contract
- advanced runtime capabilities

Release evidence requires runtime smoke success, standard feature coverage,
advanced capability coverage, package-local API and permissions contracts, UI
binding evidence, idempotent receive-event tests, retry and dead-letter tests,
owned-table-only boundary tests, and focused unit coverage for both standard and
advanced customer workflows.
