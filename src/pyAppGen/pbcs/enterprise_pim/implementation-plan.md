# Enterprise PIM Implementation Plan

## Objective

Turn `enterprise_pim` into a self-contained one-PBC application package that can be bootstrapped, seeded, driven through its owned routes and workflows, and inspected through package-local contracts, UI metadata, release evidence, and focused tests.

## Current Baseline

- `runtime.py` already contains rich domain behavior and an in-memory owned-state model.
- `services.py`, `routes.py`, `ui.py`, `events.py`, `handlers.py`, `agent.py`, `release_evidence.py`, and `seed_data.py` provide broad contract coverage.
- The main gap is execution: the package has planning metadata, but not a real standalone app harness that wires permissions, routes, runtime state, seed data, UI controls, and release evidence together.
- Evidence also needs to reflect actual package artifacts, especially migrations, standalone bootstrap, and focused tests.

## Delivery Plan

1. Add a package-local standalone app harness.
2. Provide executable bootstrap fixtures for configuration, parameters, rules, dependency schemas, and end-to-end seed steps.
3. Surface practical UI forms, wizards, and controls for taxonomy, localization, workflow, dependency, and publication operations.
4. Align permissions and release evidence with runtime behavior and actual package artifacts.
5. Add focused standalone tests and package-local docs (`README.md`, `implementation-status.md`).

## Constraints

- Edit only `src/pyAppGen/pbcs/enterprise_pim`.
- Keep the diff small and reversible.
- Preserve owned-table isolation and AppGen-X eventing.
- Do not add dependencies.

## Verification Plan

- `python3 -m compileall src/pyAppGen/pbcs/enterprise_pim`
- `python3 -m unittest discover -s src/pyAppGen/pbcs/enterprise_pim/tests -p 'test_standalone.py'`
- package-local smoke imports for `release_evidence`, `standalone`, and `seed_data`
