# Water and Wastewater Operations PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `water_wastewater_operations` with water and wastewater specific improvements for treatment plants, quality samples, permit limits, pump assets, service interruptions, field work orders, compliance sampling, regulatory reporting, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `water_wastewater_operations`.
- Domain purpose: treatment plants, water quality, permits, assets, service interruptions, field work, and compliance reporting.
- Owned records include `treatment_plant`, `water_quality_sample`, `permit_limit`, `pump_asset`, `service_interruption`, `field_work_order`, `compliance_sample`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /treatment-plants`, `POST /water-quality-samples`, `POST /permit-limits`, `POST /pump-assets`, `POST /service-interruptions`, and `GET /water-wastewater-operations-workbench`.
- Workbench surfaces include `WaterWastewaterOperationsWorkbench`, `WaterWastewaterOperationsDetail`, and `WaterWastewaterOperationsAssistantPanel`.
- AppGen-X events include `WaterWastewaterOperationsCreated`, `WaterWastewaterOperationsUpdated`, `WaterWastewaterOperationsApproved`, and `WaterWastewaterOperationsExceptionOpened`.

## 50 High-Impact Improvements

### 1. Treatment plant operating state model

**Justification:** Plants operate through normal, constrained, bypass, maintenance, emergency, shutdown, startup, and violation-risk states.

**Improvement:** Add explicit `treatment_plant` states with operating mode, capacity, operator shift, required checks, transition reason, and event emission.

**Acceptance evidence:** Tests must reject invalid state transitions and show plant state in `WaterWastewaterOperationsWorkbench`.

### 2. Process train configuration

**Justification:** Treatment performance depends on intake, clarification, filtration, disinfection, sludge handling, aeration, digestion, and effluent stages.

**Improvement:** Add process train records with units, status, capacity, bypass possibility, criticality, and active configuration by plant.

**Acceptance evidence:** Tests must link samples and permit performance to active process trains.

### 3. Source water and influent tracking

**Justification:** Raw water or influent quality drives treatment decisions and compliance risk.

**Improvement:** Add source/influent observations for turbidity, flow, pH, temperature, conductivity, rainfall, industrial load, and anomaly notes.

**Acceptance evidence:** Tests must flag abnormal influent conditions and create operator review tasks.

### 4. Water quality sample chain of custody

**Justification:** Compliance and public health decisions rely on defensible sample identity, collection, preservation, transport, and analysis.

**Improvement:** Expand `water_quality_sample` with sample point, collector, method, preservation, collection time, custody transfers, lab projection, and status.

**Acceptance evidence:** Tests must reject result approval when custody or preservation evidence is incomplete.

### 5. Sampling plan scheduler

**Justification:** Utilities must meet recurring sampling obligations by site, parameter, period, method, and population served.

**Improvement:** Add sampling plans with frequency, required parameters, locations, seasonality, due windows, alternates, and missed-sample exceptions.

**Acceptance evidence:** Tests must generate due samples and open overdue exceptions.

### 6. Compliance sample distinction

**Justification:** Operational samples and regulatory compliance samples have different rules, approval, and reporting duties.

**Improvement:** Expand `compliance_sample` with regulatory purpose, permit link, reportability, approval status, resample requirement, and certification.

**Acceptance evidence:** Tests must separate operational sample dashboards from compliance reporting packages.

### 7. Permit limit library

**Justification:** Permit limits vary by plant, outfall, parameter, averaging period, flow condition, and effective date.

**Improvement:** Expand `permit_limit` with limit type, units, parameter, sample point, averaging basis, season, effective window, and exceedance rule.

**Acceptance evidence:** Tests must evaluate samples against the correct active permit limit.

### 8. Exceedance and violation workflow

**Justification:** Limit exceedances need timely notice, investigation, corrective action, resampling, and regulatory evidence.

**Improvement:** Add exceedance cases with sample, permit limit, severity, notification deadline, root cause, corrective action, and closure evidence.

**Acceptance evidence:** Tests must open violation workflows and block closure without required notice evidence.

### 9. Disinfection residual management

**Justification:** Residual levels protect public health but must stay within operational and regulatory bounds.

**Improvement:** Add residual observations, target bands, analyzer projection, manual confirmation, dosing action, and low/high residual alerts.

**Acceptance evidence:** Tests must create alerts for residual breaches and tie actions to operator evidence.

### 10. Boil water advisory workflow

**Justification:** Pressure loss, contamination risk, or microbiological findings can require public advisories and rescission evidence.

**Improvement:** Add advisory records with affected area projection, trigger, public notice, sample requirements, rescission criteria, and communications.

**Acceptance evidence:** Tests must prevent advisory closure until resample and notice criteria are met.

### 11. Service interruption lifecycle

**Justification:** Water main breaks, sewer blockages, pressure loss, planned shutdowns, and treatment constraints affect customers and compliance.

**Improvement:** Expand `service_interruption` with type, start, affected area, customer impact, cause, crew assignment projection, advisory status, and restoration.

**Acceptance evidence:** Tests must track planned and unplanned interruptions through verification and closure.

### 12. Pressure zone impact model

**Justification:** Water interruptions and pressure events depend on zones, valves, pumps, tanks, and elevation.

**Improvement:** Store pressure zone projections with affected service area, critical customers, valves, tanks, and hydraulic freshness.

**Acceptance evidence:** Boundary tests must prove hydraulic and GIS data are projections and no external network table is mutated.

### 13. Pump asset lifecycle

**Justification:** Pumps fail, degrade, cavitate, trip, run inefficiently, and require preventive maintenance.

**Improvement:** Expand `pump_asset` with operating status, duty/standby role, flow, head, runtime, starts, vibration projection, maintenance status, and criticality.

**Acceptance evidence:** Tests must flag pump assets with abnormal runtime or unavailable standby status.

### 14. Lift station monitoring

**Justification:** Wastewater lift station failures can cause overflows and environmental harm.

**Improvement:** Add lift station operating records with wet well level, pump status, alarms, generator status, overflow risk, and response actions.

**Acceptance evidence:** Tests must open emergency work when overflow risk thresholds are crossed.

### 15. Sewer overflow event handling

**Justification:** Sanitary or combined sewer overflows require immediate response, sampling, public notice, and regulatory reporting.

**Improvement:** Add overflow records with location, estimated volume, receiving water, cause, start/stop, cleanup, sampling, and notice evidence.

**Acceptance evidence:** Tests must generate reporting tasks and preserve volume estimate assumptions.

### 16. Field work order specialization

**Justification:** Water and wastewater field work includes valve operations, hydrants, leaks, blockages, meter assists, sampling, and repairs.

**Improvement:** Expand `field_work_order` with work type, asset projection, safety controls, crew projection, materials projection, traffic control, and completion evidence.

**Acceptance evidence:** Tests must route work by asset type and required skill without mutating crew or inventory tables.

### 17. Valve operation and isolation evidence

**Justification:** Main breaks and planned shutdowns require documented valve closures, affected customers, and reopening checks.

**Improvement:** Add valve operation records with valve projection, action, sequence, operator, time, impact, and verification.

**Acceptance evidence:** Tests must reconstruct isolation plans and customer impact from valve operations.

### 18. Hydrant inspection and flushing

**Justification:** Hydrants support fire flow, flushing, water quality, and maintenance programs.

**Improvement:** Add hydrant inspection records with flow, pressure, condition, accessibility, flushing volume, discoloration notes, and repair need.

**Acceptance evidence:** Tests must create follow-up work for failed hydrant checks.

### 19. Main break response

**Justification:** Main breaks require leak confirmation, isolation, repair, flushing, sampling, restoration, and customer communication.

**Improvement:** Add main break cases with pipe projection, break type, leak severity, affected zone, repair action, flushing, samples, and closure.

**Acceptance evidence:** Tests must block closure before restoration and post-repair sample evidence.

### 20. Wastewater blockage and backup workflow

**Justification:** Blockages and backups need urgent response, cause classification, cleanup, claim handoff, and prevention.

**Improvement:** Add blockage cases with location, pipe projection, cause, affected customers, cleanup status, CCTV projection, and corrective action.

**Acceptance evidence:** Tests must route severe backups and emit claim handoff events without owning claims tables.

### 21. CCTV and inspection boundary

**Justification:** Pipe inspection results guide work but may come from specialized inspection systems.

**Improvement:** Store CCTV projections with defect codes, severity, segment, inspection date, media reference, and freshness.

**Acceptance evidence:** Boundary tests must prove inspection data is projected and not mutated.

### 22. Chemical dosing control evidence

**Justification:** Treatment chemicals affect compliance, safety, costs, and public health.

**Improvement:** Add dosing events with chemical type, dose, target parameter, operator, feed equipment, inventory projection, and adjustment reason.

**Acceptance evidence:** Tests must tie dosing changes to sample trends or operating conditions.

### 23. Sludge and biosolids handling

**Justification:** Wastewater operations require sludge volume, treatment, hauling, disposal, land application, and compliance evidence.

**Improvement:** Add biosolids records with volume, solids content, treatment class, hauling ticket, destination, pathogen/vector evidence, and certification.

**Acceptance evidence:** Tests must generate biosolids compliance packages.

### 24. Industrial discharge monitoring

**Justification:** Industrial dischargers can affect treatment performance, permit compliance, and pretreatment enforcement.

**Improvement:** Store industrial discharge projections, sample results, discharge limits, exceedance, notice, and enforcement handoff.

**Acceptance evidence:** Tests must flag industrial discharge impacts without owning industrial customer tables.

### 25. Storm and inflow response

**Justification:** Wet weather can drive infiltration, inflow, overflows, turbidity, and treatment constraints.

**Improvement:** Add storm response mode with rainfall projection, flow changes, plant constraints, lift station risk, and staffing actions.

**Acceptance evidence:** Tests must apply storm-specific thresholds and workbench queues.

### 26. Tank and reservoir operations

**Justification:** Storage levels affect pressure, fire flow, water age, and service continuity.

**Improvement:** Add storage asset projections with level, turnover, low/high thresholds, isolation status, and water quality watch.

**Acceptance evidence:** Tests must create alerts for storage level and water-age risk.

### 27. Water loss and non-revenue water signals

**Justification:** Leaks, meter errors, theft, and operational flushing affect water loss.

**Improvement:** Add water loss analytics using production, district meter projection, service interruption, flushing, and repair events.

**Acceptance evidence:** Tests must calculate district loss indicators and open investigation tasks.

### 28. Energy and process efficiency

**Justification:** Pumping and treatment consume significant energy, and operators need efficiency insight.

**Improvement:** Add energy projections by plant, pump, process train, flow, and operating mode with efficiency metrics.

**Acceptance evidence:** Tests must calculate energy intensity and expose assumptions.

### 29. Regulatory reporting package

**Justification:** Utilities submit discharge monitoring, drinking water, overflow, biosolids, and sampling reports.

**Improvement:** Add report packages with period, permit, included samples, exceedances, operator certification, attachments, and submission evidence.

**Acceptance evidence:** Tests must generate regulator-ready packages from owned records and projections.

### 30. Operator logbook

**Justification:** Shift logs record observations, process changes, alarms, incidents, and handoffs.

**Improvement:** Add operator log entries with shift, plant, process area, observation, action, linked sample/work order, and handoff status.

**Acceptance evidence:** Tests must show log continuity and unresolved handoff items.

### 31. Alarm and telemetry boundary

**Justification:** Operators need telemetry and alarms but should not own SCADA historian data.

**Improvement:** Store telemetry projections with tag, timestamp, value, quality, alarm state, and freshness for operational decisions.

**Acceptance evidence:** Boundary tests must prove telemetry is projected and raw historian tables are not mutated.

### 32. Workbench plant command board

**Justification:** Operators need one surface for plant status, samples, permits, alarms, pumps, interruptions, work orders, and reports.

**Improvement:** Add command-board views with process state, due samples, permit risk, active interruptions, pump alarms, and compliance tasks.

**Acceptance evidence:** UI tests must expose plant command sections and drilldowns.

### 33. Field crew mobile packet

**Justification:** Crews need asset location, safety, work steps, photos, traffic controls, materials, and restoration checks.

**Improvement:** Add mobile work packets with map projection, checklist, safety controls, evidence capture, and completion validation.

**Acceptance evidence:** Tests must render field packets from owned work orders and projections.

### 34. Rule and parameter workbench

**Justification:** Water operations tune permit limits, sample schedules, advisory triggers, overflow thresholds, and reporting rules.

**Improvement:** Add governed editors for sampling frequency, permit thresholds, advisory rules, storm mode, and work-order priorities.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 35. Agent-assisted sample interpretation

**Justification:** Operators need help understanding sample trends, exceedance risk, and required follow-up.

**Improvement:** Add assistant skills that summarize sample results, compare limits, identify anomalies, and propose next actions.

**Acceptance evidence:** Tests must verify assistant output cites sample and permit evidence.

### 36. Agent-assisted incident narration

**Justification:** Service interruptions and overflows need concise, accurate narratives for supervisors and regulators.

**Improvement:** Add assistant generation for incident timelines, cause summaries, public notices, and report drafts from owned evidence.

**Acceptance evidence:** Tests must require human approval before report submission or public advisory text is finalized.

### 37. Agent safety restrictions

**Justification:** AI must not silently certify samples, close violations, rescind advisories, or alter permit evidence.

**Improvement:** Require agent proposals to declare command, affected records, public health impact, regulatory impact, evidence, confidence, and approval role.

**Acceptance evidence:** Tests must block high-impact agent writes without explicit approval.

### 38. AppGen-X event specialization

**Justification:** Water operations compose with field service, asset management, customer communications, compliance, inventory, and billing through events.

**Improvement:** Define typed events for sample collected, limit exceeded, pump alarmed, interruption opened, advisory issued, work completed, and report certified.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 39. Point-in-time compliance reconstruction

**Justification:** Audits require reconstructing sample status, permit limits, plant state, and reports as of a point in time.

**Improvement:** Add event replay for samples, permit limits, plant state, interruptions, work orders, and report packages.

**Acceptance evidence:** Tests must reproduce historical compliance snapshots from owned events.

### 40. Cryptographic compliance evidence packet

**Justification:** Public health, environmental, and regulatory disputes need tamper-evident evidence.

**Improvement:** Add hash-linked packets for sample chain of custody, exceedance cases, advisories, overflow events, and regulatory reports.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 41. Asset criticality and resilience scoring

**Justification:** Pump, plant, and network issues should be prioritized by service impact, compliance risk, and redundancy.

**Improvement:** Add criticality scores using asset projection, customer impact, permit risk, redundancy, and historical failures.

**Acceptance evidence:** Tests must calculate criticality and use it in work order priority.

### 42. Preventive maintenance coordination

**Justification:** Preventive maintenance reduces pump failures, permit risk, and service interruptions.

**Improvement:** Store maintenance projections, due status, skipped maintenance, and operational risk from declared asset dependencies.

**Acceptance evidence:** Boundary tests must prove maintenance data is projected and not mutated.

### 43. Public notification and communication timeline

**Justification:** Advisories, interruptions, flushing, pressure changes, and overflows require clear communications.

**Improvement:** Add notification records with audience, channel, template, delivery evidence, revision, and rescission criteria.

**Acceptance evidence:** Tests must create notices for configured triggers and prevent duplicate sends.

### 44. Laboratory result reconciliation

**Justification:** Lab results must match sample identity, method, parameter, holding time, and reporting limits.

**Improvement:** Add lab result reconciliation with method validation, holding-time check, qualifier, detection limit, and discrepancy queue.

**Acceptance evidence:** Tests must reject invalid or mismatched lab results.

### 45. Environmental impact analytics

**Justification:** Utilities need insight into overflows, treatment efficiency, energy intensity, chemical use, and receiving-water impacts.

**Improvement:** Add analytics by plant, permit, receiving water, process train, weather event, and period.

**Acceptance evidence:** UI tests must expose environmental metrics and supporting evidence.

### 46. Emergency response mode

**Justification:** Contamination, major main breaks, floods, cyber incidents, and plant failures require emergency operations.

**Improvement:** Add emergency mode with incident command, staffing, public notices, critical customers, mutual aid, and executive briefing.

**Acceptance evidence:** Tests must apply emergency rules and command-center views.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic water operations execute after composition.

**Improvement:** Add smoke scenarios for sample collection, permit exceedance, pump alarm, service interruption, field work, advisory, and compliance report.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for every scenario.

### 48. Cross-PBC boundary proof

**Justification:** Water operations touch GIS, SCADA, field crews, inventory, customer communications, asset management, and billing without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Daily operator briefing

**Justification:** Operators need concise status for plants, samples, permits, alarms, interruptions, work, and compliance risk.

**Improvement:** Add briefing generator with due tasks, active risks, samples, pump issues, interruptions, and regulatory deadlines.

**Acceptance evidence:** Tests must generate a briefing from owned records and projections.

### 50. Water operations command center

**Justification:** Users need one operational surface for treatment, samples, limits, pumps, interruptions, work orders, compliance, and agent support.

**Improvement:** Add command center with plant status, sample calendar, permit risk, pump alerts, interruption map, report queue, and assistant panel.

**Acceptance evidence:** UI tests must expose command center context and governed actions without raw datastore access.
