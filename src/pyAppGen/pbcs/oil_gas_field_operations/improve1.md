# Oil and Gas Field Operations Improvement Backlog

## Current Domain Evidence Used

- PBC key in manifest: `oil_gas_field_operations`
- Manifest description: wells, production, maintenance, field logistics, HSE, reserves, lifting costs, and operating events
- Current owned tables in `manifest.py`: `well`, `production_reading`, `field_ticket`, `workover_plan`, `hse_event`, `reserve_estimate`, `lifting_cost`, policy/rule/runtime/control/governed-model tables
- Current APIs in `manifest.py`: `POST /wells`, `POST /production-readings`, `POST /field-tickets`, `POST /workover-plans`, `POST /hse-events`, `GET /oil-gas-field-operations-workbench`
- Current emitted events in `manifest.py`: `OilGasFieldOperationsCreated`, `OilGasFieldOperationsUpdated`, `OilGasFieldOperationsApproved`, `OilGasFieldOperationsExceptionOpened`
- Current consumed events in `manifest.py`: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- UI fragments already declared in `manifest.py`: `OilGasFieldOperationsWorkbench`, `OilGasFieldOperationsDetail`, `OilGasFieldOperationsAssistantPanel`
- Existing backlog direction already points at event history, anomaly detection, governed agent execution, release evidence, and operational workbench depth; this rewrite narrows those themes into field-operations-specific execution gaps

### 1. Canonical well, pad, and lease hierarchy
**Justification:** Field teams cannot reconcile production, downtime, tickets, or workovers when a single well is referenced differently across surface pad, lease, route, and reporting contexts.
**Improvement:** Expand the `well` domain to explicitly model operator, field, area, pad, lease, well, wellbore, completion, and producing interval hierarchy with effective-dated aliases, route codes, and retired identifiers.
**Acceptance evidence:** Fixtures show one well moving between reporting aliases without losing history; UI detail pages display the full hierarchy; API validation rejects production or field tickets that reference an unknown pad-to-well relationship.

### 2. Wellbore and completion interval granularity
**Justification:** Oil and gas operations decisions are often made at the completion or interval level, not at the lease-header level.
**Improvement:** Add structures for lateral sections, perforated intervals, completion strings, zone names, and current producing interval so production tests, artificial lift, and workovers can target the right physical asset.
**Acceptance evidence:** Test data includes a multi-completion well with interval-specific status changes; workover plans can reference a completion rather than only a well; assistant summaries cite the affected interval in generated recommendations.

### 3. End-to-end well lifecycle state model
**Justification:** Spud, drill, complete, flowback, produce, shut-in, suspend, plug, and abandon states drive different controls, approvals, and downstream reporting.
**Improvement:** Replace generic status handling with a governed lifecycle for `well` that tracks operational readiness, first production date, temporary abandonment, return-to-service, and final abandonment milestones.
**Acceptance evidence:** State-transition tests block invalid jumps such as producing after final abandonment; workbench badges show current lifecycle and last approved transition; release evidence includes lifecycle coverage for representative well scenarios.

### 4. Daily production capture by phase and disposition
**Justification:** Lease operations need oil, gas, water, and injected volumes with a clear split between produced, sold, flared, vented, trucked, transferred, and disposed quantities.
**Improvement:** Extend `production_reading` to capture gross and net phase volumes, disposition pathways, measurement basis, effective production date, reporting date, and revision reason.
**Acceptance evidence:** Example records show the same production day with gross test values, final allocated values, and a later correction; validation blocks missing disposition on gas; workbench totals reconcile daily phase balances.

### 5. Production test workflow with validity windows
**Justification:** Test data becomes dangerous when users cannot tell whether a separator test is current, superseded, partial, or invalid for allocation.
**Improvement:** Create a dedicated production-test flow covering planned test, in-progress test, validated test, superseded test, failed test, and allocation-approved test states with start/stop timestamps and reasoned invalidation.
**Acceptance evidence:** Scenario tests prove a late-entered test cannot retroactively change allocations until approved; UI shows valid-through windows; event history records who superseded a prior test and why.

### 6. Test separator, gauge, and sample quality checks
**Justification:** Field test numbers are only trustworthy if separator condition, gauge calibration, and sample integrity are captured alongside the rates.
**Improvement:** Add metadata for test separator ID, meter/gauge used, calibration date, sample condition, stabilization duration, choke setting, line pressure, and witness signoff for production tests.
**Acceptance evidence:** Invalid tests are automatically flagged when calibration is expired; detail screens show sample quality warnings; release evidence includes approved and rejected test cases with instrument metadata.

### 7. Allocation engine for commingled pads
**Justification:** Pads with shared facilities need defendable allocation logic when individual well tests, meter runs, and facility totals do not line up perfectly.
**Improvement:** Build allocation rules for commingled wells using latest valid test, fallback hierarchy, shrink factors, downtime adjustments, and tolerance thresholds between facility totals and summed well allocations.
**Acceptance evidence:** Backlog evidence includes a pad with three wells sharing a battery; tolerance breaches raise an exception rather than silently forcing a balance; workbench shows the allocation basis per well-day.

### 8. Meter hierarchy and meter-factor history
**Justification:** Production and custody volumes depend on meter lineage, proving factor changes and device swaps over time.
**Improvement:** Add metering entities and history to tie `production_reading` to meter runs, LACT units, tank gauges, gas meters, water meters, and effective-dated meter factors with calibration evidence.
**Acceptance evidence:** Historical queries show which meter and factor were active on any production date; audit views explain a volume change after factor revision; tests cover meter replacement without breaking prior reports.

### 9. Tank, LACT, and ticket reconciliation
**Justification:** Lease operators need a closed chain from tank inventory to run tickets and sales transfer evidence.
**Improvement:** Introduce reconciliation logic between tank gauges, automatic transfer measurements, truck tickets, and sales statements so oil movement out of lease storage is tied back to production and inventory variance.
**Acceptance evidence:** A reconciliation screen shows beginning inventory, produced oil, transferred oil, ending inventory, and unexplained variance; exceptions open when variance exceeds tolerance; evidence packs include linked ticket images and meter values.

### 10. Artificial lift equipment registry
**Justification:** Lift performance cannot be analyzed if the system only knows that a well is “on lift” without tracking equipment type and operating envelope.
**Improvement:** Add an equipment registry for rod pump, ESP, gas lift, plunger lift, progressive cavity pump, intermittent gas, and flowing wells, including install date, vendor/model, stage count, pump size, controller settings, and retrieval date.
**Acceptance evidence:** Each producing well shows current and prior lift systems; workover plans can target lift component replacement; analytics segment downtime and rate loss by lift type.

### 11. Rod pump surveillance and failure coding
**Justification:** Rod-pumped wells need disciplined capture of stroke rate, pump fillage, surface unit issues, and recurring failure modes.
**Improvement:** Add rod-pump-specific surveillance fields and exception logic for fluid pound, pump-off, tubing leak suspicion, parted rod, gearbox issues, and high polished-rod load.
**Acceptance evidence:** Daily surveillance screens flag wells whose cards or operating data imply suboptimal settings; failure codes from pulled jobs roll back into analytics; agent skills can draft a pumping-unit follow-up ticket with cited evidence.

### 12. ESP run-life and shutdown diagnostics
**Justification:** ESP economics are driven by run life, restart success, current imbalance, intake pressure, and trips, not only by production volumes.
**Improvement:** Add ESP-oriented operating history for shutdown reason, amperage/current imbalance, VSD alarms, intake/discharge pressure, restart attempts, and last run-life reset.
**Acceptance evidence:** Workbench views show ESP shutdown timelines and repeat-trip patterns; downtime analytics separate electrical from reservoir causes; acceptance packs include a run-life leaderboard and trip-cause distribution.

### 13. Gas lift configuration and optimization
**Justification:** Gas-lifted wells need visibility into injection allocation, valve strategy, and instability to avoid losing oil while wasting lift gas.
**Improvement:** Capture gas lift design parameters, daily injected gas, available injection source, valve depth set, operating valve assumptions, and instability notes, then surface optimization opportunities when gas is constrained.
**Acceptance evidence:** Simulated scenarios show which wells lose lift first when compressor availability drops; allocation screens separate produced gas from injected gas; workover candidates include gas-lift hardware problems backed by recent history.

### 14. Plunger and intermittent-lift cycle handling
**Justification:** Intermittent wells behave differently from steady-state wells and need event-aware production interpretation.
**Improvement:** Add cycle-aware handling for plunger arrivals, missed arrivals, shut-in windows, open-flow windows, timer settings, and gas buildup periods so volumes and downtime are not mislabeled.
**Acceptance evidence:** Production charts distinguish cycle windows from true facility downtime; control assertions catch impossible arrival sequences; operator UI shows the last several cycle outcomes before recommending intervention.

### 15. Downtime event model with start-stop discipline
**Justification:** Deferred production and root-cause analysis are unreliable when downtime is captured as a single free-text note at the end of the day.
**Improvement:** Add a structured downtime event model with start time, end time, partial-rate flag, responsible system, root cause, failed component, operational impact, and restoration action.
**Acceptance evidence:** Tests cover overlapping downtime, partial downtime, and unclosed downtime; daily deferred production is calculated from duration and baseline; event history shows who closed each outage and on what evidence.

### 16. Deferred production calculation
**Justification:** Operations leaders need defendable lost-oil and lost-gas estimates from downtime and curtailment, not a hand-entered placeholder number.
**Improvement:** Calculate deferred production using a configurable baseline derived from recent valid tests, decline-adjusted trend, or approved engineering target, with separate treatment for full shut-in versus reduced-rate operation.
**Acceptance evidence:** Exception reports explain the baseline used for each deferred estimate; users can compare calculated versus manually overridden deferment with approval trace; release evidence includes variance checks against sample field spreadsheets.

### 17. Workover candidate ranking
**Justification:** Workover dollars should flow to wells with the strongest production recovery, risk reduction, or compliance need.
**Improvement:** Rank `workover_plan` candidates using recent decline, repeated downtime, artificial lift instability, integrity flags, chemical consumption anomalies, and deferred volume exposure, while preserving engineer override with written rationale.
**Acceptance evidence:** Candidate queues show machine-ranked score plus engineer rationale; historical evidence compares recommended ranking to executed jobs; audit output shows why a lower-ranked well was advanced.

### 18. Workover scope, readiness, and after-action capture
**Justification:** A workover record without scope depth, equipment needs, and return-to-service evidence cannot support field execution or later learning.
**Improvement:** Extend `workover_plan` to capture target interval, pulling depth, suspected failure, required equipment, crew readiness, kill-fluid assumptions, planned chemicals, expected downtime, and after-action findings.
**Acceptance evidence:** Completed workovers include discovered-failure code, replaced components, days offline, and restored test result; readiness views block approval if critical equipment or permits are missing; lessons learned roll into failure analytics.

### 19. Field ticket discipline for lease operations
**Justification:** Lease operators rely on tickets for rounds, repairs, tank runs, chemical drops, and observations; those tickets need more than a generic task record.
**Improvement:** Specialize `field_ticket` for route type, visit objective, well/pad/facility reference, ticket source, urgency, service performed, materials used, and follow-up requirement.
**Acceptance evidence:** Tickets can be filtered by route, lease, or service type; mobile-ready screens show the exact asset context; acceptance evidence includes linked photos, timestamps, and closeout notes for sample daily rounds.

### 20. Lease operating rounds and route optimization
**Justification:** Pad visits consume time and cost; the system should help supervisors group field work around geography, urgency, and production impact.
**Improvement:** Build lease-route planning that groups wells and pads by route, flags must-visit sites based on downtime or HSE conditions, and creates a reasoned visit sequence for the day.
**Acceptance evidence:** Route views show travel grouping and production-impact ordering; closed tickets feed back into missed-route analytics; supervisors can see which high-risk sites were not visited and why.

### 21. Chemical program tracking by well and facility
**Justification:** Corrosion inhibitor, demulsifier, paraffin treatment, biocide, and scale inhibitor performance directly affect uptime, treating cost, and integrity.
**Improvement:** Add chemical program entities tied to wells, pads, separators, and water systems, including chemical type, target dosage, actual dosage, delivery method, vendor, and exception reason when treatment is skipped.
**Acceptance evidence:** The workbench highlights wells with missed treatment or unusual dosage variance; field tickets can close a chemical drop against the active program; release evidence includes dosage history and exception coverage.

### 22. Chemical effectiveness and spend correlation
**Justification:** Teams need to know whether chemical spend is reducing corrosion, emulsions, paraffin, scale, or water-handling trouble.
**Improvement:** Link chemical program records to downtime causes, corrosion findings, emulsion severity, BS&W outcomes, and lifting cost so the PBC can surface ineffective or over-applied treatments.
**Acceptance evidence:** Analytics compare treatment spend to repeat failure frequency; recommended program changes cite field outcomes rather than only dosage variance; evidence packs include before-and-after case histories for selected wells.

### 23. HSE boundary between operational upset and reportable incident
**Justification:** Not every outage is an HSE event, and not every HSE event should be buried inside downtime; the system needs a clear boundary.
**Improvement:** Define explicit handoff rules between downtime, `field_ticket`, and `hse_event` for spills, gas releases, line strikes, vehicle incidents, confined-space exposure, and permit breaches, with cross-links instead of duplicate records.
**Acceptance evidence:** A boundary matrix shows when a downtime event must open an HSE record; tests prevent double-counting one incident as multiple independent cases; UI cross-links let auditors trace from production loss to incident investigation.

### 24. Permit, isolation, and job-safety gating
**Justification:** Workovers and many field tasks need proof that isolation, permits, and hazard reviews were in place before work started.
**Improvement:** Add permit-to-work, lockout/isolation, gas test, line-break, confined-space, and job-safety-analysis checkpoints to `workover_plan` and high-risk `field_ticket` flows.
**Acceptance evidence:** Approval cannot advance if required safety checkpoints are incomplete; closeout evidence includes permit references and gas-test timestamps; release evidence contains blocked-action examples that prove the safety gates are active.

### 25. Regulatory production, flare, and vent reporting packs
**Justification:** Monthly and daily regulatory submissions require more than internal production totals; they need defensible classifications and correction history.
**Improvement:** Build reporting packs for oil, gas, water, injected volumes, flared gas, vented gas, downtime explanation, and revision reason with effective-dated mappings to regulatory categories.
**Acceptance evidence:** Sample monthly packs trace each reported figure back to allocated production days and corrections; workbench exports show original and revised numbers; events capture when a filed value is later restated.

### 26. Spill, release, and environmental evidence packs
**Justification:** Environmental reporting depends on rapid evidence assembly across field observations, containment actions, cleanup progress, and closure.
**Improvement:** Extend `hse_event` with spill volume estimate basis, affected media, containment status, remediation milestones, sampling references, agency-notification timestamps, and closure signoff.
**Acceptance evidence:** Incident detail pages show evidence chronology from initial field ticket to closure; required fields differ by incident class; release evidence includes a fully documented spill and a non-reportable release boundary case.

### 27. Water handling, injection, and disposal tracking
**Justification:** Produced-water movement affects cost, environmental exposure, and field uptime, especially when disposal or injection capacity is constrained.
**Improvement:** Add support for produced-water disposition to disposal, reuse, or injection, including transfer point, trucked versus piped movement, injection well destination, and disposal exception reason.
**Acceptance evidence:** Water balances can be reconciled at well, pad, and field level; downtime alerts fire when disposal constraints curtail production; regulatory packs can separate produced, injected, and disposed water totals.

### 28. Haul-off and third-party ticket verification
**Justification:** Trucked oil, water, and chemical movements create leakage and reconciliation risk if third-party ticket details are not validated.
**Improvement:** Capture hauler, truck number, ticket sequence, origin asset, destination, loaded quantity, unloaded quantity, seal status, and mismatch reason for trucked movements tied to field tickets and production records.
**Acceptance evidence:** Reconciliation logic flags duplicate or out-of-sequence truck tickets; workbench audit views show ticket chains by day; acceptance evidence includes linked origin and destination quantities with variance handling.

### 29. Well integrity and barrier surveillance
**Justification:** Annulus pressure, tubing-casing communication, packer integrity, and barrier failures affect safety, production, and workover priority.
**Improvement:** Add integrity monitoring for annulus readings, bleed-down tests, sustained casing pressure observations, integrity status, and required follow-up actions on affected wells.
**Acceptance evidence:** Wells can be filtered by integrity risk class; control assertions open exceptions when pressure thresholds or overdue bleed-down actions are breached; workover ranking incorporates unresolved barrier issues.

### 30. Pressure survey, fluid-level, and surveillance ingestion
**Justification:** Field optimization depends on pressure and fluid-level data that often lives outside daily production entry.
**Improvement:** Introduce surveillance capture for casing pressure, tubing pressure, line pressure, fluid level, pump intake estimate, and test notes, with links to artificial lift recommendations and downtime diagnosis.
**Acceptance evidence:** Trend views overlay surveillance points against production and downtime; invalid readings are rejected when unit or asset context is missing; assistant recommendations cite the exact survey values used.

### 31. Event taxonomy and idempotent operational messaging
**Justification:** Generic create/update events are not enough for field operations where downstream consumers care about tests validated, downtime opened, meter factors changed, and workovers closed.
**Improvement:** Expand emitted events into typed operational events for well lifecycle changes, production test validation, allocation finalization, downtime opened/closed, lift system changed, chemical exception raised, and regulatory pack issued.
**Acceptance evidence:** Event contracts include domain-specific payload examples; duplicate-message tests prove idempotent handling; release evidence maps each major operational action to an emitted event type.

### 32. Replayable operational timeline
**Justification:** Supervisors and auditors need to replay what the field believed on a given date, not only what the database shows after later corrections.
**Improvement:** Use event-sourced history to reconstruct the timeline of well status, production revisions, downtime, workovers, and HSE handoffs as-of any cutoff date and time.
**Acceptance evidence:** A point-in-time timeline view recreates the state before and after a correction; tests prove a restated production day does not rewrite earlier approval evidence; release packs include replay snapshots for sample incidents.

### 33. Release evidence tailored to operations readiness
**Justification:** Technical tests alone do not prove field readiness; the package needs evidence that operators, engineers, and auditors can execute core workflows with domain fidelity.
**Improvement:** Add a release-evidence structure covering daily production entry, well test approval, allocation close, downtime handling, workover closeout, HSE boundary, and regulatory export for representative field scenarios.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` references packaged scenario runs with screenshots, event traces, and reconciled numbers; every critical workflow has pass/fail evidence; unresolved gaps are visible rather than implied away.

### 34. Production surveillance workbench UI
**Justification:** Lease operations need a single screen that shows which wells are underperforming today and why.
**Improvement:** Expand `OilGasFieldOperationsWorkbench` with a production surveillance view showing yesterday versus rolling baseline, current downtime, latest test, lift type, integrity flags, and open field tickets per well.
**Acceptance evidence:** Mocked UI tests confirm sorting by deferred volume and latest exception severity; empty, stale, and degraded data states are covered; supervisors can drill from a bad actor well into its full evidence chain.

### 35. Pad map and route-first UI
**Justification:** Field personnel think in routes and pad clusters, not in a flat list of record IDs.
**Improvement:** Add a route-oriented UI that groups wells by field, pad, and lease, shows current operating condition at pad level, and exposes quick actions for field tickets, downtime start, and chemical delivery confirmation.
**Acceptance evidence:** Route screens display pad-level counts for producing, shut-in, and exception wells; mobile-width layouts preserve key actions; acceptance evidence includes route drilldowns for a multi-pad day.

### 36. Mobile-friendly field ticket capture
**Justification:** Ticket quality degrades when operators have to remember details until they return to the office.
**Improvement:** Make `field_ticket` capture resilient on low-connectivity devices with draft save, photo attachment queueing, timestamp confidence, and later conflict resolution for the same ticket.
**Acceptance evidence:** Offline-to-online sync scenarios preserve attachments and field timestamps; conflict resolution is visible when two users touch the same ticket; release evidence includes a disconnected capture and later reconciliation.

### 37. Allocation and metering audit UI
**Justification:** Allocation exceptions are hard to resolve without an interface that explains how numbers rolled from meter totals to allocated well volumes.
**Improvement:** Add dedicated audit screens for meter totals, tests used, tolerance breaches, fallback rules, manual overrides, and final approved allocations with an explicit “why this number” trace.
**Acceptance evidence:** Users can open any allocated well-day and see the exact meter totals and test basis; override history is visible with approver identity; UI tests cover toleranced and non-toleranced allocations.

### 38. Assistant skill for morning production review
**Justification:** A field operations assistant should reduce supervisor scan time without inventing facts or bypassing approvals.
**Improvement:** Add an agent skill that assembles a morning production brief covering new downtime, major rate drops, invalid tests, meter reconciliation issues, integrity alerts, and high-priority tickets, each backed by cited domain records.
**Acceptance evidence:** Skill outputs include links to underlying wells and events; blocked cases show when evidence is insufficient; acceptance scenarios prove the assistant cannot mutate data from a read-only morning review flow.

### 39. Assistant skill for workover readiness packs
**Justification:** Engineers waste time pulling the same evidence before every workover authorization.
**Improvement:** Add an assistant skill that prepares a workover readiness pack with decline trend, latest test, downtime history, lift history, integrity notes, chemical history, required permits, and expected production recovery basis.
**Acceptance evidence:** Generated packs include source citations and missing-information flags; approval flows require human confirmation before any plan update; release evidence compares a generated pack to manually assembled engineer evidence.

### 40. Assistant skill for regulatory draft preparation
**Justification:** Regulatory work benefits from automation only if draft numbers remain traceable and corrections are explicit.
**Improvement:** Add a governed agent flow that drafts monthly production and flare/vent reporting packs from approved allocations, highlights missing classifications, and blocks submission when supporting evidence is incomplete.
**Acceptance evidence:** Draft packs show source allocations, correction history, and unresolved exceptions; tests confirm no final filing state is set by the assistant alone; audit logs capture every generated draft and reviewer action.

### 41. Assistant skill for downtime root-cause summarization
**Justification:** Repeat failures are missed when supervisors must manually read every ticket and outage note across many wells.
**Improvement:** Add a skill that summarizes repeated downtime drivers by well, pad, lift type, and failed component, with recommendation categories such as operating adjustment, field repair, chemical change, or workover candidate.
**Acceptance evidence:** Summaries cite the exact downtime and field ticket records used; users can reject a recommendation and provide a reason; evidence shows the model distinguishes repeat repair noise from a true recurring cause.

### 42. Escalation rules tied to operational impact
**Justification:** Exception queues become background noise unless escalation honors deferred production, HSE severity, and reporting deadlines.
**Improvement:** Implement policy-driven escalation for downtime, meter variance, invalid tests, integrity concerns, HSE incidents, and overdue workover actions using deferred-volume exposure and regulatory due dates.
**Acceptance evidence:** Policy simulations show how the same issue escalates differently by severity and deadline; notifications are deduplicated; release evidence includes expired, acknowledged, and resolved escalation paths.

### 43. Asset, tenant, and operator boundary controls
**Justification:** Contract operators, joint interests, and multi-asset organizations require strong separation of what each team can see or change.
**Improvement:** Tighten multi-tenant and policy isolation so wells, tickets, workovers, and evidence are scoped by operator, asset, and authorized lease or pad boundaries, including assistant responses and exported reports.
**Acceptance evidence:** Negative tests prove one operator cannot see another operator’s wells or tickets; assistant outputs are filtered by the same policy boundary; exports carry the same boundary constraints as the UI.

### 44. Lease operating cost evidence and lifting-cost traceability
**Justification:** Lifting cost is only useful operationally when linked back to the wells, chemicals, workovers, hauling, and downtime that caused it.
**Improvement:** Extend `lifting_cost` with cost category, cost driver, affected asset scope, linked field ticket or workover, service date, and allocation basis so lease operating expense can be explained at field level.
**Acceptance evidence:** Cost views show per-well and per-pad operating spend alongside production and deferment; users can trace a chemical invoice or hauling charge back to the operational event that generated it; sample evidence includes month-end rollups with drill-through.

### 45. Shift handover and daily production notes
**Justification:** Important context is lost between day and night shift when handover comments remain outside the operating system.
**Improvement:** Add a shift-handover record tied to wells, pads, downtime, workovers, and HSE observations, with unresolved watch items and explicit owner for the next shift.
**Acceptance evidence:** Handover notes appear in the morning production brief and pad views; unresolved watch items persist until closed; evidence includes a shift change during an active outage without loss of context.

### 46. Shut-in, startup, and return-to-service checklists
**Justification:** Wells coming back online after outage or workover need consistent restart evidence to avoid repeated trips and unsafe starts.
**Improvement:** Create checklist-driven workflows for planned shut-in, emergency shut-in, startup, and return-to-service with required line-up confirmation, meter readiness, lift-system readiness, and HSE gate completion.
**Acceptance evidence:** Restart cannot be approved if mandatory checks are incomplete; event history records each checklist milestone; release evidence includes a well shut-in for workover and successfully returned to production.

### 47. Injection and secondary-recovery operations support
**Justification:** Many fields depend on injection wells and pressure support, so field operations coverage is incomplete without them.
**Improvement:** Add support for injection wells, injected water or gas volumes, injection downtime, pressure-support exceptions, and links between injector constraints and producer performance on the same pattern.
**Acceptance evidence:** Pattern views show injector-producer relationships; reporting separates produced and injected volumes correctly; candidate lists can identify producers impacted by nearby injector outages.

### 48. Forecast-versus-actual and target tracking
**Justification:** Supervisors need to know not only what happened, but how far operations are from field plan and recovery targets.
**Improvement:** Add daily and monthly target tracking for oil, gas, water, deferment, test frequency, and workover execution, with reason codes for variance and drill-through to supporting well events.
**Acceptance evidence:** Workbench dashboards show actual versus target at field, pad, and well level; variance explanations link directly to downtime, test, or workover records; release evidence includes a month with plan miss and resolved causation.

### 49. Domain fixtures and regression scenarios
**Justification:** Field-operations software regresses when tests use toy data that ignores commingling, lift diversity, route work, and reporting corrections.
**Improvement:** Build a durable scenario set with flowing wells, rod-pumped wells, ESP wells, gas-lift wells, an injection pattern, a shared pad battery, workover history, chemical programs, trucked water, and a reportable HSE event.
**Acceptance evidence:** Contract, workflow, and UI tests all run against the same realistic fixtures; release evidence references those scenarios by name; failures clearly show which operational story broke.

### 50. Go-live readiness evidence for the PBC
**Justification:** The package should not be considered ready until operations, engineering, HSE, and audit stakeholders can see proof that the core field stories work end to end.
**Improvement:** Require a go-live evidence gate for `oil_gas_field_operations` that bundles workflow passes, UI screenshots, event traces, allocation reconciliations, regulatory draft outputs, assistant-skill evidence, and unresolved-risk disclosure.
**Acceptance evidence:** The release bundle lists exact scenarios executed, exact evidence artifacts produced, and exact open gaps accepted for launch; the path from manifest capabilities to operational proof is visible without reading source code.
