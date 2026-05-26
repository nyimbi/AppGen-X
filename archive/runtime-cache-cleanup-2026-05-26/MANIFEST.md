# Runtime Cache Cleanup - 2026-05-26

This archive bucket holds local runtime cache artifacts moved out of the active
repository tree during cleanup.

Moved artifacts:

- `.pytest_cache/`
- 50 `__pycache__/` directories from `src/` and `tests/`
- `regenerated-cache/` contains cache directories produced by verification
  imports and then moved out of the active tree again.

Rationale:

- Python bytecode and pytest cache data are generated runtime artifacts.
- These files are not source inputs for packaging, tests, documentation, or the
  frontend.
- The project already ignores these cache paths, so keeping them in the active
  tree adds noise without preserving useful source history.

Verification:

- Active tree scan after the move found no `__pycache__/` directories outside
  `.venv` and `archive`.
- `.venv/` was left in place because it is the current local verification
  environment.
- `py_compile` completed for `src/pyAppGen/gen.py` and `tests/test_main.py`.
- Import smoke completed for `pyAppGen`, `pyAppGen.schema`, and `pyAppGen.gen`.
- A focused pytest run was attempted but stopped after it exceeded the useful
  cleanup-pass wait time without completing.
