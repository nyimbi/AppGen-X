# Release Evidence - Student Financial Aid

Package directory: `src/pyAppGen/pbcs/student_financial_aid`.

## Release audits covered

- `pbc_source_artifact_contract`
- `pbc_implementation_release_audit`
- `pbc_generation_smoke_audit`

## Evidence summary

- Owned schema, migration, models, services, routes, events, handlers, UI surfaces, governed agent previews, permissions, configuration hooks, seed plan, package metadata, and focused tests all live inside the PBC directory.
- Public contracts keep AppGen-X as the only event contract, keep stream-engine pickers hidden, and limit database backends to PostgreSQL, MySQL, and MariaDB.
- Workflow coverage includes aid year setup, aid profile intake, FAFSA/ISIR-equivalent application capture, dependency and verification review, document tracking, SAP, cost-of-attendance budgeting, need analysis, packaging, disbursement scheduling, refund/return and overaward review, professional judgment, appeals, compliance, and communications.
- Governed assistant previews are limited to owned tables and require confirmation for mutations.

## Suggested validation commands

```bash
python3 -m compileall src/pyAppGen/pbcs/student_financial_aid
PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/student_financial_aid/tests tests/test_pbc_student_financial_aid_runtime.py
git diff --check
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
print("source", pbc_source_artifact_release_audit(key)["ok"])
print("spec", pbc_specification_release_audit(key)["ok"])
print("agent", pbc_agent_capability_release_audit(key)["ok"])
print("implementation", pbc_implementation_release_audit(key)["ok"])
print("capability", pbc_implemented_capability_audit(key)["ok"])
print("generation", pbc_generation_smoke_audit(key)["ok"])
PY
```

Exact command outputs are recorded in `implementation-status.md`.
