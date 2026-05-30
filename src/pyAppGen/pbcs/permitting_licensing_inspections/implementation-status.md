# Permitting Licensing Inspections Implementation Status

Status: improve1 executable control slice complete for all 50 backlog features.

Evidence:
- `permit_control.py` maps feature 1-50 to owned permitting control tables, required fields, UI surfaces, service/API routes, declared event/API/projection dependencies, tests, and release evidence.
- Runtime exposes `permit_control` and the `evaluate_permit_control` operation.
- UI exposes 50 permit control panels, service actions, and agent tool identifiers.
- Release evidence and validation include the permitting improve1 control contract.
- `tests/test_domain_behavior.py` gates intake, parcel and party normalization, plan review, fee handoffs, issuance, inspections, violations, due process, public notice, hearings, renewals, portal transparency, agent previews, geospatial checks, audit custody, offline sync, exception recovery, training, and go-live proof.

Constraints preserved:
- Allowed database backends remain PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and `pbc.permitting_licensing_inspections.events` topic.
- Cross-PBC inputs are declared as APIs, events, or projections; shared table access remains rejected.
