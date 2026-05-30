# Trade Finance Operations Implementation Plan

## Goal

Turn `trade_finance_operations` into an executable one-PBC trade finance app inside its own package directory, with no edits to shared generator, language, or repo-level documentation files.

## Selected Backlog Themes

- Instrument issuance across letters of credit, guarantees, and SBLC
- Documentary collections, trade bills, and trade-loan linkage
- Shipment document intake, sanctions and compliance screening, and discrepancy handling
- Collateral and margin cover, limit reservations, fee accrual, and settlement orchestration
- SWIFT-like message evidence and release-evidence pack automation
- Forms, wizards, controls, workbench, detail, and assistant surfaces
- AppGen-X-only eventing, governed datastore CRUD, and confirmation-gated skills
- Package-local audits, smoke checks, and standalone journey tests

## Execution Steps

1. Replace the generic package scaffolding with trade-finance-specific domain operations, schema/service/release contracts, emitted events, and workbench metadata.
2. Add package-local forms, wizards, and controls for issuance, examination, sanctions guidance, collateral/limits, settlement, and release gating.
3. Implement a standalone one-PBC app shell with executable issuance, document, sanctions, discrepancy, collateral, fee, settlement, and SWIFT-evidence workflows.
4. Wire those surfaces into the UI contract, route metadata, agent/chatbot contract, and capability assurance checks while preserving AppGen-X eventing and hidden stream-engine controls.
5. Hand-craft `README.md`, `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`, `implementation-plan.md`, and `implementation-status.md` so source/spec audits can trace the package and its release evidence.
6. Run compile, local tests, focused audits, `git diff --check`, then commit and push with a Lore-format message.
