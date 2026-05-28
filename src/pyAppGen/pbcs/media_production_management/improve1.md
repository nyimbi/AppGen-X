# Media Production Management Improvement Backlog

## Current Domain Evidence Used

- PBC key in manifest: `media_production_management`.
- Current description: productions, budgets, crews, locations, shoots, post-production, assets, and delivery milestones.
- Current owned tables: `production`, `budget_line`, `crew_booking`, `location_permit`, `shoot_day`, `post_production_task`, `delivery_asset`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Current APIs: `POST /productions`, `POST /budget-lines`, `POST /crew-bookings`, `POST /location-permits`, `POST /shoot-days`, and `GET /media-production-management-workbench`.
- Current emitted events: `MediaProductionManagementCreated`, `MediaProductionManagementUpdated`, `MediaProductionManagementApproved`, and `MediaProductionManagementExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current UI fragments: `MediaProductionManagementWorkbench`, `MediaProductionManagementDetail`, and `MediaProductionManagementAssistantPanel`.
- Current release evidence sections: schema, services, events, handlers, UI, agent, and governance.

### 1. Development slate lifecycle
**Justification:** Media production starts long before principal photography, and the current `production` surface does not show concept, option, commissioned script, financing, greenlight, prep, production, post, delivery, and library states as first-class milestones.
**Improvement:** Expand the production lifecycle so development executives can track script drafts, package attachments, financing readiness, greenlight gates, and target release windows before a show or film becomes an active shoot.
**Acceptance evidence:** Lifecycle contract tests, seeded development-to-greenlight scenarios, workbench lane definitions for each slate stage, and release evidence that shows the lifecycle in UI and service contracts.

### 2. Script package and creative development tracking
**Justification:** A production record is incomplete if it cannot prove which script draft, treatment, lookbook, and creative package was approved for prep.
**Improvement:** Add structured development artifacts for script versions, bible or deck references, creative notes, attachment status, and greenlight comments, with dated ownership for development, production, and finance stakeholders.
**Acceptance evidence:** Document lineage fixtures, approval trail snapshots for script package changes, detail-view mock data for creative artifacts, and tests that reject prep readiness when required development assets are missing.

### 3. Budget top sheet and phase budgeting
**Justification:** Production budgeting is not a single flat ledger; teams need development, prep, shoot, post, marketing, contingency, and delivery views that reconcile to the approved top sheet.
**Improvement:** Extend `budget_line` behavior to support phase codes, account groups, above-the-line and below-the-line rollups, contingency buckets, currency handling, and approval thresholds tied to greenlight and reforecast events.
**Acceptance evidence:** Budget rollup fixtures, top-sheet calculations in workbench projections, approval threshold tests, and release evidence showing drill-down from summary totals to line-level details.

### 4. Budget revision and change-order control
**Justification:** Productions rarely finish on the first approved budget, so the package needs controlled reforecasting rather than silent overwrites.
**Improvement:** Add revision numbers, locked approved baselines, change-order reasons, variance attribution, and producer or studio approval routing whenever a budget amendment changes cash flow, shoot days, or delivery scope.
**Acceptance evidence:** Budget revision tests, before-and-after variance reports, approval events for change orders, and UI evidence showing current forecast against last approved budget.

### 5. Casting versus crew boundary
**Justification:** Talent attachments, extras, and day players are governed differently from crew hires, and a single `crew_booking` abstraction blurs payroll, contractual, and scheduling rules.
**Improvement:** Separate cast engagements from crew bookings with distinct fields for role type, billing, union status, fitting dates, rehearsal dates, work guarantees, and release obligations while keeping operational handoffs visible on one production timeline.
**Acceptance evidence:** Schema design notes in release evidence, validation tests that block cast-specific fields on crew records and vice versa, and workbench cards showing cast and crew lanes with different actions.

### 6. Deal memos and engagement packet intake
**Justification:** Scheduling decisions depend on confirmed deal points, not just names on a call sheet.
**Improvement:** Add governed intake for cast and crew deal memos, rate cards, availability windows, travel classes, accommodation rules, and special conditions so operational bookings inherit the terms that actually govern the engagement.
**Acceptance evidence:** Document extraction fixtures for deal memos, mutation preview examples in the assistant panel, rejection tests for incomplete engagement packets, and detail views that cite the source document for each key term.

### 7. Stripboard and shooting schedule planning
**Justification:** A production workbench is weak if it can create shoot days but cannot express stripboard logic, day breaks, company moves, and sequence clustering.
**Improvement:** Introduce schedule planning entities around `shoot_day` for stripboard ordering, scene grouping, unit assignment, weather cover sets, turnaround rules, and schedule versions that producers can compare before locking the plan.
**Acceptance evidence:** Schedule simulation fixtures, version-diff outputs for stripboard changes, workbench schedule boards, and tests that detect illegal sequence ordering or turnaround violations.

### 8. Call sheet generation and distribution
**Justification:** Daily execution depends on accurate call sheets, and they carry location, crew, cast, transport, safety, and weather instructions that should not live outside the package.
**Improvement:** Add call sheet generation from approved schedule data, with crew call times, cast calls, unit assignments, scene blocks, transport pickups, meal breaks, nearest hospital, weather, parking, and emergency contacts.
**Acceptance evidence:** Call sheet sample outputs, field-completeness checks, distribution audit logs, and UI actions that allow approved issue, revise, and supersede flows for each shoot date.

### 9. Location package readiness
**Justification:** Location management is more than permit status; productions need site contacts, parking plans, restrictions, curfews, and neighborhood obligations before a day can move to ready.
**Improvement:** Extend `location_permit` with location packets that capture jurisdiction, site owner terms, police or fire requirements, parking maps, power availability, curfew limits, insurance evidence, and contingency locations.
**Acceptance evidence:** Readiness checklists for location packets, permit validation tests, evidence attachments for site restrictions, and workbench indicators that show blocking gaps by location.

### 10. Travel, lodging, and movement logistics
**Justification:** Crew and cast utilization depends on transport and lodging plans, especially for remote shoots, night shoots, and company moves.
**Improvement:** Add logistics planning linked to schedule and booking data for airport transfers, hotel blocks, rooming lists, vehicle assignments, per diem rules, and company-move timing so operations can spot impossible travel plans before issue.
**Acceptance evidence:** Logistics conflict tests, movement-time simulations, detail panels for travel status, and scenario seeds showing a company move that affects the next day call sheet.

### 11. Shoot day readiness gate
**Justification:** Marking a day as ready should require more than a row in `shoot_day`; it should prove budget, people, location, equipment, safety, and approvals are in place.
**Improvement:** Add a readiness gate for each shoot day that checks cast confirmations, crew assignments, location clearance, call sheet approval, transport readiness, equipment availability, weather review, and open blocking exceptions.
**Acceptance evidence:** Readiness scorecards, blocking-rule tests, event payload samples for ready or blocked transitions, and workbench badges that explain exactly why a day cannot be released.

### 12. On-set safety planning and incident capture
**Justification:** Safety is a production control, not an afterthought, and risky scenes need documented mitigations tied to the day they affect.
**Improvement:** Add safety plans for stunts, weapons, animals, minors, water work, vehicles, special effects, night work, and extreme weather, plus incident and near-miss capture linked to the relevant shoot day and call sheet revision.
**Acceptance evidence:** Safety-plan templates, required-field tests for high-risk scenarios, incident timeline records, and release evidence showing safety controls in UI, events, and governance sections.

### 13. Departmental checklist coverage
**Justification:** Assistant directors, camera, sound, art, wardrobe, makeup, locations, transport, and production office each own day-specific tasks that the current package does not model.
**Improvement:** Add department checklists, owners, due times, and signoff states so shoot readiness can show which department still blocks first shot and which items were waived with approval.
**Acceptance evidence:** Department checklist fixtures, due-time alerts, signoff audit trails, and workbench views grouped by department and status.

### 14. Daily production report capture
**Justification:** The package needs a reliable account of what actually happened on set, not just what was scheduled.
**Improvement:** Add daily production report capture for actual call, first shot, meal, wrap, pages completed, scenes shot, overtime, weather impact, incidents, delays, and reasons, with variance against planned schedule and budget.
**Acceptance evidence:** Daily report schemas, variance calculations, UI summaries for planned versus actual, and tests that roll delay causes into budget and schedule projections.

### 15. Dailies ingest and review workflow
**Justification:** Dailies are a core production feedback loop, and the package currently has no explicit way to record ingest, sync, review status, or missing media.
**Improvement:** Create dailies workflows tied to `delivery_asset` and `post_production_task` for camera card ingest, checksum verification, sync status, review sessions, clip notes, and reshoot flags from editorial or production.
**Acceptance evidence:** Dailies ingest fixtures, checksum validation tests, review-note examples, and workbench boards that show expected versus received dailies by shoot day and camera unit.

### 16. Script supervision and continuity controls
**Justification:** Continuity breaks are expensive and often show up only after editorial review unless the system preserves script notes and coverage evidence.
**Improvement:** Add continuity records for slate, take continuity, prop continuity, costume continuity, line changes, coverage completeness, and notes requiring pick-ups or inserts.
**Acceptance evidence:** Continuity-note samples, linkage tests between scenes, dailies, and pick-up tasks, and UI evidence that highlights unresolved continuity risks before picture lock.

### 17. Equipment and kit allocation
**Justification:** Schedules become fiction when camera, grip, lighting, sound, and specialty equipment commitments are not reflected in the operational model.
**Improvement:** Add equipment package reservations, prep dates, return dates, damaged-kit incidents, sub-rental approvals, and cross-unit conflicts so each shoot day shows the kit plan that supports it.
**Acceptance evidence:** Equipment conflict simulations, prep-return tracking fixtures, approval logs for substitutions, and schedule warnings when required kit is unavailable.

### 18. Union, turnaround, and labor-rule compliance
**Justification:** Crew scheduling must respect union and labor commitments, especially across night work, sixth or seventh days, travel, and meal penalties.
**Improvement:** Add rules for turnaround windows, meal-break timing, overtime triggers, consecutive-day constraints, child labor restrictions, and role-specific rest requirements for cast and crew.
**Acceptance evidence:** Policy test matrix for labor cases, exception records when a rule is breached, cost-impact projections for penalties, and workbench warnings surfaced before call sheets are issued.

### 19. Extras and background performer operations
**Justification:** Background casting has different volume, voucher, wardrobe, and crowd-control demands from principal cast or crew.
**Improvement:** Add dedicated flows for background counts, holding-area plans, wardrobe states, meal planning, voucher capture, crowd wrangling, and release evidence for minors or restricted extras.
**Acceptance evidence:** Background booking fixtures, count reconciliation tests, voucher audit trails, and call sheet sections proving extras logistics are captured without polluting principal cast records.

### 20. Procurement, petty cash, and expense capture
**Justification:** Production offices need timely cash and purchasing visibility to control burn rate and avoid missing receipts during audits.
**Improvement:** Extend budget operations with purchase requests, purchase orders, petty cash envelopes, receipt matching, approver limits, and departmental charge coding linked back to cost reports.
**Acceptance evidence:** Expense intake examples, approval threshold tests, unmatched-receipt exception queues, and cost-report projections showing committed versus actual spend.

### 21. Cost report cadence and burn analysis
**Justification:** A budget is not operationally useful unless finance and production can see burn rate by week, by department, and by remaining schedule.
**Improvement:** Add cost-report views with current actuals, committed costs, estimate to complete, contingency drawdown, overage drivers, and schedule-linked forecast risk.
**Acceptance evidence:** Cost-report calculations, trend charts in the workbench, scenario seeds for over-budget departments, and release evidence showing finance views in UI and analytics.

### 22. Editorial handoff from set to post
**Justification:** The transition from production to post is one of the highest-risk handoffs because missing media, metadata, or notes can stall editorial immediately.
**Improvement:** Create a formal handoff that packages camera and sound manifests, script notes, dailies status, music reports, continuity notes, and open set issues into the first editorial queue.
**Acceptance evidence:** Handoff packet examples, completeness checks, event emissions for editorial-ready states, and tests that block editorial start when required set artifacts are missing.

### 23. Post-production schedule and milestone board
**Justification:** `post_production_task` should support real post workflows such as editor's cut, director's cut, producer review, picture lock, sound, color, VFX, QC, and final delivery.
**Improvement:** Add milestone templates, dependencies, planned dates, owners, and approval states for editorial, sound, music, color, graphics, subtitling, localization, and mastering.
**Acceptance evidence:** Post milestone fixtures, dependency tests, board views for milestone status, and release evidence demonstrating post-specific UI and task orchestration.

### 24. VFX shot inventory and turnover control
**Justification:** VFX work cannot be managed as generic post tasks because shot counts, versions, turnovers, bids, temps, finals, and vendor notes are central to delivery risk.
**Improvement:** Add VFX shot tracking with sequence and shot codes, vendor assignment, bid status, turnover packages, plate availability, temp comps, finals, notes, and approval rounds.
**Acceptance evidence:** VFX shot fixtures, turnover completeness rules, version-history examples, and workbench views that reconcile vendor status against delivery deadlines.

### 25. Sound, color, and finishing chain
**Justification:** Final delivery depends on interlocked finishing steps that need explicit dependencies and signoff states.
**Improvement:** Model sound editorial, ADR, Foley, premix, final mix, conform, color prep, grade, online, graphics, captions, subtitles, and mastering as linked finishing tasks with handoff evidence.
**Acceptance evidence:** Finishing dependency tests, milestone progress reports, approval trails for mix and grade signoff, and deliverable readiness gates driven by finishing completion.

### 26. Music, archive, and rights clearance
**Justification:** Music licenses, stock footage rights, archive materials, and performer releases can block exploitation even when the cut is otherwise complete.
**Improvement:** Add rights and clearance tracking for music cues, archival elements, stock material, trademarks, performer releases, and location releases with dates, terms, territories, and expiry handling.
**Acceptance evidence:** Rights metadata fixtures, expiry alerts, approval records, and release evidence showing clearance blockers in production and delivery views.

### 27. Approval matrix by stage and function
**Justification:** Media production approvals vary by stage: development, greenlight, schedule lock, call sheet issue, budget revision, picture lock, VFX finals, and master delivery should not share one generic approve action.
**Improvement:** Add stage-specific approval types with named approver roles, quorum rules, delegated authority, escalation paths, and rework reasons mapped to production, budget, schedule, post, and deliverable events.
**Acceptance evidence:** Approval policy matrix, role-based tests, approval event samples, and UI evidence showing who can approve what at each stage.

### 28. Notes, versions, and rework loops
**Justification:** Creative work depends on notes and versioning, and the package needs to distinguish current approved versions from review drafts and superseded cuts.
**Improvement:** Add version lineage for scripts, call sheets, schedules, budgets, edits, VFX shots, sound mixes, and deliverables, with note categories, reply chains, and mandatory resolution before closure.
**Acceptance evidence:** Version tree examples, note-resolution workflows, tests blocking closure with unresolved critical notes, and detail pages that show current approved version versus historical revisions.

### 29. Deliverables matrix by platform and territory
**Justification:** Final delivery is not a single asset; every platform and territory can require different masters, captions, audio stems, artwork, metadata, and legal packets.
**Improvement:** Expand `delivery_asset` into a deliverables matrix that tracks package type, spec version, territory, language, audio layout, caption set, artwork set, checksum, QC result, and shipment state.
**Acceptance evidence:** Deliverables matrix fixtures, per-platform validation tests, asset-package status boards, and release evidence showing platform-specific readiness criteria.

### 30. Technical QC and rejection handling
**Justification:** Deliverables frequently fail for spec issues, and a package that cannot trace QC failures to responsible upstream tasks will not reduce redelivery cycles.
**Improvement:** Add QC result capture for video, audio, captions, metadata, packaging, and checksum failures, with root-cause categories that route issues back to editorial, sound, VFX, mastering, or metadata owners.
**Acceptance evidence:** QC rejection fixtures, retry and reissue workflows, event samples for failed and passed QC, and dashboards showing first-pass success rate by deliverable class.

### 31. Marketing and publicity asset coordination
**Justification:** Release delivery often depends on posters, key art, trailers, stills, and publicity approvals that are adjacent to but distinct from core picture deliverables.
**Improvement:** Add coordinated tracking for marketing assets, embargo dates, approval rounds, territory variants, and linkage to final release windows so launch-critical materials are not managed off-system.
**Acceptance evidence:** Marketing asset samples, approval timelines, embargo validation rules, and workbench views that join release dates to marketing asset readiness.

### 32. Archive, restore, and library package management
**Justification:** Productions need a provable library package after delivery, including masters, project files, stems, legal packets, and metadata required for future reversioning or restoration.
**Improvement:** Add archive bundles with source media lineage, retention classes, cold-storage status, retrieval tests, and package manifests that support remastering, clip licensing, or platform redelivery later.
**Acceptance evidence:** Archive manifest fixtures, retrieval simulation results, retention-policy checks, and evidence that archive bundles can be traced back to the final approved deliverables.

### 33. Release documents and legal packet evidence
**Justification:** Production readiness depends on more than media assets; networks and distributors also require rights, insurance, compliance, and release paperwork.
**Improvement:** Create a governed evidence vault for talent releases, location releases, insurance certificates, cue sheets, chain-of-title records, censorship filings, and distribution affidavits linked to the production and deliverable they support.
**Acceptance evidence:** Evidence packet examples, required-document rules by release target, audit trails for uploads and approvals, and release evidence reports that show document completeness.

### 34. Production workbench UI for executive and line users
**Justification:** The current UI fragments list only a generic workbench, detail, and assistant panel, but production teams need role-specific boards that answer different questions.
**Improvement:** Split the workbench into views for slate and development, budget control, casting and crew, schedule and call sheets, locations, shoot-day readiness, post and VFX, deliverables, and release evidence.
**Acceptance evidence:** UI contract updates, navigation definitions, role-specific mock states, and screenshot-based release evidence for each major board.

### 35. Exception-first UI for blockers and aging
**Justification:** Producers and coordinators need to see blockers immediately, not infer them from scattered records.
**Improvement:** Add exception queues for missing approvals, location gaps, cast conflicts, labor-rule breaches, missing dailies, VFX delays, QC rejections, and missing release documents, with aging, owner, and next action.
**Acceptance evidence:** Queue fixtures, aging calculations, permission-aware actions, and analytics evidence showing blocker counts by stage and severity.

### 36. Assistant skills for production operations
**Justification:** The current agent surface supports generic read, create, and update patterns, but media production work requires guided skills tuned to domain-specific tasks.
**Improvement:** Add assistant skills for draft call sheet assembly, budget variance explanation, crew conflict review, location packet validation, dailies completeness checks, VFX turnover prep, and deliverable package review, all using governed previews before mutation.
**Acceptance evidence:** Skill manifest entries, prompt-to-preview examples, policy tests for blocked mutations, and assistant panel evidence showing domain-specific actions rather than generic CRUD.

### 37. Document instruction intake for production paperwork
**Justification:** Production teams work from scripts, deal memos, permits, call sheets, daily reports, cue sheets, and spec sheets, so document understanding should target those forms directly.
**Improvement:** Expand document intake so the assistant can parse and map production paperwork into safe draft updates, cite extracted source spans, flag low-confidence fields, and route ambiguous items to humans.
**Acceptance evidence:** Form-parsing fixtures, confidence-threshold tests, source citation examples in mutation previews, and release evidence showing document intake in the agent and governance sections.

### 38. Event model for production lifecycle and handoffs
**Justification:** The current emitted events are too generic to describe real production state changes for dependent packages and audit review.
**Improvement:** Add typed domain events for development-greenlight, budget-approved, schedule-locked, call-sheet-issued, shoot-day-ready, dailies-missing, editorial-started, VFX-turnover-sent, picture-locked, QC-passed, and package-delivered transitions.
**Acceptance evidence:** Event contract examples, payload snapshots, handler tests for downstream consumers, and release evidence showing event traceability for key production milestones.

### 39. Consumed-event handling for policy, audit, and KPI signals
**Justification:** Incoming policy, audit, and KPI events should change production behavior in observable ways instead of remaining abstract background dependencies.
**Improvement:** Map `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` to concrete actions such as approval rule recalculation, sealed-evidence locking, KPI-driven risk escalation, and workbench alerts on affected productions.
**Acceptance evidence:** Idempotent handler tests, lineage records linking inbound events to resulting exceptions or projections, and workbench evidence showing the operational effect of consumed events.

### 40. Predictive risk scoring for schedule and budget drift
**Justification:** Production management becomes more useful when it warns about likely overtime, schedule slip, undercoverage, missing dailies, or delivery failure before the problem becomes irreversible.
**Improvement:** Add predictive risk models that score shoot-day readiness, labor-risk exposure, location instability, budget burn risk, post bottlenecks, VFX delay exposure, and delivery miss probability with explainable feature outputs.
**Acceptance evidence:** Risk feature manifests, calibration examples, explainability cards in the UI, and tests for high-risk scenarios such as weather disruption or major VFX slippage.

### 41. Multi-tenant isolation for productions and vendor data
**Justification:** Studios, production companies, and service vendors may share infrastructure, but their schedules, talent data, budgets, and release assets must remain isolated.
**Improvement:** Strengthen tenant scoping for production records, bookings, call sheets, safety plans, post workflows, and deliverables so tenant boundaries hold across API, UI, events, storage, and assistant skills.
**Acceptance evidence:** Cross-tenant negative tests, tenant-specific workbench snapshots, permission checks across agent actions, and release evidence demonstrating isolation controls.

### 42. Offline and poor-connectivity field capture
**Justification:** On-set users often work in low-connectivity environments, especially at remote locations, and still need to record incidents, schedule changes, and daily actuals.
**Improvement:** Add offline draft capture and later reconciliation for daily production reports, safety incidents, location notes, and departmental checklists, with conflict detection when data syncs back to the main record.
**Acceptance evidence:** Offline-sync fixtures, reconciliation conflict examples, degraded-mode UI states, and tests proving no silent data loss during resync.

### 43. External vendor and facility collaboration
**Justification:** Post houses, VFX vendors, sound facilities, labs, and logistics providers need scoped interaction without gaining broad internal access.
**Improvement:** Add controlled external collaboration for turnover receipt, delivery acknowledgement, note response, asset reupload, and status updates using scoped roles, expiring links, and inbound evidence validation.
**Acceptance evidence:** External access policy tests, vendor activity audit logs, inbound validation fixtures, and release evidence showing collaboration boundaries in governance and UI sections.

### 44. Exception triage, retries, and dead-letter recovery
**Justification:** Production operations involve message retries, failed ingests, blocked approvals, and incomplete packets that should be handled through operational queues rather than hidden support work.
**Improvement:** Expand exception handling so dead-letter events, failed dailies ingests, rejected call sheets, broken delivery packages, and stuck approval chains surface in guided triage queues with replay, retry, and closeout actions.
**Acceptance evidence:** Dead-letter recovery fixtures, retry eligibility rules, queue screenshots, and event evidence showing exception open, retry, and resolved outcomes.

### 45. Release evidence traceability across the package
**Justification:** The package should prove what is implemented and verified across schema, services, events, handlers, UI, agent, and governance, not just claim it.
**Improvement:** Tie every production-domain capability in this backlog to explicit release evidence entries, with trace links from schema entities and API actions to UI states, event contracts, agent skills, and tests.
**Acceptance evidence:** Traceability table in release evidence, failing checks for undocumented capabilities, and generated reports that show which backlog items have executable coverage.

### 46. Seeded production scenarios and release rehearsals
**Justification:** Media production behavior is easiest to verify through realistic end-to-end examples, not isolated unit assertions alone.
**Improvement:** Add seeded scenarios for feature film, episodic television, branded content, documentary travel shoot, VFX-heavy show, and urgent redelivery, each exercising development, budgeting, scheduling, shooting, post, approvals, and deliverables.
**Acceptance evidence:** Scenario seeds, smoke-test runs, workbench screenshots per scenario, and release evidence showing pass or fail status for each rehearsal flow.

### 47. Operational metrics and service levels
**Justification:** Production leaders need leading indicators such as call-sheet issue timeliness, permit turnaround, daily report completion, dailies lag, VFX aging, approval latency, and deliverable first-pass success.
**Improvement:** Add domain analytics and service levels across development, prep, shoot, post, and delivery, with drill-down from executive summary to specific blocking records and departments.
**Acceptance evidence:** Metric definitions, projection tests, dashboards in the workbench, and alert fixtures for breached service levels by production stage.

### 48. Immutable history and audit-proof evidence
**Justification:** Production disputes often hinge on who approved what and when, especially across budgets, safety, deliveries, and legal documents.
**Improvement:** Expand event-sourced history and proof sealing so every material approval, schedule issue, budget revision, safety incident, QC outcome, and release packet change can be reconstructed with actor, timestamp, and evidence hashes.
**Acceptance evidence:** Replay tests, proof-verification outputs, event history views, and release evidence that cites audit-proof coverage in the governance section.

### 49. Schema expansion for media-specific subdomains
**Justification:** The current owned tables do not yet express several subdomains that real productions depend on, such as call sheets, daily reports, safety plans, dailies, VFX shots, approvals, and legal packets.
**Improvement:** Plan owned-schema expansion for media-specific tables and projections so the package can represent those concepts directly instead of hiding them in generic payloads or comments.
**Acceptance evidence:** Proposed schema map in package docs, migration backlog entries, contract updates for new entities, and release evidence showing how schema expansion will stay inside package boundaries.

### 50. Go-live gate for a production release candidate
**Justification:** A production should only be marked release-ready when the package can prove that creative, operational, legal, technical, and delivery obligations are all satisfied.
**Improvement:** Add a final release candidate gate that checks approved budget, locked schedule, cleared locations, completed safety review, ingested dailies, completed post milestones, approved VFX finals, passed QC, complete deliverables matrix, and complete legal packet evidence.
**Acceptance evidence:** Release-candidate checklist results, blocking exception examples, workbench release-readiness panels, and package-level release evidence showing the gate operating end to end.
