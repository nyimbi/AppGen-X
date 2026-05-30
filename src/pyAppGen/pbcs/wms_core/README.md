# Warehouse Management Core

`wms_core` is a standalone AppGen-X packaged business capability for warehouse execution. It owns warehouse masters, bin topology, inbound receipts, directed putaway, wave release, picking, packing, shipment proof, event reliability, and governance surfaces without reading foreign operational tables.

## Included surfaces

- Runtime, schema, service, route, event, handler, config, permission, agent, and seed-data contracts.
- A package-local repository in `repository.py` that backs database-oriented forms and read models using WMS-owned tables only.
- A standalone one-PBC app in `standalone.py` that bootstraps a warehouse, runs inbound-to-ship workflows, renders the workbench, and emits shipment-proof/control evidence.
- Workbench UI metadata in `ui.py` with explicit warehouse forms, wizards, controls, and assistant namespace wiring.
- Release evidence in `release_evidence.py` plus supporting package docs and focused tests.

## Standalone usage

```python
from pyAppGen.pbcs.wms_core.standalone import WmsCoreStandaloneApp

app = WmsCoreStandaloneApp()
app.load_demo_workspace(tenant="tenant_demo")
rendered = app.render_workbench(tenant="tenant_demo")
assert rendered["ok"] is True
```

## Key artifacts

- Standalone app: `standalone.py`
- Repository/read models: `repository.py`
- UI/forms/wizards/controls: `ui.py`
- Release evidence: `release_evidence.py` and `RELEASE_EVIDENCE.md`
- Status and plan: `implementation-plan.md`, `implementation-status.md`
- Focused tests: `tests/test_contract.py`, `tests/test_runtime_capabilities.py`, `tests/test_standalone.py`
