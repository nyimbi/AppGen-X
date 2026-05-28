# Capital Markets Trading Operations

This package now implements an executable one-PBC trading-operations slice centered on pre-trade trade-order intake. The slice is database-backed, uses owned tables and package-local migrations only, keeps AppGen-X as the only eventing contract, and exposes the domain as a self-contained app surface inside this directory.

## What Is Usable Now

- Database-backed owned-table persistence through `CapitalMarketsTradingOpsRepository`.
- One-PBC app shell through `CapitalMarketsTradingOpsApp`.
- Executable trade-order intake validation with reference-data checks and operational risk gates.
- Package-local form contract: `trade_order_intake`.
- Package-local wizard contract: `trade_order_release_wizard`.
- Package-local controls: `reference_data_checklist`, `risk_gate_panel`, `release_decision_card`.
- Stateful service surface through `CapitalMarketsTradingOpsService`.
- Route dispatch for `POST /trade-orders` and `GET /capital-markets-trading-ops-workbench`.
- Agent help topics for intake, wizard use, controls, and exception triage.

## Improvement Slice

Implemented backlog coverage:

- Item 3: pre-trade reference-data completeness checks.
- Item 4: pre-trade operational risk gates.
- Narrow lifecycle visibility from item 1: `draft`, `validated`, `risk_passed`, and `release_blocked`.

Current behavior:

- Clean orders move to `risk_passed` and emit `CapitalMarketsTradingOpsCreated` plus `CapitalMarketsTradingOpsApproved`.
- Incomplete or blocked orders stay visible in the workbench queue `trade_order_exceptions`.
- Duplicate-window detection is package-local and does not rely on shared-table access.

## Key Modules

- `trade_order_intake.py`: validation, lifecycle, remediation, and queue logic.
- `repository.py`: owned-table migrations and SQLite-backed persistence used by tests and the app wrapper.
- `application.py`: one-PBC app entrypoint for intake, workbench, and app contract retrieval.
- `services.py`: stateful service surface for commands, queries, forms, wizards, controls, and agent help.
- `ui.py`: form, wizard, controls, workbench, and app-shell contracts.
- `tests/`: release tests covering contracts, runtime behavior, and one-PBC app usability.

## Validation

Validated locally with:

- `python3 -m unittest discover -s src/pyAppGen/pbcs/capital_markets_trading_ops/tests -t src -v`
- `python3 -m compileall src/pyAppGen/pbcs/capital_markets_trading_ops`

Exact outcomes are captured in `implementation-status.md`.
