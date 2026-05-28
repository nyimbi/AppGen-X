# Sports Venue Event Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key from `manifest.py`: `sports_venue_event_operations`.
- Current description: venue events, seating, concessions, security, staffing, fan experience, and event operations.
- Current owned tables: `venue_event`, `seating_manifest`, `concession_plan`, `security_post`, `event_staff`, `fan_issue`, `event_settlement`, `sports_venue_event_operations_policy_rule`, `sports_venue_event_operations_runtime_parameter`, `sports_venue_event_operations_schema_extension`, `sports_venue_event_operations_control_assertion`, `sports_venue_event_operations_governed_model`.
- Current APIs: `POST /venue-events`, `POST /seating-manifests`, `POST /concession-plans`, `POST /security-posts`, `POST /event-staffs`, `GET /sports-venue-event-operations-workbench`.
- Current emitted events: `SportsVenueEventOperationsCreated`, `SportsVenueEventOperationsUpdated`, `SportsVenueEventOperationsApproved`, `SportsVenueEventOperationsExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current UI fragments: `SportsVenueEventOperationsWorkbench`, `SportsVenueEventOperationsDetail`, `SportsVenueEventOperationsAssistantPanel`.
- Current workflows: `sports_venue_event_operations_create_venue_event_workflow` and `sports_venue_event_operations_record_seating_manifest_workflow`.
- Current release evidence hooks: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Event Master Calendar With Venue Hold Hierarchy
**Justification:** The package has a `venue_event` table, but venue operations need one authoritative event calendar that separates tentative holds, confirmed games, concerts, community bookings, maintenance blocks, and dark days.

**Improvement:** Expand `venue_event` into a calendar model with event type, promoter or home-team ownership, priority rank, venue-space scope, hard hold versus soft hold, rehearsals, load-in, load-out, and cancellation lineage so the workbench can answer what owns the building at any moment.

**Acceptance evidence:** Calendar fixtures covering same-day doubleheaders and mixed-use venue conflicts, API examples for create and reschedule flows, and a workbench timeline view showing hold precedence and release of stale holds.

### 2. Blackout, Changeover, and Curfew Windows
**Justification:** A venue cannot book or activate operations solely on event start and end times; field conversion windows, noise curfews, and local authority restrictions determine what is operationally possible.

**Improvement:** Add blackout and changeover windows to `venue_event`, including minimum turnover buffers, local curfew cutoffs, mandatory crew rest periods, and venue-specific shutdown windows that block unsafe or impossible scheduling.

**Acceptance evidence:** Validation rules that reject back-to-back bookings without required turnover, scenario tests for overtime games that run into curfew, and workbench warnings when changeover buffers collapse below policy.

### 3. Competition Schedule Conflict Detection
**Justification:** Sports calendars move constantly because of league flexing, television requests, weather makeups, and cup competitions, so the PBC needs conflict logic beyond a single date field.

**Improvement:** Add schedule-conflict detection for home-team obligations, tournament windows, make-up dates, broadcast exclusivity windows, and shared-campus venue dependencies, with operator tools to compare alternative dates before approving changes.

**Acceptance evidence:** Conflict matrices for league, cup, and concert overlaps, simulation outputs for rescheduling options, and emitted exception evidence when a requested date violates a protected competition or venue rule.

### 4. Seating Manifest Ownership Boundary
**Justification:** The `seating_manifest` table should own day-of-event seat usability and operational restrictions, not the full commercial ticket ledger, or the PBC will blur a critical system boundary.

**Improvement:** Define `seating_manifest` as the operational boundary for seat kills, obstructed-view declarations, accessible-seat availability, camera-platform holds, team holds, comp blocks, and safety closures while treating price books, payment state, and fan account balances as external dependencies.

**Acceptance evidence:** Boundary notes in the specification, contract tests that reject payment-only fields from seating APIs, and workbench views that show operational seat state without pretending to own ticket commerce.

### 5. Seat Hold, Kill, and Release Workflow
**Justification:** Venue operations constantly move seats in and out of sale for staging, broadcast platforms, sponsor builds, drape kills, and late production changes.

**Improvement:** Add a governed workflow for hold creation, temporary seat kill, partial release, and final release with reason codes, owner, deadline, approval threshold, and downstream notification so seating decisions stop living in spreadsheets and chat threads.

**Acceptance evidence:** Audit-ready hold histories by section-row-seat range, tests for overlapping hold logic, and release evidence proving that late production changes flowed from request through approval to manifest projection.

### 6. Accessible Seating and Companion Seat Controls
**Justification:** Accessible inventory is an operational and compliance issue, not only a ticketing concern, because relocations, sightline obstructions, and companion-seat rules change during event setup.

**Improvement:** Add accessible-seat classifications, companion-seat pairing rules, temporary obstruction checks, relocation workflows, and required supervisor acknowledgment whenever operational changes reduce or move accessible inventory.

**Acceptance evidence:** Fixtures for relocation scenarios, rule tests for companion-seat integrity, UI indicators for accessibility-impacting changes, and release evidence showing who approved any reduction in accessible seating.

### 7. Ingress Gate Zoning and Opening Plans
**Justification:** Day-of-event readiness depends on a controlled ingress plan by gate, plaza, parking lot, fan type, and opening wave rather than a single venue-open timestamp.

**Improvement:** Model ingress zones with gate assignment, open time, expected scan rate, queue storage capacity, ticket or credential population served, bag policy, magnetometer requirement, and fallback gate routing inside `security_post` and `venue_event` planning surfaces.

**Acceptance evidence:** Gate-opening plans for a normal event and a high-security event, queue-capacity calculations, and workbench maps that show which gates serve premium guests, general admission, staff, media, and teams.

### 8. Egress Route Clearance and Phased Release
**Justification:** Safe egress requires a plan for exit paths, staged lot releases, transit coordination, and crowd dispersal after the final whistle or encore.

**Improvement:** Add egress routing, choke-point monitoring, stair and concourse clearance checks, rideshare pickup zoning, bus dispatch windows, and phased release triggers tied to event type and crowd profile.

**Acceptance evidence:** Egress playbooks for sold-out and partial-capacity events, simulation evidence for blocked-route scenarios, and incident-response links showing how operations switch to alternate egress routes when a path is compromised.

### 9. Gate Operations Versus Security Boundary
**Justification:** The current `security_post` surface risks mixing screening policy with frontline gate throughput tasks, which causes ownership confusion during event load.

**Improvement:** Separate gate-operations responsibilities from security responsibilities by recording who owns ticket scanning, bag check, wanding, credential verification, ADA access handling, and queue management, while keeping the PBC clear about which tasks escalate to security command.

**Acceptance evidence:** Responsibility matrices in the backlog and specification, workflow approvals that require both operations and security sign-off where duties overlap, and queue records that show the owning team for each gate action.

### 10. Credential Taxonomy and Issuance Workflow
**Justification:** Credentials are central to sports venue access control, and loose badge handling produces unsafe access, delayed arrivals, and untraceable backstage movement.

**Improvement:** Introduce a credential model for full-season, single-event, media, broadcast, team, league, vendor, premium service, medical, and emergency credentials with zone access, time windows, escort requirements, and revocation status.

**Acceptance evidence:** Credential templates by event type, issuance and revocation test cases, and workbench views showing which credential classes can enter field level, locker rooms, production areas, kitchens, suites, and command post spaces.

### 11. Credential Scan Trails and Back-of-House Access Windows
**Justification:** Issuing credentials is not enough; the venue needs event-day evidence of who entered sensitive zones and whether access occurred inside approved windows.

**Improvement:** Record credential scan events with gate or portal location, zone entered, timestamp, exception reason, escort linkage, and access-window validation for locker rooms, tunnels, media workrooms, control rooms, and premium service corridors.

**Acceptance evidence:** Scan-ledger examples for team arrival, media setup, and vendor access, tests for expired or zone-mismatched credentials, and incident evidence showing how access anomalies appear in the workbench.

### 12. Staffing Boundary and Role Matrix
**Justification:** The `event_staff` table should own event-day staffing plans and readiness, not payroll, labor contracts, or enterprise HR master data.

**Improvement:** Define `event_staff` as the boundary for event role assignment, post assignment, shift timing, certification status, attendance, and relief coverage while treating recruiting, pay rates, and employee master records as external systems.

**Acceptance evidence:** Boundary documentation in `SPECIFICATION.md`, rejected payload tests for HR-only fields, and workbench role matrices covering ushers, supervisors, conversion crew, security, cleaners, EMTs, guest services, parking, and suite attendants.

### 13. Shift Rostering, Breaks, and Call-Off Replacement
**Justification:** Day-of-event staffing breaks down when replacement logic lives outside the operating system and supervisors cannot see who is missing or overworked.

**Improvement:** Add rostering for check-in, no-show flags, break windows, relief assignments, standby pools, and rapid reassignment so the PBC can absorb call-offs without losing gate coverage, field coverage, or premium service coverage.

**Acceptance evidence:** Tests for minimum staffing thresholds by zone, workbench alerts for uncovered posts, and operator evidence showing replacement sourcing from standby or mutual-aid pools.

### 14. Volunteer, Temp, and Contractor Onboarding Readiness
**Justification:** Many venues rely on temporary staff on event day, and missing onboarding proof creates avoidable security and safety gaps.

**Improvement:** Add onboarding readiness checks for ID verification, orientation completion, venue rules acknowledgment, uniform pickup, device issuance, and required training before a temporary worker can be marked deployable.

**Acceptance evidence:** Readiness checklists by worker type, blocked-assignment tests for incomplete onboarding, and release evidence showing onboarding completion rates before gates open.

### 15. Concessions Planning Boundary
**Justification:** The `concession_plan` surface should own event-specific operating plans without turning into a full inventory, accounting, or procurement system.

**Improvement:** Define `concession_plan` as the boundary for stand activation, menu selection, expected demand, labor requirement, service hours, alcohol controls, mobile-order eligibility, and restock triggers while leaving supplier invoices, warehouse accounting, and corporate recipe costing external.

**Acceptance evidence:** Specification language for the owned boundary, rejected-field tests for procurement and finance-only data, and workbench planning views that show stands, kiosks, hawkers, clubs, and suite pantry readiness.

### 16. Replenishment, Stand Outage, and Degrade Mode Handling
**Justification:** Sales plans fail during high-volume events if there is no controlled response to stockouts, cooler failures, POS degradation, or cart outages.

**Improvement:** Add replenishment runs, outage tracking, fallback menus, card-only versus cash-only modes, and cart or stand closure workflows with rerouting advice for nearby demand capture.

**Acceptance evidence:** Stockout incident fixtures, stand outage workflows linked to `fan_issue` and `concession_plan`, and dashboards showing mean time to replenish, reroute, or close a location safely.

### 17. Alcohol Service and Last-Call Controls
**Justification:** Alcohol operations sit at the intersection of concessions, security, and event policy, so they need explicit controls and evidence.

**Improvement:** Encode venue- and event-specific alcohol cutoffs, section restrictions, ID-check escalation, intoxication incident linkage, and management override reasons so the PBC can prove why service continued or stopped.

**Acceptance evidence:** Rule tests for last-call timing by sport and event type, incident examples that lock a stand out of alcohol service, and release evidence showing approved exceptions to the normal cutoff.

### 18. Crowd Density Telemetry and Section Risk Monitoring
**Justification:** Crowd safety depends on live section-level awareness, not only pre-event capacity assumptions.

**Improvement:** Add crowd-density inputs by gate, concourse, club, vomitory, standing room zone, and premium lounge with thresholds for congestion, reverse-flow risk, and intervention triggers tied to `security_post` and `fan_issue`.

**Acceptance evidence:** Threshold tables by venue area, alert tests for over-density, and workbench heat-map views that show escalating risk before a crush or block occurs.

### 19. Fan Issue Taxonomy and Dispatch Workflow
**Justification:** The `fan_issue` table can become a powerful operations signal if it distinguishes seat complaints from medical requests, lost-child cases, disruptive behavior, and access barriers.

**Improvement:** Expand `fan_issue` into a dispatchable taxonomy with severity, location precision, affected parties, required response team, service-level target, and closure proof so guest services and security can work from the same record.

**Acceptance evidence:** Taxonomy fixtures for medical, behavioral, ADA, seat, parking, and restroom issues, dispatch routing tests, and closeout evidence showing response time and disposition by category.

### 20. Incident Command Workflow and Command Post Log
**Justification:** Major incidents require one command timeline that survives shift change, radio traffic, and later review.

**Improvement:** Add an incident command workflow with incident level, commander, scribe, active objectives, resource requests, agency notifications, decision log, and current status board surfaced directly in the workbench.

**Acceptance evidence:** Command-post timeline examples for severe weather and crowd fights, immutable log entries with actor identity, and after-action exports that reconstruct incident decisions minute by minute.

### 21. Medical Response, AED, and Ambulance Routing
**Justification:** Medical response readiness is a core venue-ops responsibility and should not be hidden inside generic issue records.

**Improvement:** Track first-aid rooms, roving medics, AED locations, stretcher routes, ambulance ingress points, hospital destination preferences, and medical escalation timing as explicit operational objects linked to each event.

**Acceptance evidence:** Route maps for field, bowl, suite, and parking incidents, tests for dispatcher recommendations by location, and incident-response evidence showing handoff from venue staff to EMS.

### 22. Evacuation, Shelter-in-Place, and Family Reunification
**Justification:** Different hazards require materially different crowd instructions and venue movement plans.

**Improvement:** Add playbooks for full evacuation, partial evacuation, shelter-in-place, weather sheltering, and post-incident reunification with predefined zones, message templates, and authority requirements for activation.

**Acceptance evidence:** Drill scenarios for lightning, smoke, suspicious package, and structural failure, command approvals captured in audit history, and workbench evidence proving which playbook was activated and when.

### 23. Field or Court Readiness Checklist and Sign-Off
**Justification:** The package description mentions event operations, and the event cannot open safely without a controlled readiness decision for the playing surface and competition environment.

**Improvement:** Add field or court readiness tasks for surface condition, markings, goals or hoops, protective netting, bench setup, official review, locker room turnover, and emergency equipment placement with role-based sign-off.

**Acceptance evidence:** Sport-specific readiness templates, blocked-go-live tests when a required sign-off is missing, and event timelines showing readiness completion before team warmups.

### 24. Event Changeover Turnaround Between Tenants and Event Types
**Justification:** Mixed-use venues swing between sports, concerts, festivals, and private events, and changeover is often the highest-risk operating period.

**Improvement:** Model changeover phases for de-rig, clean, seat reconfiguration, stage load, branding swap, and field protection installation, with task dependencies and no-go conditions before the next event can move from hold to approved.

**Acceptance evidence:** Turnaround plans for sport-to-concert and concert-to-sport conversions, critical path tests, and progress views showing where a late contractor threatens the next event's opening timeline.

### 25. Venue Systems Readiness: Scoreboard, PA, Lights, and Comms
**Justification:** Broadcast, officiating, crowd communication, and emergency response all depend on venue systems being checked and recoverable.

**Improvement:** Add readiness checks and outage workflows for scoreboards, ribbon boards, public address, house lights, backup power, coach-to-booth comms, radio channels, and replay systems with explicit fallback procedures.

**Acceptance evidence:** Pre-event checklists, degraded-mode decision trees, and incident logs proving that an outage triggered the correct fallback and escalation path.

### 26. Broadcast Compound Scheduling and Truck Access
**Justification:** Broadcast operations compete for loading docks, parking, power, cable paths, and compound space, making them a first-class event-ops concern.

**Improvement:** Add broadcast compound reservations, truck arrival windows, dock assignments, power requirements, cable-route approvals, camera position holds, and strike deadlines linked to the master calendar and seating manifest.

**Acceptance evidence:** Compound plans for home games and one-off events, conflict tests with vendor load-in, and seat-hold evidence for camera platforms and obstructed-view adjustments.

### 27. Run-of-Show and Broadcast Break Coordination
**Justification:** Sports venues synchronize game operations, entertainment, sponsorship activations, and broadcast timing, so the PBC needs a shared run-of-show surface.

**Improvement:** Add run-of-show segments for anthem, introductions, halftime, timeout entertainment, trophy presentation, sponsor reads, and broadcast windows with owner, target duration, and contingency branch.

**Acceptance evidence:** Timeline views with locked and flexible segments, variance reports for overrun scenarios, and cross-team sign-off showing operations, broadcast, and in-house entertainment aligned on the same plan.

### 28. VIP and Suite Entitlement Boundary
**Justification:** Premium operations need strong boundaries because guest entitlements, dining preferences, and access rights are operationally sensitive.

**Improvement:** Define the PBC boundary for suites and VIP operations around event-day access, delivery timing, catering readiness, host contacts, amenities, and incident handling while leaving contract pricing and long-term billing outside the package.

**Acceptance evidence:** Boundary notes in the backlog and specification, API validation rejecting billing-only fields, and workbench premium dashboards showing suite readiness without exposing contract-accounting data.

### 29. Premium Arrival and Suite Service Workflow
**Justification:** High-value guests experience the venue through parking, dedicated entry, elevator routing, suite stocking, and in-seat or in-suite service timing.

**Improvement:** Add premium guest workflows for arrival windows, dedicated screening, escort requirements, suite stocking deadlines, hospitality handoff, service call routing, and end-of-night closeout.

**Acceptance evidence:** Premium guest journey fixtures, service-response timing metrics, and operational evidence for a suite opening late, requiring escalation and host notification.

### 30. Parking, Rideshare, Team Bus, and Curbside Staging
**Justification:** Arrival and departure plans fail if transportation staging is tracked outside the event operating model.

**Improvement:** Add parking lot allocations, rideshare geofences, VIP curbside zones, team and official bus parking, media parking, and post-event traffic-release sequencing linked to ingress and egress plans.

**Acceptance evidence:** Lot and curb maps by event type, tests for conflicting vehicle allocations, and event dashboards that show transportation readiness before public gates open.

### 31. Weather Watch Model and Escalation Thresholds
**Justification:** Weather is one of the highest-frequency drivers of venue disruption, especially for open-air sports and mixed indoor-outdoor campuses.

**Improvement:** Add event-scoped weather monitoring for lightning radius, heat index, wind thresholds, heavy rain, snow or ice risk, and forecast confidence with distinct watch, warning, delay, and suspend states.

**Acceptance evidence:** Threshold tables by venue type, simulated weather-alert scenarios, and command-post evidence showing weather state transitions and who acknowledged them.

### 32. Lightning, Heat, Wind, and Rain Delay Procedures
**Justification:** Weather response is only safe when each hazard has a concrete procedure for players, officials, fans, staff, and premium spaces.

**Improvement:** Create hazard-specific procedures for lightning sheltering, heat mitigation, wind-borne object risk, rain delay field protection, and re-entry criteria, each tied to role assignments and public messaging plans.

**Acceptance evidence:** Playbooks for multiple hazard types, blocked-activation tests when a required role is unstaffed, and event logs proving how delay, suspension, and restart decisions were executed.

### 33. Weather-Driven Refund, Reschedule, and Settlement Evidence
**Justification:** Weather impacts flow into settlements, fan remediation, labor overruns, and sponsor obligations, so the PBC needs evidence that bridges operations to post-event outcomes.

**Improvement:** Link weather incidents to `event_settlement`, capturing delay duration, overtime labor, premium-service recovery, abandoned concessions, remediation commitments, and the trigger for any reschedule or cancellation decision.

**Acceptance evidence:** Settlement records for a delayed and a canceled event, variance reports attributed to weather, and release evidence showing the chain from weather alert through incident command to financial closeout.

### 34. Accessibility and Wayfinding Operations
**Justification:** Venue operations quality is visible in the path a guest can actually take, not only in what the ticket or event listing claims.

**Improvement:** Add wayfinding and accessibility checks for elevators, ramps, accessible parking paths, family entrances, sensory rooms, captioning support, and temporary closures so operators can redirect guests before friction becomes an incident.

**Acceptance evidence:** Venue path maps with alternate routes, issue-routing tests for inaccessible-path reports, and UI evidence highlighting temporary closures that affect accessibility commitments.

### 35. Day-of-Event Workbench Command UI
**Justification:** `SportsVenueEventOperationsWorkbench` should operate as a live command surface, not a passive CRUD page.

**Improvement:** Redesign the workbench around event status, countdown milestones, gate state, staffing gaps, field or court readiness, crowd alerts, concession outages, weather state, and active incidents with role-specific action buttons.

**Acceptance evidence:** UI contracts for operator, supervisor, security lead, and premium-services lead personas, screenshot-level evidence of the command layout, and route tests proving key actions are available only with the right permissions.

### 36. Mobile and Offline Supervisor UI
**Justification:** Gate, parking, field, and concourse supervisors work away from desks, and connectivity can degrade precisely when the event load is highest.

**Improvement:** Add mobile-first views and offline-safe task flows for checklists, incident capture, staffing confirmations, and gate-state changes with queued sync and conflict resolution when connectivity returns.

**Acceptance evidence:** Offline interaction tests, sync-conflict fixtures, and supervisor UI evidence showing that critical tasks remain usable from handheld devices during degraded connectivity.

### 37. Assistant Skill for Document Intake and Ops Order Parsing
**Justification:** Venue operations receive event riders, game-day memos, security plans, vendor load sheets, and broadcast requests that contain structured obligations hidden in documents.

**Improvement:** Add an assistant skill in `SportsVenueEventOperationsAssistantPanel` that parses ops orders, extracts dates, spaces, staffing asks, seat holds, credential requests, weather contingencies, and catering instructions into governed drafts for operator review.

**Acceptance evidence:** Source-span extraction examples from sample ops documents, review screens that show before-commit diffs, and tests proving the skill cannot mutate records without explicit confirmation.

### 38. Assistant Skill for Live Exception Triage
**Justification:** High-volume event days generate more exceptions than supervisors can triage manually, but any agent assistance must remain bounded and auditable.

**Improvement:** Add an assistant skill that summarizes open issues by severity, proposes the likely owner, recommends the next safe action, and groups duplicate reports across gates, stands, suites, and field readiness tasks.

**Acceptance evidence:** Prompt-to-action traces stored in audit history, acceptance tests for duplicate grouping and owner recommendation, and blocked-action evidence when the assistant proposes a step outside the user's permission scope.

### 39. Assistant Skill for Incident Summary and After-Action Drafting
**Justification:** After-action reporting is often delayed because incident notes are scattered across radios, chat, and handwritten logs.

**Improvement:** Add an assistant skill that compiles command-post logs, `fan_issue` closures, staffing gaps, weather milestones, and concession outages into a draft incident summary and lessons-learned pack without inventing missing facts.

**Acceptance evidence:** Draft reports with citations back to source records, hallucination-guard tests that require explicit unknown markers, and reviewer workflows showing what was accepted, edited, or rejected.

### 40. Domain Event Catalog for Day-of-Event Operations
**Justification:** The current emitted event list is too coarse to explain gate openings, field sign-offs, crowd alerts, and weather delays to downstream consumers.

**Improvement:** Expand the event catalog with operational events such as `VenueGateOpened`, `CredentialRevoked`, `CrowdDensityThresholdBreached`, `FieldReadinessApproved`, `WeatherDelayDeclared`, `SuiteServiceRecoveryStarted`, and `ConcessionStandOutageOpened`.

**Acceptance evidence:** Event schemas with examples, idempotency rules, and a mapping that shows which workbench action or workflow step emits each event and why a downstream consumer would rely on it.

### 41. Consumed-Event Contracts and Dependency Handling
**Justification:** The package already consumes `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`, but venue operations need clear reactions when policy or KPI context changes midstream.

**Improvement:** Define handler behavior for consumed events, including policy re-evaluation of active events, reopening of approval tasks when sealed audit evidence changes, and recalculation of readiness or risk indicators when new KPI inputs arrive.

**Acceptance evidence:** Handler contract tests for duplicate delivery and out-of-order delivery, visible workbench markers when an event was reopened by a dependency update, and dead-letter evidence for unprocessable inbound events.

### 42. Release Evidence Pack for Event Readiness
**Justification:** The manifest already points to `RELEASE_EVIDENCE.md`, and a venue-ops package should prove readiness the same way the venue proves it is safe to open.

**Improvement:** Build a release-evidence pack that bundles API contract results, workflow tests, UI captures, event schema snapshots, permission proofs, and domain scenario passes for weather, crowd, staffing, concessions, and field readiness.

**Acceptance evidence:** A repeatable release checklist linked to `RELEASE_EVIDENCE.md`, timestamped evidence artifacts for each critical domain scenario, and a clear pass or fail summary for approval.

### 43. Rehearsal, Tabletop, and Drill Evidence
**Justification:** Sports venue operations quality is proven through rehearsal as much as through static configuration.

**Improvement:** Add structured support for tabletop exercises, evacuation drills, medical drills, weather drills, and command-post rehearsals with scenario definition, participant roles, observed gaps, remediation owners, and closure tracking.

**Acceptance evidence:** Drill records attached to the relevant venue and event type, remediation tasks that feed back into the backlog, and readiness reports that distinguish planned capability from drilled capability.

### 44. Certification, License, and Training Expiry Controls
**Justification:** Certain posts require current credentials such as EMT certification, food-safety training, alcohol-service certification, forklift authorization, or radio-channel clearance.

**Improvement:** Add certification and expiry checks to `event_staff` and post assignment so the system blocks deployment of unqualified staff to first aid, premium food service, field conversion equipment, or command roles.

**Acceptance evidence:** Expiry fixtures across multiple certification types, blocked-assignment tests, and supervisor views showing which assignments are at risk due to expiring or missing qualifications.

### 45. Vendor Load-In and Load-Out Coordination
**Justification:** Event-day loading docks, service corridors, freight elevators, and compound space are shared choke points that often trigger schedule slip and safety issues.

**Improvement:** Add vendor load plans with arrival slots, dock assignments, freight paths, escort needs, credential prerequisites, and strike deadlines for stage vendors, caterers, merch, cleaners, and broadcast crews.

**Acceptance evidence:** Dock schedule conflict tests, escort-linked credential checks, and operational timelines that show late vendor arrival affecting changeover or opening readiness.

### 46. Team, Official, Performer, and Dignitary Arrival Itineraries
**Justification:** Not all event stakeholders arrive through the same path, and mistakes here create high-visibility breakdowns.

**Improvement:** Track protected arrival itineraries for teams, officials, performers, mascots, and dignitaries, including secure parking, tunnel or back-of-house routing, arrival windows, locker room or green room readiness, and escort ownership.

**Acceptance evidence:** Arrival-plan fixtures by stakeholder class, access-window checks against credential rules, and incident evidence for missed or compromised arrival plans.

### 47. Housekeeping, Restroom, and Waste-Service Readiness
**Justification:** Cleanliness, restroom availability, and waste removal directly affect crowd flow, fan experience, premium operations, and public-health compliance.

**Improvement:** Add pre-open and in-event readiness tasks for restroom checks, consumable replenishment, spill response, waste haul schedules, and post-event cleanup surge staffing, linked to specific zones and service-level targets.

**Acceptance evidence:** Zone-based cleanliness checklists, outage tickets for closed restrooms or missed waste pulls, and performance dashboards showing turnaround times during peak occupancy.

### 48. Post-Event Settlement, Variance Review, and Cost Attribution
**Justification:** `event_settlement` should close the loop between event execution and operational learning, not act as a final accounting stub.

**Improvement:** Expand `event_settlement` to capture staffing variance, overtime, concession outage loss, premium recovery spend, weather-related costs, damage claims, and incident-linked reimbursements so operations can see what the event actually cost to run.

**Acceptance evidence:** Settlement examples for routine and disrupted events, variance reports grouped by operating domain, and release evidence showing reconciliation from live event facts into post-event closeout.

### 49. Multi-Tenant and Confidentiality Isolation for Shared Venues
**Justification:** The manifest already calls out multi-tenant policy isolation, and shared venues must prevent promoters, teams, and premium clients from seeing one another's sensitive plans.

**Improvement:** Enforce tenant-aware isolation across event calendars, suite notes, credential classes, staffing views, and incident records with per-tenant policies for what can be shared, redacted, or entirely hidden in the UI and assistant flows.

**Acceptance evidence:** Cross-tenant negative tests, UI evidence showing redaction or absence of confidential records, and audit trails proving that an operator only saw the tenant-scoped view they were allowed to access.

### 50. Readiness Score, Approval Gate, and Go-Live Evidence
**Justification:** Operators need one defensible answer to whether the venue is ready to open gates, start the event, or continue after disruption.

**Improvement:** Create a composite readiness gate that rolls up event calendar confirmation, seat-manifest sign-off, ingress and egress readiness, staffing coverage, concessions readiness, crowd-safety posture, field or court sign-off, broadcast readiness, premium readiness, weather state, and unresolved critical incidents into one approval decision.

**Acceptance evidence:** A scored readiness model visible in `SportsVenueEventOperationsWorkbench`, hard-stop tests when a critical domain is red, and an approval artifact that can be attached to `RELEASE_EVIDENCE.md` for each production release and each event-opening decision.
