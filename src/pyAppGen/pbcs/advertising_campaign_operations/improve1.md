# Advertising Campaign Operations Improvement Backlog

This backlog replaces scaffold content with a single hand-curated, advertising-specific improvement set for the `advertising_campaign_operations` PBC.

## Current Domain Evidence Used

- Exact manifest key: `advertising_campaign_operations`.
- Manifest description: campaigns, budgets, audiences, placements, creative approvals, performance, billing, and optimization.
- Owned tables named in the manifest: `ad_campaign`, `audience_segment`, `media_placement`, `creative_asset`, `campaign_budget`, `performance_result`, `billing_event`, `advertising_campaign_operations_policy_rule`, `advertising_campaign_operations_runtime_parameter`, `advertising_campaign_operations_schema_extension`, `advertising_campaign_operations_control_assertion`, and `advertising_campaign_operations_governed_model`.
- Public APIs named in the manifest: `POST /ad-campaigns`, `POST /audience-segments`, `POST /media-placements`, `POST /creative-assets`, `POST /campaign-budgets`, and `GET /advertising-campaign-operations-workbench`.
- Emitted events named in the manifest: `AdvertisingCampaignOperationsCreated`, `AdvertisingCampaignOperationsUpdated`, `AdvertisingCampaignOperationsApproved`, and `AdvertisingCampaignOperationsExceptionOpened`.
- Consumed events named in the manifest: `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.
- Existing UI fragments named in the manifest: `AdvertisingCampaignOperationsWorkbench`, `AdvertisingCampaignOperationsDetail`, and `AdvertisingCampaignOperationsAssistantPanel`.
- Existing workflows named in the manifest: `advertising_campaign_operations_create_ad_campaign_workflow` and `advertising_campaign_operations_record_audience_segment_workflow`.

### 1. Canonical campaign brief and objective model

**Justification:** Campaign execution quality falls apart when the brief is just free text and operators interpret objectives, audience promises, and success metrics differently.

**Improvement:** Add a structured campaign brief model for objective, offer, audience promise, channels, primary KPI, guardrails, and launch dependencies so every `ad_campaign` starts from a shared planning record instead of improvised notes.

**Acceptance evidence:** Brief templates render in the workbench, required fields block incomplete launch requests, and tests prove the same brief produces the same draft campaign shape across repeated submissions.

### 2. Flight plan and channel-mix planning

**Justification:** Advertising teams need an explicit record of when spend should start, peak, pause, and taper across channels or pacing conversations become guesswork.

**Improvement:** Extend campaign planning to capture flight windows, channel mix, daypart intent, geo splits, and planned ramp curves for each campaign so media buying and pacing share one source of truth.

**Acceptance evidence:** Flight-plan views appear in the detail page, plan changes are versioned, and scenario tests compare planned versus adjusted mix before launch approval.

### 3. Media buying package negotiation and hold ledger

**Justification:** Inventory reservations, rate negotiations, and publisher holds are core buying work, yet they are usually lost in email and never reconciled to final placements.

**Improvement:** Add a buying ledger that records negotiated packages, rates, hold expiries, seller contacts, make-good promises, and approval status for each proposed `media_placement`.

**Acceptance evidence:** Buyers can see open holds and expired options in one queue, package changes are auditable, and launch cannot proceed when required inventory holds have lapsed.

### 4. Budget versioning, reserves, and commitment tracking

**Justification:** Campaign budgets change constantly, and without versioned reserve logic it is impossible to explain why approved spend diverged from booked spend.

**Improvement:** Model `campaign_budget` as a versioned object with working budget, approved budget, committed budget, held reserve, contingency reserve, and released reserve values tied to campaign milestones.

**Acceptance evidence:** Budget diffs show who changed what and why, reserve releases require the right approval path, and reconciliation tests prove no placement can commit above approved available funds.

### 5. Daily and weekly pacing guardrails

**Justification:** Overspend and underdelivery are the operational failures users feel first, so pacing has to be a first-class control rather than a downstream report.

**Improvement:** Build pacing controls that compare actual spend and delivery against daily, weekly, and flight-to-date targets, with configurable tolerance bands and automated exception opening when variance persists.

**Acceptance evidence:** The workbench shows pacing heatmaps, persistent variance triggers exceptions, and tests cover overspend, underdelivery, and controlled recovery after manual intervention.

### 6. Creative brief-to-asset lineage

**Justification:** Creative operations need to know which approved brief produced which asset set, otherwise performance and compliance reviews cannot trace intent to execution.

**Improvement:** Connect each `creative_asset` to its originating brief, requested message angle, required disclosures, target audience, format constraints, and revision chain from first draft to final approved export.

**Acceptance evidence:** Asset detail views show revision lineage, superseded assets are visibly marked, and launch validation fails when a placement references an asset without approved brief lineage.

### 7. Multi-stage creative approval matrix

**Justification:** Creative approval is rarely one click; brand, legal, regulatory, and client sign-off often occur in a specific order with different evidence requirements.

**Improvement:** Add approval matrices for `creative_asset` that define required approver roles, serial versus parallel steps, conditional review paths, rejection reasons, and expiry rules for stale approvals.

**Acceptance evidence:** Approval queues show stage ownership, rejection comments remain attached to the asset version they refer to, and tests prove that missing approvals block trafficking.

### 8. Audience eligibility, suppression, and recency rules

**Justification:** Audience targeting quality depends on who is explicitly excluded as much as who is included, especially for churn, remarketing, and conversion campaigns.

**Improvement:** Expand `audience_segment` governance with inclusion criteria, suppression lists, recency windows, exclusion precedence, audience freshness timestamps, and approval for high-risk targeting combinations.

**Acceptance evidence:** Segment previews show included and suppressed counts, stale audiences raise warnings before launch, and rules tests prove exclusion precedence is deterministic.

### 9. Audience overlap and saturation analysis

**Justification:** Separate audience segments can look correct individually while competing against each other and driving waste through overlap and frequency saturation.

**Improvement:** Add overlap analysis that estimates shared reach across selected `audience_segment` records and flags likely cannibalization before media plans are approved.

**Acceptance evidence:** Planners can compare overlap matrices in the workbench, launch checks warn when overlap exceeds policy thresholds, and simulation tests show projected reach loss from duplicate targeting.

### 10. Geo, daypart, device, and placement context targeting

**Justification:** Targeting logic needs the same depth as real buying decisions or operators will work around the PBC for the settings that matter most.

**Improvement:** Extend targeting controls to represent geo hierarchy, daypart windows, device preferences, placement environment, language, and context suitability constraints at campaign and placement level.

**Acceptance evidence:** Trafficking screens expose the targeting dimensions cleanly, invalid targeting combinations are rejected at validation time, and API fixtures cover mixed-scope overrides.

### 11. Frequency cap and reach governance

**Justification:** Aggressive delivery can damage performance and brand perception if frequency is unmanaged, especially across overlapping placements and channels.

**Improvement:** Add campaign and placement level reach goals, frequency cap policies, reset windows, and conflict detection so planners can reason about exposure management before launch.

**Acceptance evidence:** Reach and frequency settings appear in planning and activation views, policy violations raise pre-launch issues, and tests prove caps are enforced consistently across repeated updates.

### 12. Placement trafficking readiness checklist

**Justification:** Many campaign failures are not strategic mistakes; they are trafficking misses such as wrong sizes, missing tags, or incomplete placement instructions.

**Improvement:** Add a trafficking checklist for each `media_placement` covering placement IDs, ad sizes, assets attached, URLs, tracking parameters, flight dates, targeting alignment, and external delivery instructions.

**Acceptance evidence:** Placements cannot move to ready state with missing checklist items, traffickers get a dedicated readiness queue, and tests cover the most common incomplete-placement failures.

### 13. Tracking tag, pixel, and UTM governance

**Justification:** Attribution disputes usually begin with inconsistent tracking definitions rather than with reporting math.

**Improvement:** Create a governed layer for tags, pixels, conversion events, landing URLs, and UTM conventions so every placement knows which measurement payloads are required before activation.

**Acceptance evidence:** Validation catches missing or malformed tracking settings, approved tag bundles are reusable across placements, and release evidence includes the tracking configuration attached to launch.

### 14. Conversion event dictionary and ownership

**Justification:** Teams cannot compare campaign performance if “conversion” means a different action in each workflow, dashboard, or partner feed.

**Improvement:** Maintain a controlled event dictionary that defines billable actions, optimization events, reporting events, and source-of-truth ownership for each conversion type used by `performance_result`.

**Acceptance evidence:** Performance views link metrics back to named dictionary entries, duplicate event definitions are blocked, and tests prove reporting uses the correct event mapping for each campaign.

### 15. Attribution window and model version control

**Justification:** Results change materially when attribution windows or weighting rules change, so the operating system has to preserve which model was in force at the time.

**Improvement:** Version attribution settings by campaign and reporting period, including view-through and click-through windows, reattribution rules, and default model selection for performance reporting.

**Acceptance evidence:** Historical reports can be regenerated with the original attribution version, model changes require approval when campaigns are active, and tests prove prior reports remain reproducible.

### 16. Experiment design registry for creative and audience tests

**Justification:** Advertising experimentation becomes noisy when hypotheses, holdouts, and success criteria are undocumented or spread across separate tools.

**Improvement:** Add an experiment registry that records hypothesis, test cells, control cell, exposure split, success metric, stopping rule, and decision owner for creative, audience, and placement experiments.

**Acceptance evidence:** Experiment cards link to the affected campaigns and assets, invalid overlapping test setups are flagged, and post-test decisions are stored with the evidence that supported them.

### 17. Creative fatigue and rotation monitoring

**Justification:** Strong creative performance decays over time, and operations teams need to know when to rotate assets before results collapse.

**Improvement:** Build fatigue monitoring that looks at spend, impressions, CTR, conversion rate, and recency by `creative_asset` to recommend rotation, refresh, or retirement actions.

**Acceptance evidence:** The workbench surfaces fatigue signals next to active placements, rotation recommendations cite the underlying trend, and tests cover assets that recover after replacement.

### 18. Brand safety controls and adjacency policy packs

**Justification:** Brand safety is not just a publisher blacklist; it includes content adjacency, category exclusions, and escalation rules when inventory quality changes mid-flight.

**Improvement:** Model brand safety policies with exclusion categories, block lists, allow lists, adjacency requirements, escalation severity, and fallback buying guidance for affected placements.

**Acceptance evidence:** Policy packs can be assigned to campaigns, unsafe inventory creates explainable exceptions, and consumed `PolicyChanged` events update affected campaign warnings without manual cleanup.

### 19. Supplier and publisher qualification response

**Justification:** Buying teams need operational reactions when a supply source is newly approved, downgraded, or disqualified, not just a passive record that something changed elsewhere.

**Improvement:** Handle `SupplierQualified` updates by recalculating placement eligibility, flagging impacted campaigns, and routing review tasks to buyers when an in-flight or planned placement depends on that supplier.

**Acceptance evidence:** Qualification changes create visible review items, impacted placements show before-and-after eligibility status, and handler tests prove duplicate supplier events remain idempotent.

### 20. Bid strategy and floor-price governance

**Justification:** Optimization choices are part of campaign operations, and they need controlled settings for bids, floors, and pacing interactions rather than opaque partner defaults.

**Improvement:** Add governed settings for target bid strategy, floor price, bid caps, bid adjustments, and manual override reasoning at campaign and placement level.

**Acceptance evidence:** Buyers can compare strategy changes over time, approval is required for high-risk bid overrides, and simulations show expected spend effects before an active campaign is changed.

### 21. Inventory reallocation and make-good management

**Justification:** When placements underdeliver or inventory disappears, operators need a structured way to reallocate spend and honor promised delivery without losing the audit trail.

**Improvement:** Add make-good workflows that record underdelivery cause, replacement inventory, budget transfer, revised KPI expectation, and customer-facing explanation for affected campaigns.

**Acceptance evidence:** Reallocation decisions stay linked to the original placement, budget transfers remain balanced, and exception closure requires evidence that the agreed remedy was applied.

### 22. Budget-to-billing reconciliation

**Justification:** Campaign operations is incomplete if it stops at planned spend and cannot explain how booked, delivered, and billed amounts diverged.

**Improvement:** Reconcile `campaign_budget`, `media_placement`, `performance_result`, and `billing_event` so buyers and finance users can compare approved spend, delivered value, invoiced amount, and unresolved variance.

**Acceptance evidence:** Reconciliation views show line-item variance, unexplained billing differences open tracked exceptions, and tests prove matched and unmatched billing events are classified correctly.

### 23. Performance result normalization and source confidence

**Justification:** Performance feeds arrive with different grains, lateness, and trust levels, so raw ingest is not enough for operational decision-making.

**Improvement:** Normalize `performance_result` by source, metric grain, reporting delay, deduplication status, and confidence score so optimization decisions can account for feed quality as well as feed value.

**Acceptance evidence:** Performance records show source confidence and dedupe status, stale or low-confidence data is visually separated in dashboards, and tests cover conflicting feed arrivals.

### 24. Forecast-versus-actual planning loop

**Justification:** Teams need to compare expected delivery and spend against what is happening now, not just look backward once the campaign has already drifted.

**Improvement:** Add a planning loop that compares forecast impressions, clicks, conversions, spend, and pacing to actuals by flight segment, placement, and audience slice.

**Acceptance evidence:** Forecast variance charts are available in the workbench, forecast revisions are versioned, and tests prove updated forecasts do not overwrite historical plans.

### 25. Pre-launch readiness gate

**Justification:** Launch quality depends on many small dependencies being complete at the same time, and a manual checklist in chat is not auditable enough.

**Improvement:** Introduce a pre-launch gate that checks approved budget, approved creative, valid audience, trafficking completeness, tracking readiness, supplier eligibility, and policy compliance before activation.

**Acceptance evidence:** Launch attempts produce a pass or fail report with itemized blockers, the gate can be rerun without side effects, and activation is blocked until all mandatory checks pass.

### 26. In-flight operations command center

**Justification:** Once campaigns go live, operators need one place to triage pacing, delivery, quality, and billing signals without hopping between unrelated screens.

**Improvement:** Turn `AdvertisingCampaignOperationsWorkbench` into an in-flight command center with campaign health, pacing alerts, creative fatigue, brand safety issues, supplier changes, and unresolved reconciliation items.

**Acceptance evidence:** Live operations panels load from purpose-built projections, alert drill-downs preserve context, and role tests verify that each persona sees the right command-center actions.

### 27. Exception taxonomy and remediation playbooks

**Justification:** A single exception bucket hides whether the problem is budget, targeting, creative, trafficking, supplier, measurement, or billing.

**Improvement:** Define a campaign-specific exception taxonomy with severity, root cause family, owner role, remediation playbook, due window, and required closure evidence for each exception class.

**Acceptance evidence:** Exceptions are grouped by remediation path, closure requires the evidence type defined for that class, and reports show aging by exception family instead of a single generic count.

### 28. SLA timers for approvals, launches, and fixes

**Justification:** Campaign operations success depends on timing, so approval and repair work needs deadline awareness tied to campaign flight risk.

**Improvement:** Add SLA timers for creative approval, audience approval, trafficking completion, launch readiness, pacing response, and billing reconciliation based on campaign start dates and risk level.

**Acceptance evidence:** Timers pause and resume according to state changes, overdue items are highlighted in work queues, and tests prove SLA calculations respect working calendars and campaign start times.

### 29. Buyer workbench

**Justification:** Buyers need a working surface centered on packages, placements, rates, holds, and supplier health rather than a generic campaign detail page.

**Improvement:** Add a buyer-specific workbench view that prioritizes negotiating packages, hold expiries, placement readiness, supplier changes, and make-good recommendations.

**Acceptance evidence:** Buyer routes render role-specific columns and actions, package edits remain auditable, and permissions prevent non-buyers from performing buying-only actions.

### 30. Creative approver workbench

**Justification:** Approvers need fast review, side-by-side revision context, and explicit disclosure checks to keep approvals moving without guesswork.

**Improvement:** Add a creative approval workbench with preview panels, diffing between revisions, checklist prompts, rejection reason libraries, and approval delegation controls.

**Acceptance evidence:** Approvers can compare asset versions in one screen, rejection feedback stays bound to the reviewed version, and approval latency metrics are visible by stage and team.

### 31. Audience analyst workbench

**Justification:** Audience specialists need dedicated tools for freshness, overlap, suppression, and risky targeting combinations that do not belong in a generic queue.

**Improvement:** Add an audience analyst view focused on segment freshness, overlap warnings, suppression coverage, targeting complexity, and simulated reach impact before launch.

**Acceptance evidence:** Analysts can approve or reject audiences with cited reasons, risky combinations are highlighted before activation, and tests confirm the view only exposes audience-governance actions.

### 32. Executive portfolio workbench

**Justification:** Senior stakeholders need a portfolio view of campaign health, not row-level operating detail.

**Improvement:** Add a portfolio workbench that rolls up active campaign spend, pacing risk, launch readiness, experiment outcomes, brand safety exposure, and unresolved billing variance across accounts or business units.

**Acceptance evidence:** Portfolio metrics drill into campaign details without losing the executive filter context, rollups reconcile to underlying projections, and tests cover mixed-status campaign portfolios.

### 33. Agent skill for draft campaign setup from the brief

**Justification:** Operators should be able to turn a campaign brief into a governed first draft quickly without bypassing the domain model.

**Improvement:** Add an assistant skill in `AdvertisingCampaignOperationsAssistantPanel` that converts a structured brief into a draft campaign, initial budget shell, targeting proposal, and launch checklist for human review.

**Acceptance evidence:** The skill produces a preview before writing records, rejected previews leave no partial mutations behind, and audit events show which fields were agent-proposed versus human-confirmed.

### 34. Agent skill for pacing diagnosis and recovery suggestions

**Justification:** Pacing problems are frequent and time-sensitive, making them a good fit for explainable guided assistance rather than manual spreadsheet triage.

**Improvement:** Add an assistant skill that inspects pacing variance, identifies likely causes such as budget caps, supply constraints, creative fatigue, or tracking gaps, and proposes recovery actions for review.

**Acceptance evidence:** Suggested actions cite the data behind the recommendation, operators can accept or reject each action individually, and tests prove no direct mutation occurs without explicit confirmation.

### 35. Agent skill for governed change bundles

**Justification:** Operators often need coordinated changes across budget, targeting, placements, and assets, and these should move as one reviewed bundle rather than as scattered edits.

**Improvement:** Add assistant support for preparing change bundles that package related campaign edits, summarize expected impact, and route the bundle through the correct approval path before execution.

**Acceptance evidence:** Bundle previews show affected records and approvals required, partial execution is prevented when approvals are incomplete, and the final audit trail preserves the original bundle intent.

### 36. Event taxonomy expansion for campaign operations

**Justification:** Generic lifecycle events do not tell downstream systems whether the meaningful change was a launch, hold release, trafficking correction, budget shift, or creative rejection.

**Improvement:** Expand emitted events into campaign-specific business events for planning, approval, trafficking, launch, pacing breach, supplier impact, experiment decision, billing variance, and campaign closeout milestones.

**Acceptance evidence:** Event schemas are documented with examples, downstream projections subscribe to specific business events instead of generic updates, and contract tests prove event payload stability.

### 37. API boundary expansion for search, validate, simulate, and closeout

**Justification:** A real operational surface needs query and decision APIs, not just create endpoints.

**Improvement:** Extend the PBC API with search, validation-only, simulation, closeout, reconciliation, and evidence export endpoints while keeping command boundaries explicit between planning, activation, and reporting actions.

**Acceptance evidence:** Route documentation distinguishes mutation APIs from read models, validation endpoints are side-effect free, and tests prove idempotent retries for command endpoints that accept external request IDs.

### 38. Idempotent partner ingestion and trafficking imports

**Justification:** Buying and trafficking workflows often replay feeds or resend the same payloads, so import paths have to be safe under repetition and partial failure.

**Improvement:** Add idempotent import handling for placement instructions, creative delivery confirmations, and performance feed arrivals using stable external IDs and replay-safe correction logic.

**Acceptance evidence:** Duplicate imports do not create duplicate placements or metrics, partial failures can be retried safely, and dead-letter evidence preserves the original partner payload reference.

### 39. Event replay and projection recovery

**Justification:** Operational history is only useful if projections and dashboards can be rebuilt after code changes or corrupted projections.

**Improvement:** Add replay tooling for campaign events and read-model rebuild routines so workbench views can be regenerated from the durable event stream without manual database surgery.

**Acceptance evidence:** Replay tests rebuild projections to a known checksum, recovery jobs expose progress and failures, and historical campaign timelines match pre-replay snapshots.

### 40. Auditable timeline across planning, buying, launch, and billing

**Justification:** Users need one end-to-end narrative for each campaign that explains how the campaign moved from idea to closeout.

**Improvement:** Build a consolidated timeline that stitches together brief creation, budget approvals, asset revisions, placement trafficking, launch checks, pacing incidents, supplier changes, billing events, and closeout decisions.

**Acceptance evidence:** Timeline views show actor, timestamp, event class, and linked evidence for each step, users can filter by phase or entity, and tests confirm timeline ordering across multiple record types.

### 41. Continuous control testing for approval and spend discipline

**Justification:** Campaign governance should be continuously checked while work is happening rather than only after a failed launch or audit review.

**Improvement:** Add control assertions that test segregation of duties, launch without approval, spend above approved budget, missing tracking, stale audience approval, and unresolved high-severity brand safety issues.

**Acceptance evidence:** Control failures generate actionable exceptions, controls can be run on demand and on schedule, and release evidence includes the most recent control status for active campaigns.

### 42. Versioned policy evidence and approval rationale

**Justification:** When a rule changes mid-flight, the team must be able to show which policy version approved the current state and why.

**Improvement:** Capture policy version, approver rationale, and referenced evidence whenever a creative, budget, audience, or launch gate is approved so changes triggered by `PolicyChanged` remain explainable later.

**Acceptance evidence:** Approval records expose policy version and rationale side by side, policy updates can highlight now-outdated approvals, and tests prove previously approved records retain their original evidence lineage.

### 43. Schema extension registry for channel-specific fields

**Justification:** Different channels require different operational metadata, but ad hoc extension fields quickly become ungoverned sprawl.

**Improvement:** Add a schema extension registry for channel-specific planning, trafficking, and reporting fields with ownership, validation, rollout status, and projection impact declared up front.

**Acceptance evidence:** New extension fields appear through a governed registry, incompatible changes are blocked before migration, and dry-run reports show which APIs and workbench panels a new field will affect.

### 44. Multi-tenant policy and workspace isolation

**Justification:** Shared campaign operations infrastructure must preserve each tenant’s approval rules, targeting restrictions, and release evidence without leakage.

**Improvement:** Isolate tenant policy packs, approval matrices, runtime parameters, supplier eligibility views, and workbench filters so one tenant’s campaign operations settings cannot influence another tenant’s outcomes.

**Acceptance evidence:** Tenant isolation tests cover reads, writes, projections, and assistant actions, cross-tenant references are rejected, and operational dashboards remain scoped to the active tenant context.

### 45. Consent, privacy, and sensitive-audience safeguards

**Justification:** Audience targeting can become a compliance risk quickly if consent state, sensitive categories, or allowed use cases are treated as optional metadata.

**Improvement:** Add audience safeguards for consent status, sensitive targeting categories, retention windows, redaction in assistant prompts, and escalation when a segment’s intended use exceeds policy.

**Acceptance evidence:** High-risk audiences require elevated review, sensitive fields are masked where appropriate, and tests prove blocked use cases cannot be activated through API, UI, or assistant paths.

### 46. Creative asset locking and delivery provenance

**Justification:** Once an asset version is approved and trafficked, operators need certainty that the delivered file matches the approved file.

**Improvement:** Lock approved creative versions, track export hashes, record delivery destinations, and preserve provenance from approved asset to trafficked placement attachment.

**Acceptance evidence:** Approved assets cannot be silently replaced, provenance views show delivered file lineage, and validation rejects placements that reference an unapproved or superseded asset export.

### 47. Release evidence package automation

**Justification:** Release assurance for this PBC should include operational proof, not just build output, because campaign failures often come from incorrect rules or incomplete workflows.

**Improvement:** Generate release evidence that bundles control results, route coverage, event-contract checks, workbench smoke coverage, migration status, and representative campaign lifecycle fixtures for the package.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` can be regenerated from current package state, evidence bundles include campaign-specific scenarios, and release checks fail when required proof artifacts are missing.

### 48. Post-campaign wrap-up and benchmark library

**Justification:** Optimization should not end at campaign close; teams need structured learning from what happened to improve the next plan.

**Improvement:** Add a closeout workflow that records final outcomes, variance explanations, creative winners, audience insights, supplier notes, and reusable benchmarks for future planning.

**Acceptance evidence:** Closed campaigns require wrap-up evidence before archival, benchmark summaries are queryable in the workbench, and tests prove historical benchmarks remain read-only once published.

### 49. Counterfactual simulation for spend shifts and creative swaps

**Justification:** Operators frequently need to ask whether moving spend, changing targeting, or rotating creative will help before taking a risky mid-flight action.

**Improvement:** Add simulation tools that compare current state against hypothetical spend reallocations, creative swaps, targeting relaxations, and supplier replacements using the package’s planning and performance history.

**Acceptance evidence:** Simulation runs never mutate live campaign data, users can compare baseline and simulated outcomes side by side, and scenario artifacts can be attached to approval decisions.

### 50. Cutover and rollback evidence for live campaign changes

**Justification:** Mid-flight operational changes are risky, and the package should make it easy to prove what changed, when it changed, and how to revert safely.

**Improvement:** Introduce explicit cutover plans for live campaign edits with pre-change snapshot, staged activation, rollback recipe, owner assignment, and post-change verification steps for critical modifications.

**Acceptance evidence:** High-risk edits require a cutover record before execution, rollback plans are visible to operators and approvers, and tests prove a failed cutover can return the campaign to its prior approved state.
