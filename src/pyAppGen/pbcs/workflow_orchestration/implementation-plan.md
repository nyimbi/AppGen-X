# Workflow Orchestration Implementation Plan

## Objective

Upgrade `src/pyAppGen/pbcs/workflow_orchestration` into a coherent standalone
one-PBC app package without touching any other PBC or repo path.

## Package-Local Workstreams

1. Runtime truth alignment
   - Keep `runtime.py` as the behavioral source of truth.
   - Preserve AppGen-X event contract usage and owned-table-only boundaries.
   - Ensure standalone flows exercise real workflow definitions, instances,
     signals, timers, human work, compensation, and release controls.

2. Repository, model, service, and route convergence
   - Add a package-local repository contract that binds owned tables to runtime
     state.
   - Replace metadata-only service and route surfaces with executable
     package-local behavior over owned state.
   - Keep route, service, schema, and release artifacts side-effect-free for
     source package discovery and contract audits.

3. Standalone app surface
   - Add `standalone.py` to bootstrap configuration, parameters, rules, inbox
     events, workflow definitions, instances, tasking, compensation, and
     release snapshots entirely inside this package.
   - Ensure the package can render a realistic one-PBC workbench shell rather
     than only exposing metadata.

4. UI and assistant depth
   - Extend `ui.py` with forms, wizards, controls, navigation, and standalone
     shell metadata.
   - Strengthen `agent.py` with workflow-authoring previews, document intake,
     CRUD planning, and operator-safe action previews.

5. Release evidence and tests
   - Refresh `release_evidence.py` and `RELEASE_EVIDENCE.md` to include the
     repo gates `pbc_source_artifact_contract`,
     `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit`.
   - Add focused package tests for repository/model alignment, standalone app
     execution, and local gate coverage.

## Expected Deliverables

- Real executable package-local improvements in repository, models, services,
  routes, UI, events, agent planning, and standalone composition.
- `README.md`
- `implementation-plan.md`
- `implementation-status.md`
- Updated `RELEASE_EVIDENCE.md`
- Focused tests for contract and standalone app coverage

## Validation Plan

- Compile the package with `python3 -m py_compile`.
- Execute package-local gate tests by importing and running `test_` functions in
  `tests/test_contract.py` and `tests/test_standalone.py`.
- Run additional package smoke checks for runtime, routes, standalone app,
  release evidence, and `pbc_implementation_release_audit`.
