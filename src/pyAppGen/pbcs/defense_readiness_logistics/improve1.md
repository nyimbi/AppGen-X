# Defense Readiness Logistics Improvement Backlog

## Current Domain Evidence Used

- Exact key: `defense_readiness_logistics`
- Manifest label: `Defense Readiness Logistics`
- Description: `Units, readiness, assets, maintenance, supply, mission planning, deployment, and defense logistics`
- Tables: `unit_readiness`, `mission_asset`, `supply_request`, `maintenance_status`, `deployment_plan`, `readiness_inspection`, `logistics_movement`
- APIs: `POST /unit-readinesss`, `POST /mission-assets`, `POST /supply-requests`, `POST /maintenance-statuss`, `POST /deployment-plans`, `GET /defense-readiness-logistics-workbench`
- Workflows: `defense_readiness_logistics_create_unit_readiness_workflow`, `defense_readiness_logistics_record_mission_asset_workflow`
- UI fragments: `DefenseReadinessLogisticsWorkbench`, `DefenseReadinessLogisticsDetail`, `DefenseReadinessLogisticsAssistantPanel`
- Emitted events: `DefenseReadinessLogisticsCreated`, `DefenseReadinessLogisticsUpdated`, `DefenseReadinessLogisticsApproved`, `DefenseReadinessLogisticsExceptionOpened`
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`

### 1. Canonical unit readiness state model
**Justification:** Unit readiness is the core domain object, but the manifest only proves the presence of `unit_readiness_management` and `unit_readiness`; it does not prove a defensible operational lifecycle. Commanders need to distinguish draft reports, validated readiness, degraded readiness, and deployment-ready states without reading free-text notes.
**Improvement:** Define explicit readiness states and transitions for `unit_readiness` that separate reported status, validated status, commander-approved status, and deployment authorization. Make each transition carry reason codes for personnel shortfall, asset outage, maintenance hold, ammo deficit, fuel deficit, and movement-order delay.
**Acceptance evidence:** Workflow tests for valid and invalid state transitions, workbench badges showing each readiness phase, and release evidence proving every approved transition emits auditable state history.

### 2. Mission capability rollup by unit and mission set
**Justification:** Readiness alone is too coarse; operators need to know whether a unit can execute a specific mission profile with its current people, vehicles, weapons, and sustainment posture. A unit can be green for training yet amber for a live deployment window.
**Improvement:** Add mission capability projections that roll up `unit_readiness`, `mission_asset`, `maintenance_status`, and `supply_request` into mission-specific capability ratings by mission type, time window, and deployment priority. Show why a unit is capable, partially capable, or not capable for each named mission set.
**Acceptance evidence:** Projection tests with mixed readiness inputs, commander workbench cards showing mission capability by mission set, and traceable explanations from source records to final capability outcome.

### 3. Inspection evidence packs for readiness assertions
**Justification:** `readiness_inspection` exists in the manifest, but a simple inspection record does not prove that a readiness claim was inspected with sufficient evidence. Audit teams need repeatable evidence packs, not only timestamps and pass/fail flags.
**Improvement:** Build inspection evidence packs that link checklist answers, signatures, photos, document references, serial-checked assets, and corrective actions to each `readiness_inspection`. Distinguish spot checks, pre-deployment inspections, and post-maintenance inspections.
**Acceptance evidence:** Stored evidence-pack examples, failed-inspection remediation workflows, and release evidence that an inspection cannot mark a unit ready without the required evidence set.

### 4. Personnel readiness boundary checks
**Justification:** Personnel readiness is part of unit readiness, but the package must avoid turning into a full HR system. Defense operations need bounded checks for duty status, certifications, and minimum crew composition without storing unnecessary personal detail.
**Improvement:** Add personnel readiness gates that evaluate whether a unit meets minimum qualified staffing, duty availability, and required role coverage for a mission while keeping only the bounded operational attributes needed for readiness. Block green readiness when the mission requires certifications, cleared roles, or minimum crew counts that are not met.
**Acceptance evidence:** Boundary tests proving only operationally necessary personnel fields are used, readiness calculations that fail when required role coverage is missing, and UI evidence showing the shortfall without exposing excess personal data.

### 5. Mission asset availability by mission window
**Justification:** `mission_asset` without time-phased availability does not help planners decide whether assets will be present and serviceable when the mission actually launches. Asset presence today is not enough if the platform enters maintenance tomorrow.
**Improvement:** Add availability calendars for `mission_asset` that combine planned usage, location, maintenance forecasts, and movement commitments into mission-window availability. Expose conflicts where the same asset is implicitly allocated to multiple deployment plans.
**Acceptance evidence:** Conflict-detection tests, asset calendars visible in the workbench, and evidence that double-booked assets are surfaced before deployment approval.

### 6. Maintenance status projections with readiness impact
**Justification:** The manifest proves `maintenance_status` exists, but operations require forward-looking maintenance projections, not only current status. Readiness decisions are distorted when projected completion dates and parts dependency risk are ignored.
**Improvement:** Build maintenance status projections that estimate return-to-service dates, confidence ranges, and readiness impact for each affected unit and mission set. Include delays caused by long-lead spares, deferred inspections, missing technicians, and depot capacity constraints.
**Acceptance evidence:** Projection fixtures covering on-time and delayed repairs, workbench timelines that show expected readiness recovery dates, and evidence linking each projection to underlying maintenance and supply facts.

### 7. Cannibalization and donor-asset controls
**Justification:** Defense logistics often restores one mission asset by pulling parts from another, but that can silently degrade broader readiness. Without explicit controls, the package could report a local gain while hiding a unit-level loss elsewhere.
**Improvement:** Track donor-asset cannibalization events, required approvals, restoration obligations, and downstream readiness impact when a part is removed from one asset to restore another. Make the tradeoff visible in both asset and unit readiness views.
**Acceptance evidence:** Tests showing donor and receiving asset state changes, approval evidence for cannibalization actions, and workbench alerts when the action creates a readiness deficit in another unit.

### 8. Supply readiness scoring tied to mission demand
**Justification:** `supply_request` volume does not equal supply readiness. Units need to know whether critical items on hand and in transit are sufficient for the mission package they are expected to execute.
**Improvement:** Add supply readiness scoring that compares required mission demand against on-hand stock, open requests, inbound shipments, and substitute item policy. Score critical classes separately for class IX repair parts, medical items, communications spares, ration support, and other mission-essential categories.
**Acceptance evidence:** Scenario tests for complete, partial, and failed supply readiness, supply readiness panels in the workbench, and release evidence that supply readiness gates can block deployment approval.

### 9. Ammunition constraint management
**Justification:** Ammo posture is a distinct operational limiter and cannot be buried inside generic supply requests. Mission approval needs to account for training allocation, combat load, storage compatibility, and lot-specific restrictions.
**Improvement:** Add ammunition constraint handling that tracks authorized load plans, required quantities by mission, lot and compatibility restrictions, and pending replenishment. Surface when a unit is fully staffed and mechanically ready but still not mission-capable due to ammunition shortfall or restriction.
**Acceptance evidence:** Constraint tests covering sufficient and insufficient ammo states, readiness explanations citing ammo blockers, and operator evidence that lot restrictions propagate into mission capability results.

### 10. Fuel constraint management
**Justification:** Fuel shortfalls and refuel-plan gaps can make a movement or mission impossible even when assets are serviceable. Fuel posture needs explicit treatment instead of being folded into general sustainment notes.
**Improvement:** Add fuel readiness tracking for on-hand fuel, uplift plans, refuel points, consumption forecasts, convoy refuel timing, and contingency reserves. Link fuel sufficiency directly to `deployment_plan` approval and `logistics_movement` execution readiness.
**Acceptance evidence:** Fuel sufficiency calculations for multiple mission lengths, blocked deployment approvals caused by fuel gaps, and workbench displays that show which leg of the operation breaks the fuel plan.

### 11. Deployment kit composition and completeness
**Justification:** Deployment kits are often assembled from mixed equipment, documents, medical packs, communications items, and mission-specific consumables. Missing one kit component can invalidate a deployment despite otherwise healthy readiness signals.
**Improvement:** Model deployment kits with required line items, optional substitutes, expiration-sensitive components, inspection checkpoints, and packing status for each `deployment_plan`. Show completeness percentages and mission-critical missing items before movement execution.
**Acceptance evidence:** Kit-completeness test data, detailed kit panels in the deployment workbench, and release evidence that incomplete mission-critical kits prevent final deployment approval.

### 12. Pre-positioned stock and theater support visibility
**Justification:** A unit may not need every item at home station if critical support is pre-positioned in theater. Without that visibility, the package will overstate shortages or understate risk depending on assumptions hidden outside the system.
**Improvement:** Add theater support views that distinguish on-hand unit stock, pre-positioned stock, host-site support, and in-transit stock for each mission. Make assumptions explicit so planners know which support commitments are firm and which remain provisional.
**Acceptance evidence:** Visibility tests for home-station and theater-supported supply cases, workbench indicators that separate firm from assumed support, and audit evidence showing who approved each support assumption.

### 13. Movement order lifecycle control
**Justification:** `logistics_movement` exists, but defense operations need formal movement-order stages from draft through execution and closeout. Informal movement notes are not enough for convoy timing, lift coordination, and route approval.
**Improvement:** Add a movement order lifecycle with draft, route-reviewed, force-protected, lift-confirmed, released, in-transit, arrived, diverted, delayed, and closed states. Capture route changes, escort requirements, staging times, and commander approval points.
**Acceptance evidence:** Movement-order workflow tests, route and timing history visible in the workbench, and release evidence showing every released order has a complete approval trail.

### 14. Mode-specific movement planning for convoy, airlift, and sealift
**Justification:** Defense logistics planning changes materially by transport mode. One generic movement record cannot enforce the distinct constraints for road convoy, air movement, and sea movement.
**Improvement:** Split planning rules by movement mode so convoy plans enforce route and refuel constraints, airlift plans enforce pallet and aircraft limits, and sealift plans enforce port sequencing and hazardous cargo declarations. Allow a single deployment to span multiple coordinated movement modes.
**Acceptance evidence:** Mode-specific validation tests, multi-leg deployment examples, and UI evidence showing which constraints apply to each movement segment.

### 15. Load plan validation for weight, cube, and tie-down
**Justification:** Units often believe they are deployable until actual load planning reveals overweight pallets, incompatible vehicles, or tie-down shortages. Those failures should surface before the movement order is released.
**Improvement:** Add load plan validation that checks weight, cube, dimensional limits, palletization, tie-down requirements, and special handling needs for each movement segment. Highlight which assets or kit components break the load plan and what substitute configuration would pass.
**Acceptance evidence:** Validation fixtures for passing and failing load plans, load-plan drilldowns in the movement workbench, and evidence that invalid plans block release of the order.

### 16. Asset serviceability handoff between maintenance and operations
**Justification:** Assets often appear serviceable in one context and unavailable in another because maintenance and operations handoffs are implicit. The package needs an explicit serviceability decision boundary.
**Improvement:** Add a governed handoff that marks when maintenance has released an asset, operations has accepted it, and the asset is now available for mission assignment. Record outstanding discrepancies that allow limited use versus discrepancies that prohibit operational use.
**Acceptance evidence:** Handoff workflow tests, serviceability status cards for each mission asset, and audit evidence that readiness calculations only consume accepted operational serviceability.

### 17. Parts demand forecasting from maintenance workload
**Justification:** Parts requests become urgent too late when the system only reacts to failed components already reported in `supply_request`. Maintenance planning should be able to project likely demand from scheduled work and recurring fault patterns.
**Improvement:** Forecast parts demand from open maintenance actions, recurring fault codes, fleet age, and scheduled inspections so logistics teams can pre-stage critical spares. Show forecast confidence and separate planned demand from emergency demand.
**Acceptance evidence:** Forecast accuracy tests over seeded maintenance scenarios, supply readiness workbench views showing predicted shortages, and release evidence that projected demand is distinguishable from confirmed requisitions.

### 18. Deferred maintenance risk ledger
**Justification:** Not every maintenance action blocks immediate use, but deferred faults accumulate operational risk. Units need a visible ledger of what has been deferred and how it degrades mission capability over time.
**Improvement:** Add deferred maintenance tracking with risk category, expiry date, permitted operating envelope, required commander acknowledgement, and automatic readiness downgrades when the deferral window closes. Tie the ledger directly to unit and mission capability rollups.
**Acceptance evidence:** Tests for active and expired deferrals, commander acknowledgement records, and workbench indicators showing when deferred faults change a unit from capable to restricted.

### 19. Critical spares substitution policy
**Justification:** Logistics teams frequently need to substitute approved parts or alternative kit components under pressure. That decision must be bounded by policy rather than hidden in comments or ad hoc operator judgment.
**Improvement:** Add substitution policy rules for critical spares and deployment kit components, including approved substitutes, disallowed substitutes, temporary waivers, and required approvals. Show when a substitute preserves readiness and when it only enables a restricted mission profile.
**Acceptance evidence:** Policy-rule tests for allowed and blocked substitutions, substitute decisions visible in workbench detail, and release evidence that substitution approvals are fully traceable.

### 20. Serial, lot, and batch traceability for controlled items
**Justification:** Controlled military items, repair parts, ammo, and communications gear often require serial or lot traceability. Without traceability, the package cannot support recalls, restrictions, or accountability investigations.
**Improvement:** Extend `mission_asset` and supply evidence so controlled items can be traced by serial, lot, or batch through receipt, installation, movement, inspection, and disposition. Surface when a restricted lot affects a deployment kit or mission load.
**Acceptance evidence:** Traceability tests across receipt-to-use flows, search and filter support for serial and lot identifiers, and audit-ready item histories in the workbench.

### 21. Shelf-life and expiration readiness impacts
**Justification:** Medical supplies, batteries, sealed kits, lubricants, and other perishable items can quietly age into non-usable status. Readiness signals must degrade before the item expires on the day of mission execution.
**Improvement:** Add shelf-life monitoring with warning thresholds, replacement lead times, and mission-date checks so expiring items are flagged before they invalidate a deployment plan. Link replacement urgency to supply readiness and deployment kit completeness.
**Acceptance evidence:** Expiration warning tests, readiness downgrades triggered by soon-to-expire mission-critical items, and UI evidence showing replacement timelines.

### 22. Classified handling rules for plans and logistics evidence
**Justification:** Defense logistics records can include classified route details, force package composition, and sensitive sustainment assumptions. The package needs classification-aware handling rather than a single global permission tier.
**Improvement:** Add classification markings, need-to-know filtering, redaction rules, and controlled export policies for `deployment_plan`, `logistics_movement`, and sensitive readiness evidence. Ensure the assistant panel does not reveal restricted route or force details to users without the right clearance context.
**Acceptance evidence:** Permission tests across classification tiers, redacted UI snapshots for lower-access roles, and release evidence showing classified exports are separately controlled and audited.

### 23. Controlled communications and key-mat custody tracking
**Justification:** Some deployments depend on custody of controlled communications equipment or keyed material, and loss of custody can break mission execution. Those items should influence readiness without expanding into a full communications system.
**Improvement:** Add bounded custody tracking for mission-critical controlled comms items, keyed sets, or protected access devices needed for deployment execution. Show whether required custody is assigned, transferred, and acknowledged before mission launch.
**Acceptance evidence:** Custody-transfer tests, deployment readiness blockers for missing controlled items, and workbench evidence showing when custody gaps prevent mission release.

### 24. Hazardous cargo and dangerous goods restrictions
**Justification:** Ammo, fuel, batteries, and chemical support items create dangerous goods handling constraints that affect storage, transport mode, and route approval. A deployment can fail even when every item is otherwise available.
**Improvement:** Add hazardous cargo rules that flag incompatible combinations, required packaging, documentation, escort requirements, and mode restrictions for dangerous goods. Bind the rules to movement planning and deployment kit validation.
**Acceptance evidence:** Dangerous-goods validation tests, mode restriction warnings in movement planning, and release evidence that hazardous loads cannot be approved without the mandated supporting documentation.

### 25. Host-nation and customs document readiness
**Justification:** Cross-border movement often fails because customs, import, or host-nation support documents are incomplete. These external document dependencies belong in operational readiness, not only in a separate admin checklist.
**Improvement:** Add document readiness tracking for border clearance, landing rights, port entry, host-nation approvals, and contracted support letters tied to each movement or deployment plan. Distinguish drafted, submitted, accepted, expired, and waived document states.
**Acceptance evidence:** Document-state workflow tests, movement-order blockers caused by missing approvals, and workbench evidence showing which authority or office still owns the unresolved document.

### 26. Training and certification gating for mission roles
**Justification:** A unit can appear numerically staffed while still lacking certified operators, maintainers, medics, or dangerous-goods handlers needed for the mission profile. Certification status must influence readiness without requiring full personnel management.
**Improvement:** Add role-based certification gates that check whether the mission has the required count of currently qualified personnel for the selected plan. Make expiration-driven certification loss visible in future readiness projections.
**Acceptance evidence:** Qualification-gap tests, future-state readiness projections that degrade when certifications lapse, and clear workbench explanations for which role qualification is missing.

### 27. Commander readiness workbench
**Justification:** `DefenseReadinessLogisticsWorkbench` is listed in the manifest, but commanders need a role-specific view centered on deployability, mission capability, and blockers. A generic queue does not support command decisions.
**Improvement:** Create a commander workbench that prioritizes unit readiness posture, mission capability by mission set, top blockers, aging exceptions, and release decisions by operational priority. Include drill-down from force posture to unit, asset, and supply causes.
**Acceptance evidence:** Role-routed UI tests, commander dashboard screenshots in release evidence, and navigation evidence that every blocker card reaches the underlying record or action.

### 28. Maintenance control workbench
**Justification:** Maintenance controllers need a different operating picture than commanders: repair queues, parts waits, return-to-service forecasts, and cannibalization risk. Those tasks should not be buried inside a single generic detail page.
**Improvement:** Build a maintenance control workbench with fault queues, return-to-service projections, deferred maintenance risk, parts dependency heatmaps, and technician-capacity indicators. Allow quick drill-down from a unit's degraded readiness to the specific maintenance actions causing it.
**Acceptance evidence:** Workbench route coverage, projection and filter tests, and release evidence showing maintenance controllers can resolve a readiness blocker from their dedicated view.

### 29. Supply readiness workbench
**Justification:** Supply specialists need to manage requisitions, shortages, substitutions, and theater support assumptions at speed. They need an operating surface tailored to supply readiness, not only a list of `supply_request` records.
**Improvement:** Build a supply readiness workbench with shortage queues, critical-item dashboards, kit-completion views, substitute-item decisions, and in-transit shipment visibility. Surface which shortages actually block a named deployment or mission set.
**Acceptance evidence:** Workbench acceptance tests by role, blocker-to-request drilldowns, and release evidence that supply teams can clear readiness-impacting shortages from one focused view.

### 30. Movement control workbench
**Justification:** Movement planners need synchronized visibility across movement orders, routes, lift availability, staging times, and dangerous-goods restrictions. Mixing that workflow into general detail pages slows operational execution.
**Improvement:** Build a movement control workbench with order status boards, route timelines, mode assignments, load-plan validation results, and late-change alerts. Support cross-checking whether movement readiness still matches the approved deployment plan.
**Acceptance evidence:** Movement workbench tests, timeline views in release evidence, and traceable links from late-change alerts to the changed order, asset, or route assumption.

### 31. Assistant skill for movement order extraction
**Justification:** `DefenseReadinessLogisticsAssistantPanel` exists, but the assistant is only useful if it can convert messy staff inputs into governed movement drafts. Movement orders often start as operations messages, emails, or fragmented instructions.
**Improvement:** Add an agent skill that extracts movement order fields from operational messages into a draft `logistics_movement` command with source citations, ambiguity flags, and no-write preview. Require human confirmation before route, timing, or cargo assumptions become authoritative.
**Acceptance evidence:** Extraction fixtures with cited source spans, blocked-write tests for ambiguous instructions, and assistant audit logs proving that only confirmed drafts create or update movement records.

### 32. Assistant skill for maintenance narrative summarization
**Justification:** Maintenance data often arrives as narrative fault descriptions and status updates that are hard for commanders to interpret quickly. The assistant should translate those narratives into readiness-relevant summaries without inventing facts.
**Improvement:** Add an agent skill that summarizes maintenance narratives into serviceability status, expected completion, required parts, risk to mission assignments, and unresolved unknowns. Show the original source text alongside the structured summary.
**Acceptance evidence:** Summarization tests with grounded source citations, hallucination-guard cases where the assistant must mark information unknown, and workbench evidence that summaries remain linked to the original maintenance record.

### 33. Assistant skill for shortage mitigation options
**Justification:** Supply teams need decision support when critical shortages threaten readiness, but suggested workarounds must stay within policy and actual stock posture. A generic chatbot answer is not enough.
**Improvement:** Add an agent skill that proposes shortage mitigation options such as approved substitutes, cross-leveling candidates, accelerated transport, or phased mission kits based on current policy and stock facts. Require the assistant to label every option as approved, restricted, or unavailable.
**Acceptance evidence:** Policy-aware recommendation tests, assistant responses with explicit confidence and constraints, and audit evidence showing the suggested options were generated from current supply and policy data.

### 34. Command API boundary hardening
**Justification:** The manifest exposes only a handful of POST endpoints and one workbench GET route. Defense operations need a clear command boundary so external systems can submit requests without bypassing validation or approvals.
**Improvement:** Expand and harden the command API surface around readiness, assets, maintenance, supply, and deployment so commands are explicit, idempotent, and versioned by domain intent rather than generic CRUD. Separate create, validate, approve, reject, and simulate actions where the operational semantics differ.
**Acceptance evidence:** Contract tests for command endpoints, idempotency evidence for retried submissions, and release evidence proving that unauthorized field mutation cannot occur through the public API surface.

### 35. Event boundary expansion by operational fact
**Justification:** The current emitted events are too generic to explain defense operations outside the package boundary. Downstream consumers need domain facts such as readiness downgraded, movement released, or supply blocker opened.
**Improvement:** Add typed events for readiness assessed, mission capability changed, maintenance forecast slipped, supply blocker opened, deployment kit failed inspection, movement released, and movement delayed. Keep payloads narrowly focused on the operational fact and source identifiers rather than entire record snapshots.
**Acceptance evidence:** Event-schema tests, example payloads in release evidence, and consumer-facing documentation proving the event boundary is specific enough for downstream action without leaking unnecessary internals.

### 36. Outbox, inbox, and replay evidence for operational events
**Justification:** The manifest includes `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, and `retry_dead_letter_evidence`, but defense operations need visible proof that events can be retried safely. Replay must not duplicate approvals, movements, or supply commitments.
**Improvement:** Add operational evidence for event enqueue, delivery, retry, dead-letter, and replay outcomes tied to each readiness-critical event. Show when a replay changed nothing, repaired a stale projection, or reopened an exception.
**Acceptance evidence:** Replay and duplicate-handling tests, dead-letter workbench views, and release evidence demonstrating safe reprocessing for at least one readiness, maintenance, and movement scenario.

### 37. Release evidence pack for deployment readiness decisions
**Justification:** `RELEASE_EVIDENCE.md` is listed in the manifest, but deployment and readiness approvals need a package-generated evidence pack rather than a hand-assembled note. Approval should be backed by facts from the domain objects that justified it.
**Improvement:** Generate release evidence packs that capture readiness status, capability rollups, open exceptions, kit completeness, movement readiness, and classification-safe export views for each approved deployment decision. Include policy version, approver identity, and source record references.
**Acceptance evidence:** Generated evidence-pack artifacts, export tests for classified-safe and full-access variants, and release evidence showing every approved deployment references a reproducible evidence bundle.

### 38. Manifest-to-surface contract validation
**Justification:** The manifest names tables, APIs, workflows, UI fragments, docs, and tests, but there is no guarantee they remain aligned as the package evolves. A backlog improvement should close that governance gap explicitly.
**Improvement:** Add contract checks that verify manifest-declared APIs, workflows, tables, events, and UI fragments are still implemented and documented in the package. Fail release evidence generation when a declared surface is missing, renamed, or untested.
**Acceptance evidence:** Contract test failures for intentionally broken declarations, passing validation in normal builds, and release evidence showing the manifest contract status for the package version.

### 39. Exception taxonomy and escalation queues
**Justification:** `DefenseReadinessLogisticsExceptionOpened` exists, but exceptions need a domain taxonomy so teams know whether the issue is maintenance-driven, supply-driven, classified-access-driven, or movement-driven. Generic exception buckets slow recovery.
**Improvement:** Add categorized exception queues for readiness validation, maintenance delay, parts shortage, fuel shortfall, ammo shortfall, kit failure, document hold, route restriction, and policy violation. Route each exception to the correct workbench and owning role with aging thresholds.
**Acceptance evidence:** Taxonomy tests, queue routing evidence by exception type, and release evidence showing aged exceptions by operational category and owner.

### 40. Policy isolation by tenant, formation, and operation
**Justification:** The manifest lists `defense_readiness_logistics_multi_tenant_policy_isolation`, but defense logistics may also need isolation across formations or named operations that share infrastructure. Policy leakage across those boundaries creates operational and security risk.
**Improvement:** Enforce scoped policy, parameter, and assistant-context isolation by tenant and optionally by formation or named operation. Prevent one operation's override rules, supply assumptions, or classification rules from silently affecting another.
**Acceptance evidence:** Isolation tests across tenants and operations, negative cases proving one scope cannot read or apply another scope's policy, and release evidence that scoped policy selection is visible in audits.

### 41. Readiness simulation and course-of-action comparison
**Justification:** The manifest includes `defense_readiness_logistics_counterfactual_scenario_simulation`, but planners need it focused on operational tradeoffs such as moving one repair forward or reallocating fuel. Decision support should compare realistic courses of action.
**Improvement:** Add scenario simulation that compares course-of-action options for restoring readiness, prioritizing kits, reallocating lift, or accelerating critical supply lines. Show how each option changes mission capability, movement timing, and risk.
**Acceptance evidence:** Simulation fixtures with multiple courses of action, side-by-side comparison views in the workbench, and release evidence that simulated changes are clearly marked as non-authoritative until approved.

### 42. Degraded communications and offline capture path
**Justification:** Defense operations cannot assume constant network availability at depots, staging areas, or field locations. Critical readiness updates and movement changes may need to be captured offline and reconciled later.
**Improvement:** Add offline-capable capture for inspections, maintenance updates, kit checks, and movement status changes with signed local evidence, sync conflict handling, and delayed-event replay. Preserve source timestamps and operator identity from the disconnected capture context.
**Acceptance evidence:** Offline-to-sync integration tests, conflict-resolution evidence for concurrent edits, and release evidence showing offline submissions become auditable events when connectivity returns.

### 43. Reconciliation across readiness, assets, supply, and movement
**Justification:** A unit can look ready in `unit_readiness` while related asset, supply, or movement records tell a different story. The package needs explicit reconciliation instead of trusting that every projection stays perfectly aligned.
**Improvement:** Add reconciliation jobs that compare readiness claims against asset availability, maintenance projections, supply readiness, deployment kit status, and released movement orders. Open governed exceptions when the cross-table story no longer matches.
**Acceptance evidence:** Reconciliation tests covering mismatched scenarios, exception creation evidence for cross-domain conflicts, and workbench views that show what part of the readiness story disagrees.

### 44. Event-sourced operational timeline
**Justification:** The manifest names `defense_readiness_logistics_event_sourced_operational_history`, but operators need a human-usable timeline, not only replay infrastructure. Investigations and after-action reviews depend on seeing how readiness evolved over time.
**Improvement:** Build an operational timeline that reconstructs readiness, asset, maintenance, supply, and movement changes by time, actor, and event source. Support playback from the workbench so analysts can understand when a unit lost or regained deployability.
**Acceptance evidence:** Timeline reconstruction tests, playback views for seeded scenarios, and release evidence proving that timeline entries can be traced back to original commands and events.

### 45. Role-specific approval matrix
**Justification:** The manifest includes coarse permissions such as `defense_readiness_logistics.approve`, but operational approvals differ by action and sensitivity. A movement release should not use the same authority path as a routine asset update.
**Improvement:** Add role-specific approval matrices for commander release, maintenance acceptance, supply substitution approval, classified export approval, and movement-order release. Enforce the right authority path by action type, risk level, and classification.
**Acceptance evidence:** Permission-matrix tests, denied-action evidence for under-authorized roles, and workbench UI states showing why an approval action is available or blocked.

### 46. Alerting and threshold governance for readiness risk
**Justification:** Teams need alerts that are tied to operational thresholds, not generic notification spam. The difference between informational drift and mission-blocking degradation must be explicit.
**Improvement:** Add threshold-based alerts for readiness drops, maintenance slips, fuel shortfalls, ammo constraints, late movement orders, expiring certifications, and unresolved classified-access blockers. Allow thresholds and recipients to vary by mission priority and operation tempo.
**Acceptance evidence:** Threshold tests for high and low priority missions, alert-routing evidence by role, and release evidence that alert noise is suppressed for non-blocking conditions.

### 47. Readiness detail drilldown with blocker provenance
**Justification:** `DefenseReadinessLogisticsDetail` should explain exactly why a unit is not deployable, not merely display the top-level score. Users need provenance from the summary banner to each causal record.
**Improvement:** Redesign the detail view so every readiness status, capability score, or blocker badge links directly to the underlying inspection, asset, maintenance, supply, kit, or movement fact. Include a provenance chain that shows how the blocker changed the final readiness result.
**Acceptance evidence:** UI drilldown tests, detail-page screenshots in release evidence, and traceability checks proving every blocker card reaches a source record or event.

### 48. Assistant-safe redaction and citation behavior
**Justification:** `DefenseReadinessLogisticsAssistantPanel` becomes risky if it summarizes sensitive logistics details without citations or classification checks. The assistant should be useful under operational security constraints, not merely convenient.
**Improvement:** Require assistant answers to cite source records, mark uncertainty, obey classification-aware redaction, and refuse unsupported inference about route, inventory, or readiness details not present in package data. Apply the same controls to draft-generation and recommendation skills.
**Acceptance evidence:** Assistant behavior tests for citation, refusal, and redaction, plus release evidence showing assistant output remains grounded and classification-safe across representative scenarios.

### 49. End-to-end package release gate
**Justification:** Defense readiness and logistics changes should not ship without proving the declared APIs, events, workbenches, assistant skills, and release evidence all still work together. A passing unit test alone is not enough.
**Improvement:** Add an end-to-end release gate that exercises unit readiness creation, mission asset recording, maintenance projection, supply readiness scoring, deployment kit validation, movement release, and evidence-pack generation in one package-local scenario. Fail the package release when any declared surface breaks the flow.
**Acceptance evidence:** One scenario-based release test spanning the full operational path, generated release-evidence artifacts, and a recorded pass/fail summary tied to the package version.

### 50. After-action feedback loop into readiness rules
**Justification:** Readiness models drift if they never learn from actual deployment outcomes, movement delays, or sustainment failures. The package should improve based on what happened in real operations, not only on what planners expected.
**Improvement:** Add an after-action feedback loop that records whether readiness projections, maintenance forecasts, supply assumptions, and movement plans matched actual outcomes, then proposes tuned rules or parameters for review. Keep the loop governed so proposed changes require approval before they affect future readiness decisions.
**Acceptance evidence:** After-action comparison reports, governed parameter-change proposals, and release evidence showing how operational feedback is captured without automatically rewriting approved policy.
