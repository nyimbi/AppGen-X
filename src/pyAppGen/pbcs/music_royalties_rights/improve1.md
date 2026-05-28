# Music Royalties and Rights Improvement Backlog

## Current Domain Evidence Used

- The manifest names the stable PBC key as `music_royalties_rights`, describes the package as covering works, recordings, splits, licenses, usage, royalty statements, payments, and disputes, and exposes the current APIs `POST /musical-works`, `POST /recordings`, `POST /rights-splits`, `POST /licenses`, `POST /usage-reports`, and `GET /music-royalties-rights-workbench`.
- The current owned tables are `musical_work`, `recording`, `rights_split`, `license`, `usage_report`, `royalty_statement`, `rights_dispute`, plus policy, parameter, schema extension, control assertion, and governed model records.
- `domain_depth.py` currently centers the operational surface on `create_musical_work`, `record_recording`, `review_rights_split`, `approve_license`, `simulate_usage_report`, `create_royalty_statement`, and `record_rights_dispute`, which leaves several royalties-specific processes implicit rather than explicit.
- `events.py` shows emitted AppGen-X events `MusicRoyaltiesRightsCreated`, `MusicRoyaltiesRightsUpdated`, `MusicRoyaltiesRightsApproved`, and `MusicRoyaltiesRightsExceptionOpened`, with consumed events `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- `ui.py` confirms the current UI fragments `MusicRoyaltiesRightsWorkbench`, `MusicRoyaltiesRightsDetail`, and `MusicRoyaltiesRightsAssistantPanel`, with navigation sections for operations, edge-case triage, advanced intelligence, and release evidence.
- `agent.py` confirms a governed assistant surface with mutation previews, owned-table guardrails, and package-local skill namespace, which is the right base for repertoire ingestion, statement QA, and dispute support.
- `release_evidence.py` and `RELEASE_EVIDENCE.md` already organize release readiness into schema, services, events, handlers, UI, agent, and governance sections, but they do not yet prove royalties-domain completeness.

### 1. Canonical musical work identity and title governance
**Justification:** Royalty leakage starts when the same composition is entered under slightly different titles, writers, or local aliases. The current `musical_work` scope needs a canonical identity model that can survive retitles, translations, medleys, and controlled-title changes across territories.

**Improvement:** Expand work intake so each composition carries a canonical title, alternate titles, translated titles, work type, language, duration tolerance, version lineage, and external identifiers such as ISWC when available. Add explicit match confidence and duplicate-review queues before allowing a work to become statement-eligible.

**Acceptance evidence:** Test fixtures proving duplicate detection on near-match titles, a work detail view showing canonical and alternate titles, and release evidence that new work records cannot bypass title-governance checks before downstream split or usage processing.

### 2. Contributor identity ledger across composer, lyricist, arranger, and adapter roles
**Justification:** Splits cannot be trusted if contributor roles are flattened into a single free-text field. Music rights administration requires durable contributor identities because composer, lyricist, arranger, translator, and adapter claims drive different royalty flows and dispute outcomes.

**Improvement:** Add contributor records linked to each work with role type, legal name, professional name, IPI/CAE where present, share basis, contribution notes, and effective dates. Track whether the contributor is self-administered, publisher-administered, or society-administered for each right type.

**Acceptance evidence:** Schema and UI evidence that one work can hold multiple contributor roles without ambiguity, validation that total writer-side shares remain internally consistent, and release evidence demonstrating contributor-role capture in work creation flows.

### 3. Publisher, administrator, and sub-publisher chain-of-title modeling
**Justification:** Many royalty failures come from missing administration chains rather than missing works. A PBC that only stores a top-level publisher misses the territorial and right-type delegation needed for payment routing and license approval.

**Improvement:** Model publisher, administrator, and sub-publisher appointments as effective-dated relationships with territory, right type, collection scope, and termination terms. Make chain-of-title visible from the work and contributor views so operators can see who is entitled to approve licenses or receive statements.

**Acceptance evidence:** Effective-dated chain-of-title records in the owned schema, tests covering territorial handoffs and expired administrators, and workbench evidence that license review uses the correct current admin chain.

### 4. Split versioning with effective-dated rights ownership
**Justification:** Static split rows are not enough because catalog ownership changes over time. Statements and disputes need to reconstruct the split that was valid on the usage date, not the split visible today.

**Improvement:** Turn `rights_split` into a versioned ledger with proposed, approved, superseded, and disputed versions, plus effective-from and effective-to dates. Require an explicit reason code for each split change, including amendment, settlement, catalog acquisition, or court-directed correction.

**Acceptance evidence:** Replayable split history for a work, tests proving that statement generation selects the correct historical split version for a prior usage period, and release evidence tying split supersession to auditable events.

### 5. Split validation rules for writer, publisher, and recording-side shares
**Justification:** Music rights operations need more than a simple total-equals-100 check. Different rights buckets can have different share bases, and recording-side participation often differs from composition-side participation.

**Improvement:** Add rule packs that validate composer versus publisher shares, performance versus mechanical participation, and composition-side versus recording-side ownership. Flag impossible cases such as over-assigned publisher shares, missing writer shares, or a recording royalty setup with no master-side owners.

**Acceptance evidence:** Policy tests for common split edge cases, rule explanations visible in `MusicRoyaltiesRightsDetail`, and exception queues that distinguish missing-share issues from conflicting-share issues.

### 6. Recording-to-work linkage and controlled mismatches
**Justification:** Statements depend on linking sound recordings to the correct compositions, but many recordings legitimately point to multiple works or only partially match them. A shallow one-recording-to-one-work assumption will fail on live versions, samples, medleys, and derivative recordings.

**Improvement:** Introduce explicit recording-work link records with relationship types such as primary composition, interpolation, sample source, medley component, and derivative adaptation. Give operators a match-confidence queue for recordings that should not flow into statements until the linkage is resolved.

**Acceptance evidence:** Read models showing one recording mapped to multiple work claims where needed, matching tests for clean and ambiguous links, and release evidence that unmatched recording-work relationships open governed exceptions instead of silently passing through.

### 7. Recording version families for radio edit, live, acoustic, remix, and stem releases
**Justification:** Royalty systems need to differentiate a master recording from its commercial variants. Without version families, usage can be matched to the wrong asset and statements can misstate ownership or fee triggers.

**Improvement:** Add recording family structures that connect original masters with radio edits, clean versions, instrumental versions, live captures, remixes, localized releases, and stems. Track whether a variant inherits rights from its parent or carries unique producer or performer participations.

**Acceptance evidence:** Recording detail evidence that shows family trees and inheritance overrides, tests covering variant-specific rights, and usage-matching proof that a remix does not inherit the original master split when it should not.

### 8. Performer, producer, and neighboring-rights contributor capture
**Justification:** The current focus on works, recordings, and splits needs explicit neighboring-rights support to handle master-side royalties correctly. Featured artist, non-featured performer, producer, mixer, and session-player participation can drive separate statement lines and claim conflicts.

**Improvement:** Extend contributor capture on recordings to include performer class, producer points, neighboring-rights eligibility, union/session notes, and collection path. Make clear which participants are informational only and which create payable or reportable obligations.

**Acceptance evidence:** Recording-side contributor tables and UI panels, tests demonstrating separate participation on a master versus the underlying composition, and statement prototypes showing master-side payee breakdowns.

### 9. PRO and CMO affiliation registry for works and contributors
**Justification:** Performance royalty administration is incomplete without society affiliations. Composer, publisher, and neighboring-rights claims depend on current affiliations to PROs and CMOs, and those affiliations can vary by territory and right type.

**Improvement:** Create a registry for PRO and CMO affiliations tied to contributors, publishers, and recordings, including society name, member number, territory, rights administered, effective dates, and collection exclusions. Show affiliation gaps directly in work and recording readiness views.

**Acceptance evidence:** Validation that a work flagged performance-eligible cannot reach ready-for-statement status without society affiliation data or an explicit waiver, plus workbench evidence for affiliation completeness by territory.

### 10. Society conflict and territory-overlap detection
**Justification:** Duplicate or overlapping society appointments create downstream collection conflicts and disputes. Operators need early detection when two societies or administrators claim the same territory and right type for the same party.

**Improvement:** Add overlap detection for PRO, CMO, publisher-admin, and sub-publisher appointments by right bucket and territory. Present a territory heat map that highlights gaps, overlaps, and revoked appointments before license approval or statement generation.

**Acceptance evidence:** Conflict-detection tests for overlapping territories, a workbench panel that shows contested territories, and release evidence demonstrating automated exception creation for overlap scenarios.

### 11. License taxonomy covering mechanical, performance, sync, master, print, and promo use
**Justification:** The current `license` surface is too broad for real royalty operations because each license type drives different approvals, fee logic, and evidence requirements. Rights teams need to know exactly which rights were granted and which remain unlicensed.

**Improvement:** Break license records into explicit rights bundles with grant type, media type, territory, term, exclusivity, fee basis, royalty rate basis, and approval authority. Support hybrid deals where a sync grant also carries a master-use approval and backend royalty participation.

**Acceptance evidence:** License forms and API payloads that distinguish mechanical, performance, sync, and master rights, tests for invalid mixed-grant combinations, and workbench evidence that rights not granted remain visibly unlicensed.

### 12. License term, option, embargo, and holdback controls
**Justification:** A license that exists but is not in force can still cause an erroneous usage approval or payout. Music catalogs often depend on embargo windows, option periods, and media-specific holdbacks that need operational enforcement.

**Improvement:** Add license term schedules, option exercises, embargo start and end dates, media-specific holdbacks, and dependency checks against release dates and territory launches. Prevent usage approval from treating a future-dated or expired grant as active.

**Acceptance evidence:** Tests covering pre-release embargoes and expired options, UI warnings on licenses approaching expiry, and event evidence that license-state changes trigger recalculation of downstream readiness.

### 13. Cue sheet, setlist, and program metadata support for performance royalties
**Justification:** Performance royalties depend on source evidence, not just raw usage lines. Broadcast, live venue, and audiovisual performance income frequently requires cue sheets, setlists, or program logs before a claim or statement is defensible.

**Improvement:** Add evidence objects linked to works, recordings, and usage reports for cue sheets, setlists, program logs, and broadcaster certifications. Route them through the same governed intake surface as documents handled by `MusicRoyaltiesRightsAssistantPanel`.

**Acceptance evidence:** Document-ingestion traces that preserve source metadata, tests proving a performance statement line can reference its cue-sheet evidence, and release evidence showing governed storage of performance-source artifacts.

### 14. Mechanical royalty rate engine by format, territory, and deal basis
**Justification:** Mechanical royalties cannot be treated as one flat rule. Physical, download, and streaming mechanicals use different rate structures, and many catalogs override statutory norms through direct deals.

**Improvement:** Add a rate engine that can evaluate statutory-style rates, percentage-of-revenue deals, minimums, floors, caps, and per-unit rates by territory, format, and effective date. Store the exact rate source and decision path for every mechanical accrual.

**Acceptance evidence:** Calculation fixtures for physical units, downloads, and streaming mechanicals, statement line evidence showing the rate source used, and test coverage for deal overrides that supersede the default rate pack.

### 15. Performance royalty accrual rules for direct, society, and neighboring-rights flows
**Justification:** Performance royalties reach the catalog through multiple channels, each with distinct assumptions and evidence. The PBC needs to separate direct-licensed performance income from society-collected income and neighboring-rights collections.

**Improvement:** Add performance accrual modes that distinguish direct venue or broadcaster licenses, society-reported performance earnings, and neighboring-rights performance distributions. Track whether income is estimated, reported, or settled and whether it is composer-side, publisher-side, or recording-side.

**Acceptance evidence:** Statement prototypes showing separate performance buckets, rules that block accidental mixing of direct and society distributions, and audit-ready traces from usage source to performance accrual mode.

### 16. Sync fee and backend participation modeling
**Justification:** Sync deals often include both upfront fees and downstream backend royalties, and those components are governed by different splits. A single license fee field cannot support sync administration, approvals, or disputes.

**Improvement:** Add sync-specific data structures for quote request, approval chain, license execution, fee schedule, most-favored-nations notes, backend participation, and cue-based follow-on royalties. Tie sync usage back to the approved composition and master-use grants.

**Acceptance evidence:** License detail views showing upfront and backend components separately, tests for MFN-driven fee adjustments, and statement evidence linking sync backend lines to the originating sync license.

### 17. Usage ingestion contracts by source type
**Justification:** Usage reports arrive from digital services, broadcast sources, venues, distributors, and direct clients in incompatible shapes. A single `usage_report` object is not enough unless the source contract, normalization rules, and ingestion confidence are explicit.

**Improvement:** Define source-specific ingestion contracts for DSP statements, broadcaster logs, venue reports, direct licensee reports, and manual corrections. Store the original file fingerprint, source type, reporting period, line counts, unit conventions, and ingestion confidence.

**Acceptance evidence:** File-contract tests for multiple source types, a workbench ingestion queue grouped by source, and release evidence proving the original source fingerprint survives through to statement generation.

### 18. Usage line normalization, deduplication, and fingerprint matching
**Justification:** Raw usage lines are noisy and duplicate-heavy. If the PBC cannot normalize track titles, identifiers, units, and territory codes before matching, it will produce avoidable black-box income and false disputes.

**Improvement:** Add line-level normalization for identifiers, titles, territory codes, currencies, unit measures, and reporting periods, plus duplicate detection keyed by source fingerprint and line lineage. Use recording/work matching confidence rather than blind exact-match logic.

**Acceptance evidence:** Dedupe tests on repeated source loads, usage-line lineage records showing how a normalized line was derived, and exception evidence for lines that remain ambiguous after normalization.

### 19. Unmatched usage and black-box income triage
**Justification:** Unmatched usage is a core operating queue in music royalties, not an edge case. Teams need a controlled path to research, provisionally allocate, suspend, or reject unmatched income without losing traceability.

**Improvement:** Create a dedicated unmatched-usage queue with reason codes such as missing work, missing recording, conflicting split, missing affiliation, low-confidence match, or rights-territory conflict. Support provisional claim decisions with expiry dates and mandatory follow-up evidence.

**Acceptance evidence:** Queue views in `MusicRoyaltiesRightsWorkbench`, aging metrics by unmatched reason, and statement rules proving unmatched lines cannot become final payables without either resolution or a documented provisional policy.

### 20. Royalty run calendars, close rules, and statement-period controls
**Justification:** Statement quality depends on disciplined close rules. Without period-close logic, late usage, corrected splits, and delayed affiliations can leak into the wrong cycle and produce unstable statements.

**Improvement:** Add configurable royalty run calendars with preliminary, held, final, and reopened states for each accounting period. Tie period close to cutoffs for usage ingestion, split approval, license completeness, and dispute holds.

**Acceptance evidence:** Tests for late-arriving usage before and after close, workbench controls showing the state of each accounting period, and release evidence that reopened periods preserve a visible restatement reason.

### 21. Statement calculation traceability down to line and rule level
**Justification:** A statement that cannot be explained line by line will become a dispute magnet. Recipients need to see which usage lines, rates, splits, deductions, and policies created each payable amount.

**Improvement:** Turn `royalty_statement` into a traceable calculation package with statement headers, statement lines, source usage references, applied rates, split versions, deductions, reserves, and payee routing. Surface a human-readable explanation for every line in the statement detail UI.

**Acceptance evidence:** Drill-through from a statement line to its source usage and split version, test fixtures verifying deterministic recalculation, and release evidence that statement exports preserve calculation lineage.

### 22. Advances, recoupment, and cross-collateralization ledger
**Justification:** Catalog deals often recoup advances before money becomes payable, and those recoupment rules vary by contract. If recoupment sits outside the PBC, statements will be financially correct only by accident.

**Improvement:** Add contract-linked advance balances, recoupment buckets, cross-collateralization groups, and recoupment priority rules across works, recordings, or deal groupings. Show whether a statement line is earned, recouped, partially recouped, or payable after recoupment.

**Acceptance evidence:** Statement fixtures covering full recoupment, partial recoupment, and post-recoupment payouts, a ledger view for remaining advance balances, and dispute evidence that recoupment decisions can be reconstructed by period.

### 23. Reserves, holdbacks, suspense, and unapplied-cash handling
**Justification:** Not all earned royalties should be immediately payable. Operationally, teams need deliberate handling for reserves, pending ownership conflicts, minimum payment thresholds, and unapplied cash from incomplete source data.

**Improvement:** Add reserve rules, suspense buckets, minimum payout thresholds, and unapplied-cash queues with reason codes and release triggers. Separate held money caused by contractual reserves from money held because ownership is unresolved.

**Acceptance evidence:** Balance reports distinguishing reserve, suspense, and payable amounts, tests proving reserve releases follow the configured rule pack, and statement views showing held versus payable earnings clearly.

### 24. Deductions, administration fees, and pass-through cost governance
**Justification:** Recipients challenge statements when deductions are opaque or over-applied. The PBC needs explicit deduction categories rather than burying them in net calculations.

**Improvement:** Model administration commissions, sub-publisher commissions, society fees, banking costs, taxes, and approved pass-through expenses as typed deductions with basis, caps, and contractual justification. Require each deduction to point to the agreement or policy that authorizes it.

**Acceptance evidence:** Statement line traces showing gross, deduction, and net values, policy tests for capped fees, and release evidence that deductions without a rule or agreement reference are blocked from final statements.

### 25. Beneficiary and payment-instruction controls
**Justification:** Royalty accuracy is not enough if money is routed to the wrong beneficiary. Payee controls need to distinguish legal owner, administrator, payment recipient, and temporary collection account.

**Improvement:** Add beneficiary profiles with legal entity, payment method, banking status, payment currency, hold flags, and approval history. Make payment routing effective-dated so a statement reproduces the beneficiary instructions valid at issuance time.

**Acceptance evidence:** Tests for beneficiary changes mid-period, UI evidence showing the payment route history for a payee, and release evidence proving final statements cannot be approved when the beneficiary profile is incomplete or on hold.

### 26. Tax withholding, treaty treatment, and gross-up support
**Justification:** Royalty statements frequently cross borders, and withholding rules change the payable outcome. A PBC that ignores tax posture will force downstream manual correction and create payment disputes.

**Improvement:** Capture tax forms, residence claims, withholding percentages, treaty relief status, and gross-up clauses at the beneficiary or contract level. Apply tax logic as a transparent statement component rather than an opaque post-processing adjustment.

**Acceptance evidence:** Statement fixtures showing gross, withholding, and net payable values, validation that expired tax documentation triggers a hold, and release evidence that tax treatment is preserved in statement exports and audit traces.

### 27. Rights dispute intake for ownership, statement, and licensing conflicts
**Justification:** `rights_dispute` should distinguish what is being contested. Ownership conflicts, statement objections, license overreach claims, and society conflict notices have different evidence needs and resolution paths.

**Improvement:** Create dispute intake types for ownership claim, split objection, unmatched-usage objection, statement objection, unpaid-balance claim, licensing overreach, and society conflict. Require dispute intake to name the contested work, recording, statement period, or license record.

**Acceptance evidence:** Dispute intake forms with typed evidence requirements, tests showing dispute routing changes by dispute type, and release evidence that dispute records are linked to the exact contested domain object.

### 28. Dispute workflow, SLA, and evidence-preservation controls
**Justification:** Disputes become expensive when evidence is scattered and response times are ad hoc. Rights teams need disciplined workflow states and immutable evidence preservation from the first notice onward.

**Improvement:** Add dispute states such as received, under review, counter-evidence requested, on hold, resolved, settled, rejected, and escalated. Preserve every evidence item, note, calculation snapshot, and communication reference used during dispute handling.

**Acceptance evidence:** SLA timers and aging dashboards for disputes, immutable evidence snapshots attached to each workflow state, and tests proving that settlement or rejection closes the dispute with retained reasoning.

### 29. Restatement, reversal, and correction lineage
**Justification:** Corrections are inevitable in royalties administration, but opaque corrections destroy trust. Every corrected statement or reversed line needs a direct line back to the original error and the new decision.

**Improvement:** Add explicit correction objects that reference the original statement line, the reason for restatement, the affected period, and the net impact on each payee. Distinguish reversals caused by bad source usage from reversals caused by ownership changes or tax changes.

**Acceptance evidence:** Statement history views that show original, reversed, and corrected lines together, deterministic restatement tests, and release evidence that reopened periods emit visible correction events.

### 30. Catalog administration workspace and task ownership
**Justification:** Rights and royalty operations are continuous catalog administration work, not isolated transactions. Teams need a purpose-built workspace for onboarding, maintenance, renewals, issue follow-up, and release readiness across the repertoire.

**Improvement:** Add catalog administration queues for new works, pending registrations, expiring licenses, unmatched usage, open disputes, and incomplete beneficiary records. Support assignee, due date, escalation path, and workload balancing inside the package boundary.

**Acceptance evidence:** Workbench queues grouped by admin task type, operator metrics for backlog age and throughput, and release evidence that catalog tasks are package-local rather than hidden in ad hoc external lists.

### 31. Reversion, termination, and rights-sunset tracking
**Justification:** Rights do not last forever in a single shape. Catalog administration must account for contractual reversions, terminations, and sunset clauses that change who can license or collect income.

**Improvement:** Add rights-reversion schedules with trigger date, notice period, affected rights, affected territories, and successor ownership or administration path. Show upcoming reversions in the workbench before any new approval or statement cycle.

**Acceptance evidence:** Effective-dated reversion records, tests proving license approval respects sunset dates, and workbench alerts for rights due to revert within a configurable horizon.

### 32. Registration deliverables for works, recordings, and society updates
**Justification:** Good rights data still fails commercially if registrations are not submitted. Work registration, recording metadata delivery, and society updates should be first-class deliverables with their own completion evidence.

**Improvement:** Add registration tasks for work registrations, publisher updates, recording metadata deliveries, neighboring-rights enrollments, and society amendments. Track submission package, recipient, submission date, acknowledgment status, and exception reason.

**Acceptance evidence:** Catalog views that show registration status by asset and territory, tests for missing registration artifacts, and release evidence that registration completeness can be measured per catalog slice.

### 33. Mandatory evidence packages for splits, licenses, and statements
**Justification:** Rights operations are only as strong as their supporting evidence. A split without an agreement, a license without approval proof, or a statement without source lineage should never be treated as complete.

**Improvement:** Define evidence bundles by domain object: split support documents, chain-of-title artifacts, license approvals, rate references, source usage files, beneficiary documents, and dispute correspondence. Make readiness badges depend on evidence completeness, not just record presence.

**Acceptance evidence:** Evidence checklists rendered in `MusicRoyaltiesRightsDetail`, tests showing missing required evidence blocks approval, and release evidence that each major domain object has an evidence-completeness score.

### 34. AppGen-X emitted event expansion for rights-specific lifecycle changes
**Justification:** The current emitted event list is too coarse for rich downstream orchestration. Rights and royalties workflows need event granularity around split changes, statement issuance, dispute state changes, and registration actions.

**Improvement:** Expand the emitted event design so the package can distinguish work registered, split superseded, license granted, usage matched, statement issued, statement restated, dispute opened, dispute resolved, recoupment applied, and registration submitted. Keep them within the existing AppGen-X contract rather than introducing a new eventing model.

**Acceptance evidence:** Updated event manifest showing typed rights events, handler tests proving idempotent replay safety, and release evidence that each material domain transition maps to an emitted event with a stable payload contract.

### 35. Consumed-event handling for policy, audit, and KPI changes that affect royalty outcomes
**Justification:** The consumed events in the package should cause visible domain consequences. If `PolicyChanged`, `AuditEventSealed`, or `OperationalKpiChanged` arrive silently, operators cannot trust governance-driven recalculations.

**Improvement:** Define rights-specific reactions for consumed events, such as reopening license approval when a policy pack changes, sealing a statement period when audit evidence is finalized, or escalating unmatched-usage queues when KPI breach thresholds are crossed. Preserve lineage from the consumed event to the affected work, recording, statement, or dispute records.

**Acceptance evidence:** Idempotent handler tests tied to concrete domain effects, trace views showing why a record changed after a consumed event, and release evidence proving consumed events do not mutate unrelated domain objects.

### 36. Dead-letter, replay, and reconciliation operations for usage and statement events
**Justification:** Dead-letter queues in royalties systems are operationally material because missed usage or failed statement events delay money. Teams need to see which usage batches or statement transitions failed and what replay will change.

**Improvement:** Add dead-letter classifications for usage ingestion failure, match failure, statement projection failure, notification failure, and downstream acknowledgment failure. Support guarded replay with before-and-after previews so operators understand whether replay will change statements, disputes, or balances.

**Acceptance evidence:** A dead-letter triage panel in the workbench, replay preview tests for safe and unsafe retries, and release evidence that replay actions are captured with operator identity and result summaries.

### 37. Repertoire-focused workbench redesign
**Justification:** `MusicRoyaltiesRightsWorkbench` should feel like a repertoire administration console, not a generic table browser. Operators need to pivot quickly between works, recordings, contributors, registrations, statements, disputes, and admin queues.

**Improvement:** Redesign the workbench around repertoire views such as catalog health, registration gaps, split conflicts, unmatched usage, open disputes, upcoming renewals, and statement readiness. Keep the existing fragment names but make their default navigation speak the language of repertoire management.

**Acceptance evidence:** UI contract updates showing repertoire-first navigation, screenshots or UI tests demonstrating new queue groupings, and release evidence that key music-rights workflows are reachable without raw-table navigation.

### 38. Statement explainer UI with drill-through from payee to source line
**Justification:** Statement recipients and operators both need explainability. A good statement UI should answer where the money came from, why it was split that way, what was held back, and whether recoupment or tax altered the amount.

**Improvement:** Add statement detail views that can drill from payee summary to statement line, from statement line to usage source, and from usage source to rate and split decision. Highlight held, recouped, taxed, disputed, and corrected components distinctly.

**Acceptance evidence:** UI tests for statement drill-through, evidence that every statement line exposes rate, split, and usage lineage, and release evidence that statement exports remain reconcilable to the on-screen explainer.

### 39. Dispute cockpit UI for investigation and resolution
**Justification:** Rights disputes require side-by-side evidence review. Operators need a cockpit that compares the claimant’s position with current ownership, statement history, source usage, and license evidence without assembling the case manually.

**Improvement:** Add a dispute cockpit with timeline, contested assets, evidence bundles, statement impacts, ownership snapshots, proposed resolution notes, and approval actions. Make the cockpit accessible from both the dispute queue and the affected work, recording, or statement records.

**Acceptance evidence:** UI tests covering dispute evidence comparison, workflow actions that preserve resolution notes, and release evidence that the cockpit can render the full dispute package for at least one seeded scenario.

### 40. Agent skill for contract and registration extraction
**Justification:** The current assistant surface is governed, but it is still too generic for rights work. Teams need an agent skill that can extract contract terms, registration details, territories, right types, and approval obligations from documents without mutating data blindly.

**Improvement:** Add a package-local agent skill that parses agreements, split sheets, cue sheets, registration confirmations, and society notices into structured previews for human review. Limit the skill to extraction, confidence scoring, and mutation preview until a user confirms the result.

**Acceptance evidence:** Agent tests showing document-to-preview extraction for multiple rights documents, UI evidence that previews are reviewable in `MusicRoyaltiesRightsAssistantPanel`, and release evidence that no mutation occurs without explicit confirmation.

### 41. Agent skill for split validation and conflict drafting
**Justification:** Split conflicts often require structured operator support rather than raw automation. The assistant should help explain why a split is invalid and draft the follow-up needed to resolve it.

**Improvement:** Add a skill that inspects proposed split versions, explains rule failures, compares them with prior approved splits, and drafts outreach or internal resolution notes. Keep the assistant inside package boundaries by referencing only owned split, work, and contributor data.

**Acceptance evidence:** Agent fixtures showing invalid split explanations, governed draft-generation evidence for conflict notes, and permission tests proving the skill cannot bypass split approval controls.

### 42. Agent skill for statement QA, leakage explanation, and dispute prep
**Justification:** Statement review is a high-volume reasoning task where a well-governed assistant can reduce manual effort without taking approval authority away from operators. The skill should explain anomalies, not merely summarize records.

**Improvement:** Add a statement QA skill that flags unusual deltas, explains missing income versus prior periods, highlights recoupment changes, and assembles a dispute-prep packet from source lines, split history, and beneficiary changes. Route all outputs through reviewable assistant artifacts.

**Acceptance evidence:** QA scenarios showing anomaly explanations on statement drafts, operator-reviewed dispute packets assembled by the agent, and release evidence that generated packets cite only package-local facts and evidence objects.

### 43. Agent skill for catalog administration follow-up
**Justification:** Catalog administration involves repetitive but sensitive follow-up on missing registrations, incomplete affiliations, and expiring deals. An assistant can help drive these tasks if its scope and write permissions stay constrained.

**Improvement:** Add a catalog-admin skill that proposes follow-up tasks, drafts reminder notes, groups missing evidence by account or territory, and prioritizes work based on statement impact. Keep write actions behind explicit confirmation and preserve the proposed action log.

**Acceptance evidence:** Queue-prioritization examples generated by the skill, approval-gated task creation evidence, and release evidence showing assistant actions are logged with reason and outcome.

### 44. Predictive leakage, underpayment, and anomaly scoring
**Justification:** The package already advertises predictive risk and anomaly capability, but the backlog should tie that capability to concrete music-rights leakage patterns. Operators need signals for missing registrations, abnormal statement swings, duplicate usage, and under-collected territories.

**Improvement:** Train package-local scoring features around unmatched usage rates, registration gaps, sudden split changes, beneficiary holds, statement reversals, and delayed source ingestion. Score leakage risk by catalog slice, source, territory, and payee rather than only by record type.

**Acceptance evidence:** Feature manifests for leakage scoring, calibrated risk views in the workbench, and backtests showing the score identifies seeded underpayment and duplicate-usage scenarios with explainable reasons.

### 45. Release evidence upgraded from technical readiness to royalties-domain proof
**Justification:** `RELEASE_EVIDENCE.md` currently proves the package exists and its contracts load, but not that it is ready for actual rights administration. Domain release evidence should prove repertoire, statement, dispute, and registration scenarios end to end.

**Improvement:** Extend release evidence to include seeded work, recording, split, license, usage, statement, dispute, recoupment, and registration scenarios with expected outcomes. Add explicit evidence sections for rights completeness, calculation traceability, dispute reproducibility, and agent safety.

**Acceptance evidence:** A release evidence bundle showing at least one complete lifecycle from work intake to statement issuance and dispute resolution, plus machine-verifiable checks for those scenario outcomes.

### 46. Schema expansion for missing rights entities and evidence tables
**Justification:** The manifest’s current table list is a useful core, but deeper music-rights administration needs more explicit structures. Without dedicated tables for contributors, affiliations, registrations, statement lines, and recoupment balances, too much logic stays hidden in payload blobs.

**Improvement:** Add owned tables for contributors, contributor affiliations, registration submissions, statement lines, calculation traces, recoupment balances, reserve balances, beneficiary instructions, and evidence artifacts. Keep everything within the `music_royalties_rights_` namespace and package-local migration boundary.

**Acceptance evidence:** Migration plans and schema contracts for the new tables, tests proving foreign-table mutation is still disallowed, and release evidence that deeper domain records remain discoverable through typed read models.

### 47. Territory and policy packs by right type
**Justification:** Music rights rules vary heavily by territory and right type. A single policy layer for all royalties will not hold up when societies, statutory assumptions, tax posture, and licensing limits differ market by market.

**Improvement:** Add territory-aware policy packs for mechanical, performance, sync, master, and neighboring-rights processing, plus parameter packs for close calendars, materiality thresholds, and dispute SLAs. Make policy provenance visible whenever it affects a statement or approval outcome.

**Acceptance evidence:** Tests comparing the same catalog asset under different territory packs, UI evidence that affected records show the policy pack in force, and release evidence that policy changes trigger re-evaluation only where relevant.

### 48. Operational rehearsals with seeded catalog portfolios
**Justification:** Rights software often looks complete until it meets a realistic catalog. Release readiness should include rehearsal datasets that cover co-writes, sub-publishing, remixes, partial ownership, unmatched usage, recoupment, and dispute scenarios.

**Improvement:** Create seeded portfolio scenarios representing common and difficult catalogs: a self-published songwriter, a co-published work with split changes, a label catalog with producer points, a sync-heavy catalog, and a dispute-heavy legacy catalog. Use these scenarios across services, UI, agent, and release evidence checks.

**Acceptance evidence:** Seed data manifests for the rehearsal catalogs, scenario-based tests spanning workbench and statement generation, and release evidence reporting pass or fail by seeded portfolio rather than by abstract contract only.

### 49. Audit-proof hashes for statement, dispute, and evidence artifacts
**Justification:** The package already points toward cryptographic audit proofs, but the backlog should tie them to royalty-sensitive outputs. Statements, dispute packets, and evidence bundles need tamper visibility because they are the records parties rely on commercially and legally.

**Improvement:** Hash and seal statement exports, dispute evidence bundles, calculation traces, and registration submission packages with reproducible package-local proofs. Show proof status in the detail views so operators can confirm whether an artifact matches the sealed version.

**Acceptance evidence:** Proof-verification checks on exported statement and dispute artifacts, UI badges for sealed versus changed artifacts, and release evidence that proof generation and verification work on the seeded lifecycle scenarios.

### 50. Go-live scorecard for repertoire, royalties, disputes, UI, agent, events, and release evidence
**Justification:** The package needs a single readiness view that reflects domain truth, not only technical boot success. Teams should be able to answer whether the PBC is ready to administer a real catalog across works, recordings, splits, licenses, usage, statements, disputes, and collections.

**Improvement:** Build a go-live scorecard that measures canonical work coverage, split completeness, affiliation completeness, registration readiness, usage match rate, statement explainability, dispute reproducibility, recoupment accuracy, UI coverage, agent safety, event completeness, and release-evidence completeness. Use the scorecard as the final gate before promoting the package as production-ready for music-rights administration.

**Acceptance evidence:** A workbench scorecard panel, release evidence exporting the scorecard with seeded scenario results, and package tests that fail when a required readiness dimension falls below its defined threshold.
