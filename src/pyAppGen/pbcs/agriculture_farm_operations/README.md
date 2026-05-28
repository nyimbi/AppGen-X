# Agriculture Farm Operations

This PBC owns farm-operations behavior for fields, crop plans, inputs, equipment, irrigation, harvest, yield, certifications, and farm compliance. The package uses the AppGen-X event contract and stays within package-local owned tables and ordinary relational backends: PostgreSQL, MySQL, and MariaDB.

## Implemented executable slice

The current implementation adds a real crop-planning lane on top of the existing package scaffolding:

- season-aware crop plans with `season` and `market_year`
- overlap detection for active plans on shared field scope
- replant linkage with predecessor replacement tracking
- planting-window classification: `early`, `optimal`, `late`, `missed`
- pre-plant readiness gating for core operational prerequisites
- workbench-ready summaries for crop-plan alerts and blocked exceptions

## Key module entry points

- `crop_planning.py`
  Pure package-local crop-plan evaluation and workbench summarization.
- `runtime.py`
  Runtime state handling through `agriculture_farm_operations_record_crop_plan(...)`.
- `services.py`
  Service-layer preview for `record_crop_plan`.
- `ui.py`
  Workbench metadata for crop-plan timeline and planting-window alerts.

## Validation commands

```bash
./.venv/bin/pytest tests/test_pbc_agriculture_farm_operations_implementation.py tests/test_pbc_agriculture_farm_operations_runtime.py src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_contract.py
python3 -m compileall src/pyAppGen/pbcs/agriculture_farm_operations
```

## Scope notes

- No non-AppGen-X event contract is introduced.
- No stream-engine picker is exposed.
- No external ERP/CRM/accounting product terminology is used.
- The slice is intentionally limited to crop-plan planning behavior; broader agronomy, irrigation, scouting, and harvest backlog items remain open.
