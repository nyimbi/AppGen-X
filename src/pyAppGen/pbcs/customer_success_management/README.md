# Customer Success Management

`customer_success_management` is a package-local standalone PBC app. It owns its datastore schema, executable service surface, route contracts, AppGen-X events, idempotent handlers, UI/workbench definitions, forms, wizards, controls, agent planning helpers, release audits, and focused tests without depending on other PBC internals.

## What is implemented

- Owned SQLite-backed standalone app in [slice_app.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/slice_app.py)
- Owned schema and migration for 22 domain tables plus AppGen-X outbox/inbox/dead-letter tables
- Executable customer-success operations for accounts, plans, onboarding, touchpoints, health, playbooks, escalations, renewals, expansion, EBRs, objectives, value, churn, exceptions, rules, and simulations
- Package-local route dispatch, service contracts, touchpoint-aware UI workbench, forms, wizards, controls, and agent CRUD/document planning
- Release audits for `pbc_source_artifact_contract`, `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit`

## Quick package validation

```bash
PYTHONPATH=src ./.venv/bin/pytest src/pyAppGen/pbcs/customer_success_management/tests
PYTHONPATH=src ./.venv/bin/python -m py_compile src/pyAppGen/pbcs/customer_success_management/*.py
PYTHONPATH=src ./.venv/bin/python - <<'PY'
from pyAppGen.pbcs.customer_success_management.release_evidence import build_release_evidence
evidence = build_release_evidence()
print(evidence["ok"])
print([check["id"] for check in evidence["checks"]])
PY
```

## Main entry points

- Contracts: [schema_contract.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/schema_contract.py), [service_contract.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/service_contract.py), [routes.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/routes.py)
- Runtime: [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/runtime.py)
- Standalone app: [slice_app.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/slice_app.py)
- Release evidence: [release_evidence.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/release_evidence.py), [RELEASE_EVIDENCE.md](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/RELEASE_EVIDENCE.md)
- Focused tests: [tests/test_contract.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/tests/test_contract.py), [tests/test_slice_app.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/customer_success_management/tests/test_slice_app.py)
