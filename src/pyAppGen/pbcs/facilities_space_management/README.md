# Facilities Space Management PBC

`facilities_space_management` is the AppGen-X packaged business capability for facility sites, floors, spaces, occupancy, reservations, moves, safety, utilization, and workplace intelligence. It is intended to run as a standalone one-PBC application: an app composed with only this package should let a facilities team manage space inventory, assign occupancy, reserve spaces, plan moves, handle maintenance and safety constraints, analyze utilization, and guide users through a professional assistant.

## Owned Boundary

The PBC owns only `facilities_space_management_` tables. It does not directly mutate HR, lease, finance, access-control, maintenance-work-order, or energy-system tables. Those dependencies are represented through declared APIs, AppGen-X events, or package-local projections.

Owned areas include facility sites, floors, floor maps, spaces, space types, occupancy plans, occupant assignments, reservations, move requests, move tasks, maintenance signals, availability snapshots, access constraints, safety inspections, utilization observations, capacity plans, exceptions, policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X outbox/inbox/dead-letter tables.

Supported ordinary database backends are PostgreSQL, MySQL, and MariaDB.

## Core Workflows

- Create facility sites with campus topology, service zones, entrances, emergency zones, owner, operating hours, and status.
- Define floors and digital-twin map versions with zones, exits, circulation, accessibility routes, amenities, restricted areas, and map-change impact.
- Create and classify spaces with area standards, capacity method, seating, neighborhood, AV features, environmental profile, accessibility, and reservation eligibility.
- Build occupancy plans, assignment records, hybrid work patterns, team adjacency plans, and demand scenarios.
- Reserve spaces using capacity, requester role, equipment, accessibility, access constraints, maintenance state, setup buffers, visitor rules, and booking-horizon policy.
- Orchestrate room setup, cleaning, AV, catering, security, and readiness tasks tied to reservations and events.
- Open move requests and complete move tasks with dependency graphs, IT/access/furniture/cleaning/signage handoffs, occupant communication, and rollback evidence.
- Record maintenance signals, safety inspections, hazards, emergency readiness, access constraints, wayfinding closures, and availability snapshots.
- Observe utilization with privacy-safe aggregation, source confidence, sensor health, reconciliation to reservations/assignments, and heatmaps.
- Build capacity plans and simulate lease, renovation, attendance, move, emergency, and hybrid-work scenarios.

## UI Surface

The package exposes generated UI contracts for a standalone facilities workbench. Expected workbench areas include site topology, floor-map explorer, space registry, reservation board, occupancy planner, move command center, safety and maintenance panels, utilization analytics, capacity scenarios, rule/parameter editors, event status, release evidence, and assistant guidance.

Forms map to executable commands. Wizards cover site/floor setup, space onboarding, reservation readiness, move planning, safety inspection, occupancy scenario planning, and capacity-plan publication. Controls include tenant/site/floor selectors, map-version pickers, space-type filters, capacity sliders, reservation timelines, access constraint toggles, utilization confidence filters, and safety/maintenance state chips.

## Agent Skills

The PBC contributes facilities skills to the composed application assistant. The agent can explain facilities tasks, parse move or reservation instructions, draft safe CRUD plans for owned tables, recommend forms/wizards, reject foreign table writes, require confirmation for mutations, and preview AppGen-X event effects.

The agent should be used for workplace guidance such as finding suitable rooms, diagnosing blocked reservations, preparing move plans, explaining safety constraints, comparing capacity scenarios, and summarizing utilization evidence.

## Events

The package uses the AppGen-X event contract only. It emits facility, reservation, move, maintenance, safety, and capacity events. It consumes employee, work-order, access-policy, lease, policy, and maintenance signals through idempotent handlers with retry and dead-letter evidence.

No user-facing stream-engine picker is exposed.

## Configuration, Rules, And Parameters

Configuration includes database backend, AppGen-X topic, retry limits, tenant isolation, map/version behavior, reservation defaults, utilization privacy thresholds, and workbench limits.

Rules cover reservation eligibility, capacity, access constraints, safety blocking, setup buffers, privacy-safe utilization, move readiness, no-show handling, and capacity-plan approval. Parameters include booking horizon, no-show grace period, utilization confidence floor, minimum aggregation size, setup buffers, capacity targets, and scenario limits.

## Testing

Run package checks from the repository root or the PBC worktree:

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
assert pbc_generation_smoke_audit((key,))["ok"]
```

## Extension Points

Future work should deepen map rendering, GIS integrations, sensor adapters, cleaning/service scheduling, emergency communications, lease-cost projections, and energy/carbon integrations. Those extensions must preserve owned-table boundaries and AppGen-X event composition.
