# Capital Markets Trading Operations Implementation Plan

## Scope

This improvement slice implements executable pre-trade trade order intake controls inside the `capital_markets_trading_ops` package. It converts backlog items 3 and 4 into real code and adds a narrow subset of item 1 for lifecycle visibility.

Implemented slice:

- Pre-trade reference-data completeness checks for order intake.
- Pre-trade operational risk gates for restricted books, blocked counterparties, duplicate instruction windows, quantity thresholds, and four-eyes approval.
- Workbench-ready order status and remediation evidence for blocked orders.
- Single-PBC app usability surfaces for forms, wizards, controls, services, agent help, and database-backed owned-table persistence.

Out of scope for this slice:

- Stream-engine selection or alternate eventing contracts.
- Shared-table reads or writes outside the package-owned boundary.
- Full order version chains, execution corrections, allocation workflow, or settlement lifecycle expansion.

## Constraints

- Eventing remains AppGen-X only.
- The implementation stays entirely inside `src/pyAppGen/pbcs/capital_markets_trading_ops`.
- Route and service surfaces stay aligned with the existing manifest APIs.
- Blocked orders remain visible in the workbench with actionable remediation rather than being silently rejected.

## Design

1. Add a package-local trade-order intake module with deterministic completeness and risk-gate evaluation.
2. Upgrade `command_trade_order` to persist validation evidence, lifecycle state, status badges, and emitted AppGen-X events.
3. Add a package-local one-PBC app wrapper plus repository-backed migrations and models for executable owned-table persistence.
4. Make the service and route layer execute the intake slice for `POST /trade-orders` and expose the current workbench state through `GET /capital-markets-trading-ops-workbench`.
5. Surface package-local forms, wizards, controls, and agent-help contracts around the same flow.
6. Add focused tests for clean intake, blocked intake, duplicate detection, route/service behavior, and one-PBC app persistence.

## Acceptance Checks

- Clean equity order with complete reference data reaches `risk_passed`.
- Missing or invalid reference data produces `release_blocked` with actionable remediation.
- Risk-gate failures open an exception while keeping the order visible in the workbench.
- Duplicate instruction detection uses package-local records only.
- AppGen-X remains the only event contract and shared-table access stays disabled.
- The package exposes a usable single-PBC app contract with forms, wizard steps, controls, services, routes, agent help, and owned-table persistence evidence.
