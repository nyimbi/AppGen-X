# Runtime Cache Cleanup 2026-05-26 3

This archive contains Python and pytest runtime caches produced while verifying
the native runtime contract and Asset Lifecycle package changes.

Moved out of active source/test paths:

- `.pytest_cache`
- `src/pyAppGen/**/__pycache__`
- `tests/__pycache__`

Validation after move:

- No active `.pytest_cache` or `__pycache__` directories remain outside
  `.venv`, `.git`, or `archive`.
