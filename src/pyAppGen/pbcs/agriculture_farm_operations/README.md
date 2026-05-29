# Agriculture Farm Operations

This package now exposes a standalone one-PBC farm-operations app surface centered on executable crop planning. The implementation stays package-local, uses only AppGen-X event contracts, and keeps all datastore references inside `agriculture_farm_operations_*` tables.

## Standalone surface

The standalone slice covers:

- field setup and management-zone context
- season-aware crop-plan intake with overlap detection
- planting-window classification and pre-plant readiness gating
- blocked-operations inbox and workflow runs
- agronomist assistant planning and document-to-draft intake
- package-local workbench forms, wizards, controls, and release evidence

## Package entry points

- `runtime.py`
  Runtime commands, schema/service/API contracts, workbench snapshots, workflow catalog, and release evidence primitives.
- `services.py`
  Stateful command/query service for the standalone route surface.
- `routes.py`
  Route contracts and in-memory dispatch for the one-PBC app.
- `ui.py`
  Workbench/UI contract plus forms, wizards, controls, and standalone rendering.
- `standalone.py`
  Bootstrapable standalone app shell for demo state, route dispatch, assistant workspace, and release snapshots.
- `agent.py`
  Agronomist copilot, document-instruction planning, and governed CRUD planning.

## Typical standalone flow

1. Bootstrap runtime configuration, parameters, rules, and inbox events through `AgricultureFarmOperationsStandaloneApp.bootstrap(...)`.
2. Create a field through `POST /api/pbc/agriculture_farm_operations/fields`.
3. Submit a crop plan through `POST /api/pbc/agriculture_farm_operations/crop-plans`.
4. Render the workbench through `AgricultureFarmOperationsStandaloneApp.render_workbench(...)`.
5. Review assistant and release evidence through `assistant_workspace()` and `release_snapshot()`.

## Validation commands

```bash
python3 -m compileall src/pyAppGen/pbcs/agriculture_farm_operations
PYTHONPATH=src python3 -m pytest           src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_contract.py           src/pyAppGen/pbcs/agriculture_farm_operations/tests/test_standalone.py           tests/test_pbc_agriculture_farm_operations_implementation.py           tests/test_pbc_agriculture_farm_operations_runtime.py
PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbc import pbc_implementation_release_audit, pbc_implemented_capability_audit
print(pbc_implementation_release_audit(("agriculture_farm_operations",))["ok"])
print(pbc_implemented_capability_audit(("agriculture_farm_operations",))["ok"])
PY
```

## Scope notes

- No shared generator, DSL, or progress-ledger files are changed.
- No external integrations or stream-engine picker are introduced.
- The standalone slice is intentionally centered on crop planning, assistant planning, and workbench execution rather than the full agriculture backlog.
