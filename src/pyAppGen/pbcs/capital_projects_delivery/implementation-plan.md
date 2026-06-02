# Capital Projects Delivery Implementation Plan

## Objective

Upgrade `src/pyAppGen/pbcs/capital_projects_delivery` from a focused lifecycle slice into a coherent standalone one-PBC AppGen-X package without editing shared generators, DSL, or progress-ledger files.

## Selected Improvement Slice

Anchor the work in backlog item 1 from `improve1.md` (governed stage-gate lifecycle), then close the standalone-package gaps required to run that slice as a one-PBC functional app surface.

## Package-Local Workstreams

1. Runtime and contract convergence
   - Keep the executable lifecycle runtime as the behavioral source of truth.
   - Add package-local workflow, route, permission, release, and standalone-app contract evidence around the lifecycle slice.
   - Preserve AppGen-X-only eventing, hidden stream-engine selection, and owned-table-only mutation boundaries.

2. Standalone app surface
   - Add `standalone.py` to bootstrap configuration, parameters, rules, demo records, route dispatch, workbench rendering, and release snapshots entirely inside this package.
   - Ensure the package can render a real one-PBC workbench shell rather than only exposing metadata.

3. UI, forms, wizards, controls, and workflows
   - Extend `ui.py` with standalone shell metadata, navigation, permission-aware workbench rendering, and workflow visibility tied to the lifecycle slice.
   - Keep forms, wizards, and controls package-local and deterministic.

4. Agent/document planning and governed CRUD
   - Strengthen `agent.py` so document instruction intake and CRUD planning resolve to owned tables, candidate operations, routes, permissions, idempotency keys, and AppGen-X event previews.
   - Keep mutation planning side-effect-free and human-confirmed.

5. Release evidence, docs, and tests
   - Refresh `README.md`, `implementation-status.md`, and `RELEASE_EVIDENCE.md` to describe the actual standalone scope and validation evidence.
   - Add focused standalone tests plus contract coverage for workflows, route/service alignment, agent planning, and app-shell rendering.

## Expected Deliverables

- Real executable package-local improvements in runtime, services, routes, UI, permissions, agent planning, release evidence, and standalone bootstrapping.
- `standalone.py` and focused standalone tests.
- Updated `README.md`, `implementation-plan.md`, and `implementation-status.md`.

## Constraints

- Work only inside `src/pyAppGen/pbcs/capital_projects_delivery`.
- Do not edit shared generator, DSL, or progress-ledger files.
- Keep eventing AppGen-X only.
- Keep `stream_engine_picker_visible` false.
- Keep `shared_table_access` false.

## Validation Plan

- Compile the package with `python3 -m compileall`.
- Execute package-local tests by importing and running `test_` functions in `tests/test_contract.py`, `tests/test_lifecycle_app_slice.py`, and `tests/test_standalone.py`.
- Run focused PBC audits for source artifacts, implementation release evidence, and generation smoke.
- Check the scoped diff with `git diff --check -- src/pyAppGen/pbcs/capital_projects_delivery`.
