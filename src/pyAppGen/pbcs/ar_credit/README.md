# Accounts Receivable and Credit PBC

This package owns customer credit, invoice issuance, remittance handling, cash
application, collections follow-up, and release evidence for the AR and credit
boundary. The implemented slice is executable code, not docs-only metadata. It
stays inside owned AR tables and keeps AppGen-X as the only event contract.

## Executable Slice

- Customer credit onboarding evidence review and approval gating.
- Invoice readiness checks for customer status, identity, tax, obligations,
  dates, and available credit exposure before issuance.
- Receipt application that parses remittance, applies matched cash, and routes
  unmatched or excess value into unapplied cash.
- Collections follow-up assembly using aging, statements, and dunning notices.

## Wiring Surface

- `runtime.py` keeps the owned-state model and executable AR transitions.
- `receivables_workflows.py` adds the backlog-backed workflow slice that
  composes onboarding, invoice gating, receipt application, and collections.
- `services.py` exposes the slice through the stable `command_ar_*` and
  `query_ar_*` service names while preserving AppGen-X and owned-table
  contracts.
- `agent.py` contributes workflow previews for onboarding, invoice readiness,
  cash application, and collections follow-up.
- `ui.py` exposes workflow metadata for generated workbench surfaces.
- `release_evidence.py` publishes workflow evidence, implemented backlog items,
  and composed release readiness checks.

## Boundary Rules

- Owned datastore only: no shared-table reads or writes.
- Eventing remains AppGen-X only.
- Supported ordinary backends remain PostgreSQL, MySQL, and MariaDB.
- No new dependencies were introduced for this slice.

## Verification Focus

Focused tests cover onboarding approval, invoice readiness blocking and
issuance, overpayment and unmatched receipt handling, collections follow-up,
and release-surface exposure across services, UI, agent, and release evidence.
