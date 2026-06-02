# Restaurant Operations Implementation Plan

## Source Reviewed

- `improve1.md` restaurant improvement backlog.
- Existing package manifest, standalone runtime, services, routes, models, UI, agent surface, and tests.

## Implementation Intent

Make `restaurant_operations` useful as a one-PBC composed application for restaurant operators. The package must support menu/recipe governance, floor and reservation execution, kitchen display state, prep and inventory-adjacent evidence, food safety, revenue/check settlement, guest incident handling, loyalty/service recovery notes, and governed AI-assisted CRUD previews while staying inside the PBC-owned datastore boundary.

## Delivery Steps

1. Preserve the existing AppGen-X event contract and database backend policy.
2. Use PBC-owned models/services/routes/UI/agent code to expose a standalone restaurant workbench.
3. Verify that menu, recipe, floor plan, reservation/waitlist, shift launch, prep, orders, KDS state advancement, check settlement, vendor receipt evidence, safety logging, guest incident, loyalty note, and governed preview flows execute through PBC-local routes.
4. Surface the standalone route/test/UI evidence in the manifest.
5. Record verification evidence and remaining risks in `implementation-status.md`.

## Acceptance Gates

- PBC-local tests pass.
- Focused source/package/spec/agent/implementation/capability/generation audits pass.
- The package exposes one-PBC forms, workbench views, agent assistance, and in-memory database-backed workflow execution without writing foreign PBC tables.
