# Fleet Mobility Operations PBC

`fleet_mobility_operations` is a standalone AppGen-X PBC for vehicle readiness, driver assignment, telematics, route control, fuel and EV energy reconciliation, maintenance planning, safety incidents, utilization, compliance, and governed dispatch assistance.

## Owned Scope

The package owns vehicle, driver assignment, telematics event, route plan, fuel transaction, maintenance schedule, safety event, policy, parameter, schema-extension, control-assertion, governed-model, outbox, inbox, and dead-letter tables. It targets PostgreSQL, MySQL, and MariaDB only and uses the AppGen-X event contract without exposing stream-engine choices.

## Standalone Application Surface

`FleetMobilityOperationsStandaloneApp` proves a one-PBC fleet application can configure rules, register vehicles and drivers, validate dispatch readiness, block low-energy or unsafe assignments, ingest and quarantine telematics, reproject route ETAs, project maintenance holds, reconcile fuel usage, run roadside incident command, and produce preview-only assistant replans.

## UI, Wizards, Controls, and Agent

The control tower exposes forms for vehicle readiness, driver assignment, telematics intake, route planning, fuel/EV reconciliation, maintenance horizons, and safety incidents. Wizards guide dispatch readiness, live reallocation, telematics quarantine, roadside incident response, fuel fraud investigation, and workshop planning. Continuous controls cover readiness, rest and overlap, credentials, telematics quarantine, route drift, maintenance horizon, fuel fraud, EV energy fit, incident lifecycle, and assistant mutation governance.

The composed app receives `fleet_mobility_operations_skills` for dispatch help, document/instruction intake, route replan previews, and bounded datastore CRUD with human confirmation.

## Verification

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/fleet_mobility_operations`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/fleet_mobility_operations/tests`
- `standalone_smoke_test()` and `validate_release_evidence()`
- focused AppGen-X PBC audits where available
