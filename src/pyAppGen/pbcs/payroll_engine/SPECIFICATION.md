# Payroll Engine PBC Specification

## Purpose

`payroll_engine` owns gross-to-net payroll execution, payroll deductions, benefit allocations, payslips, payroll postings, and localized payroll filing preparation. It composes with personnel, time/labor, tax, treasury, general ledger, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `payroll_engine`
- Mesh: `hcm`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `payroll_run`, `payslip`, `deduction`, `benefit_allocation`
- Owned event tables: `payroll_engine_outbox`, `payroll_engine_inbox`, `payroll_engine_dead_letter`
- Consumed events: `LaborHoursApproved`, `TaxCalculated`
- Emitted events: `PayrollPosted`, `PayrollFilingPrepared`
- External access rule: no shared personnel, labor, tax, treasury, or ledger tables; use projections, APIs, and events only.

## Standard Table-Stakes Capabilities

1. Payroll calendar and run creation by tenant, legal entity, country, and period.
2. Worker payroll projection from personnel identity events.
3. Payroll-ready labor ingestion from the Time and Labor PBC.
4. Salary, hourly, overtime, premium, and supplemental gross pay calculation.
5. Pre-tax, post-tax, garnishment, loan, and employer deduction handling.
6. Benefit allocation, employer contribution, employee contribution, and eligibility handling.
7. Localized tax basis projection from tax events.
8. Gross-to-net payslip calculation with rounding and precision parameters.
9. Payroll approval workflow and posting controls.
10. Payslip publication and employee access descriptors.
11. Payroll filing preparation by jurisdiction and statutory channel.
12. Payment batch readiness for treasury handoff without treasury table access.
13. Journal posting readiness for finance handoff without ledger table access.
14. Retroactive adjustment and correction plan evidence.
15. Off-cycle payroll and termination payout support.
16. Multi-tenant and multi-entity isolation.
17. AppGen-X outbox/inbox idempotency.
18. Retry and dead-letter policy evidence.
19. RBAC descriptors for payroll operations and administration.
20. Configuration schema for runtime installation.
21. Rule engine for pay, deduction, benefit, approval, and filing policies.
22. Parameter engine for thresholds, rates, precision, and routing behavior.
23. Seed data for pay codes, deduction classes, benefit classes, filing channels, and payroll calendars.
24. Package metadata, release evidence, and source-owned implementation contract.
25. Package-local workbench UI for run control, payslips, deductions, benefits, filings, rules, parameters, and configuration.

## Advanced Capability Requirements

The runtime must prove the following advanced capabilities with deterministic smoke evidence:

- Event-sourced payroll lifecycle and immutable hash-chained audit trail.
- Graph-relational compensation topology across worker, run, payslip, deduction, benefit, tax, and posting projections.
- Multi-tenant payroll isolation and controlled schema evolution.
- Probabilistic payroll anomaly and compliance risk scoring.
- Real-time gross-to-net analytics and counterfactual pay policy simulation.
- Payroll cash forecasting and temporal exposure modeling.
- Autonomous payroll exception recommendations.
- Semantic payroll instruction parsing.
- Self-healing payroll payment and filing route selection.
- Zero-knowledge payroll proof generation for limited disclosure.
- Dynamic payroll policy screening and automated payroll control testing.
- Universal API and event contracts.
- Cross-system payroll federation through projections.
- Employee identity verification for payroll eligibility.
- Resilience drills, crypto-agility, and carbon-aware payroll batch scheduling.
- Algebraic payroll batch optimization and mechanism-design cash allocation.
- Information-theoretic payroll anomaly detection.
- Governed payroll model registration with lineage, drift, and explainability controls.

## Rules, Parameters, And Configuration

The PBC must understand and execute:

- Configuration: database backend, event topic, retry limit, default currency, allowed countries, allowed payment rails, allowed filing channels, payroll precision, and workbench limit.
- Parameters: standard pay period hours, overtime multiplier, supplemental rate, rounding precision, net pay floor, filing materiality threshold, and approval amount threshold.
- Rules: pay eligibility, deduction limits, benefit classes, filing channels, approval requirements, country policy, off-cycle eligibility, and garnishment priority.

Runtime behavior must compile rules into deterministic hashes, store parameters in owned state, reject backend configuration outside PostgreSQL, MySQL, or MariaDB, bind eventing to the AppGen-X event contract without user-facing stream-engine selection, and reject or flag operations that violate configuration or rule constraints.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- Payroll operations workbench.
- Payroll run console.
- Payslip calculation and review.
- Deduction and benefit editors.
- Filing preparation console.
- Rule studio.
- Parameter console.
- Runtime configuration panel.

UI actions must be RBAC-gated and bind only to owned tables, projections, and AppGen-X event surfaces.

## Release Evidence

Completion requires:

- Package-local specification, runtime, UI, and tests.
- `pbc_implementation_contract("payroll_engine")` returns an ok source package and advanced runtime.
- `pbc_implementation_release_audit(("payroll_engine",))` passes.
- `pbc_implemented_capability_audit(("payroll_engine",))` passes.
- Generation smoke for the full PBC catalog remains green.
