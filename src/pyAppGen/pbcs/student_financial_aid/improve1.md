# Student Financial Aid PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `student_financial_aid` with student-aid-specific improvements for aid applications, eligibility, award packaging, verification, disbursement, satisfactory academic progress, compliance, student communications, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `student_financial_aid`.
- Domain purpose: aid eligibility, awards, verification, disbursement, satisfactory progress, compliance, and student funding.
- Owned records include `aid_application`, `eligibility_review`, `award_package`, `verification_item`, `disbursement`, `sap_status`, `aid_compliance`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /aid-applications`, `POST /eligibility-reviews`, `POST /award-packages`, `POST /verification-items`, `POST /disbursements`, and `GET /student-financial-aid-workbench`.
- Workbench surfaces include `StudentFinancialAidWorkbench`, `StudentFinancialAidDetail`, and `StudentFinancialAidAssistantPanel`.
- AppGen-X events include `StudentFinancialAidCreated`, `StudentFinancialAidUpdated`, `StudentFinancialAidApproved`, and `StudentFinancialAidExceptionOpened`.

## 50 High-Impact Improvements

### 1. Aid application lifecycle state machine

**Justification:** Student aid applications move through draft, submitted, matched, verified, packaged, revised, cancelled, archived, and appeal states.

**Improvement:** Add explicit states for `aid_application` with transition reasons, required evidence, owner, allowed commands, and AppGen-X event emission.

**Acceptance evidence:** Tests must reject invalid transitions and show next allowed actions in `StudentFinancialAidWorkbench`.

### 2. Applicant identity and enrollment boundary

**Justification:** Aid eligibility depends on student identity, program, enrollment, residency, and dependency status without owning student lifecycle records.

**Improvement:** Store student, program, residency, enrollment, and dependency projections with freshness and source evidence from declared dependencies.

**Acceptance evidence:** Boundary tests must prove student records are projection inputs and no external student table is mutated.

### 3. Application year and period controls

**Justification:** Aid rules and award limits differ by academic year, term, payment period, census date, and enrollment intensity.

**Improvement:** Add year, term, payment period, census date, enrollment intensity, and rule-version evidence to each aid application and award.

**Acceptance evidence:** Tests must apply different rules by year and payment period.

### 4. Dependency and household review

**Justification:** Dependency status, household size, family members in college, and special circumstances affect aid calculations.

**Improvement:** Add dependency review records with household facts, source documents, override status, reviewer, and rationale.

**Acceptance evidence:** Tests must block packaging when required dependency evidence is incomplete.

### 5. Cost of attendance budget model

**Justification:** Award packaging requires tuition, fees, housing, food, books, transportation, personal, dependent care, and program-specific costs.

**Improvement:** Add budget components by student category, program, residency, housing status, enrollment intensity, and approved professional judgment adjustments.

**Acceptance evidence:** Tests must calculate cost budgets and preserve adjustment evidence.

### 6. Need and eligibility calculation trace

**Justification:** Students and auditors need to understand how need, resources, and eligibility were calculated.

**Improvement:** Expand `eligibility_review` with contribution inputs, budget, other resources, need, unmet need, aid limits, and calculation version.

**Acceptance evidence:** Tests must reconstruct eligibility calculations from owned records and projections.

### 7. Award packaging rules

**Justification:** Grants, scholarships, work-study, subsidized loans, unsubsidized loans, institutional funds, and private aid need ordered packaging logic.

**Improvement:** Add packaging rules with fund priority, eligibility conditions, annual limits, aggregate limits, unmet-need handling, and overaward prevention.

**Acceptance evidence:** Tests must produce deterministic packages and cite rule versions.

### 8. Fund source capacity tracking

**Justification:** Institutional and program funds can run out and require reservation, waitlist, or reallocation controls.

**Improvement:** Add fund capacity projections, reservation status, waitlist rules, release conditions, and allocation audit evidence.

**Acceptance evidence:** Tests must prevent awards that exceed available fund capacity.

### 9. Scholarship and external resource coordination

**Justification:** External scholarships and employer benefits can reduce need or require award revision.

**Improvement:** Store external resource projections, source, amount, term, restrictions, confirmation status, and award-impact calculation.

**Acceptance evidence:** Tests must revise award packages when confirmed resources create an overaward.

### 10. Verification selection and tracking

**Justification:** Selected students require specific documents, deadlines, corrections, and reviewer actions.

**Improvement:** Expand `verification_item` with selection reason, required document, status, due date, reviewer, discrepancy, and correction outcome.

**Acceptance evidence:** Tests must block disbursement while mandatory verification items remain unresolved.

### 11. Document intake and extraction

**Justification:** Tax records, identity documents, dependency forms, appeals, and statements arrive as documents.

**Improvement:** Add assistant-assisted extraction with source page, extracted fields, confidence, discrepancy flags, and reviewer approval.

**Acceptance evidence:** Tests must require confirmation before document-derived facts update aid records.

### 12. Conflicting information workflow

**Justification:** Offices must resolve conflicting income, identity, enrollment, citizenship, or academic facts before disbursing aid.

**Improvement:** Add conflict records with fact type, sources, severity, resolution owner, required correction, and closure evidence.

**Acceptance evidence:** Tests must block packaging or disbursement for unresolved high-severity conflicts.

### 13. Professional judgment decisions

**Justification:** Special circumstances can alter income, dependency, cost, or resource assumptions.

**Improvement:** Add professional judgment cases with request reason, documents, adjusted field, reviewer authority, approval, and audit note.

**Acceptance evidence:** Tests must preserve original and adjusted values with rationale.

### 14. Dependency override workflow

**Justification:** Dependency override decisions require careful evidence, approval, renewal handling, and student communication.

**Improvement:** Add override type, evidence checklist, reviewer, effective year, renewal requirement, denial reason, and notice.

**Acceptance evidence:** Tests must require elevated approval and generate decision evidence.

### 15. Satisfactory academic progress evaluation

**Justification:** Aid eligibility depends on GPA, pace, maximum timeframe, probation, appeal, and academic plan compliance.

**Improvement:** Expand `sap_status` with evaluation period, GPA result, pace result, timeframe result, appeal status, plan terms, and next review date.

**Acceptance evidence:** Tests must calculate pass, warning, probation, suspension, and plan-compliance outcomes.

### 16. Academic progress appeal handling

**Justification:** Students may appeal loss of aid due to academic progress issues.

**Improvement:** Add appeal records with reason, documentation, academic plan, committee decision, conditions, notice, and expiration.

**Acceptance evidence:** Tests must reinstate eligibility only after approved appeal or plan status.

### 17. Award acceptance and decline flow

**Justification:** Students may accept, reduce, decline, or later reinstate awards under specific rules.

**Improvement:** Add award response records with award line, response, amount, date, channel, counseling requirement, and revision impact.

**Acceptance evidence:** Tests must update award package state from student responses.

### 18. Loan counseling and promissory-note boundary

**Justification:** Loan disbursement may require counseling and signed promissory evidence from external systems.

**Improvement:** Store loan requirement projections with completion status, expiration, source, and freshness before disbursement release.

**Acceptance evidence:** Boundary tests must prove external loan requirement systems are not mutated.

### 19. Disbursement eligibility checklist

**Justification:** Disbursement must check enrollment, verification, academic progress, holds, acceptance, fund availability, and payment period.

**Improvement:** Expand `disbursement` with prerequisite checklist, blocker reasons, release date, amount, payment period, and approval evidence.

**Acceptance evidence:** Tests must block disbursement when any configured prerequisite fails.

### 20. Disbursement scheduling and split rules

**Justification:** Aid is often split by term, module, payment period, or late-start enrollment.

**Improvement:** Add schedule rules with split basis, earliest release date, census recalculation, late disbursement handling, and cancellation rules.

**Acceptance evidence:** Tests must calculate disbursement schedules for full-year, term-only, and late-start cases.

### 21. Return-of-funds calculation

**Justification:** Withdrawals or nonattendance can require returning funds based on attendance, aid earned, and disbursed amounts.

**Improvement:** Add return calculation records with withdrawal date, attendance projection, aid earned, unearned amount, institutional share, and student notification.

**Acceptance evidence:** Tests must calculate return amounts and create adjustment events.

### 22. Enrollment change recalculation

**Justification:** Dropping classes, adding modules, or changing program load can alter eligibility and disbursements.

**Improvement:** Consume enrollment-change events and add recalculation cases with affected awards, revised amounts, notices, and approval.

**Acceptance evidence:** Tests must revise awards after declared enrollment projection changes.

### 23. Overaward and overpayment resolution

**Justification:** Aid can exceed need, cost, annual limits, or eligibility after new information arrives.

**Improvement:** Add overaward cases with source, affected awards, adjustment plan, refund/repayment boundary, notice, and closure evidence.

**Acceptance evidence:** Tests must detect overawards and block further disbursement until resolved.

### 24. Compliance calendar

**Justification:** Aid operations must meet deadlines for verification, reporting, notices, reconciliation, and closeout.

**Improvement:** Add compliance obligations with due dates, owner, rule source, status, evidence, escalation, and exception handling.

**Acceptance evidence:** Tests must open exceptions for overdue obligations.

### 25. Program eligibility controls

**Justification:** Some programs, credentials, locations, or delivery modes may not be aid eligible.

**Improvement:** Store program eligibility projections with effective dates, credential status, modality, location, and restriction reason.

**Acceptance evidence:** Tests must reject aid packaging for ineligible program projections.

### 26. Citizenship and residency requirement workflow

**Justification:** Aid eligibility may require citizenship, residency, immigration, or domicile evidence.

**Improvement:** Add requirement checks with status projection, required documents, discrepancy reason, reviewer, and notice.

**Acceptance evidence:** Tests must block eligible status until required citizenship or residency evidence is resolved.

### 27. Consortium and study-abroad handling

**Justification:** Aid for consortium agreements and study abroad requires special cost, enrollment, and disbursement evidence.

**Improvement:** Add consortium records with host institution, credits, costs, agreement documents, attendance confirmation, and award adjustments.

**Acceptance evidence:** Tests must calculate packages using approved consortium cost and enrollment evidence.

### 28. Graduate, professional, and special-program packaging

**Justification:** Aid limits and fund types differ for undergraduate, graduate, professional, certificate, and non-degree students.

**Improvement:** Add student-level packaging profiles with eligible funds, limits, budget rules, and required checks.

**Acceptance evidence:** Tests must produce different packages by student level and program type.

### 29. Aggregate limit monitoring

**Justification:** Lifetime and annual limits prevent certain awards even when current-year need exists.

**Improvement:** Store aggregate usage projections with source, fund type, remaining eligibility, freshness, and override constraints.

**Acceptance evidence:** Tests must reject awards that exceed annual or aggregate limits.

### 30. Aid communications timeline

**Justification:** Students need clear communication about missing documents, awards, revisions, deadlines, and disbursements.

**Improvement:** Add communications with template, language, channel, trigger, delivery evidence, student response, and suppression reason.

**Acceptance evidence:** UI tests must show communication timeline and unresolved student actions.

### 31. Student portal action model

**Justification:** Students should see actionable tasks instead of office-only queues.

**Improvement:** Add portal tasks for documents, accept/decline awards, appeals, counseling, dependency review, and acknowledgements.

**Acceptance evidence:** Tests must expose portal-ready tasks without raw datastore access.

### 32. Advisor workbench queues

**Justification:** Financial aid staff need role-specific queues for verification, packaging, appeals, conflicts, disbursement blockers, and compliance.

**Improvement:** Add saved workbench queues with ownership, SLA, severity, student population, and next action.

**Acceptance evidence:** UI tests must show actionable queues with counts and drilldowns.

### 33. Award revision audit trail

**Justification:** Award changes can affect student decisions and compliance, so revisions need clear rationale.

**Improvement:** Add revision records with before/after award lines, reason, source event, reviewer, student notice, and effective date.

**Acceptance evidence:** Tests must reconstruct award history across revisions.

### 34. Fund reconciliation boundary

**Justification:** Aid offices need reconciliation with finance and student accounts but should not own ledger or receivable tables.

**Improvement:** Store finance and account projections for disbursed, posted, returned, and outstanding amounts with freshness.

**Acceptance evidence:** Boundary tests must show reconciliation uses projections and does not mutate finance tables.

### 35. Exception taxonomy

**Justification:** Application, eligibility, verification, award, disbursement, progress, and compliance exceptions need different owners.

**Improvement:** Add exception categories, severity, blocked action, owner, due date, escalation, closure evidence, and reopen reason.

**Acceptance evidence:** Tests must route exception types to correct workbench queues.

### 36. Aid rule and parameter workbench

**Justification:** Aid rules change by year, fund, program, student category, deadline, and institutional policy.

**Improvement:** Add governed editors for packaging priorities, verification deadlines, progress thresholds, disbursement blockers, and appeal rules.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 37. Agent-assisted student guidance

**Justification:** Students need understandable explanations of aid status, missing items, awards, and next steps.

**Improvement:** Add assistant skills that summarize status, explain blockers, draft student messages, and cite source evidence.

**Acceptance evidence:** Tests must verify assistant responses use current owned records and projections.

### 38. Agent-assisted document review

**Justification:** Staff handle high document volumes and need help triaging forms and discrepancies.

**Improvement:** Add assistant classification for document type, missing signatures, mismatched values, expiration, and required follow-up.

**Acceptance evidence:** Tests must require reviewer approval before accepted extraction mutates records.

### 39. Agent safety restrictions

**Justification:** AI must not silently approve aid, release disbursements, deny appeals, or alter award amounts.

**Improvement:** Require high-impact agent proposals to include command, affected records, financial impact, evidence, confidence, and approval role.

**Acceptance evidence:** Tests must block high-impact agent writes without explicit human approval.

### 40. Fraud and anomaly referral boundary

**Justification:** Suspicious identity, document, or pattern findings require referral but the aid PBC should not own investigation casework.

**Improvement:** Add anomaly flags, referral event payloads, hold status, source evidence, and resolution projection from declared dependencies.

**Acceptance evidence:** Boundary tests must show investigation outcomes arrive through declared events or APIs.

### 41. Equity and access analytics

**Justification:** Aid operations must monitor access, unmet need, verification burden, appeal outcomes, and disbursement delays across populations.

**Improvement:** Add analytics for unmet need, completion time, document burden, appeal approval, disbursement delay, and population segment.

**Acceptance evidence:** UI tests must expose metrics with drilldowns and privacy-safe aggregation.

### 42. Privacy and consent controls

**Justification:** Aid records contain sensitive financial, identity, family, and academic information.

**Improvement:** Add consent, authorized-party, redaction, role-based field visibility, and audit controls for student aid records.

**Acceptance evidence:** Permission tests must prevent unauthorized viewing of sensitive fields.

### 43. Point-in-time aid reconstruction

**Justification:** Appeals, audits, and disputes require knowing what the office knew at a specific time.

**Improvement:** Add event replay for application status, eligibility, verification, awards, disbursements, and progress status.

**Acceptance evidence:** Tests must reproduce historical snapshots from owned events.

### 44. Cryptographic aid evidence packet

**Justification:** Students, auditors, and sponsors may challenge award and disbursement decisions.

**Improvement:** Add hash-linked evidence packets for eligibility, award package, verification, disbursement, appeal, and return calculations.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 45. Predictive risk scoring

**Justification:** Staff should identify students at risk of missing deadlines, losing eligibility, or facing disbursement delays.

**Improvement:** Add risk scores with factors for missing items, progress status, enrollment changes, document age, and prior revisions.

**Acceptance evidence:** Tests must calculate scores and show factor explanations in the workbench.

### 46. Multi-campus and program isolation

**Justification:** Institutions may run separate campuses, calendars, programs, and fund rules under one composed app.

**Improvement:** Add campus and program scoping to applications, rules, budgets, funds, queues, permissions, and reports.

**Acceptance evidence:** Tests must prevent cross-campus data leakage and rule mixing.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic student aid workflows execute after composition.

**Improvement:** Add smoke scenarios for application intake, verification, packaging, appeal, disbursement, enrollment change, and return calculation.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for every scenario.

### 48. Cross-PBC boundary proof

**Justification:** Student aid touches student lifecycle, finance, documents, identity, compliance, and communications without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Sponsor and scholarship reporting

**Justification:** Sponsors require reports on awarded, accepted, disbursed, returned, and outstanding funds.

**Improvement:** Add reporting packages with sponsor projection, report period, included awards, adjustments, disbursements, certification, and delivery evidence.

**Acceptance evidence:** Tests must generate sponsor reports from owned records and projections.

### 50. Financial aid command center

**Justification:** Aid teams need one surface for student status, missing items, award package, disbursement blockers, appeals, compliance, and assistant support.

**Improvement:** Add command center with student summary, timeline, tasks, award view, blockers, communications, risk score, and assistant panel.

**Acceptance evidence:** UI tests must expose complete aid context and governed actions without raw datastore access.
