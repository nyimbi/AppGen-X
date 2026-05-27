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
- `simulate_segment_membership(command)`.
- `forecast_audience(command)`.
- `resolve_audience_exception(command)`.
- `parse_segment_rule(command)`.
- `score_lifecycle_risk(command)`.
- `heal_profile_merge(command)`.
- `generate_profile_proof(command)`.
- `screen_consent_policy(command)`.
- `run_data_quality_controls(tenant)`.
- `federate_customer_view(command)`.
- `allocate_activation(command)`.
- `detect_profile_anomaly(command)`.
- `register_governed_model(command)`.
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
- `POST /segment-simulations` runs counterfactual segment scoring and writes
  `segment_simulation`.
- `POST /audience-forecasts` writes audience forecast, snapshot, and exposure
  forecast evidence.
- `POST /profile-exceptions/resolve` records resolved audience/profile
  exceptions with audit evidence.
- `POST /segment-rules/parse` compiles semantic segment text into owned
  segment-rule criteria.
- `POST /lifecycle-risk-scores` writes lifecycle risk and affinity score
  evidence.
- `POST /profile-merges/heal` writes merge candidate, identity stitch, and
  identity attestation evidence.
- `POST /profile-proofs` writes cryptographic profile proof evidence.
- `POST /consent-policy-screenings` writes consent screening and consent state.
- `POST /data-quality-controls` writes quality findings and control
  assertions.
- `POST /customer-federation-views` writes customer/payment/order federation
  view projections without shared-table access.
- `POST /activation-allocations` writes activation allocation, run, delivery,
  destination, and downstream projection readiness evidence.
- `POST /profile-anomaly-signals` writes anomaly signal evidence.
- `POST /governed-models` writes governed model, crypto epoch, resilience
  drill, and carbon activation window evidence.
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

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `cdp_segmentation`
- Mesh: `relationship`
- Datastore backend: `postgresql`

### Owned Tables

- `customer_event`
- `event_identity_link`
- `identity_stitch`
- `profile`
- `profile_property`
- `profile_consent`
- `profile_enrichment`
- `segment_definition`
- `segment_rule`
- `segment_version`
- `segment_membership`
- `membership_evaluation`
- `activation_destination`
- `activation_run`
- `activation_delivery`
- `audience_snapshot`
- `audience_forecast`
- `affinity_score`
- `lifecycle_risk_score`
- `merge_candidate`
- `profile_exception`
- `data_quality_finding`
- `consent_policy_screening`
- `customer_projection`
- `payment_projection`
- `order_projection`
- `notification_projection`
- `loyalty_projection`
- `pricing_projection`
- `profile_proof`
- `profile_audit_entry`
- `cdp_control_assertion`
- `cdp_federation_view`
- `cdp_resilience_drill`
- `cdp_crypto_epoch`
- `carbon_activation_window`
- `segment_simulation`
- `activation_allocation`
- `profile_anomaly_signal`
- `audience_exposure_forecast`
- `identity_attestation`
- `cdp_governed_model`
- `cdp_seed_data`
- `cdp_segmentation_rule`
- `cdp_segmentation_parameter`
- `cdp_segmentation_configuration`
- `cdp_segmentation_appgen_outbox_event`
- `cdp_segmentation_appgen_inbox_event`
- `cdp_segmentation_dead_letter_event`

### API Routes

- `POST /events`
- `POST /profile-properties`
- `POST /segments`
- `POST /segment-evaluations`
- `POST /segment-activations`
- `POST /cdp-segmentation/events/inbox`
- `GET /memberships`
- `GET /cdp-segmentation/schema-contract`
- `GET /cdp-segmentation/service-contract`
- `GET /cdp-segmentation/release-evidence`

### Emitted Events

- `CustomerSegmentUpdated`
- `ProfileEnriched`

### Consumed Events

- `CustomerUpdated`
- `PaymentCaptured`
- `OrderShipped`

### UI Fragments

- `CdpSegmentationWorkbench`
- `CustomerEventStream`
- `ProfilePropertyPanel`
- `SegmentDefinitionBuilder`
- `MembershipEvaluationBoard`
- `ActivationConsole`
- `ConsentPolicyPanel`
- `IdentityStitchingPanel`
- `CdpRuleStudio`
- `CdpParameterConsole`
- `CdpConfigurationPanel`
- `CdpEventOutbox`
- `CdpDeadLetterQueue`
- `CdpSchemaContractExplorer`
- `CdpServiceContractExplorer`
- `CdpReleaseEvidencePanel`

### Permissions

- `cdp_segmentation.audit`
- `cdp_segmentation.analytics.write`
- `cdp_segmentation.configure`
- `cdp_segmentation.event.consume`
- `cdp_segmentation.event.write`
- `cdp_segmentation.membership.evaluate`
- `cdp_segmentation.profile.govern`
- `cdp_segmentation.segment.write`

### Configuration Keys

- `CDP_SEGMENTATION_DATABASE_URL`
- `CDP_SEGMENTATION_EVENT_TOPIC`
- `CDP_SEGMENTATION_RETRY_LIMIT`
- `CDP_SEGMENTATION_DEFAULT_REGION`
- `CDP_SEGMENTATION_DEFAULT_TIMEZONE`
- `CDP_SEGMENTATION_ACTIVATION_MODE`

### Standard Features

- `customer_event_ingestion`
- `event_identity_link`
- `identity_stitching`
- `profile_registry`
- `segment_definition`
- `segment_rule`
- `segment_versioning`
- `segment_membership`
- `membership_evaluation`
- `profile_property`
- `consent_policy`
- `profile_consent`
- `real_time_activation`
- `activation_destination`
- `activation_delivery`
- `audience_snapshot`
- `profile_enrichment`
- `affinity_scoring`
- `lifecycle_risk_scoring`
- `merge_candidates`
- `profile_exception_management`
- `data_quality_findings`
- `consent_policy_screening`
- `payment_projection`
- `order_projection`
- `customer_update_projection`
- `notification_projection`
- `loyalty_projection`
- `pricing_projection`
- `profile_proofs`
- `profile_audit_entries`
- `control_assertions`
- `federation_views`
- `resilience_drills`
- `crypto_epoch_rotation`
- `carbon_activation_windows`
- `segment_simulation`
- `activation_allocation`
- `profile_anomaly_signals`
- `audience_exposure_forecasts`
- `identity_attestation`
- `governed_model_registry`
- `tenant_isolation`
- `appgen_x_outbox`
- `appgen_x_inbox`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions`
- `configuration_schema`
- `rule_engine`
- `parameter_engine`
- `seed_data`
- `workbench`

### Advanced Capabilities

- `event_sourced_profile_lifecycle`
- `owned_cdp_schema_boundary`
- `multi_tenant_profile_isolation`
- `schema_evolution_resilient_profile_context`
- `customer_event_ingestion`
- `identity_and_profile_property_stitching`
- `segment_definition_management`
- `real_time_segment_membership`
- `transaction_payment_shipment_projection_handling`
- `profile_enrichment_and_activation`
- `probabilistic_affinity_scoring`
- `counterfactual_segment_membership_simulation`
- `temporal_audience_forecasting`
- `autonomous_audience_exception_resolution`
- `semantic_segment_rule_understanding`
- `predictive_lifecycle_risk`
- `self_healing_profile_merge`
- `cryptographic_profile_proof`
- `immutable_profile_audit_trail`
- `dynamic_consent_policy_screening`
- `automated_data_quality_control_testing`
- `cross_system_customer_payment_order_federation`
- `appgen_x_outbox_inbox_eventing`
- `idempotent_handlers`
- `retry_dead_letter_evidence`
- `permissions_governance_evidence`
- `configuration_schema`
- `parameter_engine`
- `rule_engine`
- `seed_data`
- `workbench_ui`
- `governed_model_evidence`

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `cdp_segmentation` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `cdp_segmentation_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Customer Data Platform Segmentation` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `cdp_segmentation_customer_event`, `cdp_segmentation_segment_definition`, `cdp_segmentation_segment_membership`, `cdp_segmentation_profile_property`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as `configure_runtime`, `set_parameter`, `register_rule`, `register_schema_extension`, `receive_event`, `ingest_customer_event`, uses AppGen-X event expectations such as `CustomerSegmentUpdated`, `ProfileEnriched`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `cdp_segmentation`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `cdp_segmentation_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

