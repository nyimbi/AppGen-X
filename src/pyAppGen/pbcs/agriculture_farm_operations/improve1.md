# Agriculture Farm Operations Improvement Backlog

This backlog is hand-curated for `agriculture_farm_operations` and focuses on real farm-operations depth across fields, plots, crop plans, planting windows, inputs, irrigation, scouting, pest and disease pressure, soil, weather, harvest, equipment, labor, yield, compliance, sustainability, workbenches, agent skills, event boundaries, API boundaries, and release evidence.

## Current Domain Evidence Used

- PBC key in the manifest: `agriculture_farm_operations`.
- Domain description in the manifest: fields, crops, inputs, equipment, irrigation, harvest, yield, certifications, and farm compliance.
- Owned operational tables in the manifest: `field`, `crop_plan`, `input_application`, `irrigation_event`, `equipment_use`, `harvest_lot`, `yield_observation`.
- Public APIs in the manifest: `POST /fields`, `POST /crop-plans`, `POST /input-applications`, `POST /irrigation-events`, `POST /equipment-uses`, `GET /agriculture-farm-operations-workbench`.
- UI fragments in the manifest: `AgricultureFarmOperationsWorkbench`, `AgricultureFarmOperationsDetail`, `AgricultureFarmOperationsAssistantPanel`.
- Workflows in the manifest: `agriculture_farm_operations_create_field_workflow`, `agriculture_farm_operations_record_crop_plan_workflow`.
- Emitted events in the manifest: `AgricultureFarmOperationsCreated`, `AgricultureFarmOperationsUpdated`, `AgricultureFarmOperationsApproved`, `AgricultureFarmOperationsExceptionOpened`.
- Consumed events in the manifest: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Advanced capabilities already declared: event-sourced history, anomaly detection, predictive risk scoring, counterfactual simulation, semantic document understanding, governed AI agent execution, carbon and sustainability awareness, and cryptographic audit proofs.
- Release-document surfaces already named: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Field-to-plot geometry hierarchy
**Justification:** Farm work is executed at plot, block, bed, and management-zone level, not only at the whole-field level. Without sub-field structure, recommendations and evidence stay too coarse for agronomy and compliance.
**Improvement:** Extend `field` handling to support parent field, plot, block, row-set, and management-zone geometry with acreage rollups, boundary versioning, and overlap detection.
**Acceptance evidence:** Boundary import tests, acreage reconciliation by level, and a workbench map that can switch between field, plot, and management-zone views.

### 2. Season-aware crop plans
**Justification:** The same acreage may carry spring, relay, double-crop, or replant plans in one year. A single flat `crop_plan` record cannot express that reality safely.
**Improvement:** Add season, market year, intended crop, fallback crop, previous crop, and replant linkage to `crop_plan`, with date-based conflict checks on shared acreage.
**Acceptance evidence:** Fixtures for double-crop and replant cases, validation that blocks overlapping active plans, and a season timeline in the workbench.

### 3. Planting-window intelligence
**Justification:** Planting too early or too late drives yield loss, pest pressure, irrigation demand, and harvest risk. The package should understand planting windows as decision logic, not passive dates.
**Improvement:** Add planting-window rules by crop, variety, region, soil temperature, frost risk, rainfall outlook, and irrigation readiness, with statuses for early, optimal, late, and missed windows.
**Acceptance evidence:** Rule tests at window edges, missed-window alerts, and scenario output that shows schedule and yield impact when planting slips.

### 4. Variety and seed-lot traceability
**Justification:** Variety choice changes maturity, disease resistance, stand risk, and harvest behavior. Farm operators need to trace outcomes back to the exact seed or transplant lot.
**Improvement:** Capture variety, hybrid or cultivar, seed lot, treatment status, germination, target population, and planting density on `crop_plan` and planting execution records.
**Acceptance evidence:** Variety-level reporting, seed-lot lineage from planning through harvest, and depletion checks that prevent over-allocating the same lot.

### 5. Pre-plant readiness gate
**Justification:** Planting should be blocked when tillage, drainage, soil condition, fertility prerequisites, or equipment readiness are incomplete. Otherwise downstream problems are created on day one.
**Improvement:** Add a pre-plant checklist on `field` and `crop_plan` that evaluates soil fit, residue condition, fertility preconditions, planter availability, and crew assignment before release.
**Acceptance evidence:** Blocked planting scenarios opening exceptions, visible readiness blockers in the workbench, and supervisor override evidence with reason capture.

### 6. Soil sampling zones
**Justification:** Soil chemistry and texture vary inside the same field. Treating soil as uniform weakens fertility decisions and hides persistent underperforming areas.
**Improvement:** Add zone-based soil samples linked to `field` geometry with sample date, depth, lab, pH, organic matter, macro and micro nutrients, salinity, and compaction observations.
**Acceptance evidence:** Zone-level lab import tests, soil trend views in `AgricultureFarmOperationsDetail`, and validation that prescriptions point to the latest approved sample set.

### 7. Nutrient budget accounting
**Justification:** Fertility planning should balance crop demand, soil supply, prior applications, irrigation contribution, and expected removal at harvest. Without a budget, application history is just a log.
**Improvement:** Create nutrient budgets that connect `crop_plan`, soil samples, target yield, past `input_application` events, and expected harvest removal, then compare plan to actual.
**Acceptance evidence:** Budget reports by field and zone, over- and under-application exceptions, and season-end nutrient balance evidence.

### 8. Agronomy prescription versioning
**Justification:** Recommendations change as weather, scouting, and crop condition change. Operators need to know which prescription was active when a job was released and why it changed later.
**Improvement:** Add versioned prescriptions for seeding, fertility, irrigation, crop protection, and harvest timing, each with effective dates, author, supersession reason, and impacted plots.
**Acceptance evidence:** Prescription diff views, approval history, and event history showing which version drove each executed task.

### 9. Growth-stage-aware irrigation scheduling
**Justification:** Water demand at emergence is not the same as water demand at flowering or grain fill. Recording irrigation without crop stage misses the core agronomic context.
**Improvement:** Extend `irrigation_event` planning with crop stage, root-depth assumptions, allowable depletion, target refill point, and stage-specific stress sensitivity.
**Acceptance evidence:** Schedule recommendations that change by growth stage, alerts for stress during critical reproductive periods, and tests covering early- versus late-season irrigation logic.

### 10. Water-source capacity constraints
**Justification:** A good irrigation recommendation can still be impossible if pump hours, well output, canal turns, or reservoir volume are constrained. Farm operations need feasibility, not only agronomic desire.
**Improvement:** Add water-source profiles with source type, permitted volume, flow rate, pump hours, energy need, and shared-system conflicts across fields.
**Acceptance evidence:** Constraint-aware irrigation plans, warnings when pump time is over-allocated, and simulation output for reduced water availability.

### 11. Rainfall and irrigation reconciliation
**Justification:** Applied-water totals are misleading when rainfall and irrigation are tracked separately. Soil-water decisions need a combined balance rather than isolated events.
**Improvement:** Reconcile `irrigation_event` records with measured rainfall, runoff assumptions, and effective infiltration to maintain a net plant-available water balance by zone.
**Acceptance evidence:** Water-balance dashboards, discrepancy flags between planned and effective water, and evidence traces for each daily balance calculation.

### 12. Chemigation and fertigation linkage
**Justification:** Inputs applied through irrigation have different operational and compliance risks from dry or foliar applications. Those linked events must be explicit, not implied in notes.
**Improvement:** Let `input_application` and `irrigation_event` link through chemigation or fertigation sessions with injection rate, carrier water, flush duration, and line-cleanout confirmation.
**Acceptance evidence:** Linked-event audit trails, controls that block incomplete sessions from closing, and evidence of required flush and interval checks.

### 13. Scouting round workbench
**Justification:** Scouting drives decisions on pests, disease, weeds, fertility symptoms, and harvest timing, yet it is often fragmented across notebooks and messages. The PBC should make scouting operationally first-class.
**Improvement:** Add a scouting workbench that organizes rounds by field, route, date, scout, crop stage, and issue class, with geotagged observations, photos, severity scoring, and follow-up tasks.
**Acceptance evidence:** Scouting queues in `AgricultureFarmOperationsWorkbench`, photo-backed observations attached to plots or zones, and clear links from observation to action.

### 14. Pest, disease, and weed taxonomy
**Justification:** Free-text issue names make analytics, thresholds, and treatment logic unreliable. Farm teams need a structured taxonomy for organisms, life stages, and pressure levels.
**Improvement:** Create a managed taxonomy for insect pests, diseases, weeds, beneficials, life stage, pressure rating, affected crop stage, and recommended action window.
**Acceptance evidence:** Taxonomy-backed scouting entries, duplicate-name prevention, threshold rule tests, and clean reports grouped by organism and severity.

### 15. Threshold-based treatment recommendations
**Justification:** Good crop-protection decisions depend on action thresholds, crop stage, beneficial populations, and weather. The package should help prevent unnecessary or mistimed sprays.
**Improvement:** Add threshold evaluation that converts scouting observations into treat, monitor, or no-action outcomes, then links approved treatment to `input_application` planning.
**Acceptance evidence:** Threshold simulations, audit evidence showing why treatment was or was not recommended, and blocked workflows when no threshold-based justification exists.

### 16. Restricted-entry and pre-harvest interval tracking
**Justification:** After some applications, labor access and harvest timing are legally or operationally restricted. Missing those intervals creates direct safety and compliance risk.
**Improvement:** Track restricted-entry interval and pre-harvest interval per relevant `input_application`, then project those windows onto crew assignment, scouting access, and harvest release.
**Acceptance evidence:** Calendar overlays of blocked windows, prevented harvest release before interval expiry, and compliance-ready evidence tied to the affected operation.

### 17. Equipment calibration evidence
**Justification:** Application quality depends on calibrated planters, sprayers, spreaders, and irrigation systems. A recorded job without calibration evidence is weak operational proof.
**Improvement:** Add calibration records to `equipment_use` with target rate, measured rate, nozzle or meter setup, swath width, speed assumptions, and calibration expiry.
**Acceptance evidence:** Blocks when calibration is expired, job-level linkage to the latest valid calibration, and release evidence showing which calibration supported each sensitive job.

### 18. Crew skill and certification matching
**Justification:** Not every worker can safely or legally perform chemical handling, irrigation controls, or harvest machine work. Farm operations need skill-aware assignments.
**Improvement:** Add labor qualification checks for `equipment_use`, `input_application`, scouting, and harvest tasks, including certifications, training expiry, and supervisor requirements.
**Acceptance evidence:** Assignment rejection tests for unqualified operators, crew rosters filtered by required skill, and audited supervisor-authorized exceptions.

### 19. Work-order sequencing across field operations
**Justification:** Many agronomic failures come from bad task order, such as irrigation before dry-down or harvest before moisture target. Sequencing belongs in the domain model.
**Improvement:** Build work-order dependencies across soil prep, planting, irrigation, scouting follow-up, crop protection, and harvest so downstream tasks wait for required predecessor conditions.
**Acceptance evidence:** Dependency graphs in the workbench, blocked-task exceptions naming the missing predecessor, and tests covering common sequencing conflicts.

### 20. Offline mobile field execution
**Justification:** Farm crews often work in weak-connectivity areas. They still need to record irrigation, scouting, applications, and harvest details without duplicate submission or data loss.
**Improvement:** Add offline-capable command capture with local draft state, idempotency keys, sync conflict handling, and required-photo rules for sensitive operations.
**Acceptance evidence:** Offline-to-online replay tests, duplicate sync prevention, and event lineage proving that delayed syncs do not create duplicate work.

### 21. Harvest readiness gate
**Justification:** Harvest timing depends on maturity, moisture, interval restrictions, weather, labor, and machine capacity. A farm package should know why a field is ready, delayed, or blocked.
**Improvement:** Add a harvest readiness model using crop maturity, moisture targets, field access, forecast risk, crew availability, and interval compliance.
**Acceptance evidence:** Ready versus blocked harvest status in the workbench, urgency flags before weather events, and documented reasons for approved overrides.

### 22. Harvest lot segmentation and lineage
**Justification:** Mixing product from different fields, varieties, or treatment histories can destroy traceability. `harvest_lot` should preserve the physical reality of harvest flow.
**Improvement:** Track `harvest_lot` origin by field, plot, variety, harvest date, machine pass, storage destination, and segregation rule so lots stay distinct when they should.
**Acceptance evidence:** Lot genealogy views, warnings before incompatible lots are merged, and export-ready lineage from field through storage handoff.

### 23. Crop-quality capture at harvest
**Justification:** Harvest success is not only weight or volume. Moisture, grade, defects, contamination, size, brix, or dry matter often drive the next operational decision.
**Improvement:** Extend `harvest_lot` capture with crop-appropriate quality factors and threshold logic that influences storage, drying, curing, and acceptance decisions.
**Acceptance evidence:** Quality forms tailored by crop type, quality trend views, and rules that block inappropriate storage or closeout when thresholds are missed.

### 24. Yield monitor and map ingestion
**Justification:** Field-level yield totals hide within-field variability that should shape future prescriptions. `yield_observation` should accept yield maps, not only summary values.
**Improvement:** Add ingestion for yield monitor files and zone-level yield layers with lag correction, moisture normalization, swath cleanup, and calibration metadata.
**Acceptance evidence:** Successful import of multi-pass yield files, cleaned-map previews, and zone-level yield summaries tied back to accepted harvest totals.

### 25. Yield reconciliation across sources
**Justification:** Yield numbers from monitors, truck scales, storage receipts, and manual counts rarely match exactly. The package should explain variance instead of leaving competing numbers unresolved.
**Improvement:** Reconcile `yield_observation` with `harvest_lot`, delivered weight, storage receipts, and moisture adjustments, then classify final source of truth and variance reason.
**Acceptance evidence:** Variance dashboards, mandatory investigation for large mismatches, and stored explanations for the accepted final yield figure.

### 26. Replant and stand-failure workflow
**Justification:** Emergence failure, washouts, hail, or pest damage can force replant decisions that change seed demand, timing, and expected harvest windows. That path should be explicit.
**Improvement:** Add a replant workflow that can retire part of a `crop_plan`, create a successor plan for affected acreage, preserve cause evidence, and re-sequence downstream tasks.
**Acceptance evidence:** Partial-field replant fixtures, acreage reconciliation before and after replant, and event history connecting stand failure to the revised plan.

### 27. Post-harvest drying, curing, and storage conditions
**Justification:** Harvest is not the end of farm operations. Crop condition can improve or deteriorate rapidly based on drying, curing, aeration, and storage management.
**Improvement:** Extend `harvest_lot` handling with drying targets, curing windows, aeration events, temperature, humidity, storage moves, and spoilage-risk indicators.
**Acceptance evidence:** Storage-condition trend views, blocked closeout when drying targets are unmet, and alerts for hot spots or unsafe storage duration.

### 28. Residue, tillage, and cover-crop continuity
**Justification:** Soil protection and next-season readiness depend on what happens after harvest. A good farm-operations package should carry those actions into future planning.
**Improvement:** Capture residue management, tillage passes, cover-crop establishment, and termination timing as linked field operations that feed the next `crop_plan`.
**Acceptance evidence:** Season-to-season continuity views, exceptions for missing required residue or cover actions, and evidence of soil-cover targets by field.

### 29. Conservation and stewardship practice tracking
**Justification:** Buffer strips, contouring, nutrient placement, water-saving practices, and reduced tillage matter operationally and often underpin incentive or compliance programs.
**Improvement:** Add stewardship practice records tied to `field`, `crop_plan`, and executed operations so farms can prove where and when specific practices were followed or missed.
**Acceptance evidence:** Practice maps, seasonal summaries by practice type, and export-ready evidence showing stewardship performance at field and farm level.

### 30. Sustainability KPI ledger
**Justification:** The manifest already claims carbon and sustainability awareness. Farm operators need concrete measures such as water-use efficiency, nitrogen-use efficiency, fuel intensity, and pass count.
**Improvement:** Derive sustainability measures from `input_application`, `irrigation_event`, `equipment_use`, `harvest_lot`, and `yield_observation` with farm, field, and zone rollups.
**Acceptance evidence:** KPI definitions, reproducible calculations, trend charts in the workbench, and release evidence showing how each measure was computed.

### 31. Agronomy prescription review workbench
**Justification:** Recommendations are only useful if agronomists and operations managers can review, challenge, approve, and operationalize them in one place. The current generic workbench surface is too shallow for that.
**Improvement:** Add a dedicated workbench slice for agronomy prescriptions with pending-review queues, map overlays, diffs, impacted fields, and convert-to-work-order actions.
**Acceptance evidence:** Route coverage from `GET /agriculture-farm-operations-workbench`, review-to-approval flows, and permission-aware actions in `AgricultureFarmOperationsWorkbench`.

### 32. Field-season timeline workbench
**Justification:** Farm managers think in timelines: prep, planting, emergence, scouting, spraying, irrigation peaks, harvest, and closeout. Fragmented record lists do not support that operational view.
**Improvement:** Build a field-season timeline that pulls together `crop_plan`, `input_application`, `irrigation_event`, `equipment_use`, scouting milestones, harvest readiness, and harvest execution.
**Acceptance evidence:** Timeline drill-down from field to plot, delay markers, and validation that major season events appear in chronological order.

### 33. Missed-window and blocked-operations inbox
**Justification:** Many farm losses come from late actions, blocked fields, or unresolved prerequisites. Operators need one place to see what must move now.
**Improvement:** Create an exception inbox for missed planting windows, overdue irrigation, untreated threshold breaches, expired calibration, blocked harvest, and unresolved compliance holds.
**Acceptance evidence:** Priority-ranked queues, aging metrics, owner assignment, and emitted `AgricultureFarmOperationsExceptionOpened` events with farm-specific reason codes.

### 34. Agronomist copilot skill
**Justification:** The assistant panel should behave like an agronomy-aware copilot, not a generic chatbot. Farm operators need grounded help tied to field history and evidence.
**Improvement:** Add an agent skill that can summarize field history, compare prescriptions, highlight scout-driven treatment needs, explain yield variability, and draft safe next-step recommendations for human review.
**Acceptance evidence:** Prompt-to-draft traces with source citations, blocked mutation attempts when evidence is insufficient, and explanation cards inside `AgricultureFarmOperationsAssistantPanel`.

### 35. Compliance packet assembly skill
**Justification:** Farm audits often require application records, intervals, operator qualifications, lot lineage, and stewardship evidence on short notice. Manual packet assembly is slow and error-prone.
**Improvement:** Add an agent skill that prepares audit-ready packets for a field, season, lot, or certification scope using governed data and explicit evidence selection.
**Acceptance evidence:** Packet previews with included records, missing-evidence warnings, and generated exports that match underlying field operations without silent gaps.

### 36. Document-to-draft agronomy intake
**Justification:** Recommendations arrive as PDFs, lab reports, emails, and scout notes. Semantic document understanding should turn those materials into reviewable farm-operation drafts.
**Improvement:** Extract lab values, recommendation rates, field identifiers, product names, weather notes, and restriction windows into draft `crop_plan`, `input_application`, or scouting records.
**Acceptance evidence:** Extraction accuracy fixtures, source-span review in the UI, and mandatory human confirmation before any document-derived draft becomes an operational command.

### 37. API boundary for plan versus execution
**Justification:** Farm systems often blur recommendations with actual work. Clear API boundaries help downstream consumers know whether they are reading intent, release, or execution evidence.
**Improvement:** Separate planning, approval, execution, correction, and validation-only paths around `POST /crop-plans`, `POST /input-applications`, `POST /irrigation-events`, and `POST /equipment-uses`.
**Acceptance evidence:** API contract tests, status-specific examples, and proof that execution-only records cannot be created through planning-only paths.

### 38. Field-operation event expansion
**Justification:** Generic lifecycle events do not carry enough farm context for downstream analytics or integrations. Consumers need to know whether a field was planted, irrigated, treated, or harvested.
**Improvement:** Expand emitted events with field-operation-specific events for planting released, irrigation delayed, scout threshold exceeded, treatment applied, harvest opened, lot closed, and yield reconciled.
**Acceptance evidence:** Event schema examples, idempotent publish tests, and lineage from domain record to emitted event in release evidence.

### 39. Idempotent telemetry ingestion
**Justification:** Weather stations, irrigation controllers, telematics, and yield monitors can send noisy or repeated data. Farm operations need durable ingestion without duplicate operational consequences.
**Improvement:** Add idempotent handling for external telemetry that updates projections, flags anomalies, and opens exceptions without creating duplicate `irrigation_event`, `equipment_use`, or `yield_observation` records.
**Acceptance evidence:** Duplicate-message tests, stale-feed alerts, and dead-letter evidence for malformed machine payloads.

### 40. Scenario simulation for weather and capacity shocks
**Justification:** Counterfactual simulation is only useful if it answers farm questions like late rain, sprayer failure, labor shortage, or compressed harvest windows. Generic scenarios are not enough.
**Improvement:** Add simulations for delayed planting, excessive rainfall, drought stress, irrigation outage, sprayer downtime, labor shortfall, and harvest compression.
**Acceptance evidence:** Side-by-side scenario results in the workbench, calculated effect on schedule and expected yield, and non-mutating logs tied to the requesting user.

### 41. Predictive risk scoring for agronomic loss points
**Justification:** Risk scoring should surface the fields most likely to miss yield targets, violate intervals, or suffer operational loss. Farm teams need ranked attention, not abstract package scores.
**Improvement:** Build risk models for stand failure, irrigation stress, disease escalation, harvest delay, and traceability breaks using field history, weather, scouting, input timing, and equipment constraints.
**Acceptance evidence:** Risk cards with top contributing factors, calibration checks against actual season outcomes, and manager queues sorted by predicted operational risk.

### 42. Multi-tenant regional agronomy configuration
**Justification:** Farm operations differ by crop, climate, and production region. Tenant isolation alone is not enough; the PBC must also support region-specific calendars and thresholds cleanly.
**Improvement:** Add tenant-scoped regional configuration for crop calendars, growing-degree rules, pest thresholds, water assumptions, interval defaults, and reporting periods.
**Acceptance evidence:** Tenant-isolation tests, region override history, and field behavior that changes correctly when the same crop is configured in different regions.

### 43. Controlled boundary for external inventory and procurement
**Justification:** Farms need supply awareness for inputs, but `agriculture_farm_operations` should not silently absorb stock ownership that belongs elsewhere. The boundary should stay explicit.
**Improvement:** Keep product stock and purchase authority outside the PBC while exposing clear consumption and availability contracts so `input_application` planning can validate likely supply.
**Acceptance evidence:** Contract docs, no foreign-table coupling in the PBC, and tests showing how missing supply information blocks or warns on planned applications.

### 44. Soil health trend baseline
**Justification:** Soil health changes over multiple seasons and should not be reduced to one-year yield outcomes. Farm improvement work needs long-horizon ground truth.
**Improvement:** Add multi-year soil health tracking for organic matter, infiltration, aggregate stability, pH trend, compaction, and biological indicators linked to field management history.
**Acceptance evidence:** Multi-season trend charts, alerts for degrading indicators, and evidence linking management changes such as cover crops or reduced tillage to soil response.

### 45. Cost-per-acre and cost-per-operation visibility
**Justification:** Managers need to know not only what happened, but what it cost by field, crop, and pass. Labor, fuel, water, and input use should be attributable at farm-operations granularity.
**Improvement:** Derive cost views from `input_application`, `irrigation_event`, `equipment_use`, and labor assignments so users can compare planned versus actual cost per acre, pass, or harvest lot.
**Acceptance evidence:** Cost summaries with drill-through to source operations, variance flags when actual cost departs materially from plan, and season exports grouped by field and crop.

### 46. Harvest capacity planner
**Justification:** Farms often know what is ready to harvest before they know what they can actually cut, move, dry, and store. Capacity bottlenecks should be explicit before quality or weather loss happens.
**Improvement:** Add a capacity planner that combines harvest readiness, machine hours, truck turns, dryer throughput, crew availability, and storage space into a feasible cut schedule.
**Acceptance evidence:** Capacity-versus-demand views, what-if simulations for a lost machine or extra crew, and alerts when ready acres exceed daily harvest capacity.

### 47. Certification and audit readiness ledger
**Justification:** Certifications and customer programs require repeatable proof, not hurried evidence gathering. Farm compliance should be assembled continuously as work happens.
**Improvement:** Create a compliance ledger that assembles operator qualifications, application records, interval evidence, stewardship practices, lot lineage, and corrective actions by season and program.
**Acceptance evidence:** Audit-ready reports by certification scope, missing-evidence exceptions before audit day, and sign-off history for completed compliance packets.

### 48. Continuous control tests for regulated operations
**Justification:** Farm compliance breaks when controls are checked only at season end. High-risk operations need ongoing control assertions while the season is still recoverable.
**Improvement:** Add continuous control tests for restricted products, expired qualifications, missing calibration, interval violations, blocked water sources, and unapproved lot merges.
**Acceptance evidence:** Control dashboards, failing-control events, triage queues for broken controls, and proof that reopened violations stay visible until resolved.

### 49. Release evidence pack for farm-operation changes
**Justification:** The manifest already names `RELEASE_EVIDENCE.md`; farm-specific improvements should ship with evidence that proves field logic, event behavior, UI coverage, and compliance controls actually work.
**Improvement:** Standardize release evidence for agronomy rules, field workbenches, event contracts, API boundaries, simulation behavior, and compliance ledgers whenever `agriculture_farm_operations` changes.
**Acceptance evidence:** A release-evidence checklist tied to farm-operation scenarios, screenshots or artifacts for workbench and assistant surfaces, and traceable links from tests to shipped capabilities.

### 50. Season closeout and carry-forward workflow
**Justification:** The value of farm operations is not only what happened this season, but what the next season learns from it. Closeout should turn outcomes into better starting conditions for the next crop.
**Improvement:** Add a season closeout workflow that locks final yield and quality, records lessons learned, carries forward soil and stewardship context, and seeds the next `crop_plan` with validated starting assumptions.
**Acceptance evidence:** Closeout checklists, required final reconciliations before season archival, and carry-forward previews showing which field facts will initialize the next planning cycle.
