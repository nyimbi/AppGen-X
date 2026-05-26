# Notifications PBC

`notifications` is the AppGen-X packaged business capability for omnichannel
communication orchestration, consent-aware delivery routing, template
management, preference snapshots, delivery evidence, and notification workbench
operations. It is a complete package-local implementation with owned schema,
runtime services, API descriptors, AppGen-X events, idempotent handlers, rules,
parameters, configuration, UI fragments, package metadata, focused tests, and
release evidence.

## Stable Identity

- PBC key: `notifications`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/notifications`.
- Runtime entrypoint: `notifications_runtime_capabilities()`.
- UI entrypoint: `notifications_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.notifications.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `notification_template`: tenant-scoped message templates, locale, message
  type, required variables, rendered subject/body definitions, status, and
  audit proof.
- `delivery_channel`: tenant channel registry, provider identity, channel type,
  health score, cost score, availability status, and audit proof.
- `message_delivery`: queued and attempted deliveries, rendered payload,
  selected channel, urgency, risk score, provider status, retry evidence, and
  audit proof.
- `preference_snapshot`: customer communication consent, preferred channels,
  locale, and immutable snapshot evidence.

No customer, workflow, SLA, campaign, or profile tables are shared or directly
accessed. External context arrives through declared AppGen-X events and API
projections only:

- Consumed events: `PreferenceChanged`, `SlaBreached`, and
  `WorkflowCompleted`.
- API projections: `preference_projection`, `sla_projection`, and
  `workflow_projection`.
- Runtime event tables are PBC-local:
  `notifications_appgen_outbox_event`,
  `notifications_appgen_inbox_event`, and
  `notifications_dead_letter_event`.

The boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer_profile`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary notification capabilities expected from
a production communication package:

- Runtime configuration for database backend, event topic, retry limit, default
  locale, supported locales, supported channels, timezone, delivery mode, quiet
  hours, and workbench limit.
- Parameter engine for delivery success threshold, fatigue threshold, channel
  health weighting, preference weighting, urgency weighting, cost weighting,
  daily-recipient limits, retry limit, message TTL, and workbench limit.
- Rule engine for tenant, scope, channel/locale/message-type constraints,
  consent policy, delivery policy, status, compiled hash, and policy-engine
  evidence.
- Schema extension for owned notification tables only, with versioned migration
  evidence.
- Template registration with required variable validation, localization, and
  audit proof.
- Delivery channel registration for email, SMS, push, and chat with provider
  health and cost evidence.
- Preference snapshot projection from `PreferenceChanged`.
- Trigger event intake for `SlaBreached` and `WorkflowCompleted`.
- Consent-aware message routing with template rendering and preferred-channel
  selection.
- Delivery attempt recording with terminal `MessageDelivered` or
  `MessageFailed` AppGen-X outbox evidence.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for templates, channels, deliveries, preferences, rules,
  parameters, configuration, outbox, and dead letters.
- UI fragments for template designer, channel console, message composer,
  preference snapshots, delivery status board, routing board, consent policy,
  rule studio, parameter console, configuration, outbox, and dead-letter
  queue.
- Permission/RBAC descriptors for template, channel, send, event, configure,
  and audit actions.
- Seed data for default channels and message types.

## Advanced Capabilities

The executable runtime proves the advanced notification capabilities needed for
a modern relationship PBC:

- Event-sourced message lifecycle with immutable state-event hashes.
- Owned notification schema boundary enforcement with explicit violation
  evidence.
- Multi-tenant delivery isolation across templates, channels, deliveries,
  preferences, and UI views.
- Schema-evolution-safe template and delivery extensions.
- Probabilistic delivery risk, recipient fatigue, urgency, and channel-health
  evidence.
- Counterfactual channel selection support through deterministic routing-score
  recomputation.
- Temporal delivery-window forecasting evidence through quiet hours and TTL
  parameters.
- Autonomous delivery exception resolution through channel failover and
  retry/dead-letter evidence.
- Semantic template rendering and required-variable validation.
- Dynamic consent policy screening.
- Automated communication control testing via smoke checks and release audits.
- Self-healing route selection through rule- and parameter-driven channel
  choice.
- Cryptographic delivery proofs.
- Immutable delivery audit trail.
- Cross-system preference, workflow, and SLA federation through declared
  APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed model evidence.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `register_template(command)`.
- `register_channel(command)`.
- `receive_event(event, simulate_failure=False)`.
- `send_message(command)`.
- `record_delivery_attempt(delivery_id, provider_status=...)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /templates` runs `register_template`, writes
  `notification_template`, requires `notifications.template.write`, and is
  idempotent by `template_id`.
- `POST /delivery-channels` runs `register_channel`, writes
  `delivery_channel`, requires `notifications.channel.write`, and is
  idempotent by `channel_id`.
- `POST /messages` runs `send_message`, writes `message_delivery`, requires
  `notifications.message.send`, and is idempotent by `delivery_id`.
- `POST /delivery-attempts` runs `record_delivery_attempt`, updates
  `message_delivery`, requires `notifications.message.send`, emits delivery
  events, and is idempotent by `delivery_id:provider_status`.
- `POST /notifications/events/inbox` runs `receive_event`, consumes declared
  AppGen-X events, requires `notifications.event.consume`, and is idempotent
  by `event_id`.
- `GET /delivery-status` queries `build_workbench_view`, reads only owned
  Notifications state, and requires `notifications.audit`.

The catalog-facing route set remains `POST /messages`, `POST /templates`, and
`GET /delivery-status`.

## Events And Handlers

Consumed events:

- `PreferenceChanged`.
- `SlaBreached`.
- `WorkflowCompleted`.

Emitted events:

- `MessageDelivered`.
- `MessageFailed`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, project preference snapshots and trigger payloads into package-local
state, and send simulated failures to the dead-letter evidence queue. Runtime
configuration requires the AppGen-X notifications event topic, records the
AppGen-X event contract, and never exposes a stream-engine picker or alternate
event-contract selector.

## UI And Workbench

The UI contract exposes:

- Notifications workbench.
- Template designer.
- Delivery channel console.
- Message composer.
- Preference snapshot panel.
- Delivery status board.
- Channel routing board.
- Consent policy panel.
- Notification rule studio.
- Notification parameter console.
- Notification configuration panel.
- Notification event outbox.
- Notification dead-letter queue.

Rendered workbench output includes tenant-filtered template, channel, delivery,
preference, outbox, and dead-letter counts; visible and locked actions from
RBAC permissions; and owned-table binding evidence.

## Release Evidence

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, template, channel, event
  handling, message sending, delivery status emission, UI rendering, API
  descriptors, RBAC descriptors, and workbench evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid event topics, forbidden eventing fields,
  invalid parameters, non-owned schema extensions, and simulated handler
  failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release audits.
