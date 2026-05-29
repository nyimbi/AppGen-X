# Airport Operations Management PBC

`airport_operations_management` is a standalone AppGen-X Packaged Business Capability for airport operations center work: gate and stand planning, slots and A-CDM reconciliation, turnaround control, baggage belt coordination, passenger-flow monitoring, deicing and winter readiness, disruption command, safety evidence, and governed AI assistance.

## Owned Boundary

The PBC owns gate assignments, stand allocations, slots, turnaround tasks, baggage belts, passenger-flow records, airport disruptions, airport operation policy rules, runtime parameters, schema extensions, control assertions, governed models, and AppGen-X event inbox/outbox/dead-letter tables.

It does not own AODB flight masters, ATC network slots, weather observations, baggage tracking internals, common-use resources, airline systems, or audit ledgers. Those systems are represented as declared AppGen-X event/API projections.

## Standalone App Surface

Use `standalone.py` as the one-PBC app contract:

- `single_pbc_app_contract()` exposes schema, services, APIs, runtime, UI fragments, forms, wizards, controls, routes, DSL metadata, dependencies, and drill evidence.
- `airport_forms_contract()` covers gate/stand, turnaround, surface/remote stand, winter ops, baggage/terminal flow, slot/disruption, safety/release, and assistant decision-support forms.
- `airport_wizards_contract()` covers gate-change impact, turnaround recovery, remote stand/tow, deicing, terminal/baggage contingency, command disruption, and go-live drill workflows.
- `airport_controls_contract()` enforces owned-boundary, AppGen-X eventing, stand safety, turnaround authority, PRM protection, slot/A-CDM reconciliation, agent safety, and go-live readiness gates.
- `full_airport_operations_drill()` runs a side-effect-free operational rehearsal over compatibility, milestones, deicing, slot reconciliation, baggage contingency, passenger-flow breach detection, disruption playbook, gate-change impact, assistant preview, boundary proof, and drill scorecard.

## Agent and UI

The PBC contributes `airport_operations_management_skills` to the composed application agent. Assistant plans require citations, confidence, human confirmation, and escalation for flight-critical or safety-sensitive work. UI contracts expose role-aware command-board surfaces for stand planners, turnaround controllers, baggage supervisors, terminal duty managers, supervisors, and auditors.

## Events and Backends

Eventing uses the AppGen-X event contract only. Ordinary datastore contracts are limited to PostgreSQL, MySQL, and MariaDB. The package does not expose stream-engine pickers to users.

## Verification

Run focused checks from this worktree:

```bash
PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/airport_operations_management
PYTHONPATH=src python3 -m pytest -q src/pyAppGen/pbcs/airport_operations_management/tests
```
