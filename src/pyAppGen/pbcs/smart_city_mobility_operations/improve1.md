# Smart City Mobility Operations Improvement Backlog

## Current Domain Evidence Used

- Manifest PBC key: `smart_city_mobility_operations`.
- Declared domain scope: transit, parking, traffic signals, incidents, curb management, multimodal services, and city mobility analytics.
- Existing owned tables: `transit_service`, `parking_asset`, `signal_plan`, `traffic_incident`, `curb_allocation`, `mobility_sensor`, `service_disruption`, `smart_city_mobility_operations_policy_rule`, `smart_city_mobility_operations_runtime_parameter`, `smart_city_mobility_operations_schema_extension`, `smart_city_mobility_operations_control_assertion`, `smart_city_mobility_operations_governed_model`.
- Existing APIs: `POST /transit-services`, `POST /parking-assets`, `POST /signal-plans`, `POST /traffic-incidents`, `POST /curb-allocations`, `GET /smart-city-mobility-operations-workbench`.
- Existing workflows: `smart_city_mobility_operations_create_transit_service_workflow`, `smart_city_mobility_operations_record_parking_asset_workflow`.
- Existing UI fragments: `SmartCityMobilityOperationsWorkbench`, `SmartCityMobilityOperationsDetail`, `SmartCityMobilityOperationsAssistantPanel`.
- Existing emitted events: `SmartCityMobilityOperationsCreated`, `SmartCityMobilityOperationsUpdated`, `SmartCityMobilityOperationsApproved`, `SmartCityMobilityOperationsExceptionOpened`.
- Existing consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Existing docs named in the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.

### 1. Corridor Registry And Functional Classification
**Justification:** Corridor decisions are currently implied across transit, signal, parking, and incident records, which makes cross-modal prioritization inconsistent and hard to audit.

**Improvement:** Add a first-class corridor model that ties each `transit_service`, `signal_plan`, `traffic_incident`, `curb_allocation`, and `parking_asset` record to a named corridor, directional segment, functional class, and target operating objective such as bus reliability, freight throughput, downtown access, or school safety.

**Acceptance evidence:** Schema and projection changes show corridor keys on all affected records, corridor-filtered workbench views exist, and tests prove corridor rollups reconcile underlying records without orphaned segments.

### 2. Corridor KPI Baselines By Time Of Day
**Justification:** Operators need to compare live conditions against the right baseline, not against a citywide average that hides commute peaks, event spikes, and overnight recovery periods.

**Improvement:** Create corridor KPI baselines for travel time, intersection delay, bus running time, parking occupancy, curb dwell, and incident clearance by weekday pattern, peak window, event window, and weather regime.

**Acceptance evidence:** Baseline tables or projections exist, workbench charts can toggle actual versus expected values, and tests verify the correct baseline is selected for at least peak, off-peak, weekend, and special-event windows.

### 3. Intersection Inventory With Movement-Level Geometry
**Justification:** Intersection operations cannot be improved with only corridor-level summaries because conflicts and failures happen at specific approaches, turn pockets, and crosswalks.

**Improvement:** Extend the domain with an intersection registry that stores approaches, controlled movements, lane groups, pedestrian crossings, bike crossings, nearby stops, and whether the location is fixed-time, actuated, adaptive, or flash.

**Acceptance evidence:** `signal_plan` and `traffic_incident` records can reference a concrete intersection and movement, UI detail views render movement geometry, and tests validate no signal plan is approved without a resolvable intersection reference.

### 4. Signal Phase And Timing Version Control
**Justification:** Timing changes are high-risk operational acts, and teams need to know exactly what split, offset, cycle, clearance interval, and coordination plan was active at any moment.

**Improvement:** Version `signal_plan` records at the phase and timing-plan level, including cycle length, phase split, offset, coordination pattern, minimum green, max green, yellow, all-red, pedestrian timing, and change reason.

**Acceptance evidence:** Event history can reconstruct the active plan by timestamp, diff views show changed timing parameters, and approval tests require engineer sign-off before a plan becomes active.

### 5. Transit Signal Priority Rule Packs
**Justification:** Transit priority works only when its activation logic is explicit, corridor-aware, and bounded so that bus reliability gains do not create unsafe pedestrian or side-street conditions.

**Improvement:** Add rule packs for transit signal priority that define eligible routes, lateness thresholds, occupancy thresholds, green extension limits, red truncation limits, recovery intervals, and blackout conditions for rail crossings, emergency calls, and school crossings.

**Acceptance evidence:** Simulation and validation tests show the rule pack can be evaluated before deployment, workbench panels show when priority fired and why, and release evidence includes at least one corridor rollout with before-and-after travel time metrics.

### 6. Emergency Vehicle Preemption Separation
**Justification:** Emergency preemption must never be conflated with routine transit priority because they carry different safety rules, override precedence, and post-event recovery needs.

**Improvement:** Create a distinct event and policy pathway for emergency vehicle preemption, with explicit conflict resolution against transit priority, pedestrian phases, railroad preemption, and flashing operations.

**Acceptance evidence:** Event traces distinguish preemption from transit priority, control tests verify precedence ordering, and workbench logs show recovery to coordinated operation after preemption clears.

### 7. Pedestrian Accessibility Timing Library
**Justification:** Accessible crossings require more than a yes or no field; they depend on timing parameters, audible features, refuge conditions, and temporary restrictions during outages or construction.

**Improvement:** Add a library of pedestrian accessibility timing settings covering walk interval, flashing clearance, leading pedestrian interval, audible indication status, tactile confirmation, and accessible detour instructions for each intersection approach.

**Acceptance evidence:** `signal_plan` approval fails when accessible timing fields are missing, UI views expose accessibility settings per movement, and test fixtures cover standard, senior-zone, school-zone, and temporary detour cases.

### 8. Bike And Scooter Geofence Boundaries
**Justification:** Micromobility operations fail when slow zones, no-ride zones, and parking corrals are not aligned with corridor, curb, and pedestrian policies.

**Improvement:** Represent bike and scooter operating boundaries as managed geofences with attributes for slow zone, no-ride zone, no-parking zone, sidewalk conflict zone, and designated parking corral, linked to `curb_allocation`, `parking_asset`, and incident records.

**Acceptance evidence:** Geofence revisions are versioned, incidents can be queried by boundary zone, and workbench maps show current and pending micromobility rules with approval history.

### 9. Protected Bike Intersection Conflict Monitoring
**Justification:** Protected intersections still fail when signal timing, curb use, and delivery behavior introduce turning conflicts that are visible only in combined data.

**Improvement:** Add a conflict-monitoring workflow that correlates bike crossing movements, turn phases, curb loading windows, and near-miss or blockage incidents to identify recurring unsafe patterns.

**Acceptance evidence:** Movement-level analytics flag repeated conflict hotspots, assistant summaries cite the contributing records, and remediation tasks can be opened directly from a hotspot view.

### 10. Curb Space Inventory By Use Type
**Justification:** Curb policy breaks down when the same block face is treated as an undifferentiated asset instead of a sequence of zones with different hours, users, and restrictions.

**Improvement:** Expand `curb_allocation` so each block face can be modeled as time-bounded zones for bus stop, passenger pickup, loading, accessible parking, bike corral, taxi, school loading, and flexible dynamic use.

**Acceptance evidence:** Zone segments can be queried independently, overlapping allocations are blocked by rules, and detail pages display a time-of-day curb stack for each block face.

### 11. Dynamic Curb Allocation Windows
**Justification:** Fixed curb assignments waste scarce frontage when morning commuter demand, midday deliveries, evening dining demand, and overnight loading have very different patterns.

**Improvement:** Add dynamic curb windows with effective dates, time bands, recurrence patterns, event overrides, and automatic fallbacks when feeds or field devices are unavailable.

**Acceptance evidence:** Rules prevent incompatible overlaps, workbench views show upcoming curb-state transitions, and tests cover weekday, weekend, holiday, and event-specific window changes.

### 12. Commercial Loading And Dwell Compliance
**Justification:** Loading behavior shapes lane blockage, bike-lane encroachment, and bus delay, so curb operations need dwell evidence rather than only allocation intent.

**Improvement:** Track commercial loading compliance with planned versus observed dwell time, vehicle class, block-face occupancy, repeat violator patterns, and whether a dwell event obstructed transit, bike, or travel lanes.

**Acceptance evidence:** `parking_asset` or curb-linked observations can produce dwell compliance dashboards, violations open governed exceptions, and acceptance tests cover legal dwell, overtime dwell, and unsafe obstruction cases.

### 13. Parking Occupancy And Turnover By Asset Type
**Justification:** Parking policy needs occupancy and turnover at lot, garage, block-face, and accessible-space levels, not a single aggregate fill percentage.

**Improvement:** Extend `parking_asset` analytics to capture occupancy, turnover, overstays, payment compliance, accessible-space usage, EV-space usage, and spillover into nearby curb zones.

**Acceptance evidence:** Workbench metrics can drill from citywide to asset level, test data supports multiple parking asset classes, and release evidence includes turnover changes after a policy adjustment.

### 14. Accessible Parking Integrity Controls
**Justification:** Accessible parking supply is often overstated because temporary closures, construction staging, and mis-signed spaces are not reflected in operational systems.

**Improvement:** Add integrity controls that reconcile designated accessible spaces, field status, obstruction incidents, permit restrictions, and nearby curb changes before an asset is shown as available.

**Acceptance evidence:** Accessibility-specific control assertions exist, broken or obstructed accessible spaces trigger visible exceptions, and tests confirm the workbench never reports unavailable accessible supply as available.

### 15. Parking Guidance And Wayfinding Integration
**Justification:** Drivers circling for parking create avoidable congestion, emissions, and unsafe curb behavior when guidance does not reflect live occupancy and street restrictions.

**Improvement:** Create a guidance layer that combines `parking_asset` occupancy, curb restrictions, event closures, and accessibility filters into destination-specific routing and advisory outputs.

**Acceptance evidence:** Guidance APIs or projections return filtered options, public-facing alert payloads can exclude closed assets, and regression tests verify closed or restricted assets are never recommended.

### 16. Incident Taxonomy For Mobility Operations
**Justification:** Traffic incidents, transit disruptions, curb conflicts, signal outages, and micromobility hazards have different operating playbooks and should not share one generic severity field.

**Improvement:** Replace shallow incident categories with a taxonomy covering crash, disabled vehicle, stalled transit vehicle, signal dark, flashing signal, flooding, lane blockage, curb obstruction, bike-lane encroachment, pedestrian hazard, and major special-event surge.

**Acceptance evidence:** `traffic_incident` records require a taxonomy code and response playbook, filters and KPI rollups use the new taxonomy, and tests confirm old generic categories are rejected or mapped deterministically.

### 17. Incident Command And Clearance Lifecycle
**Justification:** Clearance performance depends on knowing when an incident was detected, verified, dispatched, mitigated, lane-cleared, fully resolved, and post-reviewed.

**Improvement:** Add explicit incident lifecycle states with timestamps, responsible team, lane status, transit impact, detour status, and post-incident review outcome.

**Acceptance evidence:** Event histories reconstruct the full clearance chain, SLA clocks measure each stage, and workbench queues sort by stage-specific aging instead of a single created-at timestamp.

### 18. Construction, Work Zone, And Planned Event Coordination
**Justification:** Planned disruptions often cause more avoidable mobility damage than unplanned incidents because they span multiple corridors and modes for days or weeks.

**Improvement:** Treat work zones, festivals, sports events, marches, and utility occupations as planned disruption records linked to affected corridors, signal plans, curb changes, parking restrictions, detours, and public alerts.

**Acceptance evidence:** Planned events can be created and queried independently from emergency incidents, timeline views show all linked operational changes, and release evidence includes at least one planned-event rehearsal and rollback test.

### 19. Congestion Heatmaps With Directional Travel Time
**Justification:** Congestion management needs directional corridor truth because inbound morning and outbound evening patterns often differ more than entire neighborhoods do.

**Improvement:** Generate directional travel-time, queue, and reliability heatmaps using `mobility_sensor` data fused with incident and signal state so operators can see whether congestion is recurring, event-driven, or caused by control failure.

**Acceptance evidence:** Heatmaps can be filtered by direction and time window, sensor gaps are flagged visibly, and tests prove travel-time aggregation does not silently fill missing directional data with citywide averages.

### 20. Corridor Bottleneck Root-Cause Correlation
**Justification:** Operators need to know whether a bottleneck is caused by signal progression failure, curb misuse, parking search, a crash, transit dwell, or poor detour compliance.

**Improvement:** Add a correlation engine that joins corridor delay spikes to nearby signal plan changes, curb occupancy anomalies, parking saturation, incident records, and transit service disruptions.

**Acceptance evidence:** Bottleneck summaries list evidence-ranked contributors, assistant output cites the underlying records, and verification tests cover at least one signal-driven, one incident-driven, and one curb-driven bottleneck.

### 21. Mobility Data Feed Registry
**Justification:** Smart city mobility depends on many feeds, and operators need to know what each feed means, who owns it, how fresh it is, and what decisions depend on it.

**Improvement:** Create a feed registry for GTFS, GTFS-Realtime, AVL, APC, parking occupancy, curb sensors, signal controller status, SPaT/MAP, Bluetooth travel time, weather, and micromobility operator feeds, including owner, cadence, schema, and failure impact.

**Acceptance evidence:** Every downstream metric or rule can trace to a registered feed, workbench views show feed freshness and owner, and tests reject unregistered feeds from production workflows.

### 22. Feed Quality Scoring And Quarantine
**Justification:** A stale or noisy feed can cause worse decisions than no feed at all if the system continues to treat it as trustworthy.

**Improvement:** Score each feed on freshness, completeness, schema conformity, geospatial plausibility, duplication, and clock skew, then quarantine feeds that fall below policy thresholds before they affect routing, alerts, or priority logic.

**Acceptance evidence:** Feed health dashboards exist, quarantined feeds trigger exceptions and fallbacks, and test fixtures prove low-quality data cannot silently flow into corridor KPIs or public alerts.

### 23. Sensor Fusion For Corridor And Intersection State
**Justification:** No single sensor type can fully explain mobility conditions; loops, cameras, Bluetooth, APC, and curb sensors each see different parts of the same operating picture.

**Improvement:** Fuse `mobility_sensor` observations with transit and curb records to derive corridor speed, queue spillback, dwell obstruction, stop-level bus delay, and intersection blockage confidence scores.

**Acceptance evidence:** Derived metrics include provenance from contributing sensors, confidence scores degrade gracefully when sources fail, and simulation tests show fusion outputs outperform any single feed on representative scenarios.

### 24. Bus Stop And Platform Congestion Tracking
**Justification:** Transit reliability often collapses at stops and platforms where crowding, blocked boarding areas, or curb misuse delay vehicles more than line-haul traffic does.

**Improvement:** Add stop-level congestion views linking `transit_service`, curb allocations, nearby parking assets, sidewalk accessibility constraints, and incidents so operators can distinguish boarding delay from traffic delay.

**Acceptance evidence:** Stop congestion records can be filtered by route and corridor, UI cards surface blocked boarding or lift deployment issues, and tests validate stop congestion contributes to service disruption explanations.

### 25. Headway Recovery And Bunching Controls
**Justification:** Schedule adherence alone hides bus bunching and uneven passenger wait times, especially on high-frequency routes.

**Improvement:** Create headway recovery policies that compare planned headways to live vehicle spacing, then recommend holding, short turns, stop skipping with governance, or priority reinforcement when bunching exceeds configured thresholds.

**Acceptance evidence:** Risk and recommendation traces show the headway logic used, assistant actions require preview and approval, and release evidence documents at least one route where bunching metrics improved after controlled intervention.

### 26. School Zone And Student Travel Safeguards
**Justification:** School arrival and dismissal periods need stricter timing, curb, crossing, and alert behavior than the surrounding corridor at other times of day.

**Improvement:** Add school-zone policies for signal timing, crossing supervision windows, loading restrictions, curb priority, speed-display integration, and parent pickup spillover monitoring.

**Acceptance evidence:** Time-bounded school policies override general corridor policies when active, workbench views highlight active school protections, and tests cover normal school day, early release, and no-school-day conditions.

### 27. Freight Corridor And Loading Route Governance
**Justification:** Freight access is operationally important but can overwhelm main street transit, bike, and pedestrian objectives if it is not time-bounded and route-aware.

**Improvement:** Add freight corridor settings that define preferred loading windows, restricted turns, oversized-vehicle constraints, curb reservations, and detour rules during peak passenger movement periods.

**Acceptance evidence:** Freight-linked curb reservations can be validated against corridor rules, incidents can record freight involvement explicitly, and simulation output shows the impact of freight-window adjustments on bus and bike performance.

### 28. Accessibility Detour And Elevator/Path Outage Workflow
**Justification:** An accessible route is broken not only by roadway issues but also by elevator outages, sidewalk closures, platform gaps, and missing detour guidance.

**Improvement:** Create an accessibility disruption workflow that records path outages, lift outages, broken curb ramps, temporary detours, and the alternative path published to riders and pedestrians.

**Acceptance evidence:** Disruptions appear in both operational queues and public alerts, assistant summaries include accessible alternatives, and tests verify no accessibility outage can close without documented replacement guidance or exemption reason.

### 29. Emissions Estimation By Corridor And Control Action
**Justification:** Mobility operations should quantify whether a retiming, curb change, or parking policy reduces idling and stop-and-go emissions rather than treating sustainability as an afterthought.

**Improvement:** Add emissions estimation that combines speed profile, delay, dwell, queue, and vehicle-class assumptions to estimate corridor emissions before and after signal, curb, parking, or incident interventions.

**Acceptance evidence:** KPI views show emissions deltas alongside travel-time deltas, assumptions are versioned and reviewable, and tests cover at least passenger-car, bus, and delivery-vehicle profiles.

### 30. Idling And Queue Spillback Detection
**Justification:** Long queues and curb-induced lane blockages drive unnecessary emissions and can mask the true source of corridor failure.

**Improvement:** Detect sustained low-speed queues, repeated spillback into upstream intersections, bus stop blockages, and loading-related lane obstruction from fused sensor and incident data.

**Acceptance evidence:** Workbench alerts can distinguish transient delay from sustained spillback, emitted exceptions include estimated duration and likely source, and test cases cover peak-period spillback and special-event gridlock.

### 31. Multilingual Public Alert Templates
**Justification:** Public alerts are operational controls; if they are vague, delayed, or monolingual, the city will create avoidable confusion and mode-switching failures.

**Improvement:** Build multilingual alert templates for signal outages, major incidents, transit detours, parking closures, curb rule changes, school-zone activations, and accessibility path disruptions, with channel-specific length and severity rules.

**Acceptance evidence:** Alert payload previews exist for each template, approval history is retained, and tests confirm channel formatting works for web, push, SMS-length, and signage-oriented summaries.

### 32. Location-Aware Public Alert Triggers
**Justification:** Alerts should reach affected travelers without broadcasting every operational issue citywide.

**Improvement:** Trigger alerts by corridor, route, stop, intersection, neighborhood, and event perimeter, using feed quality and incident confidence thresholds to suppress noisy or premature messages.

**Acceptance evidence:** Alert triggers show why a message was or was not sent, false-positive suppression is configurable, and test fixtures verify that low-confidence incidents do not generate public alerts.

### 33. Operator Workbench Corridor Command View
**Justification:** Operators need a single command view where corridor speed, signal state, transit reliability, curb conflicts, parking pressure, incidents, and alerts can be assessed together.

**Improvement:** Expand `SmartCityMobilityOperationsWorkbench` with a corridor command view that supports map, table, and time-series layouts, plus pinned corridors and issue badges by severity and mode.

**Acceptance evidence:** UI contracts and screenshots show corridor drill-down across all core domain tables, permission-aware actions are available from the same view, and interaction tests cover map-to-record navigation.

### 34. Intersection Detail UI For Phase Failures
**Justification:** Signal engineers and operators need a detail page that explains why an intersection failed, not just that it is red on a map.

**Improvement:** Extend `SmartCityMobilityOperationsDetail` with an intersection-focused view showing active timing plan, detector health, recent overrides, pedestrian accessibility settings, nearby incidents, and recovery actions.

**Acceptance evidence:** The detail view renders intersection-specific data from `signal_plan`, `traffic_incident`, and `mobility_sensor`, degraded data is clearly marked, and tests validate the fallback state when detectors are offline.

### 35. Assistant Skill For Incident Playbooks
**Justification:** The assistant panel should help operators execute repeatable playbooks, not merely summarize records.

**Improvement:** Add an `SmartCityMobilityOperationsAssistantPanel` skill that can draft incident command steps, suggest detour messaging, recommend corridor mitigations, and prepare governed updates while citing the exact incidents, signal plans, and services involved.

**Acceptance evidence:** Skill manifests define allowed actions, preview and approval flows block unsafe direct mutation, and evaluation fixtures show the assistant cites correct records for at least crash, signal-dark, and curb-blockage scenarios.

### 36. Assistant Skill For Signal Retiming Review
**Justification:** Signal retiming proposals need structured reasoning so engineers can see whether a suggestion helps buses at the cost of pedestrian delay, side-street queues, or bike crossing conflicts.

**Improvement:** Add an assistant workflow that reviews proposed `signal_plan` changes against corridor goals, accessibility constraints, queue risk, and transit priority interactions before a plan is routed for approval.

**Acceptance evidence:** Review outputs include parameter diffs, risk explanations, and required human approvers, and tests verify the assistant refuses to approve or activate plans directly.

### 37. Event Taxonomy For Mobility Operations
**Justification:** Current emitted events are too generic to support downstream analytics, replay, and release evidence for specific mobility behaviors.

**Improvement:** Introduce typed domain events for corridor degraded, signal plan activated, transit priority fired, curb window changed, parking asset closed, incident stage changed, accessibility detour published, feed quarantined, and alert issued.

**Acceptance evidence:** Event schemas are versioned, event examples exist in package docs, and outbox tests verify both legacy compatibility and richer domain event emission.

### 38. Event Replay And Projection Drift Evidence
**Justification:** Mobility operators need confidence that projections shown in the workbench still match the event stream after retries, outages, or schema evolution.

**Improvement:** Add replay tooling that rebuilds corridor, intersection, curb, parking, and incident projections from the event log and highlights drift between projected and recomputed state.

**Acceptance evidence:** Replay reports can be generated on demand, drift thresholds open governed exceptions, and tests inject projection corruption to prove drift detection works.

### 39. Runtime Parameter Sets By Jurisdiction And Season
**Justification:** Cities and districts operate differently across school terms, tourism peaks, rainy seasons, and winter operations, so one global runtime parameter set is operationally brittle.

**Improvement:** Organize `smart_city_mobility_operations_runtime_parameter` values into named parameter sets by jurisdiction, season, event profile, and corridor class, with staged rollout and rollback support.

**Acceptance evidence:** Parameter sets can be compared and activated by scope, approval history is preserved, and tests show jurisdictional overrides never leak across tenant or district boundaries.

### 40. Policy Rules For Competing Modal Priorities
**Justification:** Smart mobility operations constantly balance bus priority, bike safety, pedestrian protection, freight access, and parking availability, and those tradeoffs need explicit policy representation.

**Improvement:** Expand `smart_city_mobility_operations_policy_rule` to encode precedence rules and guardrails for competing modal priorities, including maximum tolerated pedestrian delay, minimum bike crossing protection, and bus reliability targets.

**Acceptance evidence:** Policy simulations show which rule won and why, conflicting policies surface before approval, and workbench explanations reference the rule version that shaped each decision.

### 41. Special Event Mobility Scenario Simulation
**Justification:** Major events can overwhelm normal corridor assumptions, so the PBC should let operators test street closures, signal changes, shuttle operations, and curb reservations before deployment.

**Improvement:** Add scenario simulation that models attendance surges, road closures, temporary transit service, parking restrictions, and alert plans for sports, concerts, marches, and festivals.

**Acceptance evidence:** Simulations are non-mutating, comparison views show key KPI deltas, and release evidence includes an approved event scenario with documented assumptions and post-event actuals.

### 42. Weather Response Playbooks
**Justification:** Flooding, heavy rain, dust, and extreme heat create predictable mobility disruptions that need prepared playbooks rather than ad hoc operator responses.

**Improvement:** Create weather-triggered playbooks for signal flash risk, flooded corridors, reduced bike demand, sidewalk accessibility hazards, transit detours, and parking lot closures, tied to threshold-based activation.

**Acceptance evidence:** Weather triggers can open preconfigured response tasks, public alert templates can be prefilled from the playbook, and tests cover activation, escalation, and clear-down criteria.

### 43. Shift Handoff And Watchlist Continuity
**Justification:** Mobility operations are continuous, and knowledge loss at shift change leads to repeated diagnosis work and missed escalations.

**Improvement:** Add shift handoff artifacts that summarize active corridors, unresolved incidents, fragile feeds, pending approvals, and watchlist intersections, with direct links back to underlying records and events.

**Acceptance evidence:** Handoff snapshots are stored with timestamp and author, workbench users can compare current state to prior handoff notes, and tests verify no watchlist item disappears without closure or explicit deferral.

### 44. Equity And Neighborhood Impact Lens
**Justification:** Corridor improvements can unintentionally move delay, parking pressure, or unsafe conflicts into adjacent neighborhoods if equity impacts are not measured explicitly.

**Improvement:** Add an equity lens that reports whether retiming, curb changes, parking policy, and incident response patterns disproportionately shift burden onto specific neighborhoods, accessibility-sensitive destinations, or lower-service transit corridors.

**Acceptance evidence:** KPI views can segment by geography and vulnerability markers configured by policy, assistant summaries can cite equity impacts, and tests ensure policy simulations return neighborhood-level deltas rather than only citywide averages.

### 45. Privacy Controls For Plate And Device Data
**Justification:** Parking, curb, and sensor workflows may touch plate-like or device identifiers, and those fields need strong governance to prevent operational convenience from overriding privacy obligations.

**Improvement:** Add privacy classification, hashing, retention, masking, and access controls for plate-linked, device-linked, or rider-proximate identifiers stored or derived in parking, curb, and feed workflows.

**Acceptance evidence:** Sensitive fields are masked in standard UI views, export controls require elevated permission, and tests verify retention jobs purge or hash data on schedule without breaking aggregate analytics.

### 46. Multi-Tenant District And Agency Isolation
**Justification:** Regional mobility operations often involve multiple districts or agencies that share infrastructure but cannot share unrestricted data, rules, or approvals.

**Improvement:** Strengthen multi-tenant controls so each agency or district can own its corridors, parameter sets, alerts, release evidence, and assistant permissions while still consuming declared shared events.

**Acceptance evidence:** Tenant-isolation tests cover records, projections, alerts, and assistant actions, cross-tenant access attempts are audited and blocked, and shared event consumption preserves source ownership metadata.

### 47. Continuous Control Testing For Safety-Critical Operations
**Justification:** Safety-critical mobility functions need active controls that continuously check approval segregation, stale plans, missing evidence, and invalid feed dependencies rather than relying on periodic review.

**Improvement:** Expand `smart_city_mobility_operations_control_assertion` coverage to continuously test signal plan approvals, accessibility fields, alert review requirements, feed quarantine behavior, and event replay integrity.

**Acceptance evidence:** Control dashboards show pass and fail status by control family, failed assertions create visible exceptions, and automated test runs prove controls trigger on intentionally broken fixtures.

### 48. Release Evidence Pack For Corridor Changes
**Justification:** Signal retiming, curb changes, alert logic, and policy updates need a release pack that proves what changed, why it changed, what was tested, and what happened afterward.

**Improvement:** Define a release evidence pack for corridor-impacting changes that includes planned scope, approvals, simulations, test results, rollback plan, event samples, KPI baselines, and post-release observation windows.

**Acceptance evidence:** `RELEASE_EVIDENCE.md` can reference generated evidence artifacts, workbench users can open the release pack from changed records, and tests confirm every production change class requires an evidence bundle before approval.

### 49. Post-Release Observation And Rollback Criteria
**Justification:** A mobility release is not complete when it is deployed; it is complete when post-release behavior is measured against explicit success and rollback thresholds.

**Improvement:** Add observation windows and rollback criteria for signal, curb, parking, transit, and alert changes, including thresholds for corridor travel time, incident rate, bus delay, accessibility complaints, and feed health.

**Acceptance evidence:** Release workflows record observation windows and threshold outcomes, rollback readiness is visible in the workbench, and release evidence shows both successful release closure and triggered rollback scenarios.

### 50. End-To-End Go-Live Readiness Scorecard
**Justification:** Operators need one final gate that summarizes whether the smart city mobility package is actually ready for a controlled launch across data, UI, automation, events, and evidence.

**Improvement:** Build a go-live scorecard that rolls up feed readiness, control status, assistant evaluation, UI completeness, event schema coverage, simulation coverage, accessibility checks, emissions instrumentation, and release-evidence completeness for `smart_city_mobility_operations`.

**Acceptance evidence:** The scorecard is exposed in `GET /smart-city-mobility-operations-workbench`, readiness cannot show green when required evidence is missing, and package-local tests validate every scorecard dimension against seeded pass and fail cases.
