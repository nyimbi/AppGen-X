# Construction Project Controls Improvement Backlog

## Current Domain Evidence Used

- Exact `pbc`: `construction_project_controls`.
- Exact `label`: `Construction Project Controls`.
- Exact `description`: `Construction budgets, schedules, RFIs, submittals, change events, field progress, and site risk controls`.
- Exact `tables`: `construction_project`, `work_package`, `rfi`, `submittal`, `site_progress`, `change_event`, `schedule_risk`, `construction_project_controls_policy_rule`, `construction_project_controls_runtime_parameter`, `construction_project_controls_schema_extension`, `construction_project_controls_control_assertion`, `construction_project_controls_governed_model`.
- Exact `apis`: `POST /construction-projects`, `POST /work-packages`, `POST /rfis`, `POST /submittals`, `POST /site-progresss`, `GET /construction-project-controls-workbench`.
- Exact `workflows`: `construction_project_controls_create_construction_project_workflow`, `construction_project_controls_record_work_package_workflow`.
- Exact `ui_fragments`: `ConstructionProjectControlsWorkbench`, `ConstructionProjectControlsDetail`, `ConstructionProjectControlsAssistantPanel`.
- Exact `analytics`: `construction_project_controls_risk_score`, `construction_project_controls_workbench_metric`.
- Exact `emits`: `ConstructionProjectControlsCreated`, `ConstructionProjectControlsUpdated`, `ConstructionProjectControlsApproved`, `ConstructionProjectControlsExceptionOpened`.
- Exact `consumes`: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Exact `docs`: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`.
- Exact `advanced_capabilities`: `construction_project_controls_event_sourced_operational_history`, `construction_project_controls_predictive_risk_scoring`, `construction_project_controls_counterfactual_scenario_simulation`, `construction_project_controls_cryptographic_audit_proofs`, `construction_project_controls_continuous_control_testing`, `construction_project_controls_governed_ai_agent_execution`.
- Exact `configuration`: `CONSTRUCTION_PROJECT_CONTROLS_DATABASE_URL`, `CONSTRUCTION_PROJECT_CONTROLS_EVENT_TOPIC`, `CONSTRUCTION_PROJECT_CONTROLS_RETRY_LIMIT`, `CONSTRUCTION_PROJECT_CONTROLS_DEFAULT_POLICY`.

### 1. Canonical WBS and control-account hierarchy

**Justification:** `work_package` needs a governed WBS, control-account, and cost-code structure so baseline, progress, earned value, and change impacts roll up the same way every reporting period.

**Improvement:** Extend `work_package` and `construction_project` so each package carries WBS code, parent/child relationships, control account, discipline, area, responsible contractor, and reporting level. Show the hierarchy in `ConstructionProjectControlsDetail` with expand/collapse, rollup totals, and orphan-package warnings.

**Acceptance evidence:** Migration and contract tests prove WBS parentage integrity, workbench screenshots show hierarchical rollups in `GET /construction-project-controls-workbench`, and `RELEASE_EVIDENCE.md` includes a WBS navigation walkthrough for `construction_project_controls`.

### 2. Baseline schedule versioning and freeze control

**Justification:** Project controls depends on a frozen baseline; without versioned baseline dates there is no defensible variance or forecast discussion.

**Improvement:** Add baseline revision records tied to `construction_project` and `work_package` for original baseline, current approved baseline, approval date, approver, and freeze reason. Surface baseline swaps through `construction_project_controls_create_construction_project_workflow` and make re-baselining impossible without approval evidence.

**Acceptance evidence:** Tests show one active approved baseline per project, emitted evidence links baseline approvals to `ConstructionProjectControlsApproved`, and `SPECIFICATION.md` documents baseline freeze and re-baseline rules.

### 3. Quantity-based progress measurement rules

**Justification:** `site_progress` needs more than a free-form percent complete field; disciplined progress measurement requires quantities, units, and rule-based percent complete methods.

**Improvement:** Add progress methods per `work_package` such as quantity installed, milestone complete, weighted steps, and level-of-effort. Capture planned quantity, installed quantity, measurement unit, and measurement date in `site_progress`, with automatic percent complete derived from the configured method.

**Acceptance evidence:** Regression tests show consistent percent-complete calculations across methods, `ConstructionProjectControlsWorkbench` displays planned versus installed quantities, and release evidence includes a quantity-driven status cycle.

### 4. Earned value management engine

**Justification:** Earned value is central to construction project controls and is absent unless planned value, earned value, and actual cost are calculated from approved baseline and progress records.

**Improvement:** Add periodized BCWS, BCWP, ACWP, CPI, SPI, CV, and SV calculations at `work_package`, control-account, and project levels. Tie period close to approved `site_progress` and cost records so earned value reflects governed status data rather than ad hoc spreadsheet exports.

**Acceptance evidence:** Unit tests validate CPI and SPI calculations, dashboard cards expose earned value metrics through `construction_project_controls_workbench_metric`, and `RELEASE_EVIDENCE.md` includes a monthly EV calculation example.

### 5. Commitment, actual, and remaining-cost control

**Justification:** Cost control requires visibility into commitments, accruals, actuals, and remaining-to-complete, not just a lump-sum project budget.

**Improvement:** Expand `construction_project` and `work_package` cost fields to track original budget, approved budget, committed cost, accruals, invoiced cost, paid cost, and remaining cost. Add variance views that isolate scope-driven changes from production overruns.

**Acceptance evidence:** Data model tests prove period cost rollups, workbench panels show budget-versus-actual-versus-forecast by WBS, and release evidence includes a cost-control review pack for one reporting period.

### 6. Forecast engine for ETC and EAC

**Justification:** A controls package must support forward-looking cost and schedule forecast, not only current-state reporting.

**Improvement:** Add estimate-to-complete and estimate-at-completion logic using earned value trends, remaining quantities, open `change_event` exposure, and active `schedule_risk` items. Provide manual forecast override with mandatory explanation and comparison to system forecast.

**Acceptance evidence:** Tests cover system forecast, manual override, and variance from approved budget, `ConstructionProjectControlsDetail` shows ETC and EAC history, and `construction_project_controls_risk_score` reflects forecast deterioration scenarios.

### 7. Change impact chain from trend to approved event

**Justification:** Change control is weak unless early trend signals, formal change events, budget impacts, and baseline impacts are linked end to end.

**Improvement:** Extend `change_event` to capture trend reference, cause category, scope impact, cost impact, schedule impact, affected WBS codes, affected submittals or RFIs, and approval state. Ensure approved changes update forecast and baseline impact views without rewriting prior-period facts.

**Acceptance evidence:** Workflow tests trace one change from trend log to approved event, workbench cards show pending versus approved impacts, and release evidence includes before/after baseline and forecast snapshots.

### 8. Trend log before formal change approval

**Justification:** Controls teams need early visibility into likely commercial movement before a formal change is approved.

**Improvement:** Add a governed pre-change trend register under `change_event` with probability, rough-order cost range, potential schedule effect, owner, and next decision date. Show trend aging and conversion rate in `ConstructionProjectControlsWorkbench`.

**Acceptance evidence:** Tests prove trends can convert to formal `change_event` records without losing history, dashboards show trend exposure by project, and `SPECIFICATION.md` defines the trend-to-change handoff.

### 9. Contractor progress intake quality gates

**Justification:** Contractor-reported progress is often the noisiest input in project controls and needs strict validation before it affects baseline variance or payment readiness.

**Improvement:** Gate `POST /site-progresss` behind rules for date range validity, duplicate update detection, quantity overstatement, unsupported measurement units, missing photo or report evidence, and unauthorized contractor submissions. Route failures to a review queue instead of silently dropping them.

**Acceptance evidence:** API tests reject invalid contractor submissions with specific reasons, dead-letter evidence is visible for failed intake attempts, and `ConstructionProjectControlsAssistantPanel` can summarize why a progress update was held.

### 10. Schedule update quality rules

**Justification:** Schedule variance is only useful when updates follow quality rules for logic, dates, and status consistency.

**Improvement:** Add `schedule_risk` and `work_package` validations for open-ended activities, negative float spikes, missing successors, actual dates after data date violations, and percent-complete/date contradictions. Display quality flags before a schedule update is accepted into the reporting cycle.

**Acceptance evidence:** Validation tests catch broken logic scenarios, the workbench exposes a schedule-quality queue, and release evidence contains one accepted and one rejected update package with reasons.

### 11. Critical-path and near-critical monitoring

**Justification:** Project controls users need visibility into path movement and float erosion, not just a flat list of risks.

**Improvement:** Add path classification to `schedule_risk` and `work_package` for critical, near-critical, and driving-path status, including current float, prior float, and path owner. Show path movement on the main workbench and trigger exceptions when float drops past policy thresholds.

**Acceptance evidence:** Tests prove float threshold exceptions open `ConstructionProjectControlsExceptionOpened`, dashboards show current and prior path status, and `construction_project_controls_policy_rule` stores configurable float limits.

### 12. Four-week and twelve-week lookahead workbench

**Justification:** Short-horizon execution control belongs in the package so planning, progress, and risk data stay connected.

**Improvement:** Add lookahead views driven by `work_package`, `submittal`, `rfi`, and `schedule_risk` data to show upcoming work, blockers, readiness constraints, and owner actions over four-week and twelve-week windows.

**Acceptance evidence:** UI tests verify lookahead filtering and drill-through in `ConstructionProjectControlsWorkbench`, API support exists for date-window queries, and release evidence includes a lookahead review session.

### 13. RFI impact linkage to WBS and schedule

**Justification:** `rfi` records are operationally weak if they are not tied to affected work scope, activity windows, and decision deadlines.

**Improvement:** Extend `rfi` with affected WBS, affected activity or milestone, required-by date, schedule impact classification, and workaround status. Highlight overdue RFIs that threaten the current baseline or near-term lookahead.

**Acceptance evidence:** Tests validate RFI linkage to `work_package`, dashboards show open RFIs by criticality and due date, and release evidence includes one RFI-driven schedule impact trace.

### 14. Submittal constraint and approval tracking

**Justification:** `submittal` approval timing often drives field readiness and contractor progress, so constraint management must be explicit.

**Improvement:** Add `submittal` fields for planned submit date, required approval date, approval cycle count, linked WBS, linked procurement or fabrication milestone, and downstream work blocked by late approval. Surface submittal aging and blocked-work views in the workbench.

**Acceptance evidence:** Tests show blocked-work alerts from late submittals, workbench cards expose turnaround time and cycle count, and `SPECIFICATION.md` describes submittal readiness logic.

### 15. Separate risk register and issue register behavior

**Justification:** `schedule_risk` should not carry both uncertain future threats and already-realized issues with the same lifecycle.

**Improvement:** Split risk and issue handling within `schedule_risk` so threats, opportunities, realized issues, mitigations, triggers, owners, and closure evidence follow distinct state models. Provide conversion from risk to issue while preserving the original trigger and mitigation history.

**Acceptance evidence:** Tests prove risk-to-issue conversion retains lineage, dashboards show separate risk and issue counts, and release evidence includes realized-issue escalation examples.

### 16. Recovery scenario simulation

**Justification:** Project controls decisions often depend on testing recovery plans before committing resources or changing the baseline.

**Improvement:** Use `construction_project_controls_counterfactual_scenario_simulation` to model acceleration, resequencing, crew changes, and partial scope deferral against forecast cost and finish date. Keep scenarios separate from live data until approved.

**Acceptance evidence:** Simulation tests prove no live-table mutation, the workbench compares at least two recovery scenarios side by side, and `RELEASE_EVIDENCE.md` includes a recovery-decision pack for one delayed project.

### 17. Reporting period cutoff and status freeze

**Justification:** Monthly and weekly controls reporting needs a formal data date and freeze point so published variance numbers can be reproduced later.

**Improvement:** Add reporting period records with data date, cutoff timestamp, freeze owner, reopen reason, and published package hash. Lock period-bound `site_progress`, cost, and forecast edits after freeze unless a controlled reopen is approved.

**Acceptance evidence:** Tests reject edits after freeze without override approval, event history proves reopen lineage, and release evidence shows a frozen reporting pack with matching hash.

### 18. Calendar and weighting controls for progress measurement

**Justification:** Progress and forecast accuracy depend on consistent calendars, weighting rules, and period definitions across contractors and disciplines.

**Improvement:** Store reporting calendars, workday rules, weighting basis, and percent-complete rounding settings in `construction_project_controls_runtime_parameter`. Make the active calendar and weighting basis visible in `ConstructionProjectControlsDetail`.

**Acceptance evidence:** Parameter tests show tenant-safe overrides, workbench views display active calendar settings, and `CONSTRUCTION_PROJECT_CONTROLS_DEFAULT_POLICY` is linked to default measurement rules.

### 19. Progress evidence attachments and audit trace

**Justification:** Progress claims need traceable evidence such as photos, marked drawings, reports, or inspection notes before they change earned value or payment posture.

**Improvement:** Extend `site_progress` with evidence bundle metadata, uploader identity, capture timestamp, inspection reference, and acceptance status. Add audit views that show which approved progress points are evidence-backed and which were manually overridden.

**Acceptance evidence:** Tests enforce evidence requirements for configured progress methods, UI shows evidence status per update, and `AuditEventSealed` linkage is visible for published progress periods.

### 20. Payment milestone and valuation readiness

**Justification:** Contractor payment readiness is a common controls outcome and should derive from approved progress, approved change value, and held exceptions.

**Improvement:** Add valuation readiness states to `work_package` and `site_progress` so approved quantities, retention, disallowed costs, and blocked items roll into a payment-readiness view without turning the package into a finance ledger.

**Acceptance evidence:** Tests show blocked payment readiness when progress or change approvals are incomplete, dashboards expose ready/not-ready breakdowns, and release evidence includes a valuation support pack tied to one contractor.

### 21. Productivity benchmark analytics

**Justification:** Controls teams need to spot productivity deterioration before it becomes a major forecast problem.

**Improvement:** Add analytics for installed quantity per labor hour, crew-day output, and production trend versus plan at `work_package` level. Show deterioration alerts alongside cost and schedule impacts rather than as isolated charts.

**Acceptance evidence:** Metric definitions are published for `construction_project_controls_workbench_metric`, tests validate benchmark rollups, and dashboards show productivity trend overlays by WBS.

### 22. WBS-first dashboard hierarchy

**Justification:** Flat dashboards obscure whether variance sits in one control account, one contractor, or one reporting level.

**Improvement:** Rework `ConstructionProjectControlsWorkbench` so every major dashboard can pivot by WBS, control account, contractor, area, and discipline. Default project summaries should drill from project to control account to work package without changing screens.

**Acceptance evidence:** UI tests verify consistent drill-down behavior, screenshots show the same metric at three hierarchy levels, and release evidence includes dashboard navigation proof.

### 23. Executive portfolio dashboard for baseline, risk, and forecast

**Justification:** Senior users need concise portfolio views across multiple `construction_project` records without losing the ability to drill into troubled projects.

**Improvement:** Add portfolio rollups for baseline finish variance, contingency burn, forecast EAC variance, open change exposure, critical RFIs, blocked submittals, and high `construction_project_controls_risk_score` projects.

**Acceptance evidence:** Query tests prove portfolio totals reconcile to project totals, workbench cards rank projects by risk and forecast variance, and release evidence includes a portfolio review snapshot.

### 24. Detailed project-controls workbench by persona

**Justification:** `ConstructionProjectControlsDetail` should serve planners, cost engineers, package engineers, and project managers without making each persona sift through unrelated controls.

**Improvement:** Add persona-specific tabs for schedule, cost, progress, change, risk/issues, and release evidence, each with the actions and evidence that role actually needs. Preserve one shared project identity header so cross-domain context stays aligned.

**Acceptance evidence:** Permission-aware UI tests show persona-specific tabs, workbench telemetry proves role-based navigation paths, and `SPECIFICATION.md` documents the persona map for `construction_project_controls`.

### 25. Assistant skill for variance narratives

**Justification:** Controls teams spend significant time turning raw variance data into defensible explanations for reports and meetings.

**Improvement:** Add an assistant skill in `ConstructionProjectControlsAssistantPanel` that drafts schedule and cost variance narratives from baseline, progress, earned value, and open risk data, always citing the underlying WBS, period, and evidence records.

**Acceptance evidence:** Prompt-to-draft tests verify source citation and no silent mutation, the assistant preview shows linked records before use, and release evidence includes one AI-assisted narrative with reviewer approval.

### 26. Assistant skill for change impact analysis

**Justification:** Change discussions are slow when users manually gather affected scope, dates, and forecast impact from multiple screens.

**Improvement:** Add an agent workflow that summarizes one `change_event` across impacted WBS elements, current baseline finish, forecast shift, affected contractor progress, and unresolved RFIs or submittals. Require human confirmation before any recommended status change is applied.

**Acceptance evidence:** Skill tests prove the assistant reads through governed APIs only, audit history records every recommended action, and `ConstructionProjectControlsAssistantPanel` shows cited impact chains.

### 27. Assistant skill for RFI and submittal triage

**Justification:** The package already includes `agentic_document_instruction_intake`; it should help triage high-volume RFI and submittal queues in a controls-aware way.

**Improvement:** Add assistant commands that cluster overdue `rfi` and `submittal` records by impacted WBS, required-by date, contractor, and likely schedule consequence. Let users open a triage session directly from `ConstructionProjectControlsWorkbench`.

**Acceptance evidence:** Queue-triage tests verify stable clustering, the workbench opens prefiltered queues from assistant recommendations, and release evidence contains one triage session transcript with outcomes.

### 28. API boundary for baselines, forecast, and dashboard queries

**Justification:** The manifest exposes only create-style APIs plus one workbench query, which is too narrow for a controls package that needs governed read and action surfaces.

**Improvement:** Add explicit read and action APIs for baseline revisions, forecast snapshots, earned-value summaries, trend logs, lookahead views, and risk/issue queues while preserving the existing `POST /construction-projects`, `POST /work-packages`, `POST /rfis`, `POST /submittals`, `POST /site-progresss`, and `GET /construction-project-controls-workbench`.

**Acceptance evidence:** Route contract tests cover new APIs and backward compatibility for existing routes, `SPECIFICATION.md` includes API examples, and `RELEASE_EVIDENCE.md` captures one end-to-end dashboard query flow.

### 29. Backward-compatible repair for `POST /site-progresss`

**Justification:** The exact manifest route `POST /site-progresss` should remain supported, but the package also needs a corrected, predictable API surface for long-term integration quality.

**Improvement:** Keep `POST /site-progresss` working as a compatibility alias while introducing a corrected canonical route and deprecation notice in the API docs. Ensure both routes feed the same idempotent command handler and audit trail.

**Acceptance evidence:** API tests prove both routes behave identically, deprecation warnings appear only on the legacy path, and `RELEASE_EVIDENCE.md` records the compatibility decision and migration note.

### 30. Typed event model for controls milestones

**Justification:** `ConstructionProjectControlsCreated`, `ConstructionProjectControlsUpdated`, and `ConstructionProjectControlsApproved` are too broad to express baseline moves, period freeze, forecast publication, or major exception state changes.

**Improvement:** Add typed emitted events for baseline approved, period frozen, forecast published, change approved, risk escalated, and contractor progress accepted. Keep the existing emitted events as compatibility anchors while making downstream consumption more precise.

**Acceptance evidence:** Event schema tests validate payload shape and versioning, outbox tests prove ordering, and release evidence includes an event catalog tied to `CONSTRUCTION_PROJECT_CONTROLS_EVENT_TOPIC`.

### 31. Consumed-event reactions for policy and KPI changes

**Justification:** The existing `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged` subscriptions should materially alter controls behavior instead of merely being acknowledged.

**Improvement:** React to `PolicyChanged` by recalculating thresholds and permissions, to `OperationalKpiChanged` by refreshing risk and dashboard status, and to `AuditEventSealed` by locking published evidence bundles. Surface any failed reactions as operator-visible exceptions.

**Acceptance evidence:** Handler tests prove idempotent event processing, exception queues show failed reactions with retry state, and audit lineage links each projection change to its source event.

### 32. Event-sourced revision history for baseline and forecast records

**Justification:** `construction_project_controls_event_sourced_operational_history` should preserve who changed baseline, forecast, or status assumptions and when.

**Improvement:** Event-source revisions for baseline snapshots, forecast updates, reporting freezes, and approved manual overrides. Expose a timeline in `ConstructionProjectControlsDetail` that compares prior and current assumptions without requiring database inspection.

**Acceptance evidence:** Replay tests rebuild the same baseline and forecast state, timeline UI proves before/after visibility, and release evidence includes one reconstructed reporting cycle.

### 33. Idempotent handlers for repeated contractor and schedule submissions

**Justification:** Field systems and partner integrations frequently retry; project-controls logic must avoid double-counting progress or duplicate schedule updates.

**Improvement:** Use `idempotent_handlers` and explicit submission keys on `site_progress`, `change_event`, `rfi`, and `submittal` intake so duplicates are recognized before mutating rollups or event streams.

**Acceptance evidence:** Duplicate-submission tests show one accepted mutation and one recognized replay, operator views show replay status, and dead-letter logs remain clean for valid retries.

### 34. Policy thresholds for cost, float, and approval routing

**Justification:** `construction_project_controls_policy_rule` should represent real controls policy such as float erosion limits, approval levels, and contingency use thresholds.

**Improvement:** Add policy rules for change approval bands, forecast deterioration triggers, progress evidence requirements, float threshold escalation, and manual-override approval routing. Make policy simulation available before publishing rule changes.

**Acceptance evidence:** Rule-evaluation tests cover threshold crossings, policy simulation shows before/after effect, and `PolicyChanged` events propagate visible rule updates to the workbench.

### 35. Runtime parameters for calendars, currencies, and weighting logic

**Justification:** `construction_project_controls_runtime_parameter` should hold operational tuning that varies by tenant, project, or reporting regime without code edits.

**Improvement:** Add parameters for reporting calendar, base currency, unit precision, weighted-step definitions, lookahead horizon, risk score weighting, and variance-color thresholds. Show active parameter values directly in the relevant workbench views.

**Acceptance evidence:** Parameter validation tests reject out-of-range values, tenant-scoped overrides are visible and auditable, and release evidence includes one parameter change approval and rollback.

### 36. Continuous control testing for monthly reporting discipline

**Justification:** `construction_project_controls_continuous_control_testing` should continuously check whether the package is operating within agreed controls, not just whether APIs respond.

**Improvement:** Implement continuous assertions in `construction_project_controls_control_assertion` for missing baseline, late period freeze, negative float without escalation, forecast older than policy allows, unapproved change in active forecast, and evidence-free accepted progress.

**Acceptance evidence:** Assertion tests produce predictable pass/fail results, failing controls open operator-visible exceptions, and `RELEASE_EVIDENCE.md` includes a control-test summary for one release candidate.

### 37. Anomaly detection on progress and cost claims

**Justification:** `construction_project_controls_autonomous_anomaly_detection` should help controls teams spot overstated progress, unusual unit rates, and abrupt float or cost movement.

**Improvement:** Add anomaly detection for sudden percent-complete jumps, unit-cost spikes, repeated late submittals on the same contractor, and schedule compression without supporting mitigation actions. Route anomalies to review, never directly to auto-approval.

**Acceptance evidence:** Calibration tests show expected anomaly classes, reviewers can mark true or false positives in the workbench, and `construction_project_controls_risk_score` incorporates confirmed anomalies only.

### 38. Schema expansion for baseline, forecast, and cutoff snapshots

**Justification:** The listed tables cover core records, but controlled reporting also needs explicit snapshot structures for reproducible baselines, forecasts, and period packs.

**Improvement:** Use `construction_project_controls_schema_extension` to add versioned snapshot structures for baseline schedule, cost baseline, forecast, and reporting cutoff packages, including snapshot hash and source-record range.

**Acceptance evidence:** Migration tests prove snapshot tables can rebuild published views, API tests retrieve prior snapshots without mutating live state, and release evidence references snapshot identifiers.

### 39. Document instruction intake for site, change, and approval records

**Justification:** Progress reports, change notices, and meeting minutes often arrive as documents first; controls users need governed extraction into draft records.

**Improvement:** Use `agentic_document_instruction_intake` and `construction_project_controls_semantic_document_instruction_understanding` to extract WBS, dates, quantities, impacted milestones, and requested approvals from uploaded documents into draft `site_progress`, `change_event`, `rfi`, or `submittal` actions.

**Acceptance evidence:** Extraction tests show source-span citation, the assistant preview requires confirmation before any mutation, and release evidence includes one document-to-draft walkthrough.

### 40. Multi-tenant contractor and project isolation

**Justification:** `construction_project_controls_multi_tenant_policy_isolation` must prevent one tenant or project team from seeing another contractor’s sensitive controls data.

**Improvement:** Enforce tenant and project isolation across WBS hierarchies, workbench filters, assistant context, event streams, and release evidence exports. Add project-scoped and contractor-scoped access models on top of existing `permissions`.

**Acceptance evidence:** Isolation tests prove no cross-tenant and no unauthorized cross-project reads, workbench queries return only allowed records, and release evidence includes an access-control verification matrix.

### 41. Cryptographic proof for published reporting packs

**Justification:** Controls reporting often becomes dispute evidence, so published packs should be provably identical to what was approved at freeze time.

**Improvement:** Apply `construction_project_controls_cryptographic_audit_proofs` to frozen baseline, forecast, progress, and change bundles, storing signed hashes and publication timestamps linked to the reporting period.

**Acceptance evidence:** Proof-verification tests confirm published bundles have not changed, the workbench exposes verification status for each pack, and `AuditEventSealed` references the proof identifier.

### 42. Release evidence pack automation

**Justification:** The manifest already declares `RELEASE_EVIDENCE.md`; the package should automatically assemble release proof for controls-specific capabilities rather than relying on manual note gathering.

**Improvement:** Generate a controls release pack that includes API contracts, event contracts, baseline and forecast screenshots, control-test results, assistant-skill evidence, and known limitations for the current release.

**Acceptance evidence:** CI or local verification produces an updated release pack without hand edits to unrelated files, reviewers can trace each claimed capability to an artifact, and `RELEASE_EVIDENCE.md` lists dated evidence entries for `construction_project_controls`.

### 43. Permissions by persona, threshold, and action

**Justification:** The listed `permissions` are coarse for a domain where approving a baseline re-set or a major change should require more authority than viewing a dashboard.

**Improvement:** Add action-level authorization for baseline approval, period freeze, forecast override, change approval, progress acceptance, and policy editing, with monetary and schedule-impact thresholds layered over role grants.

**Acceptance evidence:** Authorization tests prove thresholds route to the correct permission path, UI controls hide or disable restricted actions, and assistant commands fail safely with explicit denial reasons.

### 44. Event and API boundaries to adjacent planning or cost systems

**Justification:** Project controls has many neighboring systems; boundary clarity prevents direct table coupling and keeps `construction_project_controls` composable.

**Improvement:** Define supported inbound and outbound contracts for schedule imports, cost actual feeds, and document references using events and APIs rather than shared tables. Document which data is authoritative inside `construction_project_controls` and which remains external.

**Acceptance evidence:** Boundary contract tests prove imported data enters through declared APIs or events only, architecture notes in `SPECIFICATION.md` identify authoritative records, and no code path reads foreign tables directly.

### 45. Forecast confidence and risk exposure scoring

**Justification:** A single forecast number is misleading without a confidence view and explicit tie-back to unresolved risk and issue exposure.

**Improvement:** Extend `construction_project_controls_predictive_risk_scoring` so each forecast carries confidence band, principal drivers, unresolved exposure amount, and exposure by WBS or contractor. Show the relationship between forecast movement and active risks/issues in the dashboard.

**Acceptance evidence:** Scoring tests cover low, medium, and high confidence cases, forecast cards expose confidence and top drivers, and release evidence includes one forecast confidence explanation.

### 46. Ordered handling of compensable versus non-compensable change events

**Justification:** Cost and schedule impacts need cleaner classification so downstream reporting distinguishes owner-driven scope, contractor-driven rework, and neutral coordination effects.

**Improvement:** Add classification and ordered approval logic in `change_event` for compensable, non-compensable, and pending-liability changes, including separate cost, time, and responsibility dimensions. Reflect these classifications in trend, change, and forecast dashboards.

**Acceptance evidence:** Tests validate classification-specific approval routes, dashboards split change exposure by responsibility, and release evidence includes a mixed-liability change log example.

### 47. Closeout and final-account controls

**Justification:** Project controls does not end when physical progress reaches 100 percent; unresolved change, retention, and closeout deliverables still affect final position.

**Improvement:** Add closeout states to `construction_project` and `work_package` for substantial completion, practical completion, punch closure, final account agreement, and archive readiness. Require all critical RFIs, submittals, and change items to be dispositioned before archive.

**Acceptance evidence:** Closeout tests prove blocking conditions work, the detail view shows remaining closeout blockers, and `RELEASE_EVIDENCE.md` includes one final-account readiness checklist.

### 48. Seed data for realistic controls demos and regression cases

**Justification:** `seed_data.py` should support realistic WBS, baseline, progress, risk, and change scenarios so controls features can be demonstrated and regression-tested against coherent data.

**Improvement:** Add seed scenarios for an on-track project, a delayed project, a change-heavy project, and a contractor-overstatement project, each with linked `construction_project`, `work_package`, `site_progress`, `change_event`, `rfi`, `submittal`, and `schedule_risk` records.

**Acceptance evidence:** Seed-data tests prove the scenarios load cleanly, dashboards display distinct scenario signatures, and release evidence references the seeded projects used for screenshots and checks.

### 49. Contract tests for APIs, events, and UI fragments

**Justification:** The package already declares `tests/test_contract.py`; controls-specific behavior should be locked down at the contract level so future changes do not quietly break reporting or audit flows.

**Improvement:** Expand contract coverage to the baseline APIs, compatibility alias for `POST /site-progresss`, emitted and consumed event schemas, `ConstructionProjectControlsWorkbench`, `ConstructionProjectControlsDetail`, and `ConstructionProjectControlsAssistantPanel`.

**Acceptance evidence:** Contract tests pass for routes, events, and UI fragment availability, test output is referenced in `RELEASE_EVIDENCE.md`, and failures identify the broken contract by exact key.

### 50. Go-live scorecard and release-readiness evidence

**Justification:** A controls package should ship with explicit evidence that baseline, progress, forecast, risk, change, dashboards, agent skills, and boundaries are operationally ready.

**Improvement:** Add a go-live scorecard that checks data model readiness, API readiness, event readiness, dashboard completeness, assistant-skill governance, control-test pass rate, and release evidence completeness for `construction_project_controls`.

**Acceptance evidence:** The scorecard publishes a dated readiness result, missing categories block approval in the workbench, and `ConstructionProjectControlsApproved` is emitted only when the release-readiness evidence bundle is complete.
