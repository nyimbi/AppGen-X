# Schema Registry Implementation Plan

## Objective

Make `schema_registry` usable as a standalone PBC with owned runtime state, database-backed forms, guided workflows, controls, assistant skills, release evidence, and focused validation.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/schema_registry`.
- Preserve the existing runtime capability proofs and owned-table boundary rules.
- Add only the missing standalone surfaces: repository, forms, wizards, app bootstrap, docs, and tests.

## Planned Work

1. Add a repository that wraps runtime operations and holds standalone state.
2. Replace the thin route/service facade with a fuller one-PBC command/query surface.
3. Extend the UI contract with concrete forms, wizards, controls, and standalone app metadata.
4. Expand the assistant workspace to expose standalone forms, wizards, and command routing.
5. Align permissions, event, handler, and seed surfaces with the standalone runtime.
6. Add README, implementation status, and standalone smoke tests.
7. Validate with compile, focused slice tests, and relevant schema_registry PBC contract checks.

## Non-Goals

- No edits outside the assigned `schema_registry` directory.
- No new dependencies.
- No shared-table persistence or cross-PBC mutation.
