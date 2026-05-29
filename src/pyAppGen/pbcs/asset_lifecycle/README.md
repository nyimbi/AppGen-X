# Asset Lifecycle

`asset_lifecycle` is the AppGen-X PBC for fixed assets, capitalization controls, depreciation, transfers, valuation changes, maintenance-driven accounting changes, retirement, and audit-oriented lifecycle evidence.

## Implemented Slice

This package now includes an executable depreciation-accounting slice for:

- Versioned straight-line depreciation schedules
- Remaining-life schedule revision after maintenance adjustments
- Idempotent depreciation runs with replayable run evidence

The implemented behavior lives in [depreciation_engine.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/depreciation_engine.py), with package surfaces wired through [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/runtime.py), [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/services.py), [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/ui.py), [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/agent.py), and [release_evidence.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/asset_lifecycle/release_evidence.py).

## Key Entry Points

- `asset_lifecycle_build_depreciation_schedule(state, asset_id, method="straight_line")`
  Builds a versioned schedule for the active asset state and preserves prior schedule versions.
- `asset_lifecycle_review_depreciation_plan(state, asset_id)`
  Returns the active version, posted periods, pending periods, and revision state for one asset.
- `asset_lifecycle_run_depreciation(state, run_id, period)`
  Posts only the due schedule lines for one accounting period and replays prior run evidence on duplicates.
- `AssetLifecycleService().preview_depreciation_plan(payload)`
  Projects a schedule build or revision from service-layer preview payloads without mutating runtime state.
- `depreciation_revision_preview(payload)`
  Exposes the same revision preview to the package assistant surface.

## Test Coverage

Focused implementation coverage lives in [tests/test_pbc_asset_lifecycle_implementation.py](/Volumes/Media/src/pjs/appgen/tests/test_pbc_asset_lifecycle_implementation.py). The implementation tests cover:

- schedule revision after useful-life extension
- idempotent rerun behavior for an already-posted depreciation period
- service, UI, agent, event, and release-evidence exposure for the depreciation slice

## Validation Commands

```bash
python3 -m py_compile src/pyAppGen/pbcs/asset_lifecycle/depreciation_engine.py \
  src/pyAppGen/pbcs/asset_lifecycle/runtime.py \
  src/pyAppGen/pbcs/asset_lifecycle/services.py \
  src/pyAppGen/pbcs/asset_lifecycle/routes.py \
  src/pyAppGen/pbcs/asset_lifecycle/events.py \
  src/pyAppGen/pbcs/asset_lifecycle/handlers.py \
  src/pyAppGen/pbcs/asset_lifecycle/ui.py \
  src/pyAppGen/pbcs/asset_lifecycle/agent.py \
  src/pyAppGen/pbcs/asset_lifecycle/release_evidence.py \
  src/pyAppGen/pbcs/asset_lifecycle/__init__.py

./.venv/bin/pytest \
  tests/test_pbc_asset_lifecycle_implementation.py \
  tests/test_pbc_asset_lifecycle_runtime.py \
  src/pyAppGen/pbcs/asset_lifecycle/tests/test_contract.py
```

## Notes

- Eventing remains AppGen-X only.
- Table access remains inside the owned asset lifecycle boundary.
- The rest of `improve1.md` remains intentionally deferred to later slices.


## Standalone one-PBC application

This directory now includes a package-local standalone application harness for the Asset Lifecycle PBC. The runtime deployment database backends remain PostgreSQL, MySQL, and MariaDB; the SQLite repository is only a deterministic local harness for tests and demos.

- `repository.py` persists runtime state, form submissions, workflow runs, control executions, agent sessions, and a workbench read model.
- `standalone.py` bootstraps a single-PBC application and publishes smoke/release snapshots.
- `services.py` and `routes.py` expose app-local commands and route dispatch for asset registration, depreciation, transfer, audit proof, and workbench reads.
- `ui.py` surfaces standalone forms, wizards, controls, and workbench cards.
- `agent.py` integrates asset lifecycle skills, document intake, depreciation preview, CRUD planning, and route/wizard candidates into the composed assistant.

Focused verification:

```bash
PYTHONPATH=src python3 -m py_compile src/pyAppGen/pbcs/asset_lifecycle/*.py src/pyAppGen/pbcs/asset_lifecycle/tests/*.py
PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/asset_lifecycle/tests
```
