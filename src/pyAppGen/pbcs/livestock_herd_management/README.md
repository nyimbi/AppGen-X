# Livestock Herd Management

`livestock_herd_management` now includes a package-local standalone AppGen-X
slice that runs entirely inside `src/pyAppGen/pbcs/livestock_herd_management`.
It stays within owned livestock records while exposing executable forms,
wizards, controls, a one-PBC app shell, release evidence, and focused tests.

## What The Standalone Slice Covers

- Animal registry with identifier continuity, provenance, genetics, and default
  herd placement.
- Herd groups, paddocks, grazing rotation, feed plans, weights, and product
  yield analytics.
- Breeding, pregnancy confirmation, calving, offspring linkage, and lineage.
- Health events, treatments, vaccinations, withdrawal controls, quarantine, and
  biosecurity release checks.
- Movement permits, traceability lots, welfare scoring, mortality handling, and
  assistant CRUD previews that remain confirmation-gated.

## Key Entrypoints

- `standalone.py` for the executable one-PBC app shell.
- `forms.py`, `wizards.py`, and `controls.py` for operator workflows.
- `ui.py` for workbench, cards, queues, and standalone shell metadata.
- `release_evidence.py` for package-local readiness proofs.
- `tests/test_standalone.py` for focused standalone validation.

## Validation Shape

- Demo bootstrap seeds a realistic herd with breeding, health, grazing,
  traceability, quarantine, biosecurity, welfare, and yield evidence.
- Assistant previews stay preview-only and reject foreign tables.
- Release evidence now includes standalone application and documentation gates.
