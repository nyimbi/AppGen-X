# Clinical Care Coordination PBC Manual Improvement Backlog

## Purpose

This manually curated backlog identifies 50 high-impact improvements for `clinical_care_coordination`. The items are specific to care plans, care teams, referrals, encounters, care gaps, transitions of care, outcome measures, patient coordination operations, and the safeguards needed for an AppGen-X PBC that owns clinical coordination state without sharing tables.

## Current Domain Evidence Used

- Stable PBC key: `clinical_care_coordination`.
- Domain purpose: care plans, referrals, encounters, care teams, transitions, outcomes, and patient coordination workflows.
- Owned domain tables: `patient_care_plan`, `care_team`, `referral`, `encounter`, `care_gap`, `transition_plan`, `outcome_measure`, `clinical_care_coordination_policy_rule`, `clinical_care_coordination_runtime_parameter`, `clinical_care_coordination_schema_extension`, `clinical_care_coordination_control_assertion`, `clinical_care_coordination_governed_model`.
- Public APIs: `POST /patient-care-plans`, `POST /care-teams`, `POST /referrals`, `POST /encounters`, `POST /care-gaps`, `GET /clinical-care-coordination-workbench`.
- Emitted AppGen-X events: `ClinicalCareCoordinationCreated`, `ClinicalCareCoordinationUpdated`, `ClinicalCareCoordinationApproved`, `ClinicalCareCoordinationExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.
- UI fragments: `ClinicalCareCoordinationWorkbench`, `ClinicalCareCoordinationDetail`, `ClinicalCareCoordinationAssistantPanel`.

## 50 High-Impact Improvements

### 1. Longitudinal Patient Care Plan State Machine

**Justification:** Care plans are longitudinal clinical commitments, not simple tasks. The PBC needs a state model that distinguishes draft goals, active interventions, suspended interventions, partially met goals, clinically contraindicated actions, patient-declined steps, and closed outcomes.

**Improvement:** Replace the generic `patient_care_plan` lifecycle with a clinical care-plan state machine covering problem linkage, goal hierarchy, planned intervention, responsible discipline, patient preference, target date, review cadence, barrier, variance, and closure reason. Include explicit transitions for care-plan revision after a new encounter, medication change, discharge event, or patient refusal.

**Acceptance evidence:** Package-local tests must prove invalid transitions are rejected, care-plan revisions emit AppGen-X events, closed goals preserve historical targets, and the workbench shows active, overdue, blocked, patient-declined, and achieved plan segments without reading foreign tables.

### 2. Interdisciplinary Care Team Roster With Role Semantics

**Justification:** A clinical care team is not just a list of users. Different team members have clinical authority, communication preferences, coverage periods, escalation responsibility, and consent restrictions.

**Improvement:** Expand `care_team` into a roster model with primary coordinator, attending clinician, specialist, social worker, pharmacist, caregiver, community resource, interpreter, and external partner roles. Track coverage windows, backup contacts, escalation routes, communication channel, patient consent scope, and whether a participant can receive protected details.

**Acceptance evidence:** Tests should validate role-specific permissions, overlapping coverage, consent-limited participants, escalation lookup, and UI filtering by active/inactive team members. The assistant must refuse to disclose restricted care-plan data to a care-team member without matching consent scope.

### 3. Referral Lifecycle With Closure Accountability

**Justification:** Referral leakage is a major failure mode in care coordination: referrals are ordered but not scheduled, scheduled but not attended, completed but not resulted, or resulted but not incorporated into the care plan.

**Improvement:** Add a referral lifecycle spanning need identified, referral drafted, authorization required, authorization obtained, sent, accepted, scheduled, completed, result received, result reconciled, declined, expired, and closed. Capture specialty, urgency, reason, receiving organization, expected turnaround, authorization evidence, appointment details, result document pointer, and closure accountability.

**Acceptance evidence:** Tests should cover urgent referrals, missing authorization, duplicate referrals to the same specialty, expired referrals, external result receipt, and result reconciliation into care-plan updates. Workbench queues must separate unsent, unscheduled, overdue, awaiting result, and unreconciled referrals.

### 4. Encounter-Derived Coordination Tasks

**Justification:** Coordination work often originates in clinical encounters, but generic encounter records do not prove that follow-up actions were extracted, assigned, and tracked.

**Improvement:** Make `encounter` intake create explicit coordination tasks for follow-up visits, labs, imaging, medication reviews, home support, care-gap closure, patient education, and social-needs referrals. Each task should retain source encounter, source note span, clinical priority, due date, owner role, and whether patient outreach is required.

**Acceptance evidence:** Encounter parsing tests must create tasks from structured payloads and document instructions, preserve source traceability, and prevent duplicate tasks when the same encounter is replayed. The workbench must show encounter-derived tasks grouped by patient, due date, and responsible role.

### 5. Care Gap Taxonomy Specific to Preventive, Chronic, Safety, and Access Gaps

**Justification:** A single care-gap status hides important differences between preventive screening gaps, chronic disease monitoring, medication safety, social needs, access barriers, and transition follow-up.

**Improvement:** Replace generic `care_gap` records with a typed taxonomy: preventive screening, immunization, chronic monitoring, medication reconciliation, high-risk medication, behavioral health follow-up, social determinant, post-discharge follow-up, missed appointment, and patient outreach gap. Add severity, source, guideline basis, denominator eligibility, exclusion reason, and closure evidence.

**Acceptance evidence:** Tests must prove each gap type can be opened, excluded, deferred, closed, reopened, and linked to a care-plan intervention. UI queues must distinguish guideline gaps from operational outreach gaps and show the evidence needed for closure.

### 6. Transition-of-Care Packet Integrity

**Justification:** Transitions between hospital, clinic, specialist, home health, and community settings are high-risk moments where missing medication lists or follow-up instructions can harm patients.

**Improvement:** Extend `transition_plan` with discharge source, receiving setting, medication reconciliation status, pending test results, follow-up appointments, durable equipment, home services, patient instructions, caregiver confirmation, transportation plan, and readmission risk. Include packet completeness scoring before transition closure.

**Acceptance evidence:** Tests must block transition closure when medication reconciliation, follow-up appointment, or patient instruction evidence is missing for configured high-risk transitions. AppGen-X events must distinguish packet completed, packet incomplete, handoff accepted, and follow-up overdue.

### 7. Outcome Measure Registry With Baseline and Target Semantics

**Justification:** Outcome measures are only meaningful when the PBC knows the baseline, target, measurement method, timing, and whether the measure is patient-reported, clinician-observed, or derived.

**Improvement:** Expand `outcome_measure` to support baseline value, target value, measure owner, unit, collection cadence, source, numerator/denominator where applicable, patient-reported outcome flag, confidence, and attribution to care-plan goals. Support trend classification: improving, stable, worsening, unreliable, and missing.

**Acceptance evidence:** Tests should verify baseline capture, target comparison, missing measurement detection, outlier detection, and trend classification. The workbench must show whether each active care-plan goal has measurable outcome evidence.

### 8. Patient Preference and Goal Concordance

**Justification:** World-class coordination should not optimize only clinical tasks; it must respect patient preferences, priorities, language, caregiver involvement, transportation constraints, and willingness to act.

**Improvement:** Add preference capture to care plans and transitions: preferred language, contact channel, caregiver contact permission, appointment constraints, cultural considerations, education format, care goals in patient wording, and declined interventions. Use these preferences when scheduling outreach, assigning tasks, and suggesting next actions.

**Acceptance evidence:** Tests must prove the assistant includes patient preferences in drafted care-plan updates, blocks outreach on disallowed channels, and flags interventions that conflict with documented preferences. UI must display preference conflicts before approval.

### 9. Social Needs and Barrier Tracking

**Justification:** Coordination often fails because of transportation, food insecurity, housing instability, cost, caregiver availability, or digital access barriers.

**Improvement:** Add barrier records linked to care gaps, referrals, transitions, and care-plan interventions. Model barrier type, severity, patient-reported source, resource referral, follow-up date, responsible role, and resolution evidence. Include barrier-aware risk scoring and task routing.

**Acceptance evidence:** Tests must show unresolved barriers increase risk and block false closure of related gaps. Workbench panels should surface patients whose clinical care plan is blocked by non-clinical barriers.

### 10. Medication Reconciliation Handoff

**Justification:** Medication discrepancies are a core coordination risk after encounters, referrals, and transitions.

**Improvement:** Add medication reconciliation checkpoints that track source medication list, patient-reported medications, discontinued medications, new prescriptions, duplicate therapies, high-risk interactions, reconciliation owner, and unresolved discrepancy reason. Keep the data inside this PBC as coordination evidence, with external medication systems represented only through events or APIs.

**Acceptance evidence:** Tests must prove reconciliation tasks are opened after transition events, discrepancies are not silently closed, and care-plan updates reference reconciliation evidence. The assistant must draft discrepancy summaries but require human confirmation before closing medication-related tasks.

### 11. Closed-Loop Patient Outreach

**Justification:** Outreach attempts are not enough; coordination requires evidence that the patient or caregiver was reached, understood the next step, and had barriers addressed.

**Improvement:** Add outreach attempts, channel, script version, contact result, patient understanding confirmation, callback request, interpreter need, barrier discovered, and next action. Support closed-loop states: attempted, reached, confirmed, declined, unreachable, escalated, and no further outreach permitted.

**Acceptance evidence:** Tests must prove outreach attempts are idempotent, do not violate consent preferences, and drive care-gap or referral state changes only when confirmation evidence exists. UI must show outreach history without mixing it into clinical encounter notes.

### 12. Care Coordination Risk Stratification

**Justification:** Coordinators need to know which patients require immediate attention across many plans, gaps, referrals, and transitions.

**Improvement:** Build a risk score that combines overdue care gaps, unresolved referrals, transition risk, outcome deterioration, social barriers, missed outreach, recent exceptions, and stale care-team coverage. Provide explainable components and configurable weights through `clinical_care_coordination_runtime_parameter`.

**Acceptance evidence:** Tests must demonstrate low, moderate, high, and critical risk cases with explanations. The workbench should sort queues by risk while showing the contributing reasons and last recalculation event.

### 13. Duplicate and Fragmented Patient Coordination Detection

**Justification:** Coordination records can fragment when the same patient is represented by multiple identifiers or multiple care plans are opened for the same episode.

**Improvement:** Add duplicate detection for care plans, referrals, transitions, and care gaps using patient identifier projections, encounter timing, specialty, diagnosis/problem references, and source-event lineage. Do not merge automatically; create review tasks with safe suggested merges.

**Acceptance evidence:** Tests must prove suspected duplicates are flagged, automatic mutation is blocked, reviewer decisions are audited, and merge suggestions preserve both source histories. No shared patient master table may be mutated.

### 14. Clinical Priority and Urgency Rules

**Justification:** A two-week routine follow-up and a same-day safety concern cannot share the same workflow semantics.

**Improvement:** Add clinical priority rules for referrals, care gaps, transitions, and outreach based on severity, age of task, transition context, high-risk medication, worsening outcome measure, and clinician-entered urgency. Include timer policies and escalation thresholds.

**Acceptance evidence:** Tests should validate priority escalation, timer pause/resume, due-date recalculation, and override justification. UI should display the current priority reason and the policy version that assigned it.

### 15. Guideline and Measure Versioning

**Justification:** Preventive care and chronic care guidance changes over time; closure evidence must be evaluated against the correct version.

**Improvement:** Version guideline basis, measure definitions, denominator rules, exclusion reasons, and closure evidence for each care gap and outcome measure. Add impact analysis for guideline changes so coordinators know which patients need reassessment.

**Acceptance evidence:** Tests must show historical gap decisions remain tied to their original rule version while new evaluations use the active version. Workbench must show guideline update impact lists.

### 16. Care Plan Goal Hierarchy

**Justification:** Care plans often include nested goals: a broad outcome goal, several clinical goals, and operational interventions.

**Improvement:** Model parent-child care-plan goals with goal type, intervention type, target outcome, responsible role, dependency, and blocker. Support goal-level closure and care-plan-level closure separately.

**Acceptance evidence:** Tests must verify a care plan cannot close while required child goals remain active unless an approved override reason exists. UI should show goal trees and blocked dependencies.

### 17. Referral Network Performance Evidence

**Justification:** Coordination quality depends on whether referral destinations accept, schedule, complete, and return results reliably.

**Improvement:** Build package-owned referral-destination performance projections from referral states: acceptance lag, scheduling lag, no-show rate, result return lag, denial rate, and unreconciled result count. Do not store external provider master data beyond coordination evidence.

**Acceptance evidence:** Tests must prove projections update from AppGen-X events and remain tenant-scoped. Workbench should show destination performance when choosing or reviewing a referral.

### 18. Transition Readmission Watchlist

**Justification:** Post-discharge patients can deteriorate quickly if follow-up, medication, equipment, or home support tasks fail.

**Improvement:** Add a watchlist that monitors transition-plan completeness, outcome signals, missed outreach, unresolved barriers, missing follow-up appointment, and care-team coverage. Trigger escalation when risk crosses configured thresholds.

**Acceptance evidence:** Tests must create readmission watchlist entries from transition plans and prove closure requires follow-up evidence. AppGen-X events should identify watchlist opened, escalated, and resolved.

### 19. Patient Education Assignment and Comprehension

**Justification:** Giving instructions is not the same as confirming comprehension.

**Improvement:** Add education assignments linked to care plans and transitions with topic, literacy level, language, delivery channel, responsible role, comprehension check, teach-back evidence, and unresolved questions.

**Acceptance evidence:** Tests must block education task closure without comprehension evidence where policy requires it. The assistant can draft education summaries but must record source documents and require confirmation.

### 20. Consent-Aware Caregiver Collaboration

**Justification:** Caregivers are central to coordination but may have limited authority or restricted information access.

**Improvement:** Add caregiver collaboration records with relationship, consent scope, expiration, allowed communication topics, preferred channel, emergency contact flag, and revocation history. Link caregiver tasks to outreach and transition plans.

**Acceptance evidence:** Tests must prove caregiver communications are blocked outside consent scope and that consent revocation prevents future assistant disclosures. UI must clearly mark caregiver access limits.

### 21. Coordination Command Center Workbench

**Justification:** The current workbench must become an operational command center, not a generic record list.

**Improvement:** Redesign `ClinicalCareCoordinationWorkbench` around coordinator queues: high-risk patients, overdue referrals, unreconciled results, active transitions, blocked care gaps, outreach due today, care-team coverage gaps, and control failures. Include quick actions, filters, and patient timeline summaries.

**Acceptance evidence:** UI contract tests must prove each queue maps to package-owned tables or declared events, respects permissions, and exposes counts, aging, and action availability.

### 22. Patient Timeline Projection

**Justification:** Coordinators need a single temporal view across care-plan changes, encounters, referrals, outreach, gaps, transitions, and outcomes.

**Improvement:** Build a patient coordination timeline projection sourced from package-owned events and consumed AppGen-X events. Include event type, actor, source, linked entity, summary, risk impact, and whether it changed the care plan.

**Acceptance evidence:** Replay tests must reconstruct a timeline in order, deduplicate events, and preserve redaction rules. The detail UI must show the timeline without querying foreign tables.

### 23. Source Document and Instruction Traceability

**Justification:** Assistant-generated coordination changes need traceability back to the document text, instruction, or source event that justified them.

**Improvement:** Add source evidence records for care plans, referrals, transitions, and care gaps: document ID, source span, extracted field, confidence, reviewer, confirmation timestamp, and resulting command.

**Acceptance evidence:** Tests must prove every assistant-drafted mutation includes source evidence and cannot be approved without reviewer confirmation when confidence is below policy threshold.

### 24. Care Team Coverage Gap Detection

**Justification:** Patients can be left unmanaged when a coordinator is unavailable, a specialist leaves the team, or coverage windows expire.

**Improvement:** Detect gaps in care-team coverage by role and time window. Open exceptions when primary coordinator, responsible clinician, interpreter, or required specialist coverage is missing for active high-risk care plans or transitions.

**Acceptance evidence:** Tests must prove coverage windows are evaluated daily and after team changes. Workbench must show coverage gaps with recommended replacement role, not just a generic exception.

### 25. Patient No-Show and Missed-Contact Patterning

**Justification:** Repeated no-shows and missed contacts are coordination signals that should change outreach strategy and barrier assessment.

**Improvement:** Add pattern detection for missed appointments, missed calls, unreturned messages, repeated declined referrals, and incomplete follow-ups. Link patterns to barriers, outreach strategy, and care-plan revision recommendations.

**Acceptance evidence:** Tests must show repeated missed contact opens a barrier review and changes recommended outreach channel according to patient preference and policy.

### 26. Care Gap Exclusion Governance

**Justification:** Exclusions can be clinically valid or can hide incomplete work; the PBC must distinguish them.

**Improvement:** Model exclusion reason, evidence type, expiration, approving role, source guideline, and re-evaluation date for care gaps. Support temporary exclusions, permanent contraindications, patient refusal, duplicate measure, and not clinically indicated.

**Acceptance evidence:** Tests must reject unsupported exclusions, reopen expired exclusions, and include exclusions in audit evidence. UI must show exclusion rationale and expiration.

### 27. Result Reconciliation Workflow

**Justification:** Referral and test results create little value if they are received but not reconciled into the care plan.

**Improvement:** Add result reconciliation records linked to referrals, encounters, outcome measures, and care-plan goals. Capture result source, clinical significance, action required, responsible role, reviewed by, and care-plan impact.

**Acceptance evidence:** Tests must prove results can be received, marked no action required, or converted into care-plan updates, and unreconciled results remain visible as blocking work.

### 28. High-Risk Medication and Allergy Coordination

**Justification:** Allergies and high-risk medications influence referrals, transitions, education, and follow-up even when medication management is owned elsewhere.

**Improvement:** Store coordination evidence for high-risk medication and allergy alerts received through events, and link them to care-plan tasks, transition plans, and patient education. Do not mutate the source medication or allergy system.

**Acceptance evidence:** Consumed-event handler tests must show allergy/medication risk opens coordination tasks and preserves source lineage. UI must mark medication-related tasks separately.

### 29. Patient Cohort Worklists

**Justification:** Coordinators often manage cohorts such as post-discharge, diabetes, oncology navigation, maternal health, frailty, or complex care.

**Improvement:** Add cohort definitions and worklists based on package-owned evidence and declared event inputs. Support cohort criteria, membership explanation, coordinator assignment, SLA policy, and cohort-level outcome measures.

**Acceptance evidence:** Tests must prove cohort membership updates after events and that users can drill from a cohort metric to patient-level coordination work.

### 30. Escalation Ladder and Command Authorization

**Justification:** Clinical coordination has escalation pathways: coordinator, supervisor, clinician, specialist, case conference, emergency escalation.

**Improvement:** Add escalation ladder rules that decide who can approve overdue referrals, urgent transition failures, patient safety exceptions, or conflicting care instructions. Include escalation reason, target role, due time, and escalation outcome.

**Acceptance evidence:** Permission tests must prove only authorized roles can resolve high-severity escalations. Events must distinguish escalation opened, reassigned, resolved, and breached.

### 31. Care Conference Planning

**Justification:** Complex patients often require interdisciplinary care conferences that produce decisions, assignments, and follow-ups.

**Improvement:** Add care conference records with agenda, participants, patient/caregiver involvement, decisions, follow-up tasks, unresolved disagreements, and next review date. Link conference outputs to care-plan goals and referrals.

**Acceptance evidence:** Tests must prove conference decisions generate tasks and preserve participant attendance. UI must show conference history on the patient timeline.

### 32. Patient Safety Exception Playbooks

**Justification:** Some coordination failures carry immediate patient safety risk and need structured playbooks rather than free-form notes.

**Improvement:** Create playbooks for urgent referral not scheduled, critical result unreconciled, failed discharge follow-up, medication discrepancy, unreachable high-risk patient, and missing caregiver support. Each playbook should specify detection, required evidence, escalation role, allowed commands, and closure criteria.

**Acceptance evidence:** Tests must prove each playbook can be opened, escalated, resolved, and audited. The assistant must guide the playbook but cannot close it without required evidence.

### 33. Coordination Quality Measures

**Justification:** The PBC should measure whether coordination improves outcomes, not merely whether tasks are completed.

**Improvement:** Add quality measures such as referral completion rate, result reconciliation time, post-discharge follow-up within policy, care-gap closure, outreach success, care-plan review timeliness, and outcome target attainment.

**Acceptance evidence:** Metric tests must prove numerator, denominator, exclusions, and time windows. Workbench analytics must expose measure definitions and drill-through records.

### 34. Clinician Burden and Task Appropriateness Controls

**Justification:** Poor coordination systems overload clinicians with administrative tasks or route clinical decisions to non-clinical users.

**Improvement:** Classify tasks by clinical decision, administrative coordination, patient outreach, evidence collection, and supervisor approval. Route tasks only to appropriate roles and track clinician-review burden.

**Acceptance evidence:** Tests must reject routing clinical decision tasks to unauthorized roles and report clinician-review workload in analytics.

### 35. Care Plan Review Cadence Automation

**Justification:** Care plans become stale unless review cadence is enforced based on risk and condition.

**Improvement:** Add review schedules driven by risk tier, transition status, outcome trend, unresolved barriers, and policy. Open review tasks, escalate overdue reviews, and mark whether the review changed the care plan.

**Acceptance evidence:** Tests must prove reviews are scheduled, skipped only with approved reason, and escalated when overdue. UI must show next review due date and staleness.

### 36. Multi-Program Coordination

**Justification:** Patients may be enrolled in multiple programs that conflict or overlap: chronic care, behavioral health, maternal care, oncology navigation, or social support.

**Improvement:** Add program enrollment evidence, program-specific goals, coordinator ownership, conflicting task detection, shared outcome measures, and program exit reasons. Keep ownership inside this PBC for coordination records only.

**Acceptance evidence:** Tests must prove overlapping programs can share a patient timeline without duplicating care gaps or violating program-specific permissions.

### 37. Transition Medication, Equipment, and Service Readiness Checklist

**Justification:** Transition readiness depends on concrete supports, not just discharge status.

**Improvement:** Add readiness checklist categories for medications obtained, equipment delivered, home health scheduled, transportation arranged, caregiver prepared, follow-up booked, warning signs taught, and emergency plan understood.

**Acceptance evidence:** Tests must block high-risk transition closure when readiness checklist items are missing and policy requires them. Workbench must display missing readiness evidence prominently.

### 38. Coordination Data Retention and Legal Hold

**Justification:** Coordination records include sensitive evidence and must support retention, amendment, and legal hold rules.

**Improvement:** Add retention category, legal hold flag, amendment history, deletion eligibility, export restriction, and redaction profile to coordination records and documents.

**Acceptance evidence:** Tests must prove legal hold blocks deletion, retention policies are tenant-scoped, and exports apply redaction profiles.

### 39. Assistant Draft Quality Scoring

**Justification:** The chatbot should draft care-plan updates and referral summaries, but users need confidence, missing evidence, and risk explanation.

**Improvement:** Score assistant drafts for source evidence coverage, clinical ambiguity, missing required fields, patient preference conflicts, policy compliance, and required reviewer role. Display the score before approval.

**Acceptance evidence:** Tests must prove low-confidence drafts require review, unsupported claims are flagged, and every accepted assistant draft emits audit evidence.

### 40. Coordination-Specific Natural Language Commands

**Justification:** Generic CRUD commands are insufficient for coordinators who use phrases like “close the loop,” “reconcile the consult,” or “open a post-discharge watch.”

**Improvement:** Add natural language skill intents for open referral, schedule follow-up, close care gap, record outreach, reconcile result, update transition plan, add barrier, create care conference, and escalate patient safety exception.

**Acceptance evidence:** Intent tests must map domain phrases to safe command previews and reject ambiguous instructions. The assistant must always show patient, entity, action, and evidence before mutation.

### 41. Patient-Level Dependency Freshness

**Justification:** A patient coordination summary can be misleading if consumed policy, identity, eligibility, or supplier/provider qualification events are stale.

**Improvement:** Score freshness for consumed events and projections affecting each patient. Display stale dependency warnings on care plans, referrals, and transitions with the last event time and fallback behavior.

**Acceptance evidence:** Tests must simulate stale consumed events and prove the workbench warns users while commands either block or require override according to policy.

### 42. Coordinated Bulk Outreach Campaigns

**Justification:** Care-gap closure and transition follow-up often require outreach to many patients while preserving individualized consent and preferences.

**Improvement:** Add bulk outreach campaign support for cohorts, with per-patient channel selection, exclusion rules, interpreter needs, retry cadence, response capture, and care-gap update mapping.

**Acceptance evidence:** Tests must show campaigns generate individual outreach records, respect consent, avoid duplicate contacts, and update care gaps only after patient-specific evidence.

### 43. Clinical Handoff Summary Generation

**Justification:** Specialists, discharge teams, and community partners need concise handoff summaries that include only relevant coordination evidence.

**Improvement:** Generate handoff summaries from care plan, referral status, transition readiness, barriers, recent outreach, outcome trends, and unresolved tasks. Include redaction rules and recipient-specific scope.

**Acceptance evidence:** Tests must prove summaries differ by recipient permission and include source references. The assistant can draft summaries but must not send them without confirmation.

### 44. Care Plan Conflict Detection

**Justification:** Multiple plans and referrals can create conflicting instructions, duplicate outreach, or incompatible appointments.

**Improvement:** Detect conflicts between care-plan interventions, referral instructions, transition tasks, patient preferences, and care-team ownership. Create conflict records with suggested resolution paths.

**Acceptance evidence:** Tests must prove conflicts are detected, false positives can be suppressed with reason, and approved resolutions update affected records through audited commands.

### 45. Patient Navigation Pathway Templates

**Justification:** Common pathways such as post-discharge, oncology navigation, pregnancy care, complex chronic care, and behavioral health require repeatable but configurable coordination patterns.

**Improvement:** Add pathway templates with default goals, tasks, review cadence, referral types, outcome measures, education items, and escalation rules. Templates should instantiate care plans while preserving patient-specific edits.

**Acceptance evidence:** Tests must instantiate multiple pathways, verify required tasks, and prove template version remains attached to generated care-plan items.

### 46. Outcome-Driven Closure Review

**Justification:** Closing tasks without confirming outcomes can make coordination look complete while patient goals remain unmet.

**Improvement:** Require closure review that checks outcome measures, open barriers, unresolved referrals, patient understanding, and care-team signoff before closing major care-plan goals or transition plans.

**Acceptance evidence:** Tests must reject closure when required outcome or barrier evidence is missing and allow policy-approved exceptions with audit proof.

### 47. Coordinator Workload Balancing

**Justification:** Uneven workload creates safety risk and missed follow-up.

**Improvement:** Track coordinator caseload by risk-adjusted patient count, overdue items, active transitions, urgent referrals, outreach tasks, and coverage absences. Recommend reassignment while preserving care-team accountability.

**Acceptance evidence:** Tests must calculate workload scores and produce reassignment suggestions without directly changing ownership until approved.

### 48. Patient-Reported Update Intake

**Justification:** Patients and caregivers often provide updates about symptoms, barriers, appointments, or medication issues between encounters.

**Improvement:** Add patient-reported update intake with category, urgency, free-text summary, structured extracted details, attachment evidence, triage decision, and linked care-plan or transition action.

**Acceptance evidence:** Tests must parse patient-reported updates, triage urgent updates, and require clinical review for safety-sensitive content.

### 49. Full Coordination Release Simulation

**Justification:** Release readiness should prove a complete patient coordination story, not isolated unit behavior.

**Improvement:** Add an end-to-end release simulation: high-risk patient admitted, transition plan opened, medication discrepancy found, referral ordered, care gap identified, outreach completed, barrier resolved, outcome measured, and care plan revised.

**Acceptance evidence:** The simulation must run side-effect-free in package tests, emit AppGen-X evidence, verify owned-table boundaries, and produce workbench projections for each step.

### 50. Composition DSL and Agent Skill Completeness

**Justification:** In composed applications, this PBC must expose its care coordination abilities through DSL and the unified application agent, not only package-local Python functions.

**Improvement:** Extend the composition metadata for `clinical_care_coordination` to express owned tables, APIs, events, UI fragments, rules, parameters, agent skills, patient timeline projection, risk queues, and release gates. Include skill descriptions for care-plan update, referral closure, transition watchlist, outreach documentation, and result reconciliation.

**Acceptance evidence:** DSL generation tests must prove composed apps include the care coordination workbench, assistant skills, AppGen-X event contracts, and package-local runtime evidence without exposing stream-engine choices or shared-table dependencies.
