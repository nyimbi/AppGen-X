# Laboratory Information Management Standalone Implementation Plan

## Goal

Deepen `src/pyAppGen/pbcs/laboratory_information_management` into a package-local standalone LIMS slice without touching shared generator code, language files, or the progress ledger.

## Scope

- Standalone application state and service methods for laboratory operations.
- Package-local forms, wizards, controls, and standalone workbench rendering.
- Table-stakes LIMS flows: accessioning, custody, orders, methods, instruments, calibration, QC, reagent lots, analyst competency, batch runs, results, OOS, stability, and CoA.
- Regulatory evidence: audit trail hash chain, e-signatures, release gates, release evidence, and assistant CRUD previews.
- Focused package-local tests and documentation artifacts only inside this PBC directory.

## Delivery Slices

1. Add the standalone application shell with domain-deep LIMS methods and smoke coverage.
2. Materialize package-local forms, wizards, and controls around the standalone flow.
3. Extend UI and release evidence to expose the standalone slice and documentation checks.
4. Add focused standalone tests that cover end-to-end release, OOS, stability, inventory watch, and assistant previews.
5. Validate with compile, focused tests, standalone smoke, release-evidence validation, and existing contract tests.
