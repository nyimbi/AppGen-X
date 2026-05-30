# Defense Readiness Logistics PBC

`defense_readiness_logistics` is a standalone AppGen-X packaged business capability for unit readiness, mission assets, inspections, maintenance forecasting, supply readiness, fuel sufficiency, deployment kits, movement control, classified custody, and deployment release governance.

## Standalone Slice

This package now exposes a coherent standalone slice rather than disconnected contracts:

- Owned model, schema, and migration definitions align around `defense_readiness_logistics_*` tables only.
- Command services execute deterministic package-local workflows for readiness validation, movement release, and deployment release.
- Routes bind to real service operations.
- Events and handlers use the fixed AppGen-X outbox, inbox, and dead-letter boundary.
- Workbench, forms, wizards, and controls reflect commander, maintenance, supply, movement, classification, and exception queues.
- Assistant skills are domain-routed, citation-required, preview-only, and confirmation-gated.

## Executable Surface

- `assess_unit_readiness`
- `record_mission_asset`
- `create_readiness_inspection`
- `verify_personnel_qualification`
- `project_maintenance_status`
- `score_supply_readiness`
- `allocate_fuel_reserve`
- `validate_deployment_kit`
- `validate_movement_load_plan`
- `verify_controlled_item_custody`
- `request_theater_support`
- `plan_logistics_movement`
- `triage_readiness_exception`
- `release_deployment_plan`
- `run_readiness_validation_workflow`
- `run_movement_release_workflow`

## Verification

```bash
python3 -m py_compile src/pyAppGen/pbcs/defense_readiness_logistics/*.py src/pyAppGen/pbcs/defense_readiness_logistics/tests/*.py
uv run --with pytest pytest -q src/pyAppGen/pbcs/defense_readiness_logistics/tests
python3 -m pyAppGen.pbcs.defense_readiness_logistics.tests.test_alignment
```

If `pytest` is not available in a local virtualenv for the worktree, use the `uv run --with pytest` fallback above.
