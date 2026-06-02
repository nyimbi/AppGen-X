# Professional Services Automation

`professional_services_automation` now exposes two layers inside this package directory:

- The existing source-package contracts used by repo-wide PBC audits.
- A package-local standalone one-PBC app slice with executable forms, wizards, controls, standalone composition, and release evidence wiring.

## Standalone Surface

The standalone slice stays local to `src/pyAppGen/pbcs/professional_services_automation` and does not change shared generators or language assets.

Key surfaces:

- `forms.professional_services_automation_form_catalog()` for package-local operator forms.
- `wizards.professional_services_automation_wizard_catalog()` for guided launch, recovery, risk, and assistant-preview flows.
- `controls.professional_services_automation_control_center()` for release, scope, billing, and assistant guardrail evidence.
- `ui.professional_services_automation_standalone_app_contract()` and `ui.professional_services_automation_render_standalone_app()` for the standalone workbench shell.
- `standalone.professional_services_automation_standalone_app_contract()` and `standalone.validate_standalone_application()` for one-PBC app validation.

## Example

```python
from pyAppGen.pbcs.professional_services_automation.standalone import smoke_test

result = smoke_test()
print(result["ok"])
print(result["validation"]["app"]["bootstrap"]["record_count"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/professional_services_automation/tests`
- `tests/test_pbc_professional_services_automation_runtime.py`
- `pyAppGen.pbc.pbc_implementation_release_audit(("professional_services_automation",))`
- `pyAppGen.pbc.pbc_implemented_capability_audit(("professional_services_automation",))`
