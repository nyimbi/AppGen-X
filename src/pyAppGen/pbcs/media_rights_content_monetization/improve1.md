# Media Rights and Content Monetization Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `media_rights_content_monetization`.
- Manifest description: rights, licensing, distribution windows, royalties, usage tracking, revenue share, and content monetization.
- Current APIs: `POST /rights-assets`, `POST /license-agreements`, `POST /distribution-windows`, `POST /usage-records`, `POST /royalty-statements`, `GET /media-rights-content-monetization-workbench`.
- Owned tables: `rights_asset`, `license_agreement`, `distribution_window`, `usage_record`, `royalty_statement`, `revenue_share`, `territory_restriction`, `media_rights_content_monetization_policy_rule`, `media_rights_content_monetization_runtime_parameter`, `media_rights_content_monetization_schema_extension`, `media_rights_content_monetization_control_assertion`, `media_rights_content_monetization_governed_model`.
- Existing workflow surfaces: `media_rights_content_monetization_create_rights_asset_workflow` and `media_rights_content_monetization_record_license_agreement_workflow`.
- Existing UI fragments: `MediaRightsContentMonetizationWorkbench`, `MediaRightsContentMonetizationDetail`, and `MediaRightsContentMonetizationAssistantPanel`.
- Published events: `MediaRightsContentMonetizationCreated`, `MediaRightsContentMonetizationUpdated`, `MediaRightsContentMonetizationApproved`, and `MediaRightsContentMonetizationExceptionOpened`.
- Consumed events: `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Release evidence surfaces already declared in the manifest: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

## Improvement Backlog

### 1. Canonical rights grant model
**Justification:** The package needs one explicit representation of what is being granted so title, season, episode, clip, trailer, artwork, subtitle, dub, and promotional rights are not mixed together in free text.

**Improvement:** Extend `rights_asset` and `license_agreement` so every grant records rights type, grantor, grantee, exclusivity, language, version, edit type, and whether the right covers primary exploitation, marketing use, or derivative packaging.

**Acceptance evidence:** Schema fields and validation rules exist for grant dimensions, seeded fixtures show at least film, episode, clip, trailer, and artwork examples, and workbench detail views display the grant breakdown without manual interpretation.

### 2. Rights window versioning
**Justification:** Window dates change repeatedly during negotiations and amendments, and operators need a defensible history of what was active on any given day.

**Improvement:** Add first-class versioning for `distribution_window` so start, end, embargo, extension, and amendment history are tracked with superseded-by links and amendment reasons.

**Acceptance evidence:** A timeline view shows original and amended windows, replay tests confirm the active version at a prior date, and approval evidence references the exact window version applied to release decisions.

### 3. Territory hierarchy and rule inheritance
**Justification:** Rights often apply to country groups, regions, and exceptions, and flat territory codes cannot express "worldwide except Canada" or "LATAM excluding Brazil."

**Improvement:** Model hierarchical territories in `territory_restriction` with parent-child inheritance, inclusion lists, exclusion lists, and effective precedence for overrides and carve-outs.

**Acceptance evidence:** Territory test cases cover country, region, worldwide, and exclusion scenarios, and the UI can explain why a title is blocked or allowed in a specific market.

### 4. Platform and channel entitlement catalog
**Justification:** Monetization decisions depend on where content is exploited, and rights vary across SVOD, AVOD, FAST, TVOD, linear, inflight, hotel, social, and owned-and-operated apps.

**Improvement:** Introduce a controlled platform catalog linked to `distribution_window` and `license_agreement`, including platform family, channel class, playback mode, download permission, and offline-viewing entitlement.

**Acceptance evidence:** Platform codes are validated at intake, seeded examples span multiple monetization channels, and availability views can filter by platform family without ambiguous labels.

### 5. Availability state machine
**Justification:** Availability is not binary; titles move through pending ingest, awaiting clearance, ready, live, expired, suspended, and takedown-required states.

**Improvement:** Add an explicit availability lifecycle tied to `rights_asset` and `distribution_window`, including state transitions for prelaunch readiness, live activation, suspension, expiration, reinstatement, and permanent withdrawal.

**Acceptance evidence:** Transition tests reject invalid moves, workbench badges expose the lifecycle state, and audit output shows the actor and evidence behind each availability change.

### 6. Holdbacks and carve-out management
**Justification:** Premium windows, pay-one holdbacks, theatrical holdbacks, and partner carve-outs are central to rights exploitation and often cause accidental early releases.

**Improvement:** Create holdback entities linked to `distribution_window` with rule types for blackout period, platform exclusion, partner carve-out, and market-specific delay.

**Acceptance evidence:** Simulation cases show how a holdback delays launch, the detail UI explains active holdbacks per title, and release approval blocks when holdback conflicts remain unresolved.

### 7. Exclusivity and competitive blackout controls
**Justification:** Exclusive deals lose value when the same content or materially similar edits appear on conflicting channels.

**Improvement:** Encode exclusivity scope in `license_agreement` and add policy checks that compare title, asset family, edit lineage, platform family, territory, and time period to detect competitive overlap.

**Acceptance evidence:** Conflict tests catch duplicate exploitation during exclusive periods, exception tickets open automatically, and reviewers can see the competing grant that caused the block.

### 8. Licensing boundary between inbound and outbound rights
**Justification:** The package must distinguish rights acquired from licensors from rights granted downstream to distributors, partners, and ad-supported outlets.

**Improvement:** Separate inbound licensing obligations from outbound commercialization rights inside `license_agreement`, and prevent downstream grants that exceed acquired scope by territory, platform, language, or term.

**Acceptance evidence:** Validation rules fail oversized downstream deals, agreement detail pages show source-rights provenance, and evidence exports include the upstream agreement that authorizes each downstream exploitation.

### 9. Term calculation and renewal workflow
**Justification:** Rights terms depend on signature date, delivery date, first-air date, launch date, or satisfaction of conditions precedent, not just a static start/end pair.

**Improvement:** Support term anchors and renewal formulas in `license_agreement` and `distribution_window`, including auto-renewal, option exercise deadlines, and notice windows.

**Acceptance evidence:** Date-calculation tests cover signature-anchored and launch-anchored terms, renewal reminders appear before cutoff dates, and approval screens display the anchor logic used.

### 10. Royalty boundary between owed, accrued, paid, and disputed
**Justification:** Royalty accounting becomes unreliable when accruals, final statements, payments, and disputes are blended into one status field.

**Improvement:** Expand `royalty_statement` so each line can be marked as calculated, accrued, invoiced, payable, paid, disputed, reversed, or carried forward, with links to the triggering usage or revenue event.

**Acceptance evidence:** Statement fixtures show mixed line statuses in one cycle, dispute workflows keep disputed lines out of payable totals, and reconciliation reports clearly separate accrual from cash settlement.

### 11. Usage ingestion normalization by platform report type
**Justification:** Usage arrives from many partners in different granularities such as views, watch minutes, ad impressions, clicks, subscriptions, and bundle allocations.

**Improvement:** Create typed ingestion profiles for `usage_record` that normalize partner-specific files into a common usage vocabulary while preserving original source units and source file lineage.

**Acceptance evidence:** Test fixtures cover at least subscription, ad-supported, transactional, and linear usage reports, normalization logs show source-to-canonical mappings, and rejected rows surface precise reasons.

### 12. Revenue share waterfall engine
**Justification:** Revenue share is rarely a single percentage; it often follows floors, tiers, commissions, deductions, and recoupment priority.

**Improvement:** Model `revenue_share` as a waterfall with ordered stages for gross revenue, allowed deductions, minimum guarantee recoupment, partner splits, commissions, and residual holdbacks.

**Acceptance evidence:** Calculation tests cover tier changes and waterfall order, statement previews explain each step of the split, and adjustment entries are traceable back to the originating rule.

### 13. Minimum guarantee and recoupment tracking
**Justification:** Minimum guarantees determine when licensors begin sharing upside, and weak recoupment tracking distorts both partner payouts and internal forecasting.

**Improvement:** Add minimum guarantee balances, recoupment schedules, and recoupment priority rules to `license_agreement`, linked directly to `revenue_share` and `royalty_statement`.

**Acceptance evidence:** Balance reports show guaranteed amount, recouped amount, outstanding amount, and recoupment source, and tests verify that partner payouts change once recoupment is satisfied.

### 14. Ad-supported monetization rights
**Justification:** AVOD and FAST exploitation requires rights for ad insertion, ad load, ad categories, and monetization geography, not just playback rights.

**Improvement:** Add ad monetization flags and restrictions to `distribution_window` and `license_agreement`, including whether pre-roll, mid-roll, dynamic ad insertion, and programmatic monetization are permitted.

**Acceptance evidence:** Availability views distinguish playback rights from ad monetization rights, policy rules block unsupported ad modes, and evidence exports show the agreement clause authorizing ad-funded exploitation.

### 15. Sponsorship and branded-content constraints
**Justification:** Sponsored placement, presenting sponsorships, and branded slates can violate talent, sports, or editorial restrictions even when general AVOD is allowed.

**Improvement:** Capture sponsorship-specific restrictions for title, series, event, and package exploitation, including prohibited sponsors, prohibited industries, exclusivity promises, and approval-needed cases.

**Acceptance evidence:** Conflict rules reject forbidden sponsor pairings, assistant drafts ask for sponsor category before approval, and release evidence includes sponsor approval artifacts when required.

### 16. Promotional use and marketing-rights exceptions
**Justification:** Marketing teams often assume promo rights follow exploitation rights, but many agreements tightly limit clip length, still usage, and campaign duration.

**Improvement:** Add a promo-rights layer to `rights_asset` and `license_agreement` covering clip duration caps, still counts, artwork rights, trailer rights, and campaign term limits by territory and platform.

**Acceptance evidence:** The workbench shows a separate marketing-rights panel, promotional exports fail when clip duration exceeds the agreement, and sample approvals demonstrate legal signoff for exceptions.

### 17. Restriction clause registry
**Justification:** Rights restrictions are where most downstream mistakes occur, and burying them inside long-form agreement text makes them hard to enforce.

**Improvement:** Create a structured clause registry for `license_agreement` and `media_rights_content_monetization_policy_rule` covering language restrictions, rating restrictions, sponsor conflicts, exclusivity promises, embargoes, and content edits required for release.

**Acceptance evidence:** Intake extracts clauses into typed records, operators can search restrictions by clause type, and validation failures cite the exact structured clause that caused the block.

### 18. Takedown initiation and SLA management
**Justification:** When rights expire or are revoked, the package must drive fast takedown action across all markets and platforms with measurable response time.

**Improvement:** Introduce takedown workflows linked to `distribution_window`, `rights_asset`, and `usage_record`, including trigger source, platform targets, deadline, completion evidence, and escalation path.

**Acceptance evidence:** Takedown queues show due times and completion state, SLA timers breach when deadlines pass, and release evidence stores platform confirmations or unresolved exceptions.

### 19. Rights conflict detection across title lineage
**Justification:** Conflicts often happen between versions of the same content, such as director's cuts, compilations, dubbed edits, or branded collections, not just identical assets.

**Improvement:** Add lineage links among `rights_asset` records so conflict checks can compare parent title, cut, season, episode, language, edit family, and packaged derivative relationships.

**Acceptance evidence:** Seed data includes related edits and derivatives, overlap scans catch conflicts on lineage-related assets, and reviewers can open the exact relationship that triggered the exception.

### 20. Rights conflict resolution workbench
**Justification:** Detecting a conflict is only half the problem; rights teams need a guided way to decide amendment, delay, takedown, or waiver.

**Improvement:** Add a conflict-resolution area in `MediaRightsContentMonetizationWorkbench` with side-by-side comparison of overlapping grants, recommended next actions, approval chain, and final resolution type.

**Acceptance evidence:** UI flows support compare, assign, decide, and close actions, conflict tickets capture rationale and approver identity, and history views show how the chosen resolution changed downstream availability.

### 21. Chain-of-title evidence tracking
**Justification:** Monetization rights are only defensible when chain-of-title evidence shows uninterrupted authority from original owner to current exploiter.

**Improvement:** Attach chain-of-title documents, amendments, rights confirmations, and approval memos to `rights_asset` and `license_agreement`, with document type, issue date, issuer, and validity status.

**Acceptance evidence:** Assets cannot reach release-ready state without required evidence classes, audit exports include the chain-of-title packet, and exception queues surface missing or stale documents.

### 22. Derivative and package rights modeling
**Justification:** Collections, box sets, thematic channels, and clips packages often require separate rights decisions from the source titles they include.

**Improvement:** Model package rights and derivative exploitation as explicit entities connected to underlying `rights_asset` records, with inherited and overridden restrictions clearly separated.

**Acceptance evidence:** Package examples show inherited and overridden constraints, approval screens list every source title contributing rights, and conflict checks work at both package and component level.

### 23. Localization rights by language and material type
**Justification:** Subtitles, dubs, metadata translations, artwork localization, and title translations are monetizable rights surfaces with different restrictions.

**Improvement:** Extend `rights_asset` and `distribution_window` to capture language-specific rights for audio dub, subtitle, captions, descriptive audio, localized metadata, and localized artwork.

**Acceptance evidence:** Language-specific availability views exist, validation catches missing rights for dubbed launch plans, and sample evidence proves that subtitle-only rights do not unlock dubbed release.

### 24. Territory-platform availability calendar UI
**Justification:** Operators need a fast visual answer to when and where a title is available, blocked, or expiring across many territories and channels.

**Improvement:** Add a calendar and matrix view in `MediaRightsContentMonetizationWorkbench` that combines `distribution_window`, `territory_restriction`, and platform entitlements into one explorable grid.

**Acceptance evidence:** Users can filter by title, territory, and platform family, cell states explain block reasons, and expiring windows are visible without leaving the workbench.

### 25. Availability read model and API
**Justification:** Downstream release tooling and partner operations need a stable answer to "can I publish this asset here, now, on this platform?"

**Improvement:** Create an availability projection and query API that resolves rights state, territory inclusion, platform rights, restrictions, holdbacks, and takedown state into a single eligibility response.

**Acceptance evidence:** Query tests cover eligible and ineligible cases, the API response includes machine-readable reasons, and the workbench uses the same read model shown to external consumers.

### 26. Agent skill for agreement intake and clause extraction
**Justification:** Rights teams spend large amounts of time turning agreement language into structured records, and that work benefits from bounded automation with human review.

**Improvement:** Add an assistant skill in `MediaRightsContentMonetizationAssistantPanel` that drafts `license_agreement`, clause registry, and window records from uploaded deal documents while requiring confirmation before any write.

**Acceptance evidence:** Draft extraction previews cite source passages, confidence thresholds trigger review when low, and accepted drafts generate audit events tied to the approving user.

### 27. Agent skill for conflict triage and release readiness
**Justification:** Conflict queues become operational bottlenecks unless the assistant can prepare comparisons, collect missing evidence, and suggest next actions without taking irreversible steps.

**Improvement:** Add an assistant workflow that summarizes rights conflicts, missing chain-of-title documents, expiring windows, and unresolved takedowns, then proposes assignment and remediation steps.

**Acceptance evidence:** Assistant output contains conflict summaries with linked records, blocked actions remain blocked without approval, and audit logs show every suggestion accepted or rejected by a human reviewer.

### 28. Expanded domain event model
**Justification:** Generic create/update events do not tell other packages whether a window opened, a takedown started, or a royalty dispute was raised.

**Improvement:** Add typed events for agreement captured, window amended, availability activated, holdback asserted, takedown opened, takedown confirmed, royalty disputed, revenue share recalculated, and rights conflict detected.

**Acceptance evidence:** Event schemas are documented, example payloads exist for each event, and event-driven tests show downstream projections responding to the new event types.

### 29. Event idempotency and replay evidence
**Justification:** Rights operations cannot tolerate double takedowns, duplicate statements, or repeated revenue allocations when events are retried.

**Improvement:** Strengthen idempotent handling for usage, royalty, takedown, and availability events using deterministic dedupe keys, replay-safe projections, and explicit conflict handling for out-of-order delivery.

**Acceptance evidence:** Duplicate delivery tests prove no duplicate business effect, projection rebuilds match live state, and dead-letter records include actionable remediation metadata.

### 30. Release evidence bundle for rights decisions
**Justification:** Release approval should rest on a packaged evidence trail rather than scattered screenshots or oral signoff.

**Improvement:** Build a release-evidence bundle that captures governing agreement, active windows, territory and platform eligibility, restriction review, takedown status, and final approver decision for each release.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` references generated bundle artifacts, approval records link to the bundle, and audits can retrieve a complete release packet for a selected asset.

### 31. Royalty statement review workbench
**Justification:** Statement review needs its own workflow because analysts must inspect source usage, waterfall calculations, disputes, and payable totals together.

**Improvement:** Add a dedicated royalty-review view in `MediaRightsContentMonetizationDetail` showing statement lines, deduction rationale, recoupment state, partner share, and dispute annotations.

**Acceptance evidence:** Review screens support line drill-down, line-level dispute creation, and approval/reject actions, and seeded examples cover both simple percentage splits and waterfall-driven statements.

### 32. Revenue reconciliation across usage and payout
**Justification:** Usage data, recognized revenue, royalty output, and partner settlement must reconcile or finance trust breaks down quickly.

**Improvement:** Create reconciliation checks tying `usage_record`, `revenue_share`, and `royalty_statement` together by partner, title, territory, platform, and accounting period, with tolerances and exception routing.

**Acceptance evidence:** Reconciliation reports show matched and unmatched totals, threshold breaches open exceptions automatically, and tests verify that corrected usage restates downstream royalty values.

### 33. Avails import and export workflows
**Justification:** Distribution and syndication teams exchange avails constantly, and the package needs to represent what can be sold or launched in a format partners understand.

**Improvement:** Add avails import and export support derived from `rights_asset`, `distribution_window`, `territory_restriction`, and platform entitlements, including title metadata, territories, platforms, and rights notes.

**Acceptance evidence:** Round-trip tests prove that exported avails re-import cleanly, error reporting identifies invalid rows, and operators can export only release-ready avails.

### 34. Policy rules for prohibited rights combinations
**Justification:** Many violations come from unsafe combinations such as ad-supported rights without ad approval, dubbed release without dub rights, or worldwide release with excluded territories.

**Improvement:** Expand `media_rights_content_monetization_policy_rule` to express prohibited combinations, required companion rights, and mandatory review conditions for monetization scenarios.

**Acceptance evidence:** Policy simulations show triggered and non-triggered combinations, blocked approvals cite the rule hit, and policy history records who changed the rule and why.

### 35. Window overlap simulator
**Justification:** Schedulers need to know the impact of changing launch dates before they accidentally overlap exclusives, violate holdbacks, or create revenue gaps.

**Improvement:** Provide a simulator that compares proposed `distribution_window` changes against active windows, holdbacks, partner obligations, and territory exceptions without mutating production records.

**Acceptance evidence:** Scenario results show overlap warnings and safe alternatives, simulations can be attached to approvals, and tests confirm no persisted state changes from simulation runs.

### 36. Pricing floors and ad-yield guardrails
**Justification:** Some agreements require minimum rental price, minimum subscription allocation, or minimum ad yield before content can be monetized in certain channels.

**Improvement:** Add monetization floor controls to `license_agreement` and `revenue_share`, including minimum unit price, minimum CPM, minimum guarantee to licensor, and exception flow when economics fall below threshold.

**Acceptance evidence:** Calculation tests cover floor breaches, release planning views warn when monetization assumptions violate deal terms, and approval records show who authorized any override.

### 37. Sponsorship inventory reservation conflict checks
**Justification:** Sponsored slates and presenting sponsor inventory can be sold in advance, so rights decisions need to avoid double-booking or contractually prohibited sponsor placement.

**Improvement:** Add sponsorship reservation tracking linked to title, series, event, territory, platform, and sponsor category, with checks against rights restrictions and exclusivity promises.

**Acceptance evidence:** Reservation conflict scenarios are blocked before approval, the workbench shows committed sponsor inventory, and sponsor-facing evidence can be exported for approved reservations.

### 38. Takedown reversal and reinstatement controls
**Justification:** Some takedowns are temporary or issued in error, and reinstatement must be controlled so rights are not reactivated without evidence.

**Improvement:** Extend the takedown workflow with reversal requests, evidence review, partial reinstatement by territory or platform, and required approvals for reactivation.

**Acceptance evidence:** Tests cover full and partial reinstatement, audit history preserves the original takedown and reversal path, and availability states update correctly after reinstatement.

### 39. Ratings, regulatory, and audience restriction handling
**Justification:** Monetization rights can depend on local ratings, watershed rules, gambling or alcohol ad restrictions, and child-directed content limitations.

**Improvement:** Add structured restriction types for rating, audience, and regulatory constraints, and enforce them across territory, platform, ad mode, and sponsorship use cases.

**Acceptance evidence:** Territory-specific restriction examples are validated, blocked launches explain the local rule in force, and release evidence shows the rating or compliance artifact reviewed.

### 40. Rights expiry and sunset alerting
**Justification:** Expiring rights affect marketing, availability, finance forecasting, and takedown operations well before the actual end date.

**Improvement:** Implement alerting for upcoming expiry, renewal notice deadlines, holdback release dates, sponsorship end dates, and recoupment milestones using the existing event and workbench surfaces.

**Acceptance evidence:** Alert thresholds are configurable, users can see upcoming expiries by title and territory, and reminder events fire at the expected lead times in test scenarios.

### 41. Multi-tenant rights segregation
**Justification:** The package may serve multiple studios, distributors, or brands, and rights evidence must remain tenant-confined throughout intake, review, and export.

**Improvement:** Strengthen tenant scoping across `rights_asset`, agreements, windows, usage, statements, events, and evidence bundles so cross-tenant lookup, export, and assistant context are blocked by default.

**Acceptance evidence:** Isolation tests prove tenant A cannot see tenant B assets or evidence, assistant prompts stay tenant-bound, and audit logs show tenant identity on every sensitive action.

### 42. Bulk correction workflow for late source data
**Justification:** Cue sheets, usage files, and rights amendments often arrive late, forcing large corrections that need traceability and controlled restatement.

**Improvement:** Add bulk correction flows for `usage_record`, `distribution_window`, and `royalty_statement` with preview diffing, row-level validation, selective approval, and automatic downstream recalculation.

**Acceptance evidence:** Bulk correction jobs show accepted and rejected rows separately, recalculation events are emitted for affected statements, and audit history links every corrected record to the batch request.

### 43. Release readiness checklist
**Justification:** Teams need one shared release gate that checks rights, materials, restrictions, economics, and takedown risk before launch.

**Improvement:** Add a release-readiness checklist assembled from agreement validity, active windows, territory eligibility, platform rights, promo rights, ad rights, sponsorship restrictions, and chain-of-title completeness.

**Acceptance evidence:** Assets cannot be approved for launch while checklist items remain red, checklist snapshots are attached to approval evidence, and users can drill into the failing item from the workbench.

### 44. Domain KPI dashboard
**Justification:** Leadership needs a compact readout of rights risk, monetization readiness, and payout accuracy without drilling into record-level screens first.

**Improvement:** Build KPI projections for expiring rights, blocked launches, open conflicts, takedown SLA performance, royalty dispute rate, recoupment progress, and monetizable title inventory by channel.

**Acceptance evidence:** Dashboard metrics are defined and tested, drill-through routes land on the underlying queues, and KPI changes can be correlated with emitted operational events.

### 45. Exception taxonomy and ownership routing
**Justification:** Rights issues vary materially between missing paperwork, conflicting windows, invalid usage files, payout disputes, and emergency takedowns.

**Improvement:** Create a typed exception model with categories for rights evidence, availability conflict, territory rule, platform rule, economics, takedown, sponsor conflict, and royalty dispute, each with required owner roles and deadlines.

**Acceptance evidence:** Exceptions open with the right category and assignee defaults, SLA and escalation policies vary by exception type, and reporting can break down backlog by category and owner.

### 46. Seed data and test scenarios for real rights cases
**Justification:** Domain changes are hard to trust without fixtures that resemble actual rights operations rather than generic sample rows.

**Improvement:** Expand `seed_data.py` and contract tests with scenarios for exclusive SVOD windows, AVOD after holdback, dubbed-only rights, sponsor-blocked content, emergency takedown, and disputed royalty statements.

**Acceptance evidence:** Seeded records can drive the workbench end to end, tests cover each named scenario, and release evidence examples are generated from seeded cases.

### 47. Specification and backlog alignment
**Justification:** The improvement backlog should map cleanly to implementation and release artifacts so domain gaps are visible rather than implied.

**Improvement:** Update `SPECIFICATION.md` structure expectations for rights grant modeling, windows, territories, monetization rules, takedowns, conflict handling, assistant behavior, and evidence bundles so backlog items can trace into delivery work.

**Acceptance evidence:** Specification sections mirror the major domain areas in this backlog, requirement identifiers can be mapped to tests and events, and release evidence cites the implemented requirement IDs.

### 48. Cross-PBC boundary hardening with event contracts
**Justification:** Rights and monetization decisions influence other areas, but ownership breaks down when those integrations drift into table coupling or undocumented side effects.

**Improvement:** Define outbound and inbound contracts around availability, takedown, payout, and policy changes using the existing event surfaces and new typed events, keeping other packages outside owned tables.

**Acceptance evidence:** Contract tests verify event schemas and consumer expectations, no integration relies on direct reads from owned rights tables, and event lineage is visible from the workbench.

### 49. Evidence-based approval gates
**Justification:** Approval must mean the approver saw the specific facts required for a rights decision, not just clicked a generic approve button.

**Improvement:** Require approval screens to present the active grant, windows, territories, platform rights, restrictions, economics, open exceptions, and attached evidence before `MediaRightsContentMonetizationApproved` can be emitted.

**Acceptance evidence:** Approval flows fail when required evidence is missing, approver attestations are stored with the decision, and tests prove approval payloads include the supporting record references.

### 50. Post-release monitoring and rollback readiness
**Justification:** Rights launches need immediate observation because bad availability or monetization settings can create contractual breaches within minutes.

**Improvement:** Add post-release monitoring for unexpected territory exposure, ad mode violations, sponsor conflicts, usage spikes, missing revenue feeds, and takedown failures, plus a rollback playbook for suspension or takedown by scope.

**Acceptance evidence:** Monitoring alerts fire on seeded failure scenarios, rollback actions can target territory and platform subsets, and release evidence stores the monitoring outcome for the first hours after launch.
