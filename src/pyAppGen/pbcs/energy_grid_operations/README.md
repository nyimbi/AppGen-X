# Energy Grid Operations

`energy_grid_operations` is a standalone AppGen-X Packaged Business Capability for control-room grid operations. It owns feeder and substation assets, topology publication, switching order review, dispatch instructions, outage restoration state, reliability constraints, governance rules and parameters, assistant guidance, and release evidence without relying on foreign PBC tables.

## What This Package Provides

- An executable package-local runtime in `runtime.py` with owned state, AppGen-X eventing, rule evaluation, bounded parameters, and workbench projections.
- An executable standalone one-PBC app in `standalone.py` that bootstraps configuration, rules, parameters, demo data, and control-room workbench rendering.
- Grid-specific service, route, event, handler, UI, agent, and release-evidence contracts that align with the package's owned schema.
- Focused package tests for contract validation, event handling, route execution, and standalone smoke coverage.

## Standalone Surface

The standalone app exposes:

- Grid asset intake and feeder modeling
- Topology publication and reliability constraints
- Switching review with hold-point simulation
- Dispatch approval with conflict detection
- Outage restoration prioritization
- Governance rule, parameter, and release-evidence workbench surfaces

## Key Files

- `runtime.py`
- `services.py`
- `routes.py`
- `ui.py`
- `standalone.py`
- `release_evidence.py`
- `tests/test_contract.py`
- `tests/test_standalone.py`

See `implementation-plan.md` for the scoped implementation slice and `implementation-status.md` for the recorded execution outcomes and verification evidence.
