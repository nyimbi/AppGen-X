# Composition Engine PBC

`composition_engine` is a standalone one-PBC composition/orchestration slice for AppGen-X. It now ships with an executable runtime, a SQLite-backed repository, a standalone application wrapper, database-backed forms and wizards, control-center evidence, and assistant skills that stay inside composition-owned tables.

## What It Owns

- Composition workspaces, selected PBCs, component registrations, UI fragments, layout bindings, generated DSL artifacts, validation runs, package-registration plans, package-index entries, release evidence, configuration, parameters, and rules.
- Package-local AppGen-X outbox, inbox, and dead-letter tables.
- Composition workbench forms, guided wizards, controls, assistant routing, CRUD previews, release rehearsal, release notes, lineage, documentation matrix, and security review.

## Standalone Surface

- [`repository.py`](./repository.py): applies owned migrations and persists the runtime snapshot into SQLite tables.
- [`standalone.py`](./standalone.py): bootstraps a usable standalone app, executes forms and wizards, renders the workbench, exposes assistant previews, and syncs runtime state to the repository.
- [`forms.py`](./forms.py): executable forms for workspace intake, selection impact, assistant routing, governance review, control-center inspection, and release-note drafting.
- [`wizards.py`](./wizards.py): bootstrap, document-driven intake, and release-gate workflows that run against real form payloads.

## Typical Flow

1. Bootstrap the app with `CompositionEngineStandaloneApp(bootstrap=True)`.
2. Submit `workspace_intake`, `pbc_selection`, `component_fragment_registration`, and `layout_binding` forms.
3. Run `workspace_governance_review` or the `bootstrap_composition` wizard.
4. Inspect `control_center()` and `assistant_preview(...)` before publication.
5. Use `render_workbench(...)` and repository queries to confirm persisted state.

## Verification

- `python3 -m compileall src/pyAppGen/pbcs/composition_engine`
- `./.venv/bin/pytest src/pyAppGen/pbcs/composition_engine/tests -q`
- `./.venv/bin/pytest tests/test_pbc_composition_engine_runtime.py -q`

See [`implementation-status.md`](./implementation-status.md) for the current evidence snapshot.
