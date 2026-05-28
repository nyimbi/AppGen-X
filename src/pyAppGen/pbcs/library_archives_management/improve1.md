# Library and Archives Management Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `library_archives_management`
- Current description: collections, circulation, cataloging, digitization, rights, preservation, and archival access
- Current owned tables: `collection_item`, `catalog_record`, `circulation_loan`, `digitization_job`, `rights_statement`, `preservation_action`, `archive_request`, `library_archives_management_policy_rule`, `library_archives_management_runtime_parameter`, `library_archives_management_schema_extension`, `library_archives_management_control_assertion`, `library_archives_management_governed_model`
- Current APIs: `POST /collection-items`, `POST /catalog-records`, `POST /circulation-loans`, `POST /digitization-jobs`, `POST /rights-statements`, `GET /library-archives-management-workbench`
- Current workflows: `library_archives_management_create_collection_item_workflow`, `library_archives_management_record_catalog_record_workflow`
- Current UI fragments: `LibraryArchivesManagementWorkbench`, `LibraryArchivesManagementDetail`, `LibraryArchivesManagementAssistantPanel`
- Current emitted events: `LibraryArchivesManagementCreated`, `LibraryArchivesManagementUpdated`, `LibraryArchivesManagementApproved`, `LibraryArchivesManagementExceptionOpened`
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Current docs named in the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`

### 1. Bibliographic record templates by material type

**Justification:** Catalogers need different required fields for monographs, serials, maps, manuscripts, photographs, oral histories, and born-digital packages. A single flat `catalog_record` intake path will miss domain-specific completeness rules and force manual cleanup later.

**Improvement:** Add material-type-aware templates to `catalog_record` creation so the workbench can prefill the right descriptive pattern, validation rules, and mandatory review steps. The template set should distinguish published library materials from archival description and expose which fields remain provisional until authoritative review.

**Acceptance evidence:** Seeded examples for at least seven material types, template-driven validation tests, and workbench screenshots showing the template switcher and missing-field guidance.

### 2. Authority control for names, subjects, and corporate bodies

**Justification:** Search quality, duplicate suppression, and patron trust depend on consistent authority data. Without authority control, one donor, author, or creating agency can fragment into many near-duplicate headings.

**Improvement:** Introduce authority resolution around `catalog_record` and `collection_item` so personal names, family names, corporate bodies, geographic headings, and topical terms can be normalized, merged, and traced over time. Store the preferred form, variant labels, source of authority, and local override reason.

**Acceptance evidence:** Merge and split test fixtures for headings, authority review screens in `LibraryArchivesManagementDetail`, and audit evidence showing when a heading was normalized or locally overridden.

### 3. Call number and shelving logic with archival exceptions

**Justification:** Library stacks depend on deterministic call number handling, while archives often retain original order or box-level location logic. The PBC needs both models without confusing operators.

**Improvement:** Add configurable classification pipelines for call number construction, cutter generation, box/folder identifiers, oversize flags, and storage location assignment. The same workflow should support item-level shelving for circulating collections and accession-level placement for archives awaiting processing.

**Acceptance evidence:** Classification rule tests, location assignment traces, and scenarios showing one circulating book, one manuscript box, and one oversized map routed to different storage schemes.

### 4. Accession register with source-of-custody detail

**Justification:** Accessioning is where archives establish legal intake, immediate control, and the first provenance statement. If `archive_request` stops at a simple intake ticket, the system loses evidentiary value.

**Improvement:** Expand accession handling so each intake records accession number, transfer type, source, donor or office of origin, custody date, quantity received, temporary restrictions, and initial appraisal notes. The accession register should also link to unprocessed holdings so staff can distinguish received material from fully described material.

**Acceptance evidence:** Accession numbering tests, register views in the workbench, and release scenarios covering donation, institutional transfer, and emergency transfer intake.

### 5. Provenance chain capture for archival collections

**Justification:** Provenance is central to archival trust. Researchers and staff need to see how materials moved from creator to repository and where the chain is uncertain.

**Improvement:** Extend `collection_item` and `archive_request` flows to record creator, creating office, intermediate custodians, acquisition event, and any known gaps in custody. Provide a provenance timeline that distinguishes asserted facts from inferred relationships.

**Acceptance evidence:** Provenance timeline snapshots, tests for partial and disputed custody chains, and a detail panel that visibly labels uncertain provenance statements.

### 6. Accession restrictions and donor agreement enforcement

**Justification:** Rights and access conditions often begin with the deed of gift or transfer agreement, not at the point of public request. Those terms must directly shape processing and access behavior.

**Improvement:** Link accession records to `rights_statement` so donor restrictions, embargo periods, cultural sensitivity clauses, and return conditions can automatically influence processing queues, reading room eligibility, and digitization publication decisions. Staff should be able to see which access rule came from which agreement clause.

**Acceptance evidence:** Restriction propagation tests, clause-to-rule lineage in the UI, and a release scenario where a donor embargo blocks researcher access until the configured date.

### 7. Hierarchical finding aid support

**Justification:** Archives are described in collection, series, subseries, file, and item context. Treating finding aids as flat records breaks both archival practice and researcher navigation.

**Improvement:** Add a hierarchical description model tied to `catalog_record` and `collection_item` so staff can create multilevel finding aids with inherited dates, scope notes, access restrictions, and container references. The UI should make it easy to move, split, and renumber levels without losing archival context.

**Acceptance evidence:** Tree-editing tests, exported multilevel sample finding aids, and release evidence showing one collection rendered at collection, series, file, and item levels.

### 8. Container and location management for boxes, folders, and volumes

**Justification:** Processing, retrieval, and preservation all fail if staff cannot trust where physical material lives. Archives need container logic beyond a generic item location field.

**Improvement:** Expand `collection_item` storage tracking to support box, folder, volume, reel, cabinet, shelf, vault, and off-site container relationships. Include capacity warnings, split container histories, and explicit temporary location moves for exhibit use or conservation treatment.

**Acceptance evidence:** Container hierarchy tests, move-history audit logs, and staff views showing current and prior locations for a boxed archival collection.

### 9. Patron registration for reading room use

**Justification:** Reading room access is not the same as open-library circulation. Archives often require identity checks, orientation acknowledgement, and special permissions before any request is fulfilled.

**Improvement:** Add a governed patron registration path connected to `archive_request` that captures registration status, identity verification date, reading room rules acknowledgement, photography permissions, and any supervision requirements. Surface expiry and renewal needs before a request can be approved.

**Acceptance evidence:** Registration validation tests, blocked-request scenarios for expired registrations, and UI evidence showing reading room eligibility before paging is authorized.

### 10. Reading room request and paging workflow

**Justification:** Researchers need predictable paging windows, while staff need control over restricted, fragile, or oversized material. A simple request create path does not cover that operational reality.

**Improvement:** Split `archive_request` into request, review, pull, ready-for-use, in-use, returned, and exception states for reading room service. Support seat assignment, paging cutoffs, container limits per patron, and explicit handling for materials that require staff-mediated access.

**Acceptance evidence:** State-transition tests for the full reading room lifecycle, queue screens for pull lists, and a release scenario where fragile material is approved for supervised use only.

### 11. Hold queue logic for circulating collections

**Justification:** Holds are core public service behavior for circulating collections, yet the manifest currently exposes only loan creation. Without a true hold queue, staff cannot manage demand fairly.

**Improvement:** Add hold request modeling around `circulation_loan` and `collection_item` with first-in-first-out queues, pickup windows, branch or service-point routing, and priority rules for course reserves or internal operations. The workbench should show why one patron advanced ahead of another when an exception rule applies.

**Acceptance evidence:** Queue-ordering tests, pickup-expiry scenarios, and UI evidence showing hold rank, expiration date, and exception justification.

### 12. Renewal, recall, and overdue escalation

**Justification:** Circulation policy is more than checkout and return. Renewals, recalls, and overdue responses are where policy complexity usually surfaces.

**Improvement:** Extend `circulation_loan` rules so renewals consider existing holds, recalls can shorten due dates, and overdue escalation can trigger notices, service blocks, or staff review. Make the policy logic visible in both operator screens and assistant-generated explanations.

**Acceptance evidence:** Renewal denial tests, recall timeline fixtures, overdue escalation event traces, and workbench views showing exactly which rule affected the new due date.

### 13. Lost, damaged, and missing item workflow

**Justification:** Libraries and archives need different responses to missing circulating books, damaged media, and missing archival folders. A single “closed with issue” status hides needed operational detail.

**Improvement:** Add exception handling to `collection_item` and `circulation_loan` for claimed returned, lost, damaged, missing during inventory, and missing during reading room use. Record financial outcome, replacement decision, preservation referral, and any change to discovery visibility.

**Acceptance evidence:** Exception taxonomy tests, inventory reconciliation scenarios, and UI evidence showing the difference between lost-in-circulation and missing-in-processing cases.

### 14. Condition surveys for preservation planning

**Justification:** Preservation work should begin from documented condition, not ad hoc impressions. Condition survey data also informs access and digitization risk.

**Improvement:** Expand `preservation_action` intake to capture support type, brittleness, mold or pest indicators, fastener risk, media decay symptoms, housing quality, and handling restrictions. Link survey findings to preservation priorities and reading room restrictions.

**Acceptance evidence:** Condition coding tests, preservation survey forms in the UI, and seeded examples for brittle newsprint, acetate negatives, magnetic media, and bound volumes.

### 15. Conservation treatment proposal and approval flow

**Justification:** Not every preservation issue becomes treatment, and not every treatment should proceed without review. Staff need documented rationale, estimated impact, and post-treatment notes.

**Improvement:** Add a treatment proposal lifecycle to `preservation_action` covering recommendation, supervisor approval, treatment execution, outcome documentation, and post-treatment access change. Capture whether the goal was stabilization, repair, rehousing, or preparation for digitization.

**Acceptance evidence:** Approval-flow tests, treatment report exports, and release evidence with before-and-after condition narratives linked to the same item.

### 16. Environmental monitoring and risk thresholds

**Justification:** Preservation risk often emerges from temperature, humidity, light, and storage incidents rather than from item handling alone. The PBC should help staff connect environmental signals to collection risk.

**Improvement:** Add environmental event ingestion to `preservation_action` and `library_archives_management_control_assertion`, with thresholds for cold storage, vaults, general stacks, and exhibit spaces. Surface alerts that name the affected collections and the recommended response window.

**Acceptance evidence:** Threshold rule tests, simulated incident alerts, and control dashboards showing active environmental risks by storage location.

### 17. Digitization intake triage with preservation and rights checks

**Justification:** Digitization requests fail when teams discover too late that an item is fragile, restricted, oversized, or not adequately described. Triage must happen before capture work starts.

**Improvement:** Expand `digitization_job` intake to require source item linkage, condition status, handling requirements, rights status, target use case, and preferred output profile. Route requests into quick capture, conservation review, metadata cleanup, or rights review before a scanner slot is reserved.

**Acceptance evidence:** Triage decision tests, queue segmentation in the workbench, and end-to-end scenarios where preservation or rights review blocks capture scheduling.

### 18. Capture specification profiles and quality control

**Justification:** Imaging quality needs repeatable standards across text, photographs, oversize materials, audiovisual reformatting, and born-digital derivatives. Informal operator judgment is not enough.

**Improvement:** Add capture profiles to `digitization_job` for resolution, color target use, bit depth, file format, derivative bundle, and naming convention. Pair them with mandatory QC checkpoints for skew, clipping, focus, color fidelity, and completeness.

**Acceptance evidence:** Profile configuration tests, QC failure fixtures, and release evidence showing one job that passes QC and one that is returned for recapture with a clear reason.

### 19. OCR, HTR, transcription, and captioning workflow

**Justification:** Digitized access improves dramatically when text and audiovisual content become searchable and usable. Different source materials need different text-extraction strategies.

**Improvement:** Add sub-workflows under `digitization_job` for OCR on printed text, HTR on manuscripts, transcript review for oral histories, and caption generation for audiovisual material. Record confidence, reviewer intervention, and language metadata so discovery systems can present trustworthy access points.

**Acceptance evidence:** Output review tests, confidence-threshold routing, and sample release evidence for OCR, HTR, transcript, and caption outputs with approval history.

### 20. Fixity, checksum, and revalidation for digital objects

**Justification:** Preservation of digital files depends on proving that bits have not silently changed. Digitization and born-digital ingest both need repeatable fixity checks.

**Improvement:** Add checksum recording and scheduled revalidation to `digitization_job` and `preservation_action`, including repair escalation when a derivative no longer matches expected fixity. The UI should distinguish a failed checksum from a missing file or an intentionally replaced master.

**Acceptance evidence:** Checksum generation tests, scheduled revalidation fixtures, and audit evidence showing a failed fixity event opening a preservation exception.

### 21. Rights determination matrix by use case

**Justification:** Access decisions differ for on-site consultation, classroom use, web publication, commercial reuse, and internal preservation copying. A single generic `rights_statement` cannot explain those distinctions.

**Improvement:** Expand `rights_statement` so each record can express status by use case, jurisdiction, copyright basis, donor restriction, privacy concern, and review date. Make the decision matrix visible to operators, researchers, and assistant skills in the exact context of the requested use.

**Acceptance evidence:** Rights matrix tests, use-case-specific UI labels, and release scenarios where the same item is cleared for reading room consultation but denied for public web distribution.

### 22. Rights review expiry and scheduled reappraisal

**Justification:** Rights status is not static. Terms expire, legal interpretations shift, and new evidence changes what can be shared.

**Improvement:** Add review scheduling to `rights_statement` so staff can set trigger dates based on publication date, creator death date, donor clause expiry, or a local review commitment. Surface upcoming review work as an operational queue rather than burying it in record notes.

**Acceptance evidence:** Scheduled-review tests, aging queue views, and scenario coverage for expired embargoes automatically reopening public access review.

### 23. Sensitive content and access restriction handling

**Justification:** Archives often contain personal data, culturally sensitive knowledge, or legally restricted records. The PBC must support nuanced restriction without making materials disappear from internal control.

**Improvement:** Add restriction coding to `collection_item`, `catalog_record`, and `rights_statement` for privacy, cultural protocols, classified material, sealed records, and staff-only notes. The model should separate internal descriptive control from what patrons may see or request.

**Acceptance evidence:** Redaction tests, permission-aware discovery views, and release evidence showing one restricted archival series with an internal note that is hidden from patron-facing outputs.

### 24. Born-digital accession and forensic intake

**Justification:** Born-digital archives require storage imaging, directory capture, and media-specific risk handling that differ from physical accessioning. They cannot be treated as ordinary digitization jobs.

**Improvement:** Add born-digital accession support around `archive_request` and `preservation_action` for media imaging, write-blocking confirmation, filesystem capture, virus screening, and package-level metadata extraction. Record original carrier, transfer method, and chain-of-custody events.

**Acceptance evidence:** Born-digital intake scenarios, chain-of-custody audit logs, and evidence showing a disk image package flowing from accession to preservation review.

### 25. Reappraisal and deaccession governance

**Justification:** Collection stewardship includes deciding what should no longer be retained, transferred, or made available. Those actions need high scrutiny and complete provenance.

**Improvement:** Add a governed deaccession workflow for `collection_item` and accession groupings with reasons, authorizing policy, stakeholder review, and disposition outcome. Require explicit linkage to provenance, donor terms, and any legal hold before material can be withdrawn.

**Acceptance evidence:** Deaccession approval tests, blocked-withdrawal scenarios for restricted material, and release evidence showing retained audit history after removal from active holdings.

### 26. Collection-level processing plans and backlogs

**Justification:** Archival work is often managed at the collection or accession level long before every file receives item-level description. Staff need a way to see processing readiness and debt.

**Improvement:** Add collection-level processing plans tied to `collection_item` groupings, with target arrangement level, expected output, staffing estimate, backlog status, and blockers such as conservation or rights review. The workbench should distinguish unprocessed accessions from processed collections with published finding aids.

**Acceptance evidence:** Backlog rollup tests, collection dashboard views, and release scenarios showing one accession moving from unprocessed to minimally processed to fully described.

### 27. Bulk ingest and metadata remediation tools

**Justification:** Retrospective conversion, vendor metadata loads, and remediation projects require safe bulk work. One-record-at-a-time editing is not viable for large library or archival programs.

**Improvement:** Add bulk operations around `catalog_record` and `collection_item` for import, validation-only preview, controlled replacement, and rollback by job. Surface row-level errors, authority conflicts, and counts of records affected before approval.

**Acceptance evidence:** Bulk import test packs, preview-versus-commit comparisons, and UI evidence for row-level remediation with preserved job audit history.

### 28. Discovery-ready search facets and relevance controls

**Justification:** Good description still fails users if search cannot separate archival collections from library holdings, or rare materials from circulating copies. Discovery behavior needs explicit tuning.

**Improvement:** Add search projections over `catalog_record`, `collection_item`, and finding-aid structures with facets for format, date, creator, repository location, access status, and collection hierarchy. Provide ranking controls that privilege exact identifiers, controlled headings, and published finding-aid context over noisy free text.

**Acceptance evidence:** Search relevance tests, facet coverage scenarios, and release evidence showing the same query resolved differently for a manuscript collection, a circulating monograph, and a digitized oral history.

### 29. Public and staff note separation

**Justification:** Catalogers, archivists, and reading room staff need internal notes that should never leak into public discovery or external request confirmation. The PBC should enforce that boundary by design.

**Improvement:** Add note classes to `catalog_record`, `collection_item`, and `archive_request` for public note, staff note, processing note, conservation note, and donor-sensitive note. UI and agent skills must obey those visibility boundaries automatically.

**Acceptance evidence:** Visibility rule tests, role-specific detail views, and a release scenario proving staff-only notes stay hidden from patron-facing outputs and API responses.

### 30. Staff workbench for cataloging and processing decisions

**Justification:** The manifest lists a generic workbench, but library and archives operations need task-focused screens. Cataloging and processing staff should not navigate the same layout as circulation staff.

**Improvement:** Break `LibraryArchivesManagementWorkbench` into role-oriented panels for cataloging, accessioning, archival processing, preservation, rights review, circulation, and public services. Each panel should foreground its own queues, KPIs, and next safe actions rather than generic record lists.

**Acceptance evidence:** Route and permission tests for each panel, UI contract snapshots, and release evidence showing different default views for archivists, catalogers, and circulation supervisors.

### 31. Reading room operations dashboard

**Justification:** Reading room service is highly time-bound and exception-heavy. Staff need immediate visibility into arrivals, pulls, returns, and restricted-use supervision.

**Improvement:** Add a dedicated dashboard around `archive_request` for today’s appointments, due pulls, items currently in use, items overdue for return to storage, and restricted requests needing staff escort or approval. Include seat occupancy and paging cutoff status.

**Acceptance evidence:** Dashboard interaction tests, same-day service scenarios, and workbench screenshots showing the pull queue and in-use materials at once.

### 32. Circulation desk workflow improvements

**Justification:** Public library-style circulation needs fast scanning, hold fulfillment, and clear exception prompts. The current PBC surfaces do not yet prove that operator flow.

**Improvement:** Add a desk-oriented circulation panel for `circulation_loan` and `collection_item` with barcode lookup, hold shelf check-in, patron block warnings, renewal prompts, and lost-item exception handling. Optimize the path for rapid repetitive work without obscuring policy decisions.

**Acceptance evidence:** Desk-flow tests, keyboard-driven interaction coverage, and release evidence for checkout, hold pickup, renewal, and claimed-return workflows.

### 33. Finding aid editor with hierarchy-safe rearrangement

**Justification:** Archival editors routinely split series, reorder files, and update inherited dates or restrictions. Those changes are risky if the UI cannot preserve container and context relationships.

**Improvement:** Add a finding aid editor that lets staff drag and restructure hierarchical description while preserving identifiers, inherited metadata, and change history. Flag edits that would break container references or published citation anchors.

**Acceptance evidence:** Hierarchy integrity tests, conflict warnings during reordering, and published-output comparisons before and after a series rearrangement.

### 34. Researcher-facing request explanations and status language

**Justification:** Patrons need clear, domain-specific status language. “Pending” is too vague when the real cause is rights review, conservation review, paging schedule, or registration expiration.

**Improvement:** Add status explanation rules for `archive_request`, `circulation_loan`, and rights-limited access so each patron-visible message names the practical next step without exposing sensitive internal notes. Make those explanations consistent across UI and outbound notices.

**Acceptance evidence:** Status text approval fixtures, notification templates, and a release scenario showing distinct explanations for paging delay, restriction review, and expired registration.

### 35. Cataloging assistant skill with safe suggestion boundaries

**Justification:** Agent assistance is useful only if staff can trust where suggestions came from and what remained uncertain. Cataloging help must remain reviewable and reversible.

**Improvement:** Expand `LibraryArchivesManagementAssistantPanel` with a cataloging skill that proposes titles, extent notes, subject headings, creator matches, and summary notes from supplied evidence, but never commits changes without explicit operator approval. Each suggestion should cite the source span or authority record used.

**Acceptance evidence:** Suggestion trace tests, approval-required mutation checks, and UI evidence showing cited source excerpts alongside each proposed cataloging field.

### 36. Accessioning assistant skill for intake triage

**Justification:** Accessioning staff often work from transfer forms, emails, and hand-entered inventories. An assistant can accelerate the first pass if it stays inside governed intake rules.

**Improvement:** Add an accessioning skill that parses intake documents into draft `archive_request`, provenance, restriction, and quantity fields, then highlights what still requires human confirmation. The skill should also warn when a proposed accession appears to duplicate an existing unprocessed transfer.

**Acceptance evidence:** Intake parsing tests, duplicate-warning scenarios, and assistant review flows showing unresolved fields before any governed create command runs.

### 37. Reference and reading room assistant skill

**Justification:** Public services staff need quick answers about access eligibility, request status, and handling rules. Those answers must respect restrictions and current operational state.

**Improvement:** Add a reading room service skill that can explain request readiness, registration issues, seat availability, handling restrictions, and retrieval timing using `archive_request`, `rights_statement`, and `preservation_action` context. Limit the skill to explanation, draft actions, and approved command paths.

**Acceptance evidence:** Permission-aware response tests, blocked-answer cases for sensitive restrictions, and release evidence showing the assistant correctly distinguishes “request approved,” “awaiting pull,” and “consult conservation staff first.”

### 38. Rights and privacy review assistant skill

**Justification:** Rights review is repetitive but high risk. Staff need help gathering evidence without letting the assistant make unsupported clearance decisions.

**Improvement:** Add a rights review skill that assembles publication date clues, donor clauses, prior rights determinations, privacy flags, and scheduled review triggers into a structured recommendation for `rights_statement`. Require a human reviewer to confirm any externally visible rights change.

**Acceptance evidence:** Recommendation trace tests, reviewer signoff logs, and cases where the assistant correctly refuses to infer public domain status from incomplete evidence.

### 39. Provenance and authenticity evidence ledger

**Justification:** Provenance statements, custody changes, and digital authenticity checks are only useful if they remain verifiable over time. The PBC already names cryptographic audit proofing and event history as advanced capabilities; this domain needs to apply them concretely.

**Improvement:** Record provenance assertions, accession events, fixity events, and significant descriptive amendments in an immutable evidence ledger linked to `LibraryArchivesManagementUpdated` and `AuditEventSealed`. Present a human-readable chain that staff can review before approving access or publication.

**Acceptance evidence:** Replay tests for the evidence ledger, UI lineage views, and release evidence showing a single item’s path from accession through rights review, digitization, and researcher access.

### 40. Policy rule library for repository operations

**Justification:** Library and archival policy lives in circulation terms, reading room rules, donor restrictions, and preservation handling policies. Staff need rule behavior that is inspectable and testable.

**Improvement:** Expand `library_archives_management_policy_rule` so it can model hold limits, renewal caps, registration expiry, paging cutoffs, handling restrictions, digitization approval thresholds, and privacy-based redaction rules. Let operators simulate the effect of a proposed rule before activation.

**Acceptance evidence:** Rule simulation tests, versioned policy manifests, and release scenarios proving a changed hold policy affects new requests without rewriting historical transactions.

### 41. Runtime parameters for repository-specific operations

**Justification:** Different repositories have different service hours, retrieval windows, storage environments, and staffing realities. Hard-coded operational assumptions would make the package brittle.

**Improvement:** Use `library_archives_management_runtime_parameter` to control service point hours, hold shelf expiry, reading room paging intervals, QC tolerances, environmental alert thresholds, and automated reminder timing. Surface current effective values in the workbench and in release evidence.

**Acceptance evidence:** Parameter validation tests, effective-date scenarios, and screenshots showing runtime values alongside the queue or workflow they influence.

### 42. Controlled schema extension for local descriptive practice

**Justification:** Repositories often need local fields for collection priorities, donor language, indigenous data governance, or institutional workflows. They still need upgrade-safe boundaries.

**Improvement:** Use `library_archives_management_schema_extension` to register local fields and controlled vocabularies without weakening the core descriptive model. Require extensions to declare scope, target record type, validation, and whether the field is public, staff-only, or analytics-only.

**Acceptance evidence:** Extension registration tests, compatibility checks during schema evolution, and release evidence showing one local field added without breaking seed scenarios or exports.

### 43. Cross-event projections for operational readiness

**Justification:** Staff decisions depend on combined context from rights, preservation, circulation, and processing status. Separate record screens are not enough for day-to-day triage.

**Improvement:** Build projections that merge `collection_item`, `catalog_record`, `circulation_loan`, `digitization_job`, `rights_statement`, and `preservation_action` into readiness views such as “safe to circulate,” “safe to digitize,” “safe for reading room use,” and “ready for publication.” These projections should react to `OperationalKpiChanged` and policy events without manual reconciliation.

**Acceptance evidence:** Projection contract tests, freshness indicators in the UI, and release scenarios where a single rights or preservation change flips readiness status immediately.

### 44. Inventory, shelf reading, and discrepancy reconciliation

**Justification:** Collection control depends on periodic inventory. Libraries need shelf-reading support; archives need box and folder spot-checking with discrepancy follow-up.

**Improvement:** Add inventory workflows to `collection_item` for scan-based shelf checks, archival container audits, discrepancy classification, and follow-up assignment. Distinguish “mis-shelved,” “barcode mismatch,” “container missing,” and “intentionally relocated” outcomes.

**Acceptance evidence:** Inventory test packs, discrepancy queue views, and release evidence showing a mis-shelved circulating item and a missing archival folder handled through separate paths.

### 45. Notification and notice evidence for patrons and staff

**Justification:** Holds, recalls, reading room appointments, and rights-related denials all generate communication that should be explainable later. Notices are part of the service record.

**Improvement:** Add notice generation tied to `circulation_loan`, `archive_request`, and `rights_statement` so reminders, denials, recalls, and ready-for-pickup messages are templated, timestamped, and linked to the state change that caused them. Preserve both the rendered message and the policy basis.

**Acceptance evidence:** Notice template tests, delivery event logs, and release evidence showing message history attached to a hold pickup and a rights-based denial.

### 46. Service analytics and queue health metrics

**Justification:** Repository managers need more than raw counts. They need to know where service is slowing down and which queue is accumulating hidden risk.

**Improvement:** Use the existing analytics surfaces to expose hold fill rate, reading room turnaround time, accession backlog age, finding aid publication latency, digitization QC failure rate, and rights review overdue count. Pair those metrics with drill-down views into the records that drive them.

**Acceptance evidence:** Metric definition docs, analytics tests, and workbench evidence showing trend lines and drill-through links for each queue health indicator.

### 47. Realistic seed data across repository workflows

**Justification:** Domain credibility improves when generated apps ship with records that resemble real repository work, not abstract placeholders. Seed data also anchors QA and demo evidence.

**Improvement:** Expand `seed_data.py` coverage so it creates a mixed repository sample: circulating books with holds, an archival accession awaiting processing, a published finding aid, a restricted oral history, a conservation case, and a digitization request under rights review. Use those same fixtures across tests and release evidence.

**Acceptance evidence:** Seed-data smoke tests, deterministic fixture snapshots, and release evidence naming which sample records prove each major workflow.

### 48. Scenario-based release evidence for public services and stewardship

**Justification:** `RELEASE_EVIDENCE.md` should prove that the package handles patron service, collection stewardship, and archival control together. Domain claims without scenario evidence are weak.

**Improvement:** Structure release evidence around named scenarios such as “hold placed through checkout,” “researcher requests restricted collection,” “digitization blocked by rights review,” “finding aid published after processing,” and “born-digital accession enters preservation review.” Each scenario should map UI actions, API calls, emitted events, and resulting state.

**Acceptance evidence:** A traceability matrix from scenario to route, event, and table, plus reproducible run output showing the scenario passed in the current package build.

### 49. Control assertions for repository risk and compliance

**Justification:** The manifest already includes `library_archives_management_control_assertion`; it should reflect repository-specific controls rather than generic technical checks. Access, custody, and preservation risks need continuous monitoring.

**Improvement:** Add control assertions for overdue rights reviews, uncited provenance edits, missing fixity rechecks, reading room approvals without valid registration, loans issued to restricted items, and unpublished finding aids that reference missing containers. Failures should open actionable exceptions instead of passive reports.

**Acceptance evidence:** Control test fixtures, exception-opening event traces, and dashboards showing active and recently resolved control failures by category.

### 50. End-to-end release gate and traceability for the PBC

**Justification:** This package should not claim readiness until cataloging, accessioning, circulation, preservation, digitization, rights, reading room service, finding aids, provenance, UI, and agent skills are all evidenced together. Release quality depends on traceable proof, not only code presence.

**Improvement:** Build a package-level release gate for `library_archives_management` that maps every manifest surface to executable proof: APIs, workflows, emitted and consumed events, UI fragments, assistant skills, seed data, and operational scenarios. The final gate should fail if any domain-critical path lacks current evidence or if the backlog and evidence drift apart.

**Acceptance evidence:** A release checklist tied to `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`, a traceability report naming every covered surface, and current run output proving the gate passed on this package revision.
