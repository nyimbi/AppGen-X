# General Ledger Core Release Evidence

Directory: `src/pyAppGen/pbcs/gl_core`

## Package Additions

- `repository.py` provides package-local database write plans and stateful row
  persistence for chart accounts, periods, journal drafts, semantic source
  documents, reconciliation cases, and close snapshots.
- `standalone.py` bootstraps a one-PBC GL app surface, loads demo finance
  workspace state, dispatches package routes, and renders the workbench shell.
- `ui.py` now exposes explicit forms, wizards, controls, and standalone shell
  metadata for operator workflows.
- Package docs now include `README.md`, `implementation-plan.md`,
  `implementation-status.md`, `SPECIFICATION.md`, and this release evidence
  file.

## Repo Gate Proxies

### `pbc_source_artifact_contract`

- Verified through package artifact existence plus schema/model/repository
  evidence.

### `pbc_implementation_release_audit`

- Verified through runtime release evidence, executable service/route/event/UI
  contracts, agent contribution, and repository coverage.

### `pbc_generation_smoke_audit`

- Verified through runtime smoke, repository smoke, and standalone app smoke.

## Focused Evidence Files

- `tests/test_contract.py`
- `tests/test_standalone.py`
- `implementation-status.md`
- `release_evidence.py`
