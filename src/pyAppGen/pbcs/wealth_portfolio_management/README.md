# Wealth Portfolio Management

`wealth_portfolio_management` is a package-local wealth advisory PBC. The directory now exposes two coordinated layers:

- the source-package contracts that feed AppGen-X repository audits and generation smoke runs;
- a standalone one-PBC wealth workbench with sqlite-backed execution for package-local onboarding, IPS, suitability, rebalancing, performance, review, and surveillance flows.

## Standalone Surface

The standalone slice stays local to this package. It does not change shared generator behavior or sibling PBCs.

Key surfaces:

- `models.WealthPortfolioManagementStandaloneStore` for sqlite-backed portfolio, mandate, suitability, fee, document, trade proposal, review, surveillance, and AppGen-X inbox/outbox/dead-letter state.
- `services.WealthPortfolioManagementStandaloneService` for executable onboarding, IPS, suitability, fee, document, tax-aware rebalance, performance, advisor review, and compliance operations.
- `routes.dispatch_standalone_route()` for package-local route execution.
- `ui.wealth_portfolio_management_standalone_workbench_blueprint()` and `ui.wealth_portfolio_management_render_standalone_workbench()` for workbench forms, wizards, and controls.
- `agent.standalone_agent_workspace_contract()` plus governed CRUD and document-intake planning for advisor workflows.
- `standalone.wealth_portfolio_management_standalone_app_contract()` and `standalone.wealth_portfolio_management_standalone_app_smoke()` for composed package-local app evidence.

## Wealth Coverage

The package-local flow covers:

- household and client profile capture
- goals, risk tolerance, risk capacity, and suitability readiness
- investment policy statements and model portfolio alignment
- accounts, custodians, holdings, tax lots, restrictions, and cash needs
- drift detection, tax-aware trade proposals, fee projection, and performance snapshots
- document package tracking, advisor review, and compliance surveillance
- governed AI assistance with confirmation-gated mutation skills and AppGen-X event evidence

## Example

```python
from pyAppGen.pbcs.wealth_portfolio_management.standalone import (
    wealth_portfolio_management_standalone_app_smoke,
)

result = wealth_portfolio_management_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["total_assets"])
```

## Validation Targets

Focused validation for this package should include:

- `src/pyAppGen/pbcs/wealth_portfolio_management/tests`
- `pbc_source_artifact_contract("wealth_portfolio_management")`
- `pbc_package_local_assurance_contract("wealth_portfolio_management")`
- `pbc_specification_contract("wealth_portfolio_management")`
- `pbc_agent_capability_contract("wealth_portfolio_management")`
- `pbc_implementation_release_audit(("wealth_portfolio_management",))`
- `pbc_implemented_capability_audit(("wealth_portfolio_management",))`
- `pbc_generation_smoke_audit(("wealth_portfolio_management",))`
