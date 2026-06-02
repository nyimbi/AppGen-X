# Release Evidence - Clinical Care Coordination

Package directory: `pbcs/clinical_care_coordination`.

This PBC now includes owned schema, migration DDL, models, services, routes, events, handlers, queue-oriented UI workbench surfaces, agent skills, permissions, configuration, a package-local standalone one-PBC app, focused tests, and release evidence.

## Evidence

- Release evidence contracts are materialized for schema, services, routes, events, handlers, UI, agent planning, governance, single-PBC app, and standalone app readiness.
- Owned datastore boundary remains package-local: every owned table starts with `clinical_care_coordination_` and cross-PBC interaction uses AppGen-X events or declared APIs.
- Event contract remains AppGen-X outbox/inbox with retry and dead-letter evidence.
- Standalone app evidence proves the package can bootstrap a demo care-coordination workspace, render the workbench shell, and expose release snapshots without shared generator changes.
- Focused package tests cover contract surfaces, the executable care-coordination slice, and standalone app behavior.

## Validation Commands

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
