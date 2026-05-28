# Airline Operations Control

`airline_operations_control` is the AppGen-X PBC for operational control of flight legs, aircraft rotations, disruptions, passenger recovery, and network recovery planning.

## Implemented Slice

This package now includes an executable planning slice for:

- Canonical flight-leg timelines
- Tail rotation continuity graphs
- Minimum-turn feasibility and OCC watchlists

The implemented behavior lives in [operations_planning.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/airline_operations_control/operations_planning.py), with package surfaces wired through [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/airline_operations_control/runtime.py), [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/airline_operations_control/services.py), [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/airline_operations_control/ui.py), and [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/airline_operations_control/agent.py).

## Key Entry Points

- `airline_operations_control_command_flight_leg(state, payload)`
  Builds one authoritative leg timeline and stores it in package-local runtime state.
- `airline_operations_control_record_aircraft_rotation(state, payload)`
  Builds one tail continuity graph from same-tail legs.
- `airline_operations_control_query_workbench(state, filters=None)`
  Returns OCC workbench metrics, a turn watchlist, and an attention queue.
- `AirlineOperationsControlService().query_workbench(payload)`
  Projects the same slice directly from scenario payloads.
- `airline_operations_control_render_workbench(...)`
  Exposes decision-support panels for canonical timelines, tail continuity, and minimum-turn watchlists.

## Test Coverage

Focused implementation coverage lives in [tests/test_pbc_airline_operations_control_implementation.py](/Volumes/Media/src/pjs/appgen/tests/test_pbc_airline_operations_control_implementation.py). The implementation tests cover:

- late inbound causing a broken outbound turn
- diversion and return-to-gate timeline branches
- service and UI projection of scenario payloads

## Validation Commands

```bash
python3 -m py_compile src/pyAppGen/pbcs/airline_operations_control/operations_planning.py \
  src/pyAppGen/pbcs/airline_operations_control/runtime.py \
  src/pyAppGen/pbcs/airline_operations_control/services.py \
  src/pyAppGen/pbcs/airline_operations_control/ui.py \
  src/pyAppGen/pbcs/airline_operations_control/agent.py \
  tests/test_pbc_airline_operations_control_implementation.py

python3 -m compileall src/pyAppGen/pbcs/airline_operations_control \
  tests/test_pbc_airline_operations_control_implementation.py

./.venv/bin/pytest \
  tests/test_pbc_airline_operations_control_implementation.py \
  tests/test_pbc_airline_operations_control_runtime.py \
  src/pyAppGen/pbcs/airline_operations_control/tests/test_contract.py
```

## Notes

- Datastore assumptions remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X only.
- The rest of the backlog in `improve1.md` remains intentionally deferred to later slices.
