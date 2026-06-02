# Hospitality Property Operations

`hospitality_property_operations` now exposes two layers inside this package only:

- The source-package contract surface used by repo-wide PBC audits.
- A package-local standalone one-PBC hotel operations slice with sqlite-backed owned data, executable routes/services, workbench rendering, shift handover support, and assistant planning helpers.

## Standalone Slice

The standalone app is local to `src/pyAppGen/pbcs/hospitality_property_operations`. It does not modify shared generator code or sibling PBCs.

Key surfaces:

- `models.HospitalityPropertyOperationsStandaloneStore` for owned room, reservation, stay, housekeeping, guest request, occupancy, rate, and AppGen-X event tables.
- `services.HospitalityPropertyOperationsStandaloneService` for executable room readiness, arrival, stay, recovery, and revenue-control flows.
- `routes.dispatch_standalone_route()` for route-level execution.
- `ui.hospitality_property_operations_standalone_workbench_blueprint()` and render helpers for forms, wizards, controls, and workbench/detail panels.
- `agent.standalone_agent_workspace_contract()` plus document-intake and governed CRUD planning helpers.
- `standalone.hospitality_property_operations_standalone_app_contract()` and `standalone.hospitality_property_operations_standalone_app_smoke()` for composed package-local app evidence.

## Example

```python
from pyAppGen.pbcs.hospitality_property_operations.standalone import (
    hospitality_property_operations_standalone_app_smoke,
)

result = hospitality_property_operations_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["lane_summary"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/hospitality_property_operations/tests`
- `pbc_source_artifact_contract("hospitality_property_operations")`
- `pbc_implementation_release_audit(("hospitality_property_operations",))`
- `pbc_generation_smoke_audit(("hospitality_property_operations",))`
