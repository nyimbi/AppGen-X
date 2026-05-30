# Utility Outage Restoration

`utility_outage_restoration` remains a source-package PBC with owned PostgreSQL/MySQL/MariaDB contracts, AppGen-X-only eventing, and no stream-engine picker. This directory now also contains a package-local standalone outage-restoration slice that executes the operational flow end to end without touching shared generator or composition code.

## Package-Local Standalone App

The standalone slice is intentionally local to `src/pyAppGen/pbcs/utility_outage_restoration`.

It covers:

- network asset projections for feeder, breaker, recloser, switch, transformer, lateral, and service-point topology
- outage incident intake, trouble calls, OMS event creation, and device interruption clustering
- crew dispatch, switching plan authoring, safety isolation, and damage assessment
- ETR calculation, nested outages, customer notifications, critical-customer prioritization, and mutual aid
- restoration verification, regulatory index snapshots, storm mode coordination, and governed AI assistance
- standalone workbench forms, wizards, controls, route contracts, and assistant workspace evidence

Key surfaces:

- `models.UtilityOutageRestorationStandaloneStore` for the SQLite-backed package-local owned tables and AppGen-X inbox/outbox/dead-letter evidence
- `services.UtilityOutageRestorationStandaloneService` for executable outage, switching, dispatch, notification, storm, and verification flows
- `routes.dispatch_standalone_route()` for route-level execution inside the one-PBC harness
- `ui.utility_outage_restoration_standalone_workbench_blueprint()` and `ui.utility_outage_restoration_render_standalone_workbench()` for workbench, forms, wizards, and controls
- `agent.standalone_agent_workspace_contract()` plus governed document/CRUD planning helpers
- `standalone.utility_outage_restoration_standalone_app_contract()` and `standalone.utility_outage_restoration_standalone_app_smoke()` for composed package-local evidence

## Example

```python
from pyAppGen.pbcs.utility_outage_restoration.standalone import (
    utility_outage_restoration_standalone_app_smoke,
)

result = utility_outage_restoration_standalone_app_smoke()
print(result["ok"])
print(result["workbench"]["result"]["result"]["critical_customer_queue"])
```

## Validation Targets

Focused validation for this package should include:

- `python3 -m py_compile src/pyAppGen/pbcs/utility_outage_restoration/*.py src/pyAppGen/pbcs/utility_outage_restoration/tests/*.py`
- `uv run pytest -q src/pyAppGen/pbcs/utility_outage_restoration/tests`
- `pbc_source_artifact_release_audit(("utility_outage_restoration",))`
- `pbc_package_local_assurance_audit(("utility_outage_restoration",))`
- `pbc_specification_release_audit(("utility_outage_restoration",))`
- `pbc_agent_capability_release_audit(("utility_outage_restoration",))`
- `pbc_implementation_release_audit(("utility_outage_restoration",))`
- `pbc_implemented_capability_audit(("utility_outage_restoration",))`
- `pbc_generation_smoke_audit(("utility_outage_restoration",))`
