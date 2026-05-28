# Insurance Underwriting PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `insurance_underwriting` with a hand-curated underwriting roadmap. The PBC owns underwriting submissions, risk profiles, rating factors, quotes, underwriting decisions, bind packages, exclusions, governed rules, agent assistance, and release evidence without owning policy administration, claims, broker management, actuarial model ownership, or general ledger tables.

## Current Domain Evidence Used

- Stable PBC key: `insurance_underwriting`.
- Domain purpose: risk submissions, rating, quote generation, underwriting decisions, bind packages, exclusions, and referral workflows.
- Owned domain tables: `underwriting_submission`, `risk_profile`, `rating_factor`, `quote`, `underwriting_decision`, `bind_package`, `exclusion`, `insurance_underwriting_policy_rule`, `insurance_underwriting_runtime_parameter`, `insurance_underwriting_schema_extension`, `insurance_underwriting_control_assertion`, `insurance_underwriting_governed_model`.
- Public APIs: `POST /underwriting-submissions`, `POST /risk-profiles`, `POST /rating-factors`, `POST /quotes`, `POST /underwriting-decisions`, `GET /insurance-underwriting-workbench`.
- Emitted AppGen-X events: `InsuranceUnderwritingCreated`, `InsuranceUnderwritingUpdated`, `InsuranceUnderwritingApproved`, `InsuranceUnderwritingExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Submission Lifecycle State Machine

**Justification:** Underwriting submissions move through intake, triage, enrichment, review, referral, quote, decline, bind, lapse, and archive states.

**Improvement:** Add explicit states with transition reasons, owner, required evidence, allowed next actions, and AppGen-X event emission for each material step.

**Acceptance evidence:** Tests must reject invalid transitions and show the submission's next allowed actions in `InsuranceUnderwritingWorkbench`.

### 2. Submission Completeness Rules

**Justification:** Underwriting quality depends on complete applicant, exposure, coverage, prior loss, financial, location, and broker information.

**Improvement:** Add completeness profiles by product, jurisdiction, segment, risk class, and submission source, with missing-evidence queues.

**Acceptance evidence:** Tests must block quote generation when required submission facts or documents are absent.

### 3. Document Intake and Extraction

**Justification:** Applications, schedules, inspections, loss runs, financials, and supplemental forms arrive as documents.

**Improvement:** Add source document evidence, extracted fields, confidence, reviewer, accepted values, rejected values, and mutation preview.

**Acceptance evidence:** Tests must require reviewer approval for low-confidence or high-impact extracted facts.

### 4. Risk Profile Construction

**Justification:** Underwriters need a consolidated view of exposures, hazards, controls, prior losses, financial condition, and operations.

**Improvement:** Expand `risk_profile` with exposure units, class of business, hazard factors, controls, loss history projection, financial signals, and risk notes.

**Acceptance evidence:** Tests must construct risk profiles from owned data and declared projections without reading external policy or claims tables.

### 5. Risk Appetite Screening

**Justification:** Carriers need to reject, refer, or approve risks based on appetite rules before spending underwriting effort.

**Improvement:** Add appetite rules by product, geography, class, limit, hazard, prior loss, financial strength, and prohibited exposure.

**Acceptance evidence:** Tests must produce accept, refer, decline, and exception outcomes with cited appetite rule versions.

### 6. Referral Workflow

**Justification:** Complex risks require specialty, authority, legal, actuarial, or reinsurance referrals.

**Improvement:** Add referral type, reason, authority level, assignee, SLA, response, condition, and unresolved blocker state.

**Acceptance evidence:** Tests must prevent decision finalization while mandatory referrals remain open.

### 7. Underwriting Authority Matrix

**Justification:** Limits, premium, risk class, endorsements, and exceptions determine who can approve a decision.

**Improvement:** Add authority thresholds, delegated authority, escalation, conflict checks, and emergency override evidence.

**Acceptance evidence:** Permission tests must reject approvals by users without authority for the risk and quote profile.

### 8. Rating Factor Evidence

**Justification:** Quotes need traceable rating factors, not opaque premium numbers.

**Improvement:** Expand `rating_factor` with factor type, source, selected value, transformation, model version projection, override, and rationale.

**Acceptance evidence:** Tests must reconstruct quote premium from factor evidence and flag unsupported overrides.

### 9. Actuarial Model Boundary

**Justification:** Underwriting consumes rating models but should not own actuarial model governance.

**Improvement:** Store model projection, version, effective date, factor requirements, freshness, and result trace from declared actuarial APIs/events.

**Acceptance evidence:** Boundary tests must fail on actuarial table reads and pass on declared model projection usage.

### 10. Quote Lifecycle

**Justification:** Quotes can be draft, rated, referred, approved, issued, revised, expired, declined, or bound.

**Improvement:** Expand `quote` with version, premium, terms, conditions, subjectivities, validity, revision reason, and bind eligibility.

**Acceptance evidence:** Tests must preserve quote versions and block binding of expired or unapproved quotes.

### 11. Quote Comparison and Scenarioing

**Justification:** Underwriters compare deductibles, limits, exclusions, rates, and conditions before issuing terms.

**Improvement:** Add scenario records for alternate limits, deductibles, endorsements, exclusions, risk improvements, and pricing changes.

**Acceptance evidence:** Tests must compare scenarios side by side and keep scenario outputs separate from issued quotes.

### 12. Subjectivity Management

**Justification:** Bind may depend on inspections, signed forms, payment, engineering recommendations, or risk improvements.

**Improvement:** Add subjectivities with owner, due date, evidence requirement, waiver authority, status, and bind/issuance blocker behavior.

**Acceptance evidence:** Tests must block bind or policy event emission until required subjectivities are met or waived.

### 13. Exclusion Governance

**Justification:** Exclusions change coverage scope and must be precise, approved, and communicated.

**Improvement:** Expand `exclusion` with coverage, clause, reason, risk trigger, approval, effective wording version, and customer-facing explanation.

**Acceptance evidence:** Tests must attach exclusions to quotes and bind packages with required approvals.

### 14. Endorsement and Condition Handling

**Justification:** Underwriting decisions often use conditions and endorsements rather than simple accept/decline outputs.

**Improvement:** Add condition type, required action, wording reference, risk rationale, review date, and status.

**Acceptance evidence:** Tests must show condition effects in bind package and decision evidence.

### 15. Bind Package Assembly

**Justification:** Binding requires approved quote, terms, subjectivities, documents, payment projection, and authority.

**Improvement:** Expand `bind_package` with required checklist, quote reference, coverage terms, conditions, documents, approval, and policy handoff event.

**Acceptance evidence:** Tests must block bind package completion when any configured evidence is missing.

### 16. Declination Evidence

**Justification:** Declines need compliant reasons, appetite references, and audit evidence.

**Improvement:** Add decline reason, appetite/rule reference, underwriter note, communication template, appeal/reconsideration path, and retention.

**Acceptance evidence:** Tests must reject declines without a valid reason and generate scoped notice events.

### 17. Loss History Analysis

**Justification:** Prior losses affect pricing, terms, referral, and risk controls.

**Improvement:** Add loss history projection with frequency, severity, trend, large-loss marker, open claim marker, and credibility.

**Acceptance evidence:** Boundary tests must prove loss history comes from declared claims projections.

### 18. Exposure Accumulation

**Justification:** Property, marine, aviation, energy, and specialty risks can create concentration by geography, peril, or counterparty.

**Improvement:** Add accumulation checks by location, peril, limit, insured group, and portfolio bucket with threshold and override.

**Acceptance evidence:** Tests must refer or block risks that exceed accumulation thresholds.

### 19. Reinsurance Referral Boundary

**Justification:** Large or unusual risks may need facultative or treaty capacity evidence.

**Improvement:** Store reinsurance capacity projection, attachment, limit, retention, facultative status, and freshness from declared dependencies.

**Acceptance evidence:** Tests must block quote issuance when required capacity evidence is stale or missing.

### 20. Risk Engineering Recommendations

**Justification:** Inspections and risk engineering recommendations can change acceptance, terms, and pricing.

**Improvement:** Add recommendation records with hazard, required improvement, priority, due date, evidence, effect on terms, and closure.

**Acceptance evidence:** Tests must tie recommendations to subjectivities, conditions, or pricing adjustments.

### 21. Inspection Ordering and Results

**Justification:** Underwriters may need site inspections, surveys, or third-party reports.

**Improvement:** Add inspection request, scope, provider projection, due date, result, findings, and risk-profile updates.

**Acceptance evidence:** Tests must route overdue inspections and require review before applying extracted findings.

### 22. Compliance and Sanction Boundary

**Justification:** Underwriting must consider sanctions, prohibited business, licensing, and market conduct without owning compliance systems.

**Improvement:** Store compliance screening projections with result, reason, freshness, hold/release decision, and override evidence.

**Acceptance evidence:** Boundary tests must fail on direct compliance table reads and pass on declared projections.

### 23. Fraud and Misrepresentation Signals

**Justification:** Inconsistent application facts, prior cancellations, abnormal losses, and document issues may indicate misrepresentation.

**Improvement:** Add fraud signal candidates, evidence, severity, investigation referral, hold state, and decision impact.

**Acceptance evidence:** Tests must open referrals and prevent automated adverse decisions without human review.

### 24. Portfolio Appetite Feedback

**Justification:** Underwriting appetite changes based on portfolio performance, capacity, catastrophe exposure, and strategy.

**Improvement:** Add appetite feedback projections from portfolio metrics, capital constraints, loss ratio, and growth targets.

**Acceptance evidence:** Tests must show stale portfolio projections and block appetite-sensitive decisions when configured.

### 25. Pricing Override Controls

**Justification:** Premium overrides can create leakage or unfair treatment.

**Improvement:** Add override type, amount, reason, authority, comparison to indication, approval, and audit flag.

**Acceptance evidence:** Tests must reject unauthorized or excessive overrides.

### 26. Underwriting Decision Record

**Justification:** Decisions must be explainable across accept, decline, refer, quote, bind, condition, and exclusion outcomes.

**Improvement:** Expand `underwriting_decision` with decision type, factors, rules, referrals, authority, effective quote, and narrative.

**Acceptance evidence:** Tests must generate a complete decision packet for every final outcome.

### 27. Decision Appeal or Reconsideration

**Justification:** Brokers and applicants may submit new evidence after a decline or adverse term.

**Improvement:** Add reconsideration request, new evidence, prior decision, reviewer, outcome, and versioned decision link.

**Acceptance evidence:** Tests must preserve original decision and new decision lineage.

### 28. Underwriting Workbench

**Justification:** Underwriters need prioritized queues instead of raw submissions.

**Improvement:** Add views for incomplete submissions, referrals due, quotes expiring, subjectivities open, high-risk accounts, compliance holds, and bind-ready packages.

**Acceptance evidence:** UI tests must prove each queue maps to owned records or declared projections with permission-aware actions.

### 29. Agent-Assisted Risk Summary

**Justification:** The assistant can summarize complex submissions but must cite evidence and preserve underwriter accountability.

**Improvement:** Add skills for submission summary, risk-profile explanation, referral memo draft, quote comparison, subjectivity checklist, and decision narrative draft.

**Acceptance evidence:** Tests must require citations and human approval before decision or quote mutation.

### 30. Governed Agent CRUD Commands

**Justification:** Chat-driven underwriting changes need previews, authority checks, and audit trails.

**Improvement:** Add command previews for create submission, update risk factor, request referral, issue quote, add exclusion, waive subjectivity, and approve bind package.

**Acceptance evidence:** Intent tests must require submission identity, evidence, preview, confirmation, authority, and audit trail.

### 31. Document Wording Control

**Justification:** Quote, condition, exclusion, and bind wording must use approved versions.

**Improvement:** Add wording reference, version, jurisdiction, approval, effective window, and retired wording restrictions.

**Acceptance evidence:** Tests must block quote issuance with obsolete wording.

### 32. Multi-Jurisdiction Rules

**Justification:** Underwriting rules vary by state, country, admitted/non-admitted market, product, and license.

**Improvement:** Add jurisdictional rule dimensions for appetite, rating, documents, disclosures, taxes, and binding authority.

**Acceptance evidence:** Tests must evaluate identical risk facts differently by jurisdiction and policy version.

### 33. Producer and Channel Boundary

**Justification:** Broker or agent status affects submissions, but producer management may be owned elsewhere.

**Improvement:** Store channel and producer projections with appointment status, authority, commission profile, and freshness.

**Acceptance evidence:** Tests must block submissions from unauthorized or stale producer projections.

### 34. SLA and Workload Management

**Justification:** Quote turnaround and referral SLAs affect broker experience and revenue.

**Improvement:** Add SLA timers, priority, assignment rules, workload score, escalation, and late-case reason.

**Acceptance evidence:** Tests must escalate overdue submissions and show workload-balanced assignment suggestions.

### 35. Underwriting Quality Review

**Justification:** Files need audits for evidence completeness, authority compliance, wording, pricing, and decision rationale.

**Improvement:** Add quality review samples, findings, severity, remediation, reviewer, and recurrence tracking.

**Acceptance evidence:** Tests must open findings and block closure without remediation evidence.

### 36. Continuous Control Assertions

**Justification:** Underwriting governance needs controls over authority, pricing overrides, subjectivities, referrals, compliance holds, and bind packages.

**Improvement:** Add control assertions with population, threshold, failing records, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and require remediation proof.

### 37. Dead-Letter and Retry Operations

**Justification:** Document intake, rating responses, compliance projections, and bind events can fail.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed events without duplicate quotes, decisions, or bind events.

### 38. Cryptographic Underwriting Evidence

**Justification:** Market conduct reviews and disputes need tamper-evident underwriting files.

**Improvement:** Add hash chains for submissions, documents, risk profiles, quotes, referrals, decisions, exclusions, and bind packages.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 39. Model Governance for Underwriting Assistance

**Justification:** Risk scoring, anomaly detection, and agent summarization affect underwriting outcomes.

**Improvement:** Register governed models with intended use, data vintage, validation evidence, threshold, limitation, drift, and feedback.

**Acceptance evidence:** Tests must block model-backed recommendations when governance evidence is missing or expired.

### 40. Risk Appetite Change Simulation

**Justification:** Appetite changes can shift submission flow, declines, premium, and referral workload.

**Improvement:** Add side-effect-free simulations over recent and pipeline submissions for appetite, authority, and pricing changes.

**Acceptance evidence:** Tests must produce impact reports before high-impact rule activation.

### 41. Quote-to-Bind Conversion Analytics

**Justification:** Leaders need insight into conversion, reasons lost, pricing friction, and referral drag.

**Improvement:** Add analytics by product, channel, segment, appetite outcome, quote age, premium band, and subjectivity burden.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with source drilldowns.

### 42. Decline and Referral Analytics

**Justification:** High declines or referrals may indicate appetite mismatch, missing data, or portfolio issues.

**Improvement:** Add analytics for decline reason, referral reason, decision cycle time, overturn rate, and exception usage.

**Acceptance evidence:** Tests must trend reasons and open governance review when thresholds breach.

### 43. Carbon and Climate Risk Evidence

**Justification:** Some underwriting decisions need climate, catastrophe, occupancy, and sustainability risk evidence.

**Improvement:** Add climate risk projection, hazard exposure, mitigation evidence, carbon-sensitive factor, and underwriting impact.

**Acceptance evidence:** Tests must include climate evidence in applicable risk profiles without owning external climate datasets.

### 44. Privacy and Minimum Necessary Views

**Justification:** Underwriting files include sensitive personal, financial, medical, and business information.

**Improvement:** Add redaction profiles for underwriter, referral reviewer, compliance, broker portal, auditor, and analytics user.

**Acceptance evidence:** Permission tests must hide restricted fields and block unauthorized exports.

### 45. Seeded Underwriting Scenario Library

**Justification:** Release audits need realistic underwriting stories.

**Improvement:** Add seeds for clean submission, incomplete application, referral, compliance hold, pricing override, quote revision, subjectivity waiver, decline, and bind.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and evidence packets.

### 46. Role-Based Permission Model

**Justification:** Assistants, underwriters, senior underwriters, referral specialists, compliance, managers, and auditors need different authority.

**Improvement:** Add permissions for submission edit, risk-profile edit, quote issue, referral decision, decline, bind, waive condition, and approve override.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 47. Policy Administration Handoff

**Justification:** Bind decisions create policy work but policy administration owns policy records.

**Improvement:** Emit bind, quote accepted, decline, subjectivity satisfied, and coverage term events with idempotency keys and evidence references.

**Acceptance evidence:** Boundary tests must fail on policy table writes and pass on declared AppGen-X event contracts.

### 48. Full Underwriting Release Simulation

**Justification:** A complete PBC must prove submission-to-bind behavior end to end.

**Improvement:** Add a simulation where a submission is received, documents extracted, risk profiled, appetite screened, referred, quoted, conditioned, approved, and bound.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate policy administration, claims, actuarial pricing, producer management, compliance systems, or GL ownership.

**Improvement:** Add overlap checks and dependency contracts for actuarial models, compliance screening, producer status, claims history, payment status, and policy handoff.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose underwriting capabilities through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for submissions, risk profiles, factors, quotes, decisions, bind packages, exclusions, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include underwriting models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
