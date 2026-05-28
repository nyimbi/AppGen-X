# Legal Matter Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `legal_matter_management`. Each item is specific to legal operations and matter management: intake, classification, parties, counsel, budgets, legal holds, custodians, deadlines, filings, documents, privilege, evidence, invoices, settlement, legal risk, outside counsel governance, and agent-assisted legal work. The intent is to move the PBC beyond table-stakes matter tracking into a complete, specialist-grade legal operating system while preserving AppGen-X package boundaries.

## Current Domain Evidence Used

- Domain purpose: owns legal matters, parties, counsel, budgets, holds, filings, deadlines, documents, invoices, risk, privilege controls, and matter lifecycle intelligence.
- Owned tables include matter, party, counsel, budget, budget line, legal hold, hold custodian, deadline, filing, document, privilege review, outside counsel invoice, task, risk assessment, settlement offer, outcome, exception, policy rule, parameter, schema extension, control assertion, governed model, outbox, inbox, and dead-letter evidence tables.
- Operations include `open_legal_matter`, `register_matter_party`, `assign_counsel`, `create_matter_budget`, `capture_budget_line`, `issue_legal_hold`, `register_hold_custodian`, `track_matter_deadline`, `record_filing`, `attach_matter_document`, `review_document_privilege`, `ingest_counsel_invoice`, `create_matter_task`, `score_matter_risk`, `record_settlement_offer`, and `close_matter_outcome`.
- Events include `LegalMatterOpened`, `LegalHoldIssued`, `MatterDeadlineTracked`, `FilingRecorded`, `MatterRiskChanged`, and `MatterClosed`; consumed events include supplier, invoice, policy, and audit proof signals.
- Existing advanced claims include legal deadline risk prediction, semantic document privilege triage, case exposure simulation, outside counsel spend intelligence, cryptographic hold evidence, and policy-aware settlement routing.

## 50 Better-Than-World-Class Improvements

### 1. Matter Intake Triage and Legal Taxonomy Engine

**Justification:** Legal operations fail early when intake captures free-text requests without normalizing jurisdiction, matter type, urgency, privilege sensitivity, business unit, regulatory exposure, and related contracts or disputes. A world-class PBC must classify legal work before tasks, counsel, budgets, or holds are created.

**Improvement:** Add an intake triage engine for `open_legal_matter` that applies configurable legal taxonomies, question sets, required evidence, jurisdiction rules, urgency scoring, duplicate matter detection, and escalation paths. The UI should provide guided intake forms, document upload prompts, agent-assisted summarization, and a confidence-ranked matter classification with human override and audit evidence.

### 2. Conflict-of-Interest and Related-Party Screening

**Justification:** Assigning internal or outside counsel without checking adverse parties, affiliates, former clients, witnesses, and business relationships creates legal and ethical risk. The current party registration surface needs specialist conflict controls.

**Improvement:** Extend `register_matter_party` and `assign_counsel` with conflict screening records, adverse-party aliases, beneficial owner projections, former representation flags, waiver tracking, wall requirements, and counsel eligibility decisions. Emit review tasks when conflicts are unresolved and block counsel assignment until waiver or clearance evidence is recorded.

### 3. Matter Type Playbooks

**Justification:** Litigation, employment, IP, regulatory, privacy, real estate, tax, commercial, and investigation matters require different phases, deadlines, documents, approvals, and risk models. A generic matter lifecycle underserves every legal team.

**Improvement:** Create configurable matter playbooks that instantiate phase templates, tasks, filing checklists, hold requirements, budget categories, document sets, approval gates, and agent guidance by matter type and jurisdiction. The workbench should show playbook progress, missing artifacts, rule exceptions, and expected next actions.

### 4. Jurisdiction and Venue Intelligence

**Justification:** Deadlines, filing formats, court calendars, service rules, preservation duties, counsel authorization, and settlement approval thresholds vary by jurisdiction and venue. Without explicit jurisdiction intelligence, the PBC cannot safely manage legal work.

**Improvement:** Add jurisdiction and venue profiles with local calendars, deadline computation rules, permitted filing methods, service constraints, venue-specific document requirements, local counsel rules, and holiday calendars. Link every deadline and filing to the applicable rule version and make agent recommendations cite the governing profile.

### 5. Legal Hold Scope Builder

**Justification:** Legal holds must be precise enough to preserve relevant material while avoiding overbroad retention and unnecessary operational burden. A simple hold record is insufficient for serious discovery, investigation, or regulatory matters.

**Improvement:** Expand `issue_legal_hold` with a hold scope builder covering custodians, systems, date ranges, data categories, keywords, business processes, preservation rationale, hold notices, acknowledgements, reminders, escalations, and release criteria. Provide UI simulations of affected custodians and repositories before issuance.

### 6. Custodian Interview and Acknowledgement Workflow

**Justification:** Hold effectiveness depends on defensible custodian communication, acknowledgement, follow-up, and interview evidence. Matter teams need more than a custodian list.

**Improvement:** Add custodian interview templates, acknowledgement records, non-response escalation, delegated acknowledgement, interview notes, preservation certifications, exception reasons, and re-issue tracking. The agent should draft custodian-specific notices from matter context and require approval before sending.

### 7. Defensible Preservation Evidence Ledger

**Justification:** Preservation disputes often turn on proof that legal hold instructions, scope changes, acknowledgements, and release decisions were timely and unaltered. Standard audit timestamps are too weak for high-stakes legal operations.

**Improvement:** Create cryptographic hash chains for hold issuance, notice delivery, acknowledgement, custodian changes, scope amendments, and releases. Surface an evidence export package with event hashes, actor identities, policy versions, delivery receipts, and dead-letter retry history for audit and court-ready preservation proof.

### 8. Deadline Computation and Calendar Assurance

**Justification:** Missed limitation periods, court deadlines, response windows, filing cutoffs, and renewal dates can create catastrophic risk. Deadlines cannot be treated as ordinary tasks.

**Improvement:** Upgrade `track_matter_deadline` with computed deadlines, source-trigger events, rule citations, jurisdiction calendars, timezone handling, business-day adjustments, dependency chains, review assignments, deadline confidence, and dual-control approval for critical dates. The UI should provide a legal deadline calendar with risk heatmaps and upcoming obligation queues.

### 9. Deadline Change Propagation

**Justification:** A continuance, filing rejection, court order, amended contract, policy change, or jurisdiction holiday can alter multiple linked deadlines. Manual updates invite inconsistency.

**Improvement:** Add dependency graphs between triggering events, filings, service dates, response dates, appeal windows, tolling periods, and renewal obligations. When a source date changes, the PBC should compute proposed changes, show impacted matters, require approval, and emit `MatterDeadlineTracked` updates with reasoned evidence.

### 10. Court and Regulator Filing Dossier Management

**Justification:** Filing readiness involves forms, exhibits, signatures, service lists, fees, confidentiality markings, page limits, venue rules, and rejection handling. A basic filing record does not cover real legal workflows.

**Improvement:** Extend `record_filing` with filing dossier checklists, exhibit binders, signature status, filing fee records, service method, confidentiality designation, submission receipts, rejection reasons, corrective actions, and final acceptance evidence. The workbench should show filing readiness and block submission when required elements are missing.

### 11. Service-of-Process Tracking

**Justification:** Service failures can invalidate proceedings or extend risk exposure. Legal matter management must track who was served, how, when, by whom, and under what rule.

**Improvement:** Add service-of-process records for parties, agents, delivery attempts, affidavits, returned mail, publication service, substituted service, proof status, and challenge windows. Link service events to filings, deadlines, party status, and agent-generated reminders.

### 12. Document Set and Evidence Binder Assembly

**Justification:** Matters require structured document sets, not just attachments: pleadings, correspondence, evidence, privileged material, work product, contracts, expert reports, transcripts, orders, and settlement drafts each need different handling.

**Improvement:** Expand `attach_matter_document` with document set types, binder ordering, exhibit numbers, Bates ranges, source provenance, confidentiality level, privilege status, admissibility notes, chain-of-custody metadata, and version lineage. The UI should support matter binders, evidence maps, and exportable production packages.

### 13. Privilege Review Workbench

**Justification:** Privilege review is a specialist legal workflow involving attorney-client privilege, work product, common interest, waiver risk, redaction, clawback, and review consistency. Generic document review is not enough.

**Improvement:** Enhance `review_document_privilege` with privilege reason codes, reviewer tiers, redaction instructions, waiver risk flags, privilege log fields, challenge status, clawback protocol references, sampling queues, and review consistency analytics. The agent should suggest privilege classifications with citations to facts, not final legal determinations without review.

### 14. Privilege Log Generation and Challenge Tracking

**Justification:** Legal teams must produce defensible privilege logs and respond to challenges. Missing metadata or inconsistent descriptions can waive protections.

**Improvement:** Add privilege log generation by matter, production set, jurisdiction, and protective order. Track document family handling, redacted descriptions, privilege basis, authors, recipients, dates, withheld status, challenge responses, meet-and-confer outcomes, and court ruling impact.

### 15. Chain-of-Custody Evidence Control

**Justification:** Investigations, litigation, claims, and regulatory matters require defensible evidence custody from collection through analysis, production, and return or destruction.

**Improvement:** Introduce chain-of-custody records with collector identity, source system, collection method, hash, transfer events, storage location, access logs, tamper checks, retention status, and disposition instructions. The UI should highlight custody gaps and evidence integrity anomalies.

### 16. eDiscovery Collection Request Orchestration

**Justification:** Legal holds do not automatically collect data. Teams need collection requests, custodian scopes, search terms, system owners, status, exceptions, and quality checks.

**Improvement:** Add collection request objects tied to legal holds and matter documents. Track sources, custodians, query criteria, export formats, chain-of-custody hashes, collection completeness, exception handling, and handoff events to discovery review tools through declared APIs or AppGen-X events.

### 17. Outside Counsel Panel Governance

**Justification:** Counsel assignment depends on jurisdiction, practice area, conflict status, diversity commitments, rate cards, performance, capacity, language, and matter complexity. A counsel table alone cannot optimize legal service delivery.

**Improvement:** Extend `assign_counsel` with counsel panel eligibility, practice specialization, jurisdiction admission, rate arrangements, staffing rules, diversity metrics, conflict clearance, capacity, prior outcomes, and scorecards. The UI should compare recommended firms and explain selection tradeoffs.

### 18. Engagement Letter and Scope Control

**Justification:** Outside counsel work must be governed by approved scope, billing terms, staffing limits, reporting obligations, confidentiality, and matter budgets. Without scope control, spend and risk drift.

**Improvement:** Add engagement records with approved scope, prohibited activities, staffing plan, rate card, alternative fee terms, reporting cadence, deliverables, conflicts waivers, confidentiality terms, and change-order approvals. Block invoice lines outside engagement scope unless an exception is approved.

### 19. Legal Budget Phase and Task Codes

**Justification:** Matter budgets need legal-specific phase, task, activity, expense, jurisdiction, and fee arrangement dimensions. A flat budget line cannot support spend control or benchmarking.

**Improvement:** Expand `create_matter_budget` and `capture_budget_line` with phase/task/activity codes, blended rate assumptions, fee caps, accrual estimates, reserves, holdbacks, contingency terms, currency handling, forecast curves, and variance thresholds. The workbench should compare budget, committed spend, billed spend, approved spend, and forecast exposure.

### 20. Outside Counsel Invoice Compliance Review

**Justification:** Counsel invoices require review for billing guidelines, block billing, duplicate entries, staffing violations, unauthorized expenses, rate mismatches, and budget overruns. Generic invoice ingestion misses legal spend leakage.

**Improvement:** Upgrade `ingest_counsel_invoice` with line-level compliance checks, billing guideline rules, rate validation, timekeeper authorization, task-code matching, duplicate detection, narrative quality scoring, expense policy checks, adjustment workflows, and counsel feedback loops.

### 21. Legal Accrual and Reserve Management

**Justification:** Legal matters often require accruals, reserves, probable loss estimates, settlement exposure, insurance recoveries, and finance-facing evidence. Legal and finance teams need controlled projections without shared table mutation.

**Improvement:** Add package-local reserve and accrual projections linked to matter risk, budget, settlement, and invoice records. Publish AppGen-X events for approved reserve changes and consume finance policy signals through read-only projections while preserving `legal_matter_management` ownership.

### 22. Case Exposure Modeling

**Justification:** Leadership needs realistic exposure ranges, not only static risk labels. Exposure changes as facts, procedural posture, insurance, defenses, venue, judge, opposing counsel, and settlement offers evolve.

**Improvement:** Extend `simulate_case_exposure` with probabilistic outcome ranges, best/base/worst scenarios, legal theory weighting, damages categories, defense offsets, insurance recovery, counterclaim exposure, litigation cost forecast, and confidence explanations. Store model metadata and human overrides in governed model evidence.

### 23. Settlement Strategy and Offer Ledger

**Justification:** Settlement decisions require controlled tracking of demands, offers, authority, concessions, confidentiality terms, non-monetary obligations, payment timing, releases, and board or executive approvals.

**Improvement:** Expand `record_settlement_offer` with demand/offer history, negotiation rounds, authorized limits, settlement terms, release conditions, payment schedule, non-monetary commitments, confidentiality clauses, tax considerations, and approval evidence. Show a negotiation timeline and decision rationale in the UI.

### 24. Settlement Approval Matrix

**Justification:** Settlement authority varies by amount, risk, jurisdiction, business unit, insurance involvement, public sensitivity, and precedent impact. Approval needs to be policy-aware.

**Improvement:** Implement configurable settlement approval matrices that route offers through legal, finance, risk, business owner, insurance, and executive reviewers based on thresholds and matter attributes. The agent should explain required approvers and block final acceptance until policy conditions are satisfied.

### 25. Matter Risk Taxonomy and Heatmap

**Justification:** Legal risk spans financial exposure, injunctive risk, regulatory risk, operational disruption, reputational harm, privilege risk, precedent risk, and criminal or personal liability. A single risk score hides critical nuance.

**Improvement:** Add a multi-dimensional risk taxonomy to `score_matter_risk` with independent scores, trend, confidence, drivers, controls, mitigations, owner, and escalation thresholds. Provide portfolio heatmaps by business unit, jurisdiction, matter type, counsel, and risk driver.

### 26. Early Warning Signals

**Justification:** Matter deterioration often appears through missed tasks, adverse rulings, budget variance, discovery issues, deadline compression, privilege challenges, counsel performance, or new facts before formal risk updates.

**Improvement:** Create early warning detection from matter events, deadlines, filings, invoice narratives, task aging, privilege queue metrics, settlement movement, and agent-ingested instructions. Generate explainable alerts, recommended mitigations, and event-backed risk changes.

### 27. Investigation Matter Support

**Justification:** Internal investigations require allegation intake, whistleblower protection, interview planning, evidence collection, confidentiality, findings, remediation, and non-retaliation controls. They differ from ordinary litigation matters.

**Improvement:** Add investigation-specific matter playbooks with allegation taxonomy, interview lists, witness status, investigation plan, evidence requests, finding categories, remediation tasks, escalation criteria, and restricted-access partitions. Surface an investigation workbench with sensitive access controls.

### 28. Regulatory Inquiry and Examination Workflow

**Justification:** Regulatory matters involve requests, response deadlines, production sets, issue lists, regulator communications, privilege positions, remediation commitments, and recurring reporting obligations.

**Improvement:** Add regulatory inquiry records for request items, response owners, production status, regulator contacts, commitments, follow-up requests, deficiency notices, and remediation links. Track regulator-specific deadlines and publish status events without mutating compliance or audit tables.

### 29. IP Matter Lifecycle Support

**Justification:** Intellectual property matters need invention disclosures, patent deadlines, trademark renewals, office actions, prosecution history, licensing links, enforcement posture, and portfolio strategy.

**Improvement:** Add IP-specific extensions for asset identifiers, prosecution deadlines, office actions, renewal dates, classes, jurisdictions, inventors, ownership chain, enforcement actions, and licensing dependencies. The UI should expose IP matter calendars and asset-linked matter portfolios.

### 30. Employment and Labor Matter Support

**Justification:** Employment matters require employee identities, allegations, accommodations, investigations, agency charges, grievance stages, settlement tax treatment, confidentiality, and reinstatement or policy-remediation obligations.

**Improvement:** Add employment matter templates with allegation types, protected-class sensitivity, agency charge tracking, grievance steps, witness lists, remediation commitments, reinstatement constraints, settlement terms, and restricted access. Integrate only through declared HR projections and events.

### 31. Contract Dispute and Obligation Linkage

**Justification:** Many matters arise from contract obligations, notices, warranties, indemnities, service levels, termination rights, and breach allegations. The legal PBC needs linked context without owning contract tables.

**Improvement:** Add package-local contract dispute projections that reference contract identifiers, obligation snapshots, notice requirements, cure periods, indemnity status, limitation clauses, and dispute milestones. Consume contract events and expose read-only legal dispute views.

### 32. Insurance Coverage and Recovery Tracking

**Justification:** Insurance notice, reservation of rights, defense cost recovery, deductibles, coverage positions, and insurer approvals materially affect matter strategy and reserves.

**Improvement:** Add insurance coverage records with policy references, notice dates, coverage positions, defense-cost eligibility, retention/deductible status, insurer counsel requirements, recovery estimates, and claim correspondence. Link coverage impacts to exposure, budget, and settlement approval workflows.

### 33. Expert Witness and Consultant Management

**Justification:** Expert and consultant work involves retention approvals, conflict checks, scope, reports, deposition dates, fee controls, privilege boundaries, and disclosure deadlines.

**Improvement:** Add expert/consultant profiles, engagement scope, discipline, conflict status, report deadlines, deposition schedule, disclosure status, budget lines, privilege classifications, and deliverable tracking. The UI should show expert readiness and disclosure risk.

### 34. Witness and Interview Management

**Justification:** Witness handling requires role, relationship, availability, interview history, statement status, credibility, confidentiality constraints, and contact restrictions.

**Improvement:** Add witness records linked to parties and custodians, with interview schedules, topics, notes, statement versions, privilege status, credibility factors, contact permissions, and follow-up tasks. Agent-generated interview outlines should be saved as drafts requiring legal approval.

### 35. Protective Order and Confidentiality Compliance

**Justification:** Protective orders control designations, access, redactions, production handling, filing under seal, challenges, and destruction or return obligations.

**Improvement:** Add protective-order records, confidentiality designations, access groups, challenge windows, seal filing requirements, production restrictions, and disposition obligations. Enforce document access and production workflows based on designation rules.

### 36. Legal Task Dependency Graph

**Justification:** Matter tasks are often dependent on filings, court rulings, evidence collection, counsel review, approvals, service, and settlement events. Flat task lists conceal critical path risk.

**Improvement:** Upgrade `create_matter_task` with dependency graphs, blockers, prerequisites, legal phase links, required artifacts, critical path indicators, and aging rules. The UI should show matter boards, phase timelines, and task-risk propagation.

### 37. Matter Timeline and Procedural History

**Justification:** Legal teams need a reliable chronological story of facts, communications, filings, decisions, offers, rulings, evidence, and deadlines. The current timeline needs to become authoritative.

**Improvement:** Build a matter timeline projection combining opened matters, parties, counsel assignments, holds, filings, deadlines, documents, invoices, risk changes, settlement offers, and closure events. Include filters for procedural, factual, financial, evidence, and privileged events.

### 38. Communications and Correspondence Register

**Justification:** Legal correspondence with parties, counsel, courts, regulators, insurers, and business owners must be tracked for privilege, deadlines, negotiation posture, and evidence.

**Improvement:** Add correspondence records with sender, recipients, channel, subject, privilege status, confidentiality designation, related deadline, response obligation, attachments, and business context. The agent should summarize correspondence and suggest follow-up tasks after confirmation.

### 39. Matter Closure and Lessons-Learned Workflow

**Justification:** Closing a matter requires final disposition, settlement performance, release of holds, final invoices, document retention, lessons learned, control improvements, and residual obligations.

**Improvement:** Expand `close_matter_outcome` with closure checklists, final exposure, outcome type, root cause, legal spend summary, hold release requirements, retention instructions, settlement obligation tracking, policy feedback, and lessons-learned reports. Prevent closure when mandatory downstream obligations remain open.

### 40. Hold Release and Data Disposition Controls

**Justification:** Holding data forever creates cost, privacy, and compliance risk, while premature release creates spoliation risk. Hold release must be explicit and defensible.

**Improvement:** Add release workflows for legal holds with release rationale, affected custodians, systems, residual matters, retention conflicts, disposition instructions, notice delivery, acknowledgement, and evidence hashes. Require policy checks before release and publish approved release events.

### 41. Legal Operations KPI and Portfolio Analytics

**Justification:** Legal leaders need portfolio views across matter volume, cycle time, spend, exposure, counsel performance, deadline risk, hold burden, privilege workload, settlement outcomes, and recurring root causes.

**Improvement:** Build analytics surfaces for matter aging, spend variance, exposure trend, counsel scorecards, deadline adherence, hold acknowledgement, filing rejection rates, privilege throughput, settlement efficiency, and closure outcomes. Include drilldowns that remain inside owned state or declared projections.

### 42. Outside Counsel Performance Scorecards

**Justification:** Legal service quality must be measured across outcomes, responsiveness, budget discipline, staffing compliance, diversity, innovation, risk management, and invoice quality.

**Improvement:** Create counsel scorecards tied to assignments, invoices, budgets, deadlines, outcomes, matter complexity, and feedback. Use these scores in counsel recommendations and panel governance while retaining manual selection authority.

### 43. Rule and Parameter Studio for Legal Policies

**Justification:** Legal teams need configurable intake, hold, deadline, privilege, budget, settlement, confidentiality, and closure policies without code changes.

**Improvement:** Expand matter policy rules and runtime parameters into a legal policy studio with versioning, simulation, approval workflow, effective dates, test cases, rollback, exception handling, and release evidence. The agent should explain rule impact before activation.

### 44. Sensitive Matter Access Partitions

**Justification:** Some matters require need-to-know isolation for investigations, executives, acquisitions, insider issues, employment claims, privileged strategy, or regulated proceedings.

**Improvement:** Add sensitive matter partitions with explicit access groups, ethical walls, field-level masking, agent tool restrictions, export controls, audit alerts, and break-glass procedures. Ensure UI, APIs, and assistant responses honor partition rules.

### 45. Agent-Assisted Document and Instruction Intake

**Justification:** Legal users frequently provide emails, notices, pleadings, contracts, invoices, regulator letters, or verbal instructions that must become structured matter updates without unsafe autonomous writes.

**Improvement:** Give the PBC agent skills to parse uploaded documents and instructions into proposed matters, parties, holds, deadlines, filings, tasks, privilege reviews, invoice issues, and settlement updates. The agent must show source-grounded extraction, confidence, policy warnings, affected tables, AppGen-X events, and a confirmation step before CRUD execution.

### 46. Legal Drafting Assistance with Governance

**Justification:** Legal teams benefit from drafting support for notices, hold letters, status reports, filing summaries, settlement memos, and counsel instructions, but drafts require governance and traceability.

**Improvement:** Add governed drafting workflows that generate drafts from matter context, approved templates, jurisdiction rules, and policy constraints. Store draft lineage, source citations, reviewer approvals, privilege designation, export status, and prohibitions against sending without human approval.

### 47. Cross-PBC Projection Boundary Enforcement

**Justification:** Legal matters naturally reference suppliers, customers, employees, contracts, invoices, assets, insurance, audit controls, and finance records. The PBC must avoid shared-table coupling while still giving complete context.

**Improvement:** Implement explicit projection contracts for external context, including source PBC, external identifier, snapshot time, fields allowed, freshness, consent or access basis, and fallback behavior. Add tests proving legal services mutate only `legal_matter_management_` tables and communicate externally through APIs, events, or projections.

### 48. Release Evidence Packs for Legal Defensibility

**Justification:** Legal systems need proof that schemas, rules, events, handlers, access controls, holds, deadlines, privilege reviews, and agent actions behaved as designed at release time.

**Improvement:** Generate release evidence packs containing schema hashes, migration manifests, route contracts, service contracts, event schemas, handler idempotency proofs, retry/dead-letter tests, access-control matrices, policy test outcomes, agent skill manifests, and representative matter smoke runs.

### 49. Matter Scenario Simulation and Strategy Board

**Justification:** Legal strategy requires scenario planning across outcomes, costs, deadlines, settlement timing, reputational effects, precedent risk, operational burden, and probability changes.

**Improvement:** Add a strategy board where users can model litigation, regulatory, investigation, IP, employment, and contract dispute scenarios. Compare expected cost, exposure, time to resolution, operational impact, settlement options, required approvals, and key assumptions with saved scenario versions.

### 50. Complete Legal Workbench Coverage

**Justification:** If advanced capabilities are hidden behind APIs, legal users cannot operate the PBC effectively. The UI must surface the full legal domain, not only matter lists.

**Improvement:** Expand the workbench into role-specific views for general counsel, matter owner, paralegal, legal operations, outside counsel coordinator, privilege reviewer, investigator, and executive sponsor. Include intake, matter detail, parties, counsel, holds, custodians, deadlines, filings, documents, privilege logs, evidence binders, budgets, invoices, risks, settlements, policies, analytics, agent drafts, and release-evidence status.
