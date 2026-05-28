# Airline Operations Control Implementation Plan

## Scope

This increment implements one executable airline operations control slice from `improve1.md` inside the package-local code:

1. Canonical flight-leg operating timeline
2. Tail rotation continuity graph
3. Minimum-turn feasibility engine

The slice stays inside AppGen-X boundaries, keeps ordinary datastore assumptions limited to PostgreSQL/MySQL/MariaDB, and avoids shared-table behavior.

## Backlog Slice

### Slice A: Authoritative leg timeline

- Normalize one `flight_leg` into a single operating timeline from publication through closure.
- Support branch handling for cancelled, diverted, return-to-gate, and ferry/reposition style legs.
- Expose authoritative status, delay minutes, completion airport, and timeline milestones for workbench use.

### Slice B: Tail rotation continuity

- Link same-tail flight legs into one ordered operating-day sequence.
- Compute previous-leg and next-leg continuity for each node in the sequence.
- Surface broken-turn and downstream-risk signals on the tail graph.

### Slice C: Minimum-turn feasibility

- Evaluate the outbound turn using inbound arrival timing plus operational factors such as crew change, fueling, catering, bags, special assistance, and outstation padding.
- Classify each turn as `feasible`, `marginal`, `impossible`, or `unknown`.
- Push broken turns into a focused OCC attention queue.

## Code Changes

- Add a package-local planning module for timeline normalization, turn assessment, tail graph construction, and workbench projection.
- Extend runtime state to store normalized `flight_leg` and `aircraft_rotation` records.
- Extend runtime/service/UI/agent surfaces so the slice is executable from package-local APIs instead of existing only as documentation.
- Add focused implementation tests in `tests/test_pbc_airline_operations_control_implementation.py`.

## Deferred Backlog

The following backlog items remain intentionally deferred after this slice:

- Crew legality projection horizon
- Maintenance overlays on aircraft availability
- Slot and curfew protection
- ATC/weather/NOTAM fusion
- Reaccommodation boundary rules
- Cancellation decision packs

## Verification Plan

- Run focused pytest coverage for the new implementation test file.
- Re-run the existing airline operations control runtime and package contract tests.
- Run Python compilation checks on the touched package files.
