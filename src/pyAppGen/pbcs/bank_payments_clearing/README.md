# Bank Payments Clearing PBC

The Bank Payments Clearing PBC owns the operational lifecycle of payment instructions after they enter the clearing domain. It validates instructions, applies participant-bank and rail rules, releases payments through maker-checker control, assembles clearing batches, generates settlement files, processes acknowledgements and returns, and reconciles bank statement evidence.

This PBC does not own deposit accounts, fraud master data, sanctions lists, FX rates, billing, or general ledger postings. Those concerns arrive as AppGen-X events, API projections, or immutable evidence references. The PBC stores its own decisions, exceptions, runtime parameters, rules, outbox/inbox evidence, and operator workbench state.

## Executable Surfaces

- `payment_operations.py` implements the domain execution slice.
- `runtime.py` exports package-level aliases and includes the payment operations evidence in runtime smoke checks.
- `services.py` exposes the payment operations in `service_operation_manifest()`.
- `ui.py` adds payment-release, clearing-batch, settlement-file, return, and reconciliation workbench actions.
- `agent.py` contributes assistant skills for payment validation, release decisions, batch assembly, acknowledgement explanation, and exception triage.
- `release_evidence.py` validates the executable payment operations alongside the existing generated release checks.

## Core Workflows

- Register participant banks with supported rails and routing identifiers.
- Validate payment instructions against rail limits, beneficiary/originator data, participant-bank status, screening freshness, and duplicate signatures.
- Release instructions only when maker-checker and liquidity controls pass.
- Assemble clearing batches idempotently and lock finalized batches.
- Generate settlement files with deterministic control totals, checksums, and signature evidence.
- Process accepted, rejected, duplicate, and partial acknowledgements.
- Process returns with reason-specific repair eligibility and financial impact.
- Reconcile statement lines, fees, variances, and unmatched records into operator-visible breaks.

## Single-PBC App Surface

A composed application containing only this PBC has enough surface to operate the payment-clearing domain:

- Database backing through owned tables, the package migration, generated models, and schema contracts.
- Forms for payment instructions, participant banks, settlement acknowledgements, returns, and bank reconciliation.
- Wizards for payment release, clearing batch assembly, and return/reconciliation triage.
- Controls for rail validation, participant-bank capability, duplicate prevention, maker-checker release, liquidity buffers, settlement-file integrity, acknowledgement idempotency, return deadlines, and reconciliation break creation.
- Workbench views and assistant skills that expose the same executable operations.

## Governance Boundaries

The implementation uses AppGen-X event evidence only and keeps every table reference within `bank_payments_clearing_*`. Stream-engine pickers are not visible to users. Reconciliation and settlement outcomes are emitted as domain evidence; external account ledgers and GL systems consume those facts through declared contracts.
