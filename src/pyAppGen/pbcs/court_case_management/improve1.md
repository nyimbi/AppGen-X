# Court Case Management Improvement Backlog

This backlog replaces the prior scaffold with one hand-crafted, court-specific set of improvements for the `court_case_management` PBC.

## Current Domain Evidence Used

- Exact manifest key: `pbc: 'court_case_management'`.
- Description: `Filings, hearings, dockets, parties, judgments, orders, calendars, and court operations`.
- Tables: `court_case`, `filing`, `hearing`, `docket_entry`, `party`, `judgment`, `court_order`, `court_case_management_policy_rule`, `court_case_management_runtime_parameter`, `court_case_management_schema_extension`, `court_case_management_control_assertion`, `court_case_management_governed_model`.
- APIs: `POST /court-cases`, `POST /filings`, `POST /hearings`, `POST /docket-entrys`, `POST /partys`, `GET /court-case-management-workbench`.
- Workflows: `court_case_management_create_court_case_workflow`, `court_case_management_record_filing_workflow`.
- UI fragments: `CourtCaseManagementWorkbench`, `CourtCaseManagementDetail`, `CourtCaseManagementAssistantPanel`.
- Docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.
- Emits: `CourtCaseManagementCreated`, `CourtCaseManagementUpdated`, `CourtCaseManagementApproved`, `CourtCaseManagementExceptionOpened`.
- Consumes: `PolicyChanged`, `CustomerUpdated`, `SupplierQualified`.
- Analytics: `court_case_management_risk_score`, `court_case_management_workbench_metric`.
- Advanced capabilities already declared: `court_case_management_event_sourced_operational_history`, `court_case_management_multi_tenant_policy_isolation`, `court_case_management_schema_evolution_resilience`, `court_case_management_autonomous_anomaly_detection`, `court_case_management_semantic_document_instruction_understanding`, `court_case_management_predictive_risk_scoring`, `court_case_management_counterfactual_scenario_simulation`, `court_case_management_cryptographic_audit_proofs`, `court_case_management_continuous_control_testing`, `court_case_management_cross_pbc_event_federation`, `court_case_management_governed_ai_agent_execution`.

## Backlog

### 1. Canonical case numbering and venue assignment

**Justification:** Clerks need one durable identity for each matter before filings, hearings, orders, and appellate activity can be tracked without duplicate jackets or venue confusion.

**Improvement:** Add court-, division-, year-, and sequence-aware case numbering with transfer lineage, original filing venue, current venue, and reason-for-transfer fields on `court_case`.

**Acceptance evidence:** Case creation tests prove unique numbers per venue policy, transfer scenarios preserve lineage, and `CourtCaseManagementDetail` shows original and current venue without manual notes.

### 2. Party roles, counsel, and representation history

**Justification:** Courts cannot manage service, motions, scheduling, or orders correctly unless plaintiffs, defendants, petitioners, respondents, intervenors, guardians, and counsel are modeled explicitly over time.

**Improvement:** Expand `party` to track role, representation status, lead counsel, self-represented flag, appearance date, withdrawal date, service address history, and alias names used in pleadings.

**Acceptance evidence:** Tests cover substitution of counsel, pro se conversion, withdrawn appearances, and multi-party cases; party views show current and prior representation history.

### 3. Filing intake with deficiency review

**Justification:** Filing acceptance is not a simple create call; clerks must identify missing signatures, wrong captions, fee issues, bad service references, and rejected document packages before the docket advances.

**Improvement:** Add intake states on `filing` for received, under clerk review, deficient, cured, accepted, rejected, and stricken, with deficiency codes and cure deadlines.

**Acceptance evidence:** Intake tests cover incomplete filings, cured re-submissions, and rejected packets; workbench queues separate accepted filings from clerk deficiencies awaiting action.

### 4. Amended and superseding filing lineage

**Justification:** Courts need to distinguish original pleadings from amended complaints, corrected motions, replacement exhibits, and withdrawn filings without losing the historical record.

**Improvement:** Add parent-child lineage between `filing` records, with amendment type, supersedes flag, strike status, and docket-note generation rules.

**Acceptance evidence:** Docket views show original and superseding filings in order, lineage tests prevent orphan amendments, and event history preserves what was operative at each point in time.

### 5. Docket chronology integrity and gap detection

**Justification:** The docket is the court’s procedural spine; missing sequence numbers, backdated entries, and hidden gaps undermine hearing preparation, appeal review, and public trust.

**Improvement:** Enforce immutable sequence ordering on `docket_entry`, require entry source and filing/order linkage, and add detection for chronology gaps, same-timestamp collisions, and backfill corrections.

**Acceptance evidence:** Tests reject invalid insertion sequences, correction flows preserve original entry numbers, and operators can see chronology warnings in `CourtCaseManagementWorkbench`.

### 6. Motion lifecycle and ruling queue

**Justification:** Motions drive much of court workload, but they are absent from the current owned tables and should not be buried as generic filings with no motion-specific deadlines or statuses.

**Improvement:** Add motion-specific extensions under `court_case_management_schema_extension` to track motion type, filing date, opposition due date, reply due date, hearing requirement, submission date, and ruling status.

**Acceptance evidence:** Motion queues show pending briefing and submitted-but-unruled motions, deadline tests fire correctly, and judges can filter by motion type and readiness.

### 7. Order drafting, signature, and issuance workflow

**Justification:** Drafting an order, routing it for judge review, signing it, and placing it on the docket is a distinct workflow from merely storing a `court_order` row.

**Improvement:** Add draft, under review, signed, entered, corrected, and vacated states to `court_order`, plus signature metadata, service linkage, and effective-date handling.

**Acceptance evidence:** Order workflow tests prove only signed orders can be entered, corrected orders preserve prior versions, and the docket references the entered order version actually in force.

### 8. Hearing scheduling with courtroom calendar controls

**Justification:** Hearing operations break down when calendars ignore courtroom availability, judge assignment, motion readiness, interpreter needs, or blackout dates.

**Improvement:** Extend `hearing` scheduling to include courtroom, session block, hearing type, assigned judge, calendar status, readiness prerequisites, interpreter requirement, and remote/in-person mode.

**Acceptance evidence:** Scheduling tests reject double-booked courtrooms and unavailable judges, and courtroom calendars show blocked, tentative, and confirmed hearing slots.

### 9. Continuance and reschedule management

**Justification:** Courts need to track why a hearing moved, who requested it, whether a continuance was granted, and which deadlines shifted as a result.

**Improvement:** Add continuance requests, grant/deny outcomes, continuance reasons, old/new dates, and deadline recalculation rules tied to affected `hearing` and `filing` records.

**Acceptance evidence:** Continuance scenarios update the calendar, preserve the prior setting, recalculate linked deadlines, and show continuance history on the case timeline.

### 10. Deadline and tickler engine for procedural dates

**Justification:** Missed filing, service, response, and appellate deadlines create immediate operational and legal risk, so deadline calculation needs to be first-class rather than manual.

**Improvement:** Introduce a deadline engine driven by `court_case_management_policy_rule` and `court_case_management_runtime_parameter` for response dates, briefing schedules, service due dates, order compliance dates, and appeal windows.

**Acceptance evidence:** Deadline tests cover weekends, holidays, extensions, continuances, and local-rule offsets; overdue items appear in the workbench with reasoned due-date calculations.

### 11. Service of process and proof-of-service tracking

**Justification:** The court cannot advance many matters until parties are served, but service attempts, completed service, defective service, and returned service need explicit operational states.

**Improvement:** Add service tracking under `court_case_management_schema_extension` for service method, attempted date, completed date, server identity, served party, proof-of-service document, and deficiency reason.

**Acceptance evidence:** Cases with unserved parties are flagged, proof-of-service uploads link back to the correct filing or order, and hearing readiness checks fail when required service is incomplete.

### 12. Summons and subpoena issuance controls

**Justification:** Clerks often issue summonses and subpoenas before service can occur, and those instruments need their own issuance, return, and cancellation history.

**Improvement:** Add issuance records tied to `filing` and `party` for summons and subpoena documents, including issue date, expiration date, served/not served status, and return metadata.

**Acceptance evidence:** Issuance tests prove one summons cannot be reused across unrelated parties, expired instruments are visible, and clerks can reissue with clear lineage.

### 13. Evidence exhibit chain of custody

**Justification:** Exhibit handling is central to hearings and trial preparation; the system needs to know which exhibit was lodged, marked, admitted, sealed, returned, or withdrawn.

**Improvement:** Add exhibit entities under `court_case_management_schema_extension` linked to `filing`, `hearing`, and `docket_entry`, with exhibit numbers, custody events, admission status, and storage location.

**Acceptance evidence:** Exhibit history is replayable from intake through disposition, hearing packets include admitted and pending exhibits, and chain-of-custody corrections never erase prior custody events.

### 14. Sealed and restricted record handling

**Justification:** Courts frequently manage sealed motions, sealed exhibits, juvenile records, and restricted party information that cannot appear on the public docket or general clerk views.

**Improvement:** Add sealed, restricted, public, and redacted access classes across `filing`, `docket_entry`, `court_order`, and exhibit records, with view and export policies enforced by permission and case context.

**Acceptance evidence:** Access tests show sealed items are invisible to unauthorized roles, redacted docket views omit restricted content, and access attempts are logged for later review.

### 15. Public docket versus internal docket projection

**Justification:** The same case often needs a public-facing docket and an internal docket with clerk notes, sealed references, and operational exceptions that cannot leak.

**Improvement:** Build separate read models for public and internal docket projections, each derived from the same event history but filtered by seal status, operational note visibility, and publication rules.

**Acceptance evidence:** Projection tests prove the public view excludes restricted entries while the internal view preserves them, and stale public projections raise visible warnings.

### 16. Minute entries and transcript readiness

**Justification:** After each hearing, clerks need to enter minutes, capture appearances, note rulings from the bench, and track transcript requests or transcript availability.

**Improvement:** Extend `hearing` and `docket_entry` handling to include minute-entry completion, appearances, on-record rulings, transcript ordered flag, transcript due date, and transcript filed date.

**Acceptance evidence:** Hearing completion workflows require minutes before final closure, transcript requests are visible on the case timeline, and docket entries reflect bench rulings and later transcript filings.

### 17. Judgment and disposition completeness

**Justification:** A matter is not operationally complete when `judgment` exists without disposition type, effective date, relief awarded, costs, post-judgment deadlines, or linkage to appealed issues.

**Improvement:** Expand `judgment` to capture disposition category, relief terms, effective date, monetary and non-monetary components, costs, compliance due dates, and appealability markers.

**Acceptance evidence:** Judgment screens show complete disposition summaries, tests cover multiple judgment types, and post-judgment deadlines are automatically created where policy requires them.

### 18. Appeal notice, stay, and mandate tracking

**Justification:** Courts must know when a notice of appeal is filed, whether enforcement is stayed, what record must be assembled, and when the appellate mandate returns.

**Improvement:** Add appellate workflow extensions tied to `court_case`, `judgment`, and `court_order` for notice of appeal date, appellate record packet status, stay status, transmission date, mandate date, and remand instructions.

**Acceptance evidence:** Appeal scenarios show notice-to-mandate status end to end, stay flags block conflicting enforcement steps, and appellate packet checklists are visible in the workbench.

### 19. Related case, consolidation, and companion matter handling

**Justification:** Courts often need to relate matters involving the same parties, facts, or orders without collapsing independent dockets unless consolidation is ordered.

**Improvement:** Add related-case and consolidation links on `court_case` with relation type, originating case, consolidation order reference, shared-hearing flags, and separation history after deconsolidation.

**Acceptance evidence:** Related-case searches show linked matters without duplicating records, consolidation preserves prior case identities, and shared proceedings are visible on both timelines.

### 20. Judge reassignment, recusal, and chambers handoff

**Justification:** Judge assignment changes affect calendars, ruling queues, deadlines, and order routing, so reassignment cannot be treated as a silent field update.

**Improvement:** Add assignment history on `court_case` and `hearing`, including assigned judge, reassignment reason, recusal indicator, chambers handoff time, and pending-matter transfer rules.

**Acceptance evidence:** Reassignment tests move only open work to the new chambers queue, prior rulings remain attributed correctly, and calendar ownership changes are reflected immediately.

### 21. Clerk intake workbench

**Justification:** Clerks need a focused workspace for reviewing incoming filings, correcting captions, issuing deficiency notices, and starting service-related follow-up.

**Improvement:** Add a clerk-oriented slice of `CourtCaseManagementWorkbench` that prioritizes intake batches, deficiency queues, fee or waiver checks, and issuance tasks tied to `court_case_management_record_filing_workflow`.

**Acceptance evidence:** Route tests show intake-specific filters and actions, permission checks hide judge-only actions, and queue metrics show pending and overdue clerk work.

### 22. Judge chambers workbench

**Justification:** Judges and chambers staff need a different operational view centered on motions under advisement, draft orders, upcoming hearings, and overdue rulings.

**Improvement:** Add a chambers workspace in `CourtCaseManagementWorkbench` with ruling queues, draft-order review, hearing prep packets, pending continuance decisions, and post-hearing follow-up.

**Acceptance evidence:** Chambers users can sort by oldest submitted motion and upcoming hearing date, draft-order actions require approval rights, and overdue-ruling alerts are visible.

### 23. Courtroom operations workbench

**Justification:** Day-of-court operations depend on a real-time view of the courtroom calendar, checked-in participants, interpreter readiness, exhibit availability, and minute-entry status.

**Improvement:** Add a courtroom operations workspace showing today’s `hearing` records by courtroom and session block, with readiness indicators for service, exhibits, participants, and minute capture.

**Acceptance evidence:** Courtroom views update hearing status in sequence, same-day continuances are visible immediately, and missing readiness items are highlighted before the session starts.

### 24. Case timeline and detail workbench

**Justification:** Staff should not stitch together procedural history from raw tables; the case detail page needs one coherent timeline for filings, motions, hearings, orders, service, exhibits, and appeals.

**Improvement:** Expand `CourtCaseManagementDetail` into a chronological case timeline with procedural filters, event grouping, sealed markers, and quick links to related orders, hearings, and appellate actions.

**Acceptance evidence:** Timeline tests show all major event types in sequence, filters work without losing chronology, and users can jump from a docket entry to its source filing or order.

### 25. Agent skill for filing triage

**Justification:** Clerk intake volume is high enough that governed agent assistance should identify caption errors, missing attachments, wrong filing categories, and likely deficiency notices before a human accepts the filing.

**Improvement:** Add a filing-triage skill in `CourtCaseManagementAssistantPanel` that reads proposed filing packets, suggests filing type, flags probable defects, and drafts deficiency notices without committing changes automatically.

**Acceptance evidence:** Assistant sessions show source citations to packet content, blocked mutations require human confirmation, and tests cover correct and incorrect triage recommendations.

### 26. Agent skill for hearing preparation packets

**Justification:** Chambers and courtroom staff need fast preparation packets that summarize pending motions, service status, exhibit readiness, prior orders, and unresolved procedural issues before a hearing.

**Improvement:** Add a hearing-prep skill that assembles hearing packets from `court_case`, `filing`, `hearing`, `docket_entry`, exhibit, and service data, with explicit citations back to the underlying record.

**Acceptance evidence:** Hearing packet output includes cited source records, sealed material is omitted for unauthorized roles, and preparation status is available directly from the workbench.

### 27. Agent skill for order draft summarization

**Justification:** Chambers staff often start from motion history, opposition papers, hearing notes, and prior orders; the assistant should reduce assembly time without issuing orders on its own.

**Improvement:** Add an order-draft support skill that summarizes briefing history, proposed rulings, prior related orders, and open compliance issues for a selected motion or hearing.

**Acceptance evidence:** Generated summaries cite the underlying docket items, never bypass `court_order` approval states, and clearly distinguish draft assistance from signed judicial action.

### 28. Agent skill for service deficiency follow-up

**Justification:** Service failures are repetitive, time-sensitive, and administratively heavy, making them a good candidate for governed task assistance.

**Improvement:** Add a service-follow-up skill that identifies parties lacking service, drafts outreach or notice text, proposes next review dates, and opens follow-up tasks when proof-of-service is overdue.

**Acceptance evidence:** Suggested actions stay inside permitted clerk workflows, overdue-service queues shrink in test scenarios, and every assistant-created task includes the triggering service defect.

### 29. API surface for court-specific commands and queries

**Justification:** The current API set is create-heavy and incomplete for a real court workload, and the route names `POST /docket-entrys` and `POST /partys` should not remain the only public shapes.

**Improvement:** Add explicit query and action APIs for docket search, motion queues, hearing calendars, continuances, service status, exhibit custody, appeals, and sealed-access review, while preserving backward compatibility for existing routes.

**Acceptance evidence:** API contract tests cover legacy and canonical aliases, query responses support case and courtroom filters, and route documentation records which endpoints are compatibility shims.

### 30. Typed event expansion for procedural milestones

**Justification:** Generic events such as `CourtCaseManagementUpdated` are too coarse to support reliable downstream reactions to filings, orders, service completion, hearing changes, or appeals.

**Improvement:** Add typed emitted events for filing accepted, filing rejected, hearing scheduled, hearing continued, order entered, judgment recorded, service completed, exhibit admitted, sealed record accessed, and appeal noticed.

**Acceptance evidence:** Event schemas are versioned, event examples are included in release evidence, and downstream consumers can subscribe without parsing generic state diffs.

### 31. Inbound event boundary handling

**Justification:** Consumed events must have narrow, visible effects on court data; unrelated upstream changes should not create silent mutations inside the case record.

**Improvement:** Define case-safe handlers for `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified` that only update court policy projections, external-party references, or exception queues where those events are explicitly relevant.

**Acceptance evidence:** Handler tests prove idempotency, non-relevant inbound events do not mutate case state, and exceptions link back to the triggering inbound event when action is required.

### 32. Duplicate filing detection and idempotent intake

**Justification:** Courts regularly receive re-submitted packets, duplicate uploads, and retry traffic from portals; intake must distinguish legitimate amendments from duplicates.

**Improvement:** Add idempotency keys and duplicate-detection heuristics on `filing` using case number, party, filing type, document hash, submitter, and submission window.

**Acceptance evidence:** Intake tests collapse repeated retries into one logical filing, amendments remain distinct, and duplicate alerts show the matched prior record and reason.

### 33. Local rules and courtroom policy configuration workbench

**Justification:** Deadline calculations, motion calendars, exhibit cutoffs, and filing requirements vary by judge, division, and court, so local rules need governed configuration rather than code edits.

**Improvement:** Use `court_case_management_policy_rule` and `court_case_management_runtime_parameter` to configure local procedural rules, judicial standing orders, courtroom blackout periods, and hearing slot policies in a dedicated configuration workbench.

**Acceptance evidence:** Local-rule changes are versioned, previewed before activation, attributable to an approver, and reflected in deadline calculations and calendar availability tests.

### 34. Motion and hearing dependency graph

**Justification:** Readiness for a hearing often depends on service completion, briefing completion, exhibit exchange, interpreter assignment, and prior orders that should be visible as one dependency graph.

**Improvement:** Build dependency relationships between `filing`, motion extensions, `hearing`, `court_order`, service records, and exhibits so staff can see what is still blocking a setting or ruling.

**Acceptance evidence:** Readiness checks identify specific blockers, dependency graphs update when prerequisite work closes, and hearings cannot move to confirmed status while required blockers remain open.

### 35. Courtroom resource scheduling

**Justification:** Courtroom calendars are not only about judges and rooms; interpreters, security, remote-video capacity, and exhibit presentation support can determine whether a hearing can proceed.

**Improvement:** Add courtroom resource reservations linked to `hearing` for interpreters, remote links, exhibit support, special accommodations, and courtroom-specific capacity constraints.

**Acceptance evidence:** Resource conflicts block confirmation, daily courtroom views show reserved support resources, and accommodation requirements are visible during scheduling.

### 36. Case-sensitive access control and action policy

**Justification:** Courts need finer control than generic read and update permissions because sealed matters, juvenile cases, judicial drafts, and clerk-only functions have different action boundaries.

**Improvement:** Extend permission enforcement beyond `court_case_management.read`, `court_case_management.create`, `court_case_management.update`, `court_case_management.approve`, and `court_case_management.admin` into action-level policies tied to role, case sensitivity, and record class.

**Acceptance evidence:** Policy tests cover clerk, judge, chambers, courtroom, and audit personas; unauthorized users cannot view sealed items or take judge-only actions; the UI removes blocked actions cleanly.

### 37. Audit proofs for sealed-record access

**Justification:** Restricted-record access must be provable after the fact, especially when chambers staff, clerks, or auditors view sealed filings, sealed exhibits, or redacted orders.

**Improvement:** Apply `court_case_management_cryptographic_audit_proofs` to sealed-access events so each view, export, and unseal action produces tamper-evident proof without exposing the underlying sealed content.

**Acceptance evidence:** Proof verification succeeds for sealed-access samples, release evidence includes a redacted proof example, and audit queries can answer who accessed a sealed item and when.

### 38. Release evidence pack for court operations

**Justification:** Court-facing releases need more than passing tests; each release should prove readiness for filings, hearings, docketing, service, orders, sealed records, and appeals.

**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations to include procedural scenario coverage, event and API contracts, sealed-access controls, deadline calculations, calendar conflict checks, and assistant governance evidence.

**Acceptance evidence:** Release packets include scenario matrices, event samples, API verification, UI screenshots or snapshots, control assertions, and sign-off records tied back to the PBC version.

### 39. Operational analytics for backlog, aging, and risk

**Justification:** Court leaders need visibility into filing backlog, overdue rulings, hearing utilization, service failures, appeal volume, and sealed-access anomalies, not just generic PBC metrics.

**Improvement:** Extend `court_case_management_workbench_metric` and `court_case_management_risk_score` to report aging by queue, continuance rates, hearing utilization, service completion lag, pending-motion backlog, and appellate throughput.

**Acceptance evidence:** Metrics definitions are documented, analytics queries are reproducible, and dashboards show drill-through from aggregated counts to affected cases.

### 40. Exception queues with procedural SLAs

**Justification:** Intake defects, failed service, missed deadlines, unsent orders, transcript delays, and stale appellate packets all need procedural SLA ownership rather than a generic exception bucket.

**Improvement:** Define exception classes and SLA timers for intake, service, calendaring, order issuance, transcript readiness, sealed-access review, and appellate record assembly.

**Acceptance evidence:** Exception queues display owner, age, due-by time, and escalation state; breach tests generate visible alerts; closed exceptions preserve remediation notes.

### 41. Bulk correction workflows for clerical fixes

**Justification:** Courts frequently need narrow clerical fixes such as correcting captions, adding omitted counsel, reclassifying filing types, or updating many hearing notices after a courtroom closure.

**Improvement:** Add bulk correction actions with preview, per-record validation, partial success handling, and correction lineage for `party`, `filing`, `hearing`, and `docket_entry`.

**Acceptance evidence:** Bulk-correction tests preserve audit history, partial failures do not roll back valid corrections, and users can export correction results for review.

### 42. Search across cases, captions, parties, and docket text

**Justification:** Clerks and chambers staff need to find matters by case number, caption fragment, party alias, filing type, hearing date, or order text without querying the database directly.

**Improvement:** Add indexed search and saved filters across `court_case`, `party`, `filing`, `docket_entry`, `hearing`, `judgment`, and `court_order`, with public and internal search scopes.

**Acceptance evidence:** Search tests cover case number, alias, caption, date, and filing-type queries; saved filters return stable results; sealed content remains excluded from unauthorized searches.

### 43. Cross-case party matching and alias resolution

**Justification:** Repeated litigants, agencies, and counsel appear under inconsistent spellings, making service tracking, related-case detection, and workload analytics unreliable.

**Improvement:** Add governed alias resolution and cross-case party matching for `party`, with confidence scoring, manual review, and safeguards against merging unrelated parties.

**Acceptance evidence:** Matching tests show true positives and false-positive rejection paths, related-case suggestions improve with confirmed aliases, and clerks can review merge recommendations before acceptance.

### 44. Document understanding for pleadings, exhibits, and orders

**Justification:** The PBC already declares `court_case_management_semantic_document_instruction_understanding`, but court operations need it aimed at pleadings, service proofs, exhibits, and orders rather than generic extraction.

**Improvement:** Add document parsing tuned for captions, hearing dates, relief requested, service certifications, exhibit labels, and operative order language, with citations back to the source document spans.

**Acceptance evidence:** Extraction tests cover pleadings, proofs of service, exhibits, and signed orders; confidence thresholds gate automation; review screens show the cited source text for each extracted field.

### 45. Retention, archival, and destruction holds

**Justification:** Court records can move from active to archived status while still being subject to appeal, seal restrictions, or destruction-hold policies that must be enforced consistently.

**Improvement:** Add archival status, retention schedule, destruction hold, and archive retrieval workflows on `court_case`, `filing`, `docket_entry`, `judgment`, and `court_order`.

**Acceptance evidence:** Archive tests prevent destruction while an appeal or hold is active, archived matters remain searchable to authorized users, and retrieval actions are audited.

### 46. Multi-tenant isolation for court and division policy

**Justification:** The manifest declares `court_case_management_multi_tenant_policy_isolation`; courts, divisions, and registries need separate procedural rules, numbering policies, and release evidence without leakage.

**Improvement:** Enforce tenant or court boundary isolation for case numbering, local rules, calendar policies, permissions, analytics, and release evidence generation.

**Acceptance evidence:** Isolation tests show one tenant cannot read another tenant’s cases, policies, or metrics, and configuration changes stay scoped to the owning court boundary.

### 47. Owned schema expansion for motion, exhibit, and service entities

**Justification:** Motion practice, exhibit custody, and service operations are substantial court workflows that should not remain hidden inside generic extension blobs forever.

**Improvement:** Add first-class owned-schema models and migrations for motion, service record, exhibit record, and appellate packet entities under the `court_case_management` namespace.

**Acceptance evidence:** Migrations create dedicated tables, models enforce foreign-key integrity to core court tables, and release evidence shows there is no shared-table reach outside the PBC boundary.

### 48. Simulation sandbox for calendar and rule changes

**Justification:** Courts should be able to test a standing-order change, holiday calendar update, or courtroom closure before it disrupts live hearings and deadlines.

**Improvement:** Use `court_case_management_counterfactual_scenario_simulation` to simulate deadline recalculation, hearing reschedules, staffing shortages, and courtroom closures against current case workloads without mutating production state.

**Acceptance evidence:** Simulation runs compare before-and-after hearing and deadline impact, scenario outputs are exportable, and no live records change during a sandbox run.

### 49. Procedural regression harness and control assertions

**Justification:** A court PBC needs scenario-based regression coverage for filings, motions, service, hearings, orders, sealed access, and appeals, not just low-level contract tests.

**Improvement:** Expand `court_case_management_control_assertion` coverage to include end-to-end procedural scenarios, assistant governance checks, event replay, and release-gate failures when core court workflows regress.

**Acceptance evidence:** Regression suites cover the main procedural paths, failing scenarios block release evidence completion, and control dashboards show which procedural assertions passed for the current version.

### 50. Post-judgment enforcement and compliance tracking

**Justification:** After judgment or order entry, courts still need to track compliance deadlines, stays, satisfaction filings, contempt motions, and case-closing conditions.

**Improvement:** Add post-judgment tracking for compliance obligations, satisfaction or release filings, stayed enforcement periods, contempt-related follow-up, and final case closure readiness on `judgment` and `court_order`.

**Acceptance evidence:** Post-judgment timelines show open obligations and satisfied obligations distinctly, stay periods suspend the right deadlines, and a case cannot be marked fully closed while post-judgment obligations remain open.
