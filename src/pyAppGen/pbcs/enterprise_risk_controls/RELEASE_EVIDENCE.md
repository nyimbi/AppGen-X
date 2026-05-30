# Enterprise Risk Controls Release Evidence

## Coverage

This package now exposes package-local evidence for:

- schema and owned-table boundaries,
- service and API contracts,
- AppGen-X events and idempotent handlers,
- workbench UI, forms, wizards, and controls,
- assistant preview guardrails,
- configuration, rules, parameters, and permissions,
- focused tests and package-local documentation.

## Primary Evidence Sources

- `release_evidence.py`
- `tests/test_contract.py`
- `tests/test_app_surface.py`
- `runtime.py`
- `services.py`, `routes.py`, `ui.py`, `agent.py`, `controls.py`

## Release Gate Expectation

The package is considered ready only when `validate_release_evidence()` passes, focused tests pass, and the package compiles without syntax errors.
