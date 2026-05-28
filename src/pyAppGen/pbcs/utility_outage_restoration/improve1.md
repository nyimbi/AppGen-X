# Utility Outage Restoration PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `utility_outage_restoration` with utility-outage-specific improvements for incident detection, device interruptions, switching, crew dispatch, restoration estimates, customer impact, reliability reporting, storm operations, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `utility_outage_restoration`.
- Domain purpose: outage detection, switching, crew dispatch, restoration estimates, customer impact, and reliability reporting.
- Owned records include `outage_incident`, `device_interruption`, `switching_step`, `crew_assignment`, `restoration_estimate`, `customer_impact`, `reliability_metric`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /outage-incidents`, `POST /device-interruptions`, `POST /switching-steps`, `POST /crew-assignments`, `POST /restoration-estimates`, and `GET /utility-outage-restoration-workbench`.
- Workbench surfaces include `UtilityOutageRestorationWorkbench`, `UtilityOutageRestorationDetail`, and `UtilityOutageRestorationAssistantPanel`.
- AppGen-X events include `UtilityOutageRestorationCreated`, `UtilityOutageRestorationUpdated`, `UtilityOutageRestorationApproved`, and `UtilityOutageRestorationExceptionOpened`.

## 50 High-Impact Improvements

### 1. Outage incident lifecycle state machine

**Justification:** Outages move through reported, predicted, confirmed, assigned, switching, partially restored, restored, verified, closed, and reopened states.

**Improvement:** Add explicit `outage_incident` states with transition reason, source, owner, required evidence, allowed commands, and AppGen-X event emission.

**Acceptance evidence:** Tests must reject invalid transitions and show next allowed actions in `UtilityOutageRestorationWorkbench`.

### 2. Multi-source outage detection

**Justification:** Outage detection can come from customer calls, smart meters, SCADA projections, AMI events, protection devices, social channels, and field reports.

**Improvement:** Add detection source records with confidence, timestamp, affected service point projection, device projection, duplicate matching, and escalation rules.

**Acceptance evidence:** Tests must cluster multiple reports into one incident and flag conflicting source evidence.

### 3. Device interruption hierarchy

**Justification:** Restoration depends on understanding feeder, breaker, recloser, transformer, lateral, switch, and service-level interruptions.

**Improvement:** Expand `device_interruption` with device projection, upstream/downstream relationship, interruption type, predicted fault segment, lockout status, and restoration dependency.

**Acceptance evidence:** Tests must derive affected downstream devices without mutating external network-model tables.

### 4. Network model boundary

**Justification:** The outage PBC needs topology and device data but should not own network asset or GIS source records.

**Improvement:** Store topology projections with feeder, device, service point, phase, connectivity timestamp, and freshness from declared dependencies.

**Acceptance evidence:** Boundary tests must prove topology is projected and no external network table is mutated.

### 5. Customer impact calculation

**Justification:** Dispatchers need affected customer counts, critical customers, life-support flags, priority sites, and restoration segments.

**Improvement:** Expand `customer_impact` with customer class, criticality, life-support projection, facility type, affected phase, start time, and segment.

**Acceptance evidence:** Tests must calculate customer impact from device interruptions and projections.

### 6. Critical customer prioritization

**Justification:** Hospitals, water plants, emergency facilities, life-support customers, and public safety sites require special handling.

**Improvement:** Add priority impact queues with critical customer type, communication requirement, backup status projection, and escalation owner.

**Acceptance evidence:** Tests must elevate incidents with critical customers and show required contacts.

### 7. Incident severity scoring

**Justification:** Dispatch decisions require consistent severity across customer count, hazards, critical load, weather, duration, and crew availability.

**Improvement:** Add severity score with factor explanations, threshold rules, manual override, and review evidence.

**Acceptance evidence:** Tests must compute severity and show explainable factors in the workbench.

### 8. Estimated restoration time lifecycle

**Justification:** Restoration estimates change as crews diagnose, switch, repair, and verify service.

**Improvement:** Expand `restoration_estimate` with estimate type, confidence, source, assumptions, revision reason, communicated timestamp, and expiry.

**Acceptance evidence:** Tests must preserve estimate history and reject stale estimates from public display.

### 9. ETR communication governance

**Justification:** Customers and regulators scrutinize restoration promises and revisions.

**Improvement:** Add communication rules for estimate approval, audience, channel, revision threshold, message template, and suppression.

**Acceptance evidence:** Tests must require approval for broad estimate communication and log all revisions.

### 10. Switching plan workflow

**Justification:** Switching must be safe, sequenced, authorized, and visible before field execution.

**Improvement:** Expand `switching_step` with sequence, device, action, hold point, authority, clearance, expected customer impact, and completion evidence.

**Acceptance evidence:** Tests must reject out-of-order steps and require authorization before energization.

### 11. Safety clearance and hold tags

**Justification:** Crews and operators need lockout, clearance, grounding, and hold-tag controls during restoration.

**Improvement:** Add clearance records with affected devices, issuer, holder, grounding evidence, release criteria, and blocked commands.

**Acceptance evidence:** Tests must block switching completion while active clearances prohibit it.

### 12. Crew assignment capability matching

**Justification:** Restoration tasks require correct crew type, voltage qualification, equipment, location, and availability.

**Improvement:** Expand `crew_assignment` with crew projection, skills, equipment, shift status, travel estimate, task type, and safety briefing.

**Acceptance evidence:** Tests must reject assignment to crews lacking required qualifications.

### 13. Crew routing and staging

**Justification:** Large outages require staging crews by geography, damage pattern, priority customers, and feeder dependencies.

**Improvement:** Add crew staging areas, route plans, access constraints, storm base, and task sequencing.

**Acceptance evidence:** Tests must produce route-aware assignments and show staging status.

### 14. Damage assessment workflow

**Justification:** Restoration estimates and repair plans depend on field assessment of poles, wires, transformers, vegetation, and hazards.

**Improvement:** Add damage assessments with location, asset projection, severity, photos, hazard type, material need, and repair recommendation.

**Acceptance evidence:** Tests must update incident diagnosis and estimate after approved assessment.

### 15. Hazard and public safety controls

**Justification:** Downed wires, fire, flooding, gas proximity, road closures, and energized equipment require public-safety coordination.

**Improvement:** Add hazard records with type, perimeter, responder notification, blocked work, mitigation owner, and clearance evidence.

**Acceptance evidence:** Tests must prevent restoration steps that ignore unresolved severe hazards.

### 16. Mutual aid request tracking

**Justification:** Major events require requesting, staging, and tracking external crews and resources.

**Improvement:** Add mutual aid requests with requesting region, crew type, quantity, ETA, lodging/staging, assigned incidents, and release status.

**Acceptance evidence:** Tests must show mutual-aid availability and assignment history.

### 17. Materials and equipment boundary

**Justification:** Restoration needs transformers, wire, fuses, poles, and mobile equipment but should not own inventory.

**Improvement:** Store material availability projections, reservation status, delivery ETA, and shortage alerts from declared dependencies.

**Acceptance evidence:** Boundary tests must prove material data is projected and no inventory table is mutated.

### 18. Vegetation-related outage handling

**Justification:** Vegetation events require tree crews, hazard assessment, blocked roads, and recurrence analytics.

**Improvement:** Add vegetation flags, tree crew requirement, location, clearance status, recurrence marker, and follow-up prevention task.

**Acceptance evidence:** Tests must route vegetation outages to appropriate crew assignment queues.

### 19. Weather and storm mode

**Justification:** Storms change dispatch priorities, crew staging, estimates, communication cadence, and reliability reporting.

**Improvement:** Add storm mode with weather projection, operating level, staging plan, communication interval, estimate policy, and mutual aid triggers.

**Acceptance evidence:** Tests must apply storm-specific rules and queues during active storm mode.

### 20. Nested outage and partial restoration handling

**Justification:** Feeder-level restoration may reveal nested transformer or service outages.

**Improvement:** Add parent-child incident links, partial restoration events, nested detection, and customer impact recalculation.

**Acceptance evidence:** Tests must preserve parent incident history while opening nested incidents for remaining outages.

### 21. Momentary interruption tracking

**Justification:** Momentary outages and repeated recloser operations affect reliability and customer experience even when service restores.

**Improvement:** Add momentary interruption events with device, duration, count, affected customers, and recurrence analysis.

**Acceptance evidence:** Tests must calculate momentary metrics separately from sustained outage duration.

### 22. Reliability metric calculation

**Justification:** Utilities track reliability metrics such as interruption frequency, duration, customers interrupted, and major event exclusions.

**Improvement:** Expand `reliability_metric` with metric type, period, customer count, outage duration, exclusion flag, event linkage, and certification.

**Acceptance evidence:** Tests must calculate reliability metrics from closed incidents and customer impact.

### 23. Major event classification

**Justification:** Reliability reporting can treat major event days differently and requires defensible classification.

**Improvement:** Add major event classification with threshold, weather evidence, affected area, approval, and reporting treatment.

**Acceptance evidence:** Tests must mark eligible incidents for major-event treatment with audit evidence.

### 24. Regulatory reporting package

**Justification:** Outage duration, customers affected, critical load, and restoration performance may require regulator-ready reports.

**Improvement:** Add report packages with period, included incidents, exclusions, metrics, certification, attachments, and submission evidence.

**Acceptance evidence:** Tests must generate reports from owned outage records and projections.

### 25. Public outage map feed

**Justification:** Customers expect outage map updates without exposing sensitive device or customer details.

**Improvement:** Add public feed projection with generalized location, affected count range, status, estimate, cause category, and suppression rules.

**Acceptance evidence:** Tests must redact sensitive data and publish only approved outage-map fields.

### 26. Customer notification timeline

**Justification:** Customers need timely notices for outage confirmation, estimate updates, restoration, and nested outage discovery.

**Improvement:** Add notification events with audience, channel, template, trigger, delivery evidence, and opt-out handling.

**Acceptance evidence:** Tests must create notices for configured milestones and prevent duplicate sends.

### 27. Call center synchronization

**Justification:** Agents need current incident status, estimates, safety messages, and customer-specific impact.

**Improvement:** Add call-center projection with incident summary, affected customer status, estimate, safety message, and next update time.

**Acceptance evidence:** Tests must expose current call-center-ready summaries without raw datastore access.

### 28. Cause code governance

**Justification:** Cause codes drive reliability analytics, prevention work, regulatory reporting, and customer communication.

**Improvement:** Add cause classification with preliminary, confirmed, corrected, unknown, and multi-cause handling.

**Acceptance evidence:** Tests must require cause confirmation before final closure unless unknown is justified.

### 29. Restoration verification

**Justification:** Crews may report completion before all customers are restored or nested outages are discovered.

**Improvement:** Add verification checks using meter pings, customer callbacks, crew confirmation, and device state projections.

**Acceptance evidence:** Tests must keep incidents in verification until configured checks pass.

### 30. Reopen and callback workflow

**Justification:** Customer callbacks after closure can indicate nested faults, incorrect status, or service-side issues.

**Improvement:** Add reopen records with callback source, affected customer, prior incident, diagnosis, nested flag, and resolution.

**Acceptance evidence:** Tests must reopen or create child incidents based on callback evidence.

### 31. Workbench incident command board

**Justification:** Dispatchers need one command surface for incidents, devices, crews, switching, estimates, hazards, and customers.

**Improvement:** Add command-board views with severity, map context, crew status, switching steps, ETR, hazards, and customer impact.

**Acceptance evidence:** UI tests must expose command board sections and role-specific actions.

### 32. Crew mobile task packet

**Justification:** Field crews need concise packets with location, hazard, device, switching, materials, customer priority, and evidence capture.

**Improvement:** Add mobile task packets with checklist, photos, GPS, safety briefing, material needs, and completion notes.

**Acceptance evidence:** Tests must render crew task context from owned records and projections.

### 33. Outage rule and parameter workbench

**Justification:** Outage operations tune thresholds for severity, estimates, storm mode, major events, and notifications.

**Improvement:** Add governed editors for incident clustering, severity factors, ETR confidence, notification cadence, storm rules, and reliability exclusions.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 34. Agent-assisted outage summarization

**Justification:** Dispatchers need fast narrative summaries from noisy incident, crew, device, and customer data.

**Improvement:** Add assistant skills that summarize incident status, blockers, next actions, affected customers, and communication guidance.

**Acceptance evidence:** Tests must verify assistant output cites current owned records and projections.

### 35. Agent-assisted switching review

**Justification:** Switching errors can create safety incidents and wider outages.

**Improvement:** Add assistant checks for missing hold points, conflicting clearances, out-of-order steps, and mismatched device projections.

**Acceptance evidence:** Tests must produce review warnings without auto-approving switching.

### 36. Agent safety restrictions

**Justification:** AI must not silently energize devices, close incidents, dispatch crews, or publish customer estimates.

**Improvement:** Require agent proposals to declare command, affected records, safety impact, customer impact, evidence, confidence, and approval role.

**Acceptance evidence:** Tests must block high-impact agent writes without explicit approval.

### 37. AppGen-X event specialization

**Justification:** Outage restoration composes with grid operations, field service, customer communications, inventory, and billing through events.

**Improvement:** Define typed events for outage confirmed, device interrupted, switching approved, crew assigned, estimate revised, customer restored, and incident closed.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 38. Point-in-time outage reconstruction

**Justification:** Disputes and regulatory reviews require reconstructing what was known during an outage.

**Improvement:** Add event replay for incident state, customer impact, estimates, switching, crew assignments, and communications at any timestamp.

**Acceptance evidence:** Tests must reproduce historical outage snapshots from owned events.

### 39. Cryptographic outage evidence packet

**Justification:** Major events, claims, and regulatory reports need tamper-evident evidence.

**Improvement:** Add hash-linked packets for incident timeline, switching plan, customer impact, estimate revisions, crew assignments, and closure.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 40. Equity and vulnerability analytics

**Justification:** Utilities must understand whether restoration patterns disproportionately affect vulnerable communities.

**Improvement:** Add privacy-safe analytics for critical customers, medical vulnerability projections, community impact, duration, and restoration sequence.

**Acceptance evidence:** Tests must aggregate without exposing individual sensitive data.

### 41. Estimated crew arrival tracking

**Justification:** Dispatchers need to know when crews will arrive and whether travel constraints delay diagnosis.

**Improvement:** Add crew ETA, travel status, route blockers, staging changes, and arrival confirmation.

**Acceptance evidence:** Tests must update incident workflow when crew arrival is delayed or confirmed.

### 42. Feeder patrol workflow

**Justification:** Unknown-cause outages require structured patrol of feeders, laterals, and devices.

**Improvement:** Add patrol segments, assigned crew, inspected devices, findings, no-fault markers, and next segment recommendations.

**Acceptance evidence:** Tests must show patrol progress and prevent duplicate segment assignments.

### 43. Restoration dependency graph

**Justification:** Some repairs and switching steps must happen before others can safely restore customers.

**Improvement:** Add dependency graph linking incidents, device interruptions, switching steps, crews, materials, and hazards.

**Acceptance evidence:** Tests must block dependent tasks until prerequisites are complete.

### 44. Mutual-aid cost and release evidence

**Justification:** Mutual aid crews require release, demobilization, work evidence, and cost handoff.

**Improvement:** Add mutual aid work logs, release status, demobilization time, work packet evidence, and cost projection handoff.

**Acceptance evidence:** Tests must produce mutual-aid summary reports without owning finance records.

### 45. Customer claims handoff boundary

**Justification:** Outages can create customer claims, but claims case handling belongs elsewhere.

**Improvement:** Add claim-intake event payloads with incident, customer impact, duration, cause, and evidence packet reference.

**Acceptance evidence:** Boundary tests must show claim handoff through declared events only.

### 46. Restoration performance benchmarking

**Justification:** Operations teams need to compare restoration performance by cause, area, crew type, storm mode, and device class.

**Improvement:** Add performance analytics for time to detect, assign, arrive, switch, restore, verify, and close.

**Acceptance evidence:** Tests must calculate benchmarks from owned timeline events.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic outage workflows execute after composition.

**Improvement:** Add smoke scenarios for customer-reported outage, device interruption, switching plan, crew assignment, ETR revision, partial restoration, and closure.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for every scenario.

### 48. Cross-PBC boundary proof

**Justification:** Outage restoration touches grid topology, field crews, customer data, inventory, communications, and billing without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Storm command center

**Justification:** Major events need a unified storm room surface for incidents, crews, mutual aid, critical customers, estimates, and public messages.

**Improvement:** Add storm command center with operating level, map, crew staging, top incidents, ETR policy, mutual aid, and reliability impact.

**Acceptance evidence:** UI tests must expose storm mode controls and summary metrics.

### 50. Outage restoration executive briefing

**Justification:** Leaders need concise status without interrupting dispatchers during active restoration.

**Improvement:** Add briefing generator with active incidents, customers out, critical impacts, crew status, ETR confidence, risks, and next updates.

**Acceptance evidence:** Tests must generate a briefing from owned records and projections with no raw datastore access.
