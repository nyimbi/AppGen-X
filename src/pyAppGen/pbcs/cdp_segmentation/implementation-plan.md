# CDP Segmentation Implementation Plan

## Scope

- Keep all edits inside `src/pyAppGen/pbcs/cdp_segmentation`.
- Deliver one executable in-memory CDP segmentation slice instead of broad generated placeholder coverage.
- Preserve owned-table boundaries and AppGen-X-only eventing.

## Domain Slice Chosen

1. Consent-aware customer event ingestion and profile/property stitching
2. Segment definition, evaluation, transition tracking, and activation readiness
3. Analyst workbench, document-instruction guidance, RBAC/governance, and release evidence

## Planned Code Changes

- Harden `runtime.py` so membership evaluation records consent-aware transitions, activation evidence, and richer workbench analytics.
- Align `services.py`, `routes.py`, and `handlers.py` so explicit state can execute real runtime behavior while still supporting side-effect-free planning mode.
- Replace `permissions.py` and `config.py` with slice-specific RBAC, runtime configuration, parameter, and rule governance surfaces.
- Expand `ui.py` and `agent.py` with CDP-specific forms, wizards, controls, and document-instruction CRUD guidance.
- Replace `release_evidence.py` with package-local aggregation over runtime, UI, agent, routes, handlers, docs, and tests.
- Add `README.md`, `implementation-status.md`, and focused execution tests.

## Verification Plan

- Run `python3 -m py_compile` across modified package files.
- Run package-local smoke paths via `python3` imports/calls because `pytest` is not installed in this environment.
- If feasible later in the repo environment, run `python3 -m pytest -q src/pyAppGen/pbcs/cdp_segmentation/tests`.
