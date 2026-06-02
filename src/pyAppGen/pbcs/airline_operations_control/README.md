# Airline Operations Control

`airline_operations_control` now ships as a package-local standalone AppGen-X slice for airline OCC workbench operations. The implemented one-PBC app surface stays entirely inside `src/pyAppGen/pbcs/airline_operations_control` and covers authoritative flight-leg timelines, tail continuity, crew/disruption/passenger recovery planning, governed decision capture, assistant document-intake planning, and release evidence.

## Implemented Standalone Slice

The standalone slice is executable through:

- `standalone.py`: one-PBC app bootstrap, route dispatch, demo workspace loading, workbench rendering, and release snapshot generation.
- `runtime.py`: owned state, schema/service/API contracts, flight-leg and rotation logic, crew/disruption/reaccommodation/decision workflows, permissions, and release evidence.
- `services.py` and `routes.py`: stateful service execution and dispatchable package-local API routes.
- `ui.py`: workbench fragments, forms, wizards, controls, role views, and standalone shell rendering.
- `agent.py`: assistant namespace, document-instruction planning, governed CRUD previews, and rotation-recovery support.

## Functional Surface

The delivered app surface includes:

- Models/schema contracts for all owned tables and package-local event tables.
- Stateful services and routes for runtime configuration, flight legs, rotations, crew pairings, disruptions, reaccommodation plans, operations decisions, delay codes, and recovery workflows.
- A role-aware workbench with timeline, tail graph, attention queue, turn watchlist, assistant planning drawer, and release evidence drawer.
- Rules, bounded parameters, permissions, AppGen-X events/handlers, and standalone release evidence scenario packs.
- AI assistant document-instruction intake that maps notes into candidate tables and CRUD previews without mutating foreign tables.

## Main Entry Points

- `AirlineOperationsControlStandaloneApp().load_demo_workspace()`
- `AirlineOperationsControlStandaloneApp().render_workbench(tenant=...)`
- `routes.dispatch_route(method, path, payload, service=...)`
- `AirlineOperationsControlService().query_workbench(...)`
- `airline_operations_control_render_standalone_app(state, tenant=..., principal_permissions=...)`
- `document_instruction_plan(document, instruction)`

## Focused Validation

Commands used for this standalone slice:

```bash
python3 -m py_compile src/pyAppGen/pbcs/airline_operations_control/*.py \
  src/pyAppGen/pbcs/airline_operations_control/tests/*.py

python3 -m compileall src/pyAppGen/pbcs/airline_operations_control

PYTHONPATH=src python3 - <<'PY'
import importlib
modules = [
    'pyAppGen.pbcs.airline_operations_control.tests.test_contract',
    'pyAppGen.pbcs.airline_operations_control.tests.test_standalone',
]
for mod_name in modules:
    mod = importlib.import_module(mod_name)
    for name in sorted(dir(mod)):
        if name.startswith('test_') and callable(getattr(mod, name)):
            getattr(mod, name)()
print('package tests executed directly')
PY

PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbcs.airline_operations_control.capability_assurance import smoke_test as capability_smoke
from pyAppGen.pbcs.airline_operations_control.release_evidence import validate_release_evidence
from pyAppGen.pbcs.airline_operations_control.routes import validate_api_route_contracts
from pyAppGen.pbcs.airline_operations_control.runtime import airline_operations_control_runtime_smoke
from pyAppGen.pbcs.airline_operations_control.standalone import smoke_test as standalone_smoke
print({
    'capability_assurance': capability_smoke()['ok'],
    'route_contracts': validate_api_route_contracts()['ok'],
    'release_evidence': validate_release_evidence()['ok'],
    'runtime_smoke': airline_operations_control_runtime_smoke()['ok'],
    'standalone_smoke': standalone_smoke()['ok'],
})
PY
```

Note: `pytest` entrypoints in this environment were broken, so the package test modules were executed directly under `python3` instead.

## Deferred Backlog

Still deferred from `improve1.md` after this standalone slice:

- deeper crew legality horizon modeling
- maintenance overlays on aircraft availability
- slot and curfew protection
- ATC/weather/NOTAM fusion beyond disruption intake dedupe
- advanced reaccommodation boundary automation
- cancellation decision economics
