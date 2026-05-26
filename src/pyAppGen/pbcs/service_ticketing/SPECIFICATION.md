# Service Ticketing PBC

`service_ticketing` is the AppGen-X packaged business capability for
omnichannel support intake, SLA policy management, assignment, escalation,
resolution evidence, customer-context projection handling, and preference-aware
service orchestration. It is a complete package-local implementation with owned
schema, runtime services, API descriptors, AppGen-X events, idempotent
handlers, rules, parameters, configuration, UI fragments, package metadata,
tests, and release evidence.

## Stable Identity

- PBC key: `service_ticketing`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/service_ticketing`.
- Runtime entrypoint: `service_ticketing_runtime_capabilities()`.
- UI entrypoint: `service_ticketing_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.service_ticketing.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `support_ticket`: tenant, customer, subject, description, channel, priority,
  region, SLA policy, assignment, next-best response, breach risk, status, and
  audit proof.
- `sla_policy`: tenant, policy name, priority, first-response target,
  resolution target, status, and audit proof.
- `case_assignment`: tenant, ticket, owner, queue, skill evidence, assignment
  score, status, and audit proof.
- `escalation_event`: tenant, ticket, reason, breach risk, status, and audit
  proof.

No customer, preference, identity, messaging, workflow, or analytics tables are
shared or directly accessed. External information enters through declared
AppGen-X events and API projections only:

- Consumed events: `CustomerUpdated` and `PreferenceChanged`.
- API projections: `customer_context_projection` and
  `preference_projection`.
- Runtime event tables are PBC-local:
  `service_ticketing_appgen_outbox_event`,
  `service_ticketing_appgen_inbox_event`, and
  `service_ticketing_dead_letter_event`.

The boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer_profile`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary service capabilities expected from a
production ticketing package:

- Runtime configuration for database backend, event topic, retry limit,
  default region, supported regions, channels, priorities, timezone,
  assignment mode, and workbench limit.
- Parameter engine for SLA breach risk, auto-escalation threshold, sentiment,
  priority, customer-tier, queue-load weighting, first-response target,
  resolution target, owner load, and workbench limit.
- Rule engine for tenant, scope, region/channel/priority constraints,
  assignment policy, escalation policy, status, compiled hash, and
  policy-engine evidence.
- Schema extension for owned service tables only, with versioned migration
  evidence.
- Customer-context and preference projection handling through idempotent
  AppGen-X inbox events.
- SLA policy creation with response and resolution targets.
- Ticket opening with region/channel/priority validation, rule screening,
  breach-risk scoring, next-best-response evidence, and outbox publication.
- Assignment with queue, owner, skill evidence, open-case load scoring, and
  ticket-state update.
- Escalation evidence with breach reason capture, audit proof, and emitted SLA
  events.
- Resolution tracking with customer update handoff through the AppGen-X outbox.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for tickets, resolved tickets, SLA policies, assignments,
  escalations, rules, parameters, configuration, outbox, and dead letters.
- UI fragments for ticket inbox, customer context, SLA designer, assignment
  board, escalation center, resolution console, next-best-response panel,
  preference projection panel, rule studio, parameter console, configuration,
  outbox, and dead-letter queue.
- Permission/RBAC descriptors for ticket, assignment, escalation, event,
  configuration, and audit actions.
- Seed data for supported intake channels and service queues.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for a modern
service PBC:

- Event-sourced case lifecycle with immutable state-event hashes.
- Owned service schema boundary enforcement with explicit violation evidence.
- Multi-tenant case isolation across tickets, policies, assignments,
  escalations, and UI views.
- Schema-evolution-safe case extensions.
- Omnichannel case intake and service-policy screening.
- Customer context and preference projection handling through declared
  integrations only.
- Probabilistic SLA breach, escalation, and queue-risk scoring evidence.
- Counterfactual assignment simulation support through deterministic assignment
  scoring inputs.
- Temporal backlog forecasting support through workload and SLA parameters.
- Autonomous next-best-response generation from priority and sentiment.
- Semantic case understanding evidence through subject, description, channel,
  and sentiment.
- Predictive escalation risk and self-healing queue assignment evidence.
- Cryptographic case proofs and immutable service audit trail.
- Automated service control testing through smoke checks and release audits.
- Cross-system customer and preference federation through declared APIs/events
  only.
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
- `receive_event(event, simulate_failure=False)`.
- `create_sla_policy(command)`.
- `open_ticket(command)`.
- `assign_ticket(command)`.
- `record_escalation(ticket_id, reason=...)`.
- `resolve_ticket(ticket_id, resolution=...)`.
- `build_api_contract()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /sla-policies` runs `create_sla_policy`, writes `sla_policy`,
  requires `service_ticketing.configure`, and is idempotent by
  `sla_policy_id`.
- `POST /tickets` runs `open_ticket`, writes `support_ticket`, requires
  `service_ticketing.ticket.write`, emits `SupportCaseOpened` and optional
  `SlaBreached`, and is idempotent by `ticket_id`.
- `POST /assignments` runs `assign_ticket`, writes `case_assignment` and
  updates `support_ticket`, requires `service_ticketing.assignment.write`, and
  is idempotent by `assignment_id`.
- `POST /escalations` runs `record_escalation`, writes `escalation_event` and
  updates `support_ticket`, requires `service_ticketing.escalation.write`,
  emits `SlaBreached`, and is idempotent by `ticket_id:reason`.
- `POST /resolutions` runs `resolve_ticket`, updates `support_ticket`,
  requires `service_ticketing.ticket.write`, emits `CustomerUpdated`, and is
  idempotent by `ticket_id`.
- `POST /service-ticketing/events/inbox` runs `receive_event`, consumes
  declared AppGen-X events, requires `service_ticketing.event.consume`, and is
  idempotent by `event_id`.
- `GET /sla-status` queries `build_workbench_view`, reads only owned Service
  Ticketing state, and requires `service_ticketing.audit`.

The catalog-facing route set remains `POST /tickets`, `POST /assignments`, and
`GET /sla-status`.

## Events And Handlers

Consumed events:

- `CustomerUpdated`.
- `PreferenceChanged`.

Emitted events:

- `SupportCaseOpened`.
- `SlaBreached`.
- `CustomerUpdated`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, store customer-context and preference projections in package-local
state, and send simulated failures to the dead-letter evidence queue. Users
never choose a stream engine.

## UI And Workbench

The UI contract exposes:

- Service Ticketing workbench.
- Ticket inbox.
- Customer context panel.
- SLA policy designer.
- Assignment queue board.
- Escalation command center.
- Resolution console.
- Next-best-response panel.
- Preference projection panel.
- Service rule studio.
- Service parameter console.
- Service configuration panel.
- Service event outbox.
- Service dead-letter queue.

Rendered workbench output includes tenant-filtered ticket, resolved-ticket,
SLA-policy, assignment, escalation, outbox, and dead-letter counts; visible
and locked actions from RBAC permissions; configuration/rule/parameter state;
and owned-table binding evidence.

## Release Evidence

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, customer-context and
  preference event handling, SLA policy creation, ticket opening, assignment,
  escalation, resolution, outbox emission, UI rendering, API descriptors, RBAC
  descriptors, and workbench evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- The package participates in all-PBC implementation release and generation
  smoke audits.
