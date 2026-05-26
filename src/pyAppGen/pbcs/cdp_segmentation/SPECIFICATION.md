# CDP Segmentation PBC

`cdp_segmentation` is the AppGen-X packaged business capability for customer
event ingestion, profile property stitching, identity evidence, consent-aware
segment definition, real-time membership evaluation, activation evidence, and
customer-audience intelligence. It is a complete package-local implementation
with owned schema, runtime services, API descriptors, AppGen-X events,
idempotent handlers, rules, parameters, configuration, UI fragments, package
metadata, tests, and release evidence.

## Stable Identity

- PBC key: `cdp_segmentation`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/cdp_segmentation`.
- Runtime entrypoint: `cdp_segmentation_runtime_capabilities()`.
- UI entrypoint: `cdp_segmentation_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.cdp_segmentation.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `customer_event`: tenant, customer, event type, region, event properties,
  identity keys, source evidence, and audit proof.
- `profile_property`: tenant, customer, property name, value, source,
  consent/identity evidence, and audit proof.
- `segment_definition`: tenant, segment name, criteria, activation policy,
  status, compiled hash, and governance evidence.
- `segment_membership`: tenant, segment, customer, score, status, evaluation
  proof, and activation evidence.

No customer master, payment, order, shipment, marketing, activation, promotion,
or loyalty tables are shared or directly accessed. External context arrives
through declared AppGen-X events and API projections only:

- Consumed events: `CustomerUpdated`, `PaymentCaptured`, and `OrderShipped`.
- API projections: `customer_projection`, `payment_projection`,
  `order_projection`, and `activation_destination_projection`.
- Runtime event tables are PBC-local:
  `cdp_segmentation_appgen_outbox_event`,
  `cdp_segmentation_appgen_inbox_event`, and
  `cdp_segmentation_dead_letter_event`.

The boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary CDP and segmentation capabilities
expected from a production audience package:

- Customer event ingestion for profile, payment, shipment, and engagement
  event types with tenant, customer, region, properties, and audit proof.
- Runtime configuration for database backend, event topic, retry limit,
  default region, supported regions, supported event types, identity keys,
  timezone, activation mode, and workbench limit.
- Parameter engine for membership threshold, profile merge confidence, event
  freshness, payment value weight, order recency weight, engagement weight,
  consent risk, activation batch limit, max segments per profile, and workbench
  limit.
- Rule engine for tenant, scope, allowed event types, allowed regions, segment
  policy, consent policy, activation policy, status, compiled hash, and
  policy-engine evidence.
- Schema extension for owned CDP tables only, with versioned migration
  evidence.
- Idempotent AppGen-X handlers for `CustomerUpdated`, `PaymentCaptured`, and
  `OrderShipped`.
- Profile property upsert and profile stitching from incoming events.
- Segment definition with compiled criteria.
- Segment evaluation that calculates membership score, writes owned membership
  state, and emits `CustomerSegmentUpdated` for qualifying members.
- Profile enrichment emission through `ProfileEnriched`.
- Segment activation evidence with member counts.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for customer events, profiles, segment definitions,
  memberships, active memberships, rules, parameters, configuration, outbox,
  and dead letters.
- UI fragments for event stream, profile properties, segment builder,
  membership board, activation console, consent policy, identity stitching,
  rule studio, parameter console, configuration, outbox, and dead-letter queue.
- Permission/RBAC descriptors for event, segment, membership evaluation, event
  consumption, configuration, and audit actions.
- Seed data for supported event types and activation destinations.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for a modern CDP
PBC:

- Event-sourced profile lifecycle with immutable state-event hashes.
- Owned CDP schema boundary enforcement with explicit violation evidence.
- Multi-tenant audience isolation across events, properties, segments,
  memberships, and UI views.
- Schema-evolution-safe profile context extensions.
- Real-time profile stitching from event payload properties.
- Consent-aware segmentation through rule and parameter evidence.
- Probabilistic affinity, lifecycle, and membership scoring.
- Counterfactual segment-membership simulation through deterministic scoring
  previews.
- Temporal audience forecasting evidence through event freshness and activation
  limits.
- Autonomous audience exception resolution evidence through dead-letter and
  policy controls.
- Semantic segment-rule understanding through compiled criteria.
- Dynamic consent policy screening.
- Automated data-quality control testing via smoke checks and release audits.
- Self-healing profile merge evidence through idempotent profile-property
  upserts.
- Cryptographic profile proofs for events, properties, segments, memberships,
  and outbox events.
- Immutable profile audit trail.
- Cross-system customer, payment, order, and activation federation through
  declared APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed model evidence through schema extensions and scoring parameters.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `receive_event(event, simulate_failure=False)`.
- `ingest_customer_event(command)`.
- `upsert_profile_property(command)`.
- `define_segment(command)`.
- `evaluate_segments(customer_id)`.
- `activate_segment(segment_id)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /events` runs `ingest_customer_event`, writes `customer_event` and
  `profile_property`, requires `cdp_segmentation.event.write`, and is
  idempotent by `event_id`.
- `POST /profile-properties` runs `upsert_profile_property`, writes
  `profile_property`, requires `cdp_segmentation.event.write`, and is
  idempotent by `property_id`.
- `POST /segments` runs `define_segment`, writes `segment_definition`,
  requires `cdp_segmentation.segment.write`, and is idempotent by `segment_id`.
- `POST /segment-evaluations` runs `evaluate_segments`, writes
  `segment_membership`, requires `cdp_segmentation.membership.evaluate`, emits
  segment and enrichment events, and is idempotent by `customer_id`.
- `POST /segment-activations` runs `activate_segment`, reads owned segment and
  membership state, requires `cdp_segmentation.membership.evaluate`, and is
  idempotent by `segment_id`.
- `POST /cdp-segmentation/events/inbox` runs `receive_event`, consumes
  declared AppGen-X events, requires `cdp_segmentation.event.consume`, and is
  idempotent by `event_id`.
- `GET /memberships` queries `build_workbench_view`, reads only owned CDP
  Segmentation state, and requires `cdp_segmentation.audit`.

The catalog-facing route set remains `POST /events`, `POST /segments`, and
`GET /memberships`.

## Events And Handlers

Consumed events:

- `CustomerUpdated`.
- `PaymentCaptured`.
- `OrderShipped`.

Emitted events:

- `CustomerSegmentUpdated`.
- `ProfileEnriched`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, translate external events into owned customer events and profile
properties, and send simulated failures to the dead-letter evidence queue.
Users never choose a stream engine.

## UI And Workbench

The UI contract exposes:

- Customer event stream.
- Profile property panel.
- Segment definition builder.
- Membership evaluation board.
- Activation console.
- Consent policy panel.
- Identity stitching panel.
- CDP rule studio.
- CDP parameter console.
- CDP configuration panel.
- CDP event outbox.
- CDP dead-letter queue.

Rendered workbench output includes tenant-filtered event, profile, segment,
membership, active-membership, outbox, and dead-letter counts; visible and
locked actions from RBAC permissions; configuration/rule/parameter state; and
owned-table binding evidence.

## Release Evidence

`cdp_segmentation_build_schema_contract()` emits the generated CDP-owned schema
plan for customer events, identity links, stitched profiles, profile
properties, consent, enrichment, segment definitions/rules/versions,
memberships, evaluations, activation destinations and runs, audience snapshots
and forecasts, affinity and lifecycle risk scores, merge candidates, profile
exceptions, data-quality findings, consent policy screenings, customer/payment
order/notification/loyalty/pricing projections, profile proofs, audit entries,
control assertions, federation views, resilience drills, crypto epochs, carbon
activation windows, segment simulations, activation allocations, anomaly and
exposure forecasts, identity attestations, governed models, seed data,
configuration/rule/parameter tables, and AppGen-X inbox/outbox/dead-letter
tables. Every table receives deterministic migration and generated model
descriptors under `pbcs/cdp_segmentation/`.

`cdp_segmentation_build_service_contract()` declares the generated app service
surface for configuration, parameters, rules, schema extension, AppGen-X inbox
handling, event ingestion, profile property upsert, segment definition,
membership evaluation, activation, workbench queries, boundary validation,
audience simulation and forecasting, exception resolution, semantic rule
parsing, lifecycle risk, profile merge healing, profile proof generation,
consent screening, data quality controls, customer federation, activation
allocation, anomaly detection, and governed model registration.

`cdp_segmentation_build_release_evidence()` proves owned-schema depth, one
model/migration descriptor per owned table, broad service coverage, AppGen-X
eventing only, relational backend allowlist compliance, permission coverage for
descriptor queries, owned runtime event tables, and no shared-table access.

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Schema, service, and release-evidence descriptors pass.
- Configuration, rule, parameter, schema-extension, event ingestion, consumed
  event handling, segment definition, segment evaluation, activation, outbox
  emission, UI rendering, API descriptors, RBAC descriptors, and workbench
  evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
