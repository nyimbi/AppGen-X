# Repository Cleanup Archive - 2026-05-26

This archive holds files moved out of the active repository surface during the
2026-05-26 hygiene pass. The goal is to keep inactive generated samples, IDE
metadata, and draft documents recoverable without leaving them in active source,
test, or documentation paths.

## Moved Tracked Folders

- `src/pyAppGen/tmp/` -> `archive/repo-cleanup-2026-05-26/tracked/src-pyAppGen-tmp/`
  - Package exclusion evidence: `pyproject.toml` excludes `src/pyAppGen/tmp/**`.
  - Reference scan evidence: no active `src`, `tests`, `docs`, `README.md`,
    `noxfile.py`, `.github`, or frontend references outside the package
    exclusion entry.
  - Contents are generated scratch models, views, API files, and DBML samples.

- `tmp/test_app/` -> `archive/repo-cleanup-2026-05-26/tracked/tmp-test-app/`
  - Package exclusion evidence: `pyproject.toml` excludes `tmp/**`.
  - Reference scan evidence: no active source, tests, docs, README, build, or
    frontend references.
  - Contents are generated sample app output and old generated app artifacts.

- `.idea/` -> `archive/repo-cleanup-2026-05-26/tracked/idea/`
  - Package exclusion evidence: `pyproject.toml` excludes `.idea/**`.
  - Runtime relevance: IDE metadata is not part of package, runtime, generated
    app, DSL, or documentation behavior.
  - Note: `.idea/inspectionProfiles/Project_Default.xml` was already missing
    before this archive pass and remains recorded as a deletion in git.

## Moved Untracked Drafts

- `docs/PBC-list.md`
- `docs/PBC-list1.md`
- `docs/pbc/`
- `docs/pbc_prompt.md`

These files were untracked draft PBC notes. They were moved under
`archive/repo-cleanup-2026-05-26/untracked-docs/` so they remain recoverable
without competing with the tracked platform documentation set.

## Intentionally Not Archived Into Git

Runtime caches such as `.pytest_cache/`, `__pycache__/`, and generated `.pyc`
files are ignored artifacts. They are not useful as archival source material and
should not be staged.

## Verification

- `rg` scan found no active references to the moved tracked sample folders.
- The moved tracked folders are excluded from package builds in `pyproject.toml`.
- This pass does not alter source package code, generated runtime code, or test
  behavior.
