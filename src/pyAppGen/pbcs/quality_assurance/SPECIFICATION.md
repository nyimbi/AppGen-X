# Quality Assurance PBC Specification

## Purpose

`quality_assurance` owns inspection planning, inspection execution, statistical sampling, quality holds, non-conformance management, disposition, release, and compliance evidence. It composes with production, inventory, procurement, returns, maintenance, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `quality_assurance`
- Mesh: `opsmfg`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `inspection_plan`, `inspection_result`, `quality_hold`, `non_conformance`, `quality_rule`, `quality_parameter`, `quality_configuration`, `quality_capa`, `quality_compliance_package`
- Owned event tables: `quality_assurance_outbox`, `quality_assurance_inbox`, `quality_assurance_dead_letter`
- Fixed AppGen-X event topic: `appgen.quality.events`
- Consumed events: `ProductionCompleted`, `GoodsReceiptPosted`, `InventoryLotMoved`, `SupplierScoreChanged`
- Emitted events: `InspectionPlanCreated`, `InspectionResultRecorded`, `QualityHoldCreated`, `NonConformanceRaised`, `NonConformanceDispositioned`, `QualityHoldReleased`
- External access rule: no shared production, inventory, procurement, returns, maintenance, or audit tables; use projections, APIs, and events only.

## Package-Local Runtime Contract

`runtime.py` is the executable source of truth for the package-local contract. It exports stable constants for owned tables, allowed database backends, the required AppGen-X event topic, emitted events, and consumed events. `quality_assurance_configure_runtime` accepts only the ordinary relational backends: PostgreSQL, MySQL, and MariaDB. The function rejects any user-provided stream engine, transport selector, eventing mode, or alternate event topic. Eventing is always the AppGen-X contract and is never exposed as a user picker.

Schema extension is package-local. `quality_assurance_register_schema_extension` may add fields only to Quality Assurance owned tables. Foreign tables such as production order, inventory balance, supplier master, maintenance order, or audit ledger tables are not valid extension targets. This keeps cross-PBC composition at the API, event, and projection layer instead of creating hidden shared-table coupling.

Inbound AppGen-X events are handled through `quality_assurance_receive_event`. The handler writes inbox evidence, uses an idempotency key, detects duplicates without replaying side effects, projects supported consumed events into package-local projection stores, records retry evidence for failed or unsupported events, and moves exhausted events into dead-letter evidence. Production completions are projected by order, goods receipts by receipt, inventory movements by lot, and supplier score updates by supplier. These projections are read models owned by the Quality Assurance PBC; they are not shared source tables.

The descriptor API contract returned by `quality_assurance_build_api_contract` exposes command/query route descriptors with owned-table write surfaces, emitted/consumed event metadata, permission requirements, and idempotency keys. `quality_assurance_permissions_contract` describes the action-level RBAC surface for inspectors, quality engineers, hold/release users, disposition approvers, configuration administrators, auditors, and event consumers. `quality_assurance_verify_owned_table_boundary` proves that generated code and workbench bindings reference only owned tables, runtime event tables, declared dependency APIs, declared projections, or consumed event names.

## Standard Table-Stakes Capabilities

1. Inspection plan master with item, site, source, sampling method, checklist, effective dates, and revision status.
2. Sampling plans for 100-percent, fixed sample, lot percentage, and risk-based inspection.
3. Inspection result recording with measurements, pass/fail decisions, defects, attachments, and inspector identity.
4. SPC metric calculation for mean, range, sigma, Cp, Cpk, and control-limit breach evidence.
5. Quality hold creation, isolation reason, location, lot, order, and item projection.
6. Non-conformance creation with severity, defect class, root cause, disposition, and corrective action.
7. Disposition workflow for use-as-is, rework, scrap, return-to-supplier, and release.
8. Quality hold release with approval and AppGen-X event emission.
9. Production completion and goods receipt projection handling.
10. Supplier, item, site, lot, and order quality analytics.
11. CAPA evidence and effectiveness check descriptors.
12. Compliance evidence packages and audit-ready traceability.
13. Multi-tenant, multi-site, lot, and item isolation.
14. AppGen-X outbox/inbox idempotency.
15. Retry and dead-letter evidence.
16. RBAC descriptors for inspector, quality engineer, supervisor, supplier quality, auditor, and admin actions.
17. Configuration schema for runtime installation.
18. Rule engine for plan eligibility, sampling, SPC, hold, non-conformance, disposition, release, and compliance policies.
19. Parameter engine for sample size, defect thresholds, Cpk minimums, severity thresholds, CAPA due days, and retention days.
20. Seed data for inspection types, defect classes, disposition codes, severity levels, sampling methods, and release statuses.
21. Package metadata, source registration, and release evidence.
22. Package-local workbench UI for plans, inspections, SPC, holds, non-conformances, CAPA, rules, parameters, and configuration.

## Advanced Capability Requirements

The runtime must prove deterministic evidence for:

- Event-sourced quality lifecycle and immutable audit trail.
- Graph-relational quality topology across plans, inspections, holds, non-conformances, lots, items, and orders.
- Multi-tenant quality isolation and schema evolution.
- Probabilistic defect, escape, and compliance risk scoring.
- Real-time SPC and quality analytics.
- Counterfactual sampling and release-policy simulation.
- Defect and quality-escape forecasting.
- Autonomous quality exception recommendations.
- Semantic inspection instruction parsing.
- Self-healing quality, inventory, and supplier route selection.
- Zero-knowledge quality compliance proof generation.
- Dynamic quality policy screening and automated controls.
- Universal API/event contracts and cross-system quality federation.
- Production, inventory, procurement, returns, and audit integration through projections.
- Decentralized lot/item/source identity verification.
- Resilience drills, crypto agility, and carbon-aware inspection scheduling.
- Algebraic inspection allocation and mechanism-design disposition allocation.
- Information-theoretic defect anomaly detection.
- Stochastic quality exposure modeling.
- Governed quality model registration with lineage, drift, and explainability controls.

## Rules, Parameters, And Configuration

The PBC must understand and execute:

- Configuration: database backend, event topic, retry limit, allowed sites, allowed inspection sources, allowed hold reasons, allowed dispositions, default timezone, and workbench limit.
- Parameters: default sample size, defect threshold, Cpk minimum, hold severity threshold, CAPA due days, retention days, and release approval threshold.
- Rules: inspection-plan eligibility, sampling method, SPC acceptance, quality hold, non-conformance severity, disposition, release, and compliance evidence policies.

Strict guarantees:

- Runtime configuration accepts only PostgreSQL, MySQL, or MariaDB backends.
- Runtime eventing is fixed to the AppGen-X contract. There is no stream-engine picker or user-facing eventing-mode selection in configuration.
- Parameters are bounded to the supported package-local names above; unknown parameter names are rejected.
- Rules must include `rule_id`, `tenant`, `rule_type`, `eligible_sources`, `allowed_sites`, `sampling_methods`, `required_measurements`, `critical_defect_classes`, `release_dispositions`, and `status`.
- Rule registration produces deterministic compile evidence, including a stable compiled hash and normalized rule payload evidence.
- Workbench and UI renderers expose binding evidence for configuration, rules, and parameters so the installed contract can be verified from package-local outputs.

Rules are compiled into deterministic hashes and evidence, parameters are stored in owned runtime state, and configuration gates inspection, hold, non-conformance, disposition, and release operations.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- Quality assurance workbench.
- Inspection plan console.
- Inspection result capture.
- SPC dashboard.
- Quality hold board.
- Non-conformance board.
- CAPA console.
- Rule studio.
- Parameter console.
- Runtime configuration panel.

UI actions are RBAC-gated and bind only to owned tables, projections, and AppGen-X event surfaces.
The UI must keep AppGen-X eventing fixed and surface explicit configuration/rule/parameter binding evidence on the package-local workbench.
The workbench also surfaces owned table names, AppGen-X outbox/inbox/dead-letter tables, inbox/dead-letter counts, and the active RBAC action map so a generated application can prove UI fragments are wired to the package-local runtime contract.

## Release Evidence

Completion requires:

- Package-local specification, runtime, UI, and tests.
- `pbc_implementation_contract("quality_assurance")` returns an ok source package and advanced runtime.
- `pbc_implementation_release_audit(("quality_assurance",))` passes.
- `pbc_implemented_capability_audit(("quality_assurance",))` passes.
- Full 46-PBC generation smoke remains green.
