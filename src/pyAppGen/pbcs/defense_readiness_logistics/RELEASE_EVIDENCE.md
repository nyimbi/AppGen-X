# Release Evidence - Defense Readiness Logistics

Package directory: `src/pyAppGen/pbcs/defense_readiness_logistics`

## Evidence Summary

- Schema, models, and `migrations/001_initial.sql` now describe the same owned domain tables and domain-specific columns.
- Services execute real standalone commands and workflows instead of placeholder operation manifests.
- Routes dispatch to live service operations for readiness, assets, supply, maintenance, deployment release, and the workbench.
- AppGen-X outbox, inbox, and dead-letter contracts are explicit and covered by focused tests.
- Workbench, forms, wizards, controls, assistant skills, rules, parameters, and seed data are all represented in release evidence.
- End-to-end package smoke covers readiness validation, asset registration, maintenance projection, supply scoring, fuel sufficiency, deployment kit validation, movement release, mission capability, and deployment release.

## Validation Commands

```bash
python3 -m py_compile src/pyAppGen/pbcs/defense_readiness_logistics/*.py src/pyAppGen/pbcs/defense_readiness_logistics/tests/*.py
uv run --with pytest pytest -q src/pyAppGen/pbcs/defense_readiness_logistics/tests
python3 -m pyAppGen.pbcs.defense_readiness_logistics.tests.test_alignment
```

## Bounded Gaps

- Database execution remains package-local and deterministic; it does not open a live PostgreSQL/MySQL/MariaDB connection during package tests.
- External PBC collaboration is still represented through declared APIs and AppGen-X event contracts only.
