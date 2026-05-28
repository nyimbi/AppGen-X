# Renewables Asset Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key in code and contracts: `renewables_asset_operations`.
- Manifest description: solar and wind assets, generation, curtailment, maintenance, PPAs, availability, and renewable performance.
- Current owned tables include `renewable_asset`, `generation_reading`, `curtailment_event`, `availability_record`, `ppa_obligation`, `maintenance_work`, and `performance_ratio`.
- Current operations include `create_renewable_asset`, `record_generation_reading`, `review_curtailment_event`, `approve_availability_record`, `simulate_ppa_obligation`, `create_maintenance_work`, and `record_performance_ratio`.
- Current UI fragments are `RenewablesAssetOperationsWorkbench`, `RenewablesAssetOperationsDetail`, and `RenewablesAssetOperationsAssistantPanel`.
- Current emitted events are `RenewablesAssetOperationsCreated`, `RenewablesAssetOperationsUpdated`, `RenewablesAssetOperationsApproved`, and `RenewablesAssetOperationsExceptionOpened`; consumed events are `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current agent surface exposes guided read/create/update skills with mutation preview and human confirmation.
- Current release evidence contract expects package proof across schema, services, events, handlers, UI, agent, and governance.

### 1. Asset hierarchy and technology-specific master data
**Justification:** A renewables operations model is weak if `renewable_asset` stops at a flat asset record and cannot distinguish a site, substation, feeder, inverter block, turbine, battery rack, meter, or weather station.
**Improvement:** Expand the backlog around a canonical asset hierarchy with technology type, OEM, model, serial number, commissioning date, nameplate capacity, site ownership, grid node, and parent-child relationships so solar, wind, and storage equipment can be operated as a fleet rather than as undifferentiated rows.
**Acceptance evidence:** Schema design notes showing parent-child asset linkage, sample site trees for solar, wind, and storage, and workbench mock states that filter KPIs by site, block, turbine, or battery unit.

### 2. Site-level availability model
**Justification:** Availability disputes usually start with ambiguity about whether the denominator is plant-level, unit-level, contractual, technical, or grid-adjusted.
**Improvement:** Define separate availability views for technical availability, contractual availability, grid-adjusted availability, and energy-based availability, each with explicit inclusion and exclusion rules for outages, derates, curtailment, force majeure, and planned work.
**Acceptance evidence:** Example calculations for a solar site, a wind site, and a storage site; comparison tables that show why each denominator differs; and approval evidence for the chosen formulas.

### 3. SCADA telemetry boundary and source-of-truth policy
**Justification:** The package already handles `generation_reading`, but it does not yet make the boundary between field telemetry, historian corrections, and governed operational records explicit.
**Improvement:** Add a backlog item for a SCADA telemetry boundary policy that states which signals may be ingested directly, which must stay in upstream historians, what rollups belong in this PBC, and how late-arriving corrections or meter true-ups revise previously approved records.
**Acceptance evidence:** A written boundary matrix for SCADA, meters, weather feeds, and manual uploads; sample lineage from raw tag to governed reading; and replay scenarios for corrected telemetry.

### 4. Solar inverter block performance accounting
**Justification:** Solar underperformance is rarely actionable unless the system can isolate losses to inverter blocks, DC strings, clipping, soiling, temperature, and communications failure.
**Improvement:** Prioritize an improvement track for inverter-block analytics that compares expected AC output against irradiance-adjusted opportunity, flags clipping versus outage behavior, and links each loss bucket to work orders, cleaning plans, or engineering review.
**Acceptance evidence:** Example inverter-block scorecards, a loss waterfall for a poor-performing day, and traceable links from anomalies to maintenance or inspection actions.

### 5. Wind turbine performance loss classification
**Justification:** Wind performance issues look different from solar issues; yaw misalignment, curtailment, icing, high-wind cut-out, and blade condition need their own vocabulary and evidence model.
**Improvement:** Create a turbine-focused backlog stream with turbine availability states, performance-loss categories, fault code normalization, nacelle and gearbox inspection references, and wake-aware comparisons among neighboring turbines.
**Acceptance evidence:** Sample turbine fault mappings, a power-curve deviation report, and exception records that distinguish turbine fault loss from curtailment or low-resource loss.

### 6. Battery storage state-of-energy and cycling operations
**Justification:** Storage assets cannot be treated as a side note in a renewables package because state of charge, availability, degradation, and dispatch compliance affect both operations and settlement.
**Improvement:** Add explicit storage backlog items for state-of-energy snapshots, charge and discharge dispatch instructions, augmentation events, cycle counting, degradation thresholds, and inverter-versus-cell fault isolation.
**Acceptance evidence:** Example storage operating timeline, cycle-count evidence for warranty claims, and test scenarios covering dispatch non-compliance, cell faults, and augmentation changes.

### 7. Meter hierarchy and revenue-grade reconciliation
**Justification:** Operations teams need to reconcile SCADA estimates, inverter totals, turbine counters, and revenue-grade meters before curtailment, availability, and PPA numbers can be trusted.
**Improvement:** Add a reconciliation backlog that models check meters, plant meters, point-of-interconnect meters, and sub-meter rollups, with tolerances and approval steps for manual adjustments or settlement corrections.
**Acceptance evidence:** Reconciliation reports showing SCADA versus revenue meter differences, tolerance breach alerts, and audit trails for approved corrections.

### 8. Curtailment taxonomy
**Justification:** `curtailment_event` is only valuable if the cause codes separate grid instruction, market dispatch, transmission congestion, local protection trips, environmental constraints, and internal derates.
**Improvement:** Replace the generic curtailment queue with a taxonomy that records initiator, instruction source, start and end times, MW requested, MW delivered, recoverability, compensation status, and supporting instruction evidence.
**Acceptance evidence:** Standard cause-code list, sample curtailment event packs with attached dispatch evidence, and reports separating compensated from uncompensated curtailment.

### 9. Availability denominator and exclusion governance
**Justification:** Teams routinely re-open monthly availability packs because exclusions for force majeure, third-party outage, curtailment, and planned work were not governed consistently.
**Improvement:** Add a dedicated backlog item for exclusion governance with reason codes, attachment requirements, approver roles, re-open rules, and period lock controls once a monthly pack is signed off.
**Acceptance evidence:** Approval matrix for exclusions, locked-period behavior examples, and side-by-side monthly packs before and after an approved exclusion change.

### 10. PPA obligation calendar and settlement traceability
**Justification:** `ppa_obligation` should do more than store obligations; it should operationalize milestone dates, guaranteed availability thresholds, reporting deadlines, and settlement dependencies.
**Improvement:** Build a PPA obligation calendar view that tracks contract milestones, availability and energy guarantees, notice periods, LD trigger conditions, settlement evidence due dates, and required attachments for each contract year or month.
**Acceptance evidence:** Contract-to-calendar mapping examples, settlement checklist output for one reporting period, and exception records for missed or at-risk PPA milestones.

### 11. Warranty claim trigger tracking
**Justification:** Repeated inverter, turbine, transformer, or battery failures lose value if they are not assembled into warranty-ready evidence while the data is still fresh.
**Improvement:** Add a warranty backlog stream that tracks start dates, warranty terms, response obligations, fault recurrence counts, outage duration thresholds, OEM notification deadlines, and evidence bundles for claim preparation.
**Acceptance evidence:** Example warranty trigger dashboard, claim evidence checklist, and linked history showing repeated component failures crossing a claim threshold.

### 12. Work order planning by asset criticality
**Justification:** `maintenance_work` becomes administrative noise if the package cannot distinguish a cosmetic task from a task that threatens megawatt availability or safety.
**Improvement:** Add criticality scoring to work orders based on asset role, MW at risk, fault persistence, spares availability, weather window, and crew access constraints so the backlog reflects operational impact rather than first-come-first-served order.
**Acceptance evidence:** Priority scoring examples, planner queue states for high-risk and low-risk work, and evidence that high-impact work rises ahead of cosmetic tasks.

### 13. Site inspection program
**Justification:** Inspections are a core renewable operations activity and need first-class support rather than being hidden inside free-text notes.
**Improvement:** Create inspection templates for solar field walks, turbine base inspections, battery container inspections, substation rounds, and perimeter checks, with photo capture, defect classification, geo-stamps, and follow-on action creation.
**Acceptance evidence:** Template library examples, completed inspection packets with photos and defect tags, and linked follow-up actions or work orders created from findings.

### 14. Vegetation management program
**Justification:** Vegetation growth degrades solar production, increases fire risk, and affects access roads, yet it is often invisible in generic maintenance models.
**Improvement:** Add vegetation backlog items for growth surveys, mowing cycles, herbicide controls where allowed, row access constraints, hotspot zones, and production-loss attribution when vegetation shading becomes material.
**Acceptance evidence:** Site map overlays for vegetation zones, scheduled and completed treatment evidence, and examples linking shading-related losses to vegetation findings.

### 15. Module cleaning strategy
**Justification:** Cleaning decisions should be based on expected energy recovery and site conditions, not on ad hoc requests.
**Improvement:** Add a solar cleaning backlog with soiling indicators, water availability constraints, cleaning crew windows, expected recovery estimates, and post-cleaning verification against control strings or irradiance-normalized performance.
**Acceptance evidence:** Pre-clean versus post-clean evidence packs, cleaning recommendation rules, and examples where cleaning was deferred because predicted recovery did not justify the cost or water use.

### 16. Weather and resource normalization
**Justification:** Operators need to separate true equipment underperformance from low irradiance, weak wind resource, ambient temperature effects, and storm conditions.
**Improvement:** Introduce a normalization backlog that uses irradiance, wind speed, ambient temperature, and site weather quality flags to translate raw output into expected-versus-actual comparisons by site and by asset class.
**Acceptance evidence:** Daily normalized performance examples, missing-weather-data fallback rules, and analytics showing how normalization changes the diagnosis of a low-output period.

### 17. Alarm rationalization and incident correlation
**Justification:** Alarm floods from inverters, turbines, BMS devices, and substations create noise unless multiple alerts are collapsed into one operational incident.
**Improvement:** Add an incident-correlation backlog that groups repeated alarms by asset, time window, fault family, and production impact, then opens a single actionable case instead of dozens of duplicate exceptions.
**Acceptance evidence:** Before-and-after alarm volumes for a fault storm, grouping rules, and operator evidence that one incident can contain many related alarm events without losing traceability.

### 18. Transformer, substation, and interconnect asset coverage
**Justification:** Renewable plants fail commercially even when generation equipment is healthy if step-up transformers, collection systems, relays, or interconnect gear are not represented in the operating model.
**Improvement:** Extend the backlog to include main transformers, breakers, relays, collectors, feeders, protection systems, and point-of-interconnect equipment, with outage classes and maintenance dependencies specific to grid-facing assets.
**Acceptance evidence:** Asset catalog examples for interconnect equipment, outage scenarios that affect availability without turbine or inverter faults, and maintenance plans for transformer or relay work.

### 19. Grid outage and dispatch instruction handling
**Justification:** The package must distinguish internal outages from external dispatch limits, otherwise availability, curtailment, and settlement metrics will be wrong.
**Improvement:** Add explicit handling for grid outages, switching instructions, dispatch caps, restart permissions, and restoration notices, including the exact evidence required to support operational and contractual classifications.
**Acceptance evidence:** Sample grid-instruction event packets, classification rules for outage versus curtailment versus derate, and monthly reports proving the chosen classification path.

### 20. Spare parts and long-lead component readiness
**Justification:** Many renewable outages stay open because no one can tie the work queue to spare availability, repair lead time, or OEM exchange programs.
**Improvement:** Add a backlog item linking work orders to critical spares, repair depots, cannibalization decisions, long-lead risks, and temporary operating restrictions while parts are in transit.
**Acceptance evidence:** Planner views showing spares constraints, evidence for long-lead risk flags, and examples where outage forecasts change because a replacement part is unavailable.

### 21. Crew safety permit-to-work controls
**Justification:** Renewable operations software is incomplete if it schedules field work without proving that isolation plans, permits, and safety approvals are in place.
**Improvement:** Add permit-to-work controls that require job hazard analysis, switching approval, access authorization, confined-space or high-voltage flags where applicable, and explicit start and end ownership before field execution starts.
**Acceptance evidence:** Permit workflow examples, blocked work-order scenarios due to missing safety approvals, and approval logs with named accountable roles.

### 22. Lockout, tagout, and remote reset governance
**Justification:** Remote restart convenience can conflict with field safety when crews are on site and equipment states are changing quickly.
**Improvement:** Add backlog support for lockout and tagout status, remote reset restrictions, field presence indicators, and dual-confirmation rules for restoring equipment after maintenance or fault investigation.
**Acceptance evidence:** Safety interlock scenarios, blocked remote reset evidence while a crew is signed on site, and audit records for each restored asset.

### 23. Contractor management and competency evidence
**Justification:** Renewable sites frequently rely on OEM technicians and third-party crews whose access and work quality depend on verified competence and scope.
**Improvement:** Add contractor records, training expiry dates, authorized task classes, site induction evidence, and rules that prevent assignment of specialized work orders to crews without valid competencies.
**Acceptance evidence:** Sample contractor qualification cards, assignment denials for expired training, and reports showing work performed by internal versus contracted teams.

### 24. Drone, thermography, and borescope inspection ingestion
**Justification:** Visual and thermal evidence is central to identifying string faults, blade issues, hot connectors, battery hotspots, and substation defects.
**Improvement:** Add a backlog path for ingesting drone imagery, IR scans, borescope findings, and structured defect tags, with links back to sites, assets, inspection routes, and generated follow-up work.
**Acceptance evidence:** Example inspection imports, annotated defect records, and evidence chains connecting an image finding to a verified corrective action.

### 25. Event model expansion for operational history
**Justification:** The current four emitted events are too coarse to describe renewable operations in a way that supports replay, audits, and downstream consumers.
**Improvement:** Expand the event backlog with typed operational events such as telemetry reconciled, curtailment classified, availability pack locked, work order released, inspection completed, warranty claim prepared, and safety hold applied or cleared.
**Acceptance evidence:** Proposed event catalog, example event payloads with idempotency keys, and release evidence showing which downstream projections consume each new event type.

### 26. Idempotent telemetry and work event ingestion
**Justification:** High-frequency telemetry, repeated dispatch messages, and field retries will create duplicates unless ingestion rules are explicit.
**Improvement:** Add backlog coverage for idempotency keys based on site, asset, interval, source system, and event version so resubmitted readings, work updates, and dispatch messages do not create phantom activity.
**Acceptance evidence:** Duplicate-ingest scenarios with stable outcomes, rejection or merge rules for colliding messages, and dead-letter handling for malformed or ambiguous replays.

### 27. Data quality scorecards for sites and fleets
**Justification:** Operations teams need to know whether the data set is trustworthy before they argue about performance or contract exposure.
**Improvement:** Add scorecards for telemetry completeness, meter reconciliation success, inspection timeliness, open exception age, work-order closure quality, and attachment completeness at site and fleet level.
**Acceptance evidence:** Mock scorecards by site, threshold policies for red or amber status, and examples where a report is blocked because evidence quality is below the agreed floor.

### 28. Performance ratio and expected-versus-actual analytics
**Justification:** `performance_ratio` needs to drive diagnosis, not just sit as a periodic metric table.
**Improvement:** Add analytics that separate weather-driven deviation, outage loss, curtailment loss, clipping loss, soiling loss, and unexplained residual loss for solar and hybrid sites, with transparent formulas and time-bucket selection.
**Acceptance evidence:** Performance ratio drill-downs, formula documentation, and an example month where residual loss becomes a prioritized investigation.

### 29. Wind power curve and yaw-misalignment analytics
**Justification:** Wind plants need turbine-specific health insight that standard fleet KPIs do not provide.
**Improvement:** Add backlog work for power-curve comparison, yaw error detection, turbulence impact context, icing suspicion, and underperforming-turbine ranking against peer groups and site wind conditions.
**Acceptance evidence:** Example turbine peer reports, yaw-misalignment detection output, and linked corrective actions such as inspection, calibration, or component replacement.

### 30. Storage round-trip efficiency and dispatch compliance
**Justification:** Storage value depends on dispatch performance and efficiency, not just uptime.
**Improvement:** Add storage-specific analytics for charge acceptance, discharge delivery, auxiliary consumption, round-trip efficiency, availability by market commitment window, and missed dispatch explanation codes.
**Acceptance evidence:** Dispatch compliance reports, efficiency trend charts, and scenario evidence where a battery is technically available but commercially unavailable because dispatch constraints were violated.

### 31. Root-cause analysis workflow for underperformance
**Justification:** Operators need a repeatable path from a low-output alert to a defensible cause statement and action list.
**Improvement:** Add an RCA workflow that walks from anomaly detection through evidence gathering, candidate causes, exclusion of alternatives, owner assignment, corrective action, and verification of recovery.
**Acceptance evidence:** Completed RCA examples for solar, wind, and storage issues, cause-code libraries, and closure evidence proving that output recovered after the chosen action.

### 32. Counterfactual simulation for curtailment recovery
**Justification:** Curtailment disputes and planning decisions need a way to estimate what could have been generated or delivered absent an external limitation.
**Improvement:** Add simulation capabilities that estimate recoverable energy or availability under alternative dispatch limits, earlier restoration, different maintenance timing, or changed battery dispatch strategy.
**Acceptance evidence:** Side-by-side scenario outputs, assumption registers for each simulation, and sample evidence used in a curtailment compensation or planning discussion.

### 33. Seasonal maintenance planning
**Justification:** Renewable fleets are exposed to seasonal constraints such as rainy-season access, high-wind crane restrictions, and summer soiling or wildfire periods.
**Improvement:** Add seasonal planning logic for outage windows, vegetation cycles, blade campaigns, cleaning campaigns, transformer maintenance, and battery HVAC checks based on site conditions and resource seasons.
**Acceptance evidence:** Annual maintenance calendar examples, conflict detection between planned work and peak generation periods, and evidence that seasonal constraints change work prioritization.

### 34. Environmental and sustainability evidence
**Justification:** The manifest mentions carbon and sustainability awareness, but operations evidence should connect that idea to practical records.
**Improvement:** Add backlog items for spill incidents, waste handling from modules or blades, water usage for cleaning, vegetation and habitat constraints, and greenhouse-gas impact records tied to outages or replacement activities.
**Acceptance evidence:** Example environmental evidence packs, permit-linked tasks, and reports showing operational actions with environmental consequence tracking.

### 35. Warranty-versus-O&M responsibility splits
**Justification:** Teams lose time when an issue is known but no one can tell whether the remedy belongs to OEM warranty, LTSA coverage, local O&M scope, or owner-funded capex.
**Improvement:** Add responsibility logic that tags each failure or performance issue with the likely commercial owner, supporting clauses, notification deadlines, and required evidence to move the claim or internal action forward.
**Acceptance evidence:** Responsibility decision trees, sample cases routed to OEM versus local O&M, and evidence bundles showing why the package chose the assigned path.

### 36. Financial loss and liquidated damages exposure
**Justification:** Operations priorities should reflect commercial exposure, not only engineering severity.
**Improvement:** Add backlog support for lost-energy estimates, expected settlement impact, PPA LD exposure, warranty recovery value, spare-cost risk, and outage cost scenarios so planners can weigh engineering and commercial urgency together.
**Acceptance evidence:** Example exposure calculations, monthly risk summaries by site, and traceable links from an outage or curtailment event to estimated financial consequence.

### 37. Geospatial workbench and site map UX
**Justification:** `RenewablesAssetOperationsWorkbench` will stay shallow if operators cannot see events, inspections, and faults in site geography.
**Improvement:** Add a geospatial UI backlog with map layers for arrays, turbines, roads, substations, fences, vegetation zones, cleaning routes, and active incidents, plus rapid filtering by severity and work status.
**Acceptance evidence:** Map-view mockups, interaction flows for clicking from a map pin to the detail view, and loading-state designs for large sites with many assets.

### 38. Shift handover and control room timeline UX
**Justification:** Renewable control rooms rely on clean shift handovers that summarize events, open holds, pending dispatch instructions, and work-in-progress.
**Improvement:** Add a timeline-focused workbench view that assembles the last shift’s alarms, curtailment events, grid instructions, approvals, work releases, and unresolved risks into a structured handover pack.
**Acceptance evidence:** Shift handover prototypes, one-click export examples, and evidence that operators can acknowledge and carry forward unresolved items without losing history.

### 39. Mobile field UI for offline inspections
**Justification:** Site teams often work with poor connectivity and still need to capture inspections, photos, and closeout evidence in the field.
**Improvement:** Add a mobile backlog for offline-capable inspection and work-order flows with cached asset context, deferred sync, camera capture, barcode or QR scan support, and conflict handling when two users sync overlapping edits.
**Acceptance evidence:** Offline-to-online sync scenarios, mobile wireframes for inspection completion, and conflict-resolution examples for competing updates to the same work item.

### 40. Assistant skills for operators and planners
**Justification:** The current guided read/create/update skills are a base layer, but renewable operations need richer domain-specific assistant behaviors.
**Improvement:** Add agent skills for diagnosing underperformance, drafting curtailment classifications, assembling availability packs, preparing warranty packets, suggesting spare usage, and summarizing open safety constraints, all with governed preview and human confirmation.
**Acceptance evidence:** Skill catalog entries, prompt-and-preview examples, blocked mutation cases when required evidence is missing, and audit traces for accepted assistant actions.

### 41. Document understanding for OEM manuals, PPAs, and warranties
**Justification:** Operational decisions frequently depend on clauses buried in OEM manuals, service contracts, PPAs, and warranty schedules.
**Improvement:** Add a document-understanding backlog that extracts maintenance intervals, response obligations, guarantee definitions, cure periods, and notice requirements from controlled documents into suggested but reviewable operational records.
**Acceptance evidence:** Source-span citations from sample documents, extraction accuracy checks, and approval workflows that turn extracted obligations into governed tasks or calendar entries.

### 42. Cross-PBC event federation for grid, market, and weather context
**Justification:** Renewable operations depend on outside context, but the package must consume that context through events and contracts rather than hidden shared tables.
**Improvement:** Add a federation backlog for weather alerts, market dispatch notices, external policy changes, and audit seals so site operations, availability accounting, and settlement evidence react to external signals with explicit lineage.
**Acceptance evidence:** Event-to-action mapping, contract tests for incoming event versions, and example traces showing one upstream event changing a downstream workbench state.

### 43. Release evidence tied to operational scenarios
**Justification:** `RELEASE_EVIDENCE.md` should prove that real renewable workflows work, not just that package modules exist.
**Improvement:** Add scenario-based release evidence for a solar inverter outage, a wind turbine fault, a storage dispatch miss, a curtailment classification, a monthly availability close, and a warranty trigger, each spanning schema, services, events, UI, agent, and governance.
**Acceptance evidence:** Named scenario evidence packs, screenshots or structured outputs for each stage, and a release checklist that fails if any scenario loses lineage or approval proof.

### 44. Continuous control testing for approvals and evidence
**Justification:** The package should continuously prove that high-risk actions still respect approval and evidence rules after changes.
**Improvement:** Add controls that automatically test separation of duties, required attachments for exclusions, approval before period lock, safety hold enforcement, and event-lineage completeness for key workflows.
**Acceptance evidence:** Automated control outputs, failing-control examples with clear remediation guidance, and release-readiness summaries that list passed and failed controls by domain area.

### 45. Multi-tenant fleet segmentation
**Justification:** Fleet operators may run portfolios for multiple owners, geographies, and contracts, and renewable operating rules often differ materially between them.
**Improvement:** Add multi-tenant backlog items for owner-specific PPA models, site calendars, safety procedures, document libraries, naming conventions, and approval chains without leaking data across tenants.
**Acceptance evidence:** Tenant-isolation scenarios, tenant-specific workbench views, and negative tests proving that one tenant cannot see another tenant’s asset, event, or evidence package.

### 46. Schema extensions for OEM-specific attributes
**Justification:** Renewable plants carry OEM-specific details such as inverter firmware families, turbine retrofit kits, battery chemistry variants, and transformer protection settings that should not force brittle schema rewrites each time.
**Improvement:** Add a governed extension model for OEM-specific fields with typed definitions, compatibility checks, UI rendering rules, and event version notes so specialized attributes stay queryable without collapsing the core schema.
**Acceptance evidence:** Extension registration examples, backward-compatibility checks for projections and APIs, and proof that extended fields remain tenant-scoped and auditable.

### 47. Bulk correction tooling for telemetry gaps
**Justification:** Missing intervals, frozen tags, and backfilled historian data are common and need governed bulk correction rather than manual row edits.
**Improvement:** Add bulk correction workflows for interval gaps, duplicate intervals, bad units, daylight-saving discontinuities, and meter true-ups, with simulation before apply and explicit reason capture for each correction batch.
**Acceptance evidence:** Batch preview outputs, apply-versus-rollback examples, and corrected monthly datasets showing old and new values with reason codes and approver identity.

### 48. Exception queues for open operational risks
**Justification:** A renewable operations backlog needs purpose-built exception queues, not one undifferentiated list of problems.
**Improvement:** Add separate triage queues for telemetry quality, asset underperformance, curtailment evidence gaps, availability exclusion disputes, overdue work orders, safety holds, and pending warranty notifications, each with SLA and owner rules.
**Acceptance evidence:** Queue definitions, age-bucket reports, and operator views showing how a record moves from open risk to closed evidence without leaving the package.

### 49. Test fixtures mirroring solar, wind, and storage realities
**Justification:** Package verification is shallow if fixtures only cover abstract create-and-update flows.
**Improvement:** Add backlog guidance for realistic fixtures: string-level solar loss days, turbine fault storms, battery dispatch schedules, revenue meter corrections, vegetation-related shading, and substation outages that affect availability without local equipment faults.
**Acceptance evidence:** Fixture catalog proposals, scenario matrices covering happy path and edge cases, and release evidence showing those fixtures are used in contract, handler, UI, and agent verification.

### 50. Production readiness dashboard and go-live exit criteria
**Justification:** The package needs a hard operational definition of “ready” that combines domain coverage, controls, data quality, and release evidence.
**Improvement:** Add a production-readiness dashboard that tracks telemetry integrity, workbench coverage, event health, open critical exceptions, safety control pass rate, contract scenario coverage, and named go-live exit gates for solar, wind, and storage operations.
**Acceptance evidence:** Go-live checklist with measurable thresholds, dashboard examples for green and blocked states, and release sign-off evidence tied back to package-local operational scenarios.
