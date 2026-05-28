# Cybersecurity Operations Center Improvement Backlog

## Current Domain Evidence Used

- Stable PBC key: `cybersecurity_operations_center`.
- Exact key: `'description': 'Security alerts, incidents, assets, threat intelligence, playbooks, containment, and response evidence'`.
- Exact key: `'apis': ('POST /security-alerts', 'POST /security-incidents', 'POST /asset-exposures', 'POST /threat-intels', 'POST /playbook-runs', 'GET /cybersecurity-operations-center-workbench')`.
- Exact key: `'tables': ('security_alert', 'security_incident', 'asset_exposure', 'threat_intel', 'playbook_run', 'containment_action', 'response_evidence', 'cybersecurity_operations_center_policy_rule', 'cybersecurity_operations_center_runtime_parameter', 'cybersecurity_operations_center_schema_extension', 'cybersecurity_operations_center_control_assertion', 'cybersecurity_operations_center_governed_model')`.
- Exact key: `'workflows': ('cybersecurity_operations_center_create_security_alert_workflow', 'cybersecurity_operations_center_record_security_incident_workflow')`.
- Exact key: `'ui_fragments': ('CybersecurityOperationsCenterWorkbench', 'CybersecurityOperationsCenterDetail', 'CybersecurityOperationsCenterAssistantPanel')`.
- Exact key: `'analytics': ('cybersecurity_operations_center_risk_score', 'cybersecurity_operations_center_workbench_metric')`.
- Exact key: `'emits': ('CybersecurityOperationsCenterCreated', 'CybersecurityOperationsCenterUpdated', 'CybersecurityOperationsCenterApproved', 'CybersecurityOperationsCenterExceptionOpened')`.
- Exact key: `'consumes': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')`.
- Exact key: `'advanced_capabilities': ('cybersecurity_operations_center_event_sourced_operational_history', 'cybersecurity_operations_center_multi_tenant_policy_isolation', 'cybersecurity_operations_center_schema_evolution_resilience', 'cybersecurity_operations_center_autonomous_anomaly_detection', 'cybersecurity_operations_center_semantic_document_instruction_understanding', 'cybersecurity_operations_center_predictive_risk_scoring', 'cybersecurity_operations_center_counterfactual_scenario_simulation', 'cybersecurity_operations_center_cryptographic_audit_proofs', 'cybersecurity_operations_center_continuous_control_testing', 'cybersecurity_operations_center_carbon_and_sustainability_awareness', 'cybersecurity_operations_center_cross_pbc_event_federation', 'cybersecurity_operations_center_governed_ai_agent_execution')`.
- Exact key: `'docs': ('SPECIFICATION.md', 'RELEASE_EVIDENCE.md')`.
- Exact key: `'configuration': ('CYBERSECURITY_OPERATIONS_CENTER_DATABASE_URL', 'CYBERSECURITY_OPERATIONS_CENTER_EVENT_TOPIC', 'CYBERSECURITY_OPERATIONS_CENTER_RETRY_LIMIT', 'CYBERSECURITY_OPERATIONS_CENTER_DEFAULT_POLICY')`.

### 1. Canonical detection-to-alert lifecycle
**Justification:** Analysts need one shared lifecycle for detections as they become alerts, are triaged, escalated, closed, or reopened; otherwise queue metrics and handoffs are unreliable.
**Improvement:** Define a state machine for `security_alert` that covers new, deduplicated, enriched, triaged, escalated, suppressed, contained, closed, and reopened states, with transition reasons and actor attribution exposed in `CybersecurityOperationsCenterWorkbench`.
**Acceptance evidence:** State transition tests for `security_alert`, invalid transition rejection cases, workbench badges showing current state and prior state, and release evidence mapping lifecycle steps to `cybersecurity_operations_center_create_security_alert_workflow`.

### 2. First-class detection entity model inside alert intake
**Justification:** The manifest starts at `security_alert`, but operators still need the upstream detection context to explain why an alert exists and whether it was grouped correctly.
**Improvement:** Add explicit detection fields to alert intake for source event ID, detection timestamp, detection rule ID, confidence, tactic tags, and raw evidence checksum without creating a new cross-domain table boundary.
**Acceptance evidence:** `POST /security-alerts` contract examples showing detection metadata, persistence tests on `security_alert`, and detail-view traces linking alert records to immutable detection context.

### 3. Alert deduplication and correlation policy
**Justification:** SOC queues fail when duplicate alerts inflate severity and response counts, especially across repeated sensor emissions and replayed events.
**Improvement:** Implement policy-driven deduplication on `security_alert` using asset, principal, indicator, detection rule, time window, and evidence hash keys, with explicit merge versus keep-separate reasoning.
**Acceptance evidence:** Deduplication fixtures with merge outcomes, configurable policy entries in `cybersecurity_operations_center_policy_rule`, and workbench correlation cards that show sibling alerts and merge lineage.

### 4. Triaging workbench lanes by urgency and confidence
**Justification:** A single alert grid does not match SOC practice; analysts need differentiated lanes for urgent triage, noisy backlog, and watchlist monitoring.
**Improvement:** Split `CybersecurityOperationsCenterWorkbench` into triage lanes based on severity, confidence, blast radius, SLA breach risk, and policy suppression status, with saved analyst filters.
**Acceptance evidence:** UI route coverage for lane filters, analytics proving lane counts roll into `cybersecurity_operations_center_workbench_metric`, and screenshots referenced in `RELEASE_EVIDENCE.md`.

### 5. Structured enrichment record on alerts
**Justification:** Enrichment steps are often where cases become actionable, but ad hoc notes do not create reusable evidence or measurable turnaround times.
**Improvement:** Extend `security_alert` updates to store structured enrichment facts such as asset criticality, user sensitivity, network exposure, prior incident links, and indicator freshness, plus who or what supplied each fact.
**Acceptance evidence:** Schema and model tests for enrichment fields, audit history of enrichment sources, and detail-page evidence panels listing enrichment provenance for each alert.

### 6. Incident promotion criteria tied to alert clusters
**Justification:** Promotion from alert to incident needs a governed threshold or analysts will either over-open incidents or suppress real multi-signal attacks.
**Improvement:** Add `security_incident` promotion rules that consider alert cluster size, asset criticality, repeated detections, containment need, and policy exceptions, with previewed impact before create.
**Acceptance evidence:** Policy simulations for promotion thresholds, `POST /security-incidents` preview fixtures, and workflow tests showing alert-to-incident linkage under `cybersecurity_operations_center_record_security_incident_workflow`.

### 7. Case timeline spanning alert, incident, containment, and evidence
**Justification:** SOC reviews depend on a single case narrative, not separate tables that require manual reconstruction after an event.
**Improvement:** Build a case timeline projection that unifies `security_alert`, `security_incident`, `containment_action`, and `response_evidence` into one chronological view with actor, action, and outcome summaries.
**Acceptance evidence:** Projection replay tests from emitted and consumed events, case timeline rendering in `CybersecurityOperationsCenterDetail`, and time-ordered export samples referenced in `RELEASE_EVIDENCE.md`.

### 8. Evidence chain-of-custody model
**Justification:** Response evidence loses credibility if the system cannot show where it came from, who handled it, and whether it was altered.
**Improvement:** Expand `response_evidence` to track collection source, hash, acquisition time, storage location reference, handling history, redaction status, and admissibility notes.
**Acceptance evidence:** Migration coverage for custody fields, append-only handling history tests, and chain-of-custody views accessible from incident detail pages.

### 9. Containment action approval boundaries
**Justification:** Containment can disrupt business operations, so analyst autonomy must be bounded by policy, asset sensitivity, and action risk.
**Improvement:** Classify `containment_action` types into no-approval, supervisor-approval, and exception-approval paths, with action-specific prerequisites and rollback instructions.
**Acceptance evidence:** Permission and policy tests on `containment_action`, approval banners in the workbench, and release evidence showing blocked high-risk actions without approval.

### 10. Threat intelligence boundary and provenance controls
**Justification:** Threat intel only helps triage if analysts can distinguish between observed facts, external reports, and derived conclusions.
**Improvement:** Segment `threat_intel` records into observed indicator, assessed relationship, campaign context, and analyst inference sections, each with provenance, confidence, and expiry controls.
**Acceptance evidence:** Typed `threat_intel` fixtures with provenance metadata, UI provenance chips in detail views, and tests that prevent derived conclusions from overwriting observed facts.

### 11. Indicator expiry and revalidation workflow
**Justification:** Stale indicators create false positives and wasted containment work if they remain active beyond their useful horizon.
**Improvement:** Add expiry, revalidation, and retirement logic to `threat_intel` so indicators age out or require analyst renewal based on source confidence and recent observation.
**Acceptance evidence:** Scheduler or rule-engine tests for expiry transitions, workbench warning states for expiring intel, and KPI outputs showing active versus retired indicator counts.

### 12. Asset exposure linkage to active cases
**Justification:** Analysts need to know whether an exposed asset is already under active investigation or containment before starting parallel work.
**Improvement:** Extend `asset_exposure` views with incident and alert linkage summaries, criticality, internet exposure context, and open containment actions relevant to the same asset.
**Acceptance evidence:** Joined projection tests using owned tables only, asset exposure detail panels surfacing active case references, and event lineage proving linkage refresh after updates.

### 13. Playbook execution stages with observable checkpoints
**Justification:** A playbook run that is merely “running” hides where automation stalled and what a responder must do next.
**Improvement:** Break `playbook_run` into staged checkpoints such as preconditions, evidence collection, analyst approval, containment, validation, communications, and closure verification.
**Acceptance evidence:** `playbook_run` stage transition tests, stage-level timestamps and assignees in the workbench, and release evidence showing partial-failure visibility rather than opaque run failures.

### 14. Human-in-the-loop breakpoints for risky automation
**Justification:** SOAR-style automation is useful only when risky steps pause at the correct moment instead of executing with blind trust.
**Improvement:** Add human confirmation breakpoints to `playbook_run` for user lockouts, host isolation, credential disablement, mass suppression, and cross-case evidence deletion.
**Acceptance evidence:** Breakpoint configuration rules in `cybersecurity_operations_center_policy_rule`, blocked automation traces, and assistant panel previews requiring explicit human confirmation.

### 15. Alert suppression governance
**Justification:** Suppression reduces noise, but ungoverned suppression can hide attacks or make detection drift invisible.
**Improvement:** Model suppression on `security_alert` with duration, reason, scope, owner, review date, and linked detection logic so temporary tuning does not become silent permanent blindness.
**Acceptance evidence:** Suppression approval tests, overdue suppression review queues, and metrics showing suppression volume, expiry, and reactivation outcomes.

### 16. False-positive capture and feedback loop
**Justification:** Analysts repeatedly classify bad detections; the platform should learn from that feedback instead of burying it in comments.
**Improvement:** Add structured false-positive causes, affected detection rule IDs, evidence references, and remediation recommendations to closed `security_alert` records.
**Acceptance evidence:** Alert closure fixtures with false-positive taxonomies, analytics feeding `cybersecurity_operations_center_workbench_metric`, and detail views showing whether rule tuning was requested.

### 17. True-positive to campaign clustering
**Justification:** SOC operations improve when recurring alerts and incidents are grouped into campaigns or waves rather than treated as isolated records.
**Improvement:** Create a campaign clustering projection that groups `security_alert` and `security_incident` records by actor hypothesis, infrastructure overlap, indicator reuse, timing, and target profile.
**Acceptance evidence:** Correlation tests across alert and incident records, campaign summary widgets in the workbench, and release evidence demonstrating cluster drill-down from analyst queue to case detail.

### 18. Incident severity with explainable scoring
**Justification:** Severity must be defendable to responders and auditors; free-form labels lead to inconsistent escalation and reporting.
**Improvement:** Calculate `security_incident` severity from business criticality, spread, credential exposure, data sensitivity, containment status, and analyst override rationale, with factor-level explanations.
**Acceptance evidence:** Severity scoring tests, override audit history, and detail-page factor breakdowns aligned with `cybersecurity_operations_center_risk_score`.

### 19. Incident commander and ownership model
**Justification:** Major incidents fail when command responsibility is implied rather than explicitly assigned and visible.
**Improvement:** Add incident commander, communications owner, evidence owner, and containment owner roles to `security_incident`, with handoff timestamps and pending-task indicators.
**Acceptance evidence:** Role assignment validation tests, workbench cards showing current owners, and SLA metrics for handoff gaps and unowned incidents.

### 20. Evidence request workflow from cases
**Justification:** Investigations often depend on targeted evidence requests, and unmanaged requests cause delay, duplication, and missing artifacts.
**Improvement:** Let analysts create evidence requests from `security_incident` or `security_alert`, track request status, due date, source system, and returned artifacts inside `response_evidence`.
**Acceptance evidence:** Request lifecycle tests, UI request tables on incident detail, and metrics showing turnaround time from request creation to fulfilled evidence.

### 21. Event-sourced operational history tuned for SOC actions
**Justification:** The advanced capability for event-sourced history should capture SOC-specific commands, not just generic CRUD transitions.
**Improvement:** Emit event history entries for triage changes, enrichment additions, playbook checkpoint decisions, containment approvals, evidence uploads, and suppression changes with actor and reason data.
**Acceptance evidence:** Replay tests on SOC-specific event envelopes, event browse views in the detail page, and proof that `CybersecurityOperationsCenterUpdated` corresponds to material operational changes.

### 22. Consumed event handlers with bounded side effects
**Justification:** `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` should update SOC behavior predictably without leaking into unrelated domains.
**Improvement:** Implement handlers that recalculate policy evaluations, mark evidence bundles as sealed, refresh KPI projections, and open exceptions when dependencies become stale or contradictory.
**Acceptance evidence:** Idempotency tests for each consumed event, dead-letter fixtures for malformed events, and workbench notices showing which incoming event changed local SOC state.

### 23. API boundary for alert updates and triage commands
**Justification:** SOC work needs command-oriented APIs, not only create endpoints, or the UI and assistant will rely on unsafe direct datastore mutation patterns.
**Improvement:** Add bounded command surfaces for triage, enrich, suppress, promote, close, reopen, and link-to-incident operations while preserving the existing create endpoints as intake boundaries.
**Acceptance evidence:** Route contract documentation adjacent to the manifest APIs, request/response fixtures, and tests proving commands enforce permissions and policy rules.

### 24. Validation-only API mode for detection and incident intake
**Justification:** Analysts and upstream systems need to know whether a payload would be accepted before creating noisy partial records.
**Improvement:** Support validation-only execution for alert, incident, asset exposure, threat intel, and playbook payloads that returns rule outcomes, required fields, and policy blockers without persistence.
**Acceptance evidence:** API fixtures showing dry-run responses, tests confirming no table mutation occurs, and assistant panel previews using the same validation-only path.

### 25. Bulk intake with partial success semantics
**Justification:** Security teams commonly import detection waves or indicator batches; all-or-nothing intake wastes time and obscures which rows failed.
**Improvement:** Extend alert and threat intel intake to accept batches with row-level validation, row-level idempotency keys, and resumable reprocessing for failed entries.
**Acceptance evidence:** Batch fixture coverage for `POST /security-alerts` and `POST /threat-intels`, resumable job traces, and workbench reporting on accepted, rejected, and duplicate rows.

### 26. Retry and dead-letter operations for failed automations
**Justification:** When playbooks or event handlers fail, responders need a visible remediation queue rather than opaque background retries.
**Improvement:** Create SOC dead-letter views for failed `playbook_run` steps and event handling attempts, with failure reason, retry eligibility, required fix, and related case context.
**Acceptance evidence:** Dead-letter queue tests tied to `retry_dead_letter_evidence`, manual retry actions in the workbench, and release evidence showing failure explanation and safe replay behavior.

### 27. Analyst assistant skills for triage summaries
**Justification:** The manifest includes `ai_agent_task_assistance`, but analysts need bounded skills that summarize evidence without fabricating unsupported claims.
**Improvement:** Add assistant skills that draft triage summaries, list likely next steps, identify missing evidence, and suggest playbook checkpoints using only referenced alert, incident, and evidence data.
**Acceptance evidence:** Skill manifests or configuration linked from `CybersecurityOperationsCenterAssistantPanel`, prompt-to-output regression tests, and source citation displays for every generated summary.

### 28. Assistant skill for threat intel enrichment with guardrails
**Justification:** Analysts benefit from drafted enrichment, but threat intel handling requires explicit separation between sourced facts and machine suggestions.
**Improvement:** Add an assistant skill that proposes `threat_intel` enrichment candidates, confidence ratings, and expiry windows while forcing human confirmation before record mutation.
**Acceptance evidence:** Preview/confirm interaction tests, blocked direct-write evidence, and audit entries recording accepted versus rejected assistant proposals.

### 29. Supervisor workbench for queue balancing
**Justification:** Supervisors need to rebalance overloaded analysts and overdue cases before response quality drops.
**Improvement:** Build supervisor views in `CybersecurityOperationsCenterWorkbench` for queue depth, analyst assignment load, overdue triage, containment bottlenecks, and incident commander span of control.
**Acceptance evidence:** Persona-aware UI tests, metrics rollups for work distribution, and screenshots or route traces referenced in `RELEASE_EVIDENCE.md`.

### 30. Evidence reviewer workbench for redaction and release
**Justification:** Evidence often needs review before it can be shared with stakeholders, responders, or auditors.
**Improvement:** Add a reviewer lane that surfaces `response_evidence` requiring redaction, approval, retention tagging, or external release decisions, with side-by-side original and redacted views.
**Acceptance evidence:** Permission-aware evidence review tests, redaction status projections, and release records showing reviewer decisions and timestamps.

### 31. Metrics for mean time to triage, contain, and close
**Justification:** Core SOC performance must be visible as time-based operational metrics rather than ad hoc spreadsheet calculations.
**Improvement:** Define `cybersecurity_operations_center_workbench_metric` measures for mean time to triage, mean time to containment, mean time to evidence readiness, and mean time to close, segmented by severity and queue.
**Acceptance evidence:** Metric definition artifacts, projection tests with known timestamps, and workbench charts that match fixture-based expected values.

### 32. Metrics for detection quality and analyst trust
**Justification:** Detection programs degrade if the system tracks only volume and not whether alerts deserve analyst attention.
**Improvement:** Add detection-quality metrics for duplicate rate, suppression rate, false-positive rate, promotion-to-incident rate, reopened rate, and median analyst confidence by detection source.
**Acceptance evidence:** Analytics tests against alert lifecycle fixtures, dashboard widgets showing trend lines, and release evidence tying metrics back to source records.

### 33. Metrics for playbook automation effectiveness
**Justification:** Automation should prove that it reduces toil without raising risk or silently failing.
**Improvement:** Track `playbook_run` success rate, breakpoint frequency, manual override rate, rollback rate, and average time saved compared with fully manual execution.
**Acceptance evidence:** Metric computation tests using staged playbook runs, workbench automation panels, and evidence snapshots in `RELEASE_EVIDENCE.md`.

### 34. Metrics for evidence completeness and admissibility
**Justification:** Cases are weaker when required evidence is missing, late, or unverifiable.
**Improvement:** Score each incident for evidence completeness based on required artifact classes, custody integrity, sealing status, and unresolved redaction blockers.
**Acceptance evidence:** Completeness scoring fixtures, UI indicators on incident detail views, and control assertions opening exceptions when evidence thresholds are missed.

### 35. Detection-to-incident graph on the detail page
**Justification:** Responders need to see how one detection expanded into multiple alerts, incidents, containment actions, and evidence branches.
**Improvement:** Add a graph or relationship map to `CybersecurityOperationsCenterDetail` that visualizes linked `security_alert`, `security_incident`, `containment_action`, `response_evidence`, and `threat_intel` nodes.
**Acceptance evidence:** UI rendering tests for graph data, API or projection fixtures supporting relationship edges, and screenshots included in release evidence.

### 36. Threat intel to playbook recommendation boundary
**Justification:** Threat intel should guide response options, but it must not auto-execute response steps without policy and operator review.
**Improvement:** Introduce a recommendation layer that maps `threat_intel` patterns to candidate `playbook_run` templates and containment options while requiring explicit analyst selection.
**Acceptance evidence:** Recommendation fixtures showing intel-to-playbook mappings, tests proving no auto-execution occurs, and assistant panel suggestions with policy rationale.

### 37. Multi-tenant separation of policy, metrics, and evidence
**Justification:** The advanced multi-tenant capability needs SOC-specific proof that one tenant's cases, indicators, and controls cannot bleed into another's.
**Improvement:** Partition `security_alert`, `security_incident`, `threat_intel`, `response_evidence`, and derived metrics by tenant, tenant policy, and tenant retention settings, including tenant-scoped assistant context.
**Acceptance evidence:** Tenant isolation tests across all core tables and projections, negative fixtures for cross-tenant access, and release evidence documenting tenant-specific workbench filtering.

### 38. Retention and legal-hold controls for incident evidence
**Justification:** Evidence retention rules differ from operational convenience and must survive case closure.
**Improvement:** Add retention policy, purge eligibility, legal-hold status, and destruction approval tracking to `response_evidence` and linked `security_incident` records.
**Acceptance evidence:** Retention scheduler tests, blocked purge cases under legal hold, and reviewer screens showing disposition decisions and future purge dates.

### 39. Cryptographic proof of sealed evidence bundles
**Justification:** The manifest's cryptographic audit proof capability should materially strengthen evidence integrity, not remain a generic platform checkbox.
**Improvement:** Create hash-chained sealed bundles for selected `response_evidence` sets tied to `AuditEventSealed`, with verification metadata stored in owned SOC tables.
**Acceptance evidence:** Bundle verification tests, evidence-seal detail views, and release evidence demonstrating successful proof validation for a sealed bundle.

### 40. Continuous control tests for SOC process integrity
**Justification:** Controls should detect missing approvals, evidence gaps, and overdue containment while incidents are active.
**Improvement:** Implement `cybersecurity_operations_center_control_assertion` checks for unapproved high-risk containment, stale untriaged high-severity alerts, missing incident owners, and unresolved evidence requests beyond SLA.
**Acceptance evidence:** Control assertion fixtures that open `CybersecurityOperationsCenterExceptionOpened`, dashboards showing active control failures, and remediation traces after fixes are applied.

### 41. Counterfactual simulation for containment decisions
**Justification:** Responders often need to compare isolate-now versus monitor-longer choices before acting on critical systems.
**Improvement:** Use the counterfactual simulation capability to model containment options, expected operational impact, residual alert volume, and evidence collection tradeoffs before executing `containment_action`.
**Acceptance evidence:** Simulation input/output examples, non-mutating execution tests, and workbench comparison panels attached to containment approval flows.

### 42. Predictive backlog and SLA breach risk scoring
**Justification:** Supervisors need forward-looking risk signals to prevent queue collapse, not just after-the-fact breach counts.
**Improvement:** Apply `cybersecurity_operations_center_predictive_risk_scoring` to estimate which alerts, incidents, evidence requests, and playbook runs are likely to breach SLA or require escalation soon.
**Acceptance evidence:** Model feature manifests derived from owned SOC data, calibration tests against historical fixtures, and risk badges visible in triage and supervisor workbench lanes.

### 43. Anomaly detection on analyst and automation behavior
**Justification:** SOC quality issues can come from process drift, not only attack activity, so the platform should flag unusual operations behavior too.
**Improvement:** Use autonomous anomaly detection to surface suspicious spikes in suppressions, repeated rollback of playbook stages, unusual evidence deletion attempts, or abrupt severity downgrades.
**Acceptance evidence:** Anomaly detection test cases with explainable output, review feedback capture for false positives, and workbench anomaly cards tied to affected records.

### 44. Release evidence that proves SOC-specific readiness
**Justification:** The docs surface includes `RELEASE_EVIDENCE.md`; SOC delivery should prove operational readiness, not only code completion.
**Improvement:** Expand release evidence to include alert lifecycle coverage, incident promotion tests, containment approval traces, dead-letter remediation, assistant guardrail checks, and workbench persona screenshots.
**Acceptance evidence:** Updated `RELEASE_EVIDENCE.md` checklist references inside this backlog item, artifact links or placeholders for each proof class, and test output summaries aligned to the SOC flows above.

### 45. Specification updates for event and API boundaries
**Justification:** SOC ownership gets blurred quickly unless the specification states exactly which commands, events, and projections belong inside this PBC.
**Improvement:** Tighten `SPECIFICATION.md` to document alert intake, incident promotion, containment approval, evidence sealing, threat intel recommendation, and event-handling boundaries for the package.
**Acceptance evidence:** Specification sections mapped to manifest keys, API and event examples consistent with tests, and review notes showing no vendor-specific SIEM or SOAR coupling.

### 46. Policy rule test harness for SOC tuning
**Justification:** Analysts and supervisors need a safe way to tune deduplication, suppression, escalation, and containment approval logic without code edits.
**Improvement:** Build a simulation harness around `cybersecurity_operations_center_policy_rule` so operators can test policy changes against representative alert and incident fixtures before activation.
**Acceptance evidence:** Policy simulation tests with before/after outcome counts, workbench previews of proposed policy effects, and activation audit trails showing which simulation run justified the change.

### 47. Runtime parameter bounds for operational safety
**Justification:** Retry counts, suppression windows, and enrichment timeouts should be constrained to values that keep the SOC stable.
**Improvement:** Add bounded validation and tenant-safe overrides for `cybersecurity_operations_center_runtime_parameter`, especially values derived from `CYBERSECURITY_OPERATIONS_CENTER_RETRY_LIMIT` and `CYBERSECURITY_OPERATIONS_CENTER_DEFAULT_POLICY`.
**Acceptance evidence:** Parameter validation tests, workbench forms enforcing safe ranges, and audit history showing who changed an operational parameter and why.

### 48. Outbox and inbox lineage on every case-affecting change
**Justification:** SOC debugging is faster when analysts can see which commands emitted which events and which handlers consumed them.
**Improvement:** Expose AppGen-X inbox/outbox lineage for `security_alert`, `security_incident`, `playbook_run`, and `containment_action` changes directly from the detail page and assistant context.
**Acceptance evidence:** Lineage projection tests, linked event views in `CybersecurityOperationsCenterDetail`, and dead-letter records referencing original inbox or outbox entries.

### 49. Analyst handoff packet generation
**Justification:** Shift changes are risky if the next analyst receives only scattered notes and partial context.
**Improvement:** Generate structured handoff packets from active alerts and incidents with summary, open questions, pending approvals, pending evidence, next checkpoints, and cited source records.
**Acceptance evidence:** Assistant-assisted packet generation tests, supervisor review flows, and workbench export views proving packets are sourced from current case data rather than free-form text.

### 50. Closure readiness checklist for incidents and campaigns
**Justification:** Cases should close only when evidence, containment validation, owner signoff, and follow-up tasks are complete; otherwise closure metrics become misleading.
**Improvement:** Add a governed closure checklist for `security_incident` and clustered campaign views that requires evidence completeness, containment verification, final severity confirmation, lesson capture, and downstream ticket or task linkage where needed.
**Acceptance evidence:** Closure gating tests, checklist completion panels in the detail page, reopened-case fixtures when required evidence is missing, and release evidence showing an end-to-end close flow.
