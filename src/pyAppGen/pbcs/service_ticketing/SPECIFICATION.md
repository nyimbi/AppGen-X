# Service Ticketing PBC

`service_ticketing` owns customer support case intake, SLA orchestration, assignment, escalation, and resolution evidence for AppGen-X generated applications. It is packaged as a composable business capability with its own runtime, owned schema boundary, service commands, APIs, events, UI fragments, configuration, rules, parameters, and release evidence.

## Owned Boundary

- Owned tables: `support_ticket`, `sla_policy`, `case_assignment`, `escalation_event`.
- Integration boundary: declared APIs, AppGen-X outbox/inbox events, and projections only.
- Datastore backends: PostgreSQL, MySQL, or MariaDB.
- Eventing: AppGen-X event contract on `appgen.service_ticketing.events`; no user-facing stream-engine selection.

## Standard Capabilities

- Omnichannel support-ticket intake across email, chat, and portal channels.
- SLA policy creation with response and resolution targets.
- Skill/queue-based case assignment and open-case load evidence.
- Escalation orchestration with breach-risk scoring and emitted SLA events.
- Resolution tracking with customer update handoff.
- Customer context and preference projection handling through idempotent event handlers.
- Retry/dead-letter evidence, RBAC descriptors, configuration schema, parameter engine, rule engine, seed data, and workbench views.

## Advanced Capabilities

- Event-sourced case lifecycle and immutable case audit trail.
- Probabilistic SLA breach, customer escalation, and queue risk scoring.
- Counterfactual assignment simulation and temporal backlog forecasting evidence.
- Autonomous next-best-response generation and semantic case understanding.
- Dynamic service policy screening and automated service control testing.
- Cross-system customer, preference, and workflow federation through declared APIs/events only.
- Governed model evidence, cryptographic case proofs, and self-healing queue assignment evidence.

## UI

The workbench exposes ticket inbox, customer context panel, SLA policy designer, assignment queue board, escalation command center, resolution console, next-best-response panel, preference projection panel, rule studio, parameter console, configuration panel, outbox, and dead-letter queue fragments.
