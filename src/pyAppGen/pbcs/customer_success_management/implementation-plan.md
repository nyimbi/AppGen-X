# Implementation Plan

## Goal

Turn `customer_success_management` into a coherent one-PBC standalone app that is package-local, database-backed, and auditable. Every visible contract in the package should describe the same executable owned implementation rather than separate placeholder layers.

## Scope

- Stay entirely inside `src/pyAppGen/pbcs/customer_success_management`
- Keep all persistence, routing, UI, events, agent planning, docs, and release evidence package-owned
- Satisfy the repo-level gates named for this PBC:
  - `pbc_source_artifact_contract`
  - `pbc_implementation_release_audit`
  - `pbc_generation_smoke_audit`

## Plan

1. Establish one shared executable core.
   - Add a package-local slice app backed by SQLite for focused smoke coverage.
   - Encode owned tables, route mappings, touchpoint workflows, forms, wizards, controls, permissions, and release artifacts in one place.

2. Make the owned database real and coherent.
   - Replace the conflicting migration with a single schema that matches the executable app and contracts.
   - Expose model/schema metadata from the same table definitions.

3. Rebind package contracts to the shared core.
   - Update runtime, schema, service, route, event, handler, UI, agent, seed, and release modules to derive from the shared implementation.
   - Preserve package entry points used by existing tests and audits.

4. Improve the domain behavior, not just the declarations.
   - Implement executable account intake, success plan creation, onboarding milestones, touchpoint capture, health scoring, playbook launch, renewal motion, churn scoring, document planning, CRUD planning, and AppGen-X event handling.

5. Add focused validation and release evidence.
   - Add tests for the standalone slice app, migration/bootstrap, route dispatch, event idempotency, and release audits.
   - Record what is implemented, what remains, and how it was validated.

## Design choices

- SQLite is used only as a package-local execution harness. Production-facing contracts still declare PostgreSQL, MySQL, and MariaDB as the supported backends.
- The migration uses a common owned-record shape across customer-success tables so the package stays small and auditable while still supporting real writes and queries.
- Legacy catalog event names are preserved as aliases in the event layer so existing package expectations remain compatible while the richer domain contract stays canonical.

## Risks to watch

- Manifest/catalog values and deep domain values intentionally differ in a few places; release evidence must keep that traceability explicit.
- The standalone app is intentionally minimal and auditable, not a full framework integration. Future work should extend the same shared core rather than reintroducing divergent generated layers.
