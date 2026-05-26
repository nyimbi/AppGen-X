# Repo Cleanup Archive - 2026-05-26 8

This archive records generated Python bytecode caches moved out of the active
source tree during the repository cleanup pass.

Moved out of the active tree:

- `src/pyAppGen/**/__pycache__/`
- `src/pyAppGen/pbcs/**/__pycache__/`
- `src/pyAppGen/pbcs/*/tests/**/__pycache__/`

Archive payloads:

- `runtime-cache/` contains the first directory-level cache move.
- `regenerated-runtime-cache/` contains bytecode regenerated during inspection.
- `final-runtime-cache/` contains the final file-level cache sweep.

The cache payload is generated runtime metadata and remains intentionally
ignored. This manifest is tracked so the cleanup decision and archive location
remain auditable.
