# Clinical Trials Management PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `clinical_trials_management` with a hand-curated clinical research operations roadmap. The PBC owns protocols, study sites, subjects, consent records, visit schedules, adverse event operations, monitoring, trial data operations, governed rules, agent assistance, and release evidence without owning EHR source-of-truth, sponsor finance, or external regulatory submission systems.

## Current Domain Evidence Used

- Stable PBC key: `clinical_trials_management`.
- Domain purpose: protocols, trial sites, subjects, consent, visits, adverse events, monitoring, and trial data operations.
- Owned domain tables: `trial_protocol`, `study_site`, `subject`, `consent_record`, `visit_schedule`, `adverse_event`, `monitoring_finding`, `clinical_trials_management_policy_rule`, `clinical_trials_management_runtime_parameter`, `clinical_trials_management_schema_extension`, `clinical_trials_management_control_assertion`, `clinical_trials_management_governed_model`.
- Public APIs: `POST /trial-protocols`, `POST /study-sites`, `POST /subjects`, `POST /consent-records`, `POST /visit-schedules`, `GET /clinical-trials-management-workbench`.
- Emitted AppGen-X events: `ClinicalTrialsManagementCreated`, `ClinicalTrialsManagementUpdated`, `ClinicalTrialsManagementApproved`, `ClinicalTrialsManagementExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.

## 50 High-Impact Improvements

### 1. Protocol Version Governance

**Justification:** Protocol amendments affect eligibility, consent, visits, assessments, safety reporting, and site activation.

**Improvement:** Add protocol version states for draft, approved, active, amended, superseded, paused, closed, and archived with amendment rationale, effective date, and impacted sites/subjects.

**Acceptance evidence:** Tests must prove historical subject visits retain the protocol version active at the time and amendments create impact worklists.

### 2. Eligibility Criteria Engine

**Justification:** Subject enrollment depends on inclusion, exclusion, washout, laboratory, prior therapy, demographic, and disease criteria.

**Improvement:** Add criteria definitions with required evidence, source, threshold, exception policy, reviewer, and eligibility decision trace.

**Acceptance evidence:** Tests must approve, screen-fail, and require review for subjects with complete, missing, and conflicting eligibility evidence.

### 3. Screening and Enrollment Lifecycle

**Justification:** Subjects move through prescreening, consent, screening, randomization, treatment, follow-up, withdrawal, and completion.

**Improvement:** Expand `subject` states with screen-fail reason, randomization status, cohort, arm, stratification factors, withdrawal reason, and end-of-study status.

**Acceptance evidence:** Tests must reject enrollment without valid consent and eligibility evidence and preserve screen-fail audit history.

### 4. Informed Consent Version Control

**Justification:** Consent must match protocol version, site language, subject capacity, and re-consent requirements.

**Improvement:** Add consent form version, language, signer role, capacity assessment, witness, re-consent trigger, withdrawal, and source document evidence.

**Acceptance evidence:** Tests must block study procedures when consent is missing, expired, withdrawn, or mismatched to protocol version.

### 5. Site Activation Checklist

**Justification:** Study sites cannot enroll safely until contracts, approvals, training, staff delegation, supplies, and systems are ready.

**Improvement:** Expand `study_site` with activation checklist, investigator qualification, delegation log, ethics approval, contract status, training completion, and activation date.

**Acceptance evidence:** Tests must block site activation and subject enrollment when required checklist evidence is missing.

### 6. Delegation of Authority

**Justification:** Trial tasks must be performed by authorized, trained staff with dates and role scope.

**Improvement:** Add delegation records for investigator, coordinator, pharmacist, lab staff, monitor, and data manager with task scope, training, start/end dates, and revocation.

**Acceptance evidence:** Permission tests must reject visit completion, consent, or adverse event review by unauthorized staff.

### 7. Visit Schedule Windowing

**Justification:** Trial visits have target dates, windows, assessments, missed-visit handling, and protocol deviations.

**Improvement:** Expand `visit_schedule` with visit type, target day, allowed window, required procedures, status, missed reason, reschedule reason, and deviation link.

**Acceptance evidence:** Tests must classify on-window, early, late, missed, skipped, and rescheduled visits with deviation evidence.

### 8. Assessment and Procedure Checklist

**Justification:** Each visit must complete protocol-required assessments, labs, questionnaires, dosing, and source documentation.

**Improvement:** Add visit procedure checklist with required/optional flag, performer, completion state, source evidence, result dependency, and missing item reason.

**Acceptance evidence:** Tests must prevent visit closure until required procedures are complete or waived with approved reason.

### 9. Randomization and Blinding Controls

**Justification:** Randomization integrity and blinding are core trial controls.

**Improvement:** Add randomization event evidence, arm assignment, stratification factors, blinded role restrictions, emergency unblinding reason, and unblinding audit.

**Acceptance evidence:** Tests must hide arm data from blinded roles and audit emergency unblinding.

### 10. Investigational Product Accountability

**Justification:** Product dispensing, returns, temperature excursions, and accountability records must reconcile.

**Improvement:** Add product lot, kit, dispensing record, return/destruction, temperature excursion, reconciliation variance, and pharmacist signoff.

**Acceptance evidence:** Tests must detect missing kits, over-dispensing, unreturned product, and unresolved reconciliation variance.

### 11. Adverse Event Intake

**Justification:** Adverse events require severity, seriousness, causality, expectedness, action taken, outcome, and reporting clocks.

**Improvement:** Expand `adverse_event` with onset, resolution, grade, seriousness, relatedness, expectedness, treatment action, outcome, reporter, and source evidence.

**Acceptance evidence:** Tests must classify non-serious and serious events and open reporting deadlines based on seriousness and expectedness.

### 12. Serious Event Reporting

**Justification:** Serious events can trigger urgent sponsor, ethics, and regulatory reporting.

**Improvement:** Add reporting obligations, initial report deadline, follow-up report, recipient, submission proof, narrative, and unresolved query state.

**Acceptance evidence:** Tests must escalate overdue serious event reporting and preserve submission evidence.

### 13. Protocol Deviation Management

**Justification:** Deviations affect subject safety, data integrity, and study credibility.

**Improvement:** Add deviation type, severity, preventability, impacted subject/visit/site, root cause, corrective action, and sponsor notification requirement.

**Acceptance evidence:** Tests must open deviations from missed visits, invalid consent, unauthorized staff action, and late safety reporting.

### 14. Monitoring Visit Planning

**Justification:** Monitors need risk-based visit plans and follow-up evidence.

**Improvement:** Add monitoring visit type, scope, site risk, planned dates, documents reviewed, findings, action items, and closeout status.

**Acceptance evidence:** Tests must create monitoring plans and close findings only after evidence is submitted.

### 15. Source Data Verification Strategy

**Justification:** Not every data point needs equal verification, but critical endpoints and safety data must be controlled.

**Improvement:** Add SDV requirements by field, visit, endpoint, risk, and site performance, with verified, queried, and waived states.

**Acceptance evidence:** Tests must enforce SDV for critical data and show risk-based reductions with approval evidence.

### 16. Data Query Lifecycle

**Justification:** Trial data queries need assignment, response, resolution, reopening, and auditability.

**Improvement:** Add query reason, data field, issuer, assignee, response, resolution, reopen reason, aging, and final lock impact.

**Acceptance evidence:** Tests must prevent data lock while required queries remain open.

### 17. Electronic Case Report Form Governance

**Justification:** CRF changes affect data capture and downstream analysis.

**Improvement:** Add form version, field definitions, validation checks, edit checks, activation date, migration impact, and retired field handling.

**Acceptance evidence:** Tests must preserve historical form versions and validate new entries against active definitions.

### 18. Endpoint and Outcome Traceability

**Justification:** Primary and secondary endpoints require source traceability and analysis readiness.

**Improvement:** Add endpoint definitions, contributing assessments, derivation rules, adjudication state, missing data reason, and lock status.

**Acceptance evidence:** Tests must trace endpoint values to source visits and block lock if critical endpoint evidence is missing.

### 19. Subject Retention and Visit Adherence

**Justification:** Missed visits and withdrawals threaten study power and safety follow-up.

**Improvement:** Add retention risk, missed-contact patterns, outreach tasks, barrier categories, travel support needs, and withdrawal prevention actions.

**Acceptance evidence:** Tests must open retention tasks for risk signals and respect consent and contact preferences.

### 20. Site Performance Scorecards

**Justification:** Sites vary in enrollment, data quality, query aging, protocol deviations, and safety reporting.

**Improvement:** Add scorecards for activation timeliness, enrollment pace, visit adherence, query aging, deviation rate, monitoring findings, and safety timeliness.

**Acceptance evidence:** Tests must calculate site metrics from owned trial evidence and show freshness.

### 21. Recruitment Funnel Tracking

**Justification:** Recruitment requires prescreening, outreach, eligibility, consent, screen failures, and enrollment conversion.

**Improvement:** Add recruitment funnel stages, referral source, outreach consent, screen-fail reason, diversity goal, and enrollment forecast.

**Acceptance evidence:** Tests must show funnel conversion and screen-fail breakdown without storing unauthorized patient data.

### 22. Diversity and Representativeness Monitoring

**Justification:** Trials need evidence that enrollment represents target populations and configured diversity goals.

**Improvement:** Add enrollment demographic projections, target cohorts, underrepresented group flags, site contribution, and corrective recruitment actions.

**Acceptance evidence:** Tests must compute representation gaps and open recruitment tasks without exposing unnecessary protected details.

### 23. Ethics and Regulatory Approval Tracking

**Justification:** Protocol, consent, recruitment material, amendments, and safety reports require approval tracking.

**Improvement:** Add approval body, submission package, approval date, expiry, conditions, amendment linkage, and renewal tasks.

**Acceptance evidence:** Tests must block site activation or amendment rollout when approvals are missing or expired.

### 24. Training Compliance

**Justification:** Staff need protocol, safety, system, privacy, and procedure training before performing trial duties.

**Improvement:** Add training curriculum, required roles, completion, expiry, waiver, and task authorization linkage.

**Acceptance evidence:** Tests must block delegated tasks for expired or missing training.

### 25. Trial Supply and Lab Kit Readiness

**Justification:** Missed supplies delay visits and compromise sample integrity.

**Improvement:** Add kit inventory, site supply level, expiry, shipment, receipt, temperature excursion, and visit supply readiness.

**Acceptance evidence:** Tests must warn when upcoming visits lack required valid kits.

### 26. Sample Collection Dependency

**Justification:** Trial visits often depend on lab samples collected within precise windows.

**Improvement:** Add sample requirement, collection window, processing requirement, shipment tracking, receipt status, and missing-sample deviation.

**Acceptance evidence:** Tests must open deviations for missed or mishandled samples and link them to visit evidence.

### 27. Safety Signal Review

**Justification:** Repeated adverse events, lab abnormalities, and discontinuations can indicate emerging safety concerns.

**Improvement:** Add safety signal candidates, frequency, seriousness mix, relatedness trend, review committee status, and action recommendation.

**Acceptance evidence:** Tests must create signal review cases and require human confirmation before protocol actions.

### 28. Risk-Based Monitoring Model Governance

**Justification:** Monitoring risk scores affect site oversight and data review.

**Improvement:** Register risk models with version, features, evaluation evidence, thresholds, drift checks, and reviewer feedback.

**Acceptance evidence:** Tests must block risk-based monitoring automation when model governance evidence is missing or stale.

### 29. Trial Master File Evidence

**Justification:** Trial operations need complete, inspectable evidence for protocol, approvals, monitoring, safety, training, and site files.

**Improvement:** Add evidence packet categories, required artifacts, missing artifact queue, owner, retention class, and inspection readiness score.

**Acceptance evidence:** Tests must identify missing essential documents and generate inspection-ready evidence packets.

### 30. Audit and Inspection Readiness

**Justification:** Trials can be inspected at site, sponsor, or study level.

**Improvement:** Add inspection request, scope, evidence room, finding, response, corrective action, due date, and closeout proof.

**Acceptance evidence:** Tests must produce scoped evidence rooms and track finding remediation.

### 31. Data Lock Readiness

**Justification:** Database lock requires resolved queries, monitored critical data, signed visits, reconciled safety, and approved deviations.

**Improvement:** Add lock checklist, blocking issue, owner, waiver, approval, and lock/unlock audit.

**Acceptance evidence:** Tests must block lock until critical open items are resolved or waived.

### 32. Consent-Aware Data Use

**Justification:** Subject consent limits data collection, optional samples, future use, and data sharing.

**Improvement:** Add consent scope for main study, optional sub-study, biospecimen, future research, recontact, and withdrawal restrictions.

**Acceptance evidence:** Tests must block data use or visit procedures outside active consent scope.

### 33. Privacy-Safe Subject Views

**Justification:** Monitors, site users, sponsors, and analysts need different access to subject data.

**Improvement:** Add role-based redaction for identifiers, clinical data, safety data, query data, and aggregate dashboards.

**Acceptance evidence:** Permission tests must prove each role sees only necessary data.

### 34. Trial Agent Evidence Summaries

**Justification:** Coordinators and monitors need concise summaries, but trial decisions need cited evidence.

**Improvement:** Add agent skills for subject status, visit readiness, safety narrative draft, monitoring finding summary, and data-lock blocker explanation.

**Acceptance evidence:** Tests must require citations and human approval for safety narratives and regulatory-facing text.

### 35. Governed Agent CRUD Commands

**Justification:** The chatbot should help with trial operations without silently changing regulated records.

**Improvement:** Add command previews for enroll subject, schedule visit, record consent, open deviation, add monitoring finding, open query, and draft safety report.

**Acceptance evidence:** Intent tests must require entity, protocol version, source evidence, preview, confirmation, and audit trail.

### 36. Protocol Amendment Impact Simulation

**Justification:** Amendments can trigger re-consent, schedule changes, endpoint changes, and site retraining.

**Improvement:** Add simulation for affected subjects, sites, visits, forms, consent records, training, and open deviations.

**Acceptance evidence:** Tests must produce amendment impact reports before activation.

### 37. Cross-PBC Boundary Proofs

**Justification:** Trial management composes with EHR, labs, devices, notifications, finance, and analytics without owning their tables.

**Improvement:** Add release gates proving external interactions use declared APIs, events, projections, or package metadata.

**Acceptance evidence:** Tests must fail on undeclared foreign table access and pass on declared AppGen-X contracts.

### 38. Trial Timeline Projection

**Justification:** Teams need a chronological view across protocol, site, subject, consent, visit, safety, monitoring, and data events.

**Improvement:** Add timeline projection with event type, actor, source, linked entity, protocol version, risk impact, and next action.

**Acceptance evidence:** Replay tests must reconstruct timelines idempotently with permission-aware redaction.

### 39. Deviation Root Cause Analytics

**Justification:** Recurrent deviations should drive prevention actions.

**Improvement:** Add root cause categories, site attribution, protocol complexity marker, training gap, process gap, and corrective action effectiveness.

**Acceptance evidence:** Tests must trend deviation causes and open prevention tasks.

### 40. Carbon and Participant Burden Awareness

**Justification:** Trial operations should consider participant travel, site burden, shipment frequency, and remote visit options.

**Improvement:** Add burden metrics, remote visit eligibility, travel support, shipment consolidation, and operational carbon estimates where relevant.

**Acceptance evidence:** Tests must show burden and sustainability metrics without overriding safety or protocol requirements.

### 41. Multi-Country Localization

**Justification:** Studies can span countries with different language, consent, reporting, and approval rules.

**Improvement:** Add jurisdiction-specific consent, safety reporting, data privacy, visit window, and document requirements.

**Acceptance evidence:** Tests must evaluate identical protocol events differently by jurisdiction and policy version.

### 42. Continuous Control Assertions

**Justification:** Trial quality requires controls over consent, eligibility, visits, safety reporting, monitoring, query aging, and lock readiness.

**Improvement:** Add controls with threshold, population, failing records, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and prevent closure without remediation proof.

### 43. Dead-Letter and Retry Operations

**Justification:** Trial events, lab results, safety documents, and monitoring updates can fail and must be replayed safely.

**Improvement:** Add dead-letter reason, risk, retry count, idempotency key, remediation action, and replay checkpoint.

**Acceptance evidence:** Tests must replay failed events without duplicate subjects, visits, adverse events, or queries.

### 44. Cryptographic Trial Evidence Proofs

**Justification:** Regulated trial records need tamper-evident evidence.

**Improvement:** Add proof chains for consent, eligibility, randomization, visit completion, adverse event reporting, monitoring findings, and data lock.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 45. Seeded Trial Scenario Library

**Justification:** Release audits need realistic clinical research stories.

**Improvement:** Add seeds for new protocol, site activation, subject enrollment, re-consent, missed visit, serious event, monitoring finding, data query, and database lock.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and workbench metrics.

### 46. Trial Operations Workbench

**Justification:** Trial users need persona-specific work queues.

**Improvement:** Add views for protocol amendments, site activation, screening, visit readiness, safety reporting, deviations, monitoring findings, queries, and lock blockers.

**Acceptance evidence:** UI tests must prove each view maps to owned data or declared projections with permission-aware actions.

### 47. Subject Discontinuation and Follow-Up

**Justification:** Withdrawal, lost-to-follow-up, safety discontinuation, and completed treatment have different data and safety obligations.

**Improvement:** Add discontinuation reason, treatment status, follow-up requirement, safety contact plan, data-use consent, and final status.

**Acceptance evidence:** Tests must distinguish treatment discontinuation from study withdrawal and preserve required follow-up tasks.

### 48. Full Clinical Trial Release Simulation

**Justification:** A complete PBC must prove the trial lifecycle end to end.

**Improvement:** Add a simulation where a protocol activates, site opens, subject consents, eligibility passes, visits occur, an adverse event is reported, monitoring finds an issue, queries resolve, and lock readiness is reached.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, UI views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate EHR, laboratory, device, finance, or regulatory-submission ownership.

**Improvement:** Add explicit overlap checks and declared dependency contracts for chart evidence, lab samples, device readings, sponsor budgets, and submission systems.

**Acceptance evidence:** Tests must fail on undeclared foreign table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose trial operations through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for protocols, sites, subjects, consents, visits, adverse events, monitoring, queries, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include trial models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
