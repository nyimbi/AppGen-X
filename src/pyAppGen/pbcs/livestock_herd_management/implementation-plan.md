# Livestock Herd Management Implementation Plan

## Objective

Implement a domain-deep standalone one-PBC slice inside
`src/pyAppGen/pbcs/livestock_herd_management` without touching shared generator
code, language files, or the progress ledger.

## Package-Local Workstreams

1. Standalone executable domain shell
   - Add `standalone.py` with mutable package-local state for animals, herd
     groups, breeding, pregnancy, calving, treatments, vaccinations, feed,
     grazing, weights, genetics, movement permits, quarantine, biosecurity,
     traceability, welfare, mortality, inventory yield, analytics, and
     assistant previews.
   - Provide demo bootstrap, workbench rendering, validation, and smoke paths.

2. Operator workflow surface
   - Add `forms.py` for animal intake, herd assignment, breeding, calving,
     health interventions, feed/grazing, movement/biosecurity, welfare/yield,
     and assistant CRUD previews.
   - Add `wizards.py` for new-arrival onboarding, breed-to-calve, health
     campaigns, pasture-to-productivity, movement release, and assistant
     preview workflows.
   - Add `controls.py` for release readiness, biosecurity, traceability,
     welfare/withdrawal, and assistant guardrails.

3. Local contract convergence
   - Update `ui.py` to expose forms, wizards, controls, cards, queues, and the
     standalone app shell.
   - Update `manifest.py`, `release_evidence.py`, and `__init__.py` to publish
     the standalone slice in package metadata and release evidence.

4. Documentation and proof
   - Add `README.md`, `implementation-plan.md`, and `implementation-status.md`.
   - Add `tests/test_standalone.py` and run package-local compile/import checks.

## Validation Plan

- `python3 -m compileall src/pyAppGen/pbcs/livestock_herd_management`
- `PYTHONPATH=src python3 -m pytest src/pyAppGen/pbcs/livestock_herd_management/tests/test_contract.py src/pyAppGen/pbcs/livestock_herd_management/tests/test_standalone.py`
- If `pytest` is unavailable, run the same test functions through a direct
  import harness.
