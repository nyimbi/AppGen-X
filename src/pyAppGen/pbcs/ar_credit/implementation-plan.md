# Accounts Receivable and Credit Implementation Plan

## Scope

This slice implements real executable AR and credit behavior inside
`src/pyAppGen/pbcs/ar_credit` without crossing the owned datastore boundary.
The focus is a practical invoice-to-cash slice from `improve1.md`:

1. Customer credit onboarding evidence pack.
2. Invoice issuance completeness gate.
3. Semantic remittance intake and executable cash application.
4. Collections follow-up evidence built from aging, dunning, and statements.

## Planned Changes

### 1. Add a package-local workflow module

- Create a deterministic workflow module for:
  - credit onboarding review,
  - invoice readiness review,
  - receipt application execution,
  - collections follow-up assembly,
  - release evidence for the implemented backlog slice.
- Keep all outputs side-effect-free except when explicitly applying state
  transitions through the existing runtime functions.

### 2. Upgrade the service surface from metadata-only to executable wrappers

- Keep the existing `command_ar_*` and `query_ar_*` contract names.
- Make the main AR operations execute the runtime/workflow logic when the
  caller provides state and payload, instead of returning only route metadata.
- Preserve AppGen-X and owned-table-only evidence in service contracts.

### 3. Expose the slice through agent and UI contracts

- Add agent previews for credit onboarding, invoice readiness, cash
  application, and collections follow-up.
- Extend document-intake hints so AR-specific instructions suggest the correct
  executable workflow.
- Add UI workflow metadata so generated workbenches can surface the slice.

### 4. Attach release evidence and implementation artifacts

- Publish implemented backlog items and generated artifact evidence from the
  new workflow slice.
- Keep release readiness checks on AppGen-X-only eventing and owned tables.
- Add package-local `README.md` and `implementation-status.md`.

## Review Checklist

- Only owned AR tables are referenced.
- AppGen-X remains the only event contract exposed.
- The new service path executes real AR behavior for the selected slice.
- Agent and UI contracts point to executable slice operations instead of docs.
- Tests prove positive and negative behavior, not only contract shape.

## Deferred Work

Later slices can deepen dispute case execution, promise-to-pay tracking,
chargebacks, invoice finance lifecycle state, and more complete credit-policy
compilation.
