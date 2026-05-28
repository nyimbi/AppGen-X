# Facilities and Space Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `facilities_space_management`. Each item is specific to facilities and workplace operations: sites, buildings, floors, spaces, occupancy, reservations, moves, maintenance blocks, access constraints, safety inspections, utilization, capacity, hybrid work, wayfinding, leases, emergency readiness, and workplace intelligence. The intent is complete domain coverage for a better-than-world-class facilities and space PBC while preserving AppGen-X package boundaries.

## Current Domain Evidence Used

- Domain purpose: owns facilities, floors, spaces, occupancy, reservations, moves, maintenance signals, access constraints, utilization, safety status, and workplace intelligence.
- Owned tables include facility site, floor, space record, space type, occupancy plan, occupancy assignment, space reservation, move request, move task, maintenance signal, availability snapshot, access constraint, safety inspection, utilization observation, capacity plan, exception case, policy rules, runtime parameters, schema extensions, control assertions, governed models, outbox, inbox, and dead-letter evidence.
- Operations include `create_facility_site`, `define_floor`, `create_space_record`, `classify_space_type`, `create_occupancy_plan`, `assign_occupant`, `reserve_space`, `open_move_request`, `complete_move_task`, `record_maintenance_signal`, `publish_availability_snapshot`, `define_access_constraint`, `record_safety_inspection`, `observe_utilization`, `build_capacity_plan`, `compile_facility_rule`, and `simulate_space_demand`.
- Events include `FacilityCreated`, `SpaceReserved`, `MoveRequested`, `MaintenanceSignalRecorded`, `SafetyInspectionRecorded`, and `CapacityPlanPublished`; consumed events include employee, work-order, access-policy, policy, lease, and maintenance signals.
- Existing advanced claims include space demand forecasting, reservation conflict optimization, occupancy scenario simulation, safety-risk scoring, maintenance-aware availability, and hybrid workplace recommendation.

## 50 Better-Than-World-Class Improvements

### 1. Facility Site Master and Campus Topology

**Justification:** A facility is more than a name and address. Facilities teams need campus relationships, buildings, wings, entrances, parking, loading docks, emergency zones, amenities, and operational ownership to manage space accurately.

**Improvement:** Expand `create_facility_site` with campus hierarchy, geospatial boundary, building group, operating hours, facility owner, service zones, emergency zones, parking assets, visitor entrances, loading areas, and site status. The UI should render a navigable site topology instead of a flat facility list.

### 2. Building and Floor Digital Twin Model

**Justification:** Floor definitions need usable geometry, adjacency, zones, vertical circulation, accessibility routes, safety exits, and maintenance areas. Generic floors cannot support reservations, moves, occupancy, and emergency planning.

**Improvement:** Upgrade `define_floor` with floor maps, coordinate systems, zones, entrances, elevators, stairs, exits, restrooms, amenities, restricted areas, and map versioning. Link every space to a floor-map version and provide change impact when floor plans are updated.

### 3. Space Record Precision and Area Standards

**Justification:** Space management depends on accurate areas, capacity, seating, room features, and usage standards. Inconsistent measurements distort utilization, chargeback, and planning.

**Improvement:** Expand `create_space_record` with gross, rentable, usable, assignable, and net area; capacity method; seating count; neighborhood; amenities; accessibility; AV features; environmental profile; and measurement evidence. Track area standards and effective dates.

### 4. Space Type and Usage Taxonomy

**Justification:** Offices, desks, conference rooms, labs, clean rooms, clinics, classrooms, warehouses, storage, hoteling desks, wellness rooms, and secure rooms have very different rules. A generic type list underserves facilities operations.

**Improvement:** Upgrade `classify_space_type` with governed space taxonomies, usage constraints, safety requirements, reservation eligibility, capacity method, access rules, amenities, compliance attributes, and lifecycle states. Use taxonomy rules in reservations, moves, and capacity planning.

### 5. Occupancy Plan Versioning and Scenario Control

**Justification:** Occupancy plans change during reorganizations, hybrid work shifts, renovations, mergers, and lease decisions. Planners need versions and scenarios, not one mutable plan.

**Improvement:** Expand `create_occupancy_plan` with plan versions, baseline, scenario assumptions, target utilization, department allocations, effective dates, approval status, freeze windows, and rollback. Compare current, approved, and proposed occupancy states in the workbench.

### 6. Occupant Assignment Governance

**Justification:** Assigning people or teams to space depends on role, department, accessibility needs, hybrid pattern, security, adjacency, equipment, and capacity. Poor assignments create safety and productivity issues.

**Improvement:** Upgrade `assign_occupant` with assignment type, occupant source projection, department, work pattern, required equipment, accessibility needs, security clearance, adjacency requirements, start/end dates, and approval evidence. Validate capacity and access constraints before assignment.

### 7. Hybrid Work Pattern Modeling

**Justification:** Modern occupancy is probabilistic: workers use spaces by schedule, team rituals, remote days, travel, and peak attendance. Static seat counts do not model real demand.

**Improvement:** Add hybrid work patterns for teams and occupants, including anchor days, visit frequency, booking preferences, peak windows, and team collocation needs. Feed patterns into demand forecasts, reservations, and capacity plans without mutating HR records.

### 8. Space Reservation Eligibility Engine

**Justification:** A reservation should respect space type, capacity, setup, equipment, access, safety, maintenance blocks, privacy, neighborhood rules, and policy. Simple calendar availability is not enough.

**Improvement:** Upgrade `reserve_space` with eligibility checks for capacity, requester role, attendee count, equipment, accessibility, maintenance blocks, access constraints, booking horizon, catering/setup buffers, and conflict policies. Explain blocked reservations in the UI and agent.

### 9. Reservation Conflict Optimization

**Justification:** Reservation conflicts are not binary. Teams need alternatives, swaps, priority rules, split bookings, equipment substitutions, and setup-time optimization.

**Improvement:** Add conflict optimization that recommends alternate spaces, times, layouts, nearby rooms, split rooms, equipment moves, and priority-based conflict resolution. Store tradeoffs and required approvals before modifying reservations.

### 10. Meeting Room Setup and Service Dependencies

**Justification:** Many spaces require setup, cleaning, AV checks, catering, security, or maintenance before use. Reservations must orchestrate those dependencies.

**Improvement:** Add setup requirements, service tasks, setup/teardown buffers, provider assignments, readiness checks, and completion evidence. Prevent reservations from becoming confirmed when dependent setup tasks are incomplete.

### 11. Hot Desk and Neighborhood Management

**Justification:** Hoteling requires desk pools, neighborhoods, amenities, quiet zones, team proximity, check-in windows, release rules, and no-show handling.

**Improvement:** Add hot-desk pools, neighborhoods, desk features, booking rules, auto-release on no-show, desk check-in evidence, team adjacency preferences, and utilization feedback. Provide a desk-finder UI with policy-aware recommendations.

### 12. Occupancy Sensing and Observation Confidence

**Justification:** Utilization observations may come from badge data, Wi-Fi, sensors, reservations, manual counts, or check-ins, each with accuracy and privacy constraints.

**Improvement:** Expand `observe_utilization` with observation source, confidence, sampling method, privacy basis, time window, occupancy estimate, sensor health, and reconciliation against reservations and assignments. Show confidence intervals in utilization analytics.

### 13. Privacy-Safe Workplace Analytics

**Justification:** Occupancy and utilization data can reveal employee movement and behavior. Facilities analytics must be privacy-preserving and purpose-limited.

**Improvement:** Add aggregation thresholds, anonymization policies, retention periods, consent/projection basis, role-based masking, and forbidden drilldowns. Reject utilization views that expose individuals beyond configured policy.

### 14. Space Availability Snapshot Semantics

**Justification:** Availability depends on reservation, occupancy, maintenance, safety, access, capacity, setup, and policy status. A simple available flag is misleading.

**Improvement:** Upgrade `publish_availability_snapshot` with availability reason, blocked intervals, confidence, source records, capacity remaining, maintenance state, safety state, access constraints, and reservation eligibility. Emit snapshots when material availability changes.

### 15. Maintenance-Aware Space Blocking

**Justification:** Maintenance work can make spaces unavailable, partially usable, noisy, unsafe, or restricted. Facilities planning must reflect maintenance state.

**Improvement:** Expand `record_maintenance_signal` with affected spaces, severity, expected duration, usable capacity, noise/odor/access impact, safety impact, required buffers, and release criteria. Integrate work-order completion events through declared projections.

### 16. Move Request Lifecycle

**Justification:** Moves involve approvals, source/destination readiness, equipment, IT, access, furniture, labels, movers, downtime, and occupant communication. Generic requests do not cover move logistics.

**Improvement:** Upgrade `open_move_request` with move type, affected occupants, source/destination spaces, approval routing, move date, dependencies, risk, communication plan, and readiness checklist. Show move impact on capacity and reservations.

### 17. Move Task Dependency Orchestration

**Justification:** Move tasks need sequencing across packing, IT setup, access provisioning, furniture, cleaning, signage, and occupant confirmation. Out-of-order tasks disrupt work.

**Improvement:** Expand `complete_move_task` with dependency graph, task role, due date, evidence, blocker, handoff, confirmation, and rollback. Prevent move completion while critical dependent tasks remain open.

### 18. Access Constraint Governance

**Justification:** Spaces can be restricted by security clearance, visitor rules, lab safety, privacy, tenant boundaries, union rules, emergency status, or temporary incidents. Access must be explicit.

**Improvement:** Upgrade `define_access_constraint` with constraint type, affected spaces, allowed roles, effective window, reason, policy basis, emergency override, and access-system projection. Apply constraints to reservations, assignments, and wayfinding.

### 19. Visitor and Guest Space Controls

**Justification:** Visitor use of rooms, desks, lobbies, labs, and secure spaces creates security, safety, and capacity requirements. Facilities systems need visitor-aware space logic.

**Improvement:** Add visitor eligibility rules, escort requirements, visitor capacity, check-in dependencies, badge prerequisites, confidentiality restrictions, and guest-host linkage. Surface visitor constraints during reservation and event planning.

### 20. Safety Inspection Program

**Justification:** Facilities safety includes fire exits, occupancy limits, equipment, labs, ergonomics, environmental conditions, hazards, and regulatory inspections. One safety status is too weak.

**Improvement:** Expand `record_safety_inspection` with inspection type, checklist, inspector, hazard severity, affected spaces, required remediation, recurrence, due dates, and evidence attachments. Block spaces when safety findings exceed policy thresholds.

### 21. Hazard and Incident Linkage

**Justification:** Safety incidents and hazards should update space availability, risk posture, maintenance blocks, and capacity. Without linkage, unsafe spaces can remain reservable.

**Improvement:** Add hazard records tied to spaces, floors, inspections, maintenance signals, and incident projections. Trigger access restrictions, reservation cancellations, remediation tasks, and safety reinspection requirements.

### 22. Capacity Plan Demand Forecasting

**Justification:** Facilities teams need forecasts for seat demand, meeting room demand, specialty space demand, hybrid peaks, growth, contractions, and relocation plans.

**Improvement:** Upgrade `build_capacity_plan` and `simulate_space_demand` with demand drivers, headcount projections, hybrid patterns, reservation trends, utilization observations, occupancy targets, and scenario assumptions. Compare capacity shortfalls and surplus by site, floor, department, and space type.

### 23. Workplace Utilization Heatmaps

**Justification:** Utilization analytics should reveal underused spaces, crowding, peak patterns, no-show behavior, and mismatch between assigned and actual use.

**Improvement:** Build heatmaps by site, floor, zone, room, desk pool, space type, day, and hour using privacy-safe observations. Show confidence, observation source, and recommendations for redesign or policy changes.

### 24. Space Demand Scenario Simulation

**Justification:** Leaders need to test office attendance mandates, lease exits, renovations, hiring plans, and team relocations before disrupting people.

**Improvement:** Add scenario simulations for attendance policies, department moves, site closures, lease changes, renovation phases, and emergency closures. Show impacts on utilization, capacity, commute, reservations, safety, and cost.

### 25. Lease and Cost Context Projections

**Justification:** Space decisions depend on leases, rent, options, service charges, expirations, and cost allocation, but the facilities PBC should not own contract or finance tables.

**Improvement:** Add lease and cost projections with source, freshness, allowed fields, cost per area, expiration, options, restrictions, and chargeback context. Use them in capacity planning and executive dashboards.

### 26. Space Chargeback and Allocation Evidence

**Justification:** Departments often pay for assigned, occupied, or consumed space. Chargeback needs defensible allocation rules and evidence.

**Improvement:** Add allocation snapshots for department, cost center projection, space, area, utilization basis, time period, and rule version. Publish finance handoff events without mutating finance records.

### 27. Accessibility and Inclusive Workplace Controls

**Justification:** Space management must support accessibility, ergonomic needs, wellness rooms, quiet rooms, lactation rooms, accessible paths, and accommodation requirements.

**Improvement:** Add accessibility attributes, accommodation constraints, accessible route mapping, privacy controls, and reservation filters. Prevent moves or assignments that violate recorded accessibility requirements.

### 28. Environmental Comfort and Indoor Quality Signals

**Justification:** Temperature, humidity, air quality, noise, light, and crowding affect workplace performance and safety. Facilities decisions need environmental context.

**Improvement:** Add environmental observations with source, time window, thresholds, affected spaces, comfort score, and remediation link. Use environmental signals in space recommendations, incidents, and maintenance blocks.

### 29. Energy and Carbon-Aware Space Operations

**Justification:** Space utilization affects heating, cooling, lighting, cleaning, and emissions. Facilities optimization should include energy and carbon outcomes.

**Improvement:** Add energy/carbon estimates by site, floor, zone, and utilization scenario. Recommend consolidation, closure days, HVAC scheduling, and reservation clustering with tradeoffs against employee experience.

### 30. Emergency Preparedness and Muster Zones

**Justification:** Facilities systems must support evacuations, shelter-in-place, muster points, emergency capacity, blocked exits, and safety communications.

**Improvement:** Add emergency zones, muster areas, route constraints, floor wardens, capacity limits, emergency contacts, and drill evidence. Link safety inspections and access constraints to emergency readiness.

### 31. Wayfinding and Occupant Experience

**Justification:** Large facilities need routes to rooms, desks, amenities, exits, and accessible paths. Poor wayfinding wastes time and creates accessibility issues.

**Improvement:** Add wayfinding graph data for spaces, paths, elevators, stairs, entrances, amenities, and accessible routes. Generate directions that respect access constraints and temporary closures.

### 32. Amenities and Service Level Management

**Justification:** Amenities such as parking, lockers, cafes, AV, quiet rooms, and wellness spaces affect reservation choice and occupancy satisfaction.

**Improvement:** Add amenity records with capacity, location, availability, service hours, restrictions, support owner, and incident state. Use amenities in space discovery, reservations, and workplace recommendations.

### 33. Cleaning and Turnover Scheduling

**Justification:** High-use spaces require cleaning, reset, inspection, and readiness windows. Reservations and utilization must account for turnover.

**Improvement:** Add cleaning policies, turnover buffers, cleaning task evidence, high-use triggers, post-event cleaning, and readiness status. Block back-to-back bookings when turnover requirements are unmet.

### 34. Event and Large Gathering Planning

**Justification:** Large meetings and events require rooms, overflow, safety capacity, catering, security, AV, setup, signage, and visitor handling.

**Improvement:** Add event planning records that coordinate multiple spaces, setup tasks, service dependencies, attendee capacity, visitor rules, emergency capacity, and approval workflows.

### 35. Renovation and Construction Phasing

**Justification:** Renovations disrupt occupancy, reservations, safety, access, and maintenance. Phased plans need space-level impacts and temporary moves.

**Improvement:** Add renovation phases, affected spaces, closure windows, temporary assignments, safety constraints, noise impacts, contractor access, and communication plans. Simulate occupancy and reservation impacts before approval.

### 36. Facility Exception Workflow

**Justification:** Facilities teams regularly handle exceptions: over-capacity events, restricted-space access, safety waivers, emergency reservations, move accelerations, and maintenance overrides.

**Improvement:** Upgrade `resolve_facility_exception` with exception type, scope, approver authority, expiry, compensating controls, affected spaces, user impact, and closure evidence.

### 37. Reservation No-Show and Release Optimization

**Justification:** No-shows waste scarce spaces and distort utilization. Policies need evidence and fair enforcement.

**Improvement:** Add check-in tracking, no-show detection, grace periods, auto-release, repeated no-show patterns, notification, and exception handling. Feed no-show signals into reservation recommendations and policy tuning.

### 38. Neighborhood and Team Adjacency Planning

**Justification:** Workplace design depends on team adjacency, collaboration needs, noise compatibility, security, and shared equipment. Random assignments degrade productivity.

**Improvement:** Add adjacency requirements, team neighborhoods, compatibility rules, collaboration frequency, quiet/noisy zones, and scenario scoring. Use them in occupancy plans and moves.

### 39. Space Search and Recommendation Engine

**Justification:** Users need to find suitable spaces by purpose, capacity, equipment, location, accessibility, privacy, availability, and policy constraints.

**Improvement:** Add search ranking and recommendations for rooms, desks, neighborhoods, and specialty spaces based on intent, attendees, amenities, access eligibility, distance, utilization, and setup needs.

### 40. Agent-Assisted Facility Document Intake

**Justification:** Facilities teams receive floor plans, lease abstracts, move sheets, safety reports, maintenance notes, occupancy spreadsheets, and employee requests that need structured updates.

**Improvement:** Give the PBC agent skills to parse documents into proposed sites, floors, spaces, reservations, move tasks, maintenance blocks, access constraints, safety findings, and capacity plans. Require source citations, confidence, affected tables, event plans, and human confirmation.

### 41. Floor Plan Change Impact Analysis

**Justification:** Changing a floor plan affects spaces, reservations, assignments, wayfinding, safety exits, access constraints, utilization history, and capacity.

**Improvement:** Add impact analysis for map and space changes showing affected reservations, occupants, safety zones, moves, maintenance, and reporting. Require approval for material plan changes.

### 42. Portfolio Rationalization and Lease Decision Support

**Justification:** Facilities leaders need to decide whether to renew, exit, consolidate, expand, or redesign sites based on utilization, cost, demand, safety, and employee experience.

**Improvement:** Add portfolio decision models combining capacity, utilization, cost projections, lease dates, commute impact, amenities, safety, and carbon. Generate scenario comparisons and executive recommendations.

### 43. Maintenance Dependency Boundary Proofs

**Justification:** Facilities and maintenance overlap, but facilities should not mutate maintenance work orders. Availability still needs maintenance awareness.

**Improvement:** Define projection contracts for maintenance signals and work-order completions, including affected spaces, downtime, readiness, freshness, and fallback. Add tests proving facilities services mutate only `facilities_space_management_` tables.

### 44. Access Policy Boundary Proofs

**Justification:** Access controls may be owned by identity or security PBCs, while facilities owns spatial constraints. Composition must be explicit.

**Improvement:** Add access policy projections with allowed fields, source PBC, effective date, freshness, and emergency override semantics. Ensure reservations and wayfinding use projections without shared-table mutation.

### 45. Workplace Experience Feedback Loop

**Justification:** Utilization data alone misses employee sentiment about noise, comfort, amenities, safety, and productivity.

**Improvement:** Add workplace feedback records tied to spaces, reservations, floors, amenities, and issues. Analyze themes, severity, and recurrence, then feed recommendations into space planning and maintenance blocks.

### 46. Facility Policy and Parameter Studio

**Justification:** Reservation horizons, occupancy buffers, move SLAs, utilization thresholds, safety review windows, and access policies vary by site and evolve.

**Improvement:** Expand `compile_facility_rule` into a policy studio with versioning, simulations, approvals, effective dates, rollback, test cases, and impact analysis on reservations, assignments, moves, and capacity plans.

### 47. Time-Travel Space and Occupancy Reconstruction

**Justification:** Auditors, planners, and investigators may need to know who was assigned, what was reservable, which constraints applied, and what safety status existed at a past time.

**Improvement:** Add temporal reconstruction for space records, reservations, occupancy assignments, access constraints, safety inspections, maintenance blocks, and availability snapshots across transaction time and effective time.

### 48. Facilities Release Evidence Packs

**Justification:** Generated facilities capabilities must prove schemas, services, events, handlers, rules, UI, agent skills, and boundary contracts before users rely on space decisions.

**Improvement:** Generate release evidence packs with schema hashes, migration manifests, service contracts, event schemas, idempotent handler proofs, retry/dead-letter tests, reservation simulations, safety gates, UI coverage, and agent skill manifests.

### 49. Dead-Letter and Replay Operations for Space Events

**Justification:** Employee, maintenance, access, lease, and policy events can arrive late, duplicate, or malformed. Facilities decisions must remain safe under event failure.

**Improvement:** Add operational views for inbox, outbox, retry, quarantine, dead-letter events, payload lineage, idempotency keys, and replay. Unknown events should be visible but unable to mutate facility state.

### 50. Complete Facilities Workbench Coverage

**Justification:** Facilities managers, space planners, move coordinators, safety reviewers, employees, executives, and workplace analysts need full operational surfaces. Hidden APIs are not enough.

**Improvement:** Expand the UI into role-specific workbenches for facility manager, space planner, employee, move coordinator, safety reviewer, maintenance liaison, workplace analyst, and executive sponsor. Cover sites, floors, maps, spaces, reservations, occupancy, moves, maintenance blocks, access constraints, safety, utilization, capacity, scenarios, policies, agent panels, and release evidence.
