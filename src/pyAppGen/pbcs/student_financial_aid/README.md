# Student Financial Aid

`student_financial_aid` is a package-local standalone PBC app. It owns its datastore schema, executable service surface, route contracts, AppGen-X events, idempotent handlers, UI/workbench definitions, forms, wizards, controls, agent planning helpers, release audits, and focused tests without depending on shared generator internals.

## What is implemented

- Owned standalone slice app in `slice_app.py` backed by a package-local database harness for executable smoke coverage while public contracts stay limited to PostgreSQL, MySQL, and MariaDB.
- Owned schema and migration for aid years, aid profiles, applications, dependency reviews, verification items, document tracking, SAP, cost of attendance, need analysis, packaging, award lines, scholarships, grants, loans, work study, disbursements, refund/return cases, overawards, professional judgment, appeals, compliance, communications, policy/runtime/control artifacts, governed models, and AppGen-X event tables.
- Executable student-aid operations for aid year setup, profile intake, FAFSA/ISIR-equivalent application capture, dependency and verification review, document registration, SAP evaluation, cost-of-attendance budgeting, need analysis, packaging, disbursement scheduling, refund/return and overaward review, professional judgment, appeals, compliance tracking, and communications.
- Package-local route dispatch, service contracts, UI workbench, forms, wizards, controls, governed assistant document/CRUD previews, and release audits.
- Focused tests for contracts, workflow execution, workbench rendering, event idempotency, and release-audit gates.

## Quick package validation

```bash
python3 -m compileall src/pyAppGen/pbcs/student_financial_aid
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/student_financial_aid/tests tests/test_pbc_student_financial_aid_runtime.py
PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbc import (
    pbc_agent_capability_release_audit,
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_implemented_capability_audit,
    pbc_source_artifact_release_audit,
    pbc_specification_release_audit,
)
key = ("student_financial_aid",)
print(pbc_source_artifact_release_audit(key)["ok"])
print(pbc_specification_release_audit(key)["ok"])
print(pbc_agent_capability_release_audit(key)["ok"])
print(pbc_implementation_release_audit(key)["ok"])
print(pbc_implemented_capability_audit(key)["ok"])
print(pbc_generation_smoke_audit(key)["ok"])
PY
```

## Main entry points

- Contracts: `schema_contract.py`, `service_contract.py`, `routes.py`
- Runtime: `runtime.py`
- Standalone app: `slice_app.py`
- Release evidence: `release_evidence.py`, `RELEASE_EVIDENCE.md`
- Focused tests: `tests/test_contract.py`, `tests/test_slice_app.py`, `tests/test_pbc_student_financial_aid_runtime.py`

See `implementation-plan.md` for the chosen slice and `implementation-status.md` for verification evidence plus resolved code-review findings.
