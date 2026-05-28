# Telecom Network Operations Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `telecom_network_operations`.
- Manifest description: network inventory, capacity, incidents, alarms, service assurance, maintenance windows, and SLA impact.
- Current owned tables: `network_element`, `capacity_segment`, `network_incident`, `alarm_event`, `service_assurance_case`, `maintenance_window`, and `sla_impact`.
- Current APIs: `POST /network-elements`, `POST /capacity-segments`, `POST /network-incidents`, `POST /alarm-events`, `POST /service-assurance-cases`, and `GET /telecom-network-operations-workbench`.
- Current event contract: emits `TelecomNetworkOperationsCreated`, `TelecomNetworkOperationsUpdated`, `TelecomNetworkOperationsApproved`, `TelecomNetworkOperationsExceptionOpened`; consumes `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Current UI surfaces: `TelecomNetworkOperationsWorkbench`, `TelecomNetworkOperationsDetail`, and `TelecomNetworkOperationsAssistantPanel`.
- Existing backlog signal: the package already points at inventory, capacity, incidents, alarms, service assurance, maintenance windows, SLA impact, analytics, governed AI, and release evidence, but it does not yet go deep on sites, cells, circuits, fiber, outages, planned work, and NOC operating detail.

### 1. Canonical site hierarchy and geospatial identity
**Justification:** The package cannot reason about outages, planned work, or field dispatch accurately until every record anchors to a site hierarchy that NOC and field teams actually use.
**Improvement:** Extend `network_element` so a site can own shelter, room, cabinet, rack, power plant, battery bank, generator, microwave node, rooftop, and fiber hut variants with canonical site codes, latitude/longitude, access restrictions, and parent-child geography.
**Acceptance evidence:** Schema and API contracts expose site hierarchy fields; workbench site pages roll alarms, trouble tickets, planned work, outages, and SLA impact up by site; seeded examples prove one incident can be traced from site to dependent cells and circuits.

### 2. Cell, sector, carrier, and radio identity model
**Justification:** Telecom operations run at cell and sector level for congestion, degradation, and customer impact, so generic assets are not enough.
**Improvement:** Add explicit models for BTS, NodeB, eNodeB, gNodeB, sector, carrier, band, PCI/PSC/BCCH, azimuth, tilt, transmit chain, and neighbor relations beneath `network_element`.
**Acceptance evidence:** Detail views show a site with its cells and sectors; KPI drill-down works from site to sector; acceptance fixtures prove alarms and trouble tickets can target a single cell without losing parent site context.

### 3. Circuit and service path topology
**Justification:** NOC operators need path-aware impact analysis before they can prioritize restoration or estimate SLA exposure.
**Improvement:** Use `capacity_segment` and related topology records to model logical circuits, A-end/Z-end endpoints, VLANs, pseudowires, leased lines, backhaul links, protection groups, and route diversity across microwave and fiber.
**Acceptance evidence:** Circuit queries show full path membership, protected versus unprotected state, and impacted services during a cut; seeded scenarios prove a failed segment can identify every affected circuit and SLA clock.

### 4. Fiber route, strand, and splice ownership
**Justification:** Fiber faults are resolved on the basis of route sections, closures, strands, and splice plans, not on abstract capacity rows.
**Improvement:** Deepen the package with fiber route, cable, sheath, tube, strand, closure, patch panel, handhole, and route-diversity metadata while keeping that physical plant inside the telecom inventory boundary.
**Acceptance evidence:** Topology screens trace a service over specific fiber segments and closures; outage evidence shows likely cut location candidates; field evidence links before/after splice validation to the affected route objects.

### 5. Alarm catalog normalization across vendors
**Justification:** Alarm floods remain unusable if vendor-specific names, severities, and probable causes are not normalized.
**Improvement:** Normalize `alarm_event` into a canonical alarm catalog with source vendor code, normalized alarm family, perceived severity, probable cause, object class, clear condition, and suppressibility flags.
**Acceptance evidence:** Alarm list pages display normalized family and severity alongside raw source values; duplicate vendor codes map to one canonical alarm; tests prove clear events close the correct normalized alarm instance.

### 6. Root-cause alarm correlation and suppression
**Justification:** A major outage can emit thousands of child alarms, and the NOC needs root cause rather than noise.
**Improvement:** Add correlation rules that collapse child alarms under transport loss, power loss, fiber cut, transmission failure, or controller failure parents while preserving the original event stream for audit.
**Acceptance evidence:** A simulated fiber cut produces one parent incident view with suppressed child counts; operators can expand suppressed alarms on demand; release evidence includes before/after alarm volume comparisons.

### 7. Trouble ticket ownership and boundary rules
**Justification:** Trouble tickets are central to telecom operations, but the package must be clear about what it owns versus what an external ITSM or workforce system owns.
**Improvement:** Make `service_assurance_case` the owned telecom trouble ticket record for network-originated issues, with mirrored external references, handoff state, severity, customer impact, and dispatch status without taking over non-telecom HR or billing workflows.
**Acceptance evidence:** Boundary notes in APIs and UI distinguish owned ticket fields from referenced external fields; seeded tickets show bi-directional linkage to alarms and outages; no write path crosses into non-owned workforce records.

### 8. Planned work and maintenance window depth
**Justification:** Planned work must capture MOP detail, rollback triggers, and customer-risk context or it will not prevent avoidable outages.
**Improvement:** Expand `maintenance_window` to represent planned work class, method-of-procedure version, rollback plan, change owner, freeze-window status, expected service impact, and dependent site/cell/circuit scope.
**Acceptance evidence:** Calendar and detail screens show planned work scope and risk; validation blocks maintenance windows without rollback criteria; release evidence includes approved MOP-to-window traceability.

### 9. Outage lifecycle and major incident control
**Justification:** Outages need a stricter lifecycle than generic incidents because restoration, communications, and SLA handling are time-critical.
**Improvement:** Add telecom outage states for suspected, declared, major incident, service restored, monitoring, closed, and reopened, with bridge commander, restoration ETA, impacted services, and customer communication milestones stored on `network_incident`.
**Acceptance evidence:** Major incident views show state transitions with timestamps and commanders; outage timelines include restoration checkpoints; scenario tests prove reopened outages preserve prior restoration evidence.

### 10. SLA clock engine tied to service impact
**Justification:** SLA exposure is the operational and commercial consequence of network faults, so it must be calculated from actual impact rather than hand-written notes.
**Improvement:** Use `sla_impact` to model start, pause, resume, exclude, and stop logic by service class, maintenance approval, customer contract, and outage cause so each trouble ticket carries a defensible SLA position.
**Acceptance evidence:** Simulated incidents show clock behavior for planned and unplanned events; breach forecasts appear on the workbench; audit exports show why each pause or exclusion was allowed.

### 11. Capacity modeling for radio, transport, and core edges
**Justification:** Capacity shortages can appear at cell, backhaul, aggregation, or core edges, and a single flat model cannot explain them.
**Improvement:** Split `capacity_segment` into radio, microwave, fiber backhaul, aggregation, and service-edge capacity classes with installed, reserved, used, forecast, and emergency headroom values.
**Acceptance evidence:** Capacity views compare installed versus used by class; congestion analysis can trace whether the bottleneck sits at sector, backhaul, or upstream transport; forecasts preserve historical snapshots.

### 12. Performance KPI catalog with telecom baselines
**Justification:** Performance issues often surface before hard outages, but only if the package knows what KPIs matter per technology and service.
**Improvement:** Add KPI definitions for availability, CSSR, DCR, handover success, PRB utilization, throughput, latency, packet loss, jitter, backhaul utilization, MTTR, and repeat-fault rate with thresholds per vendor and market.
**Acceptance evidence:** KPI cards appear on site, cell, circuit, and outage views; consumed `OperationalKpiChanged` events update projections; tests prove threshold breaches create the right warning state without opening false outages.

### 13. Congestion and degradation early warning
**Justification:** NOC teams need early warning before customer complaints turn into mass trouble tickets.
**Improvement:** Detect gradual degradations on cells, circuits, and transport segments by combining KPI trend breaches, repeat minor alarms, and growing ticket volume into predictive risk on `network_incident` and `capacity_segment`.
**Acceptance evidence:** Risk badges appear before hard failure in synthetic scenarios; operator feedback can confirm or dismiss warnings; model output cites the exact KPIs, alarms, and ticket trends that drove the score.

### 14. Field operations boundary
**Justification:** Telecom network operations must support field crews without absorbing job functions that belong to dispatch, payroll, warehouse, or contractor management systems.
**Improvement:** Define the field boundary so this PBC owns work order context, site access notes, safety prerequisites, equipment needed, and restoration evidence, while external systems remain owners of roster management, time capture, and procurement execution.
**Acceptance evidence:** Boundary diagrams are reflected in command handlers and UI labels; field-ready incidents export the owned context but never mutate external workforce masters; review tests prove only scoped field data is stored locally.

### 15. Inventory boundary
**Justification:** Telecom reliability depends on a clean line between owned operational inventory and referenced enterprise data that the package should not rewrite.
**Improvement:** Document and enforce that `network_element` owns operational topology, telecom attributes, and state needed for NOC, while finance, vendor master, and enterprise asset ledgers remain referenced systems of record.
**Acceptance evidence:** APIs reject writes to non-owned inventory attributes; mapping tables show how referenced IDs attach to owned objects; release evidence includes negative tests proving boundary enforcement.

### 16. NOC workbench queue design
**Justification:** Operators need a single workbench that surfaces what is hot now, what is aging badly, and what is blocked by missing evidence.
**Improvement:** Redesign `TelecomNetworkOperationsWorkbench` into alarm triage, outage control, planned work, capacity risk, SLA risk, and dead-letter queues with explicit filters for market, site, severity, and aging bucket.
**Acceptance evidence:** Workbench routes show stable queue definitions; queue cards expose impacted sites, cells, circuits, and tickets; empty, stale, and degraded-data states are all covered by UI tests.

### 17. Topology, map, and path UI
**Justification:** Telecom operations need visual topology and geography, not only tabular lists.
**Improvement:** Add UI views for geospatial site maps, logical path traces, fiber route diagrams, and site rack summaries with drill-down from outage to site to cell to circuit to fiber path.
**Acceptance evidence:** Click-through flows prove the same outage can be explored in map and path views; screenshots show degraded links highlighted; accessibility checks cover dense topology rendering.

### 18. Site detail UI with power and access context
**Justification:** A site page must answer whether the fault is radio, transport, power, or access-related before a truck roll is approved.
**Improvement:** Expand `TelecomNetworkOperationsDetail` for sites to show power alarms, generator status, battery autonomy estimate, access restrictions, active trouble tickets, planned work, and recent field visits.
**Acceptance evidence:** Seeded site details display distinct power, access, and radio panels; incident drill-in proves power loss can be seen as the likely root cause; release evidence includes screenshots for a live-like site detail flow.

### 19. Outage war room UI
**Justification:** Major incidents need a focused screen that keeps commanders, NOC analysts, and communications aligned.
**Improvement:** Build an outage war room view with bridge commander, event timeline, impacted services, current hypotheses, field crew status, customer updates, and SLA breach countdown.
**Acceptance evidence:** A synthetic major outage produces a populated war room; command actions are permission-gated; audit history proves every manual status update and ETA change is attributable.

### 20. Planned work calendar and conflict UI
**Justification:** Planned work causes preventable outages when conflicting windows, freeze periods, and shared dependencies are not visible.
**Improvement:** Add a calendar-first interface for `maintenance_window` that highlights market freeze periods, overlapping work on shared circuits, risky co-timed fiber activities, and missing rollback evidence.
**Acceptance evidence:** Conflict banners appear when overlapping windows touch the same dependent cells or circuits; operators can see approved versus draft work in one calendar; tests cover freeze-window blocking behavior.

### 21. Alarm triage agent skill
**Justification:** An assistant is only useful in telecom operations if it can reduce alarm load without bypassing human accountability.
**Improvement:** Add an agent skill in `TelecomNetworkOperationsAssistantPanel` that groups related alarms, proposes likely root cause, drafts the initial outage record, and asks for confirmation before mutating `alarm_event` or `network_incident`.
**Acceptance evidence:** Assistant traces show source alarms, correlation logic, and the exact draft changes; blocked actions remain blocked without approval; release evidence includes accepted and rejected triage examples.

### 22. Trouble ticket summarizer and next-action skill
**Justification:** Ticket handovers are slower when the next engineer must reconstruct the last hour from free text.
**Improvement:** Add an agent skill that summarizes `service_assurance_case` history, recent alarms, impacted sites, field notes, and SLA position, then proposes next actions such as dispatch, monitor, reroute, or customer update.
**Acceptance evidence:** Generated summaries cite underlying events and notes; users can compare proposed actions against final human choice; audit logs prove the assistant only writes through governed commands.

### 23. Planned work risk reviewer skill
**Justification:** Planned work quality depends on whether the MOP actually matches the live topology and current freeze conditions.
**Improvement:** Add an agent skill that reviews a maintenance window and its MOP, checks dependency overlap, evaluates rollback completeness, and flags risky cells, circuits, fiber segments, or customer services before approval.
**Acceptance evidence:** Approval flows show the assistant's cited risks and recommended mitigations; false-positive feedback is captured; test windows prove the skill catches missing rollback steps and shared-path conflicts.

### 24. Outage communications drafting skill
**Justification:** Customer and executive updates must be fast, accurate, and aligned with the operational truth already in the NOC record.
**Improvement:** Add an agent skill that drafts outage updates from `network_incident`, `service_assurance_case`, and `sla_impact` facts, with templates for internal bridge notes, customer advisories, and restoration updates.
**Acceptance evidence:** Drafts cite the incident facts they used; approvals are required before distribution; regression fixtures prove customer-facing text never invents root cause or ETA not present in the record.

### 25. Performance degradation investigator skill
**Justification:** Many telecom incidents start as performance complaints rather than hard-down alarms, and analysts need help linking weak signals.
**Improvement:** Add an agent skill that correlates KPI drift, low-severity alarms, repeat trouble tickets, and recent planned work to propose a degradation hypothesis on a site, cell, or circuit.
**Acceptance evidence:** Synthetic degradations show the assistant linking KPIs, alarms, and tickets into a ranked hypothesis set; each hypothesis cites evidence spans; dismissal feedback retrains thresholds without direct data mutation.

### 26. Telecom event taxonomy and naming
**Justification:** Generic lifecycle events are not rich enough for composable telecom operations.
**Improvement:** Expand the event model beyond the current broad events so the package emits typed telecom events for alarm raised, alarm cleared, outage declared, outage restored, planned work approved, fiber cut confirmed, SLA breach forecast, and field evidence attached.
**Acceptance evidence:** Event catalogs and schemas list telecom-specific event names and payloads; replay tests show downstream projections updating from the new taxonomy; release evidence maps each UI queue to the events that feed it.

### 27. Event ordering, idempotency, and replay safety
**Justification:** Telecom feeds arrive late, duplicated, and out of order, especially during major incidents and vendor outages.
**Improvement:** Harden handlers so `alarm_event`, `network_incident`, `service_assurance_case`, and `sla_impact` can tolerate duplicate clears, delayed KPI changes, and repeated ticket sync callbacks without corrupting state.
**Acceptance evidence:** Replay suites cover duplicate, late, and out-of-order telecom events; dead-letter queues retain source lineage; state snapshots after replay match the expected outage and ticket history.

### 28. Event-sourced operational timeline
**Justification:** Outage review, dispute resolution, and release evidence all need a trustworthy chronological record.
**Improvement:** Store a visible timeline for each major object that shows alarms, outage declarations, field updates, customer communications, SLA state changes, and approvals in event order with actor and source metadata.
**Acceptance evidence:** War room and ticket detail views can render the same event-sourced timeline; audit exports include actor, source system, and idempotency keys; tests prove edits append corrections rather than rewriting history.

### 29. Impact propagation from network fault to service and customer
**Justification:** A telecom incident is operationally useful only when it can show what services, regions, and customer classes are actually affected.
**Improvement:** Add propagation logic from site, cell, circuit, and fiber faults to affected service-assurance cases and SLA exposures using topology and service-path membership.
**Acceptance evidence:** A cut on one backhaul path produces the right impacted sites, cells, circuits, and tickets; operators can inspect why each service was marked impacted; negative tests prove unrelated services stay untouched.

### 30. External integration boundaries for OSS and customer systems
**Justification:** Telecom network operations sits between OSS telemetry, field execution systems, and customer-facing channels, so ownership boundaries must be explicit.
**Improvement:** Define connector contracts for NMS, PM counters, inventory discovery, ITSM, dispatch, and customer notification systems while keeping this PBC as owner of telecom operational state and evidence, not every neighboring workflow.
**Acceptance evidence:** Integration manifests show source-of-truth boundaries; connector failures degrade gracefully into visible queue states; release evidence includes negative tests that prevent writes into non-owned customer or dispatch masters.

### 31. Circuit restoration and reroute playbooks
**Justification:** Transport outages are resolved faster when reroute options and restoration steps are attached to the affected circuits.
**Improvement:** Add playbooks for protected switch, temporary reroute, traffic shed, and service-priority restoration linked to the circuit topology and available alternate paths in `capacity_segment`.
**Acceptance evidence:** Synthetic transport failures show playbook recommendations with eligible alternate paths; operator actions record why a reroute was or was not chosen; SLA projections update after reroute activation.

### 32. Fiber cut response playbooks
**Justification:** Fiber cuts have distinct evidence, field workflow, and restoration patterns that deserve first-class handling.
**Improvement:** Create fiber-specific incident templates with route segment localization, likely closure list, dispatch prerequisites, splice validation steps, and post-restoration soak monitoring.
**Acceptance evidence:** A simulated fiber cut opens a templated incident with route and closure candidates; field evidence requires splice completion and optical validation; post-restore monitoring status is visible before closure.

### 33. Power and environmental incident handling
**Justification:** Many site outages come from commercial power loss, generator failure, overheating, or access alarms rather than radio faults.
**Improvement:** Model power and environment incident dimensions on site records, including mains state, generator run state, battery autonomy, fuel concern, HVAC alarms, intrusion alarms, and site access denial.
**Acceptance evidence:** Site and outage views show power/environment panels; correlation rules can declare power loss as root cause for downstream cell alarms; acceptance tests cover recovery after mains restoration and battery exhaustion risk.

### 34. Field evidence capture and spares boundary
**Justification:** Field teams must attach proof of what changed without forcing the package to own warehouse or procurement systems.
**Improvement:** Allow incidents and planned work to collect photos, meter readings, OTDR traces, replaced part numbers, and closure notes while keeping spare stocking, reorder, and purchase workflows outside the local boundary.
**Acceptance evidence:** Evidence uploads attach to the correct site, circuit, or fiber object; controlled fields store replaced-part references without becoming a stock ledger; boundary tests reject warehouse mutations.

### 35. Search and topology query language
**Justification:** Analysts need one fast way to ask for all alarms on a fiber route, all tickets tied to a cell, or all outages in a market.
**Improvement:** Add a telecom-aware search layer that understands site code, cell ID, circuit ID, fiber route, alarm family, outage bridge, and ticket number across owned tables and projections.
**Acceptance evidence:** Search results preserve permission filters and provenance; example queries return mixed alarm, incident, ticket, and topology objects; stale-index warnings appear when projections lag.

### 36. Bulk reconciliation with discovery and monitoring feeds
**Justification:** Inventory drift and stale operational context accumulate when discovery feeds are not reconciled against the owned model.
**Improvement:** Build reconciliation jobs that compare owned sites, cells, circuits, and alarms against discovery or telemetry imports, then queue corrections for human review instead of silently overwriting records.
**Acceptance evidence:** Reconciliation reports classify missing, extra, and mismatched objects; operators can accept or reject proposed corrections in bulk; audit trails show who approved each topology correction.

### 37. Stale inventory and orphaned topology controls
**Justification:** Outages are misdiagnosed when cells, circuits, or fiber paths linger in the model after they were retired or rerouted in reality.
**Improvement:** Add controls that flag stale sites, orphaned cells, unused circuits, unreachable fiber segments, and missing parent-child links using age, last-seen telemetry, and reconciliation history.
**Acceptance evidence:** Control dashboards expose stale-object counts by market; queue filters can isolate orphaned topology; release evidence includes fixtures for stale versus active inventory states.

### 38. Release evidence matrix for telecom scenarios
**Justification:** The package should only claim telecom depth if release evidence proves the critical NOC scenarios end to end.
**Improvement:** Create a release matrix that maps sites, cells, circuits, fiber, alarms, trouble tickets, planned work, outages, capacity, KPIs, UI flows, agent skills, and events to executable evidence in `RELEASE_EVIDENCE.md`.
**Acceptance evidence:** The matrix lists every telecom scenario and its proving test or artifact; missing evidence blocks release; generated evidence includes screenshots, event traces, and queue snapshots from seeded scenarios.

### 39. Seed scenarios and synthetic incident library
**Justification:** Telecom regressions are easier to catch when the same realistic faults can be replayed in every build.
**Improvement:** Ship seed data and test scenarios for a fiber cut, site power loss, congested cell, noisy alarm storm, failed planned work rollback, repeated trouble ticket, and protected circuit reroute.
**Acceptance evidence:** Smoke runs can stand up the seeded topology and execute each scenario; workbench and detail views render stable outputs; release evidence references the scenario IDs used in verification.

### 40. Change approval, freeze windows, and rollback governance
**Justification:** Planned work should not move forward when approvals are missing or freeze periods apply to the affected market or service class.
**Improvement:** Add approval and freeze policy layers to `maintenance_window` and `network_incident`, including emergency change override, executive approval, rollback timeout, and post-change validation requirements.
**Acceptance evidence:** Approval history is visible on every planned work item; freeze-window blocks are enforced in the UI and APIs; synthetic emergency changes prove the override path remains fully audited.

### 41. SLA breach forecasting and escalation
**Justification:** Teams need time to act before a breach is certain, especially when restoration is waiting on field access or shared transport work.
**Improvement:** Forecast SLA risk from outage age, restoration ETA confidence, customer class, and pending field steps so `sla_impact` can escalate before the breach rather than only after it.
**Acceptance evidence:** Forecast badges appear with confidence and time-to-breach; major incident queues sort by breach risk; simulation evidence shows risk moving correctly when ETA or service scope changes.

### 42. Capacity forecasting with reservation awareness
**Justification:** Installed capacity is misleading if reserved headroom, planned adds, and temporary reroutes are not included.
**Improvement:** Extend `capacity_segment` forecasting to include installed, active, reserved, planned, emergency, and temporarily borrowed capacity by sector, link, and aggregation domain.
**Acceptance evidence:** Forecast charts show capacity posture before and after planned work or reroutes; congestion warnings account for reserved headroom; seeded tests prove planned capacity adds clear the expected alerts.

### 43. KPI anomaly detection with operator feedback
**Justification:** Threshold-only monitoring misses subtle degradations and creates false alarms when normal patterns shift by market or season.
**Improvement:** Add anomaly detection over KPI baselines for cells, circuits, and sites, with operator feedback loops that can suppress, confirm, or tune seasonal and market-specific behavior.
**Acceptance evidence:** KPI anomaly cards cite the baseline and deviation; confirmed anomalies can open or enrich incidents; dismissal feedback is stored and visible in release evidence for threshold tuning.

### 44. Customer and service view stitched from telecom causes
**Justification:** Customer-facing impact must trace back to technical causes without forcing the NOC to leave the operational package.
**Improvement:** Build service views that show which sites, cells, circuits, and outages are degrading a customer or service class, while preserving the boundary between internal topology and external account ownership.
**Acceptance evidence:** A service view can drill back to the underlying fault path; customer-impact counts are explainable; tests prove internal topology is visible only to allowed roles while service summaries remain scoped.

### 45. Dead-letter and replay workbench
**Justification:** Event failures are operational work, not hidden plumbing, during major outages and feed interruptions.
**Improvement:** Add a dead-letter queue in the NOC workbench for failed alarm, KPI, and ticket-sync events with replay, quarantine, root-cause notes, and blast-radius indicators.
**Acceptance evidence:** Operators can replay a failed event and see the affected queues recover; poison messages stay quarantined with explanation; release evidence includes at least one forced dead-letter recovery scenario.

### 46. Regional calendar, market hierarchy, and local operating rules
**Justification:** Telecom operations vary by market, timezone, access rules, and local freeze periods, and the package must reflect that without branching the whole code path.
**Improvement:** Add market hierarchy, timezone, holiday calendar, permit restrictions, and local response rules that shape planned work, SLA clocks, field access, and escalation routing.
**Acceptance evidence:** The same scenario behaves differently in two configured markets where rules differ; workbench filters can group by market and timezone; calendar-driven pauses and freezes are visible in audit exports.

### 47. Role segmentation and least-privilege telecom controls
**Justification:** NOC analysts, outage commanders, field reviewers, and auditors should not all have the same powers.
**Improvement:** Expand permissions so roles can separately view topology, declare outages, attach field evidence, approve planned work, override SLA states, replay events, and use high-impact agent skills.
**Acceptance evidence:** Permission tests cover allowed and denied actions across UI and APIs; disabled controls explain why access is blocked; assistant actions inherit the same role checks as manual actions.

### 48. Document intake for MOP, RCA, and field reports
**Justification:** Telecom teams rely on written MOPs, RCAs, shift handovers, and field reports that should inform the operational record without free-form copy-paste loss.
**Improvement:** Use governed document intake to parse MOP steps, rollback criteria, RCA findings, splice reports, and field visit outcomes into structured drafts linked to `maintenance_window`, `network_incident`, or `service_assurance_case`.
**Acceptance evidence:** Parsed drafts cite source spans from the uploaded document; approval is required before structured fields change; release evidence includes successful parsing of one MOP, one RCA, and one field report.

### 49. Separate executive and NOC dashboard projections
**Justification:** Executives need summarized outage and SLA posture, while NOC teams need queue-level operational detail.
**Improvement:** Create distinct projections so executives see major outage count, breach risk, MTTR, and chronic markets, while the NOC sees live alarms, blocked tickets, field waits, and pending planned work conflicts.
**Acceptance evidence:** Two dashboards render from the same underlying events with role-appropriate detail; projection freshness is visible; tests prove executive dashboards never expose raw alarm floods or operator-only notes.

### 50. Manifest-to-backlog traceability gate
**Justification:** The backlog should remain connected to package reality so improvements do not drift away from what the PBC claims to own and release.
**Improvement:** Add a release gate that traces manifest capabilities, APIs, tables, UI fragments, event contracts, and release evidence artifacts against this telecom-specific backlog, with blockers when a claimed surface has no telecom proof.
**Acceptance evidence:** The release gate reports coverage for `network_element`, `capacity_segment`, `network_incident`, `alarm_event`, `service_assurance_case`, `maintenance_window`, `sla_impact`, workbench UI, agent skills, and telecom events; uncovered claims fail the build and are listed in release evidence.
