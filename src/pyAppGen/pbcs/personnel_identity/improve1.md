# Personnel Directory and Identity PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `personnel_identity`. The items are specific to workforce identity: departments, org topology, positions, jobs, employee records, contacts, documents, employment lifecycle, manager relationships, org assignments, work locations, cost centers, role catalogs, role assignments, access context, identity attributes, assurance, verification, provisioning, directory projections, privacy, residency, retention, policy screening, event reliability, UI workbenches, and agent-assisted people operations.

## Current Domain Evidence Used

- Domain purpose: workforce identity for departments, workers, employment facts, organization structure, position and manager relationships, role assignments, identity attributes, access context, lifecycle status, and employee events used by HCM, time, payroll, onboarding, finance, and operations packages.
- Owned boundary: departments, hierarchy, positions, jobs, employees, contacts, documents, employment lifecycle and status history, manager relationships, org assignments, work locations, cost center assignments, role assignments, role catalog, role reviews, separation checks, identity attributes, assurance, verification, proofs, access policy projections, access exceptions, provisioning events and replay, directory projections, org chart projections, privacy consent, residency rules, retention policies, policy screening, audit traces, federation projections, carbon processing windows, role/access optimization, manager capacity allocation, anomaly signals, workforce risk models/forecasts, parsed events, seed data, schema extensions, controls, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: department registration, department hierarchy, employee creation, contacts, documents, lifecycle status, role assignment, identity attributes, verification, proofs, provisioning routes, AppGen-X inbox handling, rules, parameters, configuration, org chart, workbench, schema extensions, policy screening, federation, identity verification, resilience drills, crypto epochs, role/access optimization, manager capacity allocation, controls, governed models, and boundary verification.
- Existing events and dependencies: emits `DepartmentRegistered`, `EmployeeCreated`, `EmployeeStatusChanged`, `RoleChanged`, and `IdentityAttributeChanged`; consumes `EmployeeProvisioned`, `AccessPolicyChanged`, `OrgUnitChanged`, and `RoleReviewRequested`; integrates with onboarding, time, payroll, access, finance, service, and audit through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Department master lifecycle governance

**Justification:** Departments anchor reporting, approvals, cost centers, access context, payroll/time projections, and org charts; weak department state corrupts downstream identity consumers.

**Improvement:** Add department lifecycle states, legal entity, cost center, manager, effective dates, open/closed status, source event, parent constraints, and audit evidence. Emit `DepartmentRegistered` only after readiness checks pass.

### 2. Department hierarchy integrity

**Justification:** Org hierarchy errors create approval loops, access leakage, reporting gaps, and manager-span failures.

**Improvement:** Validate hierarchy depth, cycles, effective dates, inherited legal entity/cost center constraints, manager alignment, and reorg impact. Store before/after hierarchy proofs for every structural change.

### 3. Position management controls

**Justification:** Positions connect jobs, budgets, incumbents, vacancies, managers, work locations, and access eligibility.

**Improvement:** Model position lifecycle, headcount, incumbent capacity, vacancy status, funding, role eligibility, location, manager, and effective dates. Block employee assignment to invalid or overfilled positions unless policy allows.

### 4. Job catalog governance

**Justification:** Jobs define job family, title, level, grade, compliance exposure, skills, and role eligibility.

**Improvement:** Add job family, level, grade band, FLSA/exempt-style classification where applicable, sensitive role flags, required credentials, role eligibility, and deprecation. Employee and role decisions should cite job version.

### 5. Employee identity spine

**Justification:** Every workforce event depends on a stable employee identity that survives lifecycle changes and downstream projections.

**Improvement:** Add immutable employee identity spine with employee ID, worker type, tenant/entity, hire date, primary work relationship, lifecycle state, identity assurance, and source provisioning evidence. Keep mutable attributes separate from identity.

### 6. Employee creation readiness gate

**Justification:** Creating employees from incomplete provisioning events causes payroll, time, access, and org errors.

**Improvement:** Validate provisioning projection, identity proof, legal entity, worker type, job, department, manager, work location, country, contact method, and privacy basis before employee creation. Quarantine incomplete provisioning.

### 7. Contact data privacy controls

**Justification:** Employee contact data is sensitive and varies by purpose, emergency use, payroll, identity, and notification.

**Improvement:** Model contact type, verification, primary status, purpose, privacy scope, retention, region, effective dates, and redaction rules. UI and APIs should only expose contacts allowed for the consuming purpose.

### 8. Employee document governance

**Justification:** Documents such as IDs, contracts, work authorization, certifications, and policy acknowledgements require retention and access controls.

**Improvement:** Store document metadata, type, issuing authority, verification status, expiry, storage reference, privacy classification, retention policy, and proof hash. Trigger exceptions for expired or missing mandatory documents.

### 9. Employment lifecycle state machine

**Justification:** Lifecycle state drives access, payroll, time, benefits, security, and directory visibility.

**Improvement:** Implement transitions for provisioned, active, leave, suspended, terminated, alumni, and rehire-eligible states with allowed sources, reasons, effective dates, grace periods, emitted `EmployeeStatusChanged`, and downstream impact.

### 10. Bitemporal status history

**Justification:** Personnel audits need to answer what was valid, known, and processed at any point in time.

**Improvement:** Store valid time, event time, processing time, actor, source event, reason, and correction link for status history. Org chart and directory queries should support as-of reconstruction.

### 11. Manager relationship governance

**Justification:** Manager relationships drive approvals, access reviews, time approvals, performance workflows, and escalation paths.

**Improvement:** Add manager relationship types, primary/secondary managers, dotted-line relationships, effective dates, capacity, delegation, conflict checks, and cycle prevention. Emit review tasks when manager changes affect approvals.

### 12. Org assignment completeness

**Justification:** Employees may have multiple assignments across departments, roles, projects, legal entities, and countries.

**Improvement:** Model assignment type, primary flag, effective dates, allocation percent, department, position, job, manager, location, and cost center. Validate assignment totals and overlaps.

### 13. Work location and residency rules

**Justification:** Location affects tax, time, payroll, compliance, privacy residency, emergency response, and access.

**Improvement:** Add work location records with country, region, remote/hybrid/site type, effective dates, residency rule, allowed roles, privacy zone, and emergency contact requirements. Screen location changes for downstream impact.

### 14. Cost center assignment lineage

**Justification:** Cost center data feeds payroll distribution, finance, approvals, and reporting but must remain owned or projected correctly.

**Improvement:** Track cost center assignment source, percentage, effective dates, legal entity, project relation, validation projection, and change reason. Reject direct finance table access and use declared projections.

### 15. Role catalog risk model

**Justification:** Roles encode access context and risk; vague roles create access sprawl and review failures.

**Improvement:** Define role catalog with owner, sensitivity, access domain, required job/position eligibility, incompatible roles, review cadence, expiry default, and risk score. Role assignments should cite role version.

### 16. Role assignment lifecycle

**Justification:** Role changes affect access, time, payroll, approvals, and operations.

**Improvement:** Model role assignment states, start/end, request source, eligibility, approval, expiry, removal, and emitted `RoleChanged`. Automatically flag stale, orphaned, or incompatible assignments.

### 17. Segregation-of-duties checks

**Justification:** Incompatible roles can create fraud, privacy, or operational risk.

**Improvement:** Add separation checks for role pairs, job/department combinations, manager/subordinate conflicts, sensitive attribute access, and emergency exceptions. Block high-severity conflicts by default.

### 18. Role review workflow

**Justification:** Access review must be continuous and evidence-based, not periodic spreadsheet cleanup.

**Improvement:** Ingest `RoleReviewRequested`, create review tasks, show current assignments, usage/projection context, risk, manager/owner decision, remediation, and overdue escalation. Preserve review evidence.

### 19. Identity attribute taxonomy

**Justification:** Identity attributes such as email, badge, directory ID, clearance, region, payroll/time profile, and employment profile need governance.

**Improvement:** Add attribute definitions with datatype, sensitivity, purpose, source trust, verification requirement, retention, allowed regions, and downstream consumers. Attribute updates should emit `IdentityAttributeChanged`.

### 20. Identity assurance scoring

**Justification:** Workforce decisions need confidence in identity evidence, especially for remote, contractor, privileged, or regulated roles.

**Improvement:** Score assurance from identity proof, verification method, credential strength, document confidence, recency, risk, and role sensitivity. Block high-risk actions below assurance threshold.

### 21. Identity verification workflow

**Justification:** Verification is a controlled process requiring evidence, reviewer, method, and expiry.

**Improvement:** Add verification states, method, evidence hash, provider/reference, verifier, confidence, expiry, failed reason, and re-verification triggers. UI should show verification gaps by worker group.

### 22. Personnel eligibility proof

**Justification:** Downstream packages need proof of worker eligibility without seeing all personnel data.

**Improvement:** Generate redacted proofs for active employment, role eligibility, identity assurance, manager relationship, work location, and policy status with verification API and hash.

### 23. Access policy projection handling

**Justification:** Personnel decisions need access context but must not own the access control system.

**Improvement:** Project `AccessPolicyChanged` into access policy snapshots with freshness, affected roles, risk, and decision impact. Role and lifecycle changes should warn on stale policy projections.

### 24. Access exception management

**Justification:** Access exceptions arise from emergency roles, incompatible assignments, lifecycle mismatch, or stale policy.

**Improvement:** Add exception states, severity, role, employee, policy, owner, expiry, remediation, and closure evidence. Workbench should rank exceptions by access risk.

### 25. Provisioning route governance

**Justification:** Employee provisioning events can fail, duplicate, or route to wrong downstream systems.

**Improvement:** Track provisioning route, source event, target projection, retry, replay, status, idempotency key, failure reason, and downstream emitted events. Provide safe replay with impact preview.

### 26. Employee provisioning replay

**Justification:** Replaying provisioning events without controls can duplicate employees or corrupt lifecycle history.

**Improvement:** Add replay eligibility checks, duplicate detection, previous outcome, changed projection diff, authorization, and dead-letter linkage. Replays should be side-effect safe.

### 27. Directory projection quality

**Justification:** Directory search and read models power many packages and must be fresh, privacy-filtered, and correct.

**Improvement:** Build directory projections with profile fields, role, department, manager, location, lifecycle state, privacy filters, freshness, and source trace. Score projection quality and expose stale data warnings.

### 28. Org chart projection reconstruction

**Justification:** Org charts need accurate as-of views for planning, audits, approvals, and reorgs.

**Improvement:** Generate org chart projections with departments, positions, employees, manager relationships, vacancies, spans, and effective dates. Support as-of views and reorg simulation.

### 29. Privacy consent for personnel data

**Justification:** Workforce data use requires purpose, consent or lawful basis, region, retention, and minimization controls.

**Improvement:** Track privacy consent/lawful basis by data category, purpose, region, capture source, expiry, withdrawal, and downstream impact. Policy screening should enforce allowed use.

### 30. Retention and minimization policy

**Justification:** Personnel data must be retained long enough for compliance but minimized after purpose expiry.

**Improvement:** Add retention policies by record type, jurisdiction, lifecycle state, legal hold, and anonymization action. Workbench should show purge/anonymization readiness and blockers.

### 31. Residency rule enforcement

**Justification:** Personnel data residency affects storage, processing, access, and federation.

**Improvement:** Model residency zones, allowed processing regions, transfer restrictions, sensitive attributes, and exception approvals. Block actions that violate residency policy.

### 32. Personnel policy screening

**Justification:** Employee, role, location, attribute, lifecycle, and provisioning actions need consistent policy evaluation.

**Improvement:** Screen department, employee, role, attribute, verification, proof, provisioning, privacy, and retention commands. Store policy version, attributes evaluated, decision, explanation, and override path.

### 33. Workforce identity anomaly detection

**Justification:** Unusual identity, role, manager, status, or provisioning changes can indicate fraud, data quality issues, or integration failures.

**Improvement:** Detect anomalies in duplicate employees, rapid role changes, manager loops, lifecycle reversals, stale attributes, location conflicts, provisioning retries, and access exceptions. Route to review with explanations.

### 34. Workforce risk forecast

**Justification:** People operations need proactive risk signals across access, attrition, manager capacity, staffing, and compliance.

**Improvement:** Forecast workforce risk by department, role, location, lifecycle, manager span, access risk, and projection freshness. Include confidence, drift, and mitigation actions.

### 35. Manager capacity allocation

**Justification:** Manager span affects approvals, onboarding, performance, access review, and operational load.

**Improvement:** Model manager capacity by team size, role mix, location, review load, approval tasks, onboarding load, and risk. Recommend capacity balancing while preserving business constraints.

### 36. Role and access optimization

**Justification:** Role assignments should minimize overprivilege while preserving job effectiveness.

**Improvement:** Optimize role bundles using job, position, department, access projection, usage evidence, risk, and SoD constraints. Provide least-privilege recommendations with human approval.

### 37. Personnel MLOps governance

**Justification:** Identity assurance, anomaly, workforce risk, role optimization, and manager capacity models affect workers and access decisions.

**Improvement:** Add model registry, feature lineage, training windows, approval status, explainability, drift monitoring, fairness checks, rollback, and release evidence for all personnel models.

### 38. Immutable personnel audit trace

**Justification:** Workforce identity changes are high-control events with downstream payroll, time, access, and finance impact.

**Improvement:** Hash-chain departments, hierarchy, employees, status changes, roles, attributes, verifications, proofs, provisioning, privacy actions, agent previews, and event handling. Support temporal reconstruction.

### 39. AppGen-X event reliability cockpit

**Justification:** Personnel Identity depends on provisioning/access/org/role review events and emits employee and role events used by other PBCs.

**Improvement:** Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream event effects. Warn when stale projections affect decisions.

### 40. Boundary proof for personnel ownership

**Justification:** Personnel Identity must integrate with onboarding, time, payroll, access, finance, service, and audit without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only personnel-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct payroll, time, access, finance, service, onboarding, and audit table access.

### 41. Personnel workbench coverage

**Justification:** HR operations, managers, access reviewers, and auditors need the full personnel identity surface in UI.

**Improvement:** Expand UI into department console, hierarchy editor, position/job catalog, employee master, contacts, documents, lifecycle board, manager hierarchy, org assignments, locations, cost centers, role catalog, role assignment, role reviews, identity attributes, assurance, proofs, provisioning monitor, privacy center, directory search, org chart, controls, rules, parameters, configuration, events, and agent panels.

### 42. Agent-safe personnel document intake

**Justification:** The personnel_identity chatbot should parse provisioning packets, employee documents, org change notes, role requests, and verification evidence without unsafe writes.

**Improvement:** Add intake skills that extract candidate personnel facts, map them to owned tables, validate rules/permissions/privacy, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, and expected AppGen-X events.

### 43. Agent-safe identity and role planning

**Justification:** AI assistance in personnel identity can affect access, payroll, time, and privacy, so it must be strictly bounded.

**Improvement:** Require agent plans for employee creation, lifecycle changes, role assignments, attribute updates, verification, proofs, provisioning replay, and privacy actions to list command, permission, owned tables, idempotency key, emitted event, downstream impact, rollback limits, and human approval.

### 44. Counterfactual org and role simulation

**Justification:** Reorgs and role policy changes can disrupt approvals, access, payroll, time, and reporting.

**Improvement:** Simulate department moves, manager changes, role rule changes, span limits, assurance thresholds, and lifecycle policies against current personnel data. Show impacted workers, risks, and downstream event changes.

### 45. Carbon-aware identity processing

**Justification:** Non-urgent directory rebuilds, proof generation, and analytics jobs can be scheduled with energy-aware windows.

**Improvement:** Add carbon-aware windows for bulk projections, proof generation, role review analytics, and model refresh while preserving urgent lifecycle, access, and privacy actions.

### 46. Provisioning resilience drills

**Justification:** Personnel operations depend on event delivery and downstream projection health.

**Improvement:** Add drills for duplicate `EmployeeProvisioned`, access policy outage, org unit replay, role review retry, dead-letter replay, provisioning route failure, and stale projection recovery. Store drill evidence in release gates.

### 47. Crypto-agile identity authorization

**Justification:** Identity proofs, role decisions, and audit traces require durable cryptographic evidence.

**Improvement:** Add crypto epoch metadata, signed proof references, key rotation evidence, policy version, and migration readiness for future algorithms without binding business rules to a single primitive.

### 48. Continuous personnel control testing

**Justification:** Controls should run continuously across departments, employees, roles, lifecycle, identity, privacy, provisioning, and event handling.

**Improvement:** Add assertions for duplicate employee IDs, invalid manager loops, role SoD breach, stale identity assurance, expired documents, lifecycle/access mismatch, privacy violation, dead-letter aging, direct foreign-table access, and agent-preview bypass.

### 49. Personnel Identity readiness score

**Justification:** Users need an evidence-backed view of whether Personnel Identity is ready for production people operations.

**Improvement:** Compute readiness from org setup, employee identity quality, lifecycle states, manager hierarchy, role catalog, role reviews, identity attributes, assurance, provisioning, privacy policy, event reliability, UI coverage, boundary proof, controls, model governance, and agent safety.

### 50. End-to-end workforce identity proof

**Justification:** A complete Personnel Identity PBC must prove it can run the full lifecycle from provisioning to downstream employee and role events.

**Improvement:** Add an executable proof scenario covering department registration, hierarchy, employee creation from provisioning event, identity verification, role assignment, attribute update, lifecycle transition, org chart projection, privacy screening, emitted `EmployeeCreated`, `RoleChanged`, and `IdentityAttributeChanged`, UI evidence, controls, and agent explanation.
