# Trade Finance Operations PBC

`trade_finance_operations` is a package-local one-PBC trade finance app for AppGen-X. It owns letters of credit, guarantees and standby credits, documentary collections, trade bills, trade loans, shipment document packages, sanctions and compliance checks, discrepancy handling, collateral and margin cover, limit reservations, fee accruals, settlements, and SWIFT-like message evidence without crossing the PBC boundary.

## What It Exposes

- Owned runtime state and schema descriptors for issuance, presentation, compliance, discrepancy, collateral, limit, fee, settlement, release-evidence, and AppGen-X inbox/outbox/dead-letter tables.
- Guided operator forms, wizards, and controls under [`forms.py`](./forms.py), [`wizards.py`](./wizards.py), and [`controls.py`](./controls.py) for issuance, examination, trade-loan linkage, release gating, and message evidence.
- A standalone one-PBC app under [`standalone.py`](./standalone.py) with an executable case journey covering issue, present, screen, examine, waive, collateralize, reserve, assess fees, settle, and emit SWIFT-like evidence.
- Agent and chatbot contracts in [`agent.py`](./agent.py) that preserve `governed_datastore_crud`, require confirmation for every mutation, and keep all document-driven actions bounded to `trade_finance_operations_` tables.
- Package-local release evidence in [`runtime.py`](./runtime.py) and [`release_evidence.py`](./release_evidence.py), including smoke-plan synthesis, workflow coverage, event checks, assistant checks, and remaining-risk capture.

## Key Runtime Entry Points

- `trade_finance_operations_runtime_smoke()`
- `trade_finance_operations_build_schema_contract()`
- `trade_finance_operations_build_service_contract()`
- `trade_finance_operations_build_release_evidence()`
- `trade_finance_operations_build_workbench_view()`
- `TradeFinanceOperationsStandaloneApp`
- `standalone_smoke_test()`

## Boundary and Policy Notes

- Allowed backends remain PostgreSQL, MySQL, and MariaDB only.
- Eventing remains AppGen-X-only with owned outbox, inbox, and dead-letter evidence.
- No stream-engine picker is exposed anywhere in the UI, agent, route, or metadata surface.
- Cross-PBC collaboration stays on declared APIs and events; no shared-table writes are allowed.

## Verification

- `python3 -m compileall src/pyAppGen/pbcs/trade_finance_operations`
- `PYTHONPATH=src ./.venv/bin/pytest src/pyAppGen/pbcs/trade_finance_operations/tests tests/test_pbc_trade_finance_operations_runtime.py -q`
- `PYTHONPATH=src python3 - <<'PY' ... focused pbc audits ... PY`
- `git diff --check`

See [`implementation-status.md`](./implementation-status.md) for the latest recorded validation evidence.
