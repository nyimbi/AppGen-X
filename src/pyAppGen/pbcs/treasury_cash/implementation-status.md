# Implementation Status

## Completed in This Slice

- Added `repository.py` with a SQLite-backed standalone repository that applies the package migration, stores treasury workflow records, and summarizes workbench state.
- Expanded `ui.py` with explicit treasury forms, wizards, controls, and a `treasury_cash_single_pbc_app_contract()` surface.
- Expanded `agent.py` so the assistant exposes treasury execution operations and the standalone assistant panel/workbench surface.
- Added richer seed data for a treasury operating account, signatory, opening balance, liquidity rule, and counterparty-risk parameter.
- Reworked `release_evidence.py` so release readiness includes repository, standalone app, UI, agent, event, handler, seed, and execution-service evidence.
- Added package-local README and implementation plan/status documentation for this standalone slice.
- Added focused implementation tests for repository-backed treasury workflows and standalone contract wiring.

## Validation Target

- Compile treasury Python files under `src/pyAppGen/pbcs/treasury_cash`.
- Run treasury package tests only.
- Run the relevant PBC manifest/contract validation available in this repo.

## Remaining Work

- Add broader scenario libraries for sweep orchestration, intercompany netting cycles, in-house banking statements, and richer covenant/facility schedules in later treasury slices.
- Add visual UI verification once a stable generator-backed screenshot harness exists for single-PBC apps.
