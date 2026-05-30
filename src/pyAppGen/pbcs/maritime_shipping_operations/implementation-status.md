# Maritime Shipping Operations Implementation Status

Status: implemented in standalone PBC slice.

## Completed

- Added forms, wizards, controls, standalone app, tests, README, and plan/status docs.
- Covered voyage legs, vessel readiness, cargo allocation, cutoffs, bills, stowage, DG/reefer controls, charter clauses, port-call SOF, laytime, demurrage, bunkers, carbon, compliance obligations, schedule simulations, and assistant previews.
- Integrated standalone evidence into UI, manifest, package contract, and release readiness.

## Evidence

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/maritime_shipping_operations`: passed.
- `PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/maritime_shipping_operations/tests`: 12 passed.
- `standalone_smoke_test()`: true.
- `validate_release_evidence()`: true.
- Focused source/package/spec/agent/implementation/capability/generation audits: true.
- `git diff --check -- src/pyAppGen/pbcs/maritime_shipping_operations`: clean.
- Commit: pending.
