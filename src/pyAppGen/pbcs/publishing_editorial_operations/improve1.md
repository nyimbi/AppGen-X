# Publishing Editorial Operations Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `publishing_editorial_operations`.
- Manifest description: manuscripts, editorial workflow, rights, editions, production schedules, distribution, and publishing analytics.
- Current owned tables include `manuscript`, `editorial_task`, `author_contract`, `edition`, `production_schedule`, `rights_grant`, and `distribution_plan`.
- Current command APIs are `POST /manuscripts`, `POST /editorial-tasks`, `POST /author-contracts`, `POST /editions`, `POST /production-schedules`, and `GET /publishing-editorial-operations-workbench`.
- Current UI fragments are `PublishingEditorialOperationsWorkbench`, `PublishingEditorialOperationsDetail`, and `PublishingEditorialOperationsAssistantPanel`.
- Current agent contract exposes governed CRUD, document instruction intake, mutation preview, and the `publishing_editorial_operations_skills` namespace.
- Current emitted events are `PublishingEditorialOperationsCreated`, `PublishingEditorialOperationsUpdated`, `PublishingEditorialOperationsApproved`, and `PublishingEditorialOperationsExceptionOpened`.
- Current consumed events are `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current release evidence sections are `schema`, `services`, `events`, `handlers`, `ui`, `agent`, and `governance`.
- Current domain operations include manuscript creation, editorial task recording, author contract review, edition approval, production schedule simulation, rights grant creation, and distribution plan recording.

### 1. Acquisition Pipeline Intake
**Justification:** The package starts at manuscript creation, but publishing teams first decide which proposals, pitches, and agented submissions deserve acquisition attention. Without acquisition intake inside the PBC boundary, the editorial trail begins too late.
**Improvement:** Add acquisition proposal records, sponsor editor ownership, comp-title analysis, target imprint, expected season, projected format mix, and acquisition-stage state transitions that resolve into `manuscript` creation only after an explicit decision.
**Acceptance evidence:** Release evidence shows an acquisition proposal progressing into a manuscript; the workbench exposes an acquisition queue; event history proves who recommended, approved, or declined each proposal.

### 2. Acquisition Board Decision Ledger
**Justification:** Editorial boards need a durable record of why a project advanced, stalled, or was rejected, especially when forecasts change between pitch, offer, and signed contract.
**Improvement:** Introduce board packet generation, vote capture, conditions of approval, requested revisions, and post-board action tracking tied to acquisition candidates and later `author_contract` records.
**Acceptance evidence:** A decision ledger links board outcomes to contracts and manuscripts; rejected and conditional approvals are searchable; workbench evidence shows required follow-ups before a title can move forward.

### 3. Manuscript Package Completeness Rules
**Justification:** Editorial operations fail downstream when manuscripts enter the workflow missing synopsis, author bio, permissions notes, sample chapters, art logs, or target metadata.
**Improvement:** Define intake completeness profiles by book type, journal issue, reference work, or digital-first release, with explicit required artifacts, optional artifacts, and waiver reasons before a manuscript can enter active editorial processing.
**Acceptance evidence:** Completeness checks block incomplete intake; waivers are recorded with approver identity; the detail page shows a resolved checklist for each manuscript package.

### 4. Manuscript Version Lineage and Freeze Points
**Justification:** Editorial, copyediting, proof, and production conversations break when teams cannot tell which manuscript version is authoritative or when text was frozen for a given stage.
**Improvement:** Add manuscript version lineage with submission version, developmental edit version, copyedited version, proof version, corrected proof version, and final release version, including freeze timestamps and rationale.
**Acceptance evidence:** Each manuscript shows a clear version graph; proof and production records reference a specific frozen version; release evidence includes a manuscript-to-final-text lineage trace.

### 5. Editorial Calendar and Season Planning
**Justification:** Publishing operations are governed by seasonal lists, issue calendars, conference tie-ins, and marketing windows, not by standalone record deadlines.
**Improvement:** Create editorial calendar entities for season, issue, list, and campaign anchor dates, then connect manuscripts, editions, and publication schedules to those calendar objects with dependency visibility.
**Acceptance evidence:** The workbench renders season and issue calendars; titles can be filtered by editorial season; missed calendar anchors open explicit exceptions instead of hidden slippage.

### 6. Capacity-Aware Editorial Assignment
**Justification:** Manuscripts stall when assignment decisions ignore editor capacity, specialty, leave, and current queue age.
**Improvement:** Add capacity-aware routing for acquisitions editors, developmental editors, managing editors, copyeditors, and production editors using workload, domain expertise, due dates, and escalation thresholds.
**Acceptance evidence:** Assignment recommendations show why a person was chosen; overloaded assignees trigger routing warnings; SLA evidence shows reduced reassignment churn and aging.

### 7. Peer Review Workflow Models
**Justification:** Scholarly and professional publishing often depends on peer review, yet the current package does not distinguish reviewer invitation, acceptance, review receipt, or decision synthesis states.
**Improvement:** Support single-blind, double-blind, open, and editorial-only review models, with reviewer invitation tracking, reviewer deadline management, revision requests, and final editorial recommendation capture.
**Acceptance evidence:** Review workflows can be configured by imprint or publication type; manuscripts display reviewer-state timelines; decision packets cite the completed review set that informed the recommendation.

### 8. Reviewer Conflict and Anonymity Controls
**Justification:** Reviewer quality is inseparable from conflict-of-interest checks, anonymity safeguards, and recusal evidence.
**Improvement:** Add reviewer conflict declarations, institution and collaborator checks, anonymity rules for blind review, and recusal handling that preserves confidentiality while keeping the workflow auditable.
**Acceptance evidence:** Reviewer records show conflict status and recusal outcomes; blind review exports redact forbidden identities; audit evidence proves conflict checks ran before assignment.

### 9. Editorial Decision Bundle Integrity
**Justification:** Accept, revise, reject, and transfer decisions need a structured rationale bundle rather than a status code plus free text.
**Improvement:** Require decision bundles that include editorial rationale, reviewer synthesis, required revision points, rights or permissions blockers, target season impact, and communication templates before a manuscript moves state.
**Acceptance evidence:** Decisions cannot be approved without a complete bundle; the detail UI shows decision rationale sections; outbound author communication references the stored decision bundle.

### 10. Contract-to-Manuscript Alignment Checks
**Justification:** Editorial teams need to know when delivery terms, due dates, option clauses, and format rights in the contract no longer match the live manuscript plan.
**Improvement:** Add cross-checks between `author_contract` and `manuscript` for delivery dates, manuscript length expectations, optional illustrations, territory constraints, and edition commitments.
**Acceptance evidence:** Contract drift exceptions appear on the workbench; corrective tasks are generated for editor and contracts owner; release evidence includes one resolved contract-to-manuscript mismatch case.

### 11. Copyediting State Machine
**Justification:** Copyediting is not a single task; it spans assignment, style-sheet setup, query pass, author response review, cleanup, and signoff.
**Improvement:** Model copyediting as a first-class workflow with explicit stages, assignee roles, expected handoff artifacts, and re-entry paths when substantial author revisions reopen the edit.
**Acceptance evidence:** Copyediting status appears as a board, not a note field; tasks reflect each substage; manuscripts re-enter copyedit only through governed transitions with evidence.

### 12. House Style and Style-Sheet Governance
**Justification:** Editorial quality depends on consistent application of imprint style, series conventions, citation systems, transliteration rules, and naming conventions.
**Improvement:** Add style-sheet entities with imprint- and series-specific rules, exception approvals, terminology preferences, and inheritance into copyedit and proof workflows.
**Acceptance evidence:** Style sheets are versioned and linked to manuscripts and editions; copyedit tasks cite the applicable style sheet; deviations require an explicit approval record.

### 13. Author Query Resolution Tracking
**Justification:** Author queries often determine whether copyediting and proofs stay on schedule, but they are commonly buried in email threads and attachments.
**Improvement:** Capture author queries as structured records with severity, response deadline, owning editor, response status, and unresolved-impact flags tied to manuscript versions and proof rounds.
**Acceptance evidence:** Query aging is visible in the workbench; unresolved critical queries block stage exit; the package can show which author responses changed the manuscript text.

### 14. Artwork, Excerpts, and Permissions Intake
**Justification:** Publishing projects often include images, tables, excerpts, and third-party materials that can derail schedules if rights evidence arrives late.
**Improvement:** Extend manuscript intake to include asset inventories, permission request status, licensor constraints, caption requirements, and substitution plans for unlicensed content.
**Acceptance evidence:** Asset and permissions completeness appears beside manuscript readiness; missing permissions raise rights exceptions before proof generation; release evidence includes a cleared permissions packet.

### 15. Rights Boundary Ledger
**Justification:** The package owns rights grants, but publishing decisions depend on a sharper boundary across territory, language, format, duration, and sublicensing rights than the current surface implies.
**Improvement:** Build a rights boundary ledger that records granted, withheld, pending, reverted, and expired rights at title, edition, and asset level with clear upstream evidence and downstream usage rules.
**Acceptance evidence:** Rights matrices can be viewed by title or edition; a blocked reuse attempt cites the exact boundary rule; event history shows every rights change with before-and-after scope.

### 16. Territory, Language, and Format Collision Detection
**Justification:** Editions and schedules become risky when ebook, audio, translation, serial, anthology, or territorial plans conflict with existing grants.
**Improvement:** Add collision checks that evaluate proposed editions and publication schedules against rights territory, language, format, exclusivity, and embargo windows before approval.
**Acceptance evidence:** Approval attempts surface specific rights collisions; accepted editions store a clean collision check; simulations show how rights changes affect planned release windows.

### 17. Edition Lineage and Inheritance Rules
**Justification:** New editions, revised editions, reprints, and special formats should inherit from prior editions selectively rather than copying data blindly.
**Improvement:** Define edition lineage rules for inherited metadata, carried-forward corrections, reset schedules, new identifiers, rights reuse, and evidence of what changed between editions.
**Acceptance evidence:** Each edition references its parent edition when applicable; inherited and overridden fields are distinguishable; release evidence includes an edition-diff artifact.

### 18. Metadata Authority Records
**Justification:** Publishing metadata errors damage discoverability, sales, library supply, and downstream syndication.
**Improvement:** Add authority-controlled metadata for title, subtitle, contributors, series, imprint, BISAC or subject codes, keywords, audience, ISBN, DOI, ISSN, and accessibility flags with source-of-truth ownership.
**Acceptance evidence:** Metadata validation catches missing or contradictory fields; contributor authority records prevent duplicate variants; approved editions expose a complete metadata readiness score.

### 19. Metadata Export and Traceability
**Justification:** It is not enough to hold metadata internally; editorial operations need proof of what metadata was approved and what left the package.
**Improvement:** Create export-ready metadata manifests and change snapshots for internal catalog, distributor, retailer, and library feeds, with exact edition and schedule references plus release timestamps.
**Acceptance evidence:** Export evidence binds each feed to a specific edition and publication schedule; a metadata diff view shows what changed between releases; failed exports land in a recoverable queue.

### 20. Publication Schedule Critical Path
**Justification:** `production_schedule` exists, but publishing schedules are only actionable when critical dependencies such as copyedit completion, proof approval, rights clearance, and metadata readiness are visible together.
**Improvement:** Model a publication critical path that links editorial, design, production, metadata, and rights milestones to publication date risk, with hard gates and soft warnings.
**Acceptance evidence:** Schedule boards show milestone dependencies and slack; blocked dates identify the missing prerequisite; forecast evidence explains why a publication date is safe or at risk.

### 21. Production Handoff Packet
**Justification:** Production handoff often fails because text, art, specs, and metadata are delivered as fragmented artifacts rather than as a governed package.
**Improvement:** Require a production handoff packet containing frozen manuscript version, asset manifest, rights clearance state, trim and format specs, metadata snapshot, and unresolved-risk notes before production begins.
**Acceptance evidence:** Production cannot start without a complete handoff packet; the handoff packet is reviewable in the workbench; release evidence includes one signed-off handoff record.

### 22. Proof Round Orchestration
**Justification:** Proofs usually move through multiple rounds with different owners, and schedule discipline depends on knowing which round is active and what changed since the last round.
**Improvement:** Add proof round entities for first proof, second proof, final proof, and exception rounds, each with owner, due date, correction intake, and approval state.
**Acceptance evidence:** The package shows active and completed proof rounds per edition; corrections are attached to a specific round; final signoff cites the closing proof round.

### 23. Proof Correction Classification
**Justification:** Editorial teams need to distinguish author corrections, compositor errors, copyediting misses, and late-stage factual fixes because each kind has different schedule and cost implications.
**Improvement:** Classify proof corrections by source, severity, page scope, schedule impact, and whether the change requires rights or metadata revalidation.
**Acceptance evidence:** Proof dashboards summarize corrections by class; critical corrections reopen required downstream checks; analytics can separate compositor-driven and author-driven proof churn.

### 24. Accessibility and Alt-Text Readiness
**Justification:** Accessibility obligations should be visible before publication, not treated as an afterthought after files leave editorial control.
**Improvement:** Add accessibility readiness checks for alt text, reading order notes, tables, image descriptions, caption quality, and metadata flags tied to edition and proof signoff.
**Acceptance evidence:** Accessibility blockers appear in proof and release views; editions cannot reach release-ready state with unresolved accessibility defects; evidence exports include accessibility status.

### 25. Cover and Interior Asset Freeze Management
**Justification:** Publication schedules slip when covers, interiors, and marketing assets are changed after dependent metadata and proof steps have already locked.
**Improvement:** Track asset freeze milestones for cover, interior, jacket copy, and key marketing copy, with explicit reopen reasons and downstream recalculation of schedule risk.
**Acceptance evidence:** Asset freeze status is visible beside the publication schedule; unauthorized post-freeze changes are blocked or escalated; release evidence records any approved late asset reopen.

### 26. Publication Schedule Scenario Planning
**Justification:** Editors frequently need to ask what happens if a review is late, a rights clearance slips, or a proof round expands.
**Improvement:** Extend schedule simulation to model date slips, reviewer delays, proof-cycle expansion, asset changes, and territory-specific release sequencing for editions and formats.
**Acceptance evidence:** Simulation reports compare planned versus delayed schedules; decision-makers can see which milestone drives the date change; scenario evidence is attached to the chosen plan.

### 27. Editorial Exception Taxonomy
**Justification:** `PublishingEditorialOperationsExceptionOpened` is too generic to support fast triage across acquisition, review, copyedit, rights, proofs, and release readiness.
**Improvement:** Define explicit exception classes such as missing package evidence, reviewer overdue, contract drift, rights collision, metadata invalid, proof overload, late author response, and publication date breach.
**Acceptance evidence:** Exceptions are grouped by class in the workbench; each class has owner and SLA defaults; release evidence shows resolution of at least one exception from multiple classes.

### 28. Author Communication Timeline
**Justification:** Author communication is central to editorial operations and should be visible as timeline evidence, not scattered across private inboxes and ad hoc notes.
**Improvement:** Store structured author communications for offer discussion, delivery reminders, revision decisions, copyedit queries, proof instructions, and publication-date notices, linked to the relevant manuscript or edition stage.
**Acceptance evidence:** The detail UI shows a chronological author communication timeline; overdue required communications trigger alerts; communication templates are traceable to the triggering workflow event.

### 29. Reviewer and Editorial Correspondence Evidence
**Justification:** Peer and editorial review decisions are hard to defend later without a durable record of invitations, reminders, declines, and editorial follow-up.
**Improvement:** Record reviewer and editor correspondence events with message intent, recipient role, due date context, and privacy-safe summary fields while preserving blind-review safeguards.
**Acceptance evidence:** Reviewer correspondence appears in the review timeline without leaking hidden identities where prohibited; reminder events are measurable; decline and replacement paths are auditable.

### 30. Editorial Meeting Notes and Action Capture
**Justification:** Weekly editorial meetings often decide the real next action, but those decisions rarely become structured workflow changes.
**Improvement:** Add meeting-note capture that converts agreed actions into `editorial_task` records with owners, due dates, referenced manuscript or edition, and follow-up evidence requirements.
**Acceptance evidence:** Meeting actions appear automatically in task boards; unresolved actions remain linked to the originating meeting note; supervisors can filter backlog by meeting-originated tasks.

### 31. Acquisition Dashboard UI
**Justification:** `PublishingEditorialOperationsWorkbench` currently exposes broad package surfaces, but acquisitions teams need a specialized board for pitch funnel health and decision aging.
**Improvement:** Add an acquisitions dashboard with stages for unsolicited, under review, board packet pending, board decided, contract pending, and converted to manuscript, including comp-title and season views.
**Acceptance evidence:** The workbench has a dedicated acquisitions route or panel; board-stage counts are visible; users can open a candidate and see the exact blockers preventing conversion.

### 32. Manuscript Workspace UI
**Justification:** A manuscript detail screen should answer editorial questions immediately: version state, outstanding queries, review status, rights blockers, and schedule impact.
**Improvement:** Redesign the manuscript workspace around readiness panels, stage history, asset completeness, author communication, and linked edition and schedule consequences.
**Acceptance evidence:** `PublishingEditorialOperationsDetail` exposes manuscript readiness panels; unresolved blockers are visible above the fold; users can drill from manuscript state to the exact dependent tasks.

### 33. Editorial Calendar UI
**Justification:** Calendar views are operationally different from record lists and are necessary for season planning, issue management, and launch coordination.
**Improvement:** Add editorial calendar views for season, issue, and publication date planning with drag-aware previews, risk overlays, and dependency indicators rather than only tabular status.
**Acceptance evidence:** Users can view titles by season or publication week; moving a date previews impacted milestones before confirmation; risk-colored calendar cells match schedule evidence.

### 34. Peer Review Queue UI
**Justification:** Review coordinators need a focused queue of invitation status, due dates, reviewer load, and overdue manuscripts, not just general task listings.
**Improvement:** Create a peer review queue with invitation, acceptance, submission, reminder, overdue, and decision-ready columns plus blind-review-safe detail views.
**Acceptance evidence:** Review coordinators can filter by review model and overdue status; manuscripts ready for decision synthesis are surfaced explicitly; anonymity rules are preserved in the UI.

### 35. Copyedit and Proof Compare UI
**Justification:** Editors and authors need to see what changed between copyedit, author response, and proof rounds without leaving the package.
**Improvement:** Add compare views for manuscript versions and proof rounds with categorized changes, unresolved queries, and correction impact summaries tied to schedule and metadata effects.
**Acceptance evidence:** Version compare screens show changed sections and correction categories; proof corrections can be filtered by severity; compare links appear from tasks and proof records.

### 36. Rights and Editions Matrix UI
**Justification:** Rights and edition planning are inseparable, and teams need a single view that shows which editions can ship where, when, and in what formats.
**Improvement:** Build a matrix view that crosses editions with territory, language, format, embargo, and schedule status so operators can spot blocked releases before approval.
**Acceptance evidence:** Rights collisions are visible in a matrix, not buried in notes; each matrix cell links to the governing rights evidence; edition approval screens reuse the same matrix.

### 37. Acquisition and Manuscript Intake Agent Skill
**Justification:** The current agent contract exposes generic read, create, and update skills, but editorial teams need domain-specific assistance at intake.
**Improvement:** Add an agent skill that turns pitch notes, proposal documents, or agent submissions into acquisition candidates or manuscript drafts with explicit field mapping, completeness warnings, and no silent mutation path.
**Acceptance evidence:** The assistant panel previews an intake draft before save; missing evidence is highlighted in domain terms; audit history shows the human confirmer and the source document digest.

### 38. Editorial Brief and Decision Synthesis Agent Skill
**Justification:** Editors spend time synthesizing reviewer comments, board notes, and schedule impacts into an actionable decision memo.
**Improvement:** Add an agent skill that generates editorial briefs, reviewer synthesis, and decision memos grounded in stored review records, rights state, and schedule risk without inventing unsupported facts.
**Acceptance evidence:** Generated briefs cite underlying records and timestamps; unsupported fields are marked as missing rather than guessed; editors can approve or reject the brief as a draft artifact.

### 39. Copyedit Query and Change-Explanation Agent Skill
**Justification:** Author response rounds slow down when changes are opaque and queries are scattered.
**Improvement:** Add an agent skill that groups copyedit queries, explains major textual changes in plain language, and proposes author-facing summaries aligned to the current manuscript version and style sheet.
**Acceptance evidence:** Query bundles are traceable to specific text changes; author-facing summaries are previewed before send; style-sheet exceptions are called out explicitly.

### 40. Proof Risk and Release Readiness Agent Skill
**Justification:** Proof and release readiness decisions require a fast synthesis of corrections, metadata state, rights clearance, and schedule pressure.
**Improvement:** Add an agent skill that summarizes proof risk, identifies unresolved blockers, and drafts a release-readiness note grounded in proofs, publication schedules, and edition metadata.
**Acceptance evidence:** Assistant output references proof rounds, blocker counts, and target publication dates; the note cannot be finalized if required evidence is absent; reviewer feedback on assistant accuracy is stored.

### 41. Manuscript Lifecycle Event Expansion
**Justification:** Four generic emitted events do not tell downstream consumers enough about editorial state changes.
**Improvement:** Expand emitted events to include acquisition recommended, manuscript accepted, revision requested, copyedit started, copyedit completed, proof round opened, proof approved, and release readiness reached.
**Acceptance evidence:** Event contract docs list the new manuscript-stage events; handlers and tests prove idempotent publication; event history in the workbench shows fine-grained lifecycle steps.

### 42. Review and Decision Event Expansion
**Justification:** Review-heavy workflows need event fidelity for invitations, declines, reviews received, editorial decisions, and revision cycles.
**Improvement:** Add emitted events for reviewer invited, reviewer accepted, review overdue, decision memo approved, author revision returned, and editor recommendation changed.
**Acceptance evidence:** Review events appear in the outbox with stable schemas; review dashboards subscribe to them without parsing free text; dead-letter handling demonstrates recovery for one failed review event.

### 43. Production, Proof, and Publication Event Expansion
**Justification:** Production handoff and schedule control are downstream-critical and deserve explicit event boundaries.
**Improvement:** Emit events for production handoff ready, handoff accepted, proof round issued, proof corrections logged, metadata export completed, publication date changed, and edition released.
**Acceptance evidence:** Production and schedule projections react to these events; event examples are included in release evidence; schedule changes can be reconstructed purely from event history.

### 44. Time-Sensitive Notification Retry and Recovery
**Justification:** Reviewer reminders, author deadlines, proof notices, and publication-date changes are time-sensitive and should not disappear into a generic dead-letter bucket.
**Improvement:** Add retry policies and domain-aware recovery workflows for notification events, including stale-notice suppression, expiry handling, and escalations when a missed message changes editorial state.
**Acceptance evidence:** Dead-letter records classify the missed notification type; operators can see whether replay is still safe; recovered notifications link back to the original editorial deadline.

### 45. Editorial Release Evidence Binder
**Justification:** Current release evidence is package-wide, but publishing teams need a title- and edition-level binder that proves the project is actually publishable.
**Improvement:** Build a release evidence binder that assembles manuscript lineage, rights clearance, metadata readiness, proof signoff, schedule approval, communication evidence, and exception closure for each edition.
**Acceptance evidence:** A binder can be generated per edition; missing sections are called out explicitly; the workbench can show a release-ready versus not-ready verdict with supporting artifacts.

### 46. Publishing KPI and SLA Analytics
**Justification:** Editorial leaders need operating metrics such as acquisition conversion, review turnaround, copyedit age, proof churn, and on-time publication rate.
**Improvement:** Expand analytics to measure acquisition funnel conversion, reviewer acceptance rate, manuscript turnaround by stage, proof correction density, metadata defect rate, and schedule adherence by imprint or season.
**Acceptance evidence:** KPI definitions are documented; workbench charts drill into source records; SLA breaches generate visible exceptions tied to responsible stages and owners.

### 47. Owned Schema Expansion for Editorial Depth
**Justification:** The existing owned tables do not explicitly cover acquisitions, reviewer assignments, proof rounds, style sheets, metadata exports, or communication logs.
**Improvement:** Add owned tables or typed child records for acquisition candidates, reviewer assignments, review reports, style sheets, proof rounds, proof corrections, metadata snapshots, and communication events inside the PBC boundary.
**Acceptance evidence:** Schema contracts and migrations show the new domain records; no shared-table shortcuts are introduced; table browsers in the workbench expose the new entities cleanly.

### 48. Control Assertions for Editorial Integrity
**Justification:** Editorial operations need continuous checks that no edition is released with unresolved rights, missing metadata, unapproved proofs, or untracked author communication.
**Improvement:** Define control assertions that continuously test release blockers, blind-review anonymity violations, contract drift, metadata incompleteness, stale proof rounds, and post-freeze asset changes.
**Acceptance evidence:** Control assertions run and surface pass or fail states; failing controls open the right exception class automatically; release evidence includes the control results used for the final decision.

### 49. Scenario-Rich Test and Fixture Packs
**Justification:** Domain depth is only credible if tests cover real editorial edge cases rather than only CRUD smoke tests.
**Improvement:** Add fixture packs for late reviewer replacement, author non-response, image permissions denial, edition rights conflict, metadata correction after proof, schedule slip, and corrected reprint planning.
**Acceptance evidence:** Test manifests name the editorial scenarios covered; fixture data ties directly to package tables and events; release evidence references the domain scenarios exercised in verification.

### 50. Release Gate With Counted Evidence
**Justification:** The package should not claim readiness unless it can prove that editorial, rights, metadata, proofs, schedules, and communications all reached a release-safe state for the target edition.
**Improvement:** Implement a final release gate that counts required evidence artifacts, verifies their freshness, confirms that open exceptions are below the allowed threshold, and records the exact path of the generated binder.
**Acceptance evidence:** The release gate produces a counted checklist, a pass or fail verdict, and the path of the edition evidence bundle; the workbench exposes the verdict and the underlying artifact counts before any release approval.
