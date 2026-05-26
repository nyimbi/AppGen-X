# Repo Cleanup Archive 2026-05-26-11

This archive slice contains tracked legacy artifacts that were present in the
active tree but are not referenced by packaging, runtime imports, tests, docs,
or the frontend workbench.

## Cleanup Plan

- Archive stale root template metadata that only records the original project
  scaffold inputs.
- Archive one-off operational shell scripts that hard-code an old host/database
  workflow and are not referenced by any active source, docs, tests, or CI file.
- Leave active source, docs, tests, frontend code, package configuration, and
  the local virtual environment in place.

## Archived Paths

| Original Path | Archived Path | Rationale |
| --- | --- | --- |
| `.cookiecutter.json` | `archive/repo-cleanup-2026-05-26-11/tracked/root/.cookiecutter.json` | Historical scaffold metadata from the original project template; no active references outside generated-app cookiecutter support, which is implemented separately in source code. |
| `src/pyAppGen/scripts/push_to_linode.sh` | `archive/repo-cleanup-2026-05-26-11/tracked/src-pyAppGen-scripts/push_to_linode.sh` | One-off deploy command with a hard-coded legacy remote path; no active references. |
| `src/pyAppGen/scripts/reset.sh` | `archive/repo-cleanup-2026-05-26-11/tracked/src-pyAppGen-scripts/reset.sh` | One-off database reset command with a hard-coded legacy database name; no active references. |

## Restore Notes

Restore any archived file by moving it back to the original path shown above and
rerunning the relevant focused verification.
