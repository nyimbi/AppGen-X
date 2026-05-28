## Agriculture Farm Operations Implementation Status

### Completed in this slice
- Added executable crop-plan evaluation in `crop_planning.py`.
- Implemented season-aware crop-plan normalization with explicit `season`, `market_year`, `fallback_crop`, `previous_crop`, and `replant_of`.
- Added overlap detection for active plans on the same field or management zone.
- Added planting-window classification with `early`, `optimal`, `late`, and `missed` statuses.
- Added pre-plant readiness gating for soil fit, fertility readiness, equipment readiness, crew assignment, and irrigation readiness when required.
- Extended runtime state to persist crop plans, planning exceptions, and workbench-ready summaries.
- Extended the service layer with a real `record_crop_plan` planning preview.
- Extended the workbench metadata with crop-plan timeline and alert widgets.
- Added focused implementation tests for acceptance, blocking, replant handling, and service preview behavior.

### Self review
- Removed an unused constant from the planning module.
- Reduced repeated schedule normalization in crop-plan assembly.
- Tightened workbench accepted-plan counting so replaced plans do not inflate active-plan totals.

### Validation
- `./.venv/bin/pytest tests/test_pbc_agriculture_farm_operations_implementation.py tests/test_pbc_agriculture_farm_operations_runtime.py src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_contract.py`
- `python3 -m compileall src/pyAppGen/pbcs/agriculture_farm_operations`

### Remaining backlog outside this slice
- Field-to-plot geometry hierarchy and acreage reconciliation.
- Variety and seed-lot traceability beyond the lightweight plan fields added here.
- Agronomy prescription versioning, irrigation scheduling, scouting thresholds, and harvest execution depth.
- API-level separation of planning, approval, and execution flows beyond the runtime/service slice implemented here.

### Risks and limits
- Crop-plan state is still in-memory runtime evidence, not persisted relational records yet.
- Planting-window rules are payload-driven; there is no package-local rule catalog or region seed data yet.
- Service previews evaluate the submitted plan without an external persisted state snapshot, so conflict detection is authoritative in runtime state, not the stateless preview path.
