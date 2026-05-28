# Release Evidence - Capital Markets Trading Operations

Package directory: `pbcs/capital_markets_trading_ops`.

This PBC includes owned schema, migration DDL, models, services, routes, events, handlers, UI workbench surfaces, forms, wizards, controls, agent skills, permissions, configuration, seed data, package metadata, side-effect-free registration, and focused package tests.

## Evidence

- Release Evidence: schema, service, route, event, handler, UI, agent, governance, form, wizard, control, and one-PBC app contracts are materialized.
- Owned datastore boundary: every owned table starts with `capital_markets_trading_ops_` and cross-PBC collaboration uses AppGen-X events or declared APIs.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence.
- Database-backed app slice: `repository.py`, `application.py`, and migration `002_trade_order_intake_slice.sql` persist trade-order workflow state without shared-table access.
- Package tests: stdlib `unittest` covers contract integrity, trade-order intake logic, blocked-order workbench visibility, route/service execution, and one-PBC app persistence.
- Validation commands:
  - `python3 -m unittest discover -s src/pyAppGen/pbcs/capital_markets_trading_ops/tests -t src -v` -> `Ran 15 tests in 0.314s`, `OK`
  - `python3 -m compileall src/pyAppGen/pbcs/capital_markets_trading_ops` -> success
