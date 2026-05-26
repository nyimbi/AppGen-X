# Cross Border Trade PBC

`cross_border_trade` is a package-owned AppGen-X PBC for cross-border classification, landed cost, export controls, and customs declaration execution.

## Owned Boundary

- Owned implementation directory: `src/pyAppGen/pbcs/cross_border_trade`
- Owned tables: `hs_classification`, `landed_cost_quote`, `export_control_check`, `customs_declaration`
- External dependencies are represented only through AppGen-X events, APIs, and projections. The runtime never reads or writes shared external tables.
- Supported ordinary datastore backends: PostgreSQL, MySQL, MariaDB.
- Eventing uses the AppGen-X event contract on `appgen.cross_border_trade.events`; users are not offered stream-engine selection.

## Runtime Capabilities

- HS classification with confidence scoring, origin evidence, review routing, and immutable evidence hashes.
- Landed cost quote generation across goods value, shipping, duty, tax, insurance, broker fee, incoterm, and currency.
- Export control screening for destination, restricted party risk, license triggers, and blocked destinations.
- Customs declaration filing with required documents, broker route selection, and declaration status.
- AppGen-X inbox/outbox handling with idempotency keys, retry evidence, and dead-letter records.
- Configuration schema, parameter engine, compiled rule engine, RBAC descriptors, seed data, and UI workbench contract.

## Advanced Capabilities

- Event-sourced lifecycle and tamper-evident hash chain.
- Graph-relational trade topology from order to classification, quote, export check, broker, and declaration.
- Schema extension registration with migration evidence.
- Counterfactual landed-cost simulation and stochastic trade exposure modeling.
- Autonomous exception resolution and self-healing broker failover plan.
- Semantic trade document parsing for order, SKU, origin, destination, and incoterm extraction.
- Predictive export-control risk and governed model evidence.
- Dynamic policy screening and automated control tests.
- Cross-system order, inventory, payment, and logistics federation through projections.
- Carbon-aware broker routing, mathematical landed-cost optimization, and broker allocation mechanism.

## UI

The package exposes `cross_border_trade_ui_contract()` and `cross_border_trade_render_workbench()` with fragments for classification, landed cost, export controls, declarations, broker submissions, documents, topology, exposure, exceptions, rules, parameters, configuration, eventing, and dead letters.
