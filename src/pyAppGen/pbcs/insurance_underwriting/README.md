# Insurance Underwriting

`insurance_underwriting` now exposes two aligned surfaces inside this package:

- The source-package contract used by repo-level PBC discovery and audits.
- A package-local standalone underwriting slice with sqlite-backed persistence, executable services and routes, underwriting workflows, forms, wizards, controls, and assistant planning helpers.

## Standalone Slice

The standalone slice is strictly local to `src/pyAppGen/pbcs/insurance_underwriting`. It does not modify shared generators, language assets, or global composition.

Key surfaces:

- `models.InsuranceUnderwritingStandaloneStore` for owned schema, sqlite execution, and AppGen-X inbox/outbox/dead-letter evidence.
- `services.InsuranceUnderwritingStandaloneService` for submission intake, risk profiling, rating, quotes, decisions, bind readiness, exclusions, rules, parameters, and event intake.
- `routes.dispatch_standalone_route()` for route-level execution.
- `workflows.run_submission_intake_workflow()` and `workflows.run_quote_to_bind_workflow()` for executable underwriting lifecycles.
- `ui.insurance_underwriting_standalone_workbench_blueprint()` and `ui.insurance_underwriting_render_standalone_workbench()` for workbench, forms, wizards, and controls.
- `agent.standalone_agent_workspace_contract()` plus `document_instruction_plan()` and `datastore_crud_plan()` for governed assistant behavior.
- `standalone.insurance_underwriting_standalone_app_contract()` and `standalone.insurance_underwriting_standalone_app_smoke()` for composed package-local app evidence.

## Example

```python
from pyAppGen.pbcs.insurance_underwriting.standalone import (
    insurance_underwriting_standalone_app_smoke,
)

result = insurance_underwriting_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["result"]["submission_count"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/insurance_underwriting/tests`
- `py_compile` over the modified package files
- package-local standalone smoke via `insurance_underwriting_standalone_app_smoke()`
- repo audit hooks such as `pbc_source_artifact_contract("insurance_underwriting")`, `pbc_implementation_release_audit(("insurance_underwriting",))`, and `pbc_generation_smoke_audit(("insurance_underwriting",))` when available
