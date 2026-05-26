# Repository Cleanup Archive

Date: 2026-05-26

This archive contains tracked files that were safe to remove from the active
workspace because repository search found no active source, test, packaging,
or documentation-index references that require them at runtime.

## Evidence

- `docs/base_features.md` is the canonical base feature contract; the archived
  leading-space filename was a duplicate predecessor.
- `docs/Baseview_features.md` was not referenced by docs, tests, source, or the
  README.
- `req_all.txt` duplicated dependency intent outside the active
  `pyproject.toml`, lockfile, and `requirements.txt` surfaces.
- `print_schema.py` was an unreferenced standalone SQL graph helper.
- `src/pyAppGen/t2.py` and `src/pyAppGen/setup.py` were unreferenced legacy
  package modules and are not part of the current console entrypoint or
  generated application flow.
- Dirty IDE metadata, generated fixtures, and in-progress PBC files were left
  untouched.

## Archived Paths

- `docs/ base_features.md` -> `archive/cleanup-2026-05-26/docs/base_features-leading-space.md`
- `docs/Baseview_features.md` -> `archive/cleanup-2026-05-26/docs/baseview-features-stale.md`
- `req_all.txt` -> `archive/cleanup-2026-05-26/root/req_all.txt`
- `print_schema.py` -> `archive/cleanup-2026-05-26/root/print_schema.py`
- `src/pyAppGen/t2.py` -> `archive/cleanup-2026-05-26/src-pyAppGen/t2.py`
- `src/pyAppGen/setup.py` -> `archive/cleanup-2026-05-26/src-pyAppGen/setup.py`
