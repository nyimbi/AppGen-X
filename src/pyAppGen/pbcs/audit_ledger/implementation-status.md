# Implementation Status

## Completed in This Slice

- Added `implementation-plan.md` to pin the chosen backlog slice and
  verification scope before code changes.
- Added `ledger_proofs.py` with executable audit-ledger behavior for:
  canonical payload hashing, evidence-envelope validation, immutable
  correction planning, per-tenant chain proofs, disclosure minimization, and
  release notarization bundles.
- Wired the proof slice into `runtime.py` for real sealing, export planning,
  control checks, workbench proof summaries, and release evidence.
- Wired preview surfaces into `services.py`, `agent.py`, and `ui.py`.
- Attached the proof slice to `release_evidence.py` and exported it through
  the package contract in `__init__.py`.
- Added focused behavioral tests in
  `tests/test_pbc_audit_ledger_implementation.py`.

## Contract Alignment Fixes

- Corrected handler dead-letter table naming to
  `audit_ledger_dead_letter_event`.
- Expanded handler contracts to cover the full declared consumed-event set.
- Removed the service-layer fallback that incorrectly advertised emitted
  events for commands that do not emit.
- Aligned inbox/outbox/dead-letter runtime records with their owned schema
  fields.
- Added missing runtime metadata for audit events, signature-chain links,
  projection links, control assertions, and forensic export approval state.

## Validation Evidence

- `python3 -m compileall src/pyAppGen/pbcs/audit_ledger`
  Result: completed successfully.
- `./.venv/bin/pytest tests/test_pbc_audit_ledger_implementation.py tests/test_pbc_audit_ledger_runtime.py src/pyAppGen/pbcs/audit_ledger/tests/test_contract.py src/pyAppGen/pbcs/audit_ledger/tests/test_runtime_capabilities.py -q`
  Result: `18 passed in 0.72s`.

## Remaining Depth for Later Slices

- Add richer export chain-of-custody lifecycle states beyond initial
  preparation.
- Add retention conflict resolution and legal-hold workflows.
- Add deeper anomaly taxonomy and source-PBC evidence quality scoring.
- Add reviewer workspace and regulator-specific minimized evidence surfaces.
