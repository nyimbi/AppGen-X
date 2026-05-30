# Facilities Space Management Implementation Plan

## Objective

Make `facilities_space_management` usable as a standalone one-PBC AppGen-X application for facilities, workplace, occupancy, reservation, move, safety, utilization, and space planning operations. A generated application with only this PBC must let facilities teams operate a credible workplace management surface with owned data, forms, wizards, controls, workflows, events, configuration, rules, agent guidance, and release evidence.

## Domain Scope

This PBC owns facility and space operations. It does not own HR employee records, lease contract accounting, work-order execution, access-control hardware, finance chargebacks, emergency communications platforms, or energy telemetry systems. Those are represented through declared APIs, AppGen-X events, or owned projections.

Owned domain responsibilities include facility sites, campus topology, floors, floor-map versions, spaces, space types, occupancy plans, occupant assignments, hybrid work patterns, reservations, setup dependencies, move requests, move tasks, maintenance-aware availability, access constraints, safety inspections, utilization observations, capacity plans, demand simulations, exceptions, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X outbox/inbox/dead-letter records.

## Capability Plan

1. Preserve and validate the existing executable package surface.
   - Compile package modules.
   - Run focused package tests.
   - Run source/spec/release PBC gates.
   - Keep all work inside `src/pyAppGen/pbcs/facilities_space_management`.

2. Confirm table-stakes facilities operations.
   - Facility site and campus hierarchy, building/floor topology, space records, area standards, space taxonomy, and map-version evidence.
   - Occupancy plans, assignments, hybrid work patterns, team adjacency, neighborhood planning, and scenario comparisons.
   - Reservations, eligibility checks, conflict optimization, setup/teardown dependencies, no-show handling, hot desks, events, visitor controls, and service dependencies.
   - Move requests, dependency task orchestration, readiness checklists, occupant communication, and rollback evidence.
   - Maintenance-aware blocking, safety inspections, hazards, emergency zones, wayfinding, accessibility, amenities, cleaning, renovations, and exception workflows.
   - Utilization observations, privacy-safe analytics, capacity planning, demand forecasting, chargeback evidence, environmental signals, energy/carbon views, and executive dashboards.

3. Confirm AppGen-X and owned-boundary behavior.
   - Owned tables use the `facilities_space_management_` prefix.
   - Cross-PBC dependencies are APIs, AppGen-X events, or owned projections.
   - Ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
   - Eventing remains AppGen-X only, with no user-facing stream-engine picker.

4. Confirm standalone application behavior.
   - UI exposes workbench views, forms, wizards, controls, rule/parameter editors, event surfaces, release evidence, and assistant panels.
   - Services and routes map to executable commands and read-only queries.
   - Agent supports document/instruction intake, safe CRUD planning, owned-table rejection, task guidance, and composed-agent skill export.

5. Complete handoff artifacts.
   - Add this plan.
   - Add README with domain scope, workflows, UI, agent, configuration, events, and testing guidance.
   - Add implementation status with review findings, verification evidence, and known gaps.

## Verification Plan

Run:

```text
python3 -m py_compile src/pyAppGen/pbcs/facilities_space_management/*.py src/pyAppGen/pbcs/facilities_space_management/tests/*.py
/Volumes/Media/src/pjs/appgen/.venv/bin/pytest -q src/pyAppGen/pbcs/facilities_space_management/tests
```

Run PBC gates:

```python
from pyAppGen.pbc import (
    pbc_specification_contract,
    pbc_source_artifact_contract,
    pbc_implementation_release_audit,
    pbc_generation_smoke_audit,
)

key = "facilities_space_management"
assert pbc_specification_contract(key)["ok"]
assert pbc_source_artifact_contract(key)["ok"]
assert pbc_implementation_release_audit((key,))["ok"]
# Generation smoke should also pass; if it hangs, record the blocker and investigate before merge.
```
