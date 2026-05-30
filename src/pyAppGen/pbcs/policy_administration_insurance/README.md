# Policy Administration Insurance Standalone Package

`policy_administration_insurance` now includes a package-local standalone one-PBC surface built entirely inside `src/pyAppGen/pbcs/policy_administration_insurance`.

## Included local surfaces

- `standalone.PolicyAdministrationInsuranceStandaloneApplication` for package-local execution over the existing runtime contract.
- `ui.policy_administration_insurance_form_contracts()` for issuance, coverage, endorsement, renewal, cancellation, billing, document, and event intake forms.
- `ui.policy_administration_insurance_wizard_contracts()` for issuance, endorsement, renewal, cancellation/reinstatement, and document assembly flows.
- `ui.policy_administration_insurance_control_catalog()` for summary, lifecycle, coverage-gap, notice-compliance, billing-freshness, and AppGen-X event controls.
- `agent.standalone_agent_workspace_contract()` plus richer document and CRUD planning evidence for assistant-guided standalone operation.
- `release_evidence.build_release_evidence()` coverage for standalone readiness and package-local documentation presence.

## Local execution example

```python
from pyAppGen.pbcs.policy_administration_insurance.standalone import (
    bootstrap_policy_administration_insurance_standalone_app,
    policy_administration_insurance_standalone_smoke,
)

bundle = bootstrap_policy_administration_insurance_standalone_app(tenant="tenant_demo")
result = policy_administration_insurance_standalone_smoke()
```

The standalone slice is intentionally package-local. It does not modify shared generator infrastructure, shared language files, or the global progress ledger.
