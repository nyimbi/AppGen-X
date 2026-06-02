# Accounts Receivable and Credit PBC

This package is a standalone AR and credit slice for AppGen-X. It now owns an
executable one-PBC runtime with database-backed state snapshots, guided forms,
wizards, controls, route dispatch, release evidence, and assistant previews for
core invoice-to-cash work.

## Executable Slice

- Customer credit onboarding evidence review and approval gating.
- Invoice readiness checks for customer status, identity, tax, obligations,
  dates, and available credit exposure before issuance.
- Receipt application that parses remittance, applies matched cash, and routes
  unmatched or excess value into unapplied cash.
- Collections follow-up assembly using aging, statements, dunning notices, and
  recommended next actions.

## Standalone Surface

- `standalone.py` provides `ArCreditStandaloneApp` for bootstrap, form submit,
  route dispatch, workbench render, control checks, and release snapshots.
- `repository.py` persists package-local runtime snapshots, workflow runs, and
  release snapshots in SQLite without leaving the `ar_credit` boundary.
- `forms.py`, `wizards.py`, and `controls.py` define the operator-facing
  database-backed workbench contract.
- `services.py`, `routes.py`, `events.py`, and `handlers.py` are aligned on the
  AppGen-X event contract and owned-table-only execution.
- `seed_data.py` loads a demo customer, invoice, receipt, and collections view
  into the standalone app for smoke and release validation.

## Boundary Rules

- Owned datastore only: no shared-table reads or writes.
- Eventing remains AppGen-X only.
- Supported ordinary backends remain PostgreSQL, MySQL, and MariaDB.
- No new dependencies were introduced for this slice.

## Verification Focus

Focused package tests cover the standalone app, repository persistence, UI
forms/wizards/controls, onboarding approval, invoice readiness blocking and
issuance, overpayment and unmatched receipt handling, collections follow-up,
and release-surface exposure across services, UI, agent, and release evidence.
