# Livestock Herd Management PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `livestock_herd_management` with livestock-specific improvements for animal identity, herd groups, health, breeding, feed, movements, treatments, compliance, productivity, sustainability, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `livestock_herd_management`.
- Domain purpose: animals, health, breeding, feed, movements, treatments, compliance, and herd productivity.
- Owned records include `animal`, `herd_group`, `health_event`, `breeding_record`, `feed_ration`, `movement_permit`, `treatment`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /animals`, `POST /herd-groups`, `POST /health-events`, `POST /breeding-records`, `POST /feed-rations`, and `GET /livestock-herd-management-workbench`.
- Workbench surfaces include `LivestockHerdManagementWorkbench`, `LivestockHerdManagementDetail`, and `LivestockHerdManagementAssistantPanel`.
- AppGen-X events include `LivestockHerdManagementCreated`, `LivestockHerdManagementUpdated`, `LivestockHerdManagementApproved`, and `LivestockHerdManagementExceptionOpened`.

## 50 High-Impact Improvements

### 1. Permanent animal identity with tag history

**Justification:** Herd records fail when ear tags, RFID devices, tattoos, brands, or registry numbers are replaced without preserving identity continuity.

**Improvement:** Expand `animal` identity with primary identifier, alternate identifiers, tag issue and retirement events, lost-tag incidents, duplicate checks, and evidence attachments.

**Acceptance evidence:** Tests must prove tag replacement preserves the same animal record, duplicate identifiers open an exception, and the detail view shows full identifier history.

### 2. Birth, acquisition, and source provenance

**Justification:** Productivity, disease traceability, and compliance depend on whether an animal was born on farm, purchased, leased, transferred, rescued, or imported.

**Improvement:** Add source provenance, dam and sire references, acquisition documents, seller or origin premises projection, arrival condition, and quarantine requirement flags.

**Acceptance evidence:** Intake tests must require source provenance before active herd assignment and show acquisition evidence in `LivestockHerdManagementDetail`.

### 3. Herd group membership periods

**Justification:** Animals move between pens, flocks, paddocks, cohorts, production strings, and treatment groups over time.

**Improvement:** Model `herd_group` membership as dated intervals with entry reason, exit reason, location, stocking density, responsible handler, and overlap validation.

**Acceptance evidence:** Tests must reject overlapping active memberships and reconstruct group composition at any historical date.

### 4. Species and production-type profiles

**Justification:** Dairy cattle, beef cattle, poultry, swine, small ruminants, aquaculture, and working animals have different data needs.

**Improvement:** Add configurable species and production profiles that control required fields, productivity metrics, breeding semantics, health protocols, and movement rules.

**Acceptance evidence:** Tests must show different required fields for dairy, beef, poultry, and swine profiles without changing the PBC key or owned boundaries.

### 5. Animal lifecycle state machine

**Justification:** Active, quarantined, sick, treated, bred, pregnant, lactating, finished, sold, deceased, culled, and archived states must be explicit.

**Improvement:** Add lifecycle states with transition reasons, allowed commands, required evidence, effective date, and event emission for material changes.

**Acceptance evidence:** Invalid transition tests must fail and the workbench must show next allowed actions by animal state.

### 6. Biosecurity quarantine workflow

**Justification:** New arrivals, returning animals, disease exposure, and regulatory holds require controlled isolation.

**Improvement:** Add quarantine records with start trigger, location, testing schedule, observation notes, release criteria, responsible staff, and movement restrictions.

**Acceptance evidence:** Tests must block movement, breeding, and group mixing for quarantined animals until release criteria are approved.

### 7. Health event clinical taxonomy

**Justification:** A generic health note cannot support morbidity analysis, treatment protocols, or disease reporting.

**Improvement:** Expand `health_event` with symptom, diagnosis, severity, body system, infectious risk, observation method, veterinarian involvement, and reportability.

**Acceptance evidence:** Health-event tests must require disease-specific fields and produce workbench filters for reportable, severe, and unresolved cases.

### 8. Vaccination protocol scheduler

**Justification:** Preventive health depends on protocol timing by species, age, production stage, risk area, and regulatory requirement.

**Improvement:** Add vaccination protocols, due windows, booster rules, batch and lot capture, contraindications, missed-dose handling, and certificate evidence.

**Acceptance evidence:** Tests must generate due vaccinations, mark overdue animals, and reject completion without product lot and administrator evidence.

### 9. Treatment administration ledger

**Justification:** Treatments affect withdrawal, residue, welfare, cost, productivity, and auditability.

**Improvement:** Expand `treatment` with medication, dose, route, frequency, administrator, prescribing party, lot, reason, response, adverse reaction, and completion status.

**Acceptance evidence:** Tests must calculate treatment schedules and show incomplete treatments on the clinical workbench.

### 10. Withdrawal and residue controls

**Justification:** Milk, eggs, meat, and other outputs must not enter production channels during withdrawal periods.

**Improvement:** Add withdrawal intervals by product type, treatment, dose, jurisdiction, and animal output, then block sale or production release while active.

**Acceptance evidence:** Tests must prevent animals under active withdrawal from eligible sale or production rosters and display release dates.

### 11. Veterinary prescription boundary

**Justification:** The PBC must record veterinary authority without becoming a pharmacy, inventory, or external credential system.

**Improvement:** Store prescription references, veterinarian projection, authorization window, permitted treatments, and validation status through declared API/event dependencies.

**Acceptance evidence:** Boundary tests must prove veterinary data is consumed as projection evidence and no external professional registry table is mutated.

### 12. Disease outbreak investigation

**Justification:** Contagious disease management requires tracing contacts, groups, movements, treatments, and outcomes quickly.

**Improvement:** Add outbreak case clusters, suspected source, contact graph, isolation orders, testing status, control measures, and closure evidence.

**Acceptance evidence:** Tests must generate contact lists from owned movements and group intervals for a selected disease window.

### 13. Mortality and necropsy workflow

**Justification:** Deaths need cause analysis, carcass disposition, welfare review, and productivity impact.

**Improvement:** Add mortality records with discovered time, suspected cause, necropsy request, lab result projection, disposal method, regulatory notice, and corrective action.

**Acceptance evidence:** Tests must require disposition evidence before closing a mortality event and surface mortality trend metrics.

### 14. Welfare scoring and intervention tracking

**Justification:** Animal welfare is operational, ethical, and regulatory; it cannot be reduced to health events alone.

**Improvement:** Add welfare scorecards for body condition, lameness, behavior, housing, handling, heat stress, and intervention actions.

**Acceptance evidence:** Tests must flag low welfare scores, require intervention owner, and report unresolved welfare cases.

### 15. Breeding eligibility rules

**Justification:** Breeding decisions depend on age, weight, genetics, health, production status, relationship, and rest intervals.

**Improvement:** Expand `breeding_record` with eligibility checks, contraindications, planned service method, breeding objective, and rule-version evidence.

**Acceptance evidence:** Tests must reject ineligible breeding events and cite the failed eligibility rule.

### 16. Service, insemination, and mating records

**Justification:** Reproductive performance requires exact service events, semen or sire identity, technician, method, and timing.

**Improvement:** Add service events with method, sire or semen batch, technician, heat detection evidence, synchronization protocol, and repeat-service marker.

**Acceptance evidence:** Tests must calculate conception and repeat-service metrics from service events.

### 17. Pregnancy diagnosis and expected due dates

**Justification:** Herd planning depends on pregnancy status, expected calving/farrowing/lambing date, and risk flags.

**Improvement:** Add pregnancy checks with method, result, confidence, examiner, gestation estimate, expected date, and follow-up schedule.

**Acceptance evidence:** Tests must update reproductive status and generate due-date workbench queues.

### 18. Parturition and offspring linkage

**Justification:** Birth events connect dam, sire, offspring, birth weight, assistance, complications, and survival.

**Improvement:** Add parturition records with offspring creation, litter or calf identifiers, birth outcomes, assistance level, colostrum evidence, and dam recovery notes.

**Acceptance evidence:** Tests must create offspring records from an approved birth event and retain dam-offspring lineage.

### 19. Genetic and pedigree evidence

**Justification:** Breeding quality, inbreeding risk, disease traits, and market value depend on pedigree and genomic evidence.

**Improvement:** Add pedigree projections, genomic test references, trait markers, relationship coefficients, and breeding-risk warnings.

**Acceptance evidence:** Tests must warn on prohibited relationship thresholds and display pedigree evidence without owning external registry tables.

### 20. Feed ration formulation details

**Justification:** Feed cost, growth, milk output, health, and emissions depend on ration composition, not a free-text ration name.

**Improvement:** Expand `feed_ration` with ingredients, nutrient targets, dry matter, energy, protein, mineral balance, cost, effective dates, and assigned groups.

**Acceptance evidence:** Tests must reject ration assignment without required nutrient and ingredient evidence.

### 21. Feeding schedule and consumption tracking

**Justification:** Planned rations do not prove animals actually consumed feed or that refusals were monitored.

**Improvement:** Add feeding events with planned quantity, delivered quantity, refusals, feeding time, equipment, handler, weather context, and exception reason.

**Acceptance evidence:** Tests must calculate intake variance and surface underfed or overfed groups.

### 22. Feed inventory dependency boundary

**Justification:** The herd PBC needs feed availability but should not own warehouse stock or procurement.

**Improvement:** Consume feed inventory projections with lot, freshness, contaminant hold, quantity, and allocation status through declared events or APIs.

**Acceptance evidence:** Boundary tests must show ration execution uses feed projections and does not mutate inventory tables.

### 23. Pasture and grazing rotation plan

**Justification:** Grazing operations need paddock assignments, rest periods, forage availability, water access, and stocking pressure.

**Improvement:** Add grazing plans with paddock projection, entry and exit dates, forage estimate, animal units, rest requirement, and overgrazing alerts.

**Acceptance evidence:** Tests must warn when stocking density or rest period thresholds are breached.

### 24. Weight and growth monitoring

**Justification:** Growth performance drives feed decisions, market readiness, health investigation, and breeding eligibility.

**Improvement:** Add weight observations with scale source, condition, age-adjusted metrics, average daily gain, target curve, and anomaly detection.

**Acceptance evidence:** Tests must compute growth trends and flag animals deviating from expected curves.

### 25. Milk, egg, wool, or output productivity

**Justification:** Herd productivity differs by species and output type and needs time-series capture.

**Improvement:** Add output records by animal or group for milk, eggs, wool, fiber, honey, meat readiness, or other configured product metrics.

**Acceptance evidence:** Tests must aggregate output by group and detect output drops after health or feed events.

### 26. Movement permit lifecycle

**Justification:** Animal movement can require permits, certificates, inspections, quarantine, transport documents, and destination acceptance.

**Improvement:** Expand `movement_permit` with origin, destination, animals, transport party, certificate, inspection, route, permit status, and movement completion.

**Acceptance evidence:** Tests must block movement completion without approved permit and arrival confirmation.

### 27. Traceability from birth to sale

**Justification:** Buyers and regulators need a chain of custody across birth, groups, treatments, movements, and sale eligibility.

**Improvement:** Add traceability views that reconstruct animal lifecycle, health, treatment, feed, group, and movement history.

**Acceptance evidence:** Tests must generate a complete trace packet for an animal without external table reads.

### 28. Sale, transfer, cull, and slaughter readiness

**Justification:** Exit decisions depend on health status, withdrawal, weight, market class, welfare, and documentation.

**Improvement:** Add readiness checks for sale, transfer, culling, or slaughter with blocker reasons, approval, and destination projection.

**Acceptance evidence:** Tests must prevent exit approval when withdrawal, quarantine, or missing movement evidence exists.

### 29. Regulatory report generation

**Justification:** Livestock operations often must report disease events, movements, treatments, mortality, and inventory counts.

**Improvement:** Add report definitions with jurisdiction, reportable triggers, due dates, included records, approval status, and submission evidence.

**Acceptance evidence:** Tests must generate reports from owned records and open exceptions for overdue submissions.

### 30. Certification and audit readiness

**Justification:** Organic, humane, breed, export, food-safety, and quality schemes require auditable operational evidence.

**Improvement:** Add certification controls, required evidence by scheme, audit findings, corrective actions, and expiry monitoring.

**Acceptance evidence:** Tests must show certification readiness score and block certification claim when evidence is missing.

### 31. Controlled-substance and restricted treatment controls

**Justification:** Some treatments require special authority, logs, reconciliation, and tighter approval.

**Improvement:** Add restricted-treatment rules, authorization evidence, inventory projection, administrator verification, and exception escalation.

**Acceptance evidence:** Tests must require elevated permission for restricted treatment recording.

### 32. Antimicrobial stewardship analytics

**Justification:** Responsible antimicrobial use requires tracking drug class, indication, dose, duration, recurrence, and resistance concerns.

**Improvement:** Add stewardship metrics, repeated-use warnings, protocol deviation tracking, and review queues for veterinarian oversight.

**Acceptance evidence:** Tests must flag repeated antimicrobial use outside configured protocol windows.

### 33. Environmental and emissions indicators

**Justification:** Herd decisions affect methane, manure, land use, water, and feed-related footprint.

**Improvement:** Add sustainability indicators by group and production unit using feed, weight, output, manure handling projection, and configured emission factors.

**Acceptance evidence:** Tests must calculate emissions intensity and show assumptions used in the workbench.

### 34. Manure and waste handling coordination

**Justification:** Manure storage and application affect compliance, nutrient planning, and environmental risk.

**Improvement:** Add manure handling events with collection source, volume estimate, storage, application projection, spill risk, and corrective action.

**Acceptance evidence:** Tests must flag storage capacity breaches and link waste events to affected herd groups.

### 35. Heat stress and weather risk response

**Justification:** Weather extremes affect welfare, feed intake, fertility, mortality, and production.

**Improvement:** Consume weather projections and add heat-stress risk rules, mitigation tasks, hydration checks, shade status, and outcome tracking.

**Acceptance evidence:** Tests must create mitigation tasks for high-risk groups and verify closure evidence.

### 36. Staff tasking and competency requirements

**Justification:** Treatments, vaccinations, breeding, inspections, and handling require trained staff and accountability.

**Improvement:** Add task assignments with competency requirements, due windows, staff projection, completion evidence, and supervisor review.

**Acceptance evidence:** Tests must block assignment of restricted tasks to staff lacking required competency projection.

### 37. Equipment and facility readiness checks

**Justification:** Handling systems, chutes, scales, milking equipment, feeders, and transport crates can affect safety and data quality.

**Improvement:** Add readiness checks for equipment and facilities with inspection status, calibration projection, defect notes, and task blockers.

**Acceptance evidence:** Tests must block weight capture or treatment sessions when required equipment is out of service.

### 38. Mobile offline field capture

**Justification:** Barns, paddocks, and remote holdings often have unreliable connectivity.

**Improvement:** Add offline capture for health, treatment, movement, breeding, and weight events with device id, sync timestamp, conflict handling, and review queue.

**Acceptance evidence:** Tests must preserve original observation time and open conflicts instead of overwriting newer records.

### 39. Sensor and wearable data ingestion

**Justification:** Activity, rumination, temperature, location, and water intake sensors can reveal disease, estrus, stress, or equipment failures.

**Improvement:** Add sensor observation ingestion with device projection, signal quality, anomaly score, linked animal or group, and triage workflow.

**Acceptance evidence:** Tests must create reviewable alerts from abnormal sensor readings and ignore stale or low-quality signals.

### 40. Herd productivity dashboard

**Justification:** Operators need actionable metrics across health, reproduction, feed, mortality, growth, output, and compliance.

**Improvement:** Build workbench metrics for morbidity, mortality, conception, calving interval, feed conversion, growth, output, withdrawal, and open exceptions.

**Acceptance evidence:** UI contract tests must expose metric cards and drilldowns tied to owned records.

### 41. Exception taxonomy for herd operations

**Justification:** Generic exceptions hide the difference between animal welfare, compliance, health, feed, movement, and data-quality issues.

**Improvement:** Add exception categories, severity, blocker type, owner, due date, escalation policy, closure evidence, and reopen reason.

**Acceptance evidence:** Tests must route exception types to the correct workbench queues and emit exception events.

### 42. Herd rule and parameter workbench

**Justification:** Farmers, veterinarians, and compliance teams need governed configuration without source-code edits.

**Improvement:** Add UI controls for species profiles, withdrawal tables, health protocols, breeding eligibility, ration thresholds, movement rules, and alert parameters.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 43. Agent-assisted clinical note interpretation

**Justification:** Field notes, lab summaries, and veterinary instructions arrive as unstructured text or images.

**Improvement:** Add assistant skills that extract suspected diagnosis, treatment, follow-up, withdrawal, and tasks into governed CRUD previews.

**Acceptance evidence:** Tests must require human confirmation for writes and retain source-document evidence for each extracted field.

### 44. Agent-guided daily herd work plan

**Justification:** Operators need prioritized tasks for sick animals, due treatments, breeding checks, movements, feeding, welfare, and compliance.

**Improvement:** Add assistant-generated daily plan with task rationale, route grouping, dependencies, required equipment, and confirmation prompts.

**Acceptance evidence:** Tests must show task ordering uses due dates, severity, group location, and required competency.

### 45. Agent boundary and safety controls

**Justification:** AI assistance must not silently alter animal records, compliance status, or treatment evidence.

**Improvement:** Require agent proposals to declare command type, affected owned records, source evidence, confidence, policy checks, and approval requirement.

**Acceptance evidence:** Tests must reject agent writes without confirmation and log every accepted proposal.

### 46. AppGen-X event outbox and inbox specialization

**Justification:** Herd operations must coordinate with inventory, procurement, compliance, logistics, and finance without shared tables.

**Improvement:** Define typed emitted and consumed events for animal lifecycle, treatment, withdrawal, movement, productivity, and exception changes.

**Acceptance evidence:** Event contract tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 47. Cryptographic herd audit packet

**Justification:** Certifications, recalls, disputes, and regulatory reviews need tamper-evident evidence packages.

**Improvement:** Add hash-linked audit packets for animal lifecycle, treatment history, movement history, certification evidence, and report submissions.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 48. Data quality scoring

**Justification:** Missing birth dates, uncertain identifiers, stale group memberships, and unverified treatments undermine decisions.

**Improvement:** Add data quality scores by animal and herd group with issue type, severity, remediation task, and confidence trend.

**Acceptance evidence:** Tests must flag incomplete records and show remediation queues in the workbench.

### 49. Release smoke scenarios

**Justification:** The PBC needs evidence that the package can execute realistic livestock workflows after generation.

**Improvement:** Add smoke scenarios for new arrival quarantine, vaccination, treatment withdrawal, breeding, birth, movement permit, and sale readiness.

**Acceptance evidence:** Release evidence must show each scenario creates owned records, emits AppGen-X events, and respects boundary rules.

### 50. Cross-PBC boundary proof

**Justification:** Livestock workflows touch feed inventory, staff, transport, compliance, weather, finance, and sales domains but must retain owned boundaries.

**Improvement:** Add automated boundary proof that every generated model, service, route, handler, projection, and agent command uses only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on any undeclared table reference and pass for declared projection or event dependency references.
