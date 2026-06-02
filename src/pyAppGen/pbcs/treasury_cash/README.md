# Treasury Cash PBC

`treasury_cash` is a standalone treasury execution slice for AppGen-X. It owns bank-account governance, balance capture, statement ingestion and reconciliation, cash positioning and forecasting, liquidity optimization, payment-rail routing, capital actions, control evidence, AppGen-X inbox/outbox handling, and a treasury-specific workbench surface.

## Standalone Surface

This package is usable on its own with only its owned database tables and declared AppGen-X contracts.

- `runtime.py` provides executable treasury workflows for bank registration, balance capture, statement ingestion, reconciliation, positioning, forecasting, liquidity planning, rail routing, investments, debt draws, hedge recommendations, control testing, and governed-model registration.
- `repository.py` provides a SQLite-backed persistence layer for the standalone PBC app and applies the package migration locally.
- `services.py`, `routes.py`, `events.py`, and `handlers.py` expose the command/query, API, event, and idempotent handler contracts without shared-table access.
- `ui.py` defines database-backed forms, workflow wizards, treasury controls, workbench rendering, and the single-PBC app contract.
- `agent.py` contributes treasury assistant skills for liquidity planning, bank statement triage, policy explanation, controlled CRUD, and capital-actions guidance.
- `seed_data.py` provides deterministic starter rows for a tenant-scoped operating account, signatory, opening balance, rule, and parameter.
- `release_evidence.py` ties the schema/service/runtime evidence to the standalone repository, UI, agent, and tests.

## Forms, Wizards, Controls

Forms:
- `BankAccountMandateForm`
- `BalanceCaptureForm`
- `BankStatementIngestionForm`
- `CashForecastScenarioForm`
- `LiquidityFundingRequestForm`
- `CapitalActionsForm`

Wizards:
- `BankAccountActivationWizard`
- `StatementReconciliationWizard`
- `LiquidityOptimizationWizard`
- `CapitalActionsWizard`

Controls:
- Signatory authority and counterparty identity checks
- Statement completeness and duplicate-file protection
- Minimum liquidity buffer and dual-approval funding gate
- Payment-rail failover and counterparty-risk limit
- Investment policy, debt-draw, covenant, and governed-model drift gates

## Boundary

This slice does not own AP, AR, payroll, tax, identity, or general-ledger tables. It consumes those concerns only through AppGen-X events, read-only projections, and declared APIs. Every table reference remains under `treasury_cash_*`.
