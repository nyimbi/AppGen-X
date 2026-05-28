# Compensation and Payroll Engine PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `payroll_engine`. The items are specific to gross-to-net payroll operations: calendars, pay periods, pay groups, legal entities, payroll runs, worker projections, pay profiles, bank instructions, approved labor-hour intake, earning calculations, overtime, gross components, taxes, deductions, garnishments, benefits, net pay, payment instructions, filings, corrections, retro adjustments, off-cycle payments, policy screening, payroll proofs, event reliability, UI workbenches, and agent-assisted payroll operations.

## Current Domain Evidence Used

- Domain purpose: payroll execution for worker payroll projections, labor-hour intake, payslips, deductions, benefits, payroll postings, filing preparation, event evidence, rules, parameters, configuration, UI fragments, and release validation.
- Owned boundary: payroll calendars, periods, pay groups, legal entities, runs, run workers, approvals, locks, worker projections, pay profiles, bank instructions, labor hours and lines, earning codes and calculations, overtime calculations, gross pay components, payslips and lines, tax withholding projections, deductions, deduction rules, arrears, garnishment orders, benefit allocations, benefit plans, employer contributions, net pay distributions, payment instructions, payment-batch projections, journal-request projections, tax wage-base projections, filings, filing lines, corrections, retro adjustments, off-cycle payments, exceptions, policy screening, audit traces, payroll proofs, federation projections, carbon batch windows, batch optimization, cash allocation, anomaly signals, risk models, cash forecasts, parsed instructions, seed data, schema extensions, controls, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: runtime configuration, parameters, rules, schema extensions, event handling, worker projections, payroll runs, labor-hour ingestion, payslip calculation, deduction application, benefit allocation, payroll posting, filing preparation, payment/filing routing, payroll proofs, policy screening, federation, identity verification, resilience drills, crypto rotation, carbon-aware batches, batch optimization, cash allocation, controls, governed models, workbench, and boundary verification.
- Existing events and dependencies: emits `PayrollPosted` and `PayrollFilingPrepared`; consumes `LaborHoursApproved` and `TaxCalculated`; integrates with personnel, time/labor, tax, treasury, ledger, and audit through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Payroll calendar governance

**Justification:** Payroll calendars determine cutoffs, pay dates, bank holidays, statutory deadlines, and run sequencing; errors can delay pay and filings.

**Improvement:** Model calendar versions with pay frequency, cutoff windows, pay dates, bank holidays, statutory dates, approval deadlines, time-zone rules, and retro/off-cycle policy. Run creation should cite the active calendar snapshot.

### 2. Payroll period lifecycle

**Justification:** Period state controls intake, calculation, approval, posting, filing, correction, and lock behavior.

**Improvement:** Add period states from open to intake-closed, calculated, approved, posted, filed, corrected, locked, and archived. Enforce allowed transitions with reason, actor, policy hash, and downstream handoff evidence.

### 3. Pay group eligibility engine

**Justification:** Workers must be paid in the right pay group based on legal entity, worker type, country, currency, schedule, and payroll policy.

**Improvement:** Add eligibility rules for pay frequency, worker class, country, legal entity, currency, labor source, banking readiness, and tax projection. Reject run rosters when worker/pay-group evidence conflicts.

### 4. Legal entity payroll controls

**Justification:** Payroll obligations are tied to legal entities, employer registrations, currencies, filing channels, and statutory rules.

**Improvement:** Store legal entity payroll registration, country, currency, statutory authority, filing channel, payment rail, bank funding source projection, and approval policy. Block runs when entity setup is incomplete.

### 5. Payroll run readiness gate

**Justification:** Payroll runs should not start until period, worker roster, labor hours, tax projections, rules, payment rails, and approvals are ready.

**Improvement:** Compute run readiness from calendar, period, pay group, legal entity, worker projections, approved labor hours, tax projection freshness, deduction/benefit setup, payment readiness, and open exceptions.

### 6. Payroll run lock and freeze controls

**Justification:** Late changes after calculation or approval can create inconsistent payslips, payments, journals, and filings.

**Improvement:** Add lock levels for calculation freeze, approval freeze, payment freeze, posting freeze, filing freeze, and archive lock. Require break-glass approvals with full delta evidence.

### 7. Worker projection freshness

**Justification:** Payroll depends on personnel facts without owning employee master data.

**Improvement:** Track worker projection source, employment status, legal entity, pay group, tax residency, currency, compensation basis, termination date, and freshness. Block payment for stale or conflicting projections.

### 8. Worker pay profile lifecycle

**Justification:** Pay profile changes directly affect gross pay, tax, benefits, deductions, and eligibility.

**Improvement:** Model pay profiles with effective dates, salary/hourly basis, rate, currency, FTE, worker type, pay group, tax profile reference, approval evidence, and retro impact. Changes should trigger recalculation analysis.

### 9. Bank instruction verification

**Justification:** Incorrect or fraudulent bank instructions cause payment failures and payroll fraud.

**Improvement:** Add bank instruction lifecycle with verification status, account mask, payment rail, country, effective date, source, approval, change cooling period, and high-risk change flags. Payment instructions should require verified banking.

### 10. Labor hours intake reconciliation

**Justification:** Payroll must trust approved labor hours while preserving the time_labor boundary.

**Improvement:** Ingest `LaborHoursApproved` with idempotency, period mapping, worker projection, earning-code mapping, exception status, approval proof, and stale event handling. Reconcile direct API labor pulls to consumed events.

### 11. Earning code catalog governance

**Justification:** Earning codes drive gross pay, taxes, benefits, journals, filings, and payslip presentation.

**Improvement:** Model earning codes with taxable status, pensionable/benefitable flags, jurisdiction, earning category, rate basis, GL/journal projection mapping, filing box mapping, and effective dates.

### 12. Gross pay calculation trace

**Justification:** Payroll users must explain every gross pay component from hours, salary, overtime, premiums, supplemental pay, and corrections.

**Improvement:** Store gross calculation trace with inputs, earning code, rate, hours/units, multiplier, source event, rule hash, rounding, currency, and component lineage. Recalculation should version prior outcomes.

### 13. Salary proration engine

**Justification:** Hires, terminations, leaves, job changes, unpaid absences, and partial periods require accurate proration.

**Improvement:** Add proration methods by calendar days, workdays, scheduled hours, FTE, jurisdiction, and policy. Show proration basis and affected payslip lines.

### 14. Overtime and premium payroll validation

**Justification:** Payroll must validate overtime and premium outcomes from time_labor before payment.

**Improvement:** Recheck overtime and premiums against payroll rules, approved labor proof, earning code mapping, caps, and jurisdiction. Flag discrepancies for correction rather than silently accepting them.

### 15. Tax withholding projection governance

**Justification:** Tax calculations are external projections but determine net pay, filings, and compliance.

**Improvement:** Track tax projection freshness, jurisdiction, wage base, taxable wages, withholding amounts, employee/employer tax split, source event, and recalculation trigger. Block posting when required tax projections are missing or stale.

### 16. Wage base accumulation

**Justification:** Statutory taxes and benefits depend on year-to-date wage bases, thresholds, and caps.

**Improvement:** Add wage base projections with period, jurisdiction, worker, earning type, taxable base, cap, prior amounts, and source. Payslip calculation should explain threshold crossing and cap application.

### 17. Deduction rule engine

**Justification:** Deductions vary by pre-tax/post-tax status, limits, priority, arrears, eligibility, and jurisdiction.

**Improvement:** Model deduction rules with priority, taxable treatment, percentage/fixed amount, limit, arrears behavior, net pay floor interaction, effective dates, and proof. Apply rules in deterministic order.

### 18. Garnishment priority and protection

**Justification:** Garnishments are legally sensitive and require priority, limits, protected earnings, and court/order evidence.

**Improvement:** Add garnishment order lifecycle with authority, case reference, priority, protected amount, cap, start/end, remittance target, arrears, and stop notice. Payslips should show legal withholding evidence.

### 19. Deduction arrears recovery

**Justification:** Missed deductions can accumulate and must be recovered without violating net pay floors or legal limits.

**Improvement:** Track arrears origin, balance, recovery rule, max recovery per period, priority, employee notification status, and write-off approval. Recalculate arrears after corrections and off-cycle payments.

### 20. Benefit allocation and contribution controls

**Justification:** Benefits affect employee deductions, employer contributions, taxes, and filings.

**Improvement:** Model benefit plans, eligibility, employee contribution, employer contribution, taxable benefit treatment, caps, enrollment source, and retro changes. Allocate benefit cost with evidence and effective dates.

### 21. Net pay floor enforcement

**Justification:** Payroll must prevent negative or below-threshold net pay unless legally and operationally authorized.

**Improvement:** Enforce net pay floors after taxes, deductions, garnishments, benefits, and arrears. Route violations to exception workflows with suggested recovery, off-cycle, or arrears options.

### 22. Net pay distribution controls

**Justification:** Net pay may be split across accounts, cards, checks, or payment rails with limits and verification needs.

**Improvement:** Add distribution rules with priority, amount/percentage, verified bank instruction, currency, payment rail, residual account, and failed-distribution handling. Validate totals before payment batch handoff.

### 23. Payment instruction readiness

**Justification:** Treasury can only process payroll when payment instructions are complete, approved, and reconciled to net pay.

**Improvement:** Generate payment instructions with worker, amount, currency, payment rail, bank reference, pay date, legal entity, batch grouping, approval status, and treasury projection handoff evidence.

### 24. Payroll cash forecast

**Justification:** Treasury needs cash visibility before payroll posting and payment release.

**Improvement:** Forecast cash by legal entity, currency, pay date, payment rail, tax remittance, benefits, garnishments, and off-cycle payments. Include confidence and delta from prior run.

### 25. Payroll run approval workflow

**Justification:** Payroll approval authorizes employee pay, statutory remittance, accounting, and filings.

**Improvement:** Add approvals with amount threshold, legal entity, exception status, segregation-of-duties checks, batch approval, rejection reasons, and post-approval change detection. Approval UI should show risk and materiality.

### 26. Payroll posting handoff

**Justification:** Posting must create treasury, ledger, tax, and audit handoff artifacts without touching their tables.

**Improvement:** Emit posting evidence with payment batch projection, journal request projection, tax wage base projection, audit trace, proof hash, and `PayrollPosted` idempotency key. Boundary checks should reject direct treasury/ledger/tax table writes.

### 27. Payslip generation and disclosure rules

**Justification:** Payslips are employee-facing legal artifacts requiring correct line presentation and privacy.

**Improvement:** Generate payslips with earnings, taxes, deductions, benefits, employer contributions, net pay, YTD where allowed, legal disclaimers, locale, currency, and redaction rules. Preserve immutable issued payslip snapshots.

### 28. Payroll filing preparation

**Justification:** Statutory filings require jurisdiction-specific lines, materiality, deadlines, channels, and evidence.

**Improvement:** Prepare filings with jurisdiction, filing channel, period, legal entity, line classification, materiality threshold, source payslips, tax projections, validation errors, and emitted `PayrollFilingPrepared`.

### 29. Filing line reconciliation

**Justification:** Filing totals must reconcile to payslips, taxes, wage bases, benefits, and corrections.

**Improvement:** Add reconciliation checks for filing lines versus payslip lines, tax projections, wage bases, legal entity totals, prior filings, and corrections. Flag out-of-balance filings before submission handoff.

### 30. Retroactive adjustment engine

**Justification:** Retro pay changes arise from late hours, pay rate changes, benefit corrections, tax updates, and policy changes.

**Improvement:** Add retro lookback, affected periods, prior values, new values, delta calculation, tax recalculation dependency, payslip adjustment lines, approval, and audit evidence. Simulate retro before applying it.

### 31. Off-cycle payment workflow

**Justification:** Off-cycle payments handle corrections, terminations, bonuses, missed pay, and emergency pay but increase risk.

**Improvement:** Add off-cycle types, eligibility, approval threshold, payment timing, tax treatment, bank readiness, cash impact, filing impact, and linkage to regular runs. Require explicit reason and evidence.

### 32. Payroll correction lifecycle

**Justification:** Corrections must preserve original pay, reason, delta, worker communication, and downstream effects.

**Improvement:** Add correction cases with issue source, impacted payslips, amount delta, tax/deduction/benefit impact, approval, employee notification, retro/off-cycle decision, and closure proof.

### 33. Payroll exception taxonomy

**Justification:** Generic payroll exceptions hide root causes and slow resolution.

**Improvement:** Define exceptions for missing worker projection, stale tax projection, invalid bank, negative net, deduction limit breach, missing labor hours, gross variance, approval gap, filing mismatch, payment failure, and journal handoff issue. Each should define owner, SLA, severity, and recovery action.

### 34. Payroll policy screening

**Justification:** Payroll actions must comply with jurisdiction, legal entity, worker status, pay group, deduction limits, benefit eligibility, and approval rules.

**Improvement:** Screen run creation, worker roster, calculation, deduction, benefit, posting, filing, correction, and off-cycle actions. Store policy version, attributes evaluated, decision, explanation, and override path.

### 35. Payroll anomaly detection

**Justification:** Unusual gross, net, tax, deduction, benefit, bank, or filing behavior can indicate errors or fraud.

**Improvement:** Detect anomalies by worker, pay group, legal entity, earning code, deduction, net variance, bank change, retro amount, off-cycle frequency, and filing deltas. Route to review with explainable reasons.

### 36. Stochastic payroll exposure model

**Justification:** Payroll risk spans cash shortfall, compliance errors, payment failure, filing penalties, fraud, and employee impact.

**Improvement:** Model exposure distributions by run, legal entity, country, currency, payment rail, exception type, and worker group. Provide mitigation options with confidence.

### 37. Payroll MLOps governance

**Justification:** Payroll risk, anomaly, cash, and exception models affect pay and compliance decisions.

**Improvement:** Add model registry, feature lineage, training windows, approval status, drift monitoring, explainability, fairness checks, rollback, and release evidence for all payroll models.

### 38. Zero-knowledge payroll proof

**Justification:** Auditors or workers may need proof of pay facts without exposing full payslip details.

**Improvement:** Generate redacted proofs for gross, taxes, deductions, net, filing inclusion, and approval status with hash, timestamp, and verification API. Support selective disclosure by purpose.

### 39. Immutable payroll audit trace

**Justification:** Payroll is financially and legally material and must be reconstructable.

**Improvement:** Hash-chain worker projections, labor intake, calculations, deductions, benefits, approvals, postings, filings, corrections, off-cycle payments, agent previews, and event handling. Support temporal reconstruction.

### 40. AppGen-X event reliability cockpit

**Justification:** Payroll depends on labor and tax events and emits posting and filing events that downstream systems rely on.

**Improvement:** Add inbox/outbox/dead-letter views for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream handoff status. Warn on stale consumed events.

### 41. Boundary proof for payroll ownership

**Justification:** Payroll must not bypass personnel, time, tax, treasury, ledger, benefits, banking, or audit packages through shared tables.

**Improvement:** Add static/runtime checks proving commands touch only payroll-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct worker master, time entry, tax, treasury, ledger, and bank table access.

### 42. Payroll workbench coverage

**Justification:** Payroll specialists need full operational UI, not hidden backend commands.

**Improvement:** Expand UI into calendar, periods, pay groups, legal entities, run console, roster, worker profile, labor intake, payslip review, deductions, garnishments, benefits, net distributions, payment readiness, filings, corrections, retro, off-cycle, exceptions, rules, parameters, configuration, event reliability, controls, and agent panels.

### 43. Agent-safe payroll instruction intake

**Justification:** The payroll_engine chatbot should parse payroll instructions, correction requests, deduction orders, filing notes, and pay profile changes without unsafe writes.

**Improvement:** Add intake skills that extract candidate payroll facts, map them to owned tables, validate rules/permissions/projections, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, payroll impact, and expected AppGen-X events.

### 44. Agent-safe gross-to-net planning

**Justification:** AI assistance in payroll can alter pay and statutory outcomes, so it needs strict confirmation gates.

**Improvement:** Require agent plans for run creation, calculation, deduction, benefit, correction, posting, filing, and off-cycle actions to list command, permission, owned tables, idempotency key, emitted event, affected workers, net impact, filing impact, rollback limits, and human approval.

### 45. Counterfactual pay-policy simulation

**Justification:** Payroll policy changes can materially alter gross, taxes, deductions, net pay, cash, and filings.

**Improvement:** Simulate parameter/rule changes such as overtime multiplier, supplemental rate, net floor, deduction cap, retro lookback, and approval threshold against historical/current runs before activation.

### 46. Cash allocation mechanism

**Justification:** Payroll cash constraints require principled allocation across wages, taxes, garnishments, benefits, and payment batches.

**Improvement:** Add cash allocation planning with legal priority, employee protection, statutory remittance, benefit obligations, payment rail constraints, and escalation. Do not execute constrained allocation without executive approval.

### 47. Carbon-aware payroll batch scheduling

**Justification:** Non-urgent payroll batch processing can be scheduled to reduce operational energy without affecting pay timeliness.

**Improvement:** Add carbon-aware windows for simulation, proof generation, report preparation, and non-urgent filings while preserving pay-date and statutory deadlines. Show tradeoffs and constraints.

### 48. Continuous payroll control testing

**Justification:** Payroll controls should run continuously across setup, calculations, approvals, payments, postings, filings, and events.

**Improvement:** Add assertions for missing worker projection, stale tax, negative net, deduction cap breach, unapproved run, payment mismatch, filing imbalance, direct foreign-table access, dead-letter aging, and agent-preview bypass.

### 49. Payroll readiness score

**Justification:** Users need an evidence-backed view of whether Payroll Engine is ready for production gross-to-net operations.

**Improvement:** Compute readiness from calendar setup, pay groups, legal entities, worker projections, labor intake, tax projections, earning/deduction/benefit rules, payment readiness, filing setup, controls, UI coverage, event reliability, boundary proof, model governance, and agent safety.

### 50. End-to-end payroll run proof

**Justification:** A complete Payroll Engine PBC must prove it can run the full lifecycle from approved hours to posting and filing preparation.

**Improvement:** Add an executable proof scenario covering worker projection, approved labor hours, payroll run, payslip calculation, taxes, deductions, benefits, net pay distribution, approval, posting, payment/journal/tax handoff evidence, filing preparation, emitted events, UI evidence, controls, and agent explanation.
