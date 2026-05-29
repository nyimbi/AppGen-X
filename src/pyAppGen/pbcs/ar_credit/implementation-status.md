# Implementation Status

## Completed in This Slice

- Added a standalone one-PBC application surface in `standalone.py` with owned
  route dispatch, workbench rendering, control center checks, and release
  snapshot capture.
- Added `repository.py` to persist runtime snapshots, workflow runs, and
  release evidence in package-local SQLite tables.
- Added domain-specific `forms.py`, `wizards.py`, and `controls.py` for
  customer onboarding, invoice issue, cash application, collections recovery,
  and release readiness.
- Reworked `services.py`, `routes.py`, `events.py`, `handlers.py`,
  `config.py`, `permissions.py`, and `seed_data.py` so the standalone surface
  executes real AR behavior with AppGen-X-only eventing.
- Extended `ui.py`, `release_evidence.py`, and `__init__.py` so the standalone
  assets are exposed through package metadata, workbench contracts, and release
  readiness checks.
- Expanded package-local contract tests in `tests/test_contract.py` to cover
  repository, standalone app, forms, wizards, controls, and dynamic release
  evidence.

## Review Notes

- All edits remain inside `src/pyAppGen/pbcs/ar_credit`.
- The slice uses only owned AR tables plus package-local SQLite persistence for
  the standalone shell.
- AppGen-X remains the only event contract exposed by the implemented slice.
- No stream-engine selection, shared-table access, or new dependency was
  introduced.

## Validation Evidence

- Pending final compile and focused pytest run after the integration pass.
- Planned gates:
  - `python3 -m py_compile` across modified `ar_credit` Python modules.
  - `python3 -m pytest src/pyAppGen/pbcs/ar_credit/tests/test_contract.py -q`
  - Additional focused AR runtime/implementation tests if they pass without
    requiring edits outside this package.

## Remaining Depth for Later Slices

- Expand dispute resolution from recommendation-only into a full owned-case
  lifecycle.
- Add promise-to-pay tracking and collector work queues.
- Deepen credit policy compilation for temporary limits, authority bands, and
  review cadence.
- Extend the standalone repository to persist richer operator artifacts such as
  dispute evidence packs and statement exports.
