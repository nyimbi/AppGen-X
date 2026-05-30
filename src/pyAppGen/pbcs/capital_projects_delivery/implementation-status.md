# Capital Projects Delivery Implementation Status

## Status

Completed package-local convergence of `capital_projects_delivery` into a standalone one-PBC AppGen-X app slice.

## Completed

- Added a standalone package entrypoint in `standalone.py` that bootstraps configuration, parameters, rules, demo tenant data, route dispatch, workbench rendering, and release snapshots inside this package.
- Extended the runtime contract with workflow descriptors, richer release evidence, standalone app metadata, and a stronger single-PBC app contract.
- Reworked services and routes so operation contracts, owned/read tables, permissions, events, and workflow/query surfaces align with executable behavior.
- Extended `ui.py` with standalone shell metadata, navigation, permission-aware rendering, workflow visibility, and workbench summary cards.
- Strengthened `agent.py` so document-intake and CRUD planning resolve to owned tables, candidate routes, permissions, idempotency keys, workflows, and AppGen-X event previews.
- Expanded permissions and release-evidence manifests, added standalone tests, refreshed `README.md`, and updated the package manifest to advertise the standalone surface.

## Simplifications Made

- Kept the domain scope anchored on the stage-gate lifecycle slice instead of broadening into new shared abstractions or cross-PBC integrations.
- Used deterministic package-local bootstrapping and demo data rather than introducing external services, live databases, or shared runtime dependencies.
- Installed temporary local audit dependencies only in a throwaway directory under the isolated worktree to run generation smoke, then removed that directory after validation.

## Validation Evidence

Command:
`python3 -m compileall src/pyAppGen/pbcs/capital_projects_delivery`

Result:
- exit code `0`
- package compiled successfully

Command:
`python3 - <<'PY' ... import/run test_ functions from test_contract.py, test_lifecycle_app_slice.py, test_standalone.py ... PY`

Result:
- `TOTAL 18`
- `FAILED 0`

Command:
`PYTHONPATH=/private/tmp/appgen-pbc-capital-projects-delivery-standalone/.audit_deps python3 - <<'PY' ... pbc_source_artifact_contract('capital_projects_delivery'); pbc_implementation_release_audit(('capital_projects_delivery',)); pbc_generation_smoke_audit(('capital_projects_delivery',)) ... PY`

Result:
- `source_ok=True`
- `release_ok=True`
- `generation_ok=True`
- `release_blocking_gaps=0`
- `generation_failed_checks=[]`

Command:
`git diff --check -- src/pyAppGen/pbcs/capital_projects_delivery`

Result:
- no output
- exit code `0`

## Changed Files

- `README.md`
- `RELEASE_EVIDENCE.md`
- `__init__.py`
- `agent.py`
- `implementation-plan.md`
- `implementation-status.md`
- `manifest.py`
- `permissions.py`
- `release_evidence.py`
- `routes.py`
- `runtime.py`
- `services.py`
- `standalone.py`
- `tests/test_contract.py`
- `tests/test_standalone.py`
- `ui.py`

## Remaining Risks

- Validation stayed focused on this PBC package. Broader repository regression, lint, and end-to-end suites outside `capital_projects_delivery` were not run.
- The standalone app remains a package-local deterministic shell rather than a live HTTP server or database-backed deployment target in this scope.
