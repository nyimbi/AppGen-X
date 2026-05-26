# Archived Tracked Workspace Artifacts

Date: 2026-05-26

This archive contains tracked files that were present in source-like locations
but are no longer part of the active platform runtime, tests, or packaged
distribution.

## Evidence

- `pyproject.toml` excludes `gen/**`, `src/newAppGen/**`,
  `src/pyAppGen/tmp/**`, and `tmp/**` from built packages.
- Repository search found no active source, test, README, or docs references to
  the archived import paths or sample folders.
- Dirty generated folders were left in place for a separate pass:
  `src/pyAppGen/tmp/` and `tmp/test_app/`.

## Archived Paths

- `gen/` -> `archive/tracked-unused-2026-05-26/gen/`
- `src/newAppGen/` -> `archive/tracked-unused-2026-05-26/newAppGen/`
- `lang/tmp/` -> `archive/tracked-unused-2026-05-26/lang-tmp/`
- `tmp/auplat/` -> `archive/tracked-unused-2026-05-26/auplat-sample/`
