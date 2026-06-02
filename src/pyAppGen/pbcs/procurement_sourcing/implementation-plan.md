# procurement_sourcing Implementation Plan

## Scope

This PBC must be functional as a one-PBC procurement application with owned schema, migrations, models, services, APIs, events, handlers, forms, wizards, controls, assistant skills, repository read models, and release evidence.

## Delivered Architecture

1. Owned datastore boundary remains limited to `procurement_sourcing_*` tables and PostgreSQL/MySQL/MariaDB backends.
2. The runtime owns source-to-order commands from requisition through RFQ, bid capture, scoring, award, contract, and purchase order issuance.
3. Consumed AppGen-X events populate projections; emitted domain events go through the owned outbox.
4. The standalone app uses deterministic seed data and executes a full procurement workspace without shared-table access.
5. The UI contract exposes domain forms, guided wizards, controls, workbench cards, and agent skill integration.
6. Release evidence validates runtime, repository, UI, agent, model, event, service, schema, and package artifacts.

## Guardrails

- Do not add user-facing stream-engine selectors.
- Do not access shared tables for cross-PBC dependencies; consume events and declared projections instead.
- Keep all package implementation files inside `src/pyAppGen/pbcs/procurement_sourcing`.
- Mutating assistant actions must remain planned, permission checked, previewed, and bound to owned tables.
