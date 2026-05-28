# Laboratory Information Management PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `laboratory_information_management` with a hand-curated laboratory operations roadmap. The PBC owns samples, test orders, instrument runs, results, quality controls, chain of custody, laboratory workflows, governed rules, agent assistance, and release evidence without owning clinical chart source-of-truth, manufacturing batch records, or external accreditation systems.

## Current Domain Evidence Used

- Stable PBC key: `laboratory_information_management`.
- Domain purpose: samples, tests, instruments, results, quality control, chain of custody, and laboratory workflows.
- Owned domain tables: `lab_sample`, `test_order`, `instrument_run`, `result`, `quality_control`, `chain_of_custody`, `laboratory_workflow`, `laboratory_information_management_policy_rule`, `laboratory_information_management_runtime_parameter`, `laboratory_information_management_schema_extension`, `laboratory_information_management_control_assertion`, `laboratory_information_management_governed_model`.
- Public APIs: `POST /lab-samples`, `POST /test-orders`, `POST /instrument-runs`, `POST /results`, `POST /quality-controls`, `GET /laboratory-information-management-workbench`.
- Emitted AppGen-X events: `LaboratoryInformationManagementCreated`, `LaboratoryInformationManagementUpdated`, `LaboratoryInformationManagementApproved`, `LaboratoryInformationManagementExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Sample Identity and Accessioning

**Justification:** Sample identity errors can invalidate results and create safety or compliance failures.

**Improvement:** Add accession number, sample type, collection time, received time, collector, container, preservative, patient or study reference projection, and identity confidence.

**Acceptance evidence:** Tests must prevent duplicate accessioning and flag mismatched identifiers without querying foreign patient or study tables.

### 2. Chain of Custody Lifecycle

**Justification:** Many laboratory samples require provable custody from collection to disposal.

**Improvement:** Expand `chain_of_custody` with handoff actor, location, timestamp, condition, seal status, exception, and custody acceptance.

**Acceptance evidence:** Tests must reconstruct custody history and reject result release when required custody breaks are unresolved.

### 3. Specimen Condition Assessment

**Justification:** Hemolysis, clotting, temperature excursion, insufficient volume, leakage, and delayed transport can compromise results.

**Improvement:** Add condition codes, severity, accept/reject decision, recollection requirement, reviewer, and result qualification text.

**Acceptance evidence:** Tests must reject or qualify samples according to configured test and condition rules.

### 4. Test Order Completeness

**Justification:** Laboratory orders need test, priority, specimen type, ordering party, diagnosis/indication, billing context, and collection instructions.

**Improvement:** Expand `test_order` with order priority, ordered tests, required specimen, clinical context, standing order flag, reflex eligibility, and missing-order-data queue.

**Acceptance evidence:** Tests must block incomplete orders and route stat orders to urgent queues.

### 5. Order-to-Sample Matching

**Justification:** Results are unsafe if samples cannot be confidently matched to orders.

**Improvement:** Add match status, match confidence, unmatched sample queue, unmatched order queue, split sample handling, and merge/reject review.

**Acceptance evidence:** Tests must cover exact match, partial match, duplicate sample, extra sample, and no-order scenarios.

### 6. Test Method Versioning

**Justification:** Methods, reagents, reference ranges, and instruments change over time.

**Improvement:** Add test method version, validation status, effective window, instrument compatibility, reagent lot requirements, and retired method handling.

**Acceptance evidence:** Tests must result historical samples against the method version active at run time.

### 7. Instrument Registry and Status

**Justification:** Instrument availability, maintenance, calibration, and qualification affect result validity.

**Improvement:** Add instrument identity, location, status, method capability, maintenance due, calibration due, qualification state, and downtime reason.

**Acceptance evidence:** Tests must block runs on unavailable, unqualified, or overdue instruments.

### 8. Instrument Run Lifecycle

**Justification:** Runs include setup, control verification, sample loading, execution, review, result import, and acceptance.

**Improvement:** Expand `instrument_run` with run batch, operator, instrument, method, controls, sample list, run state, failure reason, and rerun link.

**Acceptance evidence:** Tests must process completed, failed, rerun, and partially accepted runs.

### 9. Quality Control Rule Engine

**Justification:** QC determines whether analytical results can be accepted.

**Improvement:** Add QC material, lot, expected range, observed value, rule, pass/fail, trend, reviewer, and corrective action.

**Acceptance evidence:** Tests must reject result release when required QC fails or is missing.

### 10. Calibration Management

**Justification:** Calibration drift can invalidate results.

**Improvement:** Add calibration schedule, calibration material, acceptance criteria, result, expiry, drift warning, and corrective action.

**Acceptance evidence:** Tests must block methods requiring current calibration when calibration is expired or failed.

### 11. Reagent and Consumable Lot Traceability

**Justification:** Reagent lot problems can require result review or recall.

**Improvement:** Add reagent lot, expiry, storage condition, lot qualification, run usage, and affected-result lookup.

**Acceptance evidence:** Tests must identify results affected by an invalidated reagent lot.

### 12. Result Validation and Review

**Justification:** Results require technical and sometimes clinical review before release.

**Improvement:** Expand `result` with preliminary/final/corrected status, reviewer, validation rule, abnormal flag, critical flag, and release authorization.

**Acceptance evidence:** Tests must prevent final release without required review and preserve correction history.

### 13. Critical Result Notification

**Justification:** Critical results require timely closed-loop notification.

**Improvement:** Add critical threshold, recipient, notification time, read-back evidence, escalation, and unresolved critical queue.

**Acceptance evidence:** Tests must escalate overdue critical notifications and emit AppGen-X events.

### 14. Reference Range Governance

**Justification:** Reference ranges vary by method, unit, age, sex, specimen, and site.

**Improvement:** Add reference range version, demographic applicability, unit, method, effective window, approval, and impact analysis.

**Acceptance evidence:** Tests must classify results against the correct reference range version.

### 15. Reflex and Add-On Testing

**Justification:** Laboratory workflows often trigger reflex or add-on tests based on preliminary findings.

**Improvement:** Add reflex rule, trigger condition, authorization requirement, sample sufficiency check, created order link, and audit evidence.

**Acceptance evidence:** Tests must create reflex orders, reject invalid add-ons, and preserve triggering result evidence.

### 16. Sample Aliquot and Derivative Tracking

**Justification:** Samples can be split, pooled, extracted, frozen, or consumed.

**Improvement:** Add aliquot identity, parent sample, derivative type, volume, storage location, freeze/thaw count, and consumption status.

**Acceptance evidence:** Tests must trace derivatives to parent samples and prevent over-consumption.

### 17. Storage Location and Stability

**Justification:** Sample validity depends on storage temperature, duration, and location.

**Improvement:** Add storage unit, position, temperature profile, stability expiry, movement history, and excursion handling.

**Acceptance evidence:** Tests must flag expired or excursion-affected samples before testing.

### 18. Turnaround Time Management

**Justification:** Lab operations are measured and governed by turnaround targets by test, priority, and setting.

**Improvement:** Add TAT start/stop rules, target, hold reason, breach risk, escalation, and completed metric.

**Acceptance evidence:** Tests must calculate TAT and escalate stat, routine, and delayed tests correctly.

### 19. Workcell and Bench Workflow

**Justification:** Labs need operational queues for accessioning, prep, analysis, review, release, and exceptions.

**Improvement:** Add `laboratory_workflow` states for intake, sample prep, queued, running, review, held, released, recollect, and disposed.

**Acceptance evidence:** Tests must route samples by department, priority, method, and exception state.

### 20. Microbiology Culture Workflow

**Justification:** Culture testing has incubation, preliminary results, organism identification, susceptibility, and finalization.

**Improvement:** Add culture stage, incubation condition, organism candidate, susceptibility panel, preliminary report, and final report logic.

**Acceptance evidence:** Tests must handle preliminary and final culture results with corrected organism data.

### 21. Molecular and Genetic Testing Controls

**Justification:** Molecular tests need sample quality, extraction, amplification, variant interpretation, and contamination controls.

**Improvement:** Add extraction batch, amplification controls, variant evidence, interpretation state, contamination flag, and confirmatory review.

**Acceptance evidence:** Tests must require controls and reviewer signoff for high-impact molecular results.

### 22. Environmental and Nonclinical Sample Support

**Justification:** Laboratories may test environmental, product, or research samples without patient identities.

**Improvement:** Add sample domain, collection site, batch/lot projection, chain of custody, specification limit, and disposition recommendation.

**Acceptance evidence:** Tests must process nonclinical samples while preserving separate identity and reporting rules.

### 23. Stability Study and Retain Sample Handling

**Justification:** Stability and retain workflows require scheduled pulls and long-term evidence.

**Improvement:** Add stability protocol, timepoint, storage condition, pull schedule, test panel, trend result, and retain disposition.

**Acceptance evidence:** Tests must schedule and complete stability timepoints with storage evidence.

### 24. Result Correction and Amendment

**Justification:** Corrected results must not erase previously released results.

**Improvement:** Add correction reason, original value, corrected value, approver, notification requirement, and downstream event.

**Acceptance evidence:** Tests must preserve original result and emit correction events idempotently.

### 25. Proficiency Testing

**Justification:** External proficiency testing proves laboratory competence.

**Improvement:** Add proficiency event, sample, expected result, submitted result, evaluation, corrective action, and accreditation evidence.

**Acceptance evidence:** Tests must track failed proficiency and require corrective action closure.

### 26. Nonconformance and CAPA

**Justification:** Laboratory errors require documented investigation and corrective/preventive action.

**Improvement:** Add nonconformance type, affected samples, severity, root cause, containment, CAPA, effectiveness check, and closure evidence.

**Acceptance evidence:** Tests must open CAPA from QC failures, custody breaks, and result corrections.

### 27. Audit Trail and E-Signature

**Justification:** Regulated laboratories require complete audit trails and controlled signatures.

**Improvement:** Add e-signature purpose, signer role, timestamp, record hash, meaning of signature, and signature revocation state.

**Acceptance evidence:** Tests must prove signed results cannot be changed without amendment workflow.

### 28. LIMS Agent Result Summaries

**Justification:** Staff need concise summaries of sample status, QC blockers, and result history.

**Improvement:** Add agent skills for sample status, run summary, QC failure explanation, critical result draft, and audit packet summary with citations.

**Acceptance evidence:** Tests must require evidence citations and confirmation before release-impacting changes.

### 29. Governed Agent CRUD Commands

**Justification:** The chatbot should help create and update lab records safely.

**Improvement:** Add command previews for accession sample, schedule test, record QC, hold result, release result, correct result, and open nonconformance.

**Acceptance evidence:** Intent tests must require entity, evidence, preview, confirmation, and audit trail.

### 30. Instrument Integration Event Contract

**Justification:** Instruments produce data streams, files, and status events that must be normalized.

**Improvement:** Add contracts for run started, result imported, QC imported, instrument error, maintenance due, and run completed events.

**Acceptance evidence:** Handler tests must be idempotent and reject malformed instrument payloads.

### 31. Result Reporting Boundary

**Justification:** Results may flow to EHR, trial, manufacturing, or customer systems without shared tables.

**Improvement:** Emit result-final, result-corrected, critical-result, sample-rejected, and nonconformance events with declared schemas.

**Acceptance evidence:** Boundary tests must fail on undeclared external table writes and pass on AppGen-X event/API usage.

### 32. Method Validation Evidence

**Justification:** New or changed methods require validation before operational use.

**Improvement:** Add validation protocol, accuracy, precision, linearity, limit of detection, interference, approval, and effective date.

**Acceptance evidence:** Tests must block unvalidated methods and preserve validation evidence.

### 33. Batch Review for High-Throughput Testing

**Justification:** Batch operations require group-level QC, outlier review, and release decisions.

**Improvement:** Add batch review state, included samples, controls, outliers, rerun list, reviewer, and release decision.

**Acceptance evidence:** Tests must release valid batches and hold affected samples when batch review fails.

### 34. Data Integrity Controls

**Justification:** Laboratories must prevent backdating, unauthorized edits, orphan results, and unverifiable imports.

**Improvement:** Add controls for timestamp order, actor authorization, source checksum, orphan detection, and signed-record integrity.

**Acceptance evidence:** Tests must open control failures and require remediation evidence.

### 35. Laboratory Role-Based Workbench

**Justification:** Accessioners, technologists, supervisors, QA users, pathologists, and managers need distinct queues.

**Improvement:** Add workbench views for accession issues, pending runs, QC failures, critical results, review queue, nonconformance, TAT risk, and audit readiness.

**Acceptance evidence:** UI tests must prove permission-aware actions and owned-data mappings for each view.

### 36. Retention and Disposal

**Justification:** Samples, results, audit records, and attachments have retention and disposal requirements.

**Improvement:** Add retention class, disposal eligibility, disposal approval, legal hold, retained sample location, and destruction evidence.

**Acceptance evidence:** Tests must block disposal under hold or active retention and audit approved destruction.

### 37. Multi-Site Laboratory Operations

**Justification:** Samples may move between collection sites, reference labs, and specialty labs.

**Improvement:** Add site, transfer, referred test, expected return, external lab status, received result, and chain-of-custody continuation.

**Acceptance evidence:** Tests must track referred samples and flag overdue external results.

### 38. Recollection Workflow

**Justification:** Rejected or compromised samples require controlled recollection requests.

**Improvement:** Add recollection reason, requester, patient or source notification, priority, linked rejected sample, and new sample match.

**Acceptance evidence:** Tests must create recollection tasks and link replacement samples to the original order.

### 39. Privacy and Redaction Profiles

**Justification:** Laboratory results and samples can contain sensitive clinical or research data.

**Improvement:** Add role-based redaction for patient identifiers, study identifiers, genetic results, quality data, and audit exports.

**Acceptance evidence:** Permission tests must prove exports and workbench views apply redaction correctly.

### 40. Predictive TAT and Capacity Risk

**Justification:** Labs need early warning before turnaround breaches.

**Improvement:** Add capacity forecasts from order volume, instrument status, staffing projection, sample priority, QC failures, and backlog.

**Acceptance evidence:** Tests must produce explainable TAT risk and compare forecast to actual performance.

### 41. Quality Trend Analytics

**Justification:** Recurrent QC failures, recollections, corrections, and TAT breaches need trend analysis.

**Improvement:** Add analytics for QC drift, rejected specimens, corrected results, instrument downtime, nonconformance categories, and bench productivity.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with drilldown to source evidence.

### 42. Cryptographic Result Proofs

**Justification:** Result history needs tamper-evident proof.

**Improvement:** Add hash chains for accession, custody, instrument run, QC, result release, correction, and disposal events.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 43. Configuration Impact Simulation

**Justification:** Changing QC rules, reference ranges, TAT targets, or method versions can affect many results.

**Improvement:** Add side-effect-free simulations over recent samples, results, QC runs, and method cohorts.

**Acceptance evidence:** Tests must produce impact reports before activation of high-risk lab configuration.

### 44. Dead-Letter and Retry Operations

**Justification:** Instrument events, result imports, custody updates, and reporting events can fail.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed events without duplicate samples, runs, results, or critical notifications.

### 45. Seeded Laboratory Scenario Library

**Justification:** Release audits need realistic laboratory stories.

**Improvement:** Add seeds for accessioning, rejected specimen, instrument run, QC failure, critical result, corrected result, chain-of-custody break, and proficiency failure.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and metrics.

### 46. Accreditation Evidence Packets

**Justification:** Laboratory inspections require method, QC, personnel, equipment, result, and nonconformance evidence.

**Improvement:** Add evidence packet generation by test, instrument, date range, sample, method, and quality event.

**Acceptance evidence:** Tests must generate scoped packets with source links and redaction.

### 47. Carbon and Resource Awareness

**Justification:** Laboratory operations consume reagents, energy, cold storage, and shipping resources.

**Improvement:** Add optional resource metrics for reagent waste, reruns, cold storage, shipment distance, and instrument utilization.

**Acceptance evidence:** Tests must report resource metrics without overriding clinical or quality requirements.

### 48. Full Laboratory Release Simulation

**Justification:** A complete PBC must prove sample-to-result behavior end to end.

**Improvement:** Add a simulation where an order is received, sample accessioned, custody tracked, instrument run completed, QC reviewed, result released, critical notification sent, and correction audited.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** LIMS must not duplicate EHR, clinical trial, manufacturing quality, medical device, or external accreditation ownership.

**Improvement:** Add overlap checks and declared dependency contracts for clinical orders, trial samples, device outputs, quality events, and reporting systems.

**Acceptance evidence:** Tests must fail on undeclared foreign table references and pass on declared AppGen-X contracts.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose laboratory capabilities through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for samples, orders, instruments, runs, results, QC, custody, workflows, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include LIMS models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
