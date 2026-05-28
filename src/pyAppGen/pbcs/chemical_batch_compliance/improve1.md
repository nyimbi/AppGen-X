# Chemical Batch Compliance Improvement Backlog

This backlog is hand-curated for the `chemical_batch_compliance` PBC and focuses on the chemical manufacturing, quality, safety, and regulatory depth implied by the current manifest.

## Current Domain Evidence Used

- Manifest key: `chemical_batch_compliance`
- Manifest description: chemical formulas, batches, SDS, hazardous materials, regulatory submissions, quality, and compliance controls
- Owned tables: `chemical_formula`, `batch_record`, `sds_document`, `hazardous_material`, `regulatory_submission`, `quality_test`, `compliance_hold`, `chemical_batch_compliance_policy_rule`, `chemical_batch_compliance_runtime_parameter`, `chemical_batch_compliance_schema_extension`, `chemical_batch_compliance_control_assertion`, `chemical_batch_compliance_governed_model`
- Public APIs: `POST /chemical-formulas`, `POST /batch-records`, `POST /sds-documents`, `POST /hazardous-materials`, `POST /regulatory-submissions`, `GET /chemical-batch-compliance-workbench`
- Emitted events: `ChemicalBatchComplianceCreated`, `ChemicalBatchComplianceUpdated`, `ChemicalBatchComplianceApproved`, `ChemicalBatchComplianceExceptionOpened`
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- Workflows: `chemical_batch_compliance_create_chemical_formula_workflow`, `chemical_batch_compliance_record_batch_record_workflow`
- UI fragments: `ChemicalBatchComplianceWorkbench`, `ChemicalBatchComplianceDetail`, `ChemicalBatchComplianceAssistantPanel`
- Release documents already named in the manifest: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`

### 1. Master recipe versioning with effectivity windows

**Justification:** `chemical_formula` should behave like a controlled master recipe, not a mutable record that quietly changes under released batches. Chemical operations need revision history for composition, target yield, scale range, and required safety notes.

**Improvement:** Introduce explicit recipe revisions with draft, technical review, quality approval, EHS approval, effective, superseded, and withdrawn states. Each revision should capture ingredient list, target batch size band, allowable line or plant, revision reason, superseded version, and mandatory SDS or permit references.

**Acceptance evidence:** The workbench shows side-by-side revision diffs, new batches always bind to one released recipe revision, expired revisions cannot be chosen for new work, and historical batches still resolve the recipe content that was effective at execution time.

### 2. Formula composition, potency, and tolerance control

**Justification:** Chemical formulations often require potency correction, concentration balancing, density adjustments, and tolerance checking rather than simple fixed quantities. Without this, the system cannot prove that an executed batch matched its intended chemistry.

**Improvement:** Model target concentration, min/max composition windows, assay-adjusted additions, density or temperature compensation rules, and critical material tolerances for each master recipe revision. Flag which formula attributes are critical-to-quality and which can vary inside approved bands.

**Acceptance evidence:** Formula review screens show calculated target versus allowed range, dispensed quantities reconcile back to corrected recipe intent, and out-of-band composition changes force a deviation or a revised recipe rather than an informal edit.

### 3. Controlled raw-material substitution and source approval

**Justification:** Substituting one raw material or supplier lot for another can change impurity profile, hazard classification, transport status, or final product claims. A chemical batch system needs formal controls around equivalence, not informal operator judgment.

**Improvement:** Add approved-substitute rules for raw materials with required supplier qualification, equivalence rationale, impurity comparison, SDS review, and quality or regulatory approval thresholds. Separate emergency substitution from standard source approval so riskier substitutions receive stronger review.

**Acceptance evidence:** Only approved alternatives appear during batch preparation, emergency substitutions generate visible exception records with approver identity, and genealogy reports preserve both the planned material and the actually consumed substitute lot.

### 4. Stepwise electronic batch execution records

**Justification:** `batch_record` needs to represent actual manufacturing sequence, not only batch header metadata. Release, deviation review, and investigation all depend on step order, dwell time, and sign-off evidence.

**Improvement:** Represent the batch record as a structured sequence of phases, steps, checkpoints, operator actions, supervisor sign-offs, and step-completion conditions. Critical steps should support pause, repeat, rollback, or hold states with reason capture.

**Acceptance evidence:** Executed batches show ordered step timelines with timestamps and actors, critical steps cannot be skipped silently, and review packets expose where the batch paused, repeated, or diverged from the expected execution path.

### 5. Equipment readiness and line-clearance enforcement

**Justification:** Cross-contamination, wrong-vessel usage, and stale cleaning status are common chemical manufacturing failure modes. Batch execution should not begin when equipment state is unknown or unsuitable for the recipe.

**Improvement:** Add pre-start checks for equipment assignment, line clearance, previous product campaign, cleaning-release state, calibration state, and maintenance lockout. Master recipes should declare which equipment classes are allowed or forbidden for each step.

**Acceptance evidence:** Batch start is blocked when assigned equipment lacks line clearance or approved cleaning, the record shows which equipment executed each step, and changeover risk is visible before material is dispensed.

### 6. Weigh-and-dispense reconciliation

**Justification:** Small weighing errors can materially change potency, reaction outcome, and downstream regulatory status. Chemical operations need reconciliation between planned additions and actual dispenses at container level.

**Improvement:** Track planned quantity, actual quantity, unit, container ID, balance used, operator, verifier, and correction reason for each dispense. Require stronger verification for potent toxics, highly reactive materials, or additions with very tight tolerances.

**Acceptance evidence:** Dispense panels show variance against target, unresolved misweighs open exceptions before the batch can proceed, and the audit trail preserves any corrected or partially discarded dispense attempts.

### 7. Process parameter capture with action and alarm bands

**Justification:** Temperature, pH, agitation speed, feed rate, pressure, vacuum, hold time, and similar process parameters determine whether a batch remains within validated conditions. Chemical compliance depends on preserving both parameter targets and excursion handling.

**Improvement:** Define setpoint, advisory band, alarm band, action limit, sampling trigger, and deviation trigger for critical process parameters. Let each batch step capture actual values, manual overrides, and justification for operating outside preferred conditions.

**Acceptance evidence:** Parameter trends are visible during execution and review, alarm-limit breaches are time-stamped and linked to response actions, and quality review can distinguish minor drift from formal process deviations.

### 8. Risk-based in-process sampling plans

**Justification:** In-process samples are how operators prove that a reaction, blend, or purification step is ready for the next phase. Sampling needs to be tied to process state and risk, not treated as a generic checkbox.

**Improvement:** Add sampling plans that trigger by phase completion, elapsed hold time, parameter threshold, or intermediate appearance. Each plan should declare required tests, minimum result set for progression, and which sample points support batch release versus process steering only.

**Acceptance evidence:** Step progression is blocked when required in-process samples are missing, the workbench shows pending and completed sample points per batch, and sample plans differ appropriately by recipe revision and risk profile.

### 9. Sample chain-of-custody and split-sample management

**Justification:** A sample result is only defensible if sample identity, storage condition, and custody are preserved. Chemical investigations often fail because sample lineage is weaker than batch lineage.

**Improvement:** Give every collected sample a unique identifier, storage condition, custody log, split-sample relationship, retain status, and disposal record. Support transfers between production, QC, stability storage, and external labs without breaking traceability.

**Acceptance evidence:** Users can trace any reported result back to the exact batch step and sample container, split samples remain linked to the original draw, and custody gaps surface as visible exceptions instead of hidden omissions.

### 10. QC specification profiles and release limits

**Justification:** `quality_test` should encode recipe-specific and product-specific specifications, not only a loose list of test names. Final release depends on agreed limits, result interpretation rules, and correct method versions.

**Improvement:** Create specification profiles for raw materials, intermediates, finished batches, stability pulls, and retain samples with method version, units, rounding rules, composite-release logic, and conditional tests triggered by known risks. Separate informational tests from true disposition-driving tests.

**Acceptance evidence:** Each result is evaluated against the correct spec profile version, release decisions show which tests were disposition-driving, and changed specification limits never retroactively alter old batch release decisions.

### 11. OOS and OOT investigation workflow

**Justification:** Out-of-specification and out-of-trend results are core compliance events in chemical manufacturing. They require structured investigation pathways so the system can distinguish lab error, manufacturing error, and emerging drift.

**Improvement:** Build dedicated workflows for initial laboratory assessment, manufacturing assessment, retest authorization, resample authorization, impact scope, and final disposition. Preserve the difference between confirmed OOS, invalid test, OOT warning, and still-open investigation.

**Acceptance evidence:** OOS packets show all required investigation stages, retest authority is explicitly recorded, open OOS states block lot release, and trending views separate single-result failures from repeated drift toward the limit.

### 12. Deviation, incident, and CAPA linkage

**Justification:** Process excursions, documentation errors, and safety incidents should not live in disconnected records. Quality needs one chain from deviation identification to corrective and preventive action completion.

**Improvement:** Add deviation classification, severity, immediate containment, impact assessment, CAPA tasks, effectiveness checks, recurrence linkage, and closure evidence. Allow deviations to originate from process excursions, sample problems, documentation edits, or permit breaches.

**Acceptance evidence:** Major deviations open from the triggering batch or QC context, CAPA tasks remain attached until effectiveness is verified, and repeat deviations are discoverable as a related pattern rather than isolated cases.

### 13. Rework, reblend, and yield-loss governance

**Justification:** Chemical sites frequently need to rework off-spec material, reblend borderline lots, or explain material losses. Those actions materially affect genealogy, release testing, and regulatory claims.

**Improvement:** Model approved rework routes, reblend formulas, additional testing requirements, yield-loss reason codes, and reprocessing approval thresholds. Require the system to distinguish routine yield adjustment from exceptional recovery of nonconforming material.

**Acceptance evidence:** Reworked lots carry parent-child lineage, reblend decisions show the recipe logic and approvals used, and yield-loss reporting separates planned process loss from unexplained shrinkage.

### 14. End-to-end lot genealogy

**Justification:** Chemical batch compliance is incomplete without forward and backward traceability across raw materials, intermediates, finished lots, samples, waste, and rework. Genealogy is the backbone for release, complaint investigation, and recall readiness.

**Improvement:** Build a genealogy model that links incoming lots, dispenses, intermediate pools, packaging lots, retained samples, waste outputs, and customer-distributed lots. Include quantity splits and merges so the model supports both trace-forward and trace-back reasoning.

**Acceptance evidence:** A user can start from any finished lot and reach all contributing material lots, related samples, waste streams, and rework branches, and the same graph supports immediate impact scoping for complaints or recalls.

### 15. Retain samples and stability program tracking

**Justification:** Release evidence often depends on the ability to produce retain material or demonstrate ongoing stability. Chemical systems need to manage retain obligations, chamber conditions, and pull schedules explicitly.

**Improvement:** Add retain-sample reservation, storage location, stability chamber assignment, pull schedule, retest plan, and shelf-life extension logic. Tie retained material obligations to recipe revision, finished product family, and jurisdiction where requirements differ.

**Acceptance evidence:** The system can show which retains exist for a released lot, when the next stability pull is due, whether chamber conditions stayed within range, and how stability outcomes affected expiry or retest status.

### 16. SDS section-level obligation extraction

**Justification:** `sds_document` should be a source of structured operating obligations, not just a file attachment. Key duties in storage, handling, PPE, firefighting, first aid, spill response, and disposal sit inside SDS sections that operators need at execution time.

**Improvement:** Parse SDS content into structured obligations for hazard classification, incompatible materials, exposure controls, handling notes, storage conditions, transport restrictions, waste handling, and emergency response. Keep the source section and page reference for every extracted obligation.

**Acceptance evidence:** Hazard and handling panels cite the originating SDS section, extracted obligations can be reviewed against the source document, and recipe or hazardous-material screens surface the exact SDS-derived constraints that apply.

### 17. SDS revision impact assessment

**Justification:** An SDS revision can change hazard class, exposure limit, storage instruction, or transport classification after a material is already in use. The system needs to tell users which active recipes, inventories, and labels are affected.

**Improvement:** Compare old and new SDS versions at section level and generate impact findings for active formulas, hazardous-material records, workplace inventories, and open batches. Flag whether the revision forces relabeling, retraining, storage reassessment, or permit review.

**Acceptance evidence:** SDS updates generate a visible impact summary, affected materials and batches are listed before the new version is adopted, and the workbench records which downstream records were reviewed or updated because of the revision.

### 18. Hazardous material segregation and storage compatibility

**Justification:** Incompatible storage of oxidizers, reducers, acids, bases, flammables, water-reactives, and toxics creates immediate safety risk. `hazardous_material` needs operational storage rules, not only classification metadata.

**Improvement:** Add compatibility matrices, segregation zones, quantity limits, temperature requirements, container constraints, and secondary-containment expectations to hazardous-material records. Link storage eligibility to SDS instructions, hazard class, and site-specific layout rules.

**Acceptance evidence:** Location assignment blocks incompatible combinations, storage dashboards show overloaded or mismatched zones, and the hazard record explains which compatibility rule triggered each exception.

### 19. GHS label, pictogram, and workplace inventory control

**Justification:** Hazard communication must reflect actual composition and current classification, especially after recipe changes or SDS revisions. Chemical operations need consistent labeling across batch containers, storage areas, and workplace inventories.

**Improvement:** Generate GHS-aligned labels with signal word, hazard statements, precautionary statements, pictograms, concentration-dependent wording, and local inventory identifiers. Update workplace inventory rollups based on actual lot state, storage location, and quantity on hand.

**Acceptance evidence:** Label previews can be produced from a hazardous-material or batch context, workplace inventory reports reconcile to active lot quantities, and classification changes automatically queue relabeling or inventory review tasks.

### 20. Exposure controls, PPE, and permit-to-work gating

**Justification:** Some chemical operations require respirators, local exhaust verification, hot-work permits, confined-space permits, or special handling authorization. Those prerequisites should block execution when missing.

**Improvement:** Allow recipe steps and hazardous-material operations to declare required PPE, engineering controls, permit types, and exposure-monitoring prerequisites. Record when controls were confirmed, who authorized them, and whether temporary overrides were used.

**Acceptance evidence:** Critical steps cannot start until required permits and PPE checks are satisfied, expired permits or missing control confirmations surface immediately, and execution history shows exactly which safety gate was used for each high-risk step.

### 21. Environmental permit and discharge or emission limit checking

**Justification:** Solvent usage, volatile emissions, wastewater constituents, scrubber loads, and hazardous air pollutants can all be regulated at plant level. Batch execution should reflect environmental permit limits before violations occur.

**Improvement:** Tie recipes and batch records to environmental permit constraints such as VOC caps, wastewater concentration limits, batch-frequency restrictions, stack emission calculations, and reporting triggers. Compare planned and actual operations against remaining permit headroom.

**Acceptance evidence:** Permit dashboards show utilization by site and period, batches forecast potential breaches before execution, and actual process data can be rolled into environmental reporting evidence without manual reconstruction.

### 22. Waste stream classification and disposal evidence

**Justification:** Chemical waste handling is a direct compliance surface, especially for spent solvents, contaminated containers, off-spec product, cleanup materials, and neutralization residues. Waste needs its own lifecycle and lineage, not a final free-text note.

**Improvement:** Create waste-lot records with source batch or activity, waste code, hazard class, accumulation start date, storage area, transporter, treatment or disposal method, and final certificate linkage. Distinguish routine byproduct from investigational or incident-driven waste.

**Acceptance evidence:** Every waste disposition can be traced back to the originating batch or cleanup event, accumulation-time alerts surface before storage limits are breached, and final disposal evidence stays linked to the waste lot and original process record.

### 23. Regulatory submission dossier assembly

**Justification:** `regulatory_submission` should represent a structured dossier, not a loose attachment bucket. Formula changes, impurity findings, labeling updates, and stability evidence often have to be assembled into jurisdiction-specific submissions.

**Improvement:** Build dossier templates that pull approved source records for composition, impurity profile, SDS references, hazard classification, stability data, label text, and supporting approvals. Track submission status, authority responses, commitments, and required follow-up changes.

**Acceptance evidence:** Submission packets are generated from governed source data with lineage to recipe, QC, SDS, and approval records, and commitment obligations remain visible until their required post-submission actions are complete.

### 24. Jurisdiction-specific threshold and reporting engine

**Justification:** Reporting triggers differ by jurisdiction for concentration, annual volume, workplace inventory, precursor status, hazardous waste, and environmental release quantity. Chemical compliance needs those thresholds encoded explicitly.

**Improvement:** Add threshold libraries by jurisdiction, site, and material class so the system can determine when a batch, inventory change, or waste event creates a reporting obligation. Support both concentration-based and cumulative quantity-based rules with effective dates.

**Acceptance evidence:** Scenario tests show different outcomes for the same material under different jurisdictions, threshold calculations show the exact rule and effective date used, and reportable conditions open visible compliance tasks rather than relying on manual monitoring.

### 25. Restricted substance and impurity surveillance

**Justification:** Restricted substances and process-generated impurities can push an otherwise acceptable batch outside market or regulatory limits. Monitoring should cover both tested values and known risk of formation.

**Improvement:** Track restricted substance lists, impurity limits, precursor rules, and known process-impurity relationships at recipe and product level. Combine raw-material data, theoretical chemistry, and actual test results to decide when enhanced testing or automatic holds are required.

**Acceptance evidence:** Lots with known impurity risk surface enhanced testing requirements, near-limit trends are visible before a full failure occurs, and hold decisions explain whether they arose from measured results, theoretical risk, or both.

### 26. Incoming certificate-of-analysis verification and approved-source control

**Justification:** Incoming lot quality determines whether the finished batch ever had a compliant starting point. Supplier certificates must be checked against internal expectations, not accepted as unstructured attachments.

**Improvement:** Compare incoming CoA values, units, method references, and supplier identity against internal raw-material specs and approved-source lists. Route discrepancies into quarantine and require identity testing or supplier follow-up where risk justifies it.

**Acceptance evidence:** Incoming lots cannot be consumed until required CoA checks pass, supplier or site mismatches are visible in receiving review, and genealogy links each consumed raw lot to the exact CoA and approval outcome used.

### 27. Campaign planning and changeover contamination prevention

**Justification:** The sequence in which products run on shared equipment can create cross-contamination risk, cleaning burden, or permit load issues. Campaign planning is a real part of chemical compliance, not only production scheduling.

**Improvement:** Define campaign families, forbidden sequence pairs, required purge or flush steps, dedicated-equipment constraints, and heightened sampling after risky changeovers. Use prior product, potency, solubility, and hazard profile to determine required controls.

**Acceptance evidence:** Unsafe product sequences are blocked during planning, approved changeovers show the required cleaning or verification steps, and the next batch record inherits the correct post-changeover control plan automatically.

### 28. Cleaning validation and residue limit evidence

**Justification:** Residue carryover limits are critical for product quality and worker safety. Cleaning validation evidence needs to be tied to equipment release, residue limits, and actual verification samples.

**Improvement:** Store cleaning methods, residue or MACO limits, swab and rinse sample plans, recovery factors, acceptance criteria, and equipment-release authority. Differentiate validated routine cleaning from exceptional cleanup after spills, reactions, or contamination events.

**Acceptance evidence:** Equipment cannot be marked ready until required cleaning samples pass, residue-limit calculations remain linked to the product pair and method version used, and failed cleaning verification opens a visible contamination-control exception.

### 29. Instrument calibration and metrology status for critical controls

**Justification:** A pH value, weight, temperature, or chromatographic result is only defensible if the instrument used was qualified and in calibration. Chemical quality review should not have to infer instrument suitability from outside records.

**Improvement:** Tag balances, probes, sensors, and analytical instruments as critical resources for specific steps and tests, then enforce due-date, maintenance, and qualification-state checks before their results are accepted. Record instrument identity with each parameter reading or QC result.

**Acceptance evidence:** Overdue instruments automatically block critical use or force visible exception routing, batch and QC records show the exact instrument used, and review-by-exception highlights results generated near calibration expiry.

### 30. Review-by-exception for electronic batch records

**Justification:** Quality reviewers need to spend time on anomalies, not manually re-reading every clean step in a long batch record. A mature chemical system should collapse routine compliance and expand only the exceptions.

**Improvement:** Build review packets that surface parameter excursions, late or missing signatures, manual overrides, skipped checks, unusual hold times, abnormal yields, and unplanned recipe branching. Keep a drill-through path for full detail without forcing reviewers to start there.

**Acceptance evidence:** Review queues rank batches by exception burden, clean steps are summarized rather than repeated in full, and reviewers can approve straightforward records faster while still seeing all critical deviations and holds.

### 31. Quarantine, hold, release, and disposition controls

**Justification:** Raw materials, intermediates, finished product, rework pools, and waste all need explicit disposition states. Shipping, reuse, or destruction should depend on formal disposition, not implicit status assumptions.

**Improvement:** Add state models for quarantine, awaiting sample, under investigation, approved for use, released, rejected, rework-authorized, and destroyed. Assign clear role-based authority for state changes and link every transition to evidence or decision reason.

**Acceptance evidence:** Downstream consumption and shipment screens respect lot disposition, every disposition change is time-stamped and attributed, and release packets show which lots were cleared versus held at each stage of the process.

### 32. Shelf-life, retest-date, and expiry lockouts

**Justification:** Expired raw materials, intermediates, standards, and finished lots create direct compliance and safety exposure. The system should block use based on condition, not rely on memory or manual labels.

**Improvement:** Calculate shelf-life and retest logic from material class, storage condition, stability outcome, and jurisdictional rules. Support temporary extensions only through explicit review with justification and impact analysis.

**Acceptance evidence:** Expired or overdue lots cannot be selected for use without controlled override, finished goods show remaining shelf-life based on actual release date and storage context, and retest results update future eligibility visibly.

### 33. External laboratory result boundary and reconciliation

**Justification:** External labs often generate high-value results, but their data should enter through a governed boundary rather than overwriting internal records. Reconciliation is especially important when sample IDs, units, or method versions differ.

**Improvement:** Add explicit API or event intake for external results with sample matching, unit normalization, method-version comparison, signature verification, and exception routing for unresolved conflicts. Preserve the external source as source-of-origin without letting it bypass internal disposition logic.

**Acceptance evidence:** Unmatched or conflicting external results remain in a reconciliation queue, accepted results show source-lab lineage and normalized values, and release logic waits for resolved mapping rather than silently accepting imported numbers.

### 34. Event boundary model for material, batch, and release state changes

**Justification:** The manifest’s current emitted events are useful but too coarse for genealogy, review-by-exception, and release evidence. Chemical operations need domain event boundaries that reflect what actually happened on the floor and in quality review.

**Improvement:** Define domain events such as recipe revision released, batch started, phase completed, sample taken, result approved, deviation opened, hold released, permit threshold breached, and lot disposition changed while preserving compatibility with `ChemicalBatchComplianceCreated`, `ChemicalBatchComplianceUpdated`, `ChemicalBatchComplianceApproved`, and `ChemicalBatchComplianceExceptionOpened`. Clarify how consumed events such as `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` affect projections and controls inside the PBC.

**Acceptance evidence:** An event catalog documents each domain event, producer, payload, consumer, replay rule, and compatibility mapping, and replay tests prove that genealogy, release status, and review workbenches rebuild correctly from the event stream.

### 35. API boundary hardening for recipe, batch, SDS, and submission workflows

**Justification:** Chemical operations need a clear separation between command APIs, review actions, and read models. Public routes should express domain intent rather than mirroring internal table shape.

**Improvement:** Extend the current APIs with validation-only, approve, hold, release, sample-collect, result-ingest, dossier-preview, and simulation commands around `POST /chemical-formulas`, `POST /batch-records`, `POST /sds-documents`, `POST /hazardous-materials`, and `POST /regulatory-submissions`. Enforce idempotency keys, typed payloads, and explicit command semantics for high-risk actions.

**Acceptance evidence:** Contract tests cover duplicate submission handling, idempotent retries, invalid state transitions, and read-versus-write separation, and request payloads expose business meaning instead of raw internal column maps.

### 36. Master recipe authoring workbench

**Justification:** Recipe stewards need a dedicated interface for composition, revision comparison, approval, and impact review. A generic detail screen hides the critical context chemical teams need to evaluate recipe changes safely.

**Improvement:** Expand `ChemicalBatchComplianceWorkbench` and `ChemicalBatchComplianceDetail` with formula composition grids, revision diffs, impurity notes, allowed-equipment matrices, linked SDS obligations, and approval lanes for technical, quality, and EHS reviewers.

**Acceptance evidence:** A steward can author, compare, route, approve, and retire recipe revisions from the workbench, each role sees only its authorized actions, and linked hazards and regulatory obligations are visible during review rather than after approval.

### 37. Batch execution workbench

**Justification:** Operators and supervisors need one operational surface for active batches, open holds, parameter trends, and required signatures. Execution becomes error-prone when batch status is split across multiple disconnected views.

**Improvement:** Create a step timeline with current phase, pending actions, weigh-and-dispense panels, live parameter charts, open deviations, sample requirements, and disposition blockers. Show planned versus actual yield and the current risk picture while the batch is still in progress.

**Acceptance evidence:** Operators can progress, pause, investigate, and sign off a batch from one surface, supervisors can see which controls are still incomplete, and quality can review the same execution trail later without reconstructing it from scattered records.

### 38. QC and sample management workbench

**Justification:** Sample custody, testing, retesting, OOS review, and retain handling are specialized workflows that deserve their own operational model. Quality teams need context-rich queues, not only a list of result rows.

**Improvement:** Add dedicated QC queues for pending samples, in-test samples, awaiting-review results, OOS or OOT investigations, retains, and stability pulls. Surface method versions, instrument state, sample storage condition, and disposition-driving significance directly in the queue and detail views.

**Acceptance evidence:** Analysts can trace a sample from draw to final decision, review packets reveal why a result is or is not release-driving, and quality can manage retests and retains without losing custody or method context.

### 39. EHS and hazardous material workbench

**Justification:** Environmental, health, and safety users need visibility into hazardous inventory, incompatible storage, open permits, spill or waste issues, and SDS changes. Those tasks are too specific to fit inside a generic manufacturing detail page.

**Improvement:** Build dashboards for SDS revision impact, storage compatibility violations, permit utilization, exposure-control prerequisites, waste accumulation timers, and hazardous-material inventory by location. Highlight emerging hotspots such as repeated incompatible storage attempts or near-limit permit utilization.

**Acceptance evidence:** EHS users can identify expiring permits, incompatible locations, and reportable waste or emission conditions from one surface, and the workbench links each alert to the underlying materials, batches, and documents involved.

### 40. Compliance release and audit workbench

**Justification:** Final release requires assembled evidence across recipe, batch record, QC, deviations, permits, SDS, and regulatory thresholds. Releasing from scattered tabs invites missed conditions and weak audit defense.

**Improvement:** Create a release cockpit that aggregates genealogy completeness, sample disposition, deviation status, permit compliance, SDS revision status, threshold calculations, and submission obligations before a lot is approved or rejected. Include review-by-exception summaries and drill-through to source evidence.

**Acceptance evidence:** Every release decision shows a structured pass or fail view of required criteria, unresolved blockers are obvious before approval, and audit reviewers can reopen the exact release packet later without reassembling evidence manually.

### 41. Agent skill for SDS and permit interpretation

**Justification:** Document-heavy chemical work benefits from automation only if the assistant can extract obligations accurately and cite the source. Without source-aware interpretation, assistant output is not trustworthy enough for regulated use.

**Improvement:** Extend `ChemicalBatchComplianceAssistantPanel` with an agent skill that reads SDS and permit documents, proposes structured hazard, storage, PPE, emission, and disposal obligations, and maps those findings to the relevant hazardous material, recipe, or batch context. Require citation to page, section, or paragraph for every proposed controlled field.

**Acceptance evidence:** Assistant suggestions include source citations and confidence markers, users can accept or reject each proposed obligation before it changes any controlled record, and accepted suggestions remain linked to the originating document version.

### 42. Agent skill for deviation triage and evidence assembly

**Justification:** Deviation investigators spend substantial time gathering context from parameter traces, batch steps, sample results, and prior incidents before they can reason about root cause. An assistant can help only if it assembles evidence instead of issuing unsupported conclusions.

**Improvement:** Add an agent skill that compiles excursion timeline, implicated material lots, related samples, prior similar deviations, open CAPAs, and likely impact scope into an investigator-ready packet. Keep recommendations explicit about uncertainty and separate from the underlying evidence bundle.

**Acceptance evidence:** Investigators can open a generated packet that links back to every cited batch step, result, and event, assistant reasoning can be corrected without losing the original source bundle, and accepted packets reduce manual evidence gathering time without weakening traceability.

### 43. Guardrails for governed agent actions in `chemical_batch_compliance`

**Justification:** Agent skills should accelerate review and preparation, but high-risk chemical actions still need controlled authority. Releasing a lot, overriding a permit, or activating a recipe revision cannot become a silent assistant side effect.

**Improvement:** Enforce dry-run diffs, policy checks, role checks, and explicit human approval for agent-initiated changes to release state, OOS disposition, permit override, hazardous-material classification, or recipe activation. Limit lower-risk autonomous actions to drafting, classification suggestions, and evidence assembly.

**Acceptance evidence:** Blocked actions show why they were denied, approved actions capture both requester and approver identity, and assistant activity logs prove that no governed mutation bypasses the command, policy, or audit boundary.

### 44. Counterfactual simulation for parameter excursions and holds

**Justification:** Supervisors often need to know whether an alternate setpoint, extended hold, extra sample, or rework route would save a batch before they take action. Chemical decision-making improves when the system can model likely downstream impact safely.

**Improvement:** Add non-mutating simulations for process-parameter excursions, extended dwell times, extra purification steps, rework options, additional sampling, and alternate release decisions. Use recipe rules, spec limits, permit thresholds, and genealogy context as the simulation boundary.

**Acceptance evidence:** Simulation results show predicted impact on quality, waste, permit headroom, and release readiness, the user can compare multiple corrective paths side by side, and no live batch state changes while a scenario is being evaluated.

### 45. Predictive anomaly detection for process drift and compliance risk

**Justification:** Drift usually appears as subtle movement in yields, impurity levels, cycle times, energy use, or recurring near-miss deviations before it becomes a clear failure. A mature PBC should surface these leading indicators early.

**Improvement:** Detect anomalies in parameter traces, sample results, supplier CoA values, batch duration, yield, waste generation, and repeated holds. Prioritize alerts by likely impact to quality, EHS, release timing, and regulatory exposure.

**Acceptance evidence:** Risk cards show the batches or materials driving the alert, the specific variables that drifted, and reviewer outcomes such as accepted concern, dismissed alert, or monitored trend, enabling later calibration of alert quality.

### 46. Continuous control testing for segregation, approval, and release readiness

**Justification:** Chemical compliance should be demonstrated continuously, not only during annual audits or release crunch time. Core controls such as dual review, calibration, SDS linkage, genealogy completeness, and permit limits are testable conditions.

**Improvement:** Add scheduled control assertions for overdue calibrations, expired materials, missing SDS links, open major deviations, incomplete genealogy, absent dual signatures, and environmental limit overruns. Route failing controls into visible exceptions with ownership and closure evidence.

**Acceptance evidence:** Control dashboards show current pass or fail state by control family, failures remain linked to remediation records after closure, and release workbenches consume the same control state instead of rechecking through manual lists.

### 47. Release evidence vault and sealed audit packs

**Justification:** Release evidence should survive inspection, complaint, recall, and legal review without spreadsheet rebuilding. A chemical batch system needs immutable evidence bundles for what was known and approved at release time.

**Improvement:** Assemble sealed release packs containing the effective recipe revision, full batch record, parameter trends, sample and QC results, deviations, permit checks, SDS snapshot, threshold calculations, and approval signatures. Link those packs to the release documents named in `RELEASE_EVIDENCE.md`.

**Acceptance evidence:** Released lots have retrievable audit packs with lineage to source records, verification checks can confirm the pack was not altered after sealing, and inspectors can review the exact evidence bundle used for release without regenerating it from live data.

### 48. Multi-tenant policy isolation by plant, business unit, and jurisdiction

**Justification:** Different plants or business units may produce different chemistries under different limits, permits, and approval chains while still sharing one PBC. Isolation has to cover policy, execution, and evidence, not only simple row scoping.

**Improvement:** Separate recipe policies, hazardous-material rules, sampling plans, permit logic, release criteria, and agent permissions by tenant, plant, and jurisdiction. Allow shared reference content only where explicitly governed and auditable.

**Acceptance evidence:** Cross-tenant and cross-site access checks fail closed, one plant’s permit thresholds never affect another plant’s batch release decisions, and the workbench renders site-specific obligations correctly for the same product family when rules differ.

### 49. Recall readiness and trace-back or trace-forward drills

**Justification:** Genealogy value is proven during complaint, incident, or recall drills, not in abstract architecture diagrams. The system should answer “what else is affected?” in minutes, not after spreadsheet reconciliation.

**Improvement:** Add recall drill mode that starts from a complaint lot, raw-material lot, impurity signal, or safety incident and traces all connected batches, intermediates, retained samples, shipments, waste dispositions, and open investigations. Include the ability to save drill outputs as investigation evidence.

**Acceptance evidence:** Drill reports list impacted lots and the reasoning path used to identify them, completion time is measurable and repeatable, and no manual spreadsheet stitching is needed to produce a defensible trace-back or trace-forward view.

### 50. Domain-complete release gate for `chemical_batch_compliance`

**Justification:** The PBC should not claim maturity until its chemical controls, domain boundaries, workbenches, and agent skills are proven together. Release readiness must reflect real chemical batch compliance scenarios rather than generic feature presence.

**Improvement:** Make release gating depend on executable evidence for master recipe control, batch execution, process parameters, hazardous-material management, SDS handling, sampling, QC, deviations, permits, lot genealogy, regulatory thresholds, event boundaries, API boundaries, UI workbenches, and governed agent skills.

**Acceptance evidence:** A release checklist maps the manifest surfaces, seeded domain scenarios, and this backlog to passing tests, scenario walkthroughs, and auditable proof before a new version is considered complete.
