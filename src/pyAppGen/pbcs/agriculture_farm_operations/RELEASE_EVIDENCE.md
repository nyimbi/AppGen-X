# Release Evidence - Agriculture Farm Operations

Package directory: `src/pyAppGen/pbcs/agriculture_farm_operations`.

This standalone slice ships executable evidence for runtime contracts, schema/models, service and route dispatch, AppGen-X events and handlers, assistant planning, UI/forms/wizards/controls, package-local workflows, and a one-PBC standalone app shell.

## Evidence areas

- Standalone app: package-local bootstrap, route dispatch, workbench rendering, assistant workspace, and release snapshot.
- Crop planning: season-aware plans, planting-window classification, pre-plant readiness checks, replant handling, and blocked-operation exceptions.
- Service and API contracts: explicit command/query route metadata with owned-table boundaries and AppGen-X event guarantees.
- UI contract: workbench fragments, forms, wizards, controls, navigation, and workflow catalog for the one-PBC surface.
- Assistant planning: document-instruction intake and governed CRUD previews limited to owned tables with human confirmation.
- Release assurance: capability assurance, route validation, and package-local focused tests.

## Verified results

- Compile: `python3 -m compileall src/pyAppGen/pbcs/agriculture_farm_operations` completed successfully.
- Focused tests: `20 passed` for the package contract tests, standalone tests, and focused agriculture farm operations runtime/implementation tests.
- PBC audits:
  - `pbc_implementation_release_audit(("agriculture_farm_operations",))` returned `ok=True`.
  - `pbc_implemented_capability_audit(("agriculture_farm_operations",))` returned `ok=True`.
