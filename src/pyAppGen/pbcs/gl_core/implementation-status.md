# GL Core Implementation Status

## Status

Implemented package-local convergence toward a standalone one-PBC GL app.

## Completed

- Aligned manifest, event contracts, handler metadata, governance hooks, and
  permissions with the runtime’s real GL event topic, event types, and
  command permissions.
- Added a database-backed repository layer in `repository.py` for core GL
  records and SQL write-plan generation.
- Upgraded `services.py` and `routes.py` into executable package-local runtime
  dispatch instead of planning-only metadata.
- Added standalone app orchestration in `standalone.py`.
- Added workbench forms, wizards, controls, and standalone shell metadata in
  `ui.py`.
- Strengthened `agent.py` so finance instruction intake resolves to GL-owned
  forms, controls, routes, and suggested ledger actions.
- Refreshed release evidence and added `README.md`, `implementation-plan.md`,
  `implementation-status.md`, and focused standalone tests.

## Remaining Risks

- Validation remains package-local and synthetic; the standalone app proves
  owned-slice behavior without wiring a live database server or HTTP process.
- Global repo integration tests outside `gl_core` were intentionally not edited
  in this slice and may continue to reflect broader repository drift.

## Repo Gates

- `pbc_source_artifact_contract`: covered by package artifact checks plus
  schema/model/repository proof.
- `pbc_implementation_release_audit`: covered by runtime-driven service,
  route, event, UI, agent, and repository evidence.
- `pbc_generation_smoke_audit`: covered by runtime smoke, repository smoke,
  and standalone app bootstrap/render smoke.

## 2026-05-30 Domain Behavior Traceability Slice

- Expanded `tests/test_domain_behavior.py` to prove the GL Core PBC executes standalone app flows, repository-backed journals, route dispatch, assistant document/CRUD planning, retry/dead-letter handling, owned-boundary enforcement, configuration rejection, advanced finance controls, audit proofs, resilience drills, private consolidation proofs, reconciliation game resolution, and release evidence.
- Updated `IMPROVE1_TRACEABILITY.md` so every improve1 row cites the expanded executable domain behavior proof.

Validation evidence:

- `/Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/gl_core/tests`
  Result: `22 passed in 1.11s`.
