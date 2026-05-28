# Customer 360

`customer_360` is a package-local Customer 360 and engagement registry PBC. The package now exposes two layers:

- The existing generated source-package contracts used by repo-level PBC audits.
- A package-local standalone one-PBC app slice with sqlite-backed persistence, executable services and routes, a workbench blueprint, forms, wizards, controls, and agent planning helpers.

## Package-Local Standalone App

The standalone slice is intentionally local to this directory. It does not change repo-wide composition behavior or other PBCs.

Key surfaces:

- `models.Customer360StandaloneStore` for sqlite-backed owned tables and AppGen-X inbox/outbox/dead-letter evidence.
- `services.Customer360StandaloneService` for executable CRUD, timeline, workbench, merge, and inbox flows.
- `routes.dispatch_standalone_route()` for route-level execution.
- `ui.customer_360_standalone_workbench_blueprint()` and `ui.customer_360_render_standalone_workbench()` for workbench, forms, wizards, and controls.
- `agent.standalone_agent_workspace_contract()` plus enriched `document_instruction_plan()` and `datastore_crud_plan()` for document intake and governed CRUD planning.
- `standalone.customer_360_standalone_app_contract()` and `standalone.customer_360_standalone_app_smoke()` for composed package-local app evidence.

## Example

```python
from pyAppGen.pbcs.customer_360.standalone import customer_360_standalone_app_smoke

result = customer_360_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["result"]["profile_count"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/customer_360/tests`
- `pbc_source_artifact_contract("customer_360")`
- `pbc_implementation_release_audit(("customer_360",))`
- `pbc_generation_smoke_audit(("customer_360",))`
