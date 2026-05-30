# Healthcare Claims Adjudication Implementation Status

## Status

Standalone PBC implementation completed on branch `pbc/claims-adjudication-healthcare-standalone`.

## Completed Work

- Added `standalone.py` with improve1-mapped forms, wizards, controls, declared projection dependencies, executable adjudication helpers, route contracts, DSL exposure, and a full simulation.
- Wired standalone evidence into `__init__.py`, `ui.py`, `routes.py`, `agent.py`, and `release_evidence.py`.
- Added `tests/test_standalone_app.py` covering improve1 surface coverage, owned tables, eventing, adjudication helpers, boundary guards, routes, release evidence, agent contribution, and package smoke.
- Refreshed README, implementation plan, and this status file inside the PBC directory.

## Boundary

The PBC owns claims, claim lines, coding reviews, benefit rules, denials, appeals, payment integrity cases, policy/rule/configuration/control/governed-model records, and AppGen-X event tables. It does not own enrollment, provider, authorization, accumulator, fee schedule, pharmacy, clinical EHR, or audit source-of-truth tables.

## Known Gaps

The slice is side-effect-free and package-local; it does not exercise live clearinghouse feeds, real payer pricing systems, or live PostgreSQL/MySQL/MariaDB instances.
