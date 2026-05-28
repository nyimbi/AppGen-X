# Healthcare Claims Adjudication PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `claims_adjudication_healthcare` with a hand-curated payer adjudication roadmap. The PBC owns healthcare claim intake, claim lines, coding validation, benefit rules, denials, appeals, payment integrity, adjudication evidence, governed rules, agent assistance, and release evidence without owning provider charge capture, member enrollment, or pharmacy benefit operations tables.

## Current Domain Evidence Used

- Stable PBC key: `claims_adjudication_healthcare`.
- Domain purpose: healthcare claim intake, coding validation, benefit rules, denials, appeals, payment integrity, and payer adjudication.
- Owned domain tables: `health_claim`, `claim_line`, `coding_review`, `benefit_rule`, `denial`, `appeal`, `payment_integrity_case`, `claims_adjudication_healthcare_policy_rule`, `claims_adjudication_healthcare_runtime_parameter`, `claims_adjudication_healthcare_schema_extension`, `claims_adjudication_healthcare_control_assertion`, `claims_adjudication_healthcare_governed_model`.
- Public APIs: `POST /health-claims`, `POST /claim-lines`, `POST /coding-reviews`, `POST /benefit-rules`, `POST /denials`, `GET /claims-adjudication-healthcare-workbench`.
- Emitted AppGen-X events: `ClaimsAdjudicationHealthcareCreated`, `ClaimsAdjudicationHealthcareUpdated`, `ClaimsAdjudicationHealthcareApproved`, `ClaimsAdjudicationHealthcareExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Claim Intake Canonicalization

**Justification:** Claims arrive from many channels with inconsistent member, provider, diagnosis, procedure, modifier, authorization, and attachment details.

**Improvement:** Add intake normalization for professional, institutional, dental, vision, encounter, paper-derived, and corrected claims with source format, submitter, batch, and canonical claim identity.

**Acceptance evidence:** Tests must parse representative intake payloads, reject malformed records with actionable reasons, and prevent duplicate claim creation on replay.

### 2. Claim Lifecycle State Machine

**Justification:** A healthcare claim is not simply approved or denied; it can suspend, pend, split, adjust, reverse, reopen, appeal, or recover.

**Improvement:** Add states for received, validated, pended, suspended, priced, adjudicated, paid, denied, partially denied, adjusted, reversed, appealed, recovered, and archived.

**Acceptance evidence:** Tests must reject invalid state transitions and preserve original claim outcomes after corrections or adjustments.

### 3. Claim Line Granularity

**Justification:** Adjudication decisions often happen at line level, not claim header level.

**Improvement:** Expand `claim_line` with service date, place of service, diagnosis pointers, procedure, modifier stack, units, charge, allowed amount, adjudication reason, and line-level payment state.

**Acceptance evidence:** Tests must adjudicate mixed paid, reduced, denied, bundled, and pended lines under a single claim.

### 4. Member Eligibility Projection Boundary

**Justification:** Claims depend on eligibility, coverage dates, plan, coordination of benefits, and accumulator state but should not own member enrollment tables.

**Improvement:** Represent eligibility as declared AppGen-X event/API projection evidence with freshness, plan version, source time, and fallback behavior.

**Acceptance evidence:** Boundary tests must fail on shared enrollment table reads and pass when eligibility is consumed through declared projections.

### 5. Provider Network and Credential Projection Boundary

**Justification:** Provider participation, taxonomy, license, facility, and contract status affect adjudication but may be owned by another PBC.

**Improvement:** Store only adjudication evidence for provider status, contract basis, network tier, and credential freshness.

**Acceptance evidence:** Tests must prove provider evidence is versioned and stale provider projections trigger pended claims or review.

### 6. Benefit Rule Versioning

**Justification:** Benefit rules change by plan, jurisdiction, effective date, service type, authorization, and member category.

**Improvement:** Add rule versions with eligibility context, covered service, exclusion, limitation, cost share, authorization requirement, effective window, and approval evidence.

**Acceptance evidence:** Tests must adjudicate historical and current claims against the correct rule version.

### 7. Medical Necessity Review

**Justification:** Some claims require clinical appropriateness evidence beyond plan coverage.

**Improvement:** Add medical necessity review cases with clinical basis, documentation required, reviewer qualification, determination, and appeal rights.

**Acceptance evidence:** Tests must pend claims for missing necessity evidence and resolve them with approved, denied, or partial outcomes.

### 8. Prior Authorization Matching

**Justification:** Claims can be incorrectly denied or paid if authorization matching is weak.

**Improvement:** Add authorization match evidence by member, provider, service, date, units, diagnosis, place of service, and authorization remaining balance.

**Acceptance evidence:** Tests must cover exact match, partial match, expired authorization, exhausted units, and no-match cases.

### 9. Coding Validation Engine

**Justification:** Invalid, incompatible, unbundled, or unsupported codes drive leakage and disputes.

**Improvement:** Add `coding_review` checks for diagnosis/procedure compatibility, modifier validity, age/sex edits, place-of-service mismatch, bundling, and documentation support.

**Acceptance evidence:** Tests must open coding review cases with line-level reasons and close them only after correction or override evidence.

### 10. Coordination of Benefits

**Justification:** Secondary payer logic and other coverage evidence materially change member responsibility and payer liability.

**Improvement:** Add COB status, primary payer evidence, allowed amount basis, paid amount from other payer, residual responsibility, and missing EOB review.

**Acceptance evidence:** Tests must adjudicate primary, secondary, missing-EOB, and corrected COB scenarios.

### 11. Deductible, Coinsurance, and Copay Application

**Justification:** Member cost sharing must be traceable to plan rules and accumulator evidence.

**Improvement:** Add line-level cost-share calculation with deductible, copay, coinsurance, out-of-pocket cap, excluded amount, and accumulator freshness.

**Acceptance evidence:** Tests must prove member responsibility is calculated with rule and accumulator version evidence.

### 12. Contract Pricing and Allowed Amount

**Justification:** Allowed amounts depend on contract, fee schedule, service site, provider status, and effective date.

**Improvement:** Add pricing basis, contract reference evidence, fee schedule version, negotiated rate, outlier rule, and manual price review state.

**Acceptance evidence:** Tests must price network, out-of-network, missing contract, and manually reviewed lines.

### 13. Claim Pend Reason Taxonomy

**Justification:** Generic pending statuses hide the work needed to resolve claims.

**Improvement:** Add pend reasons for missing eligibility, provider mismatch, missing authorization, coding issue, duplicate risk, attachment required, pricing review, and policy exception.

**Acceptance evidence:** Tests must route each pend type to the correct queue, owner role, SLA, and resolution action.

### 14. Denial Reason Governance

**Justification:** Denials must be precise, defensible, appealable, and tied to policy evidence.

**Improvement:** Add denial codes, clinical or benefit rationale, line mapping, notice text, appeal deadline, reviewer, and policy version.

**Acceptance evidence:** Tests must generate denial notices with line-specific reasons and reject denials missing policy evidence.

### 15. Appeal Lifecycle

**Justification:** Appeals require levels, deadlines, evidence packets, independent review, overturns, and final determinations.

**Improvement:** Add appeal levels, requester, evidence submitted, reviewer independence, deadline, decision, overturn reason, and reopened claim link.

**Acceptance evidence:** Tests must process appeal received, missing evidence, upheld, overturned, partially overturned, and external-review outcomes.

### 16. Duplicate Claim Detection

**Justification:** Duplicate billing can create overpayment or member confusion.

**Improvement:** Add duplicate scoring across member, provider, service dates, codes, units, charge, authorization, and source claim lineage.

**Acceptance evidence:** Tests must detect exact, near, corrected, and legitimate repeat-service cases without auto-denying ambiguous claims.

### 17. Payment Integrity Case Management

**Justification:** Payment integrity work includes prepay edits, postpay audits, recoveries, provider education, and disputes.

**Improvement:** Expand `payment_integrity_case` with trigger, suspected issue, dollar exposure, evidence, reviewer, action, recovery status, and dispute path.

**Acceptance evidence:** Tests must open prepay and postpay cases and prevent duplicate recoveries.

### 18. Fraud, Waste, and Abuse Signal Review

**Justification:** Claims patterns can indicate suspicious behavior but require governed review before adverse action.

**Improvement:** Add anomaly signals for upcoding, unbundling, excessive units, impossible services, provider outliers, and member/provider collusion indicators.

**Acceptance evidence:** Tests must create explainable investigation cases and require human review before denial or recovery actions.

### 19. Attachment and Medical Record Handling

**Justification:** Documentation drives medical necessity, coding support, and appeal decisions.

**Improvement:** Add attachment metadata, source, linked claim lines, extracted facts, missing pages, redaction profile, reviewer, and retention class.

**Acceptance evidence:** Tests must preserve attachment lineage and require reviewer confirmation for extracted facts.

### 20. Corrected and Replacement Claim Lineage

**Justification:** Corrected claims must replace or adjust prior claims without double-paying.

**Improvement:** Add original claim link, correction type, replaced lines, financial delta, submission reason, and replay-safe adjustment logic.

**Acceptance evidence:** Tests must process corrected claims and prove paid amounts are not duplicated.

### 21. Overpayment and Recovery Workflow

**Justification:** Postpay findings need recovery notices, offsets, repayment plans, disputes, and write-off policy.

**Improvement:** Add overpayment amount, reason, notice, offset status, repayment schedule, dispute, reversal, and closure evidence.

**Acceptance evidence:** Tests must create recoveries, apply offsets, handle disputes, and close with financial evidence.

### 22. Claim Adjustment and Reversal

**Justification:** Operational corrections require controlled adjustments and reversals.

**Improvement:** Add adjustment reason, initiator, affected lines, before/after amounts, member impact, provider notice, and authorization.

**Acceptance evidence:** Tests must reject unauthorized adjustments and preserve audit trails for changed amounts.

### 23. Benefit Limit Tracking

**Justification:** Visit, dollar, unit, and frequency limits require history and projection freshness.

**Improvement:** Add limit evaluation evidence with limit type, consumed amount, remaining amount, time window, and source freshness.

**Acceptance evidence:** Tests must adjudicate within-limit, exceeded-limit, and stale-limit cases.

### 24. Bundling and Unbundling Detection

**Justification:** Procedure bundling affects allowed amounts and payment integrity.

**Improvement:** Add bundling rule, primary line, bundled line, modifier exception, documentation requirement, and override reason.

**Acceptance evidence:** Tests must bundle lines, allow legitimate modifiers, and open review on questionable unbundling.

### 25. Inpatient and Episode Claim Logic

**Justification:** Facility claims can involve episodes, diagnosis related group logic, outliers, transfers, and readmissions.

**Improvement:** Add episode grouping, admission/discharge dates, stay classification, transfer flag, outlier basis, and facility review queue.

**Acceptance evidence:** Tests must adjudicate routine, transfer, outlier, and suspicious readmission scenarios.

### 26. Professional Claim Specialty Logic

**Justification:** Professional claims require provider specialty, place of service, modifier, supervision, and frequency controls.

**Improvement:** Add specialty-sensitive rules for evaluation services, procedures, telehealth, assistant roles, and same-day services.

**Acceptance evidence:** Tests must validate specialty restrictions and modifier-driven exceptions.

### 27. Member and Provider Notice Generation

**Justification:** Denials, adjustments, recoveries, appeals, and requests for information require clear notices.

**Improvement:** Add notice templates, recipient, channel, language, deadline, appeal rights, line references, and delivery proof.

**Acceptance evidence:** Tests must generate notices with accurate claim-line and policy references.

### 28. SLA and Timeliness Management

**Justification:** Claims and appeals have processing deadlines that vary by claim type and jurisdiction.

**Improvement:** Add SLA clocks, pause reasons, urgency, jurisdiction, service category, escalation, and late-case exception evidence.

**Acceptance evidence:** Tests must escalate near-deadline and overdue claims with correct timer behavior.

### 29. Adjudication Explainability Packet

**Justification:** Users need a transparent explanation of why each line paid, denied, reduced, or pended.

**Improvement:** Generate packets containing input facts, rule versions, projections, edits, pricing, cost-share, denial reasons, and reviewer actions.

**Acceptance evidence:** Tests must produce explanation packets for paid, denied, partially paid, and adjusted claims.

### 30. Rule Conflict and Impact Simulation

**Justification:** Benefit and edit changes can create contradictory outcomes or unintended claim disruption.

**Improvement:** Add side-effect-free simulation over sample claims, affected plan populations, financial impact, denial changes, and appeal risk.

**Acceptance evidence:** Tests must block activation of conflicted or unsimulated rule changes.

### 31. Claims Operations Workbench

**Justification:** Adjudicators need queues, aging, reasons, and next actions rather than generic record lists.

**Improvement:** Add views for intake rejects, pended claims, coding review, medical necessity, duplicate risk, denials, appeals, payment integrity, and SLA risk.

**Acceptance evidence:** UI tests must prove each queue maps to owned data and declared projections with permission-aware actions.

### 32. Agent-Assisted Claim Review

**Justification:** The agent can reduce review time by summarizing evidence and proposing next steps, but decisions need traceability.

**Improvement:** Add skills for claim summary, missing evidence request, denial draft, appeal packet summary, duplicate rationale, and payment integrity case notes.

**Acceptance evidence:** Tests must require cited evidence for every agent recommendation and confirmation before claim mutation.

### 33. Governed Agent CRUD Commands

**Justification:** Professional users need safe command previews for operational updates.

**Improvement:** Add command previews for pend claim, release claim, deny line, request attachment, open appeal, adjust claim, and open recovery case.

**Acceptance evidence:** Intent tests must reject ambiguous member or claim references and record source instruction, preview, approver, and command result.

### 34. Model Governance for Claim Intelligence

**Justification:** Coding suggestions, anomaly detection, and appeal prediction affect financial and member outcomes.

**Improvement:** Register governed models with intended use, version, evaluation evidence, bias checks, thresholds, drift, and human feedback.

**Acceptance evidence:** Tests must block model-backed recommendations when governance evidence is missing or expired.

### 35. Continuous Control Assertions

**Justification:** Claims adjudication must prove controls over timeliness, denial quality, duplicate payment, override use, and recovery leakage.

**Improvement:** Add control assertions with population, threshold, owner, frequency, failing sample, remediation, and closure evidence.

**Acceptance evidence:** Tests must open failures and prevent closure without remediation evidence.

### 36. Dead-Letter and Retry Queue

**Justification:** Claim events, attachments, rule updates, and payment events can fail and must be replayed safely.

**Improvement:** Add dead-letter classification, idempotency key, clinical or financial risk, retry count, replay checkpoint, and manual remediation.

**Acceptance evidence:** Tests must replay failed events without duplicate denials, payments, notices, or appeals.

### 37. Cross-PBC Dependency Freshness

**Justification:** Stale policy, audit, KPI, eligibility, provider, or authorization evidence can produce unsafe decisions.

**Improvement:** Add freshness indicators, blocking thresholds, degraded-mode policy, and override evidence for consumed projections.

**Acceptance evidence:** Tests must pend or block claims when required dependency evidence is stale.

### 38. Low-Value Care and Policy Analytics

**Justification:** Claims history can surface low-value care patterns while still preserving adjudication boundaries.

**Improvement:** Add analytics for avoidable services, repeated denials, high overturn rates, provider education targets, and policy leakage.

**Acceptance evidence:** Tests must produce tenant-scoped analytic projections with low-count suppression.

### 39. Provider Dispute Workflow

**Justification:** Providers may dispute denials, payments, recoveries, or coding decisions outside member appeals.

**Improvement:** Add dispute type, disputed lines, requested correction, evidence, reviewer, negotiation note, decision, and reopened claim link.

**Acceptance evidence:** Tests must process disputes without conflating provider dispute rights with member appeal rights.

### 40. Subrogation and Third-Party Liability

**Justification:** Accident, workers compensation, and liability cases can require recovery from third parties.

**Improvement:** Add liability indicator, accident date, third-party evidence, questionnaire status, recovery amount, and coordination state.

**Acceptance evidence:** Tests must pend, pay-and-pursue, recover, and close third-party liability scenarios.

### 41. Claim Audit Sampling

**Justification:** Quality programs need statistically and risk-based claim samples.

**Improvement:** Add sample frame, selection method, risk score, auditor assignment, findings, corrective action, and rework outcome.

**Acceptance evidence:** Tests must create random and risk-based samples with reproducible selection evidence.

### 42. Cryptographic Adjudication Proofs

**Justification:** Adjudication history needs tamper-evident proof for audit and disputes.

**Improvement:** Add hash-chained proof records for claim intake, line edits, pricing, denial, appeal, adjustment, and recovery events.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 43. Privacy and Minimum Necessary Views

**Justification:** Claim records contain sensitive clinical and financial data.

**Improvement:** Add role-specific redaction for adjudicator, clinical reviewer, appeal reviewer, auditor, provider portal, and member notice views.

**Acceptance evidence:** Permission tests must prove restricted diagnosis, attachment, and financial fields are hidden when not needed.

### 44. Correction of Erroneous Denials

**Justification:** Incorrect denials need rapid identification, correction, notice, payment, and root-cause analysis.

**Improvement:** Add denial quality monitoring, overturned-denial cohorting, systemic issue detection, corrective batch action, and notice generation.

**Acceptance evidence:** Tests must correct a cohort of erroneous denials without duplicate payments.

### 45. Seeded Adjudication Scenario Library

**Justification:** Release evidence needs realistic payer claim stories.

**Improvement:** Add seeds for clean claim, missing eligibility, authorization mismatch, coding denial, COB, duplicate, appeal overturn, overpayment recovery, and stale dependency.

**Acceptance evidence:** Scenario tests must load side-effect-free and produce expected queues, events, and explanation packets.

### 46. Financial Reconciliation Contract

**Justification:** Claim adjudication outputs need downstream payment and accounting reconciliation without owning those ledgers.

**Improvement:** Emit payable, adjustment, recovery, and member-responsibility events with traceable adjudication basis and idempotency keys.

**Acceptance evidence:** Contract tests must prove emitted events are complete and replay-safe.

### 47. Regulatory Reporting Extracts

**Justification:** Payers need defensible reporting for timeliness, denials, appeals, recoveries, and complaints.

**Improvement:** Add report projections with measure definitions, numerator, denominator, exclusion, source evidence, and submission status.

**Acceptance evidence:** Tests must generate report extracts with source links and suppression where required.

### 48. Full Claims Release Simulation

**Justification:** A complete PBC must prove adjudication from intake to final financial outcome.

**Improvement:** Add a simulation where a claim is received, validated, pended, reviewed, priced, partially denied, appealed, adjusted, paid, audited, and reported.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Boundary Proofs

**Justification:** Claims adjudication composes with provider, eligibility, finance, notification, and audit PBCs but must not share their tables.

**Improvement:** Add release gates that prove external inputs and outputs are declared API, event, projection, or package metadata contracts.

**Acceptance evidence:** Tests must fail on undeclared foreign table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose claims adjudication capabilities through DSL, UI, APIs, and the composed agent.

**Improvement:** Extend composition metadata for claims, lines, rules, coding reviews, denials, appeals, payment integrity, workbench fragments, parameters, controls, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include adjudication models, routes, services, event contracts, UI workbench artifacts, and assistant skills without stream-engine picker exposure.
