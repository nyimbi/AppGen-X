# Global Inventory Visibility

`global_inventory_visibility` is a package-local Global Inventory Visibility and pool-management PBC. The package now exposes two layers:

- The existing generated source-package contracts used by repo-level PBC audits.
- A package-local standalone one-PBC app slice with sqlite-backed repository/read models, executable services and routes, realistic seed data, workbench forms, wizards, controls, and agent planning helpers.

## Package-Local Standalone App

The standalone slice is intentionally local to this directory. It does not change repo-wide composition behavior or any other PBC.

Key surfaces:

- `repository.GlobalInventoryVisibilityRepository` for sqlite-backed owned tables, runtime event logs, control assertions, and read models.
- `services.GlobalInventoryVisibilityStandaloneService` for executable configuration, governance, node/pool/snapshot, projection, reservation, inbox, proof, workbench, and release-evidence flows.
- `routes.dispatch_standalone_route()` for route-level execution.
- `ui.global_inventory_visibility_standalone_workbench_blueprint()` and `ui.global_inventory_visibility_render_standalone_workbench()` for workbench cards, forms, wizards, and controls.
- `agent.standalone_agent_workspace_contract()` plus enriched `document_instruction_plan()` and `datastore_crud_plan()` for instruction intake and governed CRUD planning.
- `standalone.global_inventory_visibility_standalone_app_contract()` and `standalone.global_inventory_visibility_standalone_app_smoke()` for composed package-local app evidence.

## Example

```python
from pyAppGen.pbcs.global_inventory_visibility.standalone import global_inventory_visibility_standalone_app_smoke

result = global_inventory_visibility_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["result"]["available_to_promise"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/global_inventory_visibility/tests`
- `pbc_specification_contract("global_inventory_visibility")`
- `pbc_source_artifact_contract("global_inventory_visibility")`
- `pbc_implementation_release_audit(("global_inventory_visibility",))`
- `pbc_generation_smoke_audit(("global_inventory_visibility",))`
