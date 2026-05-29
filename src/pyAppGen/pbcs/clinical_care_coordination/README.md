# Clinical Care Coordination

`clinical_care_coordination` is a standalone AppGen-X packaged business capability for longitudinal patient care coordination. This package owns its schema contracts, executable runtime, stateful service layer, API routes, queue-oriented workbench UI, forms, wizards, controls, AppGen-X event contract, governed assistant planning surface, standalone one-PBC app, focused tests, and release evidence.

## What This Package Provides

- A package-local care coordination slice in `care_coordination_app.py` for care plans, care-team rostering, referrals, encounter-derived tasks, care gaps, transition packets, outcome measures, workbench queues, and assistant mutation planning.
- Executable service and route layers that dispatch real package-local workflows rather than only exposing generated manifests.
- A standalone one-PBC app in `standalone.py` that bootstraps a demo patient workspace, dispatches package routes, renders the command-center workbench, and exposes a release snapshot.
- UI contracts for the command center plus explicit forms, wizards, reusable controls, and a standalone shell contract.
- Deterministic governance and agent planning helpers for rules, document instructions, CRUD preview, and owned-table boundary enforcement.

## Key Entrypoints

- Runtime: `runtime.py`
- Domain slice: `care_coordination_app.py`
- Services: `services.py`
- Routes: `routes.py`
- UI/workbench: `ui.py`
- Standalone app: `standalone.py`
- Agent planning: `agent.py`
- Release audit: `release_evidence.py`

## Validation

Focused package validation for this standalone slice:

```bash
python3 -m py_compile src/pyAppGen/pbcs/clinical_care_coordination/*.py \
  src/pyAppGen/pbcs/clinical_care_coordination/tests/test_standalone.py
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q \
  src/pyAppGen/pbcs/clinical_care_coordination/tests
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c \
  "from pyAppGen.pbc import pbc_implementation_release_audit; print(pbc_implementation_release_audit(('clinical_care_coordination',))['ok'])"
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/python -c \
  "from pyAppGen.pbc import pbc_generation_smoke_audit; print(pbc_generation_smoke_audit(('clinical_care_coordination',))['ok'])"
```
