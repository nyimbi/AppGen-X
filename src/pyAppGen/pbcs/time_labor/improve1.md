# Time Attendance and Labor Tracking PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `time_labor`. The items are specific to workforce time and labor operations: schedules, shift patterns, assignments, swaps, schedule bids, labor demand, clock devices, clock events, geofences, exceptions, calculated time entries, breaks, overtime, premiums, holidays, absences, entitlements, approvals, labor summaries, labor costing, payroll-ready proofs, projections, policy screening, workbench coverage, and agent-assisted time operations.

## Current Domain Evidence Used

- Domain purpose: workforce time, attendance, schedules, absences, overtime, geo-fenced clock events, labor allocation, approvals, and payroll-ready labor summaries.
- Owned boundary: shifts, patterns, assignments, swap requests, schedule bids, labor demand forecasts, clock events, clock devices, clock source routes, clock exceptions, time entries and lines, break deductions, overtime buckets, premium calculations, holiday calendars, absences, absence balances, entitlements, approvals, labor summaries and lines, cost allocation, labor distribution, approval workflows and tasks, employee/role/payroll/warehouse/manufacturing/project projections, policy screenings, audit traces, hours proofs, federation projections, carbon schedule windows, schedule optimization, shift allocation, anomaly signals, labor risk models/forecasts, parsed events, seed data, schema extensions, control assertions, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: shift creation, shift patterns, shift swaps, clock events, time-entry calculation, absences, labor summary approval, AppGen-X inbox handling, rules, parameters, configuration, labor summary queries, time workbench, schema extension, policy screening, hours proof, schedule optimization, controls, and release evidence.
- Existing events and dependencies: emits `ShiftCreated`, `ClockEventRecorded`, `TimeEntryCalculated`, `LaborHoursApproved`, and `AbsenceRecorded`; consumes employee and role events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Shift readiness gate

**Justification:** A shift missing employee projection, role, site, cost center, job, time zone, eligibility, or labor policy evidence creates downstream clock and payroll exceptions.

**Improvement:** Add shift readiness checks for employee projection freshness, role eligibility, site/calendar, planned start/end, cost center/project, job, time zone, union/local rule, holiday context, and approval state. Block publish or assignment until mandatory evidence is complete.

### 2. Shift pattern lifecycle governance

**Justification:** Patterns encode recurring labor commitments and can create overtime, fatigue, coverage, and compliance problems if uncontrolled.

**Improvement:** Model pattern states, recurrence, effective dates, rotation rules, rest-period constraints, site applicability, role requirements, holiday behavior, and deprecation path. Simulate impact before activating pattern changes.

### 3. Shift assignment eligibility engine

**Justification:** Assignments must respect employee status, role, certification, availability, labor rules, rest periods, site access, and cost allocation.

**Improvement:** Score assignment eligibility using employee/role projections, schedule conflicts, absence, rest rules, certifications, overtime exposure, site authorization, and preference. Explain rejected assignments and required overrides.

### 4. Schedule bidding controls

**Justification:** Schedule bidding can improve fairness but must preserve coverage, skills, seniority, compliance, and fatigue protections.

**Improvement:** Add bid windows, eligibility, ranking rules, seniority/preference weighting, fairness constraints, conflict checks, and award evidence. Workbench should show why bids won or lost.

### 5. Shift swap workflow

**Justification:** Swaps affect coverage, qualifications, overtime, premiums, approvals, and payroll readiness.

**Improvement:** Add swap states, initiating/receiving employee, role/site compatibility, overtime impact, rest-period validation, manager approval, expiry, cancellation, and emitted evidence. Reject swaps that create compliance violations unless approved override exists.

### 6. Labor demand forecast governance

**Justification:** Staffing plans depend on forecasts that may be uncertain and biased by seasonality, volume, promotions, and site operations.

**Improvement:** Store demand forecast source, window, required hours, role mix, site, confidence, assumptions, drift, and realized variance. Use forecasts to guide scheduling while exposing uncertainty.

### 7. Schedule optimization with hard constraints

**Justification:** Optimized schedules must balance demand, availability, fairness, cost, overtime, rest, skills, and preferences.

**Improvement:** Add optimizer evidence with hard constraints, soft preferences, objective weights, rejected alternatives, labor cost impact, overtime exposure, fatigue risk, and fairness metrics. Require human approval before publishing optimized schedules.

### 8. Mechanism-design shift allocation

**Justification:** Shift allocation can create perceived unfairness, overtime concentration, or undesirable assignment patterns.

**Improvement:** Add allocation mechanisms for seniority, preference, fairness, coverage, skill scarcity, fatigue, and emergency staffing. Simulate allocation outcomes and publish auditable rationale.

### 9. Clock device registry

**Justification:** Clock evidence is only trustworthy when the device, source, firmware, location, and authorization are known.

**Improvement:** Track devices with type, site, geofence, firmware, trust level, owner, offline capability, last heartbeat, tamper status, and allowed clock actions. Clock events should cite device trust.

### 10. Clock source routing and failover

**Justification:** Kiosks, mobile apps, badges, web, and integrations fail differently and need controlled fallback.

**Improvement:** Add source route policies with priority, source health, offline mode, replay behavior, duplicate handling, and fallback approval. The workbench should show route health and source-specific exceptions.

### 11. Geo-fenced clock validation

**Justification:** Location evidence reduces time fraud but can be inaccurate or inappropriate without policy nuance.

**Improvement:** Validate clock events against site geofence, accuracy radius, device trust, employee/site assignment, privacy policy, and override reason. Store location confidence rather than treating all failures as fraud.

### 12. Clock sequence state machine

**Justification:** Time calculations require valid in/out/break sequences and clear handling of missed, duplicate, or out-of-order punches.

**Improvement:** Implement sequence validation for clock-in, clock-out, meal start/end, break start/end, transfer, and correction events. Create typed exceptions for sequence gaps and allow controlled repair.

### 13. Clock exception taxonomy

**Justification:** Generic exceptions hide root causes and create payroll rework.

**Improvement:** Define exceptions for missed punch, duplicate punch, early/late clock, geofence failure, unauthorized source, role mismatch, shift mismatch, overlapping shift, stale offline replay, and manual correction. Each exception should define owner, SLA, recovery action, and payroll impact.

### 14. Time entry calculation trace

**Justification:** Employees, managers, payroll, and auditors need to understand how raw clock events became payable time.

**Improvement:** Store calculation trace with source events, rounding rule, break deduction, shift differential, overtime bucket, premium, exception adjustments, time zone, policy hash, and resulting lines. Recalculation should preserve versions.

### 15. Rounding policy governance

**Justification:** Rounding affects pay fairness, compliance, and payroll cost.

**Improvement:** Model rounding intervals, direction, grace periods, jurisdiction/union scope, effective dates, and audit sampling. Simulate rounding changes before activation and flag biased outcomes.

### 16. Break deduction and compliance engine

**Justification:** Break rules vary by jurisdiction, role, shift length, minor status, union agreement, and meal/rest type.

**Improvement:** Add break rule evaluation for required breaks, paid/unpaid status, auto-deduction eligibility, waiver evidence, missed-break premium, and exception handling. UI should show why a deduction or premium was applied.

### 17. Overtime bucket specialization

**Justification:** Overtime can be daily, weekly, seventh-day, consecutive-day, holiday, union, project, or jurisdiction-specific.

**Improvement:** Model overtime buckets with eligibility, accumulation window, stacking rules, reset boundary, rate multiplier, earning code, and precedence. Calculation traces should show bucket consumption.

### 18. Premium and differential calculation

**Justification:** Shift differentials, hazard premiums, call-in pay, standby pay, travel time, and role premiums materially affect payroll.

**Improvement:** Add premium rules with trigger, multiplier/flat amount, earning code, stackability, approval, and jurisdiction. Time-entry lines should separate base hours from premium hours and amounts.

### 19. Holiday calendar governance

**Justification:** Holiday pay depends on region, site, employee group, observed dates, partial holidays, and eligibility.

**Improvement:** Add holiday calendars with jurisdiction/site scope, observed date, eligibility, premium behavior, blackout rules, and effective dates. Shift and time calculations should cite the holiday calendar version.

### 20. Absence entitlement engine

**Justification:** Absence eligibility requires balances, accrual rules, waiting periods, employee status, jurisdiction, and absence type.

**Improvement:** Model entitlements with accrual, carryover, caps, waiting period, negative balance policy, evidence requirements, and projection freshness. Absence recording should show entitlement impact before submission.

### 21. Absence request and approval workflow

**Justification:** Absences affect coverage, payroll, compliance, and employee experience.

**Improvement:** Add absence states, requested dates, partial days, reason/type, balance impact, required documents, coverage impact, approver, escalation, cancellation, and emitted `AbsenceRecorded` evidence.

### 22. Leave conflict and coverage analysis

**Justification:** Approving absences without coverage analysis can break site operations.

**Improvement:** Evaluate overlapping absences, shift coverage, skill/role gaps, labor demand forecast, holiday constraints, and fairness. Workbench should show operational impact before approval.

### 23. Labor summary generation

**Justification:** Payroll-ready summaries are the controlled handoff from time operations to payroll and costing.

**Improvement:** Generate summaries by employee, date, period, role, cost center, project, site, earning code, exception state, and approval status. Summaries should reject unresolved blocking exceptions.

### 24. Labor summary approval controls

**Justification:** Approving labor hours authorizes payroll and cost allocation, so approvals must be complete and auditable.

**Improvement:** Add approval workflow with approver authority, material change detection, exception clearance, segregation checks, batch approval evidence, rejection reasons, and emitted `LaborHoursApproved` events.

### 25. Payroll-ready hours proof

**Justification:** Payroll needs trusted proof without direct access to time-owned tables.

**Improvement:** Generate hours proofs with summary lines, approvals, policy hash, calculation trace hash, exception status, period, employee projection key, and redacted verification API. Preserve privacy and package boundary.

### 26. Labor cost allocation

**Justification:** Labor hours need allocation to cost centers, projects, manufacturing orders, warehouses, or jobs without sharing external tables.

**Improvement:** Allocate labor using owned distribution records plus declared project, manufacturing, warehouse, and finance projections. Store allocation rules, percentages, validation, stale projection warnings, and rejected allocation reasons.

### 27. Labor distribution audit

**Justification:** Cost allocations can be manipulated or drift from operational work actually performed.

**Improvement:** Add distribution audit comparing shifts, clock transfers, work assignments, project projections, supervisor approvals, and payroll summary lines. Flag unusual reallocations and late changes.

### 28. Employee projection freshness

**Justification:** Time decisions depend on personnel status, work eligibility, role, supervisor, and employment dates without owning employee master data.

**Improvement:** Track `EmployeeCreated` and related projection freshness, active status, employment dates, tenant/entity, employee group, and identity confidence. Block clocking or scheduling when projections are missing or stale beyond policy.

### 29. Role projection impact analysis

**Justification:** Role changes affect shift eligibility, premium rules, cost allocation, approvals, and payroll summaries.

**Improvement:** On `RoleChanged`, recompute affected open shifts, time entries, approval tasks, premium eligibility, and labor summaries. Workbench should show impacted records and required recalculations.

### 30. Approval workflow specialization

**Justification:** Different approvals are needed for overtime, exceptions, absence, corrections, schedule changes, and payroll-ready summaries.

**Improvement:** Define workflow templates with approver role, threshold, escalation, delegation, evidence required, SLA, and action permissions. Approval tasks should state what will be authorized.

### 31. Time correction governance

**Justification:** Manual edits to time are high-risk and must be transparent.

**Improvement:** Add correction requests with original values, proposed values, reason, employee acknowledgement where required, supervisor approval, recalculation effect, payroll impact, and immutable audit trace.

### 32. Labor policy screening

**Justification:** Time actions must comply with labor law, union agreements, company policy, privacy, and fatigue rules.

**Improvement:** Screen shift creation, assignment, swap, clock, absence, correction, calculation, approval, and summary handoff actions. Store policy version, attributes evaluated, decision, explanation, and override path.

### 33. Fatigue and burnout risk scoring

**Justification:** Long shifts, insufficient rest, excessive overtime, and absence patterns create safety and retention risk.

**Improvement:** Score fatigue using schedule density, overtime, night shifts, rest gaps, absence history, role/site risk, and forecast demand. Provide recommendations that respect privacy and avoid punitive automation.

### 34. Time fraud and anomaly detection

**Justification:** Fraud and data quality issues include buddy punching, impossible travel, repeated corrections, unusual clock patterns, and source anomalies.

**Improvement:** Detect anomalies with device trust, geofence, sequence, timing, correction history, peer patterns, and source route behavior. Route findings to review with non-accusatory explanations.

### 35. Stochastic labor exposure model

**Justification:** Labor exposure spans overtime cost, absence risk, coverage shortfall, payroll errors, compliance breaches, and fatigue.

**Improvement:** Model exposure distributions by site, role, period, employee group, forecast, and schedule. Provide mitigation actions and confidence rather than binary risk labels.

### 36. Labor MLOps governance

**Justification:** Models for demand, overtime, anomaly, fatigue, and scheduling affect pay, fairness, and working conditions.

**Improvement:** Add model registry, feature lineage, training windows, approval status, explainability, drift monitoring, fairness checks, rollback, and release evidence for all labor models.

### 37. AppGen-X event reliability cockpit

**Justification:** Time Labor relies on consumed employee/role events and emitted shift, clock, time-entry, absence, and approved-hours events.

**Improvement:** Add inbox/outbox/dead-letter panels for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream payroll effects. Warn when stale projections affect calculations.

### 38. Boundary proof for time ownership

**Justification:** Time Labor must integrate with personnel, payroll, project, manufacturing, warehouse, finance, and audit packages without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only time_labor-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct employee master, payroll run, ledger, warehouse, manufacturing, and project table access.

### 39. Multi-tenant and jurisdiction isolation

**Justification:** Time data is sensitive and labor rules vary by tenant, legal entity, region, union, and site.

**Improvement:** Enforce isolation in shifts, clock events, entries, absences, approvals, summaries, projections, UI filters, saved views, and agent previews. Rules should be scoped by tenant/entity/jurisdiction.

### 40. Time workbench coverage

**Justification:** Time administrators need every operational surface in UI, not hidden backend commands.

**Improvement:** Expand UI into schedule board, patterns, bids, swaps, demand forecasts, clock event queue, device health, geofence exceptions, time calculation trace, overtime review, premiums, holiday calendar, absence calendar, approval queue, labor summaries, cost allocation, policy screening, controls, rules, parameters, configuration, events, and agent panels.

### 41. Agent-safe time document intake

**Justification:** The time_labor chatbot should parse timesheets, absence notes, schedule requests, clock correction evidence, and labor instructions without unsafe writes.

**Improvement:** Add intake skills that extract candidate time facts, map them to owned tables, validate rules/permissions/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, confirmations, and expected AppGen-X events.

### 42. Agent-safe scheduling and correction planning

**Justification:** AI assistance around time can affect pay and compliance, so it must be bounded and reviewable.

**Improvement:** Require agent plans for shifts, swaps, clock corrections, absence records, recalculations, approvals, and summaries to list command, permission, owned tables, idempotency key, emitted event, payroll impact, rollback limits, and human approval.

### 43. Counterfactual overtime simulation

**Justification:** Managers need to understand overtime impact before publishing schedules or approving swaps and absences.

**Improvement:** Simulate schedule changes, swaps, demand adjustments, and absence approvals against overtime rules, premiums, coverage, fatigue, and labor cost. Show affected employees and pay impact.

### 44. Carbon-aware schedule windows

**Justification:** Some non-urgent labor activities and site operations can be scheduled to reduce energy or commuting impact.

**Improvement:** Add carbon schedule windows for optional work, batch approvals, training shifts, and non-urgent staffing moves using site and calendar metadata. Show cost, coverage, and fairness tradeoffs.

### 45. Device and offline replay resilience drills

**Justification:** Clock devices, mobile apps, and integrations fail, replay late, or duplicate events.

**Improvement:** Add drills for device outage, offline punch replay, duplicate punch, route failover, stale employee projection, retry exhaustion, and dead-letter recovery. Store drill evidence in release gates.

### 46. Crypto-agile time authorization

**Justification:** Payroll-ready proof, clock corrections, and approvals require durable authorization evidence.

**Improvement:** Add cryptographic epoch metadata, signed proof references, key rotation evidence, policy version, and migration readiness for future algorithms. Avoid binding business logic to one signature primitive.

### 47. Continuous time-control testing

**Justification:** Controls should run continuously across schedules, clocking, calculations, absences, approvals, summaries, and event handling.

**Improvement:** Add assertions for unassigned clock events, stale employee projections, geofence bypass, invalid sequence repair, unapproved overtime, unresolved exceptions in summaries, expired absence entitlement, unauthorized correction, dead-letter aging, and agent-preview bypass.

### 48. Payroll cutoff and close workflow

**Justification:** Period close requires all exceptions, approvals, corrections, absences, and summaries to be complete before payroll handoff.

**Improvement:** Add cutoff workflow with open exceptions, missing approvals, stale projections, recalculation needs, unapproved absences, summary readiness, late change detection, and handoff evidence.

### 49. Time Labor readiness score

**Justification:** Users need an evidence-backed view of whether the PBC is ready for production timekeeping and payroll handoff.

**Improvement:** Compute readiness from rules, parameters, clock devices, employee projections, schedule coverage, geofence policy, calculation traces, absence entitlement, approval workflows, event reliability, UI coverage, boundary proof, controls, model governance, and agent safety.

### 50. End-to-end payroll-ready hours proof

**Justification:** A complete Time Labor PBC must prove it can run the full lifecycle from shift plan to approved labor hours.

**Improvement:** Add an executable proof scenario covering employee projection, shift creation, clock events, exception handling, time-entry calculation, break/overtime/premium application, absence interaction, labor summary, approval, emitted `LaborHoursApproved`, hours proof, UI evidence, controls, and agent explanation.
