# Energy Trading and Risk

This package now implements an executable one-PBC energy trading and risk slice centered on trade capture safety, curve quality, exposure bucket monitoring, nomination cutoff governance, and settlement review. The slice is database-backed, uses owned tables and package-local migrations only, keeps AppGen-X as the only eventing contract, and exposes the domain as a self-contained app surface inside this directory.

## What Is Usable Now

- Database-backed owned-table persistence through `EnergyTradingRiskRepository`.
- One-PBC app shell through `EnergyTradingRiskApp`.
- Executable trade capture safety-case validation for commodity, hub, delivery, price, counterparty, approval, and duplicate-window evidence.
- Net exposure bucket rollups by commodity, hub, delivery period, and book.
- Nomination submission with version-aware cutoff governance.
- Market curve freshness and boundary checks before release.
- Package-local forms, wizards, controls, services, routes, and operator guidance.
- Release tests covering contracts, runtime behavior, and one-PBC app usability.

## Improvement Slice

Implemented backlog coverage:

- Item 1: trade capture safety case.
- Item 3: position netting and exposure buckets.
- Item 5: nomination cutoff governance.
- Item 9: market price staleness and boundary checks.
- Bounded part of item 17: book-level exposure limit monitoring.

Current behavior:

- Clean trades move to `risk_passed` and emit `EnergyTradingRiskCreated` plus `EnergyTradingRiskApproved`.
- Missing curve data, stale curves, approval gaps, duplicate trades, or limit breaches keep trades in `trade_exceptions`.
- Post-cutoff nominations remain versioned and visible in `nomination_exceptions` rather than being overwritten or silently accepted.
- Settlement capture records realized P&L against the stored trade economics.

## Key Modules

- `risk_engine.py`: trade capture validation, nomination and schedule checks, curve quality checks, settlement P&L, and workbench summary logic.
- `repository.py`: owned-table migrations and SQLite-backed persistence used by tests and the app wrapper.
- `application.py`: one-PBC app entrypoint for trade capture, nominations, curves, limits, settlements, and workbench retrieval.
- `services.py`: stateful service surface for commands, queries, forms, wizards, controls, and assistant help.
- `ui.py`, `forms.py`, `wizards.py`, and `controls.py`: package-local workbench surfaces.
- `tests/`: focused release tests covering contract integrity and executable app flows.

## Validation

Validated locally with:

- `python3 -m unittest discover -s src/pyAppGen/pbcs/energy_trading_risk/tests -t src -v`
- `python3 -m compileall src/pyAppGen/pbcs/energy_trading_risk`
- `python3 -c "import sys; sys.path.insert(0, 'src'); from pyAppGen.pbcs.energy_trading_risk import smoke_test; from pyAppGen.pbcs.energy_trading_risk.release_evidence import validate_release_evidence; print(smoke_test()['ok'], validate_release_evidence()['ok'])"`

Exact outcomes are captured in `implementation-status.md`.
