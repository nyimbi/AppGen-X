# Land and Real Estate Development

`land_real_estate_development` now includes a package-local standalone AppGen-X
slice for real land development operations inside this PBC boundary only.

## Implemented Slice

The standalone slice executes a realistic site progression:

- create a governed development project with explicit site-control thresholds,
- register parcels with APN, acreage, environmental limits, easements, and utility availability,
- track land acquisition and option clocks,
- run zoning, entitlement, permit, and site-plan readiness,
- calculate feasibility and residual land value versus seller pricing,
- gate construction readiness through risk controls,
- prepare sales and lease handoff readiness,
- preview assistant document-instruction and CRUD actions without mutating shared systems.

## Package-Local App Surfaces

The package exposes:

- `forms.py` for land control, parcel constraints, zoning, feasibility, and permit intake,
- `wizards.py` for diligence, entitlement/permitting, and investment-committee flows,
- `controls.py` for land control, environmental, utility, residual value, and handoff gates,
- `standalone.py` for the executable in-memory standalone app, service, routes, and workbench,
- `tests/test_standalone.py` for domain-deep package-local validation.

## Constraints Kept

- All edits stay inside `src/pyAppGen/pbcs/land_real_estate_development`.
- Eventing remains AppGen-X only.
- `stream_engine_picker_visible` remains `False`.
- `shared_table_access` remains `False`.
- Assistant mutations stay preview-only and owned-table scoped.

## Validation

Focused compile, pytest, standalone smoke, and release evidence validation are
recorded in `implementation-status.md`.
