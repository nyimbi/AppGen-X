# Repo Cleanup Archive - 2026-05-27

## Scope

This archive holds generated runtime cache directories moved out of the active
source and test tree during repo cleanup.

## Moved Items

- `96` live `__pycache__` directories from `src/` and `tests/`.
- Destination: `archive/repo-cleanup-2026-05-27-2/runtime-cache/`.
- `96` regenerated verification cache directories from `src/` and `tests/`.
- Destination:
  `archive/repo-cleanup-2026-05-27-2/runtime-cache-regenerated-after-verify/`.
- `92` subsequently regenerated PBC package cache directories.
- Destination: `archive/repo-cleanup-2026-05-27-2/runtime-cache-final-sweep/`.
- A single-package diagnostic cache move was retained under the same ignored
  `runtime-cache*` archive namespace while investigating immediate cache
  regeneration.
- Each archived directory is flattened by replacing path separators with
  `__`, preserving enough origin context for recovery.

## Kept Active

- Source code, tests, documentation, templates, frontend files, package
  metadata, and build configuration remain in their active locations.
- Existing in-flight PBC specification and traceability edits were not moved or
  modified by this cleanup pass.

## Verification

- Confirmed each sweep moved the then-present generated cache directories into
  the archive.
- Import verification passed after the first sweep and regenerated cache files,
  which were archived in follow-up sweeps.
- Active Python processes may regenerate ignored cache directories while they
  are running; those generated files remain excluded from source control by the
  existing ignore rules.
