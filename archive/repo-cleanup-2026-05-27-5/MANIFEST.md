# Repo Cleanup Archive - 2026-05-27 Pass 5

## Scope

Moved Python runtime cache artifacts out of the active repository tree into:

- `archive/repo-cleanup-2026-05-27-5/runtime-cache/`
- `archive/repo-cleanup-2026-05-27-5/runtime-cache-post-verify/`
- `archive/repo-cleanup-2026-05-27-5/runtime-cache-final-sweep/`
- `archive/repo-cleanup-2026-05-27-5/runtime-cache-background-sweep/`

Moved regenerated local test output out of the active package tree into:

- `archive/repo-cleanup-2026-05-27-5/generated-test-output/`

## Archived Material

- Root `.pytest_cache`
- `tests/__pycache__`
- `src/pyAppGen/__pycache__`
- `src/pyAppGen/dsl_generated/lang/__pycache__`
- PBC package and package-local test `__pycache__` directories
- Regenerated `multi_sided_market` local test package output
- Regenerated `test_pbc_multi_sided_market_runtime.py` local test output

Initial archived runtime cache directories: 97.
Post-verification regenerated runtime cache directories: 92.
Final regenerated runtime cache directories: 4.
Background pytest regenerated runtime cache directories: 97.

## Retained In Place

- `.venv` remains in the workspace because it is a local development
  environment dependency, not project source.
- Active source, tests, docs, package metadata, frontend source, and generated
  DSL sources remain in place.

## Validation

- Active-tree cache scan returned no `.pytest_cache` or `__pycache__`
  directories outside `archive/`, `.git`, and `.venv`.
- Git status before this manifest showed only the existing in-flight source
  edits plus this new archive bucket.
- A focused source-package regression run passed after the cache move and its
  regenerated local output was moved into this archive bucket.
- A second active-tree cache scan after the regression run found regenerated
  PBC package bytecode and moved it into `runtime-cache-post-verify/`.
- A final active-tree cache scan moved the last four regenerated cache
  directories into `runtime-cache-final-sweep/`.
- A concurrent pytest process regenerated the package/test output once more;
  after it exited, its output was moved into `generated-test-output/` and its
  bytecode was moved into `runtime-cache-background-sweep/`.
