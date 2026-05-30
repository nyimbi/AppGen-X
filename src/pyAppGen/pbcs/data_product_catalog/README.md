# Data Product Catalog PBC

`data_product_catalog` is a standalone AppGen-X packaged business capability for governed data products. The package owns its database tables, model contracts, service/runtime contract, routes, UI workbench, forms, wizards, controls, AppGen-X event contract, agent CRUD/document planning, tests, and release evidence inside `src/pyAppGen/pbcs/data_product_catalog`.

## What It Implements

- Owned catalog records for data products, owners, contracts, schemas, quality, lineage, access, subscriptions, certifications, usage, SLAs, incidents, changes, retention, policy, runtime parameters, control assertions, governed models, and AppGen-X inbox/outbox/dead-letter evidence.
- Executable domain operations for the full data-product governance lifecycle.
- A deterministic standalone in-memory `DataProductCatalogApp` for package-local smoke execution.
- Package-local UI contracts for a workbench plus forms, wizards, controls, analytics, and assistant surfaces.
- Agent planning for governed CRUD and document instruction intake.
- Release gates for `pbc_source_artifact_contract`, `pbc_implementation_release_audit`, and `pbc_generation_smoke_audit`.

## Key Entrypoints

- `runtime.py`
  `DataProductCatalogApp`, runtime smoke, capability contract, standalone execution path.
- `services.py`
  Dynamic service facade that exposes package operations and workbench queries.
- `routes.py`
  AppGen-X-friendly route contracts for commands and read-only workbench surfaces.
- `ui.py`
  Workbench, forms, wizards, and controls.
- `agent.py`
  Agent skill manifest, document planning, governed CRUD previews.
- `release_evidence.py`
  Source artifact, implementation audit, and generation smoke release gates.

## Validation

Focused validation is package-local:

```bash
python -m pytest src/pyAppGen/pbcs/data_product_catalog/tests -q
python -m compileall src/pyAppGen/pbcs/data_product_catalog
```

## Constraints

- No foreign-table mutation is allowed.
- Eventing is fixed to AppGen-X.
- Database backends are limited to PostgreSQL, MySQL, and MariaDB.
- Human confirmation is required for agent-proposed mutations.
