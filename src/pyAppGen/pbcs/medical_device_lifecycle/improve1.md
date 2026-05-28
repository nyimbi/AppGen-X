# Medical Device Lifecycle PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `medical_device_lifecycle` with a hand-curated medical device operations roadmap. The PBC owns medical device registry, assignments, calibration, maintenance events, recall notices, usage traceability, regulatory evidence, governed rules, agent assistance, and release evidence without owning hospital biomedical finance, EHR clinical orders, or manufacturing batch quality tables.

## Current Domain Evidence Used

- Stable PBC key: `medical_device_lifecycle`.
- Domain purpose: medical device registry, maintenance, calibration, recalls, usage traceability, and regulatory evidence.
- Owned domain tables: `medical_device`, `device_assignment`, `calibration`, `maintenance_event`, `recall_notice`, `usage_traceability`, `regulatory_evidence`, `medical_device_lifecycle_policy_rule`, `medical_device_lifecycle_runtime_parameter`, `medical_device_lifecycle_schema_extension`, `medical_device_lifecycle_control_assertion`, `medical_device_lifecycle_governed_model`.
- Public APIs: `POST /medical-devices`, `POST /device-assignments`, `POST /calibrations`, `POST /maintenance-events`, `POST /recall-notices`, `GET /medical-device-lifecycle-workbench`.
- Emitted AppGen-X events: `MedicalDeviceLifecycleCreated`, `MedicalDeviceLifecycleUpdated`, `MedicalDeviceLifecycleApproved`, `MedicalDeviceLifecycleExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Unique Device Identity Registry

**Justification:** Medical device traceability depends on manufacturer, model, serial, lot, software version, implantability, and regulatory identifiers.

**Improvement:** Expand `medical_device` with unique device identity, model, serial, lot, firmware, hardware revision, risk class, implantable flag, sterile flag, and source evidence.

**Acceptance evidence:** Tests must prevent duplicate active identities and preserve historical identity corrections.

### 2. Device Lifecycle State Machine

**Justification:** Devices move through acquisition, qualification, available, assigned, in use, quarantined, maintenance, calibration due, recall hold, retired, and disposed states.

**Improvement:** Add explicit lifecycle transitions with actor, reason, evidence, allowed next states, and AppGen-X event emission.

**Acceptance evidence:** Tests must reject unsafe transitions such as assigning recalled, unqualified, retired, or calibration-overdue devices.

### 3. Department and Location Traceability

**Justification:** Devices are mobile assets that must be findable during care, maintenance, and recall events.

**Improvement:** Add current location, owning department, physical zone, last scan, custody actor, transfer event, and location confidence.

**Acceptance evidence:** Tests must reconstruct location history and flag missing scans or conflicting custody.

### 4. Device Assignment Governance

**Justification:** Assignments to patients, rooms, clinicians, procedures, or departments require time-bounded evidence and privacy controls.

**Improvement:** Expand `device_assignment` with assignment type, assignee projection, start/end time, intended use, responsible role, consent/privacy flag, and release condition.

**Acceptance evidence:** Tests must prove assignments close correctly and redacted views hide patient-linked details when permission is absent.

### 5. Implant Tracking

**Justification:** Implantable devices require durable patient association, lot traceability, explant, adverse event, and recall follow-up.

**Improvement:** Add implant-specific fields for implant date, procedure projection, implanting clinician, body site, explant date, explant reason, and patient notification status.

**Acceptance evidence:** Tests must identify all active patients affected by an implant recall without reading EHR tables directly.

### 6. Calibration Schedule and Tolerance

**Justification:** Calibration status determines whether device readings can be trusted.

**Improvement:** Expand `calibration` with required interval, tolerance, standard used, before/after values, technician, pass/fail, due date, and out-of-tolerance impact.

**Acceptance evidence:** Tests must block use of overdue or failed-calibration devices and open impact review for out-of-tolerance findings.

### 7. Preventive Maintenance Program

**Justification:** Maintenance should be planned, risk-based, and evidence-backed.

**Improvement:** Add maintenance plans by device class, usage intensity, risk class, manufacturer guidance, last service, next due, and task checklist.

**Acceptance evidence:** Tests must generate due maintenance tasks and route overdue high-risk devices to quarantine.

### 8. Corrective Maintenance Events

**Justification:** Break/fix work must capture symptoms, diagnosis, parts, labor, downtime, and return-to-service evidence.

**Improvement:** Expand `maintenance_event` with failure mode, severity, root cause, parts replaced, technician, downtime, service vendor, and qualification result.

**Acceptance evidence:** Tests must keep failed devices unavailable until return-to-service criteria pass.

### 9. Recall Notice Intake

**Justification:** Recalls can target model, lot, serial, firmware, implant cohort, or accessory groups.

**Improvement:** Expand `recall_notice` with recall class, manufacturer notice, affected criteria, required action, deadline, patient impact flag, and closure requirements.

**Acceptance evidence:** Tests must match affected inventory and assignments from recall criteria and open worklists.

### 10. Recall Execution Workflow

**Justification:** Recall closure requires locating devices, removing them from service, notifying stakeholders, remediation, and evidence.

**Improvement:** Add recall tasks for quarantine, patient notification, firmware update, replacement, return, documentation, and unresolved exception.

**Acceptance evidence:** Tests must block recall closure until all affected devices or justified exceptions are resolved.

### 11. Field Safety Corrective Action

**Justification:** Safety corrections can require inspections, software updates, labeling changes, and user training.

**Improvement:** Add action type, target devices, procedure, completion evidence, training requirement, and effectiveness check.

**Acceptance evidence:** Tests must track action completion and prevent affected devices from use until required action is complete.

### 12. Firmware and Software Configuration

**Justification:** Device software version affects safety, cybersecurity, performance, and compatibility.

**Improvement:** Add firmware/software version, approved baseline, patch status, cybersecurity risk, rollback plan, and configuration drift.

**Acceptance evidence:** Tests must detect unauthorized version drift and block devices with critical unresolved patches.

### 13. Cybersecurity Vulnerability Tracking

**Justification:** Connected devices can introduce clinical and operational risk.

**Improvement:** Add vulnerability identifier, affected device class, severity, mitigation, network exposure, patch status, compensating control, and due date.

**Acceptance evidence:** Tests must open vulnerability remediation tasks and show risk by device, location, and assignment.

### 14. Usage Traceability

**Justification:** Device usage history supports maintenance, recalls, utilization, and safety investigations.

**Improvement:** Expand `usage_traceability` with event type, start/end time, operator projection, location, patient/procedure projection, usage metric, and exception.

**Acceptance evidence:** Tests must compute utilization and preserve redaction for patient-linked usage.

### 15. Regulatory Evidence Repository

**Justification:** Device operations require manuals, certificates, validations, service records, recall letters, and training evidence.

**Improvement:** Expand `regulatory_evidence` with document type, effective date, device scope, retention class, approval, checksum, and evidence packet membership.

**Acceptance evidence:** Tests must generate device evidence packets and detect missing required documents.

### 16. Incoming Inspection and Qualification

**Justification:** New or repaired devices must be inspected before use.

**Improvement:** Add incoming inspection checklist, acceptance criteria, device labeling check, software baseline, accessories, and qualification result.

**Acceptance evidence:** Tests must keep devices unavailable until qualification passes.

### 17. Loaner and Rental Device Controls

**Justification:** Temporary devices need the same traceability, service, and recall controls as owned devices.

**Improvement:** Add ownership type, vendor, loan/rental period, service responsibility, return condition, and evidence requirements.

**Acceptance evidence:** Tests must track temporary devices and enforce return or extension controls.

### 18. Sterilization and Reprocessing Evidence

**Justification:** Reusable devices may require cleaning, sterilization, reprocessing, and cycle tracking.

**Improvement:** Add reprocessing cycle, method, operator, lot, pass/fail, expiration, usage count, and quarantine on failure.

**Acceptance evidence:** Tests must block assignment of devices with expired or failed reprocessing evidence.

### 19. Accessories and Component Hierarchy

**Justification:** Safety often depends on compatible accessories, batteries, probes, cables, and modules.

**Improvement:** Add parent-child device components, compatibility rules, accessory assignment, replacement history, and missing component flags.

**Acceptance evidence:** Tests must reject incompatible accessory pairings and trace component recalls.

### 20. Battery and Consumable Readiness

**Justification:** Device availability depends on battery health, consumables, sensors, and sterile accessories.

**Improvement:** Add readiness checks for battery cycle, charge status, consumable expiry, accessory availability, and replacement due date.

**Acceptance evidence:** Tests must flag devices as not ready when critical consumables are unavailable or expired.

### 21. Clinical Alarm and Alert Evidence

**Justification:** Some devices generate alarms that require review, configuration, or incident linkage.

**Improvement:** Add alarm configuration, threshold, alarm event, acknowledgement, nuisance alarm marker, and safety review link.

**Acceptance evidence:** Tests must route unacknowledged high-severity alarms and preserve event history.

### 22. Adverse Event and Incident Linkage

**Justification:** Device problems can require safety investigation and regulatory reporting.

**Improvement:** Add incident link, suspected device issue, harm severity, investigation status, reportability assessment, and corrective action.

**Acceptance evidence:** Tests must open reportability review for high-severity incidents and block closure without assessment.

### 23. Regulatory Reporting Readiness

**Justification:** Certain device events require timely reporting with complete evidence.

**Improvement:** Add report candidate, jurisdiction, deadline, required fields, submission status, acknowledgement, and follow-up.

**Acceptance evidence:** Tests must escalate overdue reportable-device events and generate evidence packets.

### 24. Device Training and Competency

**Justification:** Staff should only use devices for which they are trained and competent.

**Improvement:** Add training requirements by device class, role, competency expiry, user acknowledgement, and assignment/use gate.

**Acceptance evidence:** Tests must warn or block use by untrained staff according to policy.

### 25. Work Order and Vendor Service Contract

**Justification:** External service work needs contract, scope, response time, parts, invoice evidence, and return-to-service control.

**Improvement:** Add vendor service fields, contract SLA, dispatch, repair notes, parts, service certification, and acceptance evidence.

**Acceptance evidence:** Tests must track vendor work and prevent return to service without acceptance.

### 26. Utilization and Fleet Optimization

**Justification:** Device fleets are costly and often overstocked or unavailable in the wrong places.

**Improvement:** Add utilization metrics by device class, site, department, shift, downtime, assignment duration, and idle inventory.

**Acceptance evidence:** Tests must calculate utilization and recommend redistribution without directly changing assignments.

### 27. Predictive Maintenance Risk

**Justification:** Failure can be anticipated from age, usage, service history, alarms, calibration drift, and environment.

**Improvement:** Add risk score with explanatory factors, threshold, recommended action, and confidence.

**Acceptance evidence:** Tests must generate explainable predictions and require human approval for quarantine recommendations.

### 28. Device Availability Command Center

**Justification:** Operations teams need a single view of available, in use, down, recalled, overdue, and missing devices.

**Improvement:** Add workbench queues for availability, recall, maintenance due, calibration due, cybersecurity risk, missing location, and utilization hotspots.

**Acceptance evidence:** UI tests must prove queues map to owned records and declared projections with permission-aware actions.

### 29. Agent-Assisted Device Summaries

**Justification:** Biomedical and clinical users need concise device state explanations with evidence.

**Improvement:** Add agent skills for device readiness summary, recall impact summary, maintenance history, calibration status, vulnerability exposure, and assignment timeline.

**Acceptance evidence:** Tests must require citations and mark recommendations as draft until confirmed.

### 30. Governed Agent CRUD Commands

**Justification:** The chatbot should help operate device records without unsafe mutation.

**Improvement:** Add command previews for assign device, quarantine device, record calibration, open maintenance, close recall task, update firmware status, and retire device.

**Acceptance evidence:** Intent tests must require device identity, action, evidence, preview, confirmation, and audit trail.

### 31. Continuous Control Assertions

**Justification:** Device lifecycle quality requires controls over calibration, maintenance, recalls, location, training, cybersecurity, and evidence completeness.

**Improvement:** Add controls with threshold, population, failing devices, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open failures and require remediation proof before closure.

### 32. Dead-Letter and Retry Operations

**Justification:** Device scan events, service updates, recalls, and vulnerability feeds can fail.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed events without duplicate assignments, recalls, or maintenance records.

### 33. Cross-PBC Boundary Proofs

**Justification:** Device lifecycle composes with EHR, facilities, procurement, lab, quality, notifications, and audit without table sharing.

**Improvement:** Add release gates proving external relationships use declared APIs, events, projections, or package metadata.

**Acceptance evidence:** Tests must fail on undeclared foreign table reads and pass on AppGen-X dependency contracts.

### 34. Device Timeline Projection

**Justification:** Investigations and audits need a chronological view of acquisition, assignment, use, maintenance, calibration, recall, and retirement.

**Improvement:** Build timeline projection with actor, event type, source, linked record, risk impact, and evidence reference.

**Acceptance evidence:** Replay tests must reconstruct timelines idempotently with role-based redaction.

### 35. Recall Patient Notification Boundary

**Justification:** Device recalls may require patient notification while patient identity remains owned elsewhere.

**Improvement:** Store patient impact evidence and notification task references using declared projection identifiers, not direct patient-table writes.

**Acceptance evidence:** Boundary tests must prove notification events are emitted and no external patient tables are modified.

### 36. Device Disposition and Disposal

**Justification:** Retired, returned, destroyed, donated, or sold devices require evidence and data sanitization where applicable.

**Improvement:** Add disposition type, approval, data wipe evidence, environmental handling, vendor return, destruction certificate, and final state.

**Acceptance evidence:** Tests must block disposal without required approvals and evidence.

### 37. Recall Drill and Readiness Simulation

**Justification:** Organizations need to prove they can locate affected devices quickly.

**Improvement:** Add side-effect-free recall drill simulations over inventory, assignments, locations, patient impact, and communication tasks.

**Acceptance evidence:** Tests must produce drill metrics and identify gaps without mutating live recall state.

### 38. Configuration and Policy Impact Simulation

**Justification:** Changing calibration interval, maintenance frequency, or recall handling can affect safety and availability.

**Improvement:** Add simulations over device cohorts for policy changes with risk, workload, availability, and compliance impact.

**Acceptance evidence:** Tests must require simulation evidence before activating high-risk parameter changes.

### 39. Regulatory Classification Localization

**Justification:** Device risk class, reporting, maintenance, and traceability requirements vary by jurisdiction.

**Improvement:** Add jurisdiction-specific classification, reporting duty, retention, labeling, and recall workflow rules.

**Acceptance evidence:** Tests must evaluate identical device events differently by jurisdiction and policy version.

### 40. Device Data Integrity Controls

**Justification:** Device records require trustworthy timestamps, signatures, event order, and source authenticity.

**Improvement:** Add controls for backdated events, unauthorized edits, missing source checksums, orphan assignments, and signature gaps.

**Acceptance evidence:** Tests must open data-integrity exceptions and prevent closure without remediation.

### 41. Cryptographic Device Evidence Proofs

**Justification:** Recalls, incidents, and audits need tamper-evident device history.

**Improvement:** Add hash chains for registry creation, assignment, calibration, maintenance, recall, incident, and disposal events.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 42. Seeded Device Scenario Library

**Justification:** Release audits need realistic medical device stories.

**Improvement:** Add seeds for device qualification, assignment, calibration failure, maintenance, recall, firmware vulnerability, implant trace, and disposal.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and metrics.

### 43. Device Recall Analytics

**Justification:** Recall performance should be measurable by time to locate, time to quarantine, patient impact, exception count, and closure quality.

**Improvement:** Add recall analytics by recall class, device cohort, location, patient impact, overdue task, and unresolved exception.

**Acceptance evidence:** Tests must compute recall metrics from owned evidence.

### 44. Maintenance Quality Analytics

**Justification:** Repeated failures and vendor issues indicate quality problems.

**Improvement:** Add analytics for downtime, repeat repairs, parts failures, vendor SLA, calibration failure rate, and mean time between failures.

**Acceptance evidence:** Tests must produce source-linked metrics and open quality review for recurring failures.

### 45. Role-Based Permission Model

**Justification:** Biomedical engineers, nurses, department managers, cybersecurity users, compliance users, and auditors need different authority.

**Improvement:** Add permissions for assign, quarantine, calibrate, maintain, close recall, update firmware, dispose, and view patient-linked usage.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 46. Evidence Packet Generation

**Justification:** Device audits need focused packets, not raw exports.

**Improvement:** Add packet generation for device history, recall, maintenance, calibration, cybersecurity vulnerability, incident, and disposition.

**Acceptance evidence:** Tests must generate scoped packets with source links, checksums, and redaction.

### 47. Carbon and Resource Awareness

**Justification:** Device operations involve energy, disposable accessories, shipping, and retirement waste.

**Improvement:** Add optional resource metrics for utilization efficiency, disposable use, shipping, repair versus replace decisions, and disposal category.

**Acceptance evidence:** Tests must report resource metrics without overriding safety or regulatory rules.

### 48. Full Device Lifecycle Release Simulation

**Justification:** A complete PBC must prove device lifecycle behavior end to end.

**Improvement:** Add a simulation where a device is registered, qualified, assigned, calibrated, maintained, recalled, remediated, audited, and retired.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate EHR, facilities, procurement, lab, quality, cybersecurity, or finance ownership.

**Improvement:** Add overlap checks and dependency contracts for clinical use, location, vendor procurement, lab instrument outputs, vulnerabilities, and audit evidence.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X contracts.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose device lifecycle operations through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for devices, assignments, calibrations, maintenance, recalls, usage traceability, regulatory evidence, workbench fragments, controls, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include device models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
