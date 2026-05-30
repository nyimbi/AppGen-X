# Bank Payments Clearing Implementation Plan

## Objective

Upgrade `src/pyAppGen/pbcs/bank_payments_clearing` into a coherent standalone one-PBC AppGen-X package without touching shared generator code, DSL layers, or progress ledgers.

## Package-Local Workstreams

1. Standalone execution spine
   - Keep payment-clearing behavior package-local and side-effect-free.
   - Expose an executable one-PBC app surface that boots configuration, rules, parameters, participant-bank setup, payment workflows, and workbench rendering inside this package.

2. Contract convergence
   - Replace thin aliases with executable package-local schema, model, service, route, permission, event, and release contracts.
   - Ensure every surfaced table, route, permission, and emitted event stays within `bank_payments_clearing_*` ownership boundaries.

3. Workflow depth from `improve1.md`
   - Cover the highest-value backlog items now: rail-aware validation, participant-bank governance, duplicate prevention, maker-checker release, liquidity checks, batch assembly, settlement-file integrity, acknowledgement handling, returns, reconciliation, and operator workbench evidence.
   - Keep cancellation/recall, chargebacks, cross-border chains, and richer repair queues as later-slice work.

4. UI and assistant surface
   - Provide forms, wizards, controls, workflow metadata, and workbench navigation for a standalone app surface.
   - Strengthen document-instruction and governed CRUD planning with route, permission, idempotency, and event previews.

5. Release evidence and focused validation
   - Refresh README, implementation status, and release evidence to describe the standalone slice.
   - Add focused tests for contracts, payment flow execution, route dispatch, standalone bootstrap, and repo-style release gates.

## Deliverables

- Executable package-local contracts in `schema_contract.py`, `models.py`, `services.py`, `service_contract.py`, `routes.py`, `events.py`, `handlers.py`, `permissions.py`, `config.py`, `agent.py`, and `release_evidence.py`
- Standalone one-PBC app bootstrapping in `standalone.py`
- Refreshed `README.md`, `implementation-status.md`, `implementation-plan.md`, and `RELEASE_EVIDENCE.md`
- Focused tests in `tests/test_contract.py`, `tests/test_payment_operations.py`, and `tests/test_standalone.py`

## Validation Plan

- Compile the package with `python3 -m compileall`.
- Run focused package tests through a lightweight in-repo test harness if `pytest` is unavailable.
- Run package-local smoke and audit surfaces: runtime, routes, UI, standalone app, capability assurance, and release evidence.
