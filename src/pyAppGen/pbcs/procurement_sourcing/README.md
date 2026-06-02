# procurement_sourcing PBC

`procurement_sourcing` is the standalone Procurement and Strategic Sourcing packaged business capability. It owns its source-to-order datastore, AppGen-X event contracts, requisition/RFQ/bid/award/contract/PO services, workbench forms, governed assistant skills, and release evidence.

## Standalone Domain Coverage

The package can run as a one-PBC application for governed procurement operations:

- Configure PostgreSQL/MySQL/MariaDB persistence boundaries without exposing event-stream engine selection.
- Maintain procurement rules, parameters, category policies, preferred suppliers, supplier identity, risk, and qualification evidence.
- Create purchase requisitions with line, budget, approval, and policy controls.
- Run RFQs, supplier invitations, bid capture, bid normalization, supplier scoring, split-award planning, and supplier selection.
- Create vendor contracts with clauses, compliance obligations, renewal monitoring, payment terms, and tolerance checks.
- Issue purchase orders through the AppGen-X outbox with idempotency, retry, and dead-letter evidence.
- Consume material-shortage, budget, supplier-risk, vendor-performance, contract-compliance, and access-policy events into PBC-owned projections.
- Surface workbench UI forms, wizards, controls, agent guidance, and repository read models for the full source-to-order flow.

## Executable Surfaces

- `runtime.py` contains side-effect-free source-to-order commands and advanced analytics/proof operations.
- `repository.py` backs forms and workbench read models with package-local state.
- `standalone.py` bootstraps the one-PBC app and exercises a complete requisition-to-purchase-order path.
- `ui.py` exposes the workbench fragments, forms, wizards, controls, and standalone app shell.
- `seed_data.py` provides deterministic demo workspace data.
- `release_evidence.py` validates schema, services, APIs, UI, agent, repository, artifacts, and standalone smoke behavior.

## Verification

Use the package tests plus PBC gates:

```bash
python3 -m py_compile src/pyAppGen/pbcs/procurement_sourcing/*.py src/pyAppGen/pbcs/procurement_sourcing/tests/*.py
.venv/bin/pytest -q src/pyAppGen/pbcs/procurement_sourcing/tests
```
