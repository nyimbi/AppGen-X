# Bank Payments Clearing Implementation Plan

## Improvement Focus

`improve1.md` calls out a broad payments-operations backlog: stateful payment instructions, rail profiles, participant-bank governance, validation and screening evidence, limits, clearing batches, cutoffs, settlement files, acknowledgements, returns, exception taxonomy, repair, cancellation, liquidity checks, and reconciliation. This slice implements the core execution spine those capabilities depend on.

## Plan

1. Add a package-local payment operations runtime that owns only `bank_payments_clearing_*` concepts and uses AppGen-X event evidence.
2. Implement participant-bank registration and payment instruction validation with rail-specific limits, party data checks, screening freshness, duplicate detection, and exception creation.
3. Implement maker-checker release with liquidity evidence, then batch assembly with cutoff handling and finalization locks.
4. Implement settlement-file generation with reproducible control totals, checksums, and signatures, plus acknowledgement handling for accepted, rejected, duplicate, and partial outcomes.
5. Implement return-item processing and bank-statement reconciliation with fee, one-to-one, variance, and unmatched-line evidence.
6. Wire the new operations into runtime capability lists, service manifests, UI action surfaces, agent contributions, and release evidence.
7. Add package-local tests and perform a code-review pass focused on boundary safety, idempotent behavior, and whether the runtime exposes enough evidence for operators.

## Non-Goals

- Do not own customer accounts, sanctions master data, fraud case management, general ledger, FX rates, or billing tables.
- Do not expose stream-engine pickers or alternate eventing choices.
- Do not add external dependencies or change files outside this PBC directory.
