# Talent Onboarding PBC Specification

## Purpose

`talent_onboarding` owns talent acquisition and day-one onboarding from job requisition through candidate pipeline, screening, offer, onboarding tasks, and employee provisioning handoff. It composes with personnel identity, access, payroll, notification, and audit capabilities only through AppGen-X APIs, events, and projections.

## Owned Boundary

- PBC key: `talent_onboarding`
- Mesh: `hcm`
- Owned datastore backends: PostgreSQL, MySQL, or MariaDB
- Owned tables: `candidate`, `job_requisition`, `background_check`, `onboarding_task`
- Owned event tables: `talent_onboarding_outbox`, `talent_onboarding_inbox`, `talent_onboarding_dead_letter`
- Consumed events: `RoleChanged`
- Emitted events: `EmployeeProvisioned`, `CandidateHired`
- External access rule: no shared personnel, payroll, access, or recruiting-provider tables; use projections, APIs, and events only.

## Standard Table-Stakes Capabilities

1. Job requisition creation, approval, opening, pause, and closure.
2. Position, hiring manager, department, location, budget, and headcount descriptors.
3. Candidate profile capture with consent, source, skills, identity, and contact facts.
4. Candidate pipeline stages from application through screen, interview, offer, hire, rejection, or withdrawal.
5. Interview plan and evaluation evidence descriptors.
6. Background check request, result capture, adjudication, and adverse-action evidence.
7. Offer creation, compensation package projection, acceptance, decline, and expiry handling.
8. Onboarding task generation by role, location, worker type, and jurisdiction.
9. Task assignment, due dates, completion, exceptions, and manager/HR review.
10. Employee provisioning event generation for the Personnel Identity PBC.
11. Candidate hire event generation for analytics and downstream workflows.
12. Role-change projection handling without shared identity tables.
13. Consent, privacy, retention, and data-minimization policy descriptors.
14. Diversity, source-channel, cycle-time, and conversion analytics.
15. Multi-tenant and multi-entity isolation.
16. AppGen-X outbox/inbox idempotency.
17. Retry and dead-letter evidence.
18. RBAC descriptors for recruiter, hiring manager, HR operations, auditor, and admin actions.
19. Configuration schema for runtime installation.
20. Rule engine for eligibility, checks, offers, onboarding, retention, and provisioning policies.
21. Parameter engine for score thresholds, SLA days, expiry windows, and task due dates.
22. Seed data for pipeline stages, check types, offer templates, task templates, and rejection reasons.
23. Package metadata, source registration, and release evidence.
24. Package-local workbench UI for requisitions, candidates, checks, offers, onboarding, rules, parameters, and configuration.

## Advanced Capability Requirements

The runtime must prove deterministic evidence for:

- Event-sourced talent lifecycle and immutable audit trail.
- Graph-relational hiring topology across requisitions, candidates, checks, offers, tasks, roles, and provisioning.
- Multi-tenant talent isolation and schema evolution.
- Probabilistic candidate-match, fraud, and compliance risk scoring.
- Real-time pipeline analytics and counterfactual hiring-policy simulation.
- Hiring demand and cycle-time forecasting.
- Autonomous candidate exception recommendations.
- Semantic resume/candidate instruction parsing.
- Self-healing screening and provisioning route selection.
- Zero-knowledge candidate eligibility proofs.
- Dynamic talent policy screening and automated controls.
- Universal API/event contracts and cross-system talent federation.
- Decentralized candidate identity verification.
- Resilience drills, crypto agility, and carbon-aware interview/onboarding scheduling.
- Algebraic pipeline optimization and mechanism-design interview allocation.
- Information-theoretic hiring anomaly detection.
- Stochastic hiring exposure modeling.
- Governed talent model registration with lineage, drift, and explainability controls.

## Rules, Parameters, And Configuration

The PBC must understand and execute:

- Configuration: database backend, event topic, retry limit, allowed countries, allowed candidate sources, allowed background check providers, allowed task types, default timezone, and workbench limit.
- Parameters: minimum match score, offer expiry days, onboarding SLA days, maximum active requisitions per manager, background check confidence threshold, and retention days.
- Rules: job eligibility, candidate consent, stage progression, background check adjudication, offer approval, onboarding task templates, and provisioning eligibility.

Rules are compiled into deterministic hashes, parameters are stored in owned runtime state, backend configuration rejects anything outside PostgreSQL, MySQL, or MariaDB, eventing remains bound to the AppGen-X event contract without user-facing stream-engine selection, and configuration gates candidate, check, task, and provisioning operations.

## UI Contract

`ui.py` owns package-local UI contract functions for:

- Talent onboarding workbench.
- Requisition console.
- Candidate pipeline board.
- Background check review.
- Offer approval board.
- Onboarding task board.
- Rule studio.
- Parameter console.
- Runtime configuration panel.

UI actions are RBAC-gated and bind only to owned tables, projections, and AppGen-X event surfaces.

## Release Evidence

Completion requires:

- Package-local specification, runtime, UI, and tests.
- `pbc_implementation_contract("talent_onboarding")` returns an ok source package and advanced runtime.
- `pbc_implementation_release_audit(("talent_onboarding",))` passes.
- `pbc_implemented_capability_audit(("talent_onboarding",))` passes.
- Full 46-PBC generation smoke remains green.
