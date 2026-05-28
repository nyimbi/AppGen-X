# Hotel Revenue Management Improvement Backlog

This backlog is specific to the exact key `hotel_revenue_management` and is grounded in the manifest surfaces for room types, rate plans, inventory controls, channel inventory, demand forecasts, overbooking, yield decisions, revenue snapshots, workbench APIs, assistant support, events, and release evidence.

## Current Domain Evidence Used

- PBC key: `hotel_revenue_management`
- Description: `Room inventory, rates, channels, demand forecasts, overbooking, yield, and hotel revenue controls`
- Tables: `room_type`, `rate_plan`, `channel_inventory`, `demand_forecast`, `overbooking_policy`, `yield_decision`, `revenue_snapshot`, `hotel_revenue_management_policy_rule`, `hotel_revenue_management_runtime_parameter`, `hotel_revenue_management_schema_extension`, `hotel_revenue_management_control_assertion`, `hotel_revenue_management_governed_model`
- APIs: `POST /room-types`, `POST /rate-plans`, `POST /channel-inventorys`, `POST /demand-forecasts`, `POST /overbooking-policys`, `GET /hotel-revenue-management-workbench`
- Workflows: `hotel_revenue_management_create_room_type_workflow`, `hotel_revenue_management_record_rate_plan_workflow`
- UI fragments: `HotelRevenueManagementWorkbench`, `HotelRevenueManagementDetail`, `HotelRevenueManagementAssistantPanel`
- Emits: `HotelRevenueManagementCreated`, `HotelRevenueManagementUpdated`, `HotelRevenueManagementApproved`, `HotelRevenueManagementExceptionOpened`
- Consumes: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Analytics and advanced capabilities: `hotel_revenue_management_risk_score`, `hotel_revenue_management_workbench_metric`, `hotel_revenue_management_counterfactual_scenario_simulation`, `hotel_revenue_management_cryptographic_audit_proofs`, `hotel_revenue_management_governed_ai_agent_execution`
- Release evidence docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`

## Backlog

### 1. Sellable room-type inventory matrix

**Justification:** Revenue controls are only credible if `room_type` capacity distinguishes physical rooms, sellable rooms, out-of-order buffers, and upgrade substitutes.
**Improvement:** Add a sellability matrix that tracks base inventory, maintenance holdbacks, complimentary allotments, and substitute-to room types by date band.
**Acceptance evidence:** The workbench shows sellable versus physical counts, tests prove blocked rooms no longer flow into pricing or overbooking decisions, and the matrix is traceable from room-type detail.
**Current Domain Evidence Used:** `room_type`, `POST /room-types`, `hotel_revenue_management_create_room_type_workflow`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.sellable_room_type_inventory_matrix`

### 2. Rate-plan inheritance and derivation graph

**Justification:** Hotels usually derive package, member, corporate, and wholesale pricing from a base ladder, and hidden overrides make rate maintenance unsafe.
**Improvement:** Model parent-child `rate_plan` inheritance for price, fences, restrictions, and channel scope, with explicit override markers at each derived node.
**Acceptance evidence:** The detail page renders the derivation chain, override conflicts block approval, and tests confirm parent changes only flow where a child has not overridden the field.
**Current Domain Evidence Used:** `rate_plan`, `POST /rate-plans`, `hotel_revenue_management_record_rate_plan_workflow`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.rate_plan_inheritance_graph`

### 3. BAR ladder and price-fence validator

**Justification:** Best available rate ladders fail when refundability, advance-purchase rules, and member fences contradict each other.
**Improvement:** Add validation for BAR ordering, discount gaps, refundability rules, membership fences, and advanced-purchase cutoffs before a rate plan can publish.
**Acceptance evidence:** Invalid ladders are rejected with field-level reasons, the assistant can explain the broken fence, and release evidence includes a BAR validation report for active public rates.
**Current Domain Evidence Used:** `rate_plan`, `hotel_revenue_management_policy_rule`, `HotelRevenueManagementAssistantPanel`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.bar_ladder_and_fence_validator`

### 4. Restriction calendar for CTA, CTD, and LOS controls

**Justification:** Hotel restrictions live on dates and stay patterns, not just on rate records.
**Improvement:** Create a restriction calendar supporting CTA, CTD, min LOS, max LOS, and stay-through exceptions by date, room type, and rate plan.
**Acceptance evidence:** Operators can inspect restrictions on a calendar, conflicting LOS logic opens an exception, and tests verify multi-night itinerary handling across arrival and stay dates.
**Current Domain Evidence Used:** `rate_plan`, `channel_inventory`, `HotelRevenueManagementWorkbench`, `hotel_revenue_management_policy_rule`
**Exact key:** `hotel_revenue_management.restriction_calendar_controls`

### 5. Channel allotment and stop-sell controls

**Justification:** Distribution strategy requires per-channel inventory posture rather than one undifferentiated count.
**Improvement:** Expand `channel_inventory` to manage per-channel allotments, stop-sells, release-back rules, blackout windows, and controlled reopen actions.
**Acceptance evidence:** The workbench shows channel-level positions, stop-sell actions are audit-trailed, and tests confirm that closing one OTA does not change direct-channel availability unless a shared rule says so.
**Current Domain Evidence Used:** `channel_inventory`, `POST /channel-inventorys`, `HotelRevenueManagementWorkbench`, `HotelRevenueManagementUpdated`
**Exact key:** `hotel_revenue_management.channel_allotment_stop_sell_controls`

### 6. Channel parity exception tracking

**Justification:** Revenue teams need to separate intentional parity breaks from defective rate distribution.
**Improvement:** Add parity monitoring across public channels with explicit reason codes for approved exceptions such as member rates, packages, geo-fenced offers, and wholesale net rates.
**Acceptance evidence:** Parity breaks appear in an exception queue with rationale, approved breaks are labeled distinctly from defects, and tests show approved exceptions suppress noise without hiding real mismatches.
**Current Domain Evidence Used:** `rate_plan`, `channel_inventory`, `hotel_revenue_management_analytics`, `HotelRevenueManagementExceptionOpened`
**Exact key:** `hotel_revenue_management.channel_parity_exception_tracking`

### 7. Pickup curve baselines by stay date

**Justification:** Pickup pace is one of the clearest hotel revenue signals and needs stay-date precision.
**Improvement:** Store pickup baselines in `demand_forecast` by stay date, booking window, room type, and segment so live pace can be compared against expected build.
**Acceptance evidence:** The workbench charts pickup versus baseline, pace deviations open forecast exceptions, and tests verify booking-window math for same-day, near-term, and long-lead demand.
**Current Domain Evidence Used:** `demand_forecast`, `revenue_snapshot`, `hotel_revenue_management_workbench_metric`, `OperationalKpiChanged`
**Exact key:** `hotel_revenue_management.pickup_curve_baselines`

### 8. Demand forecast segmentation by transient, group, and corporate mix

**Justification:** Total room demand without segment mix hides the drivers of displacement, restriction stance, and channel posture.
**Improvement:** Extend `demand_forecast` to hold segmented transient, negotiated corporate, group, wholesale, and house-use demand with confidence bands and mix assumptions.
**Acceptance evidence:** Forecast detail shows segment totals and mix shifts, manual overrides roll up cleanly to overall demand, and tests confirm segment totals reconcile to the property forecast.
**Current Domain Evidence Used:** `demand_forecast`, `HotelRevenueManagementDetail`, `hotel_revenue_management_predictive_risk_scoring`, `hotel_revenue_management_workbench_metric`
**Exact key:** `hotel_revenue_management.segmented_demand_forecast_mix`

### 9. Event and holiday demand-impact modeling

**Justification:** Concerts, conferences, school holidays, and citywide events distort demand in ways that ordinary seasonality cannot explain.
**Improvement:** Add event-impact factors to `demand_forecast` so operators can model compression, shoulder spill, and post-event wash separately from baseline demand.
**Acceptance evidence:** Forecast scenarios store event tags and impact coefficients, the workbench compares baseline versus event-adjusted views, and release evidence includes at least one peak-date replay.
**Current Domain Evidence Used:** `demand_forecast`, `hotel_revenue_management_counterfactual_scenario_simulation`, `HotelRevenueManagementWorkbench`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.event_holiday_demand_modeling`

### 10. Overbooking limits by room type and arrival pattern

**Justification:** Overbooking is only safe when calibrated by room type, arrival pattern, and recovery options rather than one blanket percentage.
**Improvement:** Redesign `overbooking_policy` to support per-room-type caps, day-of-week adjustments, arrival-day protections, recovery hierarchies, and temporary override approval.
**Acceptance evidence:** Policy views show distinct caps by room type and date class, override history is preserved, and tests prove arrival-day protections prevent oversell beyond approved limits.
**Current Domain Evidence Used:** `overbooking_policy`, `POST /overbooking-policys`, `HotelRevenueManagementApproved`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.room_type_overbooking_limits`

### 11. Cancellation and no-show curve calibration

**Justification:** Overbooking and pricing both rely on realistic cancellation and no-show assumptions, which vary by segment and booking window.
**Improvement:** Attach cancellation, no-show, and early-departure curves to forecasts and overbooking policies by room type, rate family, and arrival horizon.
**Acceptance evidence:** Curve assumptions are versioned, curve changes trigger downstream recalculation, and tests verify that updated no-show behavior changes recommended oversell limits.
**Current Domain Evidence Used:** `demand_forecast`, `overbooking_policy`, `yield_decision`, `hotel_revenue_management_runtime_parameter`
**Exact key:** `hotel_revenue_management.cancellation_no_show_curve_calibration`

### 12. Group block wash and release rules

**Justification:** Group inventory behaves differently from transient demand, and wash assumptions need explicit handling to avoid inflated occupancy expectations.
**Improvement:** Add group-block wash percentages, pickup checkpoints, cut-off dates, and automatic release rules so underperforming block rooms flow back into transient inventory on time.
**Acceptance evidence:** The workbench shows held, picked-up, and released rooms by stay date, release actions are auditable, and tests confirm released rooms become sellable through the expected channels.
**Current Domain Evidence Used:** `channel_inventory`, `demand_forecast`, `yield_decision`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.group_block_wash_release_rules`

### 13. Displacement analysis for group quotes and blocks

**Justification:** Accepting a group should be measured against displaced transient revenue and not just topline block value.
**Improvement:** Add displacement analysis that estimates transient displacement, shoulder-night fill, ancillary value, and minimum acceptable group rate for the requested block pattern.
**Acceptance evidence:** Analysts can compare accept-versus-reject scenarios, yield decisions retain the displacement inputs used, and tests verify that compression nights raise the minimum acceptable group value.
**Current Domain Evidence Used:** `yield_decision`, `revenue_snapshot`, `hotel_revenue_management_counterfactual_scenario_simulation`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.group_block_displacement_analysis`

### 14. Comp-set boundary governance

**Justification:** Competitive pricing is noisy when the comp set is stale, too broad, or mixed across incomparable hotel products.
**Improvement:** Govern comp-set boundaries by market, submarket, star class, brand position, and room product comparability, and bind those boundaries to pricing logic.
**Acceptance evidence:** Comp-set changes require approval, pricing explanations cite the comp-set version used, and tests confirm out-of-bound competitor inputs are ignored until approved.
**Current Domain Evidence Used:** `hotel_revenue_management_governed_model`, `hotel_revenue_management_predictive_risk_scoring`, `yield_decision`, `HotelRevenueManagementApproved`
**Exact key:** `hotel_revenue_management.comp_set_boundary_governance`

### 15. Pricing experiment registry and guardrails

**Justification:** Revenue teams need a safe way to test rate moves, fences, and restriction strategies without losing operational traceability.
**Improvement:** Create a registry for pricing experiments covering hypothesis, target market, eligible channels, holdout design, start and end dates, and rollback criteria.
**Acceptance evidence:** Experiment records link to impacted rates and inventory, outcome metrics are captured in snapshots, and release evidence shows experiments can be closed or rolled back cleanly.
**Current Domain Evidence Used:** `rate_plan`, `channel_inventory`, `revenue_snapshot`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.pricing_experiment_registry`

### 16. Yield-decision explanation trail

**Justification:** A recommended price or restriction move is only useful when the operator can see the demand, inventory, and policy drivers behind it.
**Improvement:** Store an explanation bundle on every `yield_decision` with forecast inputs, pickup signals, restrictions, channel state, comp-set version, and rule references.
**Acceptance evidence:** The detail view renders a readable explanation tree, decision events include explanation references, and tests verify completeness for automated and manual decisions.
**Current Domain Evidence Used:** `yield_decision`, `demand_forecast`, `channel_inventory`, `hotel_revenue_management_policy_rule`
**Exact key:** `hotel_revenue_management.yield_decision_explanation_trail`

### 17. Channel-mix optimization recommendations

**Justification:** Profitability depends on which channels fill the hotel, not only whether the rooms sell.
**Improvement:** Add decision support that recommends channel open-close actions and rate differentials based on net revenue, acquisition cost, pace, and room-type scarcity.
**Acceptance evidence:** Recommendations cite projected net-revenue delta by channel, accepted actions are written back as governed changes, and tests confirm high-cost channels are deprioritized when direct demand can absorb nights.
**Current Domain Evidence Used:** `channel_inventory`, `yield_decision`, `revenue_snapshot`, `hotel_revenue_management_analytics`
**Exact key:** `hotel_revenue_management.channel_mix_optimization`

### 18. Last-room-availability policy controls

**Justification:** LRA commitments shape both contract compliance and revenue leakage, so they need explicit policy treatment.
**Improvement:** Add LRA controls by account type, room type, date class, and channel so protected inventory can be distinguished from freely closable inventory.
**Acceptance evidence:** LRA exceptions appear before a stop-sell is approved, policy changes are audit-trailed, and tests confirm protected accounts retain access while non-LRA channels close correctly.
**Current Domain Evidence Used:** `channel_inventory`, `hotel_revenue_management_policy_rule`, `PolicyChanged`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.last_room_availability_controls`

### 19. Shoulder-night and gap-night optimizer

**Justification:** Hotels often fill the peak night while leaving adjacent nights weak, which wastes the opportunity to lengthen stays.
**Improvement:** Add an optimizer that detects shoulder softness and recommends LOS offers, fenced discounts, or package positioning to fill gap nights around compression periods.
**Acceptance evidence:** Operators can review shoulder-night opportunities on the calendar, accepted plays create traceable rate or restriction changes, and tests distinguish gap nights from already-compressed nights.
**Current Domain Evidence Used:** `rate_plan`, `demand_forecast`, `yield_decision`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.shoulder_gap_night_optimizer`

### 20. Compression-night playbook workbench

**Justification:** Peak nights require fast coordination across pricing, restrictions, overbooking, and channel controls.
**Improvement:** Build a compression-night workspace that assembles pace, scarcity, restrictions, oversell stance, and recommended operator actions for high-pressure dates.
**Acceptance evidence:** The workbench highlights compression nights from policy thresholds, action checklists are captured with timestamps and approvers, and tests verify that the page stays coherent when one feed is stale.
**Current Domain Evidence Used:** `HotelRevenueManagementWorkbench`, `demand_forecast`, `channel_inventory`, `overbooking_policy`
**Exact key:** `hotel_revenue_management.compression_night_playbook_workbench`

### 21. Upgrade and downgrade substitution rules

**Justification:** Room-type substitution affects guest recovery and sellable capacity, so it needs explicit revenue-aware rules.
**Improvement:** Add substitution rules that describe when inventory can be upgraded or downgraded across `room_type` values, the revenue impact, and whether protected demand must be preserved.
**Acceptance evidence:** Yield decisions can reference allowed substitution paths, overbooking recovery uses the same paths, and tests verify that blocked substitutions never appear in recommendation flows.
**Current Domain Evidence Used:** `room_type`, `yield_decision`, `overbooking_policy`, `hotel_revenue_management_policy_rule`
**Exact key:** `hotel_revenue_management.room_type_substitution_rules`

### 22. Package-rate component margin controls

**Justification:** Package rates can look healthy on occupancy while quietly eroding net revenue if inclusions are not priced explicitly.
**Improvement:** Track package components inside `rate_plan` so breakfast, parking, credits, and other inclusions carry explicit margin assumptions and minimum contribution rules.
**Acceptance evidence:** Package detail views show component economics, low-margin packages raise approval warnings, and tests confirm bundled inclusions change net value calculations without corrupting base BAR data.
**Current Domain Evidence Used:** `rate_plan`, `revenue_snapshot`, `hotel_revenue_management_control_assertion`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.package_rate_margin_controls`

### 23. Negotiated and corporate blackout governance

**Justification:** Negotiated rate access often needs temporary blackout logic during compression, but those exceptions must be deliberate and auditable.
**Improvement:** Add blackout calendars, exemption lists, and approval flows for negotiated rates so protected accounts, crew business, and strategic contracts are handled consistently on peak dates.
**Acceptance evidence:** Blackout rules display beside active negotiated plans, exception approvals generate audit history, and tests confirm a blackout closes only the intended account set and dates.
**Current Domain Evidence Used:** `rate_plan`, `hotel_revenue_management_policy_rule`, `HotelRevenueManagementApproved`, `PolicyChanged`
**Exact key:** `hotel_revenue_management.negotiated_rate_blackout_governance`

### 24. Forecast override workflow with approval evidence

**Justification:** Manual overrides are unavoidable in revenue management, but silent overrides destroy trust in the forecast.
**Improvement:** Add a structured override workflow for `demand_forecast` with reason, expected duration, evidence note, required approver, and automatic expiry or review date.
**Acceptance evidence:** Overrides appear as layered values instead of silent replacements, expired overrides trigger alerts, and tests verify approval is required above configured variance thresholds.
**Current Domain Evidence Used:** `demand_forecast`, `hotel_revenue_management_runtime_parameter`, `HotelRevenueManagementApproved`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.forecast_override_workflow`

### 25. Occupancy, ADR, and RevPAR scenario simulator

**Justification:** Revenue strategy requires the ability to test pricing and restriction moves before they hit live dates.
**Improvement:** Extend scenario simulation to compare occupancy, ADR, RevPAR, room revenue, channel mix, and oversell exposure under alternate rates, restrictions, and forecast assumptions.
**Acceptance evidence:** The simulator stores named scenarios, compares them against the current baseline, and produces side-by-side KPI deltas with referenced inputs.
**Current Domain Evidence Used:** `hotel_revenue_management_counterfactual_scenario_simulation`, `yield_decision`, `revenue_snapshot`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.revenue_kpi_scenario_simulator`

### 26. Revenue snapshot lineage to source decisions

**Justification:** Snapshot metrics lose diagnostic value when operators cannot trace them back to the rates, restrictions, and decisions that produced them.
**Improvement:** Build lineage from `revenue_snapshot` to the rate plans, forecasts, channel controls, and yield decisions that shaped each metric period.
**Acceptance evidence:** Each snapshot links back to source records and versions, replay tests reconstruct a prior snapshot from source state, and auditors can export a lineage report for a chosen date range.
**Current Domain Evidence Used:** `revenue_snapshot`, `yield_decision`, `rate_plan`, `hotel_revenue_management_event_sourced_operational_history`
**Exact key:** `hotel_revenue_management.revenue_snapshot_lineage`

### 27. Stale forecast and stale pickup detection

**Justification:** A forecast can be internally valid but still operationally stale relative to current pace and volatility.
**Improvement:** Add freshness rules that compare live pickup against forecast update age, last override date, and volatility to identify forecasts that need attention.
**Acceptance evidence:** Stale forecasts appear in the workbench queue with severity, accepted refresh actions are timestamped, and tests verify different thresholds for low-volatility and high-volatility dates.
**Current Domain Evidence Used:** `demand_forecast`, `revenue_snapshot`, `OperationalKpiChanged`, `hotel_revenue_management_risk_score`
**Exact key:** `hotel_revenue_management.stale_forecast_pickup_detection`

### 28. Inventory correction API with idempotent replay

**Justification:** Distribution corrections happen frequently, and the package needs a safe way to repair inventory without duplicating downstream effects.
**Improvement:** Add correction and reapply commands for `channel_inventory` that use correction types, source references, and idempotency keys for replay-safe remediation.
**Acceptance evidence:** Duplicate corrections are ignored, correction events retain links to the original bad publish, and tests verify repair behavior across retries and out-of-order delivery.
**Current Domain Evidence Used:** `channel_inventory`, `idempotent_handlers`, `appgen_x_outbox_inbox_eventing`, `HotelRevenueManagementUpdated`
**Exact key:** `hotel_revenue_management.inventory_correction_api`

### 29. Rate-plan publishing readiness gate

**Justification:** A rate should not publish unless pricing, fences, restrictions, channel mapping, and approvals are all internally consistent.
**Improvement:** Add a readiness gate that scores every `rate_plan` against required rule checks, dependent inventory availability, approvals, and unresolved exceptions before activation.
**Acceptance evidence:** Unready plans show explicit blocking reasons, approved plans generate a readiness artifact in release evidence, and tests verify partially configured plans cannot publish.
**Current Domain Evidence Used:** `rate_plan`, `hotel_revenue_management_policy_rule`, `HotelRevenueManagementApproved`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.rate_plan_publish_readiness_gate`

### 30. Channel inventory retry and dead-letter cockpit

**Justification:** When distribution updates fail, the revenue team needs an operational view of what failed, why it failed, and what replay will do.
**Improvement:** Add a retry and dead-letter cockpit for `channel_inventory` changes with poison-message detection, replay preview, and suppression rules for known downstream outages.
**Acceptance evidence:** Operators can inspect failed payload lineage, retry only eligible messages, and prove through tests that replaying a fixed message resolves the dead letter without duplicate state.
**Current Domain Evidence Used:** `channel_inventory`, `retry_dead_letter_evidence`, `HotelRevenueManagementWorkbench`, `HotelRevenueManagementExceptionOpened`
**Exact key:** `hotel_revenue_management.channel_inventory_retry_dead_letter_cockpit`

### 31. Revenue manager workbench

**Justification:** The primary revenue manager needs one place to review pace, rates, restrictions, inventory, and exceptions by date and room type.
**Improvement:** Shape `HotelRevenueManagementWorkbench` around a revenue-manager persona with a demand calendar, restriction board, pickup chart, decision queue, and pending approvals.
**Acceptance evidence:** The route loads persona-specific panels, each panel links to the corresponding detail view, and UI tests cover empty, stale-data, and high-compression states.
**Current Domain Evidence Used:** `HotelRevenueManagementWorkbench`, `HotelRevenueManagementDetail`, `hotel_revenue_management_workbench_metric`, `GET /hotel-revenue-management-workbench`
**Exact key:** `hotel_revenue_management.revenue_manager_workbench`

### 32. Distribution analyst workbench

**Justification:** Channel specialists need a purpose-built view of allotments, stop-sells, parity breaks, and publish failures rather than the full revenue console.
**Improvement:** Add a distribution analyst workspace with a channel inventory grid, parity monitor, publish health view, and channel-specific action history.
**Acceptance evidence:** The workspace filters by channel and stay date, publish failures deep-link into retry tools, and permission tests ensure channel analysts cannot approve pricing changes outside their remit.
**Current Domain Evidence Used:** `channel_inventory`, `HotelRevenueManagementWorkbench`, `permissions`, `HotelRevenueManagementExceptionOpened`
**Exact key:** `hotel_revenue_management.distribution_analyst_workbench`

### 33. Group and events workbench

**Justification:** Group demand, displacement, and event-driven compression need a shared operating surface for commercial and revenue teams.
**Improvement:** Add a group-and-events workbench focused on block pickup, wash, displacement value, shoulder-night exposure, and event-tagged dates.
**Acceptance evidence:** Users can compare group posture against transient demand, open displacement analyses from the same page, and tests confirm event tags and group metrics stay synchronized across date edits.
**Current Domain Evidence Used:** `demand_forecast`, `yield_decision`, `HotelRevenueManagementWorkbench`, `hotel_revenue_management_counterfactual_scenario_simulation`
**Exact key:** `hotel_revenue_management.group_events_workbench`

### 34. Agent skill for rate-plan drafting

**Justification:** Revenue teams often start from plain-language instructions, and the assistant should convert those into governed drafts rather than chat-only responses.
**Improvement:** Add an agent skill that drafts `rate_plan` changes from instructions, proposes fences and restrictions, and stops at a preview stage until a human confirms.
**Acceptance evidence:** The assistant panel shows extracted assumptions and a structured diff, blocked actions surface permission reasons, and tests verify the skill cannot publish or approve its own changes.
**Current Domain Evidence Used:** `ai_agent_task_assistance`, `agentic_document_instruction_intake`, `rate_plan`, `HotelRevenueManagementAssistantPanel`
**Exact key:** `hotel_revenue_management.agent_skill_rate_plan_drafting`

### 35. Agent skill for pickup anomaly triage

**Justification:** Pickup anomalies are time-sensitive, and the assistant should help analysts determine whether the cause is demand, pricing, or distribution failure.
**Improvement:** Add an agent skill that summarizes pickup variance, checks recent rate and inventory changes, and proposes next investigations or corrective actions without mutating data until confirmed.
**Acceptance evidence:** The assistant cites source records for its summary, accepted actions route through governed commands, and tests verify the skill can explain an anomaly but cannot bypass operator approval.
**Current Domain Evidence Used:** `demand_forecast`, `revenue_snapshot`, `HotelRevenueManagementAssistantPanel`, `hotel_revenue_management_autonomous_anomaly_detection`
**Exact key:** `hotel_revenue_management.agent_skill_pickup_anomaly_triage`

### 36. Agent skill for overbooking explanation and guest recovery

**Justification:** When oversell risk rises, operators need the assistant to explain exposure and recovery options quickly.
**Improvement:** Add an agent skill that explains the active `overbooking_policy`, cites no-show assumptions and substitute room paths, and drafts guest-recovery playbooks for review.
**Acceptance evidence:** Recovery drafts cite the active policy and substitution rules, assistant actions remain preview-only until approved, and tests confirm the skill references the correct stay dates and room types.
**Current Domain Evidence Used:** `overbooking_policy`, `room_type`, `HotelRevenueManagementAssistantPanel`, `hotel_revenue_management_governed_ai_agent_execution`
**Exact key:** `hotel_revenue_management.agent_skill_overbooking_recovery_planning`

### 37. Outbound event boundary map for hotel revenue changes

**Justification:** Downstream consumers need precise business events instead of generic lifecycle noise when pricing or inventory behavior changes.
**Improvement:** Define typed outbound event boundaries for pricing approved, restriction changed, inventory stop-sell, forecast overridden, overbooking policy changed, and yield decision accepted.
**Acceptance evidence:** Event schemas are documented with examples, the outbox emits the typed events alongside existing lifecycle events when needed, and contract tests prove payload stability and idempotent publication.
**Current Domain Evidence Used:** `HotelRevenueManagementCreated`, `HotelRevenueManagementUpdated`, `HotelRevenueManagementApproved`, `appgen_x_outbox_inbox_eventing`
**Exact key:** `hotel_revenue_management.outbound_event_boundary_map`

### 38. Inbound handler contracts for policy and KPI events

**Justification:** The package already consumes governance and KPI events, and those handlers need explicit hotel-specific side effects and failure modes.
**Improvement:** Map `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` into clear update contracts for rule refresh, proof sealing status, forecast risk recalculation, and stale-dashboard warnings.
**Acceptance evidence:** Handler tests cover duplicate delivery, out-of-order delivery, and missing dependency cases, and failure evidence is visible from the workbench rather than buried in logs.
**Current Domain Evidence Used:** `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`, `idempotent_handlers`
**Exact key:** `hotel_revenue_management.inbound_event_handler_contracts`

### 39. Continuous pricing governance assertions

**Justification:** Pricing errors should be caught continuously, not only during release review or after a market issue surfaces.
**Improvement:** Add `hotel_revenue_management_control_assertion` checks for negative price deltas beyond policy, contradictory fences, blackout leakage, missing approvals, and stale overrides on active dates.
**Acceptance evidence:** Failed assertions open visible exceptions, each assertion references the violated rule and affected date range, and tests verify corrections clear the assertion once the issue is fixed.
**Current Domain Evidence Used:** `hotel_revenue_management_control_assertion`, `hotel_revenue_management_policy_rule`, `HotelRevenueManagementExceptionOpened`, `continuous_release_assurance`
**Exact key:** `hotel_revenue_management.continuous_pricing_governance_assertions`

### 40. Runtime parameter sets by season and market

**Justification:** One global threshold rarely fits a city-center compression hotel and a resort shoulder season at the same time.
**Improvement:** Organize `hotel_revenue_management_runtime_parameter` records into named seasonal and market-specific packs for pickup alerts, oversell caps, override thresholds, and pricing experiment limits.
**Acceptance evidence:** Parameter packs can be previewed before activation, changes are time-bounded and auditable, and tests confirm the correct pack activates for the targeted market and date window.
**Current Domain Evidence Used:** `hotel_revenue_management_runtime_parameter`, `configuration_workbench`, `HOTEL_REVENUE_MANAGEMENT_DEFAULT_POLICY`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.season_market_parameter_sets`

### 41. Multi-tenant isolation for brand, property, and market policy

**Justification:** Shared-brand platforms need revenue rules isolated by tenant, property, and market so one hotel's experiments or blackouts cannot bleed into another's operations.
**Improvement:** Apply tenant-aware boundaries across forecasts, rates, controls, workbench filters, and assistant context, with explicit property and market scoping on governed changes.
**Acceptance evidence:** Isolation tests prove one tenant cannot read or mutate another tenant's revenue records, assistant prompts are scoped to the active tenant, and approval history shows tenant and property context on every governed change.
**Current Domain Evidence Used:** `hotel_revenue_management_multi_tenant_policy_isolation`, `permissions`, `hotel_revenue_management_governed_model`, `HotelRevenueManagementDetail`
**Exact key:** `hotel_revenue_management.multi_tenant_brand_property_market_isolation`

### 42. Schema extension registry for new restriction types

**Justification:** Hotels frequently introduce new restriction logic, and custom fields should evolve without silently breaking decisions or UI flows.
**Improvement:** Add a schema-extension registry so new restriction types, blackout qualifiers, and occupancy qualifiers are declared with compatibility rules, migration notes, and projection impact.
**Acceptance evidence:** Extension proposals require validation before activation, backfill previews show affected data and views, and tests verify unknown restriction types never slip into live decisions without registration.
**Current Domain Evidence Used:** `hotel_revenue_management_schema_extension`, `hotel_revenue_management_schema_evolution_resilience`, `HotelRevenueManagementDetail`, `SPECIFICATION.md`
**Exact key:** `hotel_revenue_management.restriction_schema_extension_registry`

### 43. Governed model registry for forecast and optimization models

**Justification:** Forecasts and optimization recommendations need an owned catalog of model purpose, training window, approval status, and rollback history.
**Improvement:** Extend `hotel_revenue_management_governed_model` to track forecast, pricing, and overbooking models with business purpose, feature inputs, approval state, and retirement policy.
**Acceptance evidence:** Model detail pages show active-versus-retired status, decisions cite the model version used, and tests prove that retired models cannot be selected for new recommendations.
**Current Domain Evidence Used:** `hotel_revenue_management_governed_model`, `hotel_revenue_management_predictive_risk_scoring`, `yield_decision`, `HotelRevenueManagementApproved`
**Exact key:** `hotel_revenue_management.governed_model_registry`

### 44. Audit-proof sealing for pricing approvals and overrides

**Justification:** Pricing changes on critical dates need tamper-evident proof, not just mutable row history.
**Improvement:** Seal approvals, overrides, and publish artifacts with cryptographic proofs and retain verifiable links between the decision record and the released rate or restriction state.
**Acceptance evidence:** Approval records expose proof status, proof verification can be rerun after `AuditEventSealed`, and release evidence links each critical pricing decision to a sealed artifact.
**Current Domain Evidence Used:** `hotel_revenue_management_cryptographic_audit_proofs`, `AuditEventSealed`, `HotelRevenueManagementApproved`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.audit_proof_sealed_pricing_approvals`

### 45. API surface expansion for forecast queries and simulations

**Justification:** The current API surface is command-heavy and does not yet expose the read and simulation endpoints analysts need every day.
**Improvement:** Add read, validation-only, and simulation endpoints for forecast review, pickup diagnostics, readiness checks, and what-if pricing runs while keeping ownership inside this PBC boundary.
**Acceptance evidence:** Route contracts document request and response shapes, compatibility tests cover versioned endpoints, and the workbench consumes the new APIs without bypassing the governed command flow.
**Current Domain Evidence Used:** `POST /rate-plans`, `POST /channel-inventorys`, `POST /demand-forecasts`, `GET /hotel-revenue-management-workbench`
**Exact key:** `hotel_revenue_management.forecast_and_simulation_api_surface`

### 46. Release evidence pack for pricing and inventory changes

**Justification:** Revenue teams need release proof that a pricing or inventory change passed validation, approval, and downstream publish checks before go-live.
**Improvement:** Build a release-evidence pack that bundles readiness results, approval references, event publication checks, and workbench screenshots for each production change set.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` references the exact rate, restriction, and inventory artifacts included in a release, and tests confirm the pack is incomplete until all required evidence is attached.
**Current Domain Evidence Used:** `RELEASE_EVIDENCE.md`, `continuous_release_assurance`, `HotelRevenueManagementApproved`, `HotelRevenueManagementWorkbench`
**Exact key:** `hotel_revenue_management.release_evidence_pack`

### 47. Recovery drill for forecast failure on peak dates

**Justification:** Peak-date failures are expensive, so the package should prove it can recover from a broken forecast or stale signal under stress.
**Improvement:** Add a tabletop and replay drill for peak dates that simulates stale forecasts, missing KPI events, manual overrides, and operator fallback actions.
**Acceptance evidence:** The drill produces a reproducible checklist, event replay output, and recovery timing evidence, and release documentation shows the latest successful recovery run.
**Current Domain Evidence Used:** `demand_forecast`, `OperationalKpiChanged`, `hotel_revenue_management_event_sourced_operational_history`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.peak_date_forecast_recovery_drill`

### 48. Cross-PBC boundary rules for downstream consumers

**Justification:** Pricing and inventory data are heavily reused across adjacent domains, so this PBC needs explicit rules for what leaves by API or event and what stays internal.
**Improvement:** Document and enforce boundary rules that expose hotel revenue outputs through owned APIs and events only, never through shared-table reads or hidden joins.
**Acceptance evidence:** Boundary tests fail on direct foreign-table coupling, outbound contracts identify the supported consumer-facing fields, and the specification records which records are internal-only.
**Current Domain Evidence Used:** `appgen_x_outbox_inbox_eventing`, `hotel_revenue_management_cross_pbc_event_federation`, `SPECIFICATION.md`, `HotelRevenueManagementUpdated`
**Exact key:** `hotel_revenue_management.cross_pbc_boundary_rules`

### 49. KPI definition library for occupancy, ADR, RevPAR, and pickup

**Justification:** Operators cannot trust alerts or dashboards if KPI formulas drift between analytics, workbench views, and release evidence.
**Improvement:** Create a governed KPI library that defines occupancy, ADR, RevPAR, pickup, net room revenue, and channel-mix formulas with source fields and rounding rules.
**Acceptance evidence:** KPI definitions are referenced by snapshots, dashboards, and release evidence, and tests verify that formula changes require explicit approval and recalculate affected derived metrics consistently.
**Current Domain Evidence Used:** `revenue_snapshot`, `hotel_revenue_management_workbench_metric`, `hotel_revenue_management_analytics`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.kpi_definition_library`

### 50. Go-live scorecard and release signoff drill

**Justification:** Revenue changes should close with a single operational scorecard that proves pricing logic, controls, APIs, events, workbench views, and assistant safeguards all held together.
**Improvement:** Add a go-live drill that exercises one representative rate change from draft through approval, event publication, workbench visibility, and release evidence signoff.
**Acceptance evidence:** The scorecard records pass or fail for validation, approval, event delivery, UI visibility, agent guardrails, and evidence completeness, and the latest successful run is referenced from the release evidence file.
**Current Domain Evidence Used:** `rate_plan`, `HotelRevenueManagementWorkbench`, `HotelRevenueManagementAssistantPanel`, `RELEASE_EVIDENCE.md`
**Exact key:** `hotel_revenue_management.go_live_scorecard_release_signoff`
