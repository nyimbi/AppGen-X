# Release Evidence - Gaming and Casino Operations

Package directory: `pbcs/gaming_casino_operations`.

This package now includes owned schema/migration/model alignment, executable services and routes, AppGen-X event handling, UI forms/wizards/controls, governed assistant skills, a package-local standalone app surface, and focused tests.

## Evidence sections

- schema, migrations, and model alignment
- service and route execution surfaces
- AppGen-X outbox/inbox/dead-letter evidence
- workbench, forms, wizards, and controls
- governed agent/chatbot skill contracts
- standalone app composition and package documentation artifacts

## Verification results

- `python3 -m py_compile $(rg --files src/pyAppGen/pbcs/gaming_casino_operations -g '*.py')` — passed
- direct package test harness over `tests/test_contract.py` and `tests/test_standalone.py` — passed (`12/12`)
- `pbc_source_artifact_contract("gaming_casino_operations")` — passed
- `pbc_implementation_release_audit(("gaming_casino_operations",))` — passed
- `gaming_casino_operations_runtime_smoke()` — passed
- `gaming_casino_operations_standalone_app_smoke()` — passed
- `smoke_test()` — passed

## Outstanding gap

- `pbc_generation_smoke_audit(("gaming_casino_operations",))` could not run successfully in this environment because `pyAppGen.dsl` imports `antlr4`, which is missing from the available interpreter, and the repo-managed `uv` runner is not installed in this worktree. The package-local direct smoke fallback above was used instead.
