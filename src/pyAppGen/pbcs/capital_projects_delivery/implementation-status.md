# Implementation Status

## Status

Completed a real capital project stage-gate improvement slice inside
`capital_projects_delivery`.

## Implemented

- Governed capital project lifecycle stages from `idea` through `closeout`.
- Executable gate checklist recording and approval logic.
- Invalid transition rejection with `CapitalProjectsDeliveryExceptionOpened`.
- Rollback handling that requires a rebaseline reason.
- Single-PBC app contract covering:
  - database-backed owned tables, migrations, and model contracts,
  - forms, wizards, controls, workbench, services, routes, and agent help.

## Code Review Pass

Reviewed the service/runtime integration after the first test run. Fixed one
real issue: `approve_capital_project_gate` was being intercepted by the generic
domain-depth fallback in `services.py`, which prevented state mutation during
route-driven approvals. The service now executes runtime-backed lifecycle
commands before falling back to generic domain-depth planning.

## Validation Evidence

Command:
`python3 -c "import importlib, inspect, sys, traceback; sys.path.insert(0, 'src'); modules=['pyAppGen.pbcs.capital_projects_delivery.tests.test_contract','pyAppGen.pbcs.capital_projects_delivery.tests.test_lifecycle_app_slice']; failed=[]; total=0
for mod_name in modules:
    mod=importlib.import_module(mod_name)
    for name, fn in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith('test_'):
            total += 1
            try:
                fn()
                print(f'PASS {mod_name}:{name}')
            except Exception as exc:
                failed.append((mod_name, name, exc))
                print(f'FAIL {mod_name}:{name} -> {exc.__class__.__name__}: {exc}')
                traceback.print_exc()
print(f'TOTAL {total}')
print(f'FAILED {len(failed)}')
sys.exit(1 if failed else 0)"`

Result:
- `TOTAL 12`
- `FAILED 0`

Command:
`python3 -c "import sys; sys.path.insert(0,'src'); from pyAppGen.pbcs.capital_projects_delivery import smoke_test, implementation_contract; from pyAppGen.pbcs.capital_projects_delivery.services import smoke_test as service_smoke; from pyAppGen.pbcs.capital_projects_delivery.routes import smoke_test as route_smoke; from pyAppGen.pbcs.capital_projects_delivery.ui import smoke_test as ui_smoke; result={'package_smoke': smoke_test()['ok'], 'service_smoke': service_smoke()['ok'], 'route_smoke': route_smoke()['ok'], 'ui_smoke': ui_smoke()['ok'], 'single_pbc_app': implementation_contract()['single_pbc_app_contract']['ok']}; print(result); raise SystemExit(0 if all(result.values()) else 1)"`

Result:
- `{'package_smoke': True, 'service_smoke': True, 'route_smoke': True, 'ui_smoke': True, 'single_pbc_app': True}`

Command:
`git diff --check -- src/pyAppGen/pbcs/capital_projects_delivery`

Result:
- no output
- exit code `0`

## Changed Files

- `RELEASE_EVIDENCE.md`
- `SPECIFICATION.md`
- `README.md`
- `__init__.py`
- `agent.py`
- `config.py`
- `domain_depth.py`
- `implementation-plan.md`
- `lifecycle.py`
- `manifest.py`
- `migrations/001_initial.sql`
- `models.py`
- `routes.py`
- `runtime.py`
- `seed_data.py`
- `services.py`
- `tests/test_contract.py`
- `tests/test_lifecycle_app_slice.py`
- `ui.py`

## Constraints Confirmed

- No edits were made outside `src/pyAppGen/pbcs/capital_projects_delivery`.
- Eventing remains AppGen-X only.
- No stream-engine picker was introduced.
- No shared table access was introduced.
- Nothing was staged, committed, or pushed.
