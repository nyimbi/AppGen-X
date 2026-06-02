# Bank Payments Clearing PBC

`bank_payments_clearing` is now a standalone AppGen-X packaged business capability for ACH, wire, instant, and settlement-clearing operations. The package owns its executable schema/model contracts, in-memory service layer, route contracts, AppGen-X event envelope/handler surface, UI/workbench metadata, assistant planning helpers, release evidence, and focused tests without mutating shared generator code.

## What This Package Provides

- A package-local execution spine for participant-bank registration, payment validation, duplicate prevention, maker-checker release, liquidity controls, clearing batches, settlement files, acknowledgements, returns, reconciliation, and operator workbench evidence.
- Runtime-aligned schema and model contracts that point to real package artifacts instead of placeholder migration lists.
- An executable service and route surface for a one-PBC app, including standalone bootstrap and demo workflow smoke paths.
- Forms, wizards, controls, and workflow metadata for payment intake, release, batch assembly, return/reconciliation triage, and assistant-guided document instruction review.
- Governed assistant planning for document/instruction intake and CRUD previews with route, permission, idempotency, and AppGen-X event evidence.
- Release evidence that reports package artifacts plus repo-style gates: source artifact contract, implementation release audit, and generation smoke audit.

## Key Entrypoints

- Runtime: `runtime.py`
- Schema and models: `schema_contract.py`, `models.py`
- Services and routes: `services.py`, `service_contract.py`, `routes.py`
- UI/workbench: `ui.py`
- Standalone app surface: `standalone.py`
- Assistant planning: `agent.py`
- Release audit: `release_evidence.py`

## Standalone App Surface

The one-PBC surface exposed by this package includes:

- Owned tables, migration, schema contract, and model contract metadata
- Payment, participant-bank, acknowledgement, return, reconciliation, and document-instruction forms
- Release, batching, return/reconciliation, and assistant-review wizards
- Controls for rail validation, participant capability, duplicate prevention, maker-checker release, liquidity, settlement-file integrity, acknowledgement idempotency, reconciliation breaks, and release evidence review
- Workbench and release routes: `/bank-payments-clearing-workbench` and `/bank-payments-clearing-release-evidence`

## Validation

Focused package-local validation lives in:

- `tests/test_contract.py`
- `tests/test_payment_operations.py`
- `tests/test_standalone.py`
- `implementation-status.md`
- `RELEASE_EVIDENCE.md`
