# Education Student Lifecycle PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `education_student_lifecycle` with a hand-curated student success and academic progression roadmap. The PBC owns student applicants, enrollments, curriculum plans, advising cases, course attempts, assessment results, credentials, governed rules, agent assistance, and release evidence without owning finance aid, learning-management content, identity master records, or alumni advancement tables.

## Current Domain Evidence Used

- Stable PBC key: `education_student_lifecycle`.
- Domain purpose: admissions, enrollment, curriculum, advising, progression, assessment, credentials, and student outcomes.
- Owned domain tables: `student_applicant`, `enrollment`, `curriculum_plan`, `advising_case`, `course_attempt`, `assessment_result`, `credential`, `education_student_lifecycle_policy_rule`, `education_student_lifecycle_runtime_parameter`, `education_student_lifecycle_schema_extension`, `education_student_lifecycle_control_assertion`, `education_student_lifecycle_governed_model`.
- Public APIs: `POST /student-applicants`, `POST /enrollments`, `POST /curriculum-plans`, `POST /advising-cases`, `POST /course-attempts`, `GET /education-student-lifecycle-workbench`.
- Emitted AppGen-X events: `EducationStudentLifecycleCreated`, `EducationStudentLifecycleUpdated`, `EducationStudentLifecycleApproved`, `EducationStudentLifecycleExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.

## 50 High-Impact Improvements

### 1. Applicant Lifecycle State Machine

**Justification:** Admissions work spans inquiry, application, document review, decision, offer, acceptance, deferral, waitlist, and withdrawal states.

**Improvement:** Add applicant states with application round, program choice, required documents, decision status, offer conditions, acceptance deadline, and withdrawal reason.

**Acceptance evidence:** Tests must reject invalid applicant transitions and show missing application evidence before decision.

### 2. Admissions Requirement Rules

**Justification:** Programs have different prerequisites, documents, exams, interviews, portfolios, and minimum standards.

**Improvement:** Add requirement profiles by program, intake, applicant type, residency, prior credential, and exception policy.

**Acceptance evidence:** Tests must evaluate complete, incomplete, exception, and rejected applicant scenarios by program.

### 3. Document and Transcript Intake

**Justification:** Student records are document-heavy and require source traceability.

**Improvement:** Add document evidence with type, issuing institution, received date, authenticity status, extracted fields, confidence, reviewer, and accepted values.

**Acceptance evidence:** Tests must block high-impact document-derived mutations until reviewer confirmation.

### 4. Enrollment Lifecycle

**Justification:** Enrollment includes admitted, matriculated, active, leave, withdrawn, suspended, completed, and graduated states.

**Improvement:** Expand `enrollment` with status reason, effective date, program, campus, modality, load, cohort, catalog year, and readmission link.

**Acceptance evidence:** Tests must preserve enrollment history and prevent course registration when enrollment is inactive or blocked.

### 5. Program and Curriculum Plan Versioning

**Justification:** Degree requirements change by catalog year, program, concentration, accreditation, and transfer rules.

**Improvement:** Add curriculum plan versions with requirement groups, electives, prerequisites, substitutions, waivers, effective windows, and approval.

**Acceptance evidence:** Tests must evaluate students against the plan version attached to their catalog year.

### 6. Degree Audit Engine

**Justification:** Students and advisors need a precise view of completed, in-progress, planned, missing, waived, and substituted requirements.

**Improvement:** Add audit results by requirement, course attempt, assessment result, transfer credit, waiver, substitution, and remaining credit.

**Acceptance evidence:** Tests must produce accurate degree audit states and flag conflicting substitutions.

### 7. Course Attempt Lifecycle

**Justification:** A course attempt can be registered, waitlisted, dropped, withdrawn, completed, repeated, excluded, or transferred.

**Improvement:** Expand `course_attempt` with section projection, grade mode, attempt number, repeat rule, withdrawal date, credit earned, and transcript visibility.

**Acceptance evidence:** Tests must calculate earned credits and repeat treatment correctly.

### 8. Prerequisite and Corequisite Checks

**Justification:** Course registration must respect prerequisites, corequisites, placement, program restrictions, and override approvals.

**Improvement:** Add rule evaluation with missing requirement, override request, approver, expiry, and audit trace.

**Acceptance evidence:** Tests must block registration without satisfied prerequisites unless a valid override exists.

### 9. Academic Standing Calculation

**Justification:** Standing decisions affect progression, probation, suspension, honors, and graduation eligibility.

**Improvement:** Add standing rules for GPA, credit completion, failed attempts, progress pace, remediation terms, and appeal.

**Acceptance evidence:** Tests must compute good standing, warning, probation, suspension, and reinstatement states.

### 10. GPA and Credit Calculation

**Justification:** GPA and credit rules vary by grade mode, repeated courses, transfer work, withdrawals, and program policy.

**Improvement:** Add calculation basis, grade points, attempted credits, earned credits, included/excluded flags, and transcript period.

**Acceptance evidence:** Tests must calculate term, cumulative, program, and credential GPA variants.

### 11. Advising Case Taxonomy

**Justification:** Advising cases include academic planning, risk intervention, transfer, graduation, conduct referral, accessibility support, and re-enrollment.

**Improvement:** Expand `advising_case` with type, urgency, owner, student goal, barrier, action plan, next contact, and closure evidence.

**Acceptance evidence:** Tests must route cases by type and prevent closure without documented outcome.

### 12. Student Success Risk Model

**Justification:** Early warning needs attendance, course performance, missed milestones, advising history, holds, engagement, and external support signals.

**Improvement:** Add explainable risk scores with contributing factors, confidence, intervention recommendation, and review cadence.

**Acceptance evidence:** Tests must generate risk cases and require human review before high-impact interventions.

### 13. Intervention Plan Tracking

**Justification:** Student support is effective only when interventions are assigned, followed up, and measured.

**Improvement:** Add intervention records with objective, owner, due date, student commitment, resource referral, outcome, and next step.

**Acceptance evidence:** Tests must create intervention tasks and measure completion/outcome.

### 14. Assessment Result Governance

**Justification:** Assessment results drive progression, competency, accreditation, and credentials.

**Improvement:** Expand `assessment_result` with assessment type, rubric, scorer, score, competency mapping, moderation status, appeal, and finalization.

**Acceptance evidence:** Tests must block credential completion when required assessments are missing or unfinalized.

### 15. Competency and Outcome Mapping

**Justification:** Programs increasingly certify outcomes and competencies beyond course credits.

**Improvement:** Add competency framework, mapped assessments, achievement level, evidence, remediation, and credential requirement linkage.

**Acceptance evidence:** Tests must show competency progress and identify unmet outcomes.

### 16. Credential Award Lifecycle

**Justification:** Credentials require audits, approvals, conferral dates, honors, transcript notation, and revocation/correction handling.

**Improvement:** Expand `credential` with credential type, audit status, approver, conferral date, honors, certificate number, correction, and revocation reason.

**Acceptance evidence:** Tests must block conferral until curriculum, standing, assessment, and financial/administrative hold projections satisfy policy.

### 17. Graduation Clearance Workbench

**Justification:** Graduation clearance involves requirements, applications, holds, advisor approval, and registrar signoff.

**Improvement:** Add queues for pending audits, missing requirements, unresolved holds, advisor review, registrar approval, and credential issuance.

**Acceptance evidence:** UI tests must prove each queue maps to owned records or declared projections.

### 18. Student Holds Boundary

**Justification:** Financial, conduct, immunization, library, and administrative holds may be owned elsewhere but affect enrollment actions.

**Improvement:** Store hold projections with type, source, effective date, blocking actions, freshness, and override policy.

**Acceptance evidence:** Boundary tests must fail on external hold table reads and pass on declared event/API projections.

### 19. Transfer Credit Evaluation

**Justification:** Transfer work needs equivalencies, articulation, credit limits, grade rules, and program applicability.

**Improvement:** Add transfer evaluation records with source institution, course, credit, equivalency, applicability, evaluator, and appeal state.

**Acceptance evidence:** Tests must apply transfer credit to curriculum audits and preserve evaluator evidence.

### 20. Prior Learning Assessment

**Justification:** Work experience, military training, certifications, and portfolios can satisfy requirements with controlled evidence.

**Improvement:** Add prior-learning evidence, assessment method, evaluator, credit awarded, competency mapping, and expiration.

**Acceptance evidence:** Tests must require approval and show how prior learning affects degree audit.

### 21. Enrollment Capacity and Waitlist Boundary

**Justification:** Course capacity and seat management may be owned by scheduling systems, but student lifecycle needs registration outcome evidence.

**Improvement:** Store section capacity projection, waitlist position, permission code, registration result, and freshness.

**Acceptance evidence:** Tests must handle waitlist promotion and stale capacity projections safely.

### 22. Attendance and Engagement Projection

**Justification:** Engagement signals help advisors intervene but may originate in learning systems.

**Improvement:** Add engagement projections with source, attendance rate, last activity, missing work flag, risk contribution, and privacy scope.

**Acceptance evidence:** Tests must use engagement evidence without reading learning-management tables.

### 23. International Student Compliance

**Justification:** International students may have visa, load, address, employment, and reporting obligations.

**Improvement:** Add compliance profile, required load, address confirmation, leave restrictions, reporting event, and escalation.

**Acceptance evidence:** Tests must flag noncompliance and block incompatible enrollment changes when policy requires.

### 24. Accessibility Accommodation Boundary

**Justification:** Accommodations affect assessment and enrollment but sensitive records may be owned elsewhere.

**Improvement:** Store accommodation projection with permitted adjustments, effective window, privacy classification, and stale-data warning.

**Acceptance evidence:** Permission tests must hide sensitive accommodation detail while enforcing allowed academic actions.

### 25. Academic Petition Workflow

**Justification:** Students request waivers, substitutions, late drops, overloads, reinstatement, and exceptions.

**Improvement:** Add petition type, requested exception, evidence, committee review, decision, conditions, appeal, and expiration.

**Acceptance evidence:** Tests must apply approved petitions to curriculum and enrollment rules.

### 26. Student Communication Timeline

**Justification:** Advising, admissions, progression, and credential decisions require documented communication.

**Improvement:** Add communication events with template, channel, recipient, purpose, linked case, delivery status, and response.

**Acceptance evidence:** Tests must emit notification events and preserve student-lifecycle timeline evidence.

### 27. Enrollment and Progression Timeline

**Justification:** Staff need a longitudinal view from applicant to credential.

**Improvement:** Build timeline projection for application, admission, enrollment, course attempts, assessments, advising, holds, petitions, and credential events.

**Acceptance evidence:** Replay tests must reconstruct timelines idempotently with permission-aware redaction.

### 28. Cohort and Retention Analytics

**Justification:** Institutions need cohort retention, persistence, progression, completion, and outcome metrics.

**Improvement:** Add analytics projections by cohort, program, term, demographic projection, entry pathway, risk band, and intervention exposure.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with low-count suppression.

### 29. Equity and Access Monitoring

**Justification:** Student outcomes should be monitored for disparities without exposing unnecessary protected data.

**Improvement:** Add equity metrics, protected-data projection boundary, disparity threshold, review task, and remediation plan.

**Acceptance evidence:** Tests must produce disparity indicators with privacy-preserving aggregation.

### 30. Curriculum Change Impact

**Justification:** Program changes can affect enrolled students, applicants, graduation timelines, and advising load.

**Improvement:** Add impact simulation for requirement changes, course retirements, prerequisite changes, credit changes, and substitution rules.

**Acceptance evidence:** Tests must produce affected-student lists and block activation without impact evidence.

### 31. Advising Workbench

**Justification:** Advisors need prioritized queues rather than raw student records.

**Improvement:** Add workbench views for high-risk students, missing requirements, upcoming registration blockers, petitions, graduation candidates, and inactive outreach.

**Acceptance evidence:** UI tests must prove each queue maps to owned data or declared projections with permission-aware actions.

### 32. Admissions Workbench

**Justification:** Admissions teams need actionable queues for incomplete applications, review-ready files, interviews, decisions, offers, and yield outreach.

**Improvement:** Add admissions persona views with aging, requirements, reviewer assignment, decision readiness, and offer acceptance risk.

**Acceptance evidence:** UI tests must validate queue counts and action permissions.

### 33. Agent-Assisted Student Guidance

**Justification:** The assistant should help students and staff understand progress without inventing academic advice.

**Improvement:** Add agent skills for degree audit explanation, registration blocker summary, advising case summary, petition draft, graduation readiness, and applicant checklist.

**Acceptance evidence:** Tests must require citations and mark recommendations that need advisor confirmation.

### 34. Governed Agent CRUD Commands

**Justification:** Chat-driven student lifecycle changes must be previewed and authorized.

**Improvement:** Add command previews for create advising case, update curriculum plan, apply petition, record assessment, change enrollment status, and award credential.

**Acceptance evidence:** Intent tests must require student identity, evidence, preview, confirmation, authority, and audit trail.

### 35. Privacy and FERPA-Like Redaction

**Justification:** Student records require role-based minimum necessary access.

**Improvement:** Add redaction profiles for applicant reviewer, advisor, instructor, registrar, student self-service, auditor, and analytics user.

**Acceptance evidence:** Permission tests must hide sensitive fields and block unauthorized exports.

### 36. Data Retention and Amendment

**Justification:** Academic records need retention, amendment history, legal hold, and transcript correction controls.

**Improvement:** Add retention class, amendment reason, original value, corrected value, approver, legal hold, and export eligibility.

**Acceptance evidence:** Tests must block deletion under retention and preserve correction history.

### 37. Continuous Control Assertions

**Justification:** Student lifecycle quality needs controls over admissions decisions, enrollment status, degree audits, petitions, credentials, and privacy.

**Improvement:** Add controls with population, threshold, failing records, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and require remediation proof.

### 38. Dead-Letter and Retry Operations

**Justification:** Applicant documents, enrollment events, assessment results, holds, and credential events can fail.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue.

**Acceptance evidence:** Tests must replay failed events without duplicate enrollments, credentials, or notifications.

### 39. Cryptographic Academic Record Proofs

**Justification:** Credentials, transcripts, and decisions need tamper-evident evidence.

**Improvement:** Add hash chains for application decisions, enrollment changes, course attempts, assessments, petitions, and credentials.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 40. Credential Verification Contract

**Justification:** External verification should confirm credential facts without exposing full student records.

**Improvement:** Add verification API/event contract with credential identifier, conferral date, status, revocation flag, and proof reference.

**Acceptance evidence:** Contract tests must return scoped verification evidence and preserve privacy.

### 41. Student Outcome Tracking

**Justification:** Programs need evidence of completion, employment, further study, licensure, and competency outcomes.

**Improvement:** Add outcome records with source, date, category, confidence, linked credential/program, and aggregation scope.

**Acceptance evidence:** Tests must track outcomes without overwriting alumni or employer-system ownership.

### 42. Accreditation Evidence

**Justification:** Accrediting bodies require proof of curriculum, assessment, progression, completion, and outcomes.

**Improvement:** Add evidence packets by program, cohort, outcome, assessment, credential, and reporting period.

**Acceptance evidence:** Tests must generate scoped evidence packets with source links and redaction.

### 43. Multi-Campus and Multi-Program Support

**Justification:** Students can move across campuses, modalities, programs, concentrations, and credentials.

**Improvement:** Add campus, modality, program hierarchy, dual enrollment, primary program, secondary credential, and residency transitions.

**Acceptance evidence:** Tests must evaluate progression correctly for dual and transferred program paths.

### 44. Leave, Withdrawal, and Reinstatement

**Justification:** Stops and returns affect progression, billing boundaries, visa compliance, and credential timelines.

**Improvement:** Add leave type, withdrawal reason, effective date, return conditions, reinstatement petition, and transcript notation.

**Acceptance evidence:** Tests must preserve status history and enforce return conditions.

### 45. Seeded Student Lifecycle Scenario Library

**Justification:** Release audits need realistic student journeys.

**Improvement:** Add seeds for applicant admission, transfer credit, advising risk, petition approval, course repeat, graduation audit, credential conferral, and privacy-restricted record.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and evidence packets.

### 46. Role-Based Permission Model

**Justification:** Applicants, students, advisors, admissions staff, instructors, registrars, compliance users, and auditors need different authority.

**Improvement:** Add permissions for applicant review, enrollment change, curriculum override, advising note, assessment finalization, credential award, and export.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 47. Financial Aid and Billing Boundary

**Justification:** Student status affects aid and billing, but those domains own money and awards.

**Improvement:** Emit enrollment status, credit load, satisfactory-progress, credential, and withdrawal events with idempotency keys and evidence.

**Acceptance evidence:** Boundary tests must fail on finance table writes and pass on declared AppGen-X event contracts.

### 48. Full Student Lifecycle Release Simulation

**Justification:** A complete PBC must prove applicant-to-credential behavior end to end.

**Improvement:** Add a simulation where an applicant applies, is admitted, enrolls, follows a curriculum plan, receives advising, completes assessments, earns credits, petitions a substitution, and receives a credential.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate financial aid, course catalog ownership, learning content, identity master data, or alumni advancement.

**Improvement:** Add overlap checks and dependency contracts for identity, holds, course sections, learning engagement, aid eligibility, billing status, and alumni outcomes.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose student lifecycle capabilities through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for applicants, enrollments, curriculum plans, advising, course attempts, assessments, credentials, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include student lifecycle models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
