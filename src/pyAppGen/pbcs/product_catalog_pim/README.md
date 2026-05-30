# Product Catalog PIM PBC

This package is a standalone AppGen-X Packaged Business Capability for product information management. It owns product family, product master, variant, taxonomy, attribute schema, enrichment, localized content, media reference, price metadata, compliance, publication, event, rule, parameter, configuration, control, agent, and workbench records.

The runtime deployment database backends remain limited to PostgreSQL, MySQL, and MariaDB. The package-local SQLite repository is only a deterministic test/demo harness for one-PBC application execution.

## Standalone application surface

- `repository.py` persists runtime state, form submissions, workflow runs, control executions, agent sessions, and a workbench read model.
- `standalone.py` bootstraps a one-PBC application with seed data and smoke evidence.
- `services.py` exposes standalone commands and queries for demo seeding, workbench reads, product registration, localized content, publication, and publication proofs.
- `routes.py` dispatches app-local routes without exposing stream-engine choices.
- `ui.py` defines forms, wizards, controls, and renderable workbench cards for catalog operators.
- `agent.py` adds document-intake, wizard matching, governed CRUD planning, and route candidates to the composed application assistant.

## Build and verify

Use `PYTHONPATH=src` when validating this package in an isolated worktree. Focused checks are:

```bash
PYTHONPATH=src python3 -m py_compile src/pyAppGen/pbcs/product_catalog_pim/*.py src/pyAppGen/pbcs/product_catalog_pim/tests/*.py
PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/product_catalog_pim/tests
```
