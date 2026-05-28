# Talent Acquisition and Onboarding PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `talent_onboarding`. The items are specific to requisition-to-day-one operations: job requisitions, approvals, budgets, skills, sourcing campaigns, candidates, consent, candidate profiles, stage history, duplicate checks, privacy requests, interviews, evaluations, scorecards, background checks, adjudication, adverse action, offers, compensation projections, onboarding tasks, equipment requests, access preload and welcome notification handoffs, provisioning, event reliability, UI workbenches, and agent-assisted hiring operations.

## Current Domain Evidence Used

- Domain purpose: job requisitions, candidates, consents, interview and evaluation evidence, background checks, offers, onboarding tasks, provisioning handoffs, event evidence, rules, parameters, configuration, UI fragments, and release validation from requisition through day-one employee provisioning.
- Owned boundary: requisitions, approvals, budgets, skills, sourcing campaigns, candidate sources, candidates, candidate consents, profiles, skills, stage histories, duplicate checks, privacy requests, interview plans/panels/schedules/feedback, evaluation evidence, scorecards, background checks, background packages, adjudications, adverse-action notices, offers, offer approvals, acceptances, compensation projections, onboarding tasks/templates/checklists, equipment requests, access preload projections, welcome notification projections, personnel identity projections, payroll worker projections, role projections, policy screenings, audit traces, candidate proofs, federation projections, carbon schedule windows, pipeline optimization, interview allocation, anomaly signals, candidate risk models, hiring forecasts, parsed instructions, seed data, schema extensions, controls, governed models, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: job requisition creation, candidate creation, candidate stage advancement, background check recording, offer extension and acceptance, onboarding task creation/completion, employee provisioning, AppGen-X inbox handling, rules, parameters, configuration, schema extensions, workbench, candidate proofs, policy screening, federation, identity verification, resilience drills, carbon-aware interviews, pipeline optimization, interview allocation, controls, governed models, and boundary verification.
- Existing events and dependencies: emits `EmployeeProvisioned` and `CandidateHired`; consumes `RoleChanged` and `WorkerIdentityVerified`; integrates with personnel, access, payroll, notification, identity, and audit packages only through declared APIs/projections.

## 50 Better-Than-World-Class Improvements

### 1. Requisition readiness gate

**Justification:** Weak requisitions produce poor candidate matches, approval rework, budget leakage, and onboarding failures.

**Improvement:** Add readiness checks for job title, department, manager, location, legal entity, worker type, headcount, budget, required skills, role projection, compensation range, opening reason, and approval status. Block opening until mandatory evidence is complete.

### 2. Requisition approval and headcount control

**Justification:** Hiring starts a financial and organizational commitment, so approvals must prove headcount, budget, and manager authority.

**Improvement:** Model approval routing by requisition type, manager, department, location, budget threshold, backfill/new headcount, and worker type. Store approval decisions, rejection reasons, delegated approvals, and policy version.

### 3. Requisition budget governance

**Justification:** Recruiting without budget evidence creates offer delays and compensation exceptions.

**Improvement:** Track budget source, approved range, currency, compensation projection, headcount allocation, expiry, and change history. Offer extension should reconcile against requisition budget.

### 4. Skill requirement taxonomy

**Justification:** Poorly defined skills produce biased screening, inconsistent interviews, and bad matches.

**Improvement:** Model required, preferred, trainable, certification, proficiency, and evidence expectations for each skill. Candidate scoring and interviews should cite skill definitions and avoid free-form ambiguity.

### 5. Sourcing campaign governance

**Justification:** Sourcing strategy affects candidate quality, cost, diversity, time-to-fill, and compliance.

**Improvement:** Add campaign goals, channels, target markets, budget, diversity objectives, consent language, source attribution, campaign dates, and effectiveness metrics. Campaigns should link to requisitions and candidate sources.

### 6. Candidate source attribution

**Justification:** Candidate source drives cost attribution, vendor performance, referral rewards, and compliance reporting.

**Improvement:** Track source type, campaign, referrer/vendor, attribution confidence, first/last source, duplicate source conflict, and fee/referral eligibility. Preserve source lineage through hire.

### 7. Candidate capture completeness

**Justification:** Candidate records without identity, consent, skills, location, eligibility, and source evidence cannot be safely processed.

**Improvement:** Add candidate readiness checks for identity, contact, country, work authorization indicator, source, consent, resume/profile, skills, desired location, availability, and privacy notices. Incomplete candidates should remain in intake.

### 8. Candidate consent lifecycle

**Justification:** Recruiting data requires consent, purpose limitation, withdrawal, and retention controls.

**Improvement:** Model consent with purpose, source, language version, jurisdiction, capture timestamp, expiry, withdrawal, allowed processing, and downstream effects. Candidate actions should require current consent evidence.

### 9. Candidate privacy request workflow

**Justification:** Candidates can request access, correction, deletion, restriction, portability, or consent withdrawal.

**Improvement:** Add privacy request lifecycle with identity verification, scope, due date, affected records, legal hold, deletion/anonymization action, response evidence, and exception reasons.

### 10. Duplicate candidate detection

**Justification:** Duplicate candidates fragment stage history, interview feedback, consent, source attribution, and offer controls.

**Improvement:** Detect duplicates using email, phone, external profile, resume fingerprints, identity proofs, source identifiers, and semantic profile similarity. Route ambiguous duplicates to review with merge/split evidence.

### 11. Candidate profile enrichment

**Justification:** Profiles need structured, verified evidence rather than raw resumes.

**Improvement:** Extract education, experience, skills, certifications, work authorization, location, compensation expectations, availability, and portfolio evidence with confidence and reviewer approval. Keep raw documents linked but not authoritative.

### 12. Stage state machine

**Justification:** Candidate pipeline stages must be deterministic and policy-compliant from application to provisioning or rejection.

**Improvement:** Implement allowed transitions for application, screen, interview, assessment, background check, offer, accepted, hired, rejected, withdrawn, and provisioned. Store actor, reason, timestamp, policy hash, and candidate communication readiness.

### 13. Fair screening controls

**Justification:** Screening recommendations can create bias or unlawful exclusion if opaque.

**Improvement:** Add screening scorecards with job-related criteria, evidence, weights, adverse-impact monitoring, explainability, reviewer override, and prohibited-attribute exclusion. Require human review for rejection recommendations.

### 14. Interview plan design

**Justification:** Interviews should measure job requirements consistently without overburdening candidates or interviewers.

**Improvement:** Build interview plans with competencies, structured questions, evaluation rubric, required panel roles, sequence, duration, accommodation needs, and evidence requirements. Plans should align to requisition skills.

### 15. Interview panel allocation

**Justification:** Panel choice affects fairness, availability, expertise, load, and candidate experience.

**Improvement:** Allocate interviewers by skill coverage, role, seniority, availability, conflict-of-interest, diversity goals, workload, and training status. Show why panelists are selected or rejected.

### 16. Interview scheduling resilience

**Justification:** Scheduling failures slow hiring and damage candidate experience.

**Improvement:** Add scheduling states, timezone handling, candidate availability, interviewer conflicts, reschedule reasons, SLA, reminders, no-show handling, and carbon-aware remote/in-person tradeoffs.

### 17. Structured feedback quality

**Justification:** Interview feedback must be timely, job-related, comparable, and defensible.

**Improvement:** Add feedback completeness checks, rubric scoring, evidence fields, prohibited-content detection, late feedback escalation, calibration, and confidence. Block stage advancement when mandatory feedback is missing.

### 18. Evaluation evidence chain

**Justification:** Hiring decisions require traceable evidence across screens, interviews, assessments, checks, and offers.

**Improvement:** Create an evaluation evidence chain with source, competency, score, evaluator, confidence, timestamp, candidate visibility policy, and audit hash. Scorecards should cite evidence rather than summaries alone.

### 19. Candidate scorecard explainability

**Justification:** Scorecards influence hire/no-hire decisions and must be explainable and fair.

**Improvement:** Build scorecards with job-related dimensions, required skill coverage, interview feedback, assessment evidence, check status, risk flags, calibration, and decision rationale. Show sensitivity to weight changes.

### 20. Background check package governance

**Justification:** Background checks vary by role, location, country, customer access, and regulatory requirements.

**Improvement:** Define check packages by role, jurisdiction, worker type, access level, and customer/regulatory exposure. Store provider, required checks, consent, expiry, and policy version.

### 21. Background check adjudication

**Justification:** Check results require nuanced, fair, and legally controlled review.

**Improvement:** Add adjudication states, result type, confidence threshold, relevance to role, reviewer, adverse-action eligibility, candidate response, decision reason, and audit evidence. Avoid automatic disqualification for ambiguous results.

### 22. Adverse-action notice workflow

**Justification:** Some jurisdictions require notice, waiting period, evidence, and candidate response before adverse decisions.

**Improvement:** Model notices with reason, check reference, notice date, waiting period, response deadline, candidate response, final decision, and proof of delivery. Stage transitions should respect adverse-action status.

### 23. Offer readiness gate

**Justification:** Offers should not be extended until requisition, budget, candidate, checks, compensation, and approvals are ready.

**Improvement:** Check requisition status, budget, candidate stage, consent, check adjudication, compensation projection, offer approval policy, start date, and onboarding dependencies before offer extension.

### 24. Compensation projection governance

**Justification:** Offers require compensation data without payroll table access.

**Improvement:** Store compensation projection with range, currency, pay frequency, variable pay, equity/bonus references, benefits eligibility, source, approval, and freshness. Offer approvals should cite projection evidence.

### 25. Offer approval workflow

**Justification:** Offers create binding commitments and can exceed budget, policy, or equity controls.

**Improvement:** Add approval routing by amount, role, location, compensation variance, exception reason, relocation/sign-on terms, and hiring manager authority. Preserve approvals and reapproval triggers for changed offers.

### 26. Offer acceptance and expiry control

**Justification:** Acceptance status drives onboarding, provisioning, payroll setup, and communication.

**Improvement:** Track offer sent, viewed, accepted, declined, expired, rescinded, renegotiated, and withdrawn states with timestamps, candidate signature evidence, start date, and dependency triggers.

### 27. Candidate communication readiness

**Justification:** Hiring operations require communication but must preserve notification package boundaries.

**Improvement:** Generate communication-ready facts for interview invites, feedback requests, offer messages, adverse notices, onboarding reminders, and welcome sequences. Handoff via declared notification projections, not shared notification tables.

### 28. Onboarding checklist generation

**Justification:** Day-one readiness depends on role, location, worker type, jurisdiction, equipment, access, payroll, and compliance tasks.

**Improvement:** Generate checklists from task templates, role projections, location, worker type, start date, equipment needs, compliance documents, and access requirements. Show why each task is included.

### 29. Onboarding task SLA management

**Justification:** Late tasks cause day-one failures, access gaps, equipment delays, and payroll setup issues.

**Improvement:** Track task owner, due date, dependency, SLA, blocker, completion evidence, escalation, exception reason, and downstream provisioning impact. Workbench should rank tasks by day-one risk.

### 30. Equipment request lifecycle

**Justification:** Equipment readiness affects onboarding and requires coordination without sharing procurement or asset tables.

**Improvement:** Model equipment requests with role need, location, due date, approved device type, delivery status projection, exception, and receipt evidence. Preserve handoff boundary to procurement/asset packages.

### 31. Access preload governance

**Justification:** New hires need access on day one, but premature or excessive access creates security risk.

**Improvement:** Generate access preload requests with role, start date, manager, location, least-privilege bundles, approval, expiry, and activation condition. Use declared access APIs/projections only.

### 32. Personnel identity provisioning handoff

**Justification:** Talent must hand off hire facts cleanly to personnel identity without writing employee master tables.

**Improvement:** Generate provisioning payloads with candidate identity, accepted offer, start date, role, manager, location, consent/privacy scope, and proof hash. Emit `CandidateHired` and `EmployeeProvisioned` idempotently.

### 33. Payroll worker projection handoff

**Justification:** Payroll readiness starts during onboarding but payroll remains a separate package.

**Improvement:** Produce payroll worker projection handoffs with pay group, compensation projection, start date, legal entity, bank readiness status, and missing setup tasks. Do not write payroll-owned tables.

### 34. Candidate proof generation

**Justification:** Auditors may need proof of eligibility, consent, checks, offer, and hire decision without full candidate file disclosure.

**Improvement:** Generate redacted candidate proofs for consent, stage, evaluation, check, offer, acceptance, and provisioning status with hashes, policy version, and verification API.

### 35. Immutable talent audit trace

**Justification:** Hiring records are legally sensitive and must be reconstructable.

**Improvement:** Hash-chain requisition changes, approvals, candidate capture, consent, stages, interviews, feedback, checks, adjudications, offers, tasks, provisioning, agent previews, and event handling.

### 36. Talent policy screening

**Justification:** Hiring actions must comply with country, worker type, consent, background check, offer, retention, and provisioning policies.

**Improvement:** Screen requisition, candidate creation, stage movement, interview scheduling, check adjudication, offer, onboarding task, and provisioning actions. Store policy version, attributes evaluated, decision, explanation, and override route.

### 37. Hiring pipeline analytics

**Justification:** Recruiters need real-time pipeline health across requisitions, sources, stages, interviews, offers, and onboarding.

**Improvement:** Add analytics for funnel conversion, cycle time, source quality, stage aging, interview load, offer acceptance, onboarding SLA, diversity proxy safeguards, and requisition risk. Cite source records and freshness.

### 38. Hiring forecast and capacity model

**Justification:** Talent teams need to anticipate hiring demand, cycle time, recruiter load, and onboarding capacity.

**Improvement:** Forecast time-to-fill, interview demand, offer acceptance, background check delay, task workload, and provisioning risk by role, location, source, and season. Include confidence and drift evidence.

### 39. Candidate risk model governance

**Justification:** Match, attrition, compliance, and exception models influence candidate treatment and must be governed.

**Improvement:** Add model registry, feature lineage, training windows, approval status, explainability, fairness/adverse-impact checks, drift monitoring, rollback, and release evidence for every talent model.

### 40. Talent anomaly detection

**Justification:** Abnormal hiring patterns can indicate fraud, bias, integration defects, or process breakdown.

**Improvement:** Detect anomalies in source spikes, duplicate candidates, stage loops, feedback delays, offer exceptions, check failures, task overdue clusters, and provisioning retries. Route to review with explanations.

### 41. Stochastic hiring exposure model

**Justification:** Hiring exposure spans compliance, attrition, cycle time, offer decline, check delay, onboarding failure, and provisioning risk.

**Improvement:** Model exposure by requisition, candidate, role, location, source, stage, and start date. Provide mitigation actions and confidence intervals.

### 42. AppGen-X event reliability cockpit

**Justification:** Talent onboarding depends on role and identity events and emits candidate/hire provisioning events.

**Improvement:** Add inbox/outbox/dead-letter panels for idempotency, duplicates, retries, handler version, payload lineage, projection freshness, replay eligibility, and downstream provisioning effects.

### 43. Boundary proof for talent ownership

**Justification:** Talent must integrate with personnel, payroll, access, notifications, recruiting providers, and audit without shared tables.

**Improvement:** Add static/runtime checks proving commands touch only talent-owned tables plus AppGen-X runtime tables. Include failing fixtures for direct personnel, payroll, access, notification, provider, and audit table access.

### 44. Talent workbench coverage

**Justification:** Recruiters, coordinators, managers, HR, and auditors need the full hiring and onboarding surface in UI.

**Improvement:** Expand UI into requisition console, sourcing campaigns, candidate intake, consent/privacy, pipeline board, duplicate review, interview planning, scheduling, feedback, scorecards, checks, adverse action, offer board, onboarding tasks, equipment, provisioning, analytics, rules, parameters, configuration, events, and agent panels.

### 45. Agent-safe candidate document intake

**Justification:** The talent_onboarding chatbot should parse resumes, job descriptions, interview notes, check results, offer instructions, and onboarding documents without unsafe writes.

**Improvement:** Add intake skills that extract candidate/requisition facts, map them to owned tables, validate rules/permissions/privacy, reject foreign-table mutations, and produce side-effect-free previews with confidence, risks, approvals, and expected AppGen-X events.

### 46. Agent-safe hiring and onboarding planning

**Justification:** AI can improve recruiter throughput only if decisions remain human-reviewed and policy-bound.

**Improvement:** Require agent plans for requisitions, candidate stages, interviews, checks, offers, tasks, and provisioning to list command, permission, owned tables, idempotency key, emitted event, candidate impact, privacy basis, rollback limits, and human approval.

### 47. Carbon-aware interview and onboarding scheduling

**Justification:** Interview and onboarding logistics can reduce travel and energy while preserving candidate experience.

**Improvement:** Add carbon-aware scheduling for interviews, onboarding sessions, equipment delivery windows, and non-urgent tasks with remote/in-person tradeoffs, fairness constraints, and candidate preference.

### 48. Resilience drills for screening and provisioning

**Justification:** Background providers, identity verification, access preload, and notification routes fail during active hiring.

**Improvement:** Add drills for provider outage, duplicate event, identity verification delay, notification failure, provisioning retry, dead-letter replay, and offer expiry handling. Store drill evidence in release gates.

### 49. Talent onboarding readiness score

**Justification:** Users need an evidence-backed view of whether the package is ready for production hiring operations.

**Improvement:** Compute readiness from requisition setup, approval rules, consent policy, candidate capture, interview workflows, check packages, offer controls, onboarding templates, provisioning handoffs, event reliability, UI coverage, boundary proof, controls, model governance, and agent safety.

### 50. End-to-end hire-to-provision proof

**Justification:** A complete Talent Onboarding PBC must prove it can run the full lifecycle from approved requisition to day-one provisioning.

**Improvement:** Add an executable proof scenario covering requisition, approval, sourcing, candidate capture, consent, screening, interview, background check, offer, acceptance, onboarding tasks, access preload, personnel/payroll projections, emitted `CandidateHired` and `EmployeeProvisioned`, UI evidence, controls, and agent explanation.
