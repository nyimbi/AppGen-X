# Facility Energy Management PBC Improvement Backlog

## Current Domain Evidence Used

- `pbc`: `facility_energy_management`
- `label`: `Facility Energy Management`
- `description`: `Facility meters, loads, equipment schedules, demand response, optimization, tariffs, and energy performance`
- `tables`: `energy_meter`, `load_profile`, `equipment_schedule`, `demand_response_event`, `energy_optimization`, `tariff_signal`, `energy_baseline`, `facility_energy_management_policy_rule`, `facility_energy_management_runtime_parameter`, `facility_energy_management_schema_extension`, `facility_energy_management_control_assertion`, `facility_energy_management_governed_model`
- `apis`: `POST /energy-meters`, `POST /load-profiles`, `POST /equipment-schedules`, `POST /demand-response-events`, `POST /energy-optimizations`, `GET /facility-energy-management-workbench`
- `ui_fragments`: `FacilityEnergyManagementWorkbench`, `FacilityEnergyManagementDetail`, `FacilityEnergyManagementAssistantPanel`
- `workflows`: `facility_energy_management_create_energy_meter_workflow`, `facility_energy_management_record_load_profile_workflow`
- `analytics`: `facility_energy_management_risk_score`, `facility_energy_management_workbench_metric`
- `emits`: `FacilityEnergyManagementCreated`, `FacilityEnergyManagementUpdated`, `FacilityEnergyManagementApproved`, `FacilityEnergyManagementExceptionOpened`
- `consumes`: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- `capabilities`: `energy_meter_management`, `facility_energy_management_workflow`, `facility_energy_management_analytics`, `configuration_schema`, `rule_engine`, `parameter_engine`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`, `workbench`, `agentic_document_instruction_intake`, `ai_agent_task_assistance`, `configuration_workbench`, `continuous_release_assurance`
- `advanced_capabilities`: `facility_energy_management_event_sourced_operational_history`, `facility_energy_management_multi_tenant_policy_isolation`, `facility_energy_management_schema_evolution_resilience`, `facility_energy_management_autonomous_anomaly_detection`, `facility_energy_management_predictive_risk_scoring`, `facility_energy_management_counterfactual_scenario_simulation`, `facility_energy_management_cryptographic_audit_proofs`, `facility_energy_management_continuous_control_testing`, `facility_energy_management_carbon_and_sustainability_awareness`, `facility_energy_management_governed_ai_agent_execution`
- `docs`: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`
- `tests`: `tests/test_contract.py`

## Improvement Backlog

### 1. Meter and Submeter Topology in `energy_meter`

**Justification:** Building totals are not trustworthy unless the package can explain how whole-building meters, branch meters, floor meters, tenant submeters, and virtual rollups relate to each other.

**Improvement:** Extend `energy_meter` with parent-child links, virtual meter formulas, feeder identifiers, tenant tags, service-point metadata, meter role, and rollup validation surfaced in `FacilityEnergyManagementWorkbench`.

**Acceptance evidence:** A seeded hierarchy with one utility meter, floor submeters, and tenant submeters; reconciliation tests that flag unexplained residuals; and `RELEASE_EVIDENCE.md` examples showing drilldown from site total to submeter.

### 2. Interval Read Fidelity in `load_profile`

**Justification:** Fifteen-minute and hourly intervals are the raw material for peak demand, after-hours waste, and curtailment proof; day totals lose the patterns that matter.

**Improvement:** Upgrade `load_profile` to store interval width, read quality, timezone, daylight-saving crossover handling, estimated-versus-observed flags, and channel mappings for kWh, kW, gas, steam, and chilled water.

**Acceptance evidence:** Import fixtures for missing intervals, duplicate intervals, daylight-saving boundary days, and mixed utility channels; plus route tests showing interval charts in `FacilityEnergyManagementDetail`.

### 3. Commissioning and Health Evidence for `energy_meter`

**Justification:** Operators need to know whether a meter is live, stale, swapped, inverted, or under maintenance before using its numbers in optimization and tenant allocation.

**Improvement:** Add commissioning date, decommission date, heartbeat cadence, health status, failed-read counters, calibration evidence, and replacement lineage to `energy_meter`.

**Acceptance evidence:** Tests that block active use of stale or decommissioned meters, a health queue in `FacilityEnergyManagementWorkbench`, and release evidence showing meter swap history preserved across replacements.

### 4. Utility Account and Service Point Mapping in `energy_meter`

**Justification:** Tariff decisions and bill checks fail when meters are not anchored to the utility account, service class, rate code, and physical service point they belong to.

**Improvement:** Attach service account identifiers, premise identifiers, tariff eligibility, utility ownership, transformer reference, and point-of-delivery semantics to `energy_meter`.

**Acceptance evidence:** Validation that prevents an `energy_meter` from being approved without service mapping, plus examples that show one campus with multiple utilities and separate service classes.

### 5. Estimated Read Provenance and Correction Workflow in `load_profile`

**Justification:** Energy teams need to distinguish raw reads, utility estimates, analyst backfills, and corrected data before using the profile for baselines or chargeback.

**Improvement:** Add provenance codes, correction reasons, source document links, superseded intervals, and governed reprocessing through `facility_energy_management_record_load_profile_workflow`.

**Acceptance evidence:** Correction scenarios with before-and-after interval traces, permission tests for who may revise estimated reads, and event evidence that downstream projections refresh after correction.

### 6. Seasonal and Time-of-Use Tariff Calendars in `tariff_signal`

**Justification:** Cost optimization is weak unless `tariff_signal` can express season, weekday class, holiday treatment, on-peak windows, and shoulder periods with no ambiguity.

**Improvement:** Model season calendars, time bands, holiday overrides, coincident-peak markers, and tariff-effective dates directly in `tariff_signal`.

**Acceptance evidence:** Tariff fixtures for summer and winter schedules, tests for holiday exceptions, and workbench views that highlight which time band each interval fell into.

### 7. Demand Charge and Ratchet Determinants in `tariff_signal`

**Justification:** Facilities often pay more for demand than for energy, so the package has to compute billing determinants, not just display rate labels.

**Improvement:** Extend `tariff_signal` with ratchet rules, rolling demand windows, contract demand, non-coincident peak, coincident peak, and minimum-bill determinants that can drive `energy_optimization`.

**Acceptance evidence:** Billing-determinant tests covering ratchet carry-forward, contract exceedance, and multiple billing windows; plus release evidence comparing expected versus computed demand charges.

### 8. Tariff Scenario Comparison in `energy_optimization`

**Justification:** Energy managers need to compare the current tariff against proposed rate structures before moving loads, changing schedules, or enrolling in new programs.

**Improvement:** Add scenario inputs to `energy_optimization` for tariff swaps, seasonal rate changes, riders, and dynamic-price exposure, with side-by-side cost and demand outcomes.

**Acceptance evidence:** Scenario reports showing two tariff options against the same `load_profile`, APIs that return deltas without mutating production records, and `RELEASE_EVIDENCE.md` screenshots of tariff comparison output.

### 9. HVAC Schedule Hierarchy in `equipment_schedule`

**Justification:** Real facilities run schedule layers for campus, building, floor, zone, air handler, and exception calendars; a single flat schedule cannot capture HVAC operations.

**Improvement:** Expand `equipment_schedule` with hierarchy level, zone mapping, schedule inheritance, holiday calendars, occupancy-linked exceptions, and equipment group definitions for HVAC assets.

**Acceptance evidence:** Tests proving inherited schedules resolve deterministically, workbench views that show overridden versus inherited hours, and examples for a campus-wide holiday shutdown with one 24/7 critical zone exception.

### 10. Occupancy, Weather, and Holiday Overrides in `equipment_schedule`

**Justification:** HVAC schedules should respond to whether the building is actually occupied, how hot or cold it is, and whether a holiday pattern applies.

**Improvement:** Add override triggers in `equipment_schedule` for occupancy windows, weather thresholds, holiday sets, event bookings, and pre-cool or pre-heat logic that can feed `energy_optimization`.

**Acceptance evidence:** Simulation cases for heat waves, cold mornings, and holiday closures; route tests showing projected runtime changes; and release evidence that an override explains why schedules deviated from the default.

### 11. Schedule Conflict Detection and Lock Windows in `equipment_schedule`

**Justification:** Controls engineers need to see when two schedules claim the same equipment, when demand response conflicts with comfort commitments, and when a change lands inside a maintenance lock window.

**Improvement:** Add conflict detection, lock windows, maintenance blackout periods, and reviewer sign-off rules to `equipment_schedule`.

**Acceptance evidence:** Negative tests for overlapping commands, UI conflict cards in `FacilityEnergyManagementWorkbench`, and audit trails that show who resolved a schedule collision.

### 12. Controls Command Boundary for `energy_optimization`

**Justification:** Optimization output must stop at a governed command boundary so the package does not act like an unreviewed building automation controller.

**Improvement:** Make `energy_optimization` produce proposed setpoint changes, schedule changes, and load-shed actions as approval-gated commands with explicit handoff status instead of direct device writes.

**Acceptance evidence:** Approval tests showing blocked direct execution, command preview panels in `FacilityEnergyManagementDetail`, and emitted events proving that accepted actions move through a bounded handoff state.

### 13. Manual Override Governance in `facility_energy_management_policy_rule`

**Justification:** Manual overrides are necessary during tenant complaints, comfort issues, and equipment faults, but they should never become invisible policy bypasses.

**Improvement:** Add override categories, expiry times, required rationale, approver rules, and automatic reversion logic to `facility_energy_management_policy_rule`.

**Acceptance evidence:** Tests that expire temporary overrides, views that separate active overrides from baseline policy, and evidence that expired overrides stop influencing schedules and optimization runs.

### 14. Critical Load, Generator, and UPS Awareness in `load_profile`

**Justification:** Hospitals, labs, data rooms, and life-safety systems cannot be treated like generic load when shedding or rescheduling energy use.

**Improvement:** Annotate `load_profile` segments with criticality class, backup power availability, transfer status, and shed eligibility so demand response and optimization respect mission-critical loads.

**Acceptance evidence:** Scenario tests where generator-backed loads remain exempt during curtailment, critical-load badges in the workbench, and release evidence showing blocked recommendations for protected circuits.

### 15. Baseline Versioning in `energy_baseline`

**Justification:** Baselines shift after retrofits, occupancy changes, and tenant turnover; one mutable baseline erases the history needed for savings claims and dispute review.

**Improvement:** Add version number, effective window, baseline method, reviewer approval, and supersession lineage to `energy_baseline`.

**Acceptance evidence:** Baseline history views, tests that prevent overlapping active baseline windows for the same scope, and documentation of which retrofit or occupancy event triggered a new baseline version.

### 16. Weather-Normalized Performance in `energy_baseline`

**Justification:** A colder winter or hotter summer should not masquerade as an operational improvement or regression.

**Improvement:** Extend `energy_baseline` with degree-day normalization, weather source lineage, expected-load curves, and adjusted-versus-actual comparisons for electricity and thermal loads.

**Acceptance evidence:** Regression tests using hot, normal, and mild weather periods, charts in `FacilityEnergyManagementDetail` that separate weather effect from operational effect, and release evidence for one building before and after normalization.

### 17. Baseload, After-Hours, and Drift Anomalies in `facility_energy_management_autonomous_anomaly_detection`

**Justification:** Energy waste often appears as quiet drift rather than dramatic spikes, especially in baseload, night setbacks, and equipment that never quite turns off.

**Improvement:** Tune `facility_energy_management_autonomous_anomaly_detection` to detect baseload creep, after-hours spikes, weekend runtime, stuck setpoints, and load shape drift by meter, submeter, and zone.

**Acceptance evidence:** Anomaly fixtures with explainable feature contributions, reviewer feedback capture on false positives, and workbench cards showing whether the anomaly came from a main meter, tenant submeter, or HVAC branch.

### 18. Investigation Case Packs for `FacilityEnergyManagementExceptionOpened`

**Justification:** An anomaly is only useful if the operator can see the timeline, suspected cause, affected schedules, and impacted tenants in one place.

**Improvement:** Make `FacilityEnergyManagementExceptionOpened` carry links to meter context, tariff band, schedule state, baseline delta, and recommended next action, all rendered in `FacilityEnergyManagementWorkbench`.

**Acceptance evidence:** Exception views that assemble interval charts, schedule history, and tenant impact in one screen; plus event payload tests that guarantee the same links exist in the emitted exception record.

### 19. HVAC Fault Detection and Diagnostics in `facility_energy_management_workbench_metric`

**Justification:** Operators need more than “high load” alerts; they need diagnostics for simultaneous heating and cooling, short cycling, stuck dampers, and runaway fans.

**Improvement:** Add HVAC-specific diagnostic metrics to `facility_energy_management_workbench_metric` with symptom, likely cause, confidence, and affected equipment-schedule linkages.

**Acceptance evidence:** Diagnostic examples for short cycling and after-hours airflow, charts that correlate `equipment_schedule` with interval load, and tests that route severe diagnostics into exception queues.

### 20. Peak Demand Forecasting in `facility_energy_management_risk_score`

**Justification:** Demand-charge control depends on knowing which afternoon is likely to set the billing peak before the peak actually happens.

**Improvement:** Expand `facility_energy_management_risk_score` with peak-likelihood scoring based on recent intervals, weather forecast, occupancy, schedule state, and known demand-response commitments.

**Acceptance evidence:** Forecast backtests on historical peak days, risk bands in `FacilityEnergyManagementWorkbench`, and release evidence showing forecast lead time before a near-peak event.

### 21. Demand Response Asset Eligibility in `demand_response_event`

**Justification:** A curtailment program only works if the package knows which loads, buildings, and tenants are actually eligible to respond.

**Improvement:** Add enrollment status, shed capacity, opt-out rules, notice requirements, tenant exclusions, and fallback assets to `demand_response_event`.

**Acceptance evidence:** Eligibility tests that reject enrollment for protected loads, roster views showing enrolled assets and excluded tenants, and examples of one campus with mixed participation.

### 22. Demand Response Dispatch Orchestration in `demand_response_event`

**Justification:** Dispatch has to track notice time, acknowledgement, execution state, and missed steps; otherwise the facility cannot prove whether it responded correctly.

**Improvement:** Model `demand_response_event` through planned, notified, acknowledged, active, partially executed, completed, failed, and settled states with timestamps and responsible roles.

**Acceptance evidence:** Workflow tests that block invalid state jumps, workbench timelines for each dispatch, and emitted-event traces that show the exact progression of one curtailment event.

### 23. Curtailment Measurement and Settlement in `demand_response_event`

**Justification:** Programs pay or penalize based on measured reduction against a baseline, so the package needs repeatable measurement rules rather than ad hoc spreadsheets.

**Improvement:** Add baseline selection, performance calculation, exclusion windows, weather adjustments, and settlement-ready summaries to `demand_response_event`.

**Acceptance evidence:** Settlement fixtures for full, partial, and failed curtailment, traceable baseline links back to `energy_baseline`, and export evidence ready for audit review.

### 24. Comfort and Safety Guardrails in `facility_energy_management_control_assertion`

**Justification:** Load shed actions that protect cost but violate temperature, ventilation, or safety guardrails create operational and legal exposure.

**Improvement:** Encode occupant comfort bands, ventilation minimums, freezer limits, pressure relationships, and life-safety constraints as continuous checks in `facility_energy_management_control_assertion`.

**Acceptance evidence:** Failing-control examples that block an overaggressive shed plan, dashboards showing which assertion blocked the action, and release evidence that guardrails stay active during demand response.

### 25. Post-Event Rebound Management in `demand_response_event`

**Justification:** Many facilities erase curtailment gains when all equipment snaps back at the end of the event.

**Improvement:** Add staged recovery plans, rebound limits, and warm-start or cool-start strategies to `demand_response_event` so recovery is controlled instead of immediate.

**Acceptance evidence:** Simulations comparing uncontrolled versus staged rebound, operator controls for recovery sequencing, and interval traces proving the rebound peak stayed below the original event threshold.

### 26. Carbon Factor Registry in `facility_energy_management_carbon_and_sustainability_awareness`

**Justification:** Carbon reporting is meaningless if grid factors, district energy factors, and fuel conversion factors are opaque or inconsistent across buildings.

**Improvement:** Maintain factor source, geography, effective date, marginal-versus-location basis, and revision lineage under `facility_energy_management_carbon_and_sustainability_awareness`.

**Acceptance evidence:** Factor-version tests, views that show which factor set drove each carbon calculation, and release evidence for an updated factor set changing reported emissions without rewriting historical periods.

### 27. Carbon and Cost Co-Optimization in `energy_optimization`

**Justification:** Facilities increasingly choose between least-cost, least-carbon, and comfort-preserving actions; the package should expose the tradeoff, not hide it.

**Improvement:** Add objective weighting in `energy_optimization` for cost, carbon, demand, comfort, and tenant impact, with explainable tradeoff scoring.

**Acceptance evidence:** Scenario runs that choose different actions under cost-first and carbon-first settings, explanation panels in `FacilityEnergyManagementDetail`, and tests that preserve auditability of the chosen weights.

### 28. Tenant Allocation Rules in `energy_meter`

**Justification:** Mixed-use buildings need defensible energy allocation by suite, floor, lease, or agreed percentage when only some tenants are submetered.

**Improvement:** Extend `energy_meter` with allocation scope, tenant mapping, fallback split rules, vacancy treatment, and lease-effective dates for tenant energy allocation.

**Acceptance evidence:** Allocation examples for direct submeter, prorated common load, and vacant-suite treatment; plus tests that prevent overlapping active allocation rules for the same tenant and period.

### 29. Common-Area Reconciliation in `load_profile`

**Justification:** Tenant bills and internal chargebacks fail when common-area consumption is not reconciled back to the main meter and the submeters beneath it.

**Improvement:** Add reconciliation views to `load_profile` that compare master-meter consumption, summed submeter consumption, estimated common-area residual, and loss tolerance bands.

**Acceptance evidence:** Reconciliation reports by billing cycle, alerts when residual loss exceeds tolerance, and `RELEASE_EVIDENCE.md` output for one building with transparent common-area apportionment.

### 30. Retrofit Opportunity Register in `energy_optimization`

**Justification:** Energy management should preserve not only operational actions but also retrofit ideas such as lighting upgrades, VFD additions, insulation work, and controls retuning.

**Improvement:** Add a retrofit register to `energy_optimization` with measure type, affected meters or schedules, expected savings, capex, dependency, and status from idea to verified savings.

**Acceptance evidence:** Example retrofit records for lighting, HVAC controls, and building envelope measures; plus views that tie each measure to baseline deltas and approval history.

### 31. Savings Persistence Tracking in `energy_baseline`

**Justification:** A retrofit that saves energy for one month and drifts back six months later should not still be counted as fully successful.

**Improvement:** Compare post-retrofit performance against the approved `energy_baseline`, track persistence by month and season, and open exceptions when savings decay beyond a configured threshold.

**Acceptance evidence:** Persistence charts across multiple months, alerts for savings slippage, and release evidence that one retrofit remains on track while another opens a remediation case.

### 32. Retrofit Prioritization Scenarios in `facility_energy_management_counterfactual_scenario_simulation`

**Justification:** Portfolio teams need to rank retrofits by cost, demand relief, carbon reduction, disruption, and tenant sensitivity before funding decisions are made.

**Improvement:** Use `facility_energy_management_counterfactual_scenario_simulation` to compare retrofit bundles, staging windows, and expected operational side effects across facilities.

**Acceptance evidence:** Side-by-side scenario packs for at least three retrofit bundles, explainable rankings for cost and carbon impact, and non-mutating APIs that return scenario results without altering live records.

### 33. Tariff and O&M Document Intake in `agentic_document_instruction_intake`

**Justification:** Tariff riders, equipment operating manuals, and seasonal operating instructions often arrive as documents before anyone keys them into the system.

**Improvement:** Teach `agentic_document_instruction_intake` to extract tariff periods, rate clauses, demand-response obligations, HVAC operating windows, and meter identifiers into reviewable drafts.

**Acceptance evidence:** Document extraction tests with source-span citations, blocked writes until a human approves the draft, and assistant previews in `FacilityEnergyManagementAssistantPanel`.

### 34. Anomaly Triage Skill in `ai_agent_task_assistance`

**Justification:** The assistant should reduce analyst load by assembling evidence and likely causes, not by issuing vague summaries.

**Improvement:** Add an `ai_agent_task_assistance` skill that reads anomaly context, recent schedule changes, tariff exposure, weather conditions, and tenant allocation rules, then prepares a triage brief.

**Acceptance evidence:** Assistant sessions that open with cited interval, schedule, and baseline evidence; permission tests that prevent direct mutation without approval; and reviewer feedback capture on suggested root causes.

### 35. Tenant Allocation Explanation Skill in `FacilityEnergyManagementAssistantPanel`

**Justification:** Tenant disputes are easier to resolve when the allocation rule and the supporting meter evidence can be explained in plain language with exact inputs.

**Improvement:** Add an explanation workflow to `FacilityEnergyManagementAssistantPanel` that narrates how a tenant charge was derived from `energy_meter`, `load_profile`, and allocation rules.

**Acceptance evidence:** Example explanations for submetered and prorated tenants, links back to the exact intervals and rules used, and blocked responses when supporting evidence is incomplete.

### 36. Operator Queue in `FacilityEnergyManagementWorkbench`

**Justification:** Control-room users need one queue for stale meters, missed reads, active peaks, open anomalies, and pending demand-response actions instead of hopping across generic admin screens.

**Improvement:** Make `FacilityEnergyManagementWorkbench` expose a role-specific operations queue with urgency ranking, site filter, meter health, active tariff band, and direct links to the affected schedule or baseline.

**Acceptance evidence:** Route tests for queue states, screenshots of filtered operations views, and release evidence showing how one active peak alert and one stale-meter alert appear together with different actions.

### 37. Sustainability and Carbon Detail View in `FacilityEnergyManagementDetail`

**Justification:** Sustainability teams need emissions, avoided carbon, retrofit savings, and weather-normalized performance without losing connection to the operational records underneath.

**Improvement:** Extend `FacilityEnergyManagementDetail` with carbon intensity overlays, avoided-emissions calculations, monthly savings persistence, and drill-through from carbon totals to the underlying meter and baseline records.

**Acceptance evidence:** Detail-view tests for carbon drilldown, example records showing electricity and thermal emissions side by side, and release evidence with a verified monthly carbon report.

### 38. Controls Engineer Tuning Workspace in `configuration_workbench`

**Justification:** Controls staff need a place to tune thresholds, blackout windows, and optimization parameters without editing code or raw tables.

**Improvement:** Use `configuration_workbench` to manage schedule thresholds, rebound limits, anomaly sensitivities, comfort guardrails, and demand-response defaults under approval control.

**Acceptance evidence:** Parameter change history, rollback tests, approval flows for high-risk settings, and UI proof that changed parameters immediately annotate the affected recommendations.

### 39. Tenant Services Allocation View in `FacilityEnergyManagementWorkbench`

**Justification:** Property or facilities teams field tenant questions about charges, after-hours HVAC use, and suite-level consumption every billing cycle.

**Improvement:** Add a tenant services view in `FacilityEnergyManagementWorkbench` that shows tenant submeters, common-area share, after-hours HVAC runs, demand-response participation, and open billing disputes.

**Acceptance evidence:** Permission-aware screens by tenant scope, examples covering one direct-submeter tenant and one prorated tenant, and exportable evidence packs for billing review.

### 40. Command and Query API Coverage Beyond `POST /energy-meters`

**Justification:** The current API list is heavy on create commands and light on validation, simulation, correction, and read models that operational tools actually need.

**Improvement:** Expand `POST /energy-meters`, `POST /load-profiles`, `POST /equipment-schedules`, `POST /demand-response-events`, `POST /energy-optimizations`, and `GET /facility-energy-management-workbench` into a clear command/query boundary with validate-only, simulate, correction, projection, and evidence-export routes.

**Acceptance evidence:** A route catalog that distinguishes commands from queries, compatibility tests for existing endpoints, and examples showing validate-only and simulation calls returning non-mutating results.

### 41. Event Boundary Expansion Beyond `FacilityEnergyManagementCreated`

**Justification:** Downstream consumers should not infer important state changes from generic lifecycle events when the energy domain has distinct operational milestones.

**Improvement:** Add typed events around meter commissioned, baseline approved, demand-response dispatched, curtailment settled, retrofit verified, anomaly suppressed, and tariff updated while keeping `FacilityEnergyManagementCreated`, `FacilityEnergyManagementUpdated`, `FacilityEnergyManagementApproved`, and `FacilityEnergyManagementExceptionOpened` as envelope events.

**Acceptance evidence:** Event schema fixtures, versioning notes, and release evidence that one end-to-end flow emits the typed operational events in a predictable order.

### 42. Replay-Safe Inbox and Outbox Evidence in `appgen_x_outbox_inbox_eventing`

**Justification:** Energy operations cannot tolerate duplicate curtailment events or missed baseline updates when messages are retried or replayed.

**Improvement:** Strengthen `appgen_x_outbox_inbox_eventing` with idempotency keys, replay markers, deterministic event ordering, and dead-letter evidence tied back to the affected facility record.

**Acceptance evidence:** Duplicate-message tests, replay checks that preserve exactly-once business effect, and workbench panels that let operators inspect dead-letter causes without leaving the package.

### 43. Policy-Driven Tenant Isolation in `facility_energy_management_multi_tenant_policy_isolation`

**Justification:** Campus operators, landlords, and third-party energy managers may share infrastructure while requiring strict separation of tenant data, thresholds, and actions.

**Improvement:** Use `facility_energy_management_multi_tenant_policy_isolation` to partition meter visibility, tenant allocation rules, assistant context, and workbench filters by tenant and operating entity.

**Acceptance evidence:** Cross-tenant negative tests, tenant-scoped workbench screenshots, and evidence that one operator can manage common plant assets without seeing another tenant's charge details.

### 44. Runtime Parameter Governance in `facility_energy_management_runtime_parameter`

**Justification:** Peak thresholds, anomaly sensitivity, comfort bands, and rebound limits are operational settings that need versioning and approval, not hidden constants.

**Improvement:** Add typed parameter groups, safe bounds, approval requirements, and effective dates to `facility_energy_management_runtime_parameter`.

**Acceptance evidence:** Parameter schema validation, rollback scenarios, UI diff views in `configuration_workbench`, and release evidence showing a threshold change propagating to forecasts and control assertions.

### 45. Continuous Control Testing in `facility_energy_management_continuous_control_testing`

**Justification:** It should be possible to prove, every day, that the package still enforces critical controls around overrides, tenant boundaries, demand response, and billing evidence.

**Improvement:** Implement `facility_energy_management_continuous_control_testing` over `facility_energy_management_control_assertion` to continuously test no-expired-overrides, no-missing-baseline-settlement, no-cross-tenant allocation, and no-unapproved load-shed commands.

**Acceptance evidence:** Control dashboards with pass/fail history, failing-control events tied to specific records, and release evidence that all high-severity controls passed for the candidate build.

### 46. Schema Extension Registry in `facility_energy_management_schema_extension`

**Justification:** Facilities will need local attributes for campus type, green lease clauses, tenant classes, and utility programs without breaking the shared domain core.

**Improvement:** Use `facility_energy_management_schema_extension` to register extension fields, ownership, compatibility rules, backfill needs, and UI placement for energy-specific custom attributes.

**Acceptance evidence:** Extension registration examples for at least two facilities, migration preview output, and tests that prevent extensions from colliding with core keys like `energy_meter` and `tariff_signal`.

### 47. Governed Model Lifecycle in `facility_energy_management_governed_model`

**Justification:** Scoring models and optimization logic need promotion, rollback, and explanation controls if they influence curtailment, anomaly severity, or retrofit ranking.

**Improvement:** Add versioned model registration, approval states, champion-challenger comparisons, and rollback metadata to `facility_energy_management_governed_model`.

**Acceptance evidence:** Model promotion tests, comparison reports between two scoring versions, and audit-ready records showing which model version produced each recommendation.

### 48. Consumed-Event Freshness for `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`

**Justification:** Energy decisions should visibly degrade or pause when upstream policy or KPI feeds are stale rather than silently continuing with outdated assumptions.

**Improvement:** Add freshness tracking, fallback behavior, and operator warnings for `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` consumption paths.

**Acceptance evidence:** Staleness tests that mark projections as degraded, workbench warnings when a consumed feed is behind, and evidence that high-risk recommendations are blocked until freshness recovers.

### 49. Regression Narratives in `seed_data.py` and `tests/test_contract.py`

**Justification:** Release confidence improves when the package ships with realistic facility stories rather than isolated happy-path fixtures.

**Improvement:** Build seed narratives and contract tests that cover mixed tariff structures, tenant submeters, HVAC schedule overrides, demand-response dispatch, anomaly escalation, retrofit verification, and carbon reporting.

**Acceptance evidence:** Deterministic seed datasets, contract tests that fail on missing route or event boundaries, and release notes that point to the exact seeded scenarios used for verification.

### 50. End-to-End Release Drill in `RELEASE_EVIDENCE.md`

**Justification:** The package is not ready until it can prove one complete operational story from interval ingestion through tariff analysis, scheduling, anomaly handling, demand response, tenant allocation, and release sign-off.

**Improvement:** Make `RELEASE_EVIDENCE.md` capture a repeatable release drill using `facility_energy_management_create_energy_meter_workflow`, `facility_energy_management_record_load_profile_workflow`, the workbench, assistant flows, APIs, events, and control assertions.

**Acceptance evidence:** A dated drill record with commands used, projections verified, emitted and consumed event traces, workbench screenshots, failed-control review, and explicit sign-off that no manual database edits were required.
