# DAM Core Implementation Plan

## Objective

Upgrade `src/pyAppGen/pbcs/dam_core` into a coherent standalone one-PBC app
package without touching global files or other PBCs.

## Package-Local Workstreams

1. Runtime truth alignment
   - Keep `runtime.py` as the behavioral source of truth.
   - Fix event drift so metadata, rights-policy, and rendition-request events
     are actually emitted by runtime transitions.
   - Make schema artifact paths point to real package-local files.

2. Contract convergence
   - Replace static generated constants in `manifest.py`, `events.py`,
     `models.py`, `schema_contract.py`, `service_contract.py`, `services.py`,
     `routes.py`, `permissions.py`, and `seed_data.py` with runtime-driven,
     executable package-local contracts.
   - Preserve side-effect-free planning surfaces required by source package
     discovery.

3. Standalone app surface
   - Add `standalone.py` to bootstrap configuration, parameters, rules, inbox
     events, asset lifecycle actions, route dispatch, workbench rendering, and
     release snapshots entirely inside `dam_core`.
   - Ensure the package can render a realistic one-PBC app shell rather than
     only exposing metadata.

4. UI/workbench depth
   - Extend `ui.py` with forms, wizards, controls, navigation, and standalone
     shell metadata.
   - Keep workbench rendering deterministic and side-effect-free.

5. Agent/document planning
   - Strengthen `agent.py` so CRUD planning and document-intake planning resolve
     to owned tables, candidate routes, permissions, idempotency keys, and
     event previews.

6. Release evidence and tests
   - Refresh `release_evidence.py` and `RELEASE_EVIDENCE.md` to include the
     named repo gates: `pbc_source_artifact_contract`,
     `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit`.
   - Add focused package tests for contracts, lifecycle smoke, standalone app
     execution, and the three repo gates.

## Expected Deliverables

- Real executable package-local improvements in runtime, models, services,
  routes, UI, events, and agent planning.
- `README.md`
- `implementation-status.md`
- Updated `RELEASE_EVIDENCE.md`
- Focused tests for contract, standalone app, and gate coverage

## Validation Plan

- Compile the package with `python3 -m compileall`.
- Execute package-local gate tests by importing and running `test_` functions in
  `tests/test_contract.py` and `tests/test_standalone.py`.
- Run additional package smoke checks for runtime, routes, standalone app, and
  release evidence.
