# Energy Trading and Risk Implementation Plan

## Scope

This improvement slice implements an executable standalone energy trading and risk workbench inside `energy_trading_risk`. It turns a generated contract package into a real one-PBC app with package-local persistence, trade capture controls, exposure monitoring, nomination governance, and release evidence.

Implemented slice:

- Trade capture safety-case validation with duplicate-window, approval, limit, and market-curve checks.
- Exposure bucket aggregation by commodity, hub, delivery period, and book.
- Nomination submission with cutoff-aware exception handling and version lineage markers.
- Curve publication and exposure-limit setup as package-local operational controls.
- Schedule approval and settlement capture to keep the workbench end-to-end enough for a daily risk review.
- Single-PBC app usability surfaces for forms, wizards, controls, services, routes, assistant guidance, and SQLite-backed owned-table persistence.

Out of scope for this slice:

- Multi-book VaR engines, full stress-scenario libraries, and formal backtesting.
- Shared-table reads or writes outside the package-owned boundary.
- Cross-PBC orchestration beyond AppGen-X events and declared APIs.
- Full nomination supersession rewriting of earlier persisted versions.

## Constraints

- Eventing remains AppGen-X only.
- The implementation stays entirely inside `src/pyAppGen/pbcs/energy_trading_risk`.
- Route and service surfaces stay aligned with the existing manifest APIs.
- Package-local persistence must use owned tables only.
- Blocked trades and nominations remain visible in workbench exception queues with actionable remediation.

## Design

1. Add package-local risk logic for trade capture, nomination cutoff checks, schedule validation, curve-quality checks, settlement P&L, and exposure buckets.
2. Upgrade runtime commands so the public package APIs execute real domain behavior instead of returning only generic scaffolding.
3. Add a SQLite-backed repository and a one-PBC app wrapper for executable standalone usage.
4. Surface forms, wizards, controls, and operator guidance around the same bounded flow.
5. Extend release evidence to include app usability, docs presence, and package-local UI/assistant contracts.
6. Add focused tests for clean trade capture, blocked trade capture, post-cutoff nominations, route dispatch, runtime smoke, and repository-backed app behavior.

## Acceptance Checks

- A clean trade with a fresh matching curve and an active limit reaches `risk_passed`.
- A trade with stale or missing market data is visible in `trade_exceptions` with remediation.
- Nomination submissions after the configured cutoff stay versioned and route to `nomination_exceptions`.
- Exposure buckets roll up net signed volume and projected MTM from accepted trades only.
- AppGen-X remains the only event contract and shared-table access stays disabled.
- The package exposes a usable single-PBC app contract with forms, wizards, controls, services, routes, agent help, and owned-table persistence evidence.
