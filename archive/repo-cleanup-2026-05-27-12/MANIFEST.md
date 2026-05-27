# Repository Cleanup 2026-05-27 12

Scope:

- Moved active generated Python runtime caches from the repository source and
  test trees into `runtime-cache/`.
- Moved the root pytest cache into `runtime-cache/root/pytest-cache/`.
- Left source, tests, docs, frontend code, and in-progress PBC edits untouched.

Inventory:

- `97` active `__pycache__` directories were archived.
- `858` generated cache files were moved into this archive bucket.
- Verification regenerated `96` `__pycache__` directories containing `848`
  generated cache files; those were moved into `runtime-cache-post-verify/`.

Restore:

- Restore only if local debugging needs the exact pre-cleanup bytecode cache.
- These files are generated artifacts and are not required for normal builds,
  tests, packaging, or development.
