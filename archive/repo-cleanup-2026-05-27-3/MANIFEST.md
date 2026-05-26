# Repository Cleanup Archive - 2026-05-27

Archived local runtime artifacts that are not source, documentation, tests, or frontend assets.

## Payload

- `runtime-cache/current-tree/` - first Python bytecode cache payload moved from active `src/` and `tests/` package trees.
- `runtime-cache/regenerated-after-cleanup/` - bytecode cache payload that reappeared during verification.
- `runtime-cache/final-regenerated-pass/` - final bytecode cache payload moved after the second scan.

## Rationale

- Keeps generated runtime cache files out of active source directories.
- Preserves the artifacts locally instead of deleting them.
- Leaves the local virtual environment in place so developer tooling continues to work.

## Verification

- Archived bytecode files across all cleanup passes: 2,600.
- Active tree bytecode files observed after final pass: 718; a local watcher or background import path appears to be regenerating ignored cache files.
- Tracked source files were not moved by this cleanup.
