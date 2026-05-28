# Environment Health and Safety Improvement Backlog

## Current Domain Evidence Used

- `pbc`: `environment_health_safety`
- `label`: `Environment Health and Safety`
- `description`: `EHS incidents, inspections, permits, hazards, corrective actions, training, audits, and compliance evidence`
- `tables`: `ehs_incident`, `hazard`, `inspection`, `permit`, `corrective_action`, `safety_training`, `audit_finding`, `environment_health_safety_policy_rule`, `environment_health_safety_runtime_parameter`, `environment_health_safety_schema_extension`, `environment_health_safety_control_assertion`, `environment_health_safety_governed_model`
- `apis`: `POST /ehs-incidents`, `POST /hazards`, `POST /inspections`, `POST /permits`, `POST /corrective-actions`, `GET /environment-health-safety-workbench`
- `workflows`: `environment_health_safety_create_ehs_incident_workflow`, `environment_health_safety_record_hazard_workflow`
- `ui_fragments`: `EnvironmentHealthSafetyWorkbench`, `EnvironmentHealthSafetyDetail`, `EnvironmentHealthSafetyAssistantPanel`
- `analytics`: `environment_health_safety_risk_score`, `environment_health_safety_workbench_metric`
- `emits`: `EnvironmentHealthSafetyCreated`, `EnvironmentHealthSafetyUpdated`, `EnvironmentHealthSafetyApproved`, `EnvironmentHealthSafetyExceptionOpened`
- `consumes`: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- `advanced_capabilities`: `environment_health_safety_event_sourced_operational_history`, `environment_health_safety_multi_tenant_policy_isolation`, `environment_health_safety_schema_evolution_resilience`, `environment_health_safety_autonomous_anomaly_detection`, `environment_health_safety_semantic_document_instruction_understanding`, `environment_health_safety_predictive_risk_scoring`, `environment_health_safety_counterfactual_scenario_simulation`, `environment_health_safety_cryptographic_audit_proofs`, `environment_health_safety_continuous_control_testing`, `environment_health_safety_carbon_and_sustainability_awareness`, `environment_health_safety_cross_pbc_event_federation`, `environment_health_safety_governed_ai_agent_execution`
- `docs`: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`
- `configuration`: `ENVIRONMENT_HEALTH_SAFETY_DATABASE_URL`, `ENVIRONMENT_HEALTH_SAFETY_EVENT_TOPIC`, `ENVIRONMENT_HEALTH_SAFETY_RETRY_LIMIT`, `ENVIRONMENT_HEALTH_SAFETY_DEFAULT_POLICY`

### 1. Recordable incident lifecycle and severity gates
**Exact key:** `ehs_incident`
**Justification:** First aid, medical treatment, lost time, restricted work, fatality, environmental release, and near miss need different handling, escalation, and closure rules.
**Improvement:** Add an incident lifecycle that separates draft, triaged, recordability-review, regulator-notified, investigation-open, corrective-action-open, closed, and reopened states, with explicit severity and recordability codes.
**Acceptance evidence:** Transition tests block invalid closures, and `EnvironmentHealthSafetyWorkbench` shows severity, recordability, and notification status on one incident queue card.

### 2. Serious-incident notification clocks and escalation paths
**Exact key:** `ehs_incident`
**Justification:** Fatalities, hospitalizations, major releases, and fire events carry clock-based reporting duties that cannot depend on manual reminders.
**Improvement:** Add jurisdiction-aware timers, escalation rules, regulator contact packs, and acknowledgement evidence for serious-incident notifications.
**Acceptance evidence:** Seeded incidents show countdown timers, overdue notifications open exceptions automatically, and approval history captures who sent each notice and when.

### 3. Investigation dossier with barrier and cause analysis
**Exact key:** `ehs_incident`
**Justification:** Investigations need more than a narrative; they need failed barriers, contributing conditions, and a defensible causal chain.
**Improvement:** Build an investigation dossier with chronology, witness statements, equipment state, immediate cause, basic cause, root cause, and failed-control mapping.
**Acceptance evidence:** `EnvironmentHealthSafetyDetail` renders a causal chain for seeded incidents, and closure is blocked until mandatory investigation fields and evidence links are complete.

### 4. Near-miss to hazard promotion rules
**Exact key:** `hazard`
**Justification:** Repeated near misses should strengthen prevention before harm occurs, not disappear into closed incident logs.
**Improvement:** Add promotion rules that open or update `hazard` records when incident patterns show repeated unsafe conditions, similar tasks, or repeated control failures.
**Acceptance evidence:** Policy simulations show why a near-miss cluster becomes a hazard entry, and duplicate-hazard handling keeps lineage back to the triggering incidents.

### 5. Corrective action effectiveness verification
**Exact key:** `corrective_action`
**Justification:** Closing a CAPA on date alone does not prove the risk was reduced or the failed control was replaced with something stronger.
**Improvement:** Require owner, due date, hierarchy-of-controls classification, verification step, effectiveness review window, and re-open logic when a corrective action fails to hold.
**Acceptance evidence:** Actions cannot close without verifier evidence, failed effectiveness reviews reopen the action, and linked incidents reflect the reopened control gap.

### 6. Hazard register by site, area, task, and energy source
**Exact key:** `hazard`
**Justification:** Operators need to see chemical, physical, biological, ergonomic, and stored-energy hazards in the context where work actually happens.
**Improvement:** Build a hierarchical hazard register keyed by site, area, process, task step, exposed population, energy source, existing controls, and residual risk.
**Acceptance evidence:** Workbench filters return hazards by site, area, or task, and seeded data shows duplicate detection across overlapping hazard descriptions.

### 7. Dynamic risk assessment before non-routine work
**Exact key:** `hazard`
**Justification:** Static hazards do not account for weather, occupancy, temporary bypasses, shutdown conditions, or concurrent work.
**Improvement:** Add pre-job dynamic risk assessments that pull active hazards, temporary controls, permit conditions, isolation state, and site alerts into one risk decision.
**Acceptance evidence:** High-risk work cannot proceed without a signed dynamic assessment, and the detail view shows which live conditions changed the residual risk.

### 8. Inspection program by asset, area, theme, and frequency
**Exact key:** `inspection`
**Justification:** Housekeeping rounds, confined-space inspections, environmental rounds, and behavior observations need different cadence and scope.
**Improvement:** Define inspection templates with recurrence rules, mandatory evidence, route or area scope, finding severity, and overdue escalation behavior.
**Acceptance evidence:** Scheduled inspections appear in due queues automatically, skipped inspections require reason codes, and overdue inspections escalate according to policy.

### 9. Offline and mobile inspection capture with governed sync
**Exact key:** `inspection`
**Justification:** Many inspections happen in plants, yards, and remote locations where connectivity is intermittent.
**Improvement:** Support offline answers, photos, measurements, signatures, and later sync through idempotent handlers with stale-form warnings and conflict resolution.
**Acceptance evidence:** Sync tests show no duplicate findings on reconnect, and replayed submissions preserve original capture time and inspector identity.

### 10. Permit-to-work conflict matrix
**Exact key:** `permit`
**Justification:** Hot work, line break, excavation, confined space, and energized work can invalidate each other when they overlap in time or location.
**Improvement:** Enforce permit conflict rules by area, time window, energy source, gas test status, rescue readiness, simultaneous operations, and linked isolation boundaries.
**Acceptance evidence:** Conflicting permit issuance is blocked with a named rule, and the workbench shows the dependency chain that caused the block.

### 11. Permit suspension, extension, and handback control
**Exact key:** `permit`
**Justification:** Permits often drift across shift changes, weather delays, and maintenance interruptions unless suspension and return-to-service are explicit.
**Improvement:** Add suspended, extended, handed-back, cancelled, and expired states with required revalidation, supervisor acknowledgement, and return-to-service evidence.
**Acceptance evidence:** Expired permits disappear from active boards, and handback requires completed isolation removal evidence plus area acceptance before closure.

### 12. High-risk permit prerequisites and competency gates
**Exact key:** `permit`
**Justification:** Confined-space and energized-work permits should prove testing, rescue readiness, and qualified personnel before issue, not after an incident.
**Improvement:** Bind permit validation to gas-test windows, lockout verification, role coverage, equipment readiness, and linked training validity for the assigned crew.
**Acceptance evidence:** Validation-only permit requests list missing prerequisites before issue, and permit cards show which specific preconditions are still unmet.

### 13. Training matrix linked to hazards, roles, and permits
**Exact key:** `safety_training`
**Justification:** Training records only matter if they map to the hazards people face and the permits they are allowed to work under.
**Improvement:** Map each training or competency record to hazard families, permit types, emergency roles, contractor categories, and refresher intervals.
**Acceptance evidence:** The detail view explains why a worker is or is not qualified for a task, and permit issue checks the linked training matrix automatically.

### 14. Expiry, retraining, and grace-period governance
**Exact key:** `safety_training`
**Justification:** Lapsed qualifications are a leading risk indicator and should not remain buried in a separate export or spreadsheet.
**Improvement:** Add expiry logic, grace windows, restricted-duty flags, and site or jurisdiction overrides for mandatory retraining and reassessment.
**Acceptance evidence:** Expired training opens exceptions, and active permits can be auto-flagged when a required qualification lapses mid-job.

### 15. Exposure monitoring for chemical, noise, dust, and ergonomic load
**Exact key:** `environment_health_safety_schema_extension`
**Justification:** EHS needs owned exposure facts even though the current manifest has no dedicated exposure table.
**Improvement:** Extend the schema with exposure samples, similar exposure groups, dose calculations, task duration, control type, and action thresholds while keeping the boundary operational rather than clinical.
**Acceptance evidence:** Migrations and projections show sample histories and exceedances, and the workbench can filter open exposure issues by agent, area, and hazard family.

### 16. Medical-surveillance trigger boundary inside EHS
**Exact key:** `environment_health_safety_policy_rule`
**Justification:** EHS must know when surveillance is required without becoming the system of record for diagnosis or treatment.
**Improvement:** Express policy rules that open surveillance-required tasks from exposure thresholds, respirator enrollment, and hazardous-substance categories while storing only bounded operational status.
**Acceptance evidence:** Tests prove only trigger status and completion evidence are retained, and assistant output never exposes sensitive health details beyond that boundary.

### 17. Spill, waste, and emissions boundary accounting
**Exact key:** `environment_health_safety_carbon_and_sustainability_awareness`
**Justification:** Releases, waste streams, and fugitive emissions often begin as EHS events and later feed environmental reporting, so the handoff boundary must be explicit.
**Improvement:** Capture release type, quantity estimate, containment status, reportability, waste classification, and downstream environmental-report handoff status on incidents and permits.
**Acceptance evidence:** Seeded spill cases show EHS containment evidence, regulator notification status, and a federated handoff record without duplicate manual entry.

### 18. Permit and incident linkage for release and spill events
**Exact key:** `ehs_incident`
**Justification:** A release during maintenance or line breaking should trace back to the authorizing permit and the controls that failed.
**Improvement:** Require incidents involving fires, spills, or loss of containment to link the active permit, isolation step, task owner, and area conditions at the time of the event.
**Acceptance evidence:** Investigation pages can navigate from incident to permit and back, and incident closure is blocked if the initiating permit context is missing.

### 19. Compliance obligation register with due dates and evidence owners
**Exact key:** `environment_health_safety_policy_rule`
**Justification:** Compliance work fails when obligations live outside the package that already owns inspections, permits, incidents, and audits.
**Improvement:** Create obligation records for inspections, reports, monitoring, training, permit renewals, and notices with jurisdiction, recurrence, owner, due date, and evidence expectation.
**Acceptance evidence:** The workbench shows upcoming and overdue obligations by site, and each obligation record links to its submitted evidence or open exception.

### 20. Jurisdiction-aware policy packs
**Exact key:** `environment_health_safety_policy_rule`
**Justification:** One organization can operate under different rules for recordability, waste handling, inspection cadence, and permit conditions across sites.
**Improvement:** Version policy packs by jurisdiction, site class, contractor presence, and hazard profile, with effective dates and comparison views before approval.
**Acceptance evidence:** Policy simulations show exactly which incidents, permits, and training requirements change under a proposed policy pack revision.

### 21. Runtime parameters for risk thresholds and escalation timing
**Exact key:** `environment_health_safety_runtime_parameter`
**Justification:** Field operations need bounded tuning for risk bands, gas-test windows, overdue tolerances, and escalation timing without code edits.
**Improvement:** Expose approved parameters for risk-score bands, notification countdowns, inspection grace periods, permit extension limits, and CAPA aging.
**Acceptance evidence:** Parameter history shows who changed what, unsafe ranges are rejected, and affected queues re-score immediately after approval.

### 22. Role-based workbench lanes for EHS operations
**Exact key:** `EnvironmentHealthSafetyWorkbench`
**Justification:** Permit issuers, investigators, supervisors, and compliance leads do not all need the same operational view.
**Improvement:** Provide separate lanes for active incidents, open permits, overdue inspections, at-risk corrective actions, training expiries, exposure exceedances, and regulator obligations.
**Acceptance evidence:** Persona tests show the right lane mix per role, and every card drills directly into the required next action.

### 23. Evidence-first detail view for incidents, permits, and audits
**Exact key:** `EnvironmentHealthSafetyDetail`
**Justification:** Detail pages should explain what happened, which control failed, and what evidence exists instead of pushing users to raw tables.
**Improvement:** Redesign detail views around chronology, linked hazards, linked permits, corrective actions, attachments, approvals, and event provenance.
**Acceptance evidence:** Traceability checks prove each badge or metric links to a source record or emitted event, and seeded screenshots can be reproduced from package data.

### 24. Assistant skill for shift-ready incident summaries
**Exact key:** `EnvironmentHealthSafetyAssistantPanel`
**Justification:** Supervisors need fast, grounded handover summaries for open incidents and active controls.
**Improvement:** Add a summarization skill that drafts incident status, open actions, affected area, controls in place, and unanswered questions with citations to incident, permit, and inspection records.
**Acceptance evidence:** Regression tests show every assistant paragraph cites source records, and unsupported claims are refused rather than invented.

### 25. Assistant skill for permit review and field coaching
**Exact key:** `ai_agent_task_assistance`
**Justification:** Permit issuers need guided review for complex work involving testing, isolation, rescue, and contractor competence.
**Improvement:** Add a bounded assistant skill that reviews draft permit packages, highlights missing prerequisites, and proposes pre-start briefing points without auto-issuing the permit.
**Acceptance evidence:** Preview and confirm flows prove no record mutation happens before human approval, and the review output lists the exact missing evidence.

### 26. Document intake for SDS, procedures, and permit attachments
**Exact key:** `agentic_document_instruction_intake`
**Justification:** EHS instructions arrive in safety data sheets, method statements, work packs, and regulator letters, not only in typed forms.
**Improvement:** Parse attached documents into structured hazard controls, PPE requirements, inspection criteria, and permit prerequisites while preserving source excerpts and confidence.
**Acceptance evidence:** Golden document fixtures show extracted controls in review state first, and accepted extracts retain links back to the original source passages.

### 27. Assistant skill for investigation evidence gaps
**Exact key:** `ai_agent_task_assistance`
**Justification:** Investigations often miss witness statements, photos, barrier checks, or training links that later matter in audits and litigation.
**Improvement:** Add a skill that inspects an open investigation dossier and flags missing evidence, contradictory timestamps, and likely next interviews or documents.
**Acceptance evidence:** Seeded investigation cases show the assistant identifying true gaps with citations, and no direct mutation of the incident record is allowed.

### 28. API expansion for search, dry-run, bulk close, and evidence export
**Exact key:** `POST /ehs-incidents`
**Justification:** Create-only endpoints do not cover operational search, regulator-ready exports, or safe validation of complex incident and permit payloads.
**Improvement:** Extend the API surface with search and read models, validation-only commands for incidents and permits, bulk governed close or reopen paths, and evidence export routes.
**Acceptance evidence:** API fixtures show dry-run responses with rule failures, idempotency tests cover retries, and exported evidence matches the detail view for the same record set.

### 29. Bulk intake for hazards, inspections, and training completions
**Exact key:** `POST /hazards`
**Justification:** Mobilizations and contractor onboarding often require large-volume loading of hazards, inspection findings, and course completions.
**Improvement:** Support batch ingest with row-level validation, row-level idempotency, resumable failures, and governed correction workflows.
**Acceptance evidence:** Batch tests preserve accepted rows while isolating rejected rows with clear error explanations and retry eligibility.

### 30. Typed emitted events for real EHS facts
**Exact key:** `emits`
**Justification:** Generic created and updated events are too coarse for downstream safety reporting and operational automation.
**Improvement:** Emit typed facts for incident severity changed, permit issued, permit suspended, inspection failed, corrective action overdue, exposure exceeded, training lapsed, and audit finding reopened.
**Acceptance evidence:** Event-schema tests and example payloads show consumers can act without reading internal tables or ambiguous free text.

### 31. Policy-change consumption with targeted re-evaluation
**Exact key:** `PolicyChanged`
**Justification:** When a policy pack changes, open permits, incidents, training obligations, and inspection schedules need re-evaluation rather than a blind configuration swap.
**Improvement:** Implement an idempotent `PolicyChanged` handler that recomputes affected records, opens exceptions where new rules are violated, and preserves the prior policy version used at the original decision point.
**Acceptance evidence:** Duplicate-event tests show safe replay, and changed records display both the old and new policy versions that influenced their state.

### 32. Audit-seal consumption for locked evidence bundles
**Exact key:** `AuditEventSealed`
**Justification:** Once an investigation or audit package is sealed, edits should be constrained and visible.
**Improvement:** Consume `AuditEventSealed` to mark evidence bundles, audit findings, and release packs as sealed, read-only, or amendment-required based on their lifecycle state.
**Acceptance evidence:** Handler tests prove sealed evidence cannot be silently edited, and amendment flows retain the original sealed bundle alongside the new revision.

### 33. KPI feedback loops into risk prioritization
**Exact key:** `OperationalKpiChanged`
**Justification:** Rising minor injuries, inspection drift, or repeated permit suspensions should alter queue priority before a severe event happens.
**Improvement:** Handle `OperationalKpiChanged` by recalculating risk scores, anomaly baselines, and escalation priority for affected sites, tasks, and hazard clusters.
**Acceptance evidence:** Before-and-after fixtures show queue reprioritization with lineage back to the incoming KPI event.

### 34. Dead-letter, retry, and replay operations for EHS eventing
**Exact key:** `retry_dead_letter_evidence`
**Justification:** Failed event handling can leave stale permit views, missing CAPA escalations, or out-of-date incident queues.
**Improvement:** Create an operator queue for failed EHS messages with reason, last attempt, replay safety, domain impact, and required remediation notes.
**Acceptance evidence:** Replay tests show idempotent recovery, poison messages stay quarantined, and every operator retry decision is logged in the workbench.

### 35. Event-sourced operating timeline for investigations and audits
**Exact key:** `environment_health_safety_event_sourced_operational_history`
**Justification:** Investigators and auditors need to reconstruct what changed, in what order, and under which policy version.
**Improvement:** Build a time-travel timeline across incidents, hazards, inspections, permits, actions, and audit findings with actor, command, event, and projection checkpoints.
**Acceptance evidence:** Replay tests rebuild seeded scenarios exactly, and the detail view can step through the sequence that led to closure or escalation.

### 36. Predictive risk scoring from leading indicators
**Exact key:** `environment_health_safety_risk_score`
**Justification:** Severe events are often preceded by inspection drift, repeated near misses, overdue corrective actions, training gaps, and permit churn.
**Improvement:** Score sites, tasks, and hazard clusters using those leading indicators and expose interpretable drivers rather than opaque weights.
**Acceptance evidence:** Model-evaluation fixtures show the top drivers for each score, and supervisors can drill from a score to the records that created it.

### 37. Autonomous anomaly detection for exposure, waste, and permit behavior
**Exact key:** `environment_health_safety_autonomous_anomaly_detection`
**Justification:** Sudden noise spikes, unusual spill quantities, repeated permit extensions, or inspection finding surges should surface automatically.
**Improvement:** Detect anomalies across exposure readings, release quantities, permit duration patterns, CAPA aging, and inspection failure rates using site-specific baselines.
**Acceptance evidence:** Seeded outlier scenarios open explainable alerts that cite the baseline window, observed deviation, and affected record set.

### 38. Counterfactual simulation for control selection
**Exact key:** `environment_health_safety_counterfactual_scenario_simulation`
**Justification:** EHS teams need to compare ventilation, guarding, scheduling, and training interventions before committing capital or shutting down work.
**Improvement:** Simulate alternative controls against expected incident likelihood, permit restrictions, exposure reduction, and operational disruption for a defined hazard cluster.
**Acceptance evidence:** Simulation views compare options side by side and clearly mark modeled outcomes as non-authoritative until a change is approved.

### 39. Continuous control tests for stale risk and overdue obligations
**Exact key:** `environment_health_safety_continuous_control_testing`
**Justification:** A package that waits for manual audit has already missed the point of operational safety control.
**Improvement:** Run continuous assertions for overdue serious-incident notification, expired permits, overdue corrective actions, lapsed training on active high-risk work, and unresolved exposure exceedances.
**Acceptance evidence:** Failing assertions open `EnvironmentHealthSafetyExceptionOpened` records with the exact breached control and affected record identifiers.

### 40. Cryptographic proof bundles for investigations and submissions
**Exact key:** `environment_health_safety_cryptographic_audit_proofs`
**Justification:** Regulator submissions and serious-incident investigations need integrity proof beyond mutable attachments.
**Improvement:** Hash-chain evidence packages, approvals, event payloads, and release bundles so tampering is detectable without exposing restricted content.
**Acceptance evidence:** Verification commands succeed on seeded bundles, and redacted exports still validate against the stored proof chain.

### 41. Tenant, site, and jurisdiction isolation
**Exact key:** `environment_health_safety_multi_tenant_policy_isolation`
**Justification:** Contractors, business units, and regulated sites may share infrastructure but cannot share rules, evidence, or queue visibility by accident.
**Improvement:** Isolate policy packs, runtime parameters, workbench filters, assistant context, and evidence storage by tenant and site or jurisdiction scope.
**Acceptance evidence:** Negative tests prove one scope cannot read or apply another scope's incidents, permits, or policy overrides.

### 42. Controlled schema evolution for site-specific forms
**Exact key:** `environment_health_safety_schema_evolution_resilience`
**Justification:** Sites will request local fields on permits and inspections, but ad hoc columns break APIs, analytics, and release evidence.
**Improvement:** Add a schema-extension registry for approved local fields, validation rules, migration previews, projection impact checks, and rollback metadata.
**Acceptance evidence:** Dry-run migrations show downstream effects before approval, and backfill evidence proves old records remain readable after an extension rollout.

### 43. Guardrails for governed AI models and autonomous actions
**Exact key:** `environment_health_safety_governed_ai_agent_execution`
**Justification:** AI can help draft and triage, but it should never issue permits, downgrade severity, or close incidents without human approval.
**Improvement:** Define approved agent skills, blocked decisions, required human checkpoints, prompt provenance, and model-version capture for every AI-assisted action.
**Acceptance evidence:** Policy tests show the agent can draft and recommend but cannot issue permits, close incidents, or suppress exceptions autonomously.

### 44. Audit program planning and repeat-finding memory
**Exact key:** `audit_finding`
**Justification:** Audits matter when they show recurrence, aging, and control weakness across sites and time periods.
**Improvement:** Model audit plans, finding taxonomy, recurrence clustering, owner escalation, and linkage from audit findings to incidents, hazards, and corrective actions.
**Acceptance evidence:** The workbench shows repeat findings by site and control family, and closure requires evidence that the underlying condition changed rather than only the wording.

### 45. Compliance calendar and regulator submission evidence
**Exact key:** `environment_health_safety_policy_rule`
**Justification:** Recurring reports, notice postings, and permit renewals need the same rigor as incident response and CAPA management.
**Improvement:** Add a compliance calendar that tracks submission due dates, draft status, approver, submitted artifact, regulator acknowledgement, and late-filing justification.
**Acceptance evidence:** Overdue submissions raise exceptions, and each reporting cycle links directly to the filed artifact and acknowledgement evidence.

### 46. Cross-PBC event federation at EHS boundaries
**Exact key:** `environment_health_safety_cross_pbc_event_federation`
**Justification:** EHS decisions often depend on maintenance, workforce, or environmental signals, but the package must integrate through events rather than shared tables.
**Improvement:** Formalize federation contracts for incoming operational signals and outgoing spill, waste, emissions, and exposure events with freshness and ownership rules.
**Acceptance evidence:** Contract tests show no foreign-table references, and federated event lineage is visible from the originating EHS record.

### 47. Release evidence packs for incidents, permits, audits, and controls
**Exact key:** `RELEASE_EVIDENCE.md`
**Justification:** Package release should prove that serious workflows and evidence bundles work, not merely that the file exists.
**Improvement:** Generate release packs that include an incident investigation, a permit issue-suspend-handback cycle, an overdue-training block, an inspection failure, an audit finding, and the resulting emitted events.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` contains reproducible artifacts, route traces, and verifier notes tied to the package version.

### 48. Specification-backed contract checks for declared surfaces
**Exact key:** `SPECIFICATION.md`
**Justification:** Manifest-declared tables, APIs, workflows, UI fragments, analytics, docs, and tests should not drift from implementation silently.
**Improvement:** Add contract checks that compare `SPECIFICATION.md`, manifest surfaces, route registration, event schemas, and UI workbench routes.
**Acceptance evidence:** Intentionally broken declarations fail validation, and normal runs produce a pass/fail matrix across declared surfaces.

### 49. End-to-end release assurance scenario
**Exact key:** `continuous_release_assurance`
**Justification:** Incidents, hazards, inspections, permits, corrective actions, training, and audits should be proven together in one package-local story.
**Improvement:** Build an end-to-end scenario that records a hazard, issues a permit, fails an inspection, opens an incident, assigns a corrective action, blocks a worker with lapsed training, and closes with sealed evidence.
**Acceptance evidence:** One release gate exercises the full path with deterministic outputs and fails if any declared workflow, event, or UI projection breaks.

### 50. Workbench metrics for operational safety and compliance
**Exact key:** `environment_health_safety_workbench_metric`
**Justification:** EHS leaders need metrics that show exposure and control health, not just record counts.
**Improvement:** Define workbench metrics for high-risk permits active, inspection overdue rate, serious-incident notification timeliness, corrective-action aging, training expiry exposure, exposure exceedance count, repeat audit findings, and open compliance obligations.
**Acceptance evidence:** Metric definitions are traceable to source records, dashboard values match fixture calculations, and supervisors can drill from each metric to the queue that produced it.
