# Payroll Engine Implementation Status

Status: improve1 executable control slice complete for all 50 backlog features.

Evidence:
- `payroll_control.py` maps feature 1-50 to owned payroll control tables, required fields, UI surfaces, service/API routes, declared event/API/projection dependencies, tests, and release evidence.
- Runtime exposes `payroll_control` and the `evaluate_payroll_control` operation.
- UI exposes 50 payroll control panels, service actions, and agent tool identifiers.
- Release evidence and validation include the payroll improve1 control contract.
- `tests/test_domain_behavior.py` gates payroll calendars, periods, worker projections, gross-to-net, tax, deductions, garnishments, net pay, payments, postings, filings, corrections, event reliability, agent safety, boundary proof, simulations, carbon scheduling, readiness, and end-to-end run proof.

Constraints preserved:
- Allowed database backends remain PostgreSQL, MySQL, and MariaDB.
- Eventing uses the AppGen-X event contract and `appgen.payroll.events` topic.
- Cross-PBC inputs are declared as APIs, events, or projections; shared table access remains rejected.
