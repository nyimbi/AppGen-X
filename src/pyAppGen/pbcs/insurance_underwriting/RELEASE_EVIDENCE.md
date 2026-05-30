# Release Evidence - Insurance Underwriting

Package directory: `src/pyAppGen/pbcs/insurance_underwriting`.

This package includes aligned owned schema metadata and migration DDL, executable standalone store/services/routes/workflows, AppGen-X event and handler contracts, governance contracts, assistant skills, UI workbench/forms/wizards/controls, release evidence, metadata, documentation, and focused tests.

## Evidence Categories

- Schema and migration alignment for all owned business and event tables.
- Source-package service and API contract coverage.
- Standalone package-local app execution evidence.
- Governance coverage for rules, parameters, permissions, and authority checks.
- AppGen-X outbox/inbox/dead-letter evidence with idempotent event handling.
- Documentation coverage: `README.md`, `implementation-plan.md`, `implementation-status.md`, and this release evidence file.

## Validation Snapshot

- compile: passed via `py_compile` over the package and focused tests
- package tests: passed via direct harness fallback over `test_contract` and `test_standalone`
- focused audits: `pbc_source_artifact_contract("insurance_underwriting")` and `pbc_implementation_release_audit(("insurance_underwriting",))` both passed
- package smokes: `smoke_test()` and `insurance_underwriting_standalone_app_smoke()` both passed
- repo generation smoke: blocked by missing `antlr4` dependency in `pyAppGen.dsl`

Detailed command results are recorded in `implementation-status.md`.
