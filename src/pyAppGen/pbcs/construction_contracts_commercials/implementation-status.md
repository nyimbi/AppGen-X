# Construction Contracts and Commercials Implementation Status

## Completed

- Added a real standalone package-local store, service, route, UI, agent-workspace, and app-bootstrap surface on top of the executable construction-commercials core.
- Kept runtime, services, routes, UI, events, handlers, config, permissions, seed data, and manifest wrappers inside the PBC-owned boundary.
- Extended release evidence so it now proves standalone app coverage and package documentation presence.
- Added focused standalone tests for the store, route/UI/agent integration, release evidence, and package-local docs.

## Validation Evidence

- `python3 -m compileall src/pyAppGen/pbcs/construction_contracts_commercials`
- `pytest src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_contract.py src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_standalone.py`
- `PYTHONPATH=src python3 -c "from pyAppGen.pbcs.construction_contracts_commercials.standalone import construction_contracts_commercials_standalone_app_smoke; print(construction_contracts_commercials_standalone_app_smoke()['ok'])"`
- `PYTHONPATH=src python3 -c "from pyAppGen.pbcs.construction_contracts_commercials.release_evidence import validate_release_evidence; print(validate_release_evidence()['ok'])"`

## Pending / Risks

- The slice remains intentionally in-memory and contract-driven; it does not include a real persistence adapter or HTTP server binding inside this PBC.
- `SPECIFICATION.md` remains broader than the implemented executable subset and may still describe ambitions beyond the current standalone slice.
- Release evidence should be refreshed if additional standalone routes, forms, or governed operations are added later.

## improve1 Commercial Control Completion Pass

Added `commercial_control.py` as the package-local executable control layer for all 50 manually curated improve1 items. Each control now carries required construction-commercial evidence fields, owned-table targeting, AppGen-X event metadata, rule and parameter handles, retry/dead-letter evidence, agent skill exposure, UI route metadata, and package-boundary checks.

The new `tests/test_domain_behavior.py` proves all 50 controls execute side-effect-free and validates construction-specific failure modes for invalid contract lifecycle transitions, unsupported pricing bases, schedule-of-values overclaiming, uncertified payment event requests, unapproved variation value increases, missing lien waivers, unapproved agent review/CRUD, low-confidence document ingestion, unauthorized roles, unredacted contractor portal notes, and overlap with external schedule/cost/finance/document ownership. `core.py` and `runtime.py` now expose the commercial-control contract as release evidence, runtime smoke evidence, and 50 UI commercial-control panels.

Validation pending in this slice: focused construction-commercial tests, improve1 sweep, and `git diff --check`.
