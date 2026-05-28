# Agriculture Supply Chain Traceability Improvement Backlog

This backlog is intentionally hand-curated for the `agri_supply_chain_traceability` domain and focuses on traceability realities across farm lots, harvest batches, custody transfers, certifications, quality controls, storage, transport, recall readiness, provenance proof, sustainability claims, operator tooling, agent skills, event boundaries, and release evidence.

## Current Domain Evidence Used

- PBC key from manifest: `agri_supply_chain_traceability`.
- Current owned tables: `farm_lot`, `input_batch`, `certification`, `storage_event`, `transport_leg`, `recall_link`, `provenance_proof`, `agri_supply_chain_traceability_policy_rule`, `agri_supply_chain_traceability_runtime_parameter`, `agri_supply_chain_traceability_schema_extension`, `agri_supply_chain_traceability_control_assertion`, `agri_supply_chain_traceability_governed_model`.
- Current public APIs: `POST /farm-lots`, `POST /input-batchs`, `POST /certifications`, `POST /storage-events`, `POST /transport-legs`, `GET /agri-supply-chain-traceability-workbench`.
- Current emitted events: `AgriSupplyChainTraceabilityCreated`, `AgriSupplyChainTraceabilityUpdated`, `AgriSupplyChainTraceabilityApproved`, `AgriSupplyChainTraceabilityExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current advanced capabilities already declared: event-sourced operational history, anomaly detection, predictive risk scoring, counterfactual simulation, cryptographic audit proofs, carbon and sustainability awareness, semantic document understanding, and governed AI agent execution.
- Current documentation anchors: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Canonical farm lot identity and boundary model

**Justification:** Traceability breaks early when a farm lot can mean a field, a grower contract area, or a harvested pile depending on who entered the record. The package needs one canonical identity model for lot geography, crop season, ownership, and operational status.

**Improvement:** Define farm lot identity around grower, site, field block, season, crop, planting window, and status. Add explicit rules for retired lots, subdivided plots, leased land, and shared irrigation zones so downstream lineage stays stable.

**Acceptance evidence:** A farm lot contract with required keys and examples, migration notes for legacy lot records, and tests that reject overlapping active lot identities unless the overlap is explicitly modeled.

### 2. Harvest batch creation from farm lot reality

**Justification:** A farm lot is not the same thing as a harvest batch. The package needs harvest-batch lineage so traceability can follow real picking, cutting, threshing, and packing events rather than static field records.

**Improvement:** Add a harvest batch model linked to `farm_lot` with harvest date, crew, method, quantity, unit, containerization, and first receiving point. Support multiple harvest batches per lot and partial harvests across multiple days.

**Acceptance evidence:** Example traces from one farm lot to many harvest batches, validation rules for impossible harvest dates, and tests that prevent shipment creation for harvest batches with no source lot.

### 3. Split and merge lineage across batches

**Justification:** Agricultural traceability is mostly a split and merge problem. Grain bins, milk tanks, packhouse sort lines, and mixed pallets all break origin confidence if the lineage graph cannot represent merging and re-segmentation.

**Improvement:** Add first-class lineage operations for split, merge, rework, repack, and relabel events. Record quantitative contribution percentages so the blast radius of a contamination event can be calculated precisely.

**Acceptance evidence:** A lineage graph replay test covering split, merge, and repack flows, a residual percentage reconciliation check, and operator-visible lineage views that explain how a downstream batch was composed.

### 4. Input application evidence at lot and batch level

**Justification:** Seeds, fertilizer, crop protection chemicals, veterinary inputs, and cleaning agents often determine recall, certification, and sustainability outcomes. The package needs more than a generic `input_batch` record to prove what was applied, where, and when.

**Improvement:** Extend input tracking to cover supplier, formulation, active ingredients, application method, target lot or batch, operator, dose, pre-harvest interval, and withholding period. Support batch-level evidence for both crop and livestock supply chains.

**Acceptance evidence:** Input application records tied to lot or harvest-batch IDs, warnings when harvest occurs inside a withholding window, and audit-ready export views showing which inputs touched which saleable batches.

### 5. Certification validity windows and scope coverage

**Justification:** Certifications fail traceability programs when their scope is vague. Operators need to know whether a certificate covered the exact grower, site, commodity, and time period attached to a shipment.

**Improvement:** Model `certification` scope around certificate type, issuing body, holder, covered sites, covered commodities, validity start and end dates, suspension state, and evidence documents. Add rules for expired, suspended, superseded, and partial-scope certificates.

**Acceptance evidence:** Certificate coverage checks against lot, batch, and shipment dates, negative tests for expired and out-of-scope certificates, and a workbench panel that highlights which records are covered and which are not.

### 6. Chain-of-custody handoff event model

**Justification:** Chain of custody is the core promise of this package, yet the manifest surfaces focus on lots, storage, and transport. The backlog should explicitly close the gap between physical handoff events and digital lineage.

**Improvement:** Introduce custody transfer events with from-party, to-party, location, timestamp, seal state, quantity, packaging state, and receiving confirmation. Require custody continuity between harvest, storage, transport, processing, and dispatch.

**Acceptance evidence:** Tests that reject a dispatch if the previous custodian never accepted the goods, a timeline view showing every handoff, and discrepancy reports for unmatched ship/receive quantities.

### 7. Storage condition telemetry and exception capture

**Justification:** Storage is not a passive step for perishables, grains, seeds, dairy, or cold-chain produce. Temperature, humidity, aeration, fumigation, and dwell time directly affect quality, safety, and compliance.

**Improvement:** Extend `storage_event` to record storage zone, container, entry and exit times, target condition ranges, observed telemetry, treatment events, and exception reason codes. Support both manual readings and sensor-derived readings.

**Acceptance evidence:** Storage-event examples with sensor snapshots, alerts for threshold breaches, and end-to-end traces that show which saleable batches experienced a storage exception.

### 8. Cold-chain breach workflow

**Justification:** Cold-chain failures are among the fastest ways to turn a traceability record into a recall. The package needs an explicit domain path for quarantine, investigation, and disposition after a temperature excursion.

**Improvement:** Add a cold-chain breach workflow that can automatically quarantine affected batches, request QA review, record corrective action, and block release until disposition is complete. Surface time-above-threshold and severity scoring.

**Acceptance evidence:** A test scenario with a temperature excursion leading to automatic quarantine, an operator review screen with breach duration calculations, and release gating that stays blocked until QA disposition is recorded.

### 9. Transport leg seal integrity and vehicle hygiene evidence

**Justification:** A `transport_leg` record is too shallow if it only knows origin and destination. Agricultural traceability often depends on tamper seals, trailer cleanliness, and load compatibility.

**Improvement:** Extend `transport_leg` with vehicle identity, driver, seal numbers, pre-load sanitation check, prior load category, route plan, handoff condition notes, and delivery acceptance status. Add incompatibility rules for allergen, animal, chemical, and fresh produce loads.

**Acceptance evidence:** Transport-leg validation against incompatible prior loads, proof that seal numbers remained consistent across handoffs, and exception cards for broken or missing seal evidence.

### 10. Weight, count, and yield reconciliation

**Justification:** Traceability is weak when quantities drift without explanation. Operators need to reconcile harvested weight, stored quantity, shipped quantity, processed yield, shrinkage, and waste.

**Improvement:** Add quantitative reconciliation logic across lot, harvest batch, storage, transport, rework, and recall flows. Support unit conversions, moisture adjustments, pack-count conversions, and documented tolerance bands by commodity.

**Acceptance evidence:** Commodity-specific tolerance rules, reports that show unexplained gain or loss, and tests that require a reason code when reconciliation falls outside the allowed band.

### 11. Quality sampling plan linked to traceability units

**Justification:** Quality sampling often sits outside the traceability graph, which makes it difficult to understand whether a failing sample affected one pallet, one harvest batch, or an entire farm lot.

**Improvement:** Add sampling-plan entities tied to the exact traceability unit under review, including sampling method, sample size, sampler, lab destination, and disposition trigger. Support both routine and event-driven sampling.

**Acceptance evidence:** Sampling records linked to lot, harvest batch, or shipment IDs, sample-chain-of-custody documentation, and tests that prevent quality release when required samples are still pending.

### 12. Laboratory result lineage and disposition rules

**Justification:** Lab results only matter if the package can connect them to the affected lots and act on them consistently. This is especially important for pesticide residue, microbiology, mycotoxins, heavy metals, and adulteration checks.

**Improvement:** Add laboratory result entities with analyte, method, limit, result value, pass or fail interpretation, uncertainty, and source sample linkage. Drive automatic disposition proposals for quarantine, retest, downgrade, or destruction.

**Acceptance evidence:** Lab-result fixtures for pass, fail, and borderline cases, analyte-specific disposition rules, and trace views that show every downstream batch touched by a failed sample.

### 13. Contamination and hazard registry

**Justification:** Recalls need a consistent hazard vocabulary or every event becomes a free-text incident. The package needs a domain registry for biological, chemical, physical, and fraud-related hazards.

**Improvement:** Add a hazard registry with hazard type, regulatory significance, affected commodities, likely entry points, required actions, and severity logic. Link hazards to recalls, samples, storage exceptions, transport incidents, and supplier nonconformances.

**Acceptance evidence:** Hazard-code catalogs, incident examples that classify correctly, and recall rules that derive default actions from the selected hazard profile.

### 14. Recall blast-radius engine

**Justification:** During a contamination event, operators need the smallest accurate recall set, not a manual spreadsheet exercise. The package should calculate the blast radius directly from lineage, custody, and quantity contribution data.

**Improvement:** Add a recall impact engine that starts from a failed sample, suspect input, supplier notification, or transport incident and computes affected lots, batches, pallets, customers, and locations. Support forward and backward tracing.

**Acceptance evidence:** Simulated recall drills with computed impact sets, tests for both upstream and downstream tracing, and evidence that unaffected sibling batches remain outside the recall set.

### 15. Origin proof bundle and provenance pack

**Justification:** `provenance_proof` should be more than a document pointer. Buyers, regulators, and certification auditors need a reusable origin pack that proves geography, grower, custody, and handling history.

**Improvement:** Build provenance bundles that combine lot identity, harvest batch history, custody transfers, key certifications, storage and transport exceptions, and supporting documents into one verifiable package. Include optional geospatial evidence and signed attestations.

**Acceptance evidence:** A generated provenance pack for a sample batch, verification that every referenced event exists in the lineage chain, and export artifacts suitable for external review.

### 16. Sustainability claim traceability

**Justification:** Carbon, water, regenerative, and no-deforestation claims are only credible when they inherit from the same lineage graph as the physical product. Sustainability claims should not live in an isolated reporting layer.

**Improvement:** Attach sustainability attributes to lot, harvest, input, storage, and transport events with clear allocation logic to downstream batches. Record whether a claim is measured, estimated, inherited, or self-attested.

**Acceptance evidence:** Claim-allocation examples from farm lot to shipped batch, tests for mixed-claim merges, and a buyer-facing explanation that shows how each sustainability claim was derived.

### 17. Smallholder aggregator and collection-center model

**Justification:** Many agricultural programs source through aggregators and collection centers, not only directly from large farms. Traceability breaks when the model assumes a single grower per lot and a single dispatch point.

**Improvement:** Add support for aggregator networks, village collection centers, and pooled deliveries with contributor lists, contribution weights, receiving checkpoints, and segregation flags. Distinguish pooled traceability from identity-preserved traceability.

**Acceptance evidence:** Contributor-level lineage examples for pooled lots, rules that block identity-preserved claims on pooled batches, and receiving views that show who contributed to each pooled intake.

### 18. Grower attestation and seasonal compliance capture

**Justification:** Traceability programs often depend on field-level attestations such as no prohibited input use, water-source declarations, labor compliance, or harvest hygiene checks. These need structured capture, not ad hoc attachments.

**Improvement:** Add attestation records tied to season, lot, grower, or crew with question sets, evidence attachments, signature state, expiry rules, and reviewer outcomes. Allow attestation versioning as standards evolve.

**Acceptance evidence:** Structured attestation forms, tests for expired or missing attestations blocking shipment release, and audit views showing who signed and who reviewed each attestation.

### 19. Mixed-commodity and co-product handling

**Justification:** Real facilities handle co-products, by-products, grade-outs, and mixed commodities. The package needs to represent when traceability branches into feed, waste, processing input, or downgraded sale channels.

**Improvement:** Add handling rules for commodity conversion, co-product creation, grade changes, and non-food diversion. Preserve lineage links even when a batch becomes waste, animal feed, or industrial input.

**Acceptance evidence:** Conversion scenarios with preserved lineage, disposition categories for downgraded outputs, and reports that show where every kilogram or unit ended up after grading or processing.

### 20. Repack, relabel, and palletization lineage

**Justification:** Consumer-facing units often change repeatedly after harvest. Repacking and relabeling can sever traceability unless the package records packaging transformations as first-class events.

**Improvement:** Add events for repack, relabel, pallet build, pallet break, carton substitution, and label correction. Require source-to-output quantity reconciliation and preserve all packaging identifiers used in commerce.

**Acceptance evidence:** Pallet-level lineage screens, tests for relabel without source linkage, and ability to trace a consumer unit code back to the contributing harvest batches.

### 21. Shrinkage, loss, and waste accounting

**Justification:** Agricultural product dehydrates, spoils, spills, and gets reworked. Without structured shrinkage and waste events, the lineage graph cannot explain why physical and digital stock diverged.

**Improvement:** Add explicit loss, spoilage, waste, and destruction events with reason codes, measured quantity, approval requirements, and whether the loss affects recall scope or sustainability claims.

**Acceptance evidence:** Reconciliation reports that incorporate shrinkage, approval logs for destruction events, and tests that prevent silent quantity disappearance from active stock.

### 22. Traceability exception taxonomy and triage queue

**Justification:** The package emits a generic exception event, but operators need a domain vocabulary for what kind of traceability problem occurred. Missing custody, failed certificate coverage, unresolved quantity gap, and contaminated storage are different operational problems.

**Improvement:** Define exception classes, severities, owners, due-date logic, blocking impact, and remediation playbooks. Prioritize exceptions by food safety, compliance exposure, and customer-shipment risk.

**Acceptance evidence:** Exception queues grouped by severity and class, SLA timers per exception type, and sample remediation playbooks for missing origin proof, failed lab result, and broken cold chain.

### 23. Traceability graph explorer workbench

**Justification:** Operators need to see the graph, not infer it from row lists. A lineage-heavy domain deserves a graph-first workbench for investigation and proof assembly.

**Improvement:** Add a graph explorer that can pivot from farm lot, harvest batch, storage event, transport leg, recall, or provenance proof and show upstream and downstream neighbors with event timestamps and quantities.

**Acceptance evidence:** Interactive graph views for forward and backward tracing, stable node and edge semantics, and screenshots or route tests proving that graph navigation works for complex split-and-merge scenarios.

### 24. Receiving and intake workbench

**Justification:** Traceability quality is won or lost at receiving. The package needs a purpose-built intake workbench for field receipts, weighbridge tickets, collection-center deliveries, and first receiving inspections.

**Improvement:** Build a receiving workbench with fast lot lookup, harvest-batch intake, document capture, discrepancy handling, and immediate hold or quarantine actions. Support commodity-specific receiving checklists.

**Acceptance evidence:** Intake flows for lot receipt and pooled delivery, discrepancy review queues, and permission-aware actions for receiving clerks, supervisors, and QA reviewers.

### 25. Recall command center workbench

**Justification:** Recall response needs one place for impact calculation, communication status, action tracking, and evidence collection. Operators cannot coordinate a contamination event from a generic detail page.

**Improvement:** Add a recall workbench showing suspect trigger, affected lineage, customer and location reach, contact status, hold status, return or destruction status, and required regulator notifications. Include a drill mode and a live mode.

**Acceptance evidence:** Drill scenario outputs, communication task tracking, hold-status dashboards, and evidence bundles that can be attached to `RELEASE_EVIDENCE.md` or recall review records.

### 26. Certification and compliance workbench

**Justification:** Certifications, attestations, and policy checks need a dedicated view because they cut across lots, batches, shipments, and suppliers. Compliance reviewers need a surface that explains scope gaps and expiring coverage quickly.

**Improvement:** Add a compliance workbench for certificate coverage, attestation status, pending renewals, blocked shipments, and policy overrides. Support filtering by grower, site, commodity, buyer program, and region.

**Acceptance evidence:** Coverage dashboards, renewal queues, override audit views, and scenario tests that show how an expiring certificate blocks specific batches and shipments.

### 27. Agent skill for document-led intake

**Justification:** Traceability teams spend large amounts of time transcribing grower declarations, transport manifests, lab reports, and certificates. The package already declares semantic document understanding and governed AI execution, so the backlog should turn that into a concrete operator skill.

**Improvement:** Add an agent skill that extracts candidate records from documents, maps them to farm lot, harvest batch, certification, storage, or transport entities, and presents a diff for operator confirmation. Require source citation for every suggested field.

**Acceptance evidence:** Example agent sessions on certificates and weighbridge tickets, field-level citation links, confidence thresholds, and blocked writes when confidence or permissions are below the allowed threshold.

### 28. Agent skill for recall investigation and evidence assembly

**Justification:** During a contamination event, teams need fast answers grounded in the actual lineage graph. A governed investigation skill can accelerate impact assessment without bypassing domain controls.

**Improvement:** Add an agent skill that assembles suspect lineage, summarizes relevant storage and transport exceptions, identifies impacted customers or locations, and drafts a recall evidence pack for human review. Keep all recommendations tied to underlying records and events.

**Acceptance evidence:** Investigation transcripts with source-linked findings, impact summaries that match the recall engine output, and approval-gated export of the assembled recall pack.

### 29. API boundary completeness and naming cleanup

**Justification:** The current manifest exposes only a small set of create endpoints and one workbench read route, and one route name uses the awkward `input-batchs` form. A mature traceability package needs explicit command and query boundaries.

**Improvement:** Expand the backlog to cover validation-only commands, correction commands, search and filter reads, lineage queries, recall simulation, provenance export, and workbench projection endpoints. Clean up API naming so batch resources read consistently and clearly.

**Acceptance evidence:** A route catalog that distinguishes commands from queries, compatibility rules for route evolution, and tests for idempotency, pagination, and explicit correction semantics.

### 30. Event taxonomy for traceability state changes

**Justification:** Generic created and updated events are not enough for downstream consumers that need to react differently to quarantine, release, certificate suspension, recall opening, or custody transfer. Event boundaries should encode domain meaning.

**Improvement:** Define a richer event set for lot registered, harvest batch created, custody transferred, storage breach detected, certificate suspended, recall opened, recall narrowed, provenance pack issued, and sustainability claim revised. Keep payloads typed and versioned.

**Acceptance evidence:** Event contracts with examples, compatibility notes for version bumps, and replay tests that rebuild core traceability projections from the event stream.

### 31. Idempotent command handling for physical-world retries

**Justification:** Field devices, collection-center kiosks, and transport integrations often retry the same command after weak connectivity. The package needs strong idempotency at the boundary where physical events enter the system.

**Improvement:** Require idempotency keys for intake, custody transfer, storage entry, storage exit, transport dispatch, transport receipt, and recall actions. Preserve the original command result so repeat submissions do not fork lineage.

**Acceptance evidence:** Retry tests for duplicate submissions, evidence that repeated custody or dispatch commands do not create duplicate events, and operator-visible messages that explain when an incoming command was deduplicated.

### 32. Release evidence pack for traceability readiness

**Justification:** The manifest already declares `RELEASE_EVIDENCE.md`, so the backlog should explicitly define what release evidence means in a traceability package. Readiness must prove the lineage chain, not only test counts.

**Improvement:** Standardize release evidence around sample end-to-end traces, recall drill outputs, certificate coverage checks, workbench screenshots, event replay checks, and agent-skill guardrail evidence. Make it easy to compare one release to the previous release.

**Acceptance evidence:** A release checklist template, artifacts for a representative farm-lot-to-shipment trace, and signed evidence that a recall drill and provenance export succeeded on the release candidate.

### 33. Policy and rule versioning with effective dating

**Justification:** Traceability rules change with seasons, customers, commodity programs, and regulations. Investigations later depend on knowing which policy version was in force when a batch moved.

**Improvement:** Add effective-dated policy versions for certificate coverage, quarantine thresholds, sampling rules, origin-proof requirements, and sustainability claim logic. Preserve the applied policy version on every decision and exception.

**Acceptance evidence:** Time-travel checks showing how a historical record was evaluated, diff views between policy versions, and replay tests confirming that historical decisions remain explainable after policy updates.

### 34. Sustainability scenario simulation

**Justification:** Sustainability claims are operational decisions, not only reporting outputs. Operators need to understand how route choices, storage delays, and input substitutions change claim quality before they commit them.

**Improvement:** Extend simulation to compare carbon, water, waste, and claim-eligibility outcomes for alternative transport routes, cold-store dwell times, packaging choices, and input programs. Show whether a scenario breaks an existing buyer claim.

**Acceptance evidence:** Side-by-side simulation outputs, claim-eligibility warnings for losing a program qualification, and examples where one routing choice preserves a sustainability claim while another invalidates it.

### 35. Risk scoring for storage and transport exposure

**Justification:** Predictive risk should focus on the places where traceability problems become food safety problems. Storage and transport conditions are rich predictors of quality and contamination exposure.

**Improvement:** Train risk models on dwell time, route duration, seal breaks, prior load class, telemetry excursions, repeat supplier incidents, and overdue sampling. Surface risk at lot, batch, shipment, and facility levels.

**Acceptance evidence:** Feature manifests, score explanation cards, monitored drift metrics, and test scenarios where known high-risk combinations receive materially higher risk scores.

### 36. Counterfactual routing and hold-release analysis

**Justification:** When a batch is at risk, operators need to compare alternatives quickly. Counterfactual analysis should answer whether rerouting, holding, or repacking would narrow risk or preserve customer commitments.

**Improvement:** Add a what-if tool for route changes, alternate cold stores, delayed shipment, additional sampling, partial hold, and selective recall. Show impact on lineage, customer reach, shelf-life, and sustainability claims.

**Acceptance evidence:** Scenario comparisons with clear outcome deltas, saved simulation records, and evidence that simulations do not mutate live traceability data.

### 37. Jurisdiction and tenant isolation for multi-program traceability

**Justification:** Different buyers, regions, and operating companies may require different traceability rules for the same commodity. The package needs isolation without duplicating the entire product for each program.

**Improvement:** Support tenant and jurisdiction layers for policies, workbench defaults, certificate rules, recall thresholds, and export formats. Ensure one tenant cannot see another tenant's growers, batches, or incident evidence.

**Acceptance evidence:** Isolation tests across tenant and region combinations, negative permission checks, and policy examples where one jurisdiction requires a stronger recall threshold than another.

### 38. Retention, legal hold, and evidence preservation

**Justification:** Traceability investigations often outlive normal operational retention windows. The package should preserve the right records when litigation, regulator review, or customer dispute requires a legal hold.

**Improvement:** Add retention policies by record class, legal-hold flags for active incidents, and preservation logic for linked lineage, documents, events, and agent-generated evidence. Make deletion policy visible and auditable.

**Acceptance evidence:** Retention schedules by entity type, tests that prevent deletion while legal hold is active, and audit records showing who placed and released each hold.

### 39. Offline field and collection-center capture

**Justification:** Many agricultural environments have unreliable connectivity. Traceability packages that assume always-online entry produce paper workarounds and later transcription errors.

**Improvement:** Add offline-capable capture for harvest, receiving, custody, sampling, and storage readings with sync conflict handling and durable local queueing. Preserve original capture time and device identity when syncing later.

**Acceptance evidence:** Offline capture scenarios, conflict-resolution rules, tests for duplicate sync attempts, and evidence that delayed sync still preserves correct lineage ordering.

### 40. Scan-first mobile UX for lots, pallets, and containers

**Justification:** Traceability data entry should follow the movement of physical goods. Mobile scanning reduces manual entry errors during receiving, storage moves, loading, and recall verification.

**Improvement:** Add scan-first flows for lot codes, pallet IDs, container IDs, seal numbers, and shipment IDs with commodity-specific shortcuts. Support scanning to confirm custody transfer, quarantine placement, and recall hold execution.

**Acceptance evidence:** Mobile route tests, scanned-code validation against known entities, and user flows proving that a receiving or loading task can be completed with scan-driven interactions instead of manual search.

### 41. Packaging and label evidence management

**Justification:** Packaging codes and labels are what downstream customers and regulators often see first. The package should keep packaging and label evidence tightly linked to provenance and recall logic.

**Improvement:** Record packaging runs, label templates, print lots, date codes, and label corrections as traceability events. Link every consumer-facing code to the originating batch set and packaging session.

**Acceptance evidence:** Reverse lookup from a consumer code to source batches, packaging-run trace screens, and tests that prevent label reprints from silently changing the linked source batch set.

### 42. Substitution, adulteration, and fraud anomaly detection

**Justification:** Not every traceability failure is accidental. The package should look for quantity, origin, and quality patterns that suggest substitution, dilution, or document fraud.

**Improvement:** Add anomaly signals for impossible origin hops, suspicious certificate reuse, quantity inflation, repeated relabeling, inconsistent grade shifts, and document-content mismatch. Prioritize high-severity signals for manual review.

**Acceptance evidence:** Fraud-oriented test fixtures, anomaly cards with feature explanations, reviewer feedback capture, and suppression controls so known false positives do not flood the queue.

### 43. Supplier and grower corrective action tracking

**Justification:** Traceability programs improve when incidents lead to corrective action, not only closed tickets. The package should connect nonconformances to remediation plans and follow-up evidence.

**Improvement:** Add corrective-action plans tied to hazards, failed certificates, failed samples, and recurring storage or transport incidents. Track owner, due date, verification visit, and whether future lots remain blocked pending closure.

**Acceptance evidence:** Corrective-action queues, recurrence tracking for suppliers and growers, and tests showing that unresolved severe corrective actions can block new batch approval.

### 44. Projection freshness and rebuild guarantees

**Justification:** Workbenches will depend on projections, and stale projections undermine trust during incidents. The package should expose whether graph, recall, and compliance views are fresh enough for decision making.

**Improvement:** Add freshness timestamps, lag indicators, rebuild tooling, and projection checksums for lineage, recall, compliance, and analytics read models. Make stale projections visible rather than silently serving outdated data.

**Acceptance evidence:** Projection lag monitors, rebuild runbooks, replay checksums, and tests that flag workbench views as stale when event processing falls behind defined thresholds.

### 45. Controlled schema extension for commodity-specific needs

**Justification:** Agricultural traceability differs by commodity. Coffee, dairy, aquaculture, fresh produce, seed, and grain each need extra attributes, but uncontrolled schema growth would fracture the package.

**Improvement:** Use `agri_supply_chain_traceability_schema_extension` as a governed extension registry for commodity-specific fields, rules, and UI fragments. Require ownership, validation rules, and migration evidence for every extension.

**Acceptance evidence:** Extension registration examples for at least two commodities, validation tests that enforce extension ownership, and release evidence showing that extensions do not break core lineage and recall flows.

### 46. Seed data and demo narratives that reflect the domain

**Justification:** Weak seed data hides domain gaps. Traceability packages need seeded scenarios that look like real agricultural operations, including harvest waves, storage moves, transport legs, quality incidents, and recalls.

**Improvement:** Build seed narratives for at least one perishable crop and one durable commodity with realistic lot structures, harvest batches, certifications, quality samples, storage events, transport legs, and one recall drill path. Use them in demos and regression checks.

**Acceptance evidence:** Seed datasets with documented storylines, deterministic IDs for replayable demos, and verification that each seed narrative exercises lineage, compliance, and recall features end to end.

### 47. Negative-path test suite for contamination and recall

**Justification:** Traceability systems often test the happy path and then fail in the exact moments they are needed. The backlog should explicitly demand negative-path coverage for the hardest domain moments.

**Improvement:** Add scenario suites for failed lab results, missing custody confirmation, broken cold chain, expired certificate, conflicting origin proof, duplicate dispatch, and partial recall closure. Include buyer and regulator communication steps where relevant.

**Acceptance evidence:** Automated scenario tests, expected hold and quarantine outputs, and evidence that each negative case creates the right exception, event, and workbench state.

### 48. Human override governance and reason capture

**Justification:** Agricultural operations sometimes require overrides, but overrides without context destroy audit trust. The package needs strict controls around who can override what and why.

**Improvement:** Add override types for release under review, quantity tolerance approval, certificate waiver, delayed sampling acceptance, and manual lineage correction. Require reason codes, approver identity, expiry, and follow-up review for every override.

**Acceptance evidence:** Override audit records, permission tests for high-risk overrides, expiry checks, and views that clearly distinguish normal decisions from overridden decisions.

### 49. Quality release gate before customer shipment

**Justification:** Traceability value peaks at release time, when the package should decide whether product can move. Lots and batches should not ship if required lineage, quality, or compliance evidence is incomplete.

**Improvement:** Add a pre-shipment release gate that checks lineage completeness, certificate scope, pending hazards, storage and transport exceptions, pending lab results, and unresolved corrective actions. Produce a release verdict with explainable blockers.

**Acceptance evidence:** Shipment-release verdict records, tests for blocked and passed releases, and operator views that show which missing evidence prevented release for a specific batch or shipment.

### 50. End-to-end provenance and recall release drill

**Justification:** The strongest proof of readiness is an end-to-end drill that starts with a farm lot and ends with both a customer-ready provenance pack and a regulator-ready recall response. This ties together the package's domain promise and its release evidence.

**Improvement:** Define a repeatable release drill that covers farm lot registration, harvest batch creation, input applications, storage, transport, quality sampling, certificate validation, provenance-pack export, and a simulated contamination recall on the same lineage set. Require the drill before major releases of `agri_supply_chain_traceability`.

**Acceptance evidence:** A recorded drill run with timestamps, generated provenance and recall artifacts, event replay verification, workbench screenshots, and sign-off that the release candidate passed the traceability drill without manual database intervention.
