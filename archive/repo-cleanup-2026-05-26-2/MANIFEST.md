# Repo Cleanup Archive - 2026-05-26

## Scope

This archive batch contains runtime cache artifacts moved out of the active
workspace during repository cleanup.

Archived active artifacts:

- Root `.pytest_cache` from focused verification runs.
- Python `__pycache__` directories under `src/pyAppGen`.
- Python `__pycache__` directories under `src/pyAppGen/pbcs`.
- Python `__pycache__` directories under `tests`.

Inventory at archive time:

- 50 active `__pycache__` directories moved.
- 157 cache files moved.

Post-verification cleanup:

- Focused verification regenerated the same cache family.
- 50 regenerated `__pycache__` directories moved to `post-verify-cache`.
- 157 regenerated cache files moved to `post-verify-cache`.

Generated history verification cleanup:

- Focused generated-app verification regenerated the same cache family.
- Regenerated cache artifacts moved to `post-version-history-cache`.

Procurement verification cleanup:

- Follow-on PBC verification regenerated a small cache subset.
- Regenerated cache artifacts moved to `post-procurement-cache`.

Wizard verification cleanup:

- Focused generated-app verification regenerated Python import/test caches.
- Regenerated cache artifacts moved to `post-wizard-cache` and
  `post-wizard-cache-2`.

## Rationale

These files are generated interpreter/test-run artifacts. They are not source
contracts, documentation, generated application templates, PBC package source,
or required test fixtures.

## Restore

Restore only if a diagnostic run specifically needs the original cache state.
Normal test and generation workflows recreate these artifacts automatically.
