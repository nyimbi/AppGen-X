# Insurance Underwriting Implementation Plan

## Scope

Package-local uplift only. All changes stay inside `src/pyAppGen/pbcs/insurance_underwriting`.

## Delivery Shape

1. Replace scaffold-only contracts with owned underwriting schema metadata and aligned migration DDL.
2. Add a sqlite-backed standalone store for executable submission, risk, quote, decision, bind, exclusion, parameter, rule, and event flows.
3. Expose standalone service, route, workflow, UI, and agent contracts without changing shared runtime infrastructure.
4. Update release evidence and metadata so repo-level audits can see the package-local slice.
5. Add focused tests for the underwriting lifecycle and package-local documentation/evidence artifacts.

## Guardrails

- No edits outside this PBC directory.
- No shared generator, language, or progress-ledger changes.
- Keep all cross-PBC collaboration at declared API or AppGen-X event boundaries.
- Preserve source-package entrypoints while enriching the package-local standalone slice.
