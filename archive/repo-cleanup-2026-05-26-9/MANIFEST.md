# Repo Cleanup Archive - 2026-05-26 Pass 9

This archive records a conservative cleanup pass that moved generated Python
bytecode cache artifacts out of the active source and test trees.

## Scope

- `src/**/__pycache__/`
- `tests/**/__pycache__/`

## Result

- Archived bytecode payloads under `archive/repo-cleanup-2026-05-26-9/`.
- Left source, tests, generated package code, and application behavior unchanged.
- Verified active `src/` and `tests/` trees contain no `__pycache__` directories
  and no files under `*/__pycache__/*` after the move.

The archived bytecode payload remains ignored by git; this manifest is the
tracked audit record for the cleanup.
