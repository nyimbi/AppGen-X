# Maritime Shipping Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key: `maritime_shipping_operations`
- Manifest description: voyages, vessels, cargo, charter parties, port calls, demurrage, bunkers, and marine operations
- Owned tables: `voyage`, `vessel`, `cargo_booking`, `charter_party`, `port_call`, `demurrage_claim`, `bunker_event`, `maritime_shipping_operations_policy_rule`, `maritime_shipping_operations_runtime_parameter`, `maritime_shipping_operations_schema_extension`, `maritime_shipping_operations_control_assertion`, `maritime_shipping_operations_governed_model`
- Current APIs: `POST /voyages`, `POST /vessels`, `POST /cargo-bookings`, `POST /charter-partys`, `POST /port-calls`, `GET /maritime-shipping-operations-workbench`
- Emitted events: `MaritimeShippingOperationsCreated`, `MaritimeShippingOperationsUpdated`, `MaritimeShippingOperationsApproved`, `MaritimeShippingOperationsExceptionOpened`
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Workflows: `maritime_shipping_operations_create_voyage_workflow`, `maritime_shipping_operations_record_vessel_workflow`
- UI fragments: `MaritimeShippingOperationsWorkbench`, `MaritimeShippingOperationsDetail`, `MaritimeShippingOperationsAssistantPanel`
- Release artifacts named in the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`
- Advanced capabilities already declared in the package: event-sourced history, anomaly detection, semantic document understanding, predictive risk scoring, scenario simulation, audit proofs, continuous controls, carbon awareness, cross-PBC event federation, and governed AI execution

### 1. Voyage Leg And Rotation Model
**Justification:** The package exposes voyage creation, but maritime operators need each voyage decomposed into legs, rotations, sea passages, and terminal stays before schedule promises or cost exposure can be trusted.

**Improvement:** Expand `voyage` so one record carries service string, trade lane, laden versus ballast status, sequential voyage legs, linked `port_call` milestones, canal transits, and revised versus actual ETA/ETD values. Model voyage status around planning, published, commenced, disrupted, completed, and post-voyage settlement rather than a single flat status field.

**Acceptance evidence:** Schema and API examples showing multi-leg voyages, timeline rendering in `MaritimeShippingOperationsDetail`, and tests proving a late upstream leg propagates to downstream calls and customer-facing milestones.

### 2. Vessel Schedule Reliability Baseline
**Justification:** Shipping operations live or die on schedule reliability, and the current manifest has vessels and voyages but no explicit baseline for on-time performance or recovery logic.

**Improvement:** Add schedule reliability projections that compare proforma versus revised versus actual vessel movements, with berth window adherence, weather delay, canal delay, and congestion delay buckets. Link the schedule baseline to `vessel` and `voyage` so planners can see whether a delay is isolated or part of a persistent string slippage pattern.

**Acceptance evidence:** Workbench metrics for schedule reliability, drill-down from vessel to voyage string performance, and test fixtures that differentiate pure port congestion from cascading network delay.

### 3. Port Call Window Commitment Management
**Justification:** A port call is more than an arrival timestamp; nomination, pilotage, berth assignment, tug requirements, and cutoff commitments must be coordinated in one operational view.

**Improvement:** Extend `port_call` with berth window commitment, terminal code, pilot ordered/boarded timestamps, tug arrangement, gang requested/confirmed, crane intensity assumptions, and load/discharge working windows. Include explicit reasons for call omission, call swap, and berth rollover.

**Acceptance evidence:** `MaritimeShippingOperationsWorkbench` views for upcoming port calls, alert badges for missed nomination windows, and route-level tests for berth rollover scenarios.

### 4. Statement Of Facts And Time-Sheet Capture
**Justification:** Laytime, demurrage, and post-call disputes depend on an auditable statement of facts rather than after-the-fact commentary.

**Improvement:** Add structured `port_call` event capture for NOR tendered, all fast, first line, hatch open, hose connected, cargo operations start/stop, weather interruption, strike, shifting, and final line. Preserve source, local time zone, and evidence attachment for every event so the sequence can support laytime calculations later.

**Acceptance evidence:** Event timeline screenshots in `MaritimeShippingOperationsDetail`, attachments linked to each operational milestone, and tests proving time-sheet corrections keep full audit lineage.

### 5. Voyage Capacity And Cargo Booking Allocation
**Justification:** `cargo_booking` cannot remain a generic order object; bookings need allocation against vessel intake, deadweight, TEU, reefer plugs, and hazardous cargo limits.

**Improvement:** Add allocation logic that reserves slots by voyage leg, equipment type, commodity class, and stowage constraint, with waitlist handling when a sailing is oversubscribed. Support booking acceptance, conditional acceptance, and rollover recommendation based on remaining vessel capacity and commercial priority.

**Acceptance evidence:** Capacity utilization projections, booking waitlist tests, and UI evidence that overbooked sailings surface the specific limiting factor instead of a generic rejection.

### 6. Booking Amendment And Cutoff Governance
**Justification:** Late changes to quantity, commodity, or documentation create downstream port and stowage risk if the cutoffs are not explicit.

**Improvement:** Introduce booking cutoffs for documentation, customs filing, hazardous declaration, VGM, container release, and gate-in, each tied to the relevant `voyage` and `port_call`. Every amendment should state whether it remains inside cutoff, requires approval, or must be rolled to another sailing.

**Acceptance evidence:** Booking amendment audit trail, cutoff countdown indicators in the workbench, and regression tests covering accepted, conditionally accepted, and rejected late amendments.

### 7. Bill Of Lading Draft To Issue Lifecycle
**Justification:** Bills of lading are core maritime evidence, yet the current table set does not expose a governed draft, approval, issue, surrender, and amendment lifecycle.

**Improvement:** Represent bill of lading status inside the shipping domain as draft, customer-review, approved-to-issue, issued, surrendered, switched, corrected, and archived, with linkage to `cargo_booking`, `voyage`, and discharge obligations. Capture shipper, consignee, notify party, freight term, original count, and release mode without relying on free-text only.

**Acceptance evidence:** Document lifecycle tests, UI trace from booking to issued bill, and release evidence showing who approved each bill transition and which booking instructions were applied.

### 8. Stowage Planning Constraints
**Justification:** Maritime execution quality depends on where cargo sits on the vessel, not only whether it was booked.

**Improvement:** Add stowage planning data for bay/row/tier intent, discharge sequence, stack weight, segregation rule, lashing requirement, hatch constraint, and restow exposure. Use this to warn when bookings accepted commercially create operationally impossible load lists.

**Acceptance evidence:** Stowage conflict cards, restow-risk indicators for multi-port voyages, and tests proving the system blocks impossible discharge sequences before final load confirmation.

### 9. Dangerous Goods And Special Cargo Controls
**Justification:** Hazardous cargo, breakbulk, OOG, and project cargo need tighter controls than standard container or bulk bookings.

**Improvement:** Add class-specific validation for IMDG segregation, flashpoint evidence, packing certificate completeness, over-dimension measurements, lifting requirements, and terminal acceptance prerequisites. Surface exceptions early so planners can reject or reroute hazardous and special cargo before the cargo reaches the quay.

**Acceptance evidence:** Rule packs for dangerous goods and OOG cargo, exception queues separated by severity, and evidence that booking approval is blocked when mandatory special-cargo data is missing.

### 10. Reefer And Temperature-Controlled Cargo Assurance
**Justification:** Reefer bookings fail operationally when plug availability, set-point instructions, and monitoring responsibilities are not explicit.

**Improvement:** Extend `cargo_booking` and voyage allocation views with reefer plug reservation, set-point, ventilation, humidity, pre-trip inspection, genset dependency, and temperature deviation handling. Support exception flows for late set-point changes and lost reefer telemetry.

**Acceptance evidence:** Reefer capacity views by sailing, exception tests for missing PTI confirmation, and UI evidence that temperature-controlled bookings are isolated from standard dry cargo work queues.

### 11. Charter Party Clause Library
**Justification:** `charter_party` needs to hold operational clauses that drive voyage behavior, not only a signed commercial reference.

**Improvement:** Normalize charter party terms for laycan, loading/discharge rates, demurrage rate, despatch rate, off-hire triggers, bunker quality obligations, performance warranties, speed and consumption basis, and notice requirements. Each clause should be versioned and mapped to the operational objects it constrains.

**Acceptance evidence:** Clause registry entries, comparison views between charter versions, and tests proving operational calculations use clause data instead of hand-entered overrides.

### 12. Laytime Computation Engine
**Justification:** Laytime determines whether a call becomes profitable or contentious, and it must be computable directly from operational events.

**Improvement:** Build laytime logic from `port_call` events and charter clauses, including notice validity, reversible versus non-reversible laytime, SHEX/SHINC handling, weather interruption, shifting, strike, and pumping warranty exceptions. Show running used laytime, remaining laytime, and when the clock is stopped or resumed.

**Acceptance evidence:** Laytime calculation fixtures for tanker and dry-bulk patterns, detailed computation traces, and audit exports that reconstruct the final statement used in a claim.

### 13. Demurrage And Detention Exposure Engine
**Justification:** The manifest includes `demurrage_claim`, but commercial teams also need forward-looking exposure before a claim is filed.

**Improvement:** Distinguish voyage-level demurrage from equipment detention, calculate exposure from current event sequences, and classify the charge by responsible party, port, container/equipment, and dispute status. Include running exposure, invoiced amount, contested amount, and collected amount so finance and operations read the same truth.

**Acceptance evidence:** Exposure dashboards, test cases for laytime-generated demurrage and container detention, and evidence that disputed claims remain traceable back to the triggering operational events.

### 14. Demurrage Claim Dossier Assembly
**Justification:** Claims succeed or fail on the completeness of supporting evidence, not only on the arithmetic.

**Improvement:** Add a dossier builder for `demurrage_claim` that packages statement of facts, NOR, charter clauses, communications, pumping logs, weather evidence, and approval notes into one governed claim set. Track whether a claim is draft, submitted, rebutted, negotiated, settled, or written off.

**Acceptance evidence:** Claim dossier previews, document completeness rules, and release evidence demonstrating a full claim package can be reproduced without manual file hunting.

### 15. Bunker Uplift Planning
**Justification:** `bunker_event` should support bunker planning, not only bunker recording after the fact.

**Improvement:** Model planned uplift port, supplier nomination, grade, quantity, density, sulfur cap context, price basis, barge window, and expected ROB effect for each voyage segment. Let planners compare whether to bunker at the current port, defer to the next port, or hedge against congestion and ECA entry.

**Acceptance evidence:** Scenario comparison screens for bunker ports, tests for ROB sufficiency across voyage legs, and explicit decision evidence linking uplift plans to the selected voyage plan.

### 16. ROB And Consumption Variance Tracking
**Justification:** Fuel cost and schedule risk both hinge on whether actual consumption matches the assumed speed and weather profile.

**Improvement:** Track ROB at departure and arrival, noon-report consumption, idle consumption, berth consumption, speed/consumption deviation, and unexplained loss versus expected burn. Associate variance with weather, waiting time, speed-up orders, hull condition, or possible reporting anomalies.

**Acceptance evidence:** Consumption variance charts, anomaly flags on missing or implausible ROB changes, and calculations showing how bunker variance alters voyage contribution.

### 17. Carbon And Sustainability Operating View
**Justification:** The manifest already declares carbon and sustainability awareness, so the backlog should turn that flag into operational behavior.

**Improvement:** Add voyage-level carbon indicators such as emissions per TEU or ton moved, CII exposure, ECA fuel-switch events, and carbon impact of schedule recovery choices. Show when a speed-up decision improves schedule reliability but materially worsens emissions and bunker spend.

**Acceptance evidence:** Carbon-aware voyage scenarios, UI badges for ECA entry and fuel-switch obligations, and tests proving carbon metrics update when voyage distance, speed, or bunker grade changes.

### 18. Crewing Boundary And Hand-Off Rules
**Justification:** Maritime shipping operations must respect the crewing boundary; this PBC should consume crewing status that affects voyages without becoming a crew management system.

**Improvement:** Define a boundary contract where the shipping package reads vessel readiness signals such as minimum safe manning valid, bridge-team deficiency, or crew change restriction, then opens voyage or port-call exceptions when those signals block operations. Avoid storing crew rosters as owned maritime shipping tables; store only the operational impact and source reference.

**Acceptance evidence:** Boundary tests showing incoming crewing readiness signals affect voyage release decisions, plus negative tests proving the package does not create crew roster CRUD surfaces.

### 19. Voyage Compliance Obligation Register
**Justification:** The same voyage can trigger customs, sanctions, emissions, cargo, and port-state compliance requirements that must be tracked together.

**Improvement:** Add a compliance register tied to `voyage`, `port_call`, and `cargo_booking` for customs filing, manifest submission, hazardous declaration, ballast water obligation, sulfur compliance, sanctions approval, and discharge permit readiness. Each obligation should carry due date, status, accountable role, source regulation, and closure evidence.

**Acceptance evidence:** Compliance board views in `MaritimeShippingOperationsWorkbench`, overdue obligation alerts, and test fixtures for missed filing deadlines that automatically open exceptions.

### 20. Restricted Party And Sanctions Screening
**Justification:** Commercial acceptance and document issue must stop when shipper, consignee, bank, or service counterparty is restricted.

**Improvement:** Screen parties connected to bookings, bills of lading, charters, and bunker suppliers, then record screening outcome, list version, analyst disposition, and approval trail. Trigger re-screening when party data changes or when a sailing nears a restricted port or cargo corridor.

**Acceptance evidence:** Re-screening event tests, blocked-document issue scenarios, and analyst review evidence that matches the screening decision shown to users.

### 21. Port And Corridor Restriction Intelligence
**Justification:** Local rules around draft, congestion, strike action, tidal windows, pilotage, canal booking, and war-risk corridors materially change the voyage plan.

**Improvement:** Introduce a rule layer that attaches port and corridor restrictions to `port_call` and `voyage`, including draft limits, daylight-only movements, convoy windows, tug minima, strike notices, and high-risk area routing. Use these rules to explain why a schedule or bunker plan must change.

**Acceptance evidence:** Rule simulation examples for tide-limited ports and restricted corridors, decision cards showing which restriction fired, and tests proving schedule options respect those local constraints.

### 22. Domain Event Taxonomy Expansion
**Justification:** The current emitted events are broad lifecycle markers; downstream shipping, finance, and compliance consumers need events at the level of operational truth.

**Improvement:** Add typed events for voyage published, schedule slipped, berth window missed, cargo booking waitlisted, bill issued, laytime commenced, demurrage claim filed, bunker plan approved, and compliance obligation breached. Keep the existing package-level events for compatibility while making downstream automation depend on the richer event set.

**Acceptance evidence:** Event schemas, compatibility notes, and tests showing both legacy package events and new maritime-specific events are emitted in the correct order.

### 23. Event-Sourced Operational History
**Justification:** The manifest already claims event-sourced operational history, but voyage disputes and audit reviews require full replayable reconstruction of what changed and why.

**Improvement:** Persist immutable domain events for material changes across `voyage`, `port_call`, `cargo_booking`, `charter_party`, `demurrage_claim`, and `bunker_event`, including actor, command, policy version, and source document span where relevant. Use replay to rebuild timeline views and to compare historical projections with current corrected truth.

**Acceptance evidence:** Replay tests, point-in-time read models, and UI evidence that operators can inspect the exact event sequence leading to a disrupted voyage or contested claim.

### 24. Consumed Event Federation
**Justification:** `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` are declared consumed events, but each needs a clear maritime reaction path.

**Improvement:** Define handler outcomes for each consumed event: policy changes re-evaluate open bookings and compliance obligations, audit seals lock evidence packages, and KPI changes refresh risk and workbench signals. Preserve source event lineage on every resulting maritime state transition or exception.

**Acceptance evidence:** Idempotency tests, lineage links back to the consumed event, and operator-visible annotations explaining why a booking or voyage changed after external events arrived.

### 25. Retry And Dead-Letter Operator Console
**Justification:** Dead-letter handling is listed as a capability, yet maritime operations teams need a controlled console for resubmitting failed messages without corrupting the operational record.

**Improvement:** Build a dead-letter work queue that shows failed message type, voyage or booking context, retry count, poison-message reason, and safe replay options. Require analyst classification before replay when the failed message could reopen claims, alter document issue, or re-trigger customer notifications.

**Acceptance evidence:** Dead-letter queue views, retry audit logs, and tests proving duplicate replays do not create duplicate bookings, claims, or bunker events.

### 26. Policy Rule Governance Workbench
**Justification:** `maritime_shipping_operations_policy_rule` should be governed by domain users, not edited indirectly through code changes.

**Improvement:** Create policy-rule screens for booking acceptance, dangerous-goods checks, sanctions gates, demurrage approval limits, and bunker decision thresholds, each with effective-from dates and controlled rollout. Show impact preview on open voyages and bookings before a rule version is activated.

**Acceptance evidence:** Rule version history, preview simulations, and approval evidence proving policy edits are visible and auditable in the package UI.

### 27. Runtime Parameter Guardrails
**Justification:** `maritime_shipping_operations_runtime_parameter` should hold safe operating tolerances, not undocumented constants embedded in handlers.

**Improvement:** Externalize thresholds such as minimum schedule buffer, reefer alert tolerance, laytime warning percentage, demurrage auto-escalation value, bunker variance tolerance, and stale-port-call timer. Add bounds, owner, rationale, and rollback data to every parameter.

**Acceptance evidence:** Parameter registry screens, validation rules for out-of-range updates, and tests showing changed parameters affect calculations only after approved activation.

### 28. Schema Extension Registry For New Maritime Fields
**Justification:** Trade lanes, fuel rules, and cargo products evolve, so the package needs a disciplined way to add new fields without breaking projections and evidence packs.

**Improvement:** Use `maritime_shipping_operations_schema_extension` to register new attributes, reference lists, and projection dependencies for fields such as alternative fuel indicators, terminal partner references, or new cargo handling flags. Require compatibility checks against APIs, events, analytics, and release evidence templates before activation.

**Acceptance evidence:** Extension review checklist, backfill plan artifacts, and tests proving older voyage and booking records remain readable after new fields are enabled.

### 29. Voyage-Centric Workbench Board
**Justification:** The current `GET /maritime-shipping-operations-workbench` surface needs a clear operating model for planners and supervisors.

**Improvement:** Make `MaritimeShippingOperationsWorkbench` default to voyage boards that group work by pre-fixture planning, pre-arrival readiness, in-port execution, post-departure settlement, and exception resolution. Let users pivot between vessel-string view, port view, and cargo commitment view without losing the same operational filters.

**Acceptance evidence:** UI route contracts, saved filters for voyage planner personas, and screenshots showing one-click access from a voyage card to bookings, port calls, claims, and bunker plans.

### 30. Detail View Narrative Timeline
**Justification:** Maritime users need one coherent story per voyage or port call rather than scattered tabs with no chronology.

**Improvement:** Turn `MaritimeShippingOperationsDetail` into a narrative timeline that merges domain events, documents, policy decisions, consumption updates, laytime clock events, and human comments in strict order. Support local time and UTC display so investigators can reconcile shipboard logs with office actions.

**Acceptance evidence:** Timeline rendering tests, timezone conversion checks, and operator evidence that corrected events retain both original and superseding entries.

### 31. Assistant Panel With Previewed Maritime Actions
**Justification:** The manifest includes governed datastore CRUD and AI task assistance, so the assistant must act like a controlled shipping operator, not a side channel.

**Improvement:** Use `MaritimeShippingOperationsAssistantPanel` to preview schedule recovery actions, booking amendments, bill-of-lading corrections, claim-note drafts, and bunker plan alternatives before any mutation occurs. Each action should display affected voyages, bookings, documents, obligations, and emitted events.

**Acceptance evidence:** Preview/confirm flows, denied-action examples when permissions are insufficient, and audit entries showing the assistant path is indistinguishable from a governed human command path.

### 32. Agent Skill For Schedule Recovery
**Justification:** Late vessels create many small decisions, and operators need an assistant skill dedicated to maritime recovery rather than generic task generation.

**Improvement:** Add a skill that evaluates skipping a call, swapping berth sequence, cutting cargo, revising cutoffs, or speeding up the next leg, with visible tradeoffs in customer impact, bunker cost, demurrage risk, and emissions. It should propose options, not silently choose one.

**Acceptance evidence:** Skill manifests, option-comparison outputs, and tests showing the skill cites the exact schedule, port, and cargo facts behind each recovery recommendation.

### 33. Agent Skill For Booking And Bill Intake
**Justification:** Semantic document understanding becomes valuable only when it can turn booking requests and shipping instructions into safe drafts.

**Improvement:** Add an intake skill that reads booking forms, shipping instructions, and bill-of-lading amendment requests, extracts parties, container counts, commodity, freight terms, marks, and routing, then builds draft `cargo_booking` or bill changes for review. It should highlight ambiguities such as conflicting consignee names, missing notify party, or inconsistent quantity totals.

**Acceptance evidence:** Extraction test set for maritime documents, confidence and ambiguity markers in the assistant panel, and approval evidence that accepted drafts retain source-document references.

### 34. Agent Skill For Claims Triage
**Justification:** Claims handling is repetitive but sensitive; the assistant should assemble facts without masking uncertainty.

**Improvement:** Provide a claim-triage skill that reviews statement-of-facts sequences, charter clauses, correspondence, and prior settlements, then drafts a disposition path such as accept, negotiate, rebut, or request more evidence. The skill should surface the exact event gaps or conflicting timestamps that weaken a claim.

**Acceptance evidence:** Triage summaries linked to `demurrage_claim`, rebuttal draft examples, and tests confirming the skill refuses to recommend settlement when mandatory claim evidence is missing.

### 35. Counterfactual Voyage Simulation
**Justification:** The manifest declares scenario simulation, and maritime planners need to ask what happens if a vessel diverts, skips, speeds up, or changes bunker port.

**Improvement:** Build non-mutating simulations for voyage alternatives including call omission, terminal swap, transshipment reroute, speed change, and alternative bunker uplift. Show consequences across schedule reliability, booking fulfillment, laytime risk, claim exposure, bunker cost, and carbon profile.

**Acceptance evidence:** Side-by-side scenario panels, reproducible simulation inputs, and tests proving simulation results do not mutate live voyage, booking, or claim records.

### 36. Predictive Risk Scoring
**Justification:** Predictive risk scoring is listed in the manifest but needs shipping-specific features to be operationally credible.

**Improvement:** Score voyages, port calls, and bookings using features such as historical terminal delay, weather severity, congestion trend, hazardous cargo mix, short document lead time, repeated supplier variance, and charter clause exposure. Expose the score together with the dominant factors so planners can act before disruption materializes.

**Acceptance evidence:** Feature manifests, calibration reports, and UI explanation cards that map risk changes back to vessel, port, cargo, and clause conditions.

### 37. Autonomous Anomaly Detection
**Justification:** Maritime data streams contain many subtle contradictions that humans miss under time pressure.

**Improvement:** Detect anomalies such as impossible time order, missing departure after completion, bunker quantity inconsistent with ROB change, bill quantities that exceed booking totals, and duplicated port-call milestones. Separate operational anomalies from likely data-entry mistakes so teams know whether to stop execution or simply correct records.

**Acceptance evidence:** Anomaly categories with severity, suppression governance, and tests proving the system distinguishes a late but plausible event from a logically impossible one.

### 38. Multi-Tenant And Service-Line Isolation
**Justification:** The manifest claims multi-tenant policy isolation, and shipping operators often need separation by business unit, liner service, chartering desk, or regional cluster.

**Improvement:** Partition workbench data, policy rules, runtime parameters, and evidence packages by tenant and operating segment while still allowing controlled shared reference data. Prevent one operator from viewing or mutating voyages, bookings, or claims outside the assigned tenant boundary.

**Acceptance evidence:** Tenant-isolation tests, policy scoping examples, and UI permission checks that hide unrelated service-line data without breaking shared operational metrics.

### 39. Maritime Reference Data Quality Gates
**Justification:** Core shipping records are only as reliable as their reference identifiers.

**Improvement:** Validate IMO number, call sign, UN/LOCODE, terminal code, carrier/service identifiers, cargo harmonized descriptions, dangerous-goods references, and bunker grade codes at intake and amendment time. Track when values were matched, overridden, or manually justified.

**Acceptance evidence:** Reference validation fixtures, override audit logs, and workbench warnings that identify exactly which identifier blocks progression to the next workflow step.

### 40. Bulk Operations For Schedules And Bookings
**Justification:** Shipping lines and operators often revise dozens of sailings or bookings in one disruption event.

**Improvement:** Add bulk update flows for schedule revisions, booking rollover, cutoff changes, party notifications, and claim-status progression with row-level validation and partial success handling. Preserve per-record audit history even when the action begins as one bulk instruction.

**Acceptance evidence:** Bulk action job views, row-level outcome reports, and tests proving one failed booking update does not hide successful updates on the same voyage.

### 41. Search, Report, And Export Surfaces
**Justification:** Maritime operations teams need to answer questions such as which voyages are exposed to demurrage this week or which bills remain unissued for tomorrow's sailings.

**Improvement:** Add search and export views over voyages, port calls, bookings, bills, claims, and bunker events using shipping-specific filters like service string, load port, discharge port, vessel, charter type, laytime status, and document release mode. Ensure exports retain reference keys back to the governed package records.

**Acceptance evidence:** Filter contract tests, export previews with stable identifiers, and report evidence showing users can reach operational answers without ad hoc database access.

### 42. Partner Integration And Acknowledgement Tracking
**Justification:** Port agents, terminals, bunker suppliers, and customs intermediaries create operational dependencies that need explicit message tracking.

**Improvement:** Track outbound and inbound partner exchanges for berth requests, terminal instructions, manifest filings, bunker nominations, and claim correspondence, including sent time, acknowledgement time, rejection reason, and manual fallback. Link partner exchanges to the voyage, port call, or claim they affect.

**Acceptance evidence:** Integration status panels, acknowledgement timeout alerts, and tests showing a rejected partner message opens an actionable exception with the correct operational context.

### 43. Mobile And Responsive Port Operations UX
**Justification:** Port-call execution often happens away from a desk, so the package UI must support responsive operational use rather than assuming a wide desktop only.

**Improvement:** Prioritize mobile-ready views for port-call event capture, statement-of-facts updates, exception acknowledgement, and approval actions with large touch targets and low-bandwidth tolerance. Keep the same operational facts visible on both handheld and desktop layouts.

**Acceptance evidence:** Responsive UI snapshots for `MaritimeShippingOperationsWorkbench` and `MaritimeShippingOperationsDetail`, offline/intermittent-network interaction tests, and evidence that critical actions remain permission-guarded on smaller devices.

### 44. Continuous Control Testing
**Justification:** Continuous release assurance and `maritime_shipping_operations_control_assertion` should verify controls while operations are in motion.

**Improvement:** Add active controls for segregation of duties on bill issue and claim approval, stale sanction screening, missing charter clause linkage, missing statement-of-facts evidence, and parameter overrides outside approved ranges. Emit control failures as first-class operational exceptions rather than burying them in logs.

**Acceptance evidence:** Control dashboards, failing-control events, and test fixtures proving control assertions are generated automatically for broken maritime workflows.

### 45. Cryptographic Audit Proofs
**Justification:** Audit logs are more credible when the package can prove the integrity of the evidence set presented to reviewers.

**Improvement:** Hash-chain critical maritime artifacts including operational timelines, bill approvals, claim dossiers, policy versions, and release evidence packs so reviewers can verify nothing was altered after sealing. Support redacted proofs when documents contain commercially sensitive freight terms or sanctioned-party references.

**Acceptance evidence:** Proof manifests, verification commands or screens, and release artifacts showing sealed evidence for at least one voyage, one claim, and one bill-of-lading workflow.

### 46. Maritime Analytics Cockpit
**Justification:** The declared analytics surface should answer operating questions, not only display generic counts.

**Improvement:** Build dashboards for schedule reliability, booking conversion, booking rollover rate, bill issue latency, laytime utilization, demurrage exposure, bunker variance, carbon intensity, and unresolved compliance exceptions. Make every KPI drill into the underlying voyages, calls, bookings, claims, or bunker events that drive it.

**Acceptance evidence:** Metric definitions, drill-through routes, and tests confirming KPI values reconcile with the governed source records for a sample operating period.

### 47. Release Evidence Pack For Maritime Changes
**Justification:** The manifest explicitly names `RELEASE_EVIDENCE.md`, so shipping-critical changes need a release pack that proves the domain was exercised, not merely deployed.

**Improvement:** Require every material release to capture affected voyage scenarios, booking and bill flows, claim calculations, bunker scenarios, event contracts, control assertions, and UI screenshots for the changed maritime surfaces. Organize the pack so auditors and operators can see what changed, how it was tested, and what residual shipping risk remains.

**Acceptance evidence:** A release pack template tied to `RELEASE_EVIDENCE.md`, signed-off scenario checklists, and sample evidence that covers at least one end-to-end voyage from booking through post-call settlement.

### 48. Test Fixtures And Digital-Twin Voyage Data
**Justification:** Deep maritime logic cannot be validated with flat placeholder data.

**Improvement:** Create fixture sets representing liner, tanker, and dry-bulk patterns with realistic port rotations, laytime events, bunker movements, document flows, and claim outcomes. Use those fixtures across contract tests, analytics checks, assistant skills, and release evidence generation.

**Acceptance evidence:** Named fixture catalogs, replayable event streams, and tests showing the same digital-twin voyage data drives API, UI, and analytics verification consistently.

### 49. Operational Readiness And Incident Drills
**Justification:** Maritime disruptions are certain, so the package needs practiced responses for congestion spikes, missed cutoffs, and partner outages.

**Improvement:** Add readiness drills for schedule collapse, berth cancellation, sanctions hit after booking confirmation, dead-letter accumulation, bunker delivery failure, and claim-evidence corruption alerts. Record who responded, what fallback path was used, and whether the operational SLA was preserved.

**Acceptance evidence:** Drill playbooks, incident rehearsal logs, and release evidence proving at least one recovery exercise was run for messaging failure and one for severe schedule disruption.

### 50. Go-Live Acceptance Gates
**Justification:** Shipping operations should not promote new logic unless the core voyage, cargo, document, claim, bunker, UI, and evidence paths all work together.

**Improvement:** Define go-live gates covering voyage creation, vessel schedule revision, port-call event capture, booking acceptance, bill issue, laytime and demurrage calculation, bunker planning, compliance exception handling, assistant preview flows, event emission, and evidence sealing. A release should fail the gate if any one of those maritime-critical paths lacks current proof.

**Acceptance evidence:** A single acceptance checklist with pass/fail results, linked scenario evidence, and a release decision record showing the package was promoted only after all critical maritime paths passed.
