# Tax Localization Implementation Plan

## Objective

Make `tax_localization` usable as a standalone PBC with executable database-backed forms, workflows, controls, AI assistant previews, release evidence, and package-local validation.

## Scope

All work remains inside `src/pyAppGen/pbcs/tax_localization`.

## Work Items

1. Add a package-local repository contract so the slice can prove bounded persistence without shared tables.
2. Add operator-facing forms for jurisdiction setup, rule authoring, quote calculation, invoice tax recording, filing preparation, and assistant document intake.
3. Add wizard flows that connect the forms into realistic tax operations.
4. Add a control center that proves release readiness, filing gating, assistant guardrails, and owned-boundary isolation.
5. Add a standalone app-surface contract that ties repository, forms, wizards, controls, and assistant previews together.
6. Rewire UI, agent, permissions, release evidence, capability assurance, manifest metadata, and package exports to include the new standalone surface.
7. Add focused tests and implementation documentation.

## Design Constraints

- No shared-table writes.
- No stream-engine picker exposure.
- AppGen-X remains the only declared event contract.
- The standalone surface must stay domain-specific and side-effect free in contract tests.
- The repository is for deterministic local evidence and does not widen supported runtime backends.

## Verification Plan

- Compile the package Python modules.
- Run package-local tests for contracts and the standalone app surface.
- Run targeted `pyAppGen.pbc` implementation and capability audits for `tax_localization`.
- Record the results in `implementation-status.md` after validation.
