# Distributed Order Management

This PBC now runs as a standalone one-PBC application inside `src/pyAppGen/pbcs/dom`.

## What it does

- Captures and validates distributed orders with channel context and promise hints.
- Applies tax and fraud projections through the fixed AppGen-X event contract surface.
- Verifies, prices, allocates, routes, plans, and ships orders with package-owned state only.
- Tracks holds, backorders, substitutions, cancellations, exceptions, and audit traces.
- Exposes package-local UI forms, wizards, controls, workbench rendering, document intake, CRUD mutation planning, and release/audit evidence.

## Main entrypoints

- `standalone.DomStandaloneApplication` for the mutable one-PBC app shell with SQLite-backed repository/read models.
- `services.DomStandaloneService` for package-local service methods.
- `routes.dispatch_standalone_route` for route-to-service execution.
- `ui.dom_ui_contract` and `ui.dom_render_workbench` for forms, wizards, controls, and workbench output.
- `agent.document_instruction_plan` and `agent.datastore_crud_plan` for document intake and governed mutation previews.
- `standalone.standalone_release_snapshot` and `seed_data.standalone_seed_bundle` for demo/bootstrap and release-proof snapshots.
- `audit.run_dom_pbc_audit` and `release_evidence.build_release_evidence` for package-local audits.

## Constraints

- Eventing is AppGen-X only.
- No stream-engine picker or alternate transport is exposed.
- Supported backends remain PostgreSQL, MySQL, and MariaDB only.
- All executable behavior stays inside the `dom` PBC boundary.
