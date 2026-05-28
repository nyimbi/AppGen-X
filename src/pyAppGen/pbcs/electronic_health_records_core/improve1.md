# Electronic Health Records Core PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `electronic_health_records_core` with a hand-curated clinical record roadmap. The scope is the owned electronic chart: patient charts, encounters, orders, observations, allergies, medication lists, care notes, summaries, documentation integrity, clinical safety, consent-aware access, governed agent assistance, and release evidence for a composable AppGen-X PBC.

## Current Domain Evidence Used

- Stable PBC key: `electronic_health_records_core`.
- Domain purpose: clinical encounters, orders, observations, allergies, medication lists, care notes, and patient summaries.
- Owned domain tables: `patient_chart`, `clinical_encounter`, `clinical_order`, `observation`, `allergy`, `medication_list`, `care_note`, `electronic_health_records_core_policy_rule`, `electronic_health_records_core_runtime_parameter`, `electronic_health_records_core_schema_extension`, `electronic_health_records_core_control_assertion`, `electronic_health_records_core_governed_model`.
- Public APIs: `POST /patient-charts`, `POST /clinical-encounters`, `POST /clinical-orders`, `POST /observations`, `POST /allergys`, `GET /electronic-health-records-core-workbench`.
- Emitted AppGen-X events: `ElectronicHealthRecordsCoreCreated`, `ElectronicHealthRecordsCoreUpdated`, `ElectronicHealthRecordsCoreApproved`, `ElectronicHealthRecordsCoreExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.

## 50 High-Impact Improvements

### 1. Longitudinal Chart Identity and Merge Review

**Justification:** A clinical chart can be fragmented by duplicate identities, registration corrections, or imported records, and unsafe automatic merging can corrupt the longitudinal record.

**Improvement:** Add chart identity confidence, duplicate candidate review, provisional chart state, merge recommendation, merge rejection reason, source-system lineage, and reversible chart-link decisions inside `patient_chart`.

**Acceptance evidence:** Tests must prove duplicate charts are flagged but not merged automatically, reviewers can accept or reject links with audit evidence, and generated summaries show identity uncertainty without reading a foreign master table.

### 2. Encounter Type and Care Setting Semantics

**Justification:** Ambulatory visits, emergency visits, virtual visits, inpatient rounds, procedures, and external consults require different documentation, signature, and order rules.

**Improvement:** Extend `clinical_encounter` with encounter class, care setting, visit modality, attending role, service line, arrival/discharge timestamps, external source, and required documentation checklist.

**Acceptance evidence:** Tests must validate setting-specific required fields, incomplete encounter warnings, and workbench queues for unsigned, incomplete, amended, and externally sourced encounters.

### 3. Clinical Note Authorship and Attestation

**Justification:** A care note is a clinical assertion with authorship, co-signature, addendum, and amendment rules, not a mutable text blob.

**Improvement:** Add note author, contributor, supervising signer, attestation status, co-signature requirement, addendum chain, correction reason, late-entry marker, and source evidence to `care_note`.

**Acceptance evidence:** Tests must reject unauthorized note signing, preserve original note text after amendment, and show attestation state in the EHR workbench and generated patient summary.

### 4. Problem-Oriented Chart Sections

**Justification:** Clinicians need records organized by active problems and episodes, not only chronological documents.

**Improvement:** Add chart section projections that group encounters, observations, orders, medications, allergies, and notes by problem, episode, acuity, and responsible clinician.

**Acceptance evidence:** Replay tests must rebuild problem-oriented views from owned events and package-owned records while preserving tenant boundaries and redaction rules.

### 5. Clinical Order Lifecycle

**Justification:** Orders move through draft, signed, released, scheduled, performed, resulted, canceled, discontinued, expired, and corrected states.

**Improvement:** Expand `clinical_order` with order type, priority, ordering clinician, indication, required specimen or procedure details, scheduling dependency, result expectation, cancellation reason, and discontinuation authority.

**Acceptance evidence:** Tests must prove invalid order transitions are rejected, result-required orders cannot close without evidence, and order cancellation emits AppGen-X events.

### 6. Order Set Governance

**Justification:** Order sets reduce variability but can create unsafe defaults if not versioned and reviewed.

**Improvement:** Add governed order-set templates with indication, included orders, optional orders, contraindication prompts, version, approving committee, activation window, and rollback plan.

**Acceptance evidence:** Tests must instantiate order sets, preserve template version on each order, block retired templates, and run policy impact simulation before activation.

### 7. Observation Units and Reference Ranges

**Justification:** Observations are unsafe without units, methods, reference ranges, abnormality interpretation, and specimen context.

**Improvement:** Extend `observation` with unit, method, specimen type, collection time, result time, reference range, abnormal flag, critical flag, performer, and corrected-result lineage.

**Acceptance evidence:** Tests must validate unit compatibility, critical-result routing, corrected-result history, and trend displays for numeric and categorical observations.

### 8. Critical Result Acknowledgement

**Justification:** Critical lab, imaging, and device observations require closed-loop acknowledgement and escalation.

**Improvement:** Add acknowledgement owner, deadline, notified party, notification channel, read-back evidence, escalation tier, and unresolved critical result queue.

**Acceptance evidence:** Tests must open critical-result exceptions, escalate missed acknowledgements, and prevent false closure without acknowledgement evidence.

### 9. Allergy Substance and Reaction Specificity

**Justification:** Allergy records must distinguish intolerance, adverse reaction, contraindication, inactive allergy, and unverified patient report.

**Improvement:** Expand `allergy` with substance class, specific substance, reaction, severity, onset, verification status, source, inactive reason, and clinical override guidance.

**Acceptance evidence:** Tests must prove duplicate allergy entries are detected, inactive allergies remain visible, and medication order warnings reference reaction and severity.

### 10. Medication List Reconciliation

**Justification:** Medication lists drift across encounters, transitions, external data, and patient reports.

**Improvement:** Add medication-list reconciliation sessions with source list, patient-reported medication, start/stop/change action, discrepancy reason, reviewer, and unresolved discrepancy.

**Acceptance evidence:** Tests must preserve reconciliation history, block encounter closure when required reconciliation is incomplete, and require confirmation before agent-proposed medication changes.

### 11. Medication Safety Screening Projection

**Justification:** The EHR core must expose medication safety evidence without becoming a pharmacy claims or dispensing system.

**Improvement:** Build projections for allergy conflict, duplicate therapy, dose-range warning, medication-observation conflict, pregnancy or renal caution, and active high-risk medication.

**Acceptance evidence:** Tests must prove safety warnings are derived from owned chart evidence and declared event/API inputs, never from shared tables.

### 12. Patient Summary Assembly

**Justification:** Patient summaries need curated clinical sections, freshness markers, and redaction, not raw record dumps.

**Improvement:** Generate summaries with active problems, recent encounters, active medications, allergies, key observations, pending orders, care notes, risk flags, and source freshness.

**Acceptance evidence:** Tests must show summaries differ by permission, include source timestamps, and flag stale or incomplete sections.

### 13. Snapshot and Point-in-Time Chart Review

**Justification:** Legal, safety, and clinical review often require seeing what the chart looked like at a past time.

**Improvement:** Add immutable event history and projection checkpoints for patient chart, encounter, order, observation, allergy, medication list, and note mutations.

**Acceptance evidence:** Replay tests must reconstruct chart state at a requested time and prove amendments do not erase prior clinical assertions.

### 14. Clinical Documentation Deficiency Workqueue

**Justification:** Missing signatures, incomplete fields, absent diagnosis links, and late notes create operational and compliance risk.

**Improvement:** Add deficiency records with type, responsible role, due date, severity, blocker status, linked encounter or note, remediation action, and closure evidence.

**Acceptance evidence:** Tests must open deficiencies automatically from incomplete records and close them only after the underlying evidence is fixed.

### 15. Patient-Generated Data Intake

**Justification:** Patient-reported symptoms, device readings, questionnaires, and attachments can enrich care but must be triaged before becoming chart evidence.

**Improvement:** Add intake states for submitted, parsed, clinically relevant, needs review, accepted into chart, rejected, and escalated, with source and reviewer evidence.

**Acceptance evidence:** Tests must require review for safety-sensitive patient submissions and preserve rejected submissions with reason and audit trail.

### 16. External Document Reconciliation

**Justification:** Imported summaries, referral notes, diagnostic reports, and scanned documents need structured reconciliation before they affect the chart.

**Improvement:** Add document extraction evidence, matched chart section, extracted finding, confidence, reviewer, accepted field, rejected field, and source span.

**Acceptance evidence:** Tests must prove agent-extracted fields cannot mutate chart state without reviewer approval when confidence or policy requires review.

### 17. Consent-Aware Chart Access

**Justification:** Clinical records include sensitive sections that need purpose, role, patient consent, and break-glass controls.

**Improvement:** Add access purpose, consent scope, sensitive-section labels, emergency override reason, review queue, and post-access audit notification.

**Acceptance evidence:** Permission tests must block restricted sections, allow policy-governed emergency override, and record override evidence for audit.

### 18. Segment-Level Redaction

**Justification:** Sharing a full note when only a medication list or problem summary is needed exposes unnecessary clinical detail.

**Improvement:** Support redaction profiles for patient summary, specialist handoff, patient portal, legal export, research export, and public-health report.

**Acceptance evidence:** Tests must prove each profile includes required fields, excludes restricted sections, and cites redaction reasons.

### 19. Clinical Coding Support Boundary

**Justification:** Diagnoses and procedures matter for documentation and downstream workflows, but this PBC should not own payer adjudication.

**Improvement:** Add chart-owned coding evidence for encounter diagnosis, procedure evidence, clinical indication, documentation support, and unresolved coding clarification.

**Acceptance evidence:** Tests must show coding evidence can be emitted through AppGen-X events while claims and payment workflows remain external dependencies.

### 20. Clinical Decision Support Rule Registry

**Justification:** Safety alerts and reminders need governed rules, versioning, explainability, and override capture.

**Improvement:** Add rule definitions for allergy warnings, overdue observations, missing follow-up, unsafe orders, contraindications, and documentation gaps with severity and override policies.

**Acceptance evidence:** Rule tests must show versioned evaluation, visible explanation, override justification, and rollback behavior.

### 21. Override Fatigue Controls

**Justification:** Excessive alerts train users to ignore clinically important warnings.

**Improvement:** Track alert frequency, accepted overrides, duplicate alerts, low-value rules, user burden, and suppression candidates with governance review.

**Acceptance evidence:** Tests must compute alert burden and require approval before suppressing a rule.

### 22. Chart Search With Clinical Semantics

**Justification:** Search should understand chart concepts such as active allergies, abnormal observations, unsigned notes, and pending orders.

**Improvement:** Add package-owned search indexes for chart sections, note text, order status, observation trends, allergy reaction, medication name, and source documents.

**Acceptance evidence:** Search tests must return permission-filtered results and prove sensitive segments are not exposed through snippets.

### 23. Problem List Quality Review

**Justification:** Active, inactive, duplicate, vague, and stale problems reduce clinical usefulness.

**Improvement:** Add problem quality signals derived from note references, encounter relevance, active orders, observation evidence, medication links, and last reviewed date.

**Acceptance evidence:** Tests must open quality review tasks for stale or conflicting problem evidence and require human confirmation for problem status changes.

### 24. Longitudinal Trend Panels

**Justification:** Single observations rarely explain clinical trajectory.

**Improvement:** Add trend panels for configurable observation groups with baseline, latest value, slope, abnormality pattern, missing measurements, and clinical note references.

**Acceptance evidence:** Tests must classify improving, stable, worsening, missing, and unreliable trends with unit consistency.

### 25. Encounter Timeline Reconstruction

**Justification:** Clinicians need a coherent timeline across arrival, notes, orders, observations, medications, and discharge events.

**Improvement:** Build encounter timelines with actor, event type, timestamp, source, linked entity, and whether the event changed chart state.

**Acceptance evidence:** Replay tests must sort concurrent events deterministically and show amended events without hiding the original sequence.

### 26. Agent-Assisted Chart Summarization

**Justification:** The EHR agent must help summarize records while staying evidence-cited and permission-aware.

**Improvement:** Add chart summarization skills for encounter recap, medication history, allergy review, observation trend, pending work, and patient-friendly summary with source citations.

**Acceptance evidence:** Tests must prove every generated sentence is backed by chart evidence or marked as an inference, and restricted sections are omitted by permission.

### 27. Governed Agent CRUD Previews

**Justification:** The agent should help create and update chart entries, but it must not silently mutate clinical records.

**Improvement:** Add command previews for create encounter, draft note, add allergy, record observation, reconcile medication, and close order, each with required fields and evidence.

**Acceptance evidence:** Tests must reject ambiguous commands, require confirmation for mutation, and store the instruction, source evidence, actor, and resulting command.

### 28. Documented Clinical Ambiguity Handling

**Justification:** Clinical documents often contain uncertain, conflicting, or negated statements.

**Improvement:** Add ambiguity markers for suspected condition, ruled-out condition, historical condition, family history, patient-reported item, conflicting source, and low-confidence extraction.

**Acceptance evidence:** Extraction tests must preserve uncertainty instead of converting it into confirmed chart facts.

### 29. Configurable Chart Section Schema Extensions

**Justification:** Specialty practices need custom fields without breaking the core chart contract.

**Improvement:** Use `electronic_health_records_core_schema_extension` for governed specialty templates, validation rules, UI placement, migration evidence, and backward-compatible projections.

**Acceptance evidence:** Tests must add, activate, deprecate, and read specialty extensions without invalidating existing chart records.

### 30. Tenant-Specific Clinical Policy Isolation

**Justification:** Health systems, regions, and programs can have different documentation and consent rules.

**Improvement:** Add tenant-scoped policies for signature timing, observation critical thresholds, order review, access restrictions, retention, and agent approval gates.

**Acceptance evidence:** Tests must prove tenant policies do not leak and identical chart events can evaluate differently by tenant.

### 31. Retention, Amendment, and Legal Hold

**Justification:** Clinical records require long-term retention, amendment visibility, export support, and legal hold.

**Improvement:** Add retention category, amendment chain, legal hold flag, export eligibility, deletion prohibition reason, and evidence packet generation.

**Acceptance evidence:** Tests must block deletion under retention or legal hold and produce redacted evidence packets by request type.

### 32. Privacy-Safe Analytics Extracts

**Justification:** Operational analytics should not expose raw notes or sensitive chart sections unnecessarily.

**Improvement:** Add de-identified and limited-data-set projections for encounter volume, documentation lag, order turnaround, observation abnormality, and deficiency aging.

**Acceptance evidence:** Tests must verify low-count suppression, redaction, permission gating, and explicit analytic purpose.

### 33. Public Health and Reporting Readiness

**Justification:** Some chart data must support reportable-condition, immunization, and surveillance workflows while preserving ownership boundaries.

**Improvement:** Add reportability indicators, reporting trigger evidence, destination profile, required fields, submission state, and correction history.

**Acceptance evidence:** Tests must create reportable-event candidates and emit AppGen-X events without owning external public-health registry tables.

### 34. Downtime and Offline Documentation Mode

**Justification:** Clinical care continues during connectivity or dependency failures.

**Improvement:** Add offline draft capture, local sequence numbers, delayed reconciliation, conflict detection, degraded-mode warnings, and recovery audit.

**Acceptance evidence:** Tests must replay offline entries, detect conflicts, and require review before conflicting records become active chart evidence.

### 35. Data Quality Controls for Core Chart Fields

**Justification:** Incorrect dates, units, patient age conflicts, impossible values, and missing authorship create safety risk.

**Improvement:** Add controls for demographic projection freshness, encounter time consistency, observation plausibility, order indication completeness, allergy severity, and note signer validity.

**Acceptance evidence:** Control tests must open exceptions with severity, owner, due date, and closure evidence.

### 36. Dead-Letter and Retry Clinical Inbox

**Justification:** Consumed events and document imports can fail and must be remediated without losing clinical evidence.

**Improvement:** Add retry classification, dead-letter reason, clinical risk, reprocess eligibility, human remediation note, and replay checkpoint.

**Acceptance evidence:** Tests must prove failed events are idempotent on replay and visible in a clinical operations queue.

### 37. Cross-PBC Boundary Proofs

**Justification:** The EHR core must integrate with care coordination, revenue cycle, pharmacy, and analytics without sharing tables.

**Improvement:** Add release checks that every dependency is represented as declared API, event, projection, or package metadata rather than foreign table reads.

**Acceptance evidence:** Boundary tests must fail if generated EHR artifacts reference undeclared external tables.

### 38. Patient Portal Summary Controls

**Justification:** Patient-facing records need language level, release timing, sensitive-result handling, and correction request workflows.

**Improvement:** Add portal summary profiles, delayed-release rules, patient-friendly terminology, correction-request intake, and clinician review tasks.

**Acceptance evidence:** Tests must hold sensitive results when policy requires delay and track patient correction requests through resolution.

### 39. Clinical Attachment Handling

**Justification:** Images, PDFs, scanned forms, device files, and external reports need metadata, source, retention, and review state.

**Improvement:** Add attachment descriptors with type, source, linked entity, extracted text status, review state, checksum, redaction profile, and retention class.

**Acceptance evidence:** Tests must validate checksum preservation, linked-record visibility, and redacted export behavior.

### 40. Workbench Role Views

**Justification:** Clinicians, nurses, health information managers, administrators, and privacy officers need different EHR work queues.

**Improvement:** Redesign `ElectronicHealthRecordsCoreWorkbench` around role views for unsigned notes, critical results, pending orders, chart deficiencies, privacy overrides, imports, and patient correction requests.

**Acceptance evidence:** UI contract tests must prove each view maps to owned data, declared dependencies, and permission-aware actions.

### 41. Specialty Template Library

**Justification:** Pediatrics, oncology, behavioral health, surgery, chronic disease, and emergency care require different documentation structures.

**Improvement:** Add specialty templates with required sections, order prompts, observation panels, note headings, summary fragments, and review cadence.

**Acceptance evidence:** Tests must instantiate specialty templates and preserve template version on created notes and encounters.

### 42. Clinical Quality Measure Traceability

**Justification:** Quality measures require denominator, numerator, exclusion, and source evidence, not informal reporting.

**Improvement:** Add measure trace records linking chart facts to quality measure candidates, exclusions, and unresolved evidence gaps.

**Acceptance evidence:** Tests must prove measure candidates cite chart evidence and emit events to reporting PBCs without owning their reporting state.

### 43. Record Locking and Concurrent Editing

**Justification:** Concurrent edits to notes, medication lists, and orders can overwrite clinical work.

**Improvement:** Add optimistic versioning, edit sessions, conflict previews, merge suggestions, and required signoff for conflicting clinical updates.

**Acceptance evidence:** Tests must simulate concurrent edits and preserve both user changes until a reviewer resolves the conflict.

### 44. Chart Completeness Score

**Justification:** Users need an actionable measure of whether a chart is clinically usable.

**Improvement:** Score chart completeness using identity confidence, active allergies, medication reconciliation, recent encounter documentation, pending orders, critical results, and deficiencies.

**Acceptance evidence:** Tests must calculate completeness components and show missing evidence rather than a single opaque score.

### 45. Clinical Safety Exception Taxonomy

**Justification:** Safety exceptions need precise categories for response and governance.

**Improvement:** Add exception types for critical result missed, unsafe order, medication conflict, missing allergy review, incomplete encounter, privacy override, data-quality risk, and stale projection.

**Acceptance evidence:** Tests must route exceptions by severity and close only with remediation evidence.

### 46. Cryptographic Chart Integrity Proofs

**Justification:** Auditors and regulators may need proof that chart history was not altered.

**Improvement:** Add hash-chained evidence packets for chart mutations, note signatures, order transitions, observation corrections, and export bundles.

**Acceptance evidence:** Tests must verify proof chains and fail on tampered event order or modified payload hashes.

### 47. Governed Model Registry for Clinical Agent Features

**Justification:** Clinical agent recommendations need model, prompt, evaluation, and drift evidence.

**Improvement:** Register summarization, extraction, risk, and recommendation models with version, evaluation cohort, intended use, confidence thresholds, and human feedback.

**Acceptance evidence:** Tests must block model-backed commands when model approval is missing or expired.

### 48. Seeded Clinical Scenario Library

**Justification:** Release audits need realistic clinical stories rather than isolated fixtures.

**Improvement:** Add seed scenarios for routine visit, critical lab, medication reconciliation, allergy conflict, external document import, patient correction, privacy override, and amended note.

**Acceptance evidence:** Scenario tests must load seeds side-effect-free and prove workbench queues, events, and summaries reflect each story.

### 49. Full EHR Release Simulation

**Justification:** A complete PBC should prove the chart lifecycle end to end.

**Improvement:** Add a release simulation where a patient chart is created, an encounter opens, notes are drafted and signed, orders are placed, observations result, allergy and medication lists reconcile, a summary is generated, and an amendment is audited.

**Acceptance evidence:** The simulation must validate owned tables, AppGen-X events, idempotent handlers, UI fragments, agent skills, permissions, and release evidence.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** The EHR core must compose cleanly into generated applications and expose its skills through the unified application agent.

**Improvement:** Extend composition metadata for chart entities, order workflows, observation contracts, summary projections, UI fragments, rule parameters, agent skills, and boundary proof gates.

**Acceptance evidence:** DSL generation tests must prove composed apps include EHR-owned models, routes, services, workbench views, assistant skills, and AppGen-X event contracts without exposing stream-engine picker choices.
