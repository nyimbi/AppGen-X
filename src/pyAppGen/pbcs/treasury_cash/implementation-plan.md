# Treasury Cash Implementation Plan

## Focus

`improve1.md` points at a broad treasury backlog. This slice concentrates on the standalone execution spine needed to operate treasury cash without relying on any other PBC's tables: bank-account governance, bank balances, statement ingestion, reconciliation, liquidity planning, capital actions, AppGen-X events, UI workflows, controls, and assistant support.

## Plan

1. Keep the existing treasury runtime, routes, events, handlers, configuration, permissions, and contract evidence intact as the executable domain core.
2. Add a package-local repository so the PBC can persist treasury records in a standalone database-backed app.
3. Add explicit forms, wizards, and controls for bank-account activation, statement reconciliation, liquidity optimization, and capital actions.
4. Bind the standalone app surface into UI contracts, assistant contributions, and release evidence.
5. Add richer deterministic seed data for an operating account, signatory, opening balance, treasury rule, and parameter.
6. Add focused package-local implementation tests covering repository persistence, standalone app wiring, and release-evidence integration.
7. Validate with Python compilation, treasury-local tests, and the relevant PBC manifest/contracts.

## Non-Goals

- Do not introduce shared-table access or dependencies outside declared AppGen-X APIs, projections, and events.
- Do not change files outside `src/pyAppGen/pbcs/treasury_cash`.
- Do not add new third-party dependencies.
