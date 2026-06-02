# Release Evidence - Court Case Management

Package directory: `pbcs/court_case_management`.

This PBC now includes a standalone one-PBC application surface for case intake, filing deficiency review, evidence lodging, hearing scheduling, order entry, operational tasks, workbench/detail UI metadata, governed agent assistance, AppGen-X events, package-local audits, and focused package tests.

## Evidence

- Source artifacts: `README.md`, `implementation-plan.md`, `implementation-status.md`, `RELEASE_EVIDENCE.md`, and `migrations/001_initial.sql` are present inside the package.
- Standalone app: `standalone.py` exposes an executable `CourtCaseManagementStandaloneApplication` with runtime defaults, event intake, workbench, detail, and governed mutation preview paths.
- Owned datastore boundary: every owned table starts with `court_case_management_`, including the new `court_case_management_evidence_item` and `court_case_management_case_task` tables.
- UI surface: forms, wizards, and controls cover intake, evidence, hearings, orders, tasks, and sealed-record governance.
- Agent surface: filing triage, hearing preparation, and order follow-up skills require human confirmation for mutations.
- Event contract: AppGen-X outbox, inbox, and dead-letter evidence remain fixed.
- Focused audits: `audit.py` aggregates standalone smoke, implementation audit, generation audit, docs presence, UI/agent coverage, and owned-boundary checks.
- Package tests: `tests/test_contract.py`, `tests/test_court_operations_app.py`, and `tests/test_standalone.py` cover the executable behavior.
