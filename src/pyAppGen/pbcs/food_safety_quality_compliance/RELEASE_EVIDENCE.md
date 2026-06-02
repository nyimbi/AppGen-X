# Release Evidence

Package directory: `pbcs/food_safety_quality_compliance`

## Evidence Areas

- Schema, models, and migration align to the owned food safety tables and local AppGen-X event tables.
- Services, routes, handlers, and runtime contracts all resolve to the standalone package-local slice.
- HACCP approval enforces CCP coverage for required hazards.
- Inspections pin to the active HACCP plan version and escalate to holds/nonconformances when risk thresholds are crossed.
- Recall analysis rejects foreign table access and runs mock drills without mutating live recall records.
- Assistant CRUD previews require owned tables, citations, human confirmation, and release review when applicable.

## Verification Hooks

- `python3 -m compileall src/pyAppGen/pbcs/food_safety_quality_compliance`
- `python3 -m pytest src/pyAppGen/pbcs/food_safety_quality_compliance/tests`
- `python3 - <<'PY' ... food_safety_quality_compliance_runtime_smoke() ... PY`
- `git diff --check`
