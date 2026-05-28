# Construction Contracts and Commercials PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `construction_contracts_commercials` with a hand-curated construction commercial-controls roadmap. The PBC owns construction contracts, pay applications, retainage, variation orders, commercial claims, lien waivers, subcontract packages, commercial controls, governed rules, agent assistance, and release evidence without owning project scheduling, procurement sourcing, general ledger, or document storage source-of-truth tables.

## Current Domain Evidence Used

- Stable PBC key: `construction_contracts_commercials`.
- Domain purpose: construction contracts, pay applications, retainage, claims, variations, lien waivers, and commercial controls.
- Owned domain tables: `construction_contract`, `pay_application`, `retainage`, `variation_order`, `commercial_claim`, `lien_waiver`, `subcontract_package`, `construction_contracts_commercials_policy_rule`, `construction_contracts_commercials_runtime_parameter`, `construction_contracts_commercials_schema_extension`, `construction_contracts_commercials_control_assertion`, `construction_contracts_commercials_governed_model`.
- Public APIs: `POST /construction-contracts`, `POST /pay-applications`, `POST /retainages`, `POST /variation-orders`, `POST /commercial-claims`, `GET /construction-contracts-commercials-workbench`.
- Emitted AppGen-X events: `ConstructionContractsCommercialsCreated`, `ConstructionContractsCommercialsUpdated`, `ConstructionContractsCommercialsApproved`, `ConstructionContractsCommercialsExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Contract Commercial Lifecycle

**Justification:** Construction contracts move through tender, award, execution, variation, suspension, practical completion, final account, defects, and closeout states.

**Improvement:** Add contract lifecycle states with effective dates, responsible party, required evidence, allowed transitions, and closeout blockers.

**Acceptance evidence:** Tests must reject invalid transitions and show contract stage, blockers, and next commercial action in the workbench.

### 2. Contract Type and Pricing Basis

**Justification:** Lump-sum, unit-rate, cost-plus, guaranteed maximum, target-cost, framework, and reimbursable contracts have different controls.

**Improvement:** Expand `construction_contract` with pricing basis, measurement rules, pain/gain share, provisional sums, contingency, allowances, escalation, and risk allocation.

**Acceptance evidence:** Tests must evaluate pay applications and variations differently by contract type and pricing basis.

### 3. Scope and Schedule of Values

**Justification:** Payment certification depends on a controlled schedule of values and scope breakdown.

**Improvement:** Add schedule-of-values lines with work package, quantity, unit, original value, approved changes, previous certified, current claimed, stored materials, and remaining balance.

**Acceptance evidence:** Tests must block over-claiming and reconcile current certificate totals to line evidence.

### 4. Pay Application Intake

**Justification:** Pay applications often arrive as mixed documents with progress claims, materials, variations, deductions, and attachments.

**Improvement:** Add intake states for received, parsed, incomplete, under review, certified, disputed, rejected, revised, paid event emitted, and archived.

**Acceptance evidence:** Tests must parse structured and document-derived applications, identify missing attachments, and require certification before payment events.

### 5. Progress Measurement Evidence

**Justification:** Claimed progress should be supported by inspections, quantities, milestones, photographs, or engineer certificates.

**Improvement:** Add progress evidence references, measurement method, certifier, field verification status, variance reason, and disputed quantity.

**Acceptance evidence:** Tests must reject certification where required progress evidence is absent or inconsistent with claimed percentage.

### 6. Retainage Rules

**Justification:** Retainage can vary by contract, work package, jurisdiction, milestone, cap, and release event.

**Improvement:** Expand `retainage` with percentage, cap, withheld amount, release trigger, partial release, substitution bond, and final release blockers.

**Acceptance evidence:** Tests must calculate retainage and release it only when configured milestones and waiver requirements are met.

### 7. Advance Payment and Recovery

**Justification:** Advances and mobilization payments require guarantees, recovery schedules, and exposure controls.

**Improvement:** Add advance amount, guarantee evidence, recovery percentage, recovered-to-date, outstanding exposure, expiry, and default trigger.

**Acceptance evidence:** Tests must calculate recovery across pay applications and flag expired guarantees.

### 8. Variation Order Lifecycle

**Justification:** Changes need instruction, quotation, evaluation, approval, implementation, valuation, and incorporation into contract value.

**Improvement:** Expand `variation_order` with initiator, instruction source, cost/time impact, quote, negotiation, approval route, disputed status, and executed amount.

**Acceptance evidence:** Tests must prevent unapproved variations from increasing certified contract value.

### 9. Change Notice Timeliness

**Justification:** Construction contracts often require notice within strict time bars.

**Improvement:** Add notice date, event date, contractual deadline, waiver status, late reason, and entitlement risk scoring for variations and claims.

**Acceptance evidence:** Tests must classify timely, late, waived, and disputed notice scenarios.

### 10. Commercial Claim Register

**Justification:** Delay, disruption, acceleration, differing site condition, prolongation, and loss/expense claims need separate handling.

**Improvement:** Expand `commercial_claim` with claim type, causation event, notice evidence, quantum basis, time impact, entitlement assessment, status, and settlement.

**Acceptance evidence:** Tests must route claims through entitlement, substantiation, negotiation, determination, settlement, and rejection states.

### 11. Delay and Time Impact Boundary

**Justification:** Commercial claims depend on schedule analysis but should not own the project schedule.

**Improvement:** Store schedule impact projections, critical-path evidence, delay window, concurrent delay marker, and freshness from declared project-controls events.

**Acceptance evidence:** Boundary tests must fail on direct schedule table reads and pass on declared projection evidence.

### 12. Quantum Calculation

**Justification:** Claim valuation requires labor, equipment, material, overhead, markup, escalation, and disruption evidence.

**Improvement:** Add quantum lines with cost category, rate, quantity, source evidence, markup rule, disallowed amount, and negotiated amount.

**Acceptance evidence:** Tests must recalculate claimed, assessed, and settled values from line evidence.

### 13. Subcontract Package Lifecycle

**Justification:** Subcontracts require award, insurance, bonds, scope alignment, payment, variations, claims, and closeout controls.

**Improvement:** Expand `subcontract_package` with package scope, subcontractor projection, contract value, insurance/bond status, compliance holds, and closeout checklist.

**Acceptance evidence:** Tests must block subcontract pay certification when required commercial compliance evidence is missing.

### 14. Lien Waiver Governance

**Justification:** Lien waivers protect owners and contractors but vary by payment, jurisdiction, conditionality, and party.

**Improvement:** Expand `lien_waiver` with waiver type, covered amount, covered period, party, conditional/unconditional status, notarization, and release dependency.

**Acceptance evidence:** Tests must block configured payments until required valid waivers are present.

### 15. Bonds and Guarantees

**Justification:** Performance bonds, payment bonds, retention bonds, parent guarantees, and advance guarantees need expiry and value controls.

**Improvement:** Add guarantee records with type, issuer, value, expiry, beneficiary, linked obligation, renewal requirement, and call status.

**Acceptance evidence:** Tests must flag expiring or insufficient guarantees and block closeout when required guarantees are missing.

### 16. Insurance Compliance

**Justification:** Contracts require insurance evidence by coverage type, limit, deductible, expiry, and project-specific endorsement.

**Improvement:** Add insurance compliance projections, coverage requirements, certificate evidence, expiry warning, and noncompliance holds.

**Acceptance evidence:** Tests must open compliance exceptions and prevent payment release according to policy.

### 17. Backcharge and Contra-Charge

**Justification:** Contractors may recover costs for damage, rework, cleanup, or third-party impacts.

**Improvement:** Add backcharge case, responsible party, notice, cost evidence, response, offset link, and dispute state.

**Acceptance evidence:** Tests must apply approved backcharges to payment certification and preserve dispute evidence.

### 18. Liquidated Damages and Incentives

**Justification:** Delay damages, milestone bonuses, safety incentives, and performance deductions must be transparent.

**Improvement:** Add damage/incentive rules, trigger evidence, grace periods, cap, assessed amount, waiver, and approval route.

**Acceptance evidence:** Tests must calculate damages and incentives from milestone and contract evidence.

### 19. Provisional Sums and Allowances

**Justification:** Allowances and provisional sums need drawdown, conversion to variations, and remaining balance controls.

**Improvement:** Add allowance ledger with original value, committed amount, approved draw, remaining balance, and closeout disposition.

**Acceptance evidence:** Tests must prevent allowance overdraws and reconcile final account treatment.

### 20. Escalation and Price Adjustment

**Justification:** Material, labor, fuel, and index escalation clauses can materially change payment.

**Improvement:** Add escalation formula, index projection, base date, calculation period, cap/floor, assessed amount, and evidence references.

**Acceptance evidence:** Tests must calculate escalation and reject stale or missing index projections.

### 21. Tax and Withholding Boundary

**Justification:** Pay applications may require taxes and withholdings while tax engines own tax rules.

**Improvement:** Store tax projection, withholding status, exemption evidence, and freshness as declared dependencies tied to payment certification.

**Acceptance evidence:** Boundary tests must fail on tax table reads and pass on declared projection usage.

### 22. Payment Certificate Generation

**Justification:** Certified payment must reconcile contract value, previous payments, variations, retainage, deductions, tax, and net due.

**Improvement:** Add payment certificate records with calculation trace, certifier, approval, revision, and payable event reference.

**Acceptance evidence:** Tests must reconstruct net due and emit idempotent payment events after approval.

### 23. Final Account Workflow

**Justification:** Final account closes all variations, claims, retainage, bonds, waivers, and disputed amounts.

**Improvement:** Add final account checklist, agreed contract sum, outstanding matters, settlement terms, signoff, and release conditions.

**Acceptance evidence:** Tests must block contract closeout until final account prerequisites are resolved or formally reserved.

### 24. Dispute and Determination Tracking

**Justification:** Construction disputes can move through negotiation, determination, adjudication, arbitration, or settlement.

**Improvement:** Add dispute forum, disputed amount, issues, submissions, decisions, settlement terms, and financial impact.

**Acceptance evidence:** Tests must preserve dispute timeline and update claim/pay status based on determinations.

### 25. Commercial Correspondence Evidence

**Justification:** Notices, instructions, determinations, and acknowledgements often live in correspondence.

**Improvement:** Add evidence references with source document, sender, recipient, date, contract clause, extracted obligation, confidence, and reviewer.

**Acceptance evidence:** Tests must require reviewer confirmation before document-derived commercial mutations.

### 26. Contract Clause Obligation Register

**Justification:** Payment, notice, insurance, reporting, quality, and closeout obligations are clause-driven.

**Improvement:** Add obligation records with clause, responsible party, due date, trigger, status, evidence, and noncompliance consequence.

**Acceptance evidence:** Tests must open obligation tasks from contract terms and route overdue obligations to the workbench.

### 27. Commercial Risk Register

**Justification:** Commercial exposure accumulates through claims, variations, under-certified work, expiring guarantees, and disputed deductions.

**Improvement:** Add risk entries with exposure value, probability, driver, owner, mitigation, linked contract records, and trend.

**Acceptance evidence:** Tests must compute risk exposure and update it from claim and variation lifecycle changes.

### 28. Forecast Final Cost Boundary

**Justification:** Commercial controls need cost forecast evidence but should not own project cost-control ledgers.

**Improvement:** Store cost forecast projection, committed value, approved changes, pending changes, claims exposure, and confidence from declared project events.

**Acceptance evidence:** Boundary tests must fail on project-cost table reads and pass on declared AppGen-X projections.

### 29. Cash Flow Forecast

**Justification:** Pay applications and retainage releases affect cash planning.

**Improvement:** Add cash flow projections by contract, period, certified amount, expected payment date, retainage release, claim settlement, and confidence.

**Acceptance evidence:** Tests must generate cash flow forecasts without writing treasury or GL tables.

### 30. Contractor Performance Scorecard

**Justification:** Commercial outcomes depend on claim frequency, payment accuracy, waiver compliance, change discipline, and closeout quality.

**Improvement:** Add scorecards for variation cycle time, claim substantiation, pay-app rejection rate, compliance holds, dispute rate, and closeout aging.

**Acceptance evidence:** Tests must calculate scorecards from owned contract evidence.

### 31. Commercial Controls Workbench

**Justification:** Commercial managers need actionable queues, not raw contract lists.

**Improvement:** Add workbench views for pay apps awaiting certification, missing waivers, expiring guarantees, notice deadlines, disputed variations, claims, retainage release, and final account blockers.

**Acceptance evidence:** UI tests must prove each queue maps to owned records or declared projections with permission-aware actions.

### 32. Agent-Assisted Contract Review

**Justification:** The agent should summarize payment, claim, variation, and clause evidence but not create unsupported commercial decisions.

**Improvement:** Add skills for pay application summary, variation entitlement draft, claim evidence gap analysis, waiver checklist, final account blockers, and contract clause explanation.

**Acceptance evidence:** Tests must require citations and human approval before any commercial record mutation.

### 33. Governed Agent CRUD Commands

**Justification:** Chat-driven commercial operations must be previewed and approved.

**Improvement:** Add command previews for certify pay application, hold payment, create variation, open claim, release retainage, record waiver, and close final account item.

**Acceptance evidence:** Intent tests must require contract identity, evidence, preview, confirmation, authority, and audit trail.

### 34. Commercial Document Ingestion

**Justification:** Pay apps, lien waivers, notices, bonds, insurance certificates, and claims are document-heavy.

**Improvement:** Add extraction pipelines with source spans, extracted fields, confidence, reviewer, accepted fields, and rejected fields.

**Acceptance evidence:** Tests must block low-confidence or high-impact extracted changes until reviewed.

### 35. Change Impact Simulation

**Justification:** Commercial rule changes can affect payment timing, retained cash, claims exposure, and compliance holds.

**Improvement:** Add simulations for retainage rules, waiver requirements, certification thresholds, approval tiers, and notice deadlines.

**Acceptance evidence:** Tests must produce impact reports before high-risk configuration activation.

### 36. Continuous Control Assertions

**Justification:** Construction commercial governance needs controls over approvals, waivers, retainage, claims, variations, guarantees, and closeout.

**Improvement:** Add controls with population, threshold, failing records, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and require remediation evidence before closure.

### 37. Dead-Letter and Retry Operations

**Justification:** Contract events, document intake, payment events, and project projections can fail.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed events without duplicate pay certificates, variations, claims, or payment events.

### 38. Cryptographic Commercial Evidence

**Justification:** Disputes and audits need tamper-evident proof of notices, certifications, variations, claims, waivers, and final accounts.

**Improvement:** Add hash chains for contract, pay application, certificate, retainage, variation, claim, waiver, and closeout events.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 39. Role-Based Permission Model

**Justification:** Contract admins, quantity surveyors, commercial managers, project managers, finance users, legal users, and auditors need distinct authority.

**Improvement:** Add permissions for certify, approve variation, assess claim, release retainage, accept waiver, approve settlement, and close final account.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 40. Contractor Portal Contract

**Justification:** Contractors need scoped ways to submit pay apps, waivers, notices, and claims without internal table access.

**Improvement:** Add scoped API views for submissions, status, missing evidence, responses, and certified outcomes.

**Acceptance evidence:** Tests must prove portal scopes cannot access unrelated contracts or internal assessment notes.

### 41. Lien and Statutory Compliance Localization

**Justification:** Waiver, notice, withholding, and payment requirements vary by jurisdiction.

**Improvement:** Add jurisdiction-specific rules for lien waivers, prompt payment, statutory notices, retention limits, and dispute deadlines.

**Acceptance evidence:** Tests must evaluate identical payment facts differently by jurisdiction and policy version.

### 42. Commercial Claim Analytics

**Justification:** Recurring claim causes should drive project and contract improvements.

**Improvement:** Add analytics for claim type, root cause, entitlement success, substantiation quality, settlement ratio, cycle time, and prevented recurrence.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with drilldown to claim evidence.

### 43. Variation Trend Analytics

**Justification:** Change growth and approval lag indicate scope instability and commercial risk.

**Improvement:** Add analytics for variation source, value growth, cycle time, pending exposure, approved/unapproved ratio, and contract-value impact.

**Acceptance evidence:** Tests must calculate trend metrics and open risk tasks for threshold breaches.

### 44. Final Account Evidence Packet

**Justification:** Final account agreements need defensible proof of all payments, changes, claims, deductions, waivers, and releases.

**Improvement:** Add packet generation with contract summary, payment history, variations, claims, retainage, waivers, guarantees, disputes, and signoffs.

**Acceptance evidence:** Tests must generate scoped evidence packets with source links and redaction.

### 45. Financial Handoff Boundary

**Justification:** Commercial certification feeds payables and finance but should not write accounting entries.

**Improvement:** Emit payable, retainage, deduction, claim settlement, and final account events with idempotency keys and evidence references.

**Acceptance evidence:** Contract tests must prove finance handoff events are complete and replay-safe.

### 46. Sustainability and Local Content Clauses

**Justification:** Construction contracts increasingly include carbon, local content, labor, and social value obligations.

**Improvement:** Add clause obligations, measurement evidence, reporting cadence, noncompliance consequence, and commercial impact.

**Acceptance evidence:** Tests must track obligation compliance and connect failures to holds or claims where configured.

### 47. Seeded Commercial Scenario Library

**Justification:** Release audits need realistic construction commercial stories.

**Improvement:** Add seeds for pay application, retainage release, missing waiver, variation negotiation, delay claim, backcharge, expiring bond, and final account closeout.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and evidence packets.

### 48. Full Commercial Release Simulation

**Justification:** A complete PBC must prove contract-to-final-account behavior end to end.

**Improvement:** Add a simulation where a contract activates, pay applications certify, retainage withholds, variations approve, claims settle, waivers validate, and final account closes.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate project scheduling, cost management, procurement, finance, legal matter, or document storage ownership.

**Improvement:** Add overlap checks and dependency contracts for project status, schedule impact, cost forecasts, vendor identity, finance postings, legal disputes, and document references.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose construction commercial controls through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for contracts, pay applications, retainage, variations, claims, waivers, subcontract packages, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include commercial models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
