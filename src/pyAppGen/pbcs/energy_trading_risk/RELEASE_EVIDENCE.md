# Release Evidence - Energy Trading and Risk

Package directory: `pbcs/energy_trading_risk`.

This PBC now includes owned schema, migration DDL, payload models, a runtime risk engine, services, routes, events, handlers, UI forms, wizards, controls, assistant guidance, package metadata, side-effect-free registration, release documentation, and focused package tests.

## Evidence

- Release evidence: schema, service, route, event, handler, UI, forms, wizards, controls, assistant, and governance contracts are materialized.
- Owned datastore boundary: every owned table starts with `energy_trading_risk_`; all persistence remains package-local.
- Event contract: AppGen-X outbox/inbox with retry and dead-letter evidence only.
- Trade capture safety case: required book, strategy, side, delivery, price, counterparty, approval, curve, and limit evidence are validated before release.
- Exposure bucket workbench: accepted trades aggregate into net exposure buckets by commodity, hub, tenor, and book.
- Nomination cutoff governance: post-cutoff submissions stay visible as exceptions with version lineage markers.
- Package tests validate contracts, runtime smoke, route execution, app usability, and exception behavior.
