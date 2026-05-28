# Pharmacy Benefits Management PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `pharmacy_benefits_management` with a hand-curated pharmacy benefits roadmap. The PBC owns formulary, drug coverage rules, prior authorizations, pharmacy claims, rebate contracts, utilization review, pharmacy networks, medication affordability, governed configuration, agent assistance, and release evidence without owning prescribing, dispensing, or external payer adjudication tables.

## Current Domain Evidence Used

- Stable PBC key: `pharmacy_benefits_management`.
- Domain purpose: formulary, prior authorization, pharmacy network, claims, rebates, utilization controls, and medication affordability.
- Owned domain tables: `formulary`, `drug_coverage_rule`, `prior_authorization`, `pharmacy_claim`, `rebate_contract`, `utilization_review`, `pharmacy_network`, `pharmacy_benefits_management_policy_rule`, `pharmacy_benefits_management_runtime_parameter`, `pharmacy_benefits_management_schema_extension`, `pharmacy_benefits_management_control_assertion`, `pharmacy_benefits_management_governed_model`.
- Public APIs: `POST /formularys`, `POST /drug-coverage-rules`, `POST /prior-authorizations`, `POST /pharmacy-claims`, `POST /rebate-contracts`, `GET /pharmacy-benefits-management-workbench`.
- Emitted AppGen-X events: `PharmacyBenefitsManagementCreated`, `PharmacyBenefitsManagementUpdated`, `PharmacyBenefitsManagementApproved`, `PharmacyBenefitsManagementExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.

## 50 High-Impact Improvements

### 1. Formulary Version Lifecycle

**Justification:** Formularies change by plan, region, effective date, market segment, and therapeutic policy, so mutable lists cannot support real PBM operations.

**Improvement:** Add formulary version states for draft, modeled, approved, published, active, sunset, corrected, and archived with effective windows, approval evidence, and rollback links.

**Acceptance evidence:** Tests must prove version activation is date-bounded, historical claims evaluate against the correct version, and rollback preserves published evidence.

### 2. Therapeutic Class and Drug Identity Model

**Justification:** Coverage rules depend on therapeutic class, ingredient, dosage form, strength, route, package, brand status, specialty status, and biosimilar relationships.

**Improvement:** Expand `formulary` records with normalized drug identity, class hierarchy, reference product, interchangeable product, specialty flag, maintenance flag, and exclusion reason.

**Acceptance evidence:** Tests must classify covered, excluded, specialty, biosimilar, maintenance, and non-formulary drugs without relying on shared external drug tables.

### 3. Tiering and Cost-Share Rules

**Justification:** Members and pharmacies need precise tier, copay, coinsurance, deductible, max out-of-pocket, and exception rules.

**Improvement:** Add tier definitions, cost-share formula, accumulator interaction, network differential, days-supply limit, and patient affordability flags to `drug_coverage_rule`.

**Acceptance evidence:** Tests must calculate sample member cost exposure and show the rule version, tier, and affordability reason used.

### 4. Step Therapy Pathways

**Justification:** Step therapy requires ordered prerequisites, clinical exceptions, time windows, and documented failure reasons.

**Improvement:** Add pathway steps, prerequisite drug classes, trial duration, failure criteria, exception categories, bypass policy, and appeal trigger.

**Acceptance evidence:** Tests must approve, deny, bypass, and appeal step therapy cases with full evidence trace.

### 5. Prior Authorization Intake Completeness

**Justification:** Prior authorization delays often come from missing diagnosis, prescriber, medication history, labs, or clinical rationale.

**Improvement:** Add required field profiles by drug, indication, plan, and urgency, with incomplete submission queues and missing-evidence guidance.

**Acceptance evidence:** Tests must reject incomplete PA packets, identify missing fields, and allow urgent provisional review according to policy.

### 6. Prior Authorization Clinical Criteria Engine

**Justification:** PA decisions must be consistent, explainable, versioned, and reviewable.

**Improvement:** Add criteria sets with indication, age, diagnosis evidence, labs, contraindications, step history, specialist requirement, duration, renewal rules, and override authority.

**Acceptance evidence:** Criteria tests must show approval, denial, partial approval, renewal, and override outcomes with policy version and reason.

### 7. Expedited and Urgent Review SLA

**Justification:** Some medications require accelerated review to avoid patient harm.

**Improvement:** Add urgency classification, SLA timer, clinical risk, reviewer assignment, escalation route, and delayed-review exception.

**Acceptance evidence:** Tests must escalate expired urgent PA cases and show SLA status in the workbench.

### 8. PA Renewal and Continuity of Therapy

**Justification:** Members on stable therapy should not be disrupted by renewal mechanics or plan changes.

**Improvement:** Add renewal windows, continuity protections, grandfathering, transition fill eligibility, and evidence reuse rules.

**Acceptance evidence:** Tests must allow continuity fills, block improper denials, and cite the continuity policy.

### 9. Pharmacy Claim Edit Engine

**Justification:** Claims require real-time edits for eligibility, coverage, quantity, days supply, refill timing, network, prescriber, and safety rules.

**Improvement:** Add claim edit definitions, priority order, reject code, soft reject, hard reject, paid with warning, and override capture.

**Acceptance evidence:** Tests must process representative paid, rejected, reversed, adjusted, and overridden claim flows.

### 10. Quantity Limit Governance

**Justification:** Quantity limits must be clinically defensible and plan-specific.

**Improvement:** Add dose basis, max quantity, days supply, age/weight context, exception policy, and override expiration.

**Acceptance evidence:** Tests must prove limits evaluate by product and plan version and that overrides expire correctly.

### 11. Refill Too Soon and Adherence Logic

**Justification:** Refill edits can prevent waste but must not block legitimate therapy changes or emergency fills.

**Improvement:** Add refill threshold, vacation supply, lost medication, dose change, emergency fill, and adherence gap signals.

**Acceptance evidence:** Tests must distinguish early refill abuse, dose change, emergency override, and adherence risk.

### 12. Specialty Pharmacy Routing

**Justification:** Specialty drugs may require limited distribution, cold chain, training, monitoring, or designated pharmacy networks.

**Improvement:** Add specialty routing rules, network requirement, handling requirements, clinical monitoring checklist, and exception handling.

**Acceptance evidence:** Tests must route specialty claims and PA approvals to the correct network constraints and workbench queues.

### 13. Pharmacy Network Contract Modeling

**Justification:** Network participation affects coverage, cost, reimbursement, mail order, specialty access, and quality controls.

**Improvement:** Expand `pharmacy_network` with contract type, participation dates, preferred status, specialty capability, mail order flag, performance metrics, and dispute state.

**Acceptance evidence:** Tests must evaluate in-network, preferred, out-of-network, terminated, and specialty-network scenarios.

### 14. Rebate Contract Terms

**Justification:** Rebate value depends on formulary placement, utilization thresholds, exclusions, guarantees, and evidence.

**Improvement:** Expand `rebate_contract` with manufacturer, product scope, tier commitment, market basket, guarantee, utilization basis, exclusion rule, and settlement cadence.

**Acceptance evidence:** Tests must calculate eligible utilization and detect missing evidence before rebate accrual.

### 15. Rebate Accrual and True-Up Evidence

**Justification:** Rebate accruals must reconcile estimated and actual utilization while preserving auditability.

**Improvement:** Add accrual snapshots, true-up periods, variance reasons, dispute flags, settlement status, and supporting claim cohorts.

**Acceptance evidence:** Tests must produce accrual, adjustment, dispute, and settlement evidence without exposing raw unrelated tables.

### 16. Utilization Review Case Taxonomy

**Justification:** Utilization review includes safety, medical necessity, high cost, duplicate therapy, fraud concern, and policy exception cases.

**Improvement:** Add review type, trigger, clinical basis, assigned reviewer, requested evidence, determination, appeal path, and closure reason.

**Acceptance evidence:** Tests must open and resolve each review type with deadline and decision evidence.

### 17. Medication Safety Screening

**Justification:** PBM edits can identify duplicate therapy, high dose, age contraindication, pregnancy caution, and dangerous combinations.

**Improvement:** Add safety-screen projections from claims, PA evidence, and declared chart events with severity, rationale, and human review state.

**Acceptance evidence:** Tests must generate safety warnings and require clinical review for high-severity cases.

### 18. Opioid and Controlled Substance Controls

**Justification:** Controlled medications require specialized controls, lock-in programs, thresholds, prescriber review, and exception governance.

**Improvement:** Add controlled-drug flags, cumulative dose checks, prescriber/pharmacy lock-in, duplicate prescriber detection, and emergency override workflow.

**Acceptance evidence:** Tests must distinguish legitimate acute use, chronic threshold breach, lock-in violation, and emergency exception.

### 19. Member Affordability Assistance

**Justification:** Coverage approval is incomplete if the member cannot afford therapy.

**Improvement:** Add affordability flags, lower-cost alternatives, assistance eligibility, coupon conflict warnings, out-of-pocket risk, and outreach tasks.

**Acceptance evidence:** Tests must rank alternatives and open affordability tasks without changing prescribing records.

### 20. Biosimilar and Generic Substitution Policy

**Justification:** Substitution rules vary by product, jurisdiction, indication, prescriber instruction, and plan.

**Improvement:** Add substitution eligibility, non-substitution reason, interchangeable status, step priority, and member/prescriber notice requirement.

**Acceptance evidence:** Tests must evaluate allowed, blocked, notice-required, and exception cases.

### 21. Formulary Exception and Appeal Lifecycle

**Justification:** Members and prescribers need a governed path for non-formulary access and adverse decisions.

**Improvement:** Add exception request, denial reason, appeal level, evidence packet, reviewer independence, deadline, external review status, and final determination.

**Acceptance evidence:** Tests must process exception, appeal, overturn, uphold, and external review outcomes.

### 22. Clinical Criteria Document Ingestion

**Justification:** Medical policies, compendia updates, and plan documents drive benefit rules but arrive as complex documents.

**Improvement:** Add document extraction with source span, candidate rule, confidence, reviewer, effective date, and impact analysis.

**Acceptance evidence:** Tests must require review before extracted criteria become active and show all affected products and plans.

### 23. Plan Benefit Configuration Workbench

**Justification:** Operations users need controlled configuration, not hidden constants.

**Improvement:** Add workbench panels for formulary versions, PA criteria, edit rules, networks, rebate contracts, utilization thresholds, and approval workflows.

**Acceptance evidence:** UI tests must prove each configuration action validates, simulates, approves, activates, and audits changes.

### 24. Parameter Impact Simulation

**Justification:** Changing refill thresholds, tiering, criteria, or network rules can affect claims, cost, and patient access.

**Improvement:** Add side-effect-free simulations against sampled claims and PA cases with access, rejection, cost, and exception impact.

**Acceptance evidence:** Tests must produce impact reports and block activation when required simulation evidence is missing.

### 25. Pharmacy Claim Reversal and Adjustment

**Justification:** Claims can be reversed, corrected, resubmitted, or adjusted after payment.

**Improvement:** Add reversal reason, original claim link, adjusted claim link, timing rules, financial impact, and downstream event emission.

**Acceptance evidence:** Tests must preserve claim lineage and prevent duplicate financial impact on replay.

### 26. Real-Time Benefit Check Contract

**Justification:** Prescribers and members need coverage, alternatives, PA requirements, and cost expectations before dispensing.

**Improvement:** Add API projections for real-time benefit response, including covered status, tier, PA requirement, step requirement, alternatives, network constraints, and estimate confidence.

**Acceptance evidence:** Contract tests must return permission-safe, plan-versioned responses without mutating claim state.

### 27. Pharmacy Performance and Quality Metrics

**Justification:** Network quality affects adherence, access, error rates, and member experience.

**Improvement:** Add metrics for fill timeliness, reversal rate, reject rate, specialty turnaround, adherence support, complaint rate, and audit findings.

**Acceptance evidence:** Tests must calculate metrics from owned PBM evidence and show tenant-scoped network scorecards.

### 28. Fraud, Waste, and Abuse Signals

**Justification:** PBM operations must detect suspicious prescribing, dispensing, member behavior, and pharmacy patterns.

**Improvement:** Add anomaly signals for excessive controlled fills, improbable combinations, pharmacy switching, high reversal loops, and unusual rebate patterns.

**Acceptance evidence:** Tests must open investigation cases with explainable signals and avoid automatic adverse action without review.

### 29. Member Communication and Notice Rules

**Justification:** Denials, formulary changes, PA expirations, and alternatives require compliant, understandable notices.

**Improvement:** Add notice templates, required recipients, language, delivery channel, deadline, appeal rights, and proof of delivery.

**Acceptance evidence:** Tests must generate notices for denial, change, expiration, and appeal outcomes with source evidence.

### 30. Prescriber Collaboration Portal Contract

**Justification:** Prescribers need scoped access to submit evidence, see missing data, and respond to PA questions without internal table access.

**Improvement:** Add scoped API views for PA evidence submission, status, missing evidence, peer review request, and decision notice acknowledgement.

**Acceptance evidence:** Tests must prove scoped tokens cannot access unrelated member or rebate data.

### 31. Clinical Reviewer Assignment

**Justification:** PA and utilization reviews require qualified reviewers, workload balancing, independence, and escalation.

**Improvement:** Add reviewer specialty, license evidence, conflict flag, workload score, assignment history, and backup routing.

**Acceptance evidence:** Tests must assign cases by qualification and prevent conflicted reviewers from final decisions.

### 32. Benefit Rule Conflict Detection

**Justification:** Tier, PA, step, quantity, network, and exception rules can contradict each other.

**Improvement:** Add rule conflict analysis for duplicate active rules, impossible criteria, inconsistent effective dates, and contradictory outcomes.

**Acceptance evidence:** Tests must block conflicted publication and show the exact rules and plans involved.

### 33. Accumulator and Deductible Projection Boundary

**Justification:** PBM must use accumulator evidence but should not own the member financial ledger if another PBC owns it.

**Improvement:** Represent accumulator status as declared event/API projections with freshness and confidence, and store only PBM decision evidence.

**Acceptance evidence:** Boundary tests must fail on shared-table accumulator reads and pass on declared projection usage.

### 34. Drug Shortage and Supply Constraint Handling

**Justification:** Coverage and substitution decisions may need to react to shortages without losing auditability.

**Improvement:** Add shortage status, affected products, therapeutic alternatives, temporary exception rules, communication plan, and expiration.

**Acceptance evidence:** Tests must activate and expire shortage exceptions with member and prescriber notices.

### 35. Cross-Border and Jurisdictional Rule Support

**Justification:** Pharmacy rules vary by geography, plan type, product approval, and controlled substance law.

**Improvement:** Add jurisdiction dimension to coverage, PA, network, notice, controlled substance, and substitution rules.

**Acceptance evidence:** Tests must prove identical claim facts can evaluate differently by jurisdiction and policy version.

### 36. Dead-Letter and Retry Operations

**Justification:** Claim events, PA submissions, criteria updates, and network changes can fail and must be remediated safely.

**Improvement:** Add retry class, dead-letter reason, risk level, replay eligibility, remediation action, and idempotency key tracking.

**Acceptance evidence:** Tests must replay failed events without duplicate claims, notices, or rebate accruals.

### 37. Agent-Assisted PA Case Summaries

**Justification:** Reviewers need concise evidence summaries, but clinical conclusions require traceability.

**Improvement:** Add agent skills to summarize PA packets, missing evidence, criteria match, appeal basis, and reviewer questions with citations.

**Acceptance evidence:** Tests must prove unsupported summary claims are flagged and high-impact decisions require human confirmation.

### 38. Governed Agent CRUD for PBM Operations

**Justification:** The chatbot should help create rules, PA cases, claim adjustments, and notices without unsafe direct mutation.

**Improvement:** Add command previews for create coverage rule, draft PA decision, open utilization review, adjust claim, generate notice, and simulate formulary change.

**Acceptance evidence:** Intent tests must require entity, plan, version, action, evidence, and confirmation before mutation.

### 39. Rebate and Coverage Ethical Guardrails

**Justification:** Formulary and rebate decisions can create conflicts between economics and patient access.

**Improvement:** Add control assertions comparing rebate incentives, coverage restrictions, clinical alternatives, exception rates, and affordability impact.

**Acceptance evidence:** Tests must open governance exceptions when financial terms conflict with configured patient-access policies.

### 40. Member-Level Benefit Timeline

**Justification:** Users need to understand PA, claims, denials, appeals, notices, and affordability events in sequence.

**Improvement:** Build a timeline projection with event type, actor, source, linked entity, plan version, decision reason, and next action.

**Acceptance evidence:** Replay tests must reconstruct timelines idempotently and show redacted views by permission.

### 41. Pharmacy Audit Evidence Room

**Justification:** Network pharmacies, claims, PA decisions, and rebates require audit packets.

**Improvement:** Add evidence packets containing rule version, claim cohort, PA packet, communications, overrides, reviewer, and proof chain.

**Acceptance evidence:** Tests must generate packets for claim audit, PA audit, network audit, and rebate audit.

### 42. Cryptographic Benefit Decision Proofs

**Justification:** Sensitive benefit decisions need tamper-evident proof without exposing unnecessary member data.

**Improvement:** Add hash-chained decision records for coverage evaluation, PA determination, claim edit, rebate accrual, and notice generation.

**Acceptance evidence:** Tests must verify proof chains and fail on altered decision payloads.

### 43. Utilization and Trend Analytics

**Justification:** PBM leaders need visibility into utilization, rejection patterns, specialty spend, PA turnaround, adherence, and affordability.

**Improvement:** Add analytics projections for claims volume, reject reasons, PA SLA, exception rates, drug trend, network performance, and rebate variance.

**Acceptance evidence:** Tests must produce tenant-scoped metrics with low-count suppression and freshness indicators.

### 44. Policy Change Impact Analysis

**Justification:** New benefit policies can disrupt members, prescribers, pharmacies, and contracts.

**Improvement:** Add impact analysis for formulary removals, tier moves, PA additions, network changes, quantity changes, and notice obligations.

**Acceptance evidence:** Tests must identify affected members, claims, PA cases, pharmacies, and notices before activation.

### 45. Seeded PBM Scenario Library

**Justification:** Release audits need realistic PBM stories instead of isolated happy paths.

**Improvement:** Add seed scenarios for non-formulary request, urgent PA, step therapy appeal, specialty routing, claim reject, rebate true-up, shortage exception, and affordability outreach.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected workbench queues and AppGen-X events.

### 46. Workbench Persona Coverage

**Justification:** Benefit configurators, clinical reviewers, claim operators, network managers, rebate analysts, and compliance users need different surfaces.

**Improvement:** Add workbench views for formulary governance, PA queue, claim edits, utilization reviews, network health, rebate settlement, member access, and controls.

**Acceptance evidence:** UI contract tests must prove every core PBM capability is surfaced with permission-aware actions.

### 47. Governed Model Registry

**Justification:** PA summarization, anomaly detection, affordability recommendations, and rule extraction need model governance.

**Improvement:** Register governed models with intended use, version, evaluation evidence, confidence thresholds, drift checks, and human feedback.

**Acceptance evidence:** Tests must block agent/model use when approval is missing, stale, or below confidence policy.

### 48. Full PBM Release Simulation

**Justification:** A complete package needs end-to-end evidence across benefit configuration and runtime operations.

**Improvement:** Add a simulation where a formulary is published, a PA is submitted, criteria are evaluated, a claim processes, an appeal occurs, a rebate accrues, and notices are generated.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, idempotent handlers, UI queues, agent skills, permissions, and release evidence.

### 49. Package Boundary and Dependency Proofs

**Justification:** PBM composes with EHR, payer, finance, provider, and notification PBCs but must not share their tables.

**Improvement:** Add release gates that prove all external relationships use declared APIs, events, projections, or package metadata.

**Acceptance evidence:** Tests must fail on undeclared foreign table references and pass for AppGen-X event/API dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose PBM capabilities through DSL, workbench UI, and the single composed application agent.

**Improvement:** Extend composition metadata for formulary, coverage, PA, claims, rebate, network, utilization review, rules, parameters, UI fragments, and agent skills.

**Acceptance evidence:** DSL generation tests must prove composed apps include PBM-owned models, routes, services, workbench views, assistant skills, and AppGen-X event contracts without stream-engine picker exposure.
