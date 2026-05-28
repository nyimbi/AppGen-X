# Mortgage Servicing PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `mortgage_servicing` with mortgage-servicing-specific improvements for loan boarding, payment processing, escrow, borrower communications, default management, loss mitigation, foreclosure controls, investor reporting, regulatory evidence, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `mortgage_servicing`.
- Domain purpose: mortgage accounts, escrow, payments, statements, loss mitigation, investor reporting, and foreclosure controls.
- Owned records include `mortgage_loan`, `escrow_account`, `payment_event`, `servicing_statement`, `loss_mitigation_case`, `investor_report`, `foreclosure_milestone`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /mortgage-loans`, `POST /escrow-accounts`, `POST /payment-events`, `POST /servicing-statements`, `POST /loss-mitigation-cases`, and `GET /mortgage-servicing-workbench`.
- Workbench surfaces include `MortgageServicingWorkbench`, `MortgageServicingDetail`, and `MortgageServicingAssistantPanel`.
- AppGen-X events include `MortgageServicingCreated`, `MortgageServicingUpdated`, `MortgageServicingApproved`, and `MortgageServicingExceptionOpened`.

## 50 High-Impact Improvements

### 1. Loan boarding data-quality gate

**Justification:** Servicing defects often begin when loans board with missing terms, wrong escrow flags, stale borrower data, or investor mismatches.

**Improvement:** Add boarding checks for note terms, payment due date, interest method, escrow status, investor projection, borrower projection, property projection, and exception reason.

**Acceptance evidence:** Tests must reject active servicing state until required boarding evidence is complete and visible in `MortgageServicingWorkbench`.

### 2. Servicing transfer reconciliation

**Justification:** Transfers from prior servicers require reconciling balances, suspense, escrow, payment history, delinquency, and open loss-mitigation activity.

**Improvement:** Add transfer-in records with prior-servicer trial balance, payment history, escrow ledger, open items, borrower notices, and reconciliation variance workflow.

**Acceptance evidence:** Tests must open exceptions for unresolved transfer variances and prevent first statement generation until approved.

### 3. Mortgage loan lifecycle state machine

**Justification:** Performing, delinquent, bankruptcy, loss mitigation, foreclosure, REO, paid off, transferred, and closed states drive different legal actions.

**Improvement:** Add explicit `mortgage_loan` states, allowed transitions, effective dates, reason codes, required approvals, and AppGen-X event emission.

**Acceptance evidence:** Invalid transition tests must fail and the workbench must show next allowed actions by loan state.

### 4. Payment application waterfall

**Justification:** Payments must apply correctly across principal, interest, escrow, fees, late charges, suspense, corporate advances, and unapplied funds.

**Improvement:** Expand `payment_event` with configurable application order, payment source, effective date, reversal link, component allocations, and reason evidence.

**Acceptance evidence:** Tests must calculate allocations for full, partial, late, extra-principal, and reversal scenarios.

### 5. Suspense handling controls

**Justification:** Partial payments and unidentified funds require controlled suspense handling instead of silent balance changes.

**Improvement:** Add suspense buckets with receipt source, matching status, borrower instruction, aging, release rule, and exception workflow.

**Acceptance evidence:** Tests must keep partial funds in suspense until release conditions are met and show aging in the workbench.

### 6. Late charge assessment rules

**Justification:** Late fees depend on grace period, payment receipt date, investor rules, jurisdiction, borrower protections, and waiver history.

**Improvement:** Add late-charge rules with grace days, fee calculation, waiver authority, cap, protected status, and audit evidence.

**Acceptance evidence:** Tests must assess, waive, and reverse late charges with cited rule versions.

### 7. Interest accrual and amortization schedule

**Justification:** Servicing requires accurate scheduled balances, interest accrual, curtailments, recasts, and maturity handling.

**Improvement:** Add amortization projections with scheduled principal, interest, unpaid principal balance, interest method, recast flag, and variance detection.

**Acceptance evidence:** Tests must reconstruct balances after normal payments, extra principal, missed payments, and rate changes.

### 8. Adjustable-rate mortgage change controls

**Justification:** Adjustable loans require index, margin, caps, floor, lookback, notices, effective dates, and payment recalculation evidence.

**Improvement:** Add ARM change records with index projection, rate calculation, cap test, payment change, notice schedule, and borrower-facing explanation.

**Acceptance evidence:** Tests must calculate rate changes and block changes without required notice evidence.

### 9. Escrow account lifecycle

**Justification:** Escrow accounts must track setup, analysis, shortage, surplus, disbursement, waiver, cancellation, and reinstatement states.

**Improvement:** Expand `escrow_account` with lifecycle status, tax/insurance lines, cushion parameters, analysis date, shortage option, surplus disposition, and waiver rules.

**Acceptance evidence:** Tests must produce valid escrow lifecycle transitions and reject disbursements on closed escrow accounts.

### 10. Escrow analysis engine

**Justification:** Escrow analysis needs projected disbursements, cushion limits, shortage/surplus, payment changes, and statement evidence.

**Improvement:** Add annual and short-year analysis calculations with line items, projected balance, minimum balance, borrower options, and approval.

**Acceptance evidence:** Tests must generate analysis outputs and borrower notices for shortage, surplus, and no-change cases.

### 11. Tax and insurance disbursement controls

**Justification:** Missed tax or insurance payments create borrower harm and operational losses.

**Improvement:** Add disbursement schedules, payee projection, due dates, invoice evidence, payment status, exception reason, and stop-payment handling.

**Acceptance evidence:** Tests must flag upcoming disbursements, block duplicate disbursements, and open overdue exceptions.

### 12. Force-placed insurance workflow

**Justification:** Lapsed hazard or flood coverage requires notices, evidence windows, placement decisions, and cancellation when borrower coverage arrives.

**Improvement:** Add coverage gap records, notice sequence, placement status, premium projection, borrower evidence review, and cancellation/refund workflow.

**Acceptance evidence:** Tests must enforce notice timing before placement and remove placement after valid coverage evidence.

### 13. Flood-zone monitoring boundary

**Justification:** Flood determinations affect escrow, insurance, and borrower notices but may come from external compliance services.

**Improvement:** Store flood-zone projections with determination date, map status, required coverage, appeal status, and freshness.

**Acceptance evidence:** Boundary tests must prove flood data is consumed as projection evidence and no external compliance table is mutated.

### 14. Servicing statement generation

**Justification:** Statements must present due amount, payment history, fees, escrow, delinquency, messages, and required disclosures.

**Improvement:** Expand `servicing_statement` with statement period, line items, message blocks, disclosure set, delivery method, suppression reason, and render evidence.

**Acceptance evidence:** Tests must generate statements for current, delinquent, escrow-change, and bankruptcy-suppressed cases.

### 15. Borrower notice schedule

**Justification:** Servicing events trigger notices for payment changes, delinquency, escrow, ARM changes, loss mitigation, and foreclosure milestones.

**Improvement:** Add notice requirements with trigger, deadline, template version, delivery channel, language, proof of delivery, and suppression rules.

**Acceptance evidence:** Tests must open exceptions for missed notices and show notice timeline in loan detail.

### 16. Communication preference and language controls

**Justification:** Borrowers may require specific language, accessibility format, authorized contact handling, or restricted communication windows.

**Improvement:** Store borrower communication projections, preferred channel, consent, language, accessibility requirement, and contact restriction status.

**Acceptance evidence:** Tests must select notices based on preferences and block unauthorized contact changes.

### 17. Delinquency aging buckets

**Justification:** Current, 30, 60, 90, rolling delinquency, and charge-off candidates need precise aging by contractual due date.

**Improvement:** Add delinquency calculations with due date, paid-through date, days delinquent, rolling status, cure amount, and trend.

**Acceptance evidence:** Tests must classify loans across aging buckets after missed, partial, and catch-up payments.

### 18. Collections contact strategy

**Justification:** Collection actions must respect borrower protections, contact limits, hardship, bankruptcy, and loss mitigation status.

**Improvement:** Add contact strategies with allowed action, suppression reason, next contact date, script version, outcome, and compliance evidence.

**Acceptance evidence:** Tests must prevent collection tasks when bankruptcy, cease-contact, or active loss mitigation rules apply.

### 19. Bankruptcy servicing controls

**Justification:** Bankruptcy affects notices, payments, fees, escrow, claims, and collection suppression.

**Improvement:** Add bankruptcy status projection, chapter, filing date, stay status, claim deadline, payment handling rule, and attorney contact controls.

**Acceptance evidence:** Tests must suppress prohibited communications and route payments according to bankruptcy status.

### 20. Military and protected-status controls

**Justification:** Protected borrowers may receive rate caps, foreclosure restrictions, fee limits, and notice protections.

**Improvement:** Add protected-status projections with effective dates, evidence source, applicable protections, and required approvals.

**Acceptance evidence:** Tests must block protected-status violations in fee, foreclosure, and collection workflows.

### 21. Loss mitigation intake

**Justification:** Borrower assistance requests require document checklists, hardship narratives, income evidence, and intake completeness.

**Improvement:** Expand `loss_mitigation_case` with application status, hardship reason, required documents, received documents, missing items, and review deadline.

**Acceptance evidence:** Tests must distinguish incomplete, complete, approved, denied, appealed, withdrawn, and expired applications.

### 22. Document-driven assistance package review

**Justification:** Pay stubs, tax returns, bank statements, hardship letters, and occupancy proof arrive as documents.

**Improvement:** Add agent-assisted document extraction with confidence, source page, field mapping, reviewer approval, and mutation preview.

**Acceptance evidence:** Tests must require human confirmation before document-derived fields update loss-mitigation records.

### 23. Workout option decisioning

**Justification:** Forbearance, repayment plan, deferral, modification, short sale, and deed-in-lieu have distinct eligibility and calculations.

**Improvement:** Add workout option evaluations with eligibility rules, waterfall order, investor constraint, trial requirement, payment impact, and decision rationale.

**Acceptance evidence:** Tests must produce eligible and ineligible outcomes with cited rule versions and borrower-facing reasons.

### 24. Trial payment plan tracking

**Justification:** Modifications often depend on timely trial payments before permanent terms are offered.

**Improvement:** Add trial plan records with due dates, required amounts, payment matching, missed-payment consequences, and completion evidence.

**Acceptance evidence:** Tests must mark trial plans successful or failed based on actual payment events.

### 25. Loan modification term generation

**Justification:** Approved modifications must produce precise new principal, rate, term, maturity, escrow, deferred balance, and effective date.

**Improvement:** Add modification term package with calculation trace, approval, borrower acceptance, document status, and boarding event.

**Acceptance evidence:** Tests must board new terms only after approval and signed-document evidence.

### 26. Foreclosure referral controls

**Justification:** Foreclosure referral must be blocked by notices, protected status, loss mitigation, bankruptcy, and investor requirements.

**Improvement:** Add referral checklist with prerequisite validations, approval authority, attorney projection, referral package, and hold reasons.

**Acceptance evidence:** Tests must block referral when any configured precondition is unmet.

### 27. Foreclosure milestone management

**Justification:** Foreclosure timelines require jurisdiction-specific milestones, deadlines, holds, hearings, sales, and cancellations.

**Improvement:** Expand `foreclosure_milestone` with milestone type, jurisdiction, due date, actual date, responsible party, hold, outcome, and evidence.

**Acceptance evidence:** Tests must calculate due milestones and open exceptions for missed or blocked milestones.

### 28. Foreclosure hold and restart governance

**Justification:** Holds for loss mitigation, bankruptcy, disaster, litigation, or protected status must prevent improper action.

**Improvement:** Add hold records with reason, effective date, blocked actions, owner, review date, release criteria, and restart evidence.

**Acceptance evidence:** Tests must prevent milestone completion during active holds and require release approval.

### 29. Payoff quote generation

**Justification:** Payoff quotes need principal, interest through date, fees, escrow, recording charges, wire instructions, and expiry.

**Improvement:** Add payoff quote records with good-through date, component lines, per diem, delivery evidence, and quote cancellation.

**Acceptance evidence:** Tests must generate payoff quotes and reject payoff posting against expired quotes.

### 30. Loan payoff and release tracking

**Justification:** Paid-off loans require funds validation, escrow disposition, lien release, document recording, and investor reporting.

**Improvement:** Add payoff completion workflow with received funds, balance zeroing, escrow refund, lien-release milestones, and closure event.

**Acceptance evidence:** Tests must prevent loan closure until payoff funds and release tasks are complete or waived.

### 31. Investor remittance reporting

**Justification:** Investors require scheduled principal, interest, curtailments, fees, delinquencies, advances, and exceptions.

**Improvement:** Expand `investor_report` with reporting period, investor projection, pool, remittance lines, certification, exception list, and submission evidence.

**Acceptance evidence:** Tests must reconcile payment events to investor report lines and flag unreconciled variances.

### 32. Advance tracking

**Justification:** Servicers advance taxes, insurance, principal, interest, legal fees, inspections, and property preservation costs.

**Improvement:** Add advance records with type, amount, recoverability, investor eligibility, reimbursement status, and write-off approval.

**Acceptance evidence:** Tests must show advance balances and block unsupported recovery claims.

### 33. Fee assessment and waiver governance

**Justification:** Fees must be permissible, disclosed, capped, and reversible when assessed incorrectly.

**Improvement:** Add fee records with type, trigger, rule version, amount, waiver authority, reversal reason, and borrower notice link.

**Acceptance evidence:** Tests must reject prohibited fees and preserve waiver/reversal audit evidence.

### 34. Property inspection and preservation boundary

**Justification:** Delinquent loans may require inspections, occupancy checks, winterization, repairs, or preservation tasks.

**Improvement:** Store property-service projections, inspection results, preservation recommendations, cost estimates, and completion status from declared dependencies.

**Acceptance evidence:** Boundary tests must prove property-service data is projected and no vendor table is mutated.

### 35. Disaster assistance workflow

**Justification:** Declared disasters can alter contact strategy, forbearance, inspections, fees, and foreclosure activity.

**Improvement:** Add disaster-zone projection, affected-property flag, borrower assistance request, relief option, suppression rules, and review dates.

**Acceptance evidence:** Tests must apply disaster-specific holds and relief options to affected loans.

### 36. Complaint and dispute linkage

**Justification:** Borrower disputes about payments, escrow, fees, credit reporting, or servicing transfers must influence operations.

**Improvement:** Add complaint/dispute projections with category, due date, related records, response status, and operational hold effects.

**Acceptance evidence:** Tests must surface active disputes on loan detail and block affected actions when configured.

### 37. Credit reporting furnishing controls

**Justification:** Payment status, delinquency, bankruptcy, disputes, and forbearance must be reported accurately.

**Improvement:** Add credit-reporting snapshot with reporting period, status code, suppression reason, dispute flag, and correction evidence.

**Acceptance evidence:** Tests must generate furnishing snapshots and suppress reporting when required.

### 38. Compliance rule and parameter workbench

**Justification:** Servicing rules change by investor, jurisdiction, product, borrower status, and regulatory deadline.

**Improvement:** Add workbench editors for late fees, notices, escrow cushions, loss-mitigation waterfalls, foreclosure preconditions, and contact limits.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 39. Exception taxonomy and queues

**Justification:** Boarding, escrow, payment, notice, loss-mitigation, foreclosure, investor, and compliance exceptions need distinct ownership.

**Improvement:** Add exception categories, severity, impacted action, owner queue, SLA, escalation, closure evidence, and reopen reason.

**Acceptance evidence:** Tests must route exception types to the correct workbench queues and emit exception events.

### 40. Borrower-facing account timeline

**Justification:** Borrower service teams need a clear timeline of payments, statements, notices, escrow, assistance, and milestones.

**Improvement:** Add a timeline projection that orders servicing events, documents, notices, exceptions, and decisions with source links.

**Acceptance evidence:** UI tests must show chronological timeline entries with filters by event type.

### 41. Agent-assisted payment research

**Justification:** Payment complaints often require comparing receipts, bank files, suspense, reversals, and application history.

**Improvement:** Add assistant skills that summarize payment history, identify likely misapplications, propose corrections, and require confirmation.

**Acceptance evidence:** Tests must reject unconfirmed agent corrections and retain source evidence for accepted adjustments.

### 42. Agent-assisted loss-mitigation checklist

**Justification:** Borrowers and specialists need help understanding missing documents, deadlines, and eligible workout paths.

**Improvement:** Add assistant prompts that parse borrower instructions, build checklist drafts, explain missing evidence, and generate governed case updates.

**Acceptance evidence:** Tests must show assistant output as a preview, not a committed mutation, until approved.

### 43. Agent safety and authority limits

**Justification:** AI must not silently assess fees, advance foreclosure, deny assistance, or alter borrower obligations.

**Improvement:** Require agent proposals to state command, affected records, rule checks, confidence, source evidence, approval role, and irreversible-impact flag.

**Acceptance evidence:** Tests must block high-impact agent commands without elevated human approval.

### 44. AppGen-X event specialization

**Justification:** Servicing composes with origination, payments, compliance, documents, investors, property services, and accounting through events.

**Improvement:** Define typed events for loan boarded, payment applied, escrow analyzed, notice sent, loss mitigation decisioned, foreclosure held, and investor report certified.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency use.

### 45. Point-in-time servicing reconstruction

**Justification:** Audits and disputes require reconstructing loan state as of a specific date.

**Improvement:** Add event-sourced reconstruction for balances, escrow, delinquency, notices, loss mitigation, and foreclosure status.

**Acceptance evidence:** Tests must replay owned events to reproduce historical snapshots.

### 46. Cryptographic servicing audit packet

**Justification:** Regulators, investors, and borrowers may challenge servicing decisions and need tamper-evident evidence.

**Improvement:** Add hash-linked packets for payment application, escrow analysis, loss-mitigation decision, foreclosure referral, and payoff closure.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 47. Operational risk scoring

**Justification:** Servicers need early warning for loans likely to create borrower harm, compliance breach, or investor loss.

**Improvement:** Add risk scores for escrow shortage, payment dispute, missed notice, delinquency roll, foreclosure breach, and investor-report variance.

**Acceptance evidence:** Tests must calculate risk factors and show score explanations in the workbench.

### 48. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic servicing workflows execute after composition.

**Improvement:** Add smoke scenarios for boarding, payment application, escrow analysis, statement generation, delinquency, loss mitigation, foreclosure hold, and payoff.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for each scenario.

### 49. Cross-PBC boundary proof

**Justification:** Mortgage servicing touches payment rails, documents, property, compliance, investors, accounting, and contact systems without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 50. End-to-end borrower assistance workbench

**Justification:** Specialists need one operational surface for hardship intake, document collection, option review, trial plans, notices, and closure.

**Improvement:** Add a loss-mitigation workspace with borrower timeline, checklist, eligibility results, payment history, next action, compliance clock, and assistant panel.

**Acceptance evidence:** UI tests must show complete case context and allow governed updates without raw datastore access.
