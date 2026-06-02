# Capital Markets Trading Operations

`capital_markets_trading_ops` is an executable standalone AppGen-X PBC for middle-office trading operations. It owns trade-order intake, execution capture, allocation review, confirmation matching, settlement-instruction governance, settlement fail tracking, trade-break classification, position snapshot provenance, workbench UI contracts, agent guidance, and release evidence inside its own PBC directory.

## Usable Domain Surface

The PBC now supports a one-PBC application that can run an order-to-settlement workflow without shared tables:

- trade-order intake with reference-data completeness checks, asset-class required fields, duplicate-window detection, restricted books, blocked counterparties, quantity/notional thresholds, and four-eyes approval gates
- lifecycle evidence for draft, validated, risk-passed, release-blocked, and release-ready order states
- execution capture with partial-fill fields, venue/broker timestamps, price/quantity validation, fee capture, and correction-type evidence for busts, price corrections, quantity corrections, and duplicate suppression
- allocation splitting with account eligibility, mandate gates, residual policy handling, block-to-child lineage, and allocation evidence hashes
- broker/counterparty confirmation normalization with API/file/document channels, economic affirmation, price/quantity/commission tolerances, and mismatch classes
- settlement-instruction governance with effective-date, approval, market/currency/custodian/place-of-settlement fields, and market-enrichment completeness checks
- settlement status tracking through failed settlement, penalty, buy-in, owner, and remediation context
- trade-break taxonomy across booking, allocation, confirmation, settlement, position, cash, fee, corporate action, and external reference-data breaks
- position snapshot provenance over executions, allocations, and settlements with provisional/final state
- agent document-instruction planning, governed CRUD previews, operator guidance, and single-agent skill namespace contribution

## One-PBC Application

`standalone.py` exposes `CapitalMarketsTradingOpsStandaloneApp`. The demo workspace creates a valid trade order, records an execution, allocates the fill, matches a confirmation, governs an SSI, records a failed settlement with buy-in exposure, opens a settlement break, builds a position snapshot, and renders a workbench summary. The standalone contract surfaces forms, wizards, controls, workbench views, DSL exposure, and agent tools for the composed application.

## Main Modules

- `trade_order_intake.py`: trade-order validation, lifecycle state, duplicate detection, policy gates, remediation, and workbench summary logic
- `post_trade.py`: execution, allocation, confirmation, settlement, break, and position logic
- `workflows.py`: package-local create-order and execution-review workflow contracts
- `application.py`: database-backed one-PBC order intake shell using package-owned migrations
- `standalone.py`: order-to-settlement standalone app wrapper and smoke test
- `repository.py`: owned-table SQLite harness for package tests and app demonstration
- `services.py`, `routes.py`, `ui.py`, `agent.py`: service, API, UI, and assistant surfaces

## Boundaries

All persistence contracts remain owned by `capital_markets_trading_ops_*` tables. Cross-PBC concerns such as market data, surveillance, custody, accounting, corporate actions, and policy/audit signals are represented through AppGen-X event/API boundaries rather than shared table access. Ordinary backend declarations remain PostgreSQL, MySQL, and MariaDB only, and no stream-engine picker is visible to users.

## Validation

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/capital_markets_trading_ops`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/capital_markets_trading_ops/tests`
- focused AppGen-X audits for source artifact, package-local assurance, specification, agent capability, implementation, implemented capability, and generation smoke
