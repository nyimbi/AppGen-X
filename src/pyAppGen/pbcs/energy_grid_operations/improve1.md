# Energy Grid Operations Improvement Backlog

## Current Domain Evidence Used

- Stable PBC key: `energy_grid_operations`.
- Domain purpose: grid assets, topology, switching, dispatch, outages, load forecasts, DER, reliability constraints, and control-room operations.
- Owned domain tables include `grid_asset`, `grid_topology`, `switching_order`, `dispatch_instruction`, `outage_event`, `load_forecast`, `reliability_constraint`, and governed policy, parameter, control, and model records.
- Public APIs include `POST /grid-assets`, `POST /switching-orders`, `POST /dispatch-instructions`, `POST /outage-events`, and `GET /energy-grid-operations-workbench`.
- UI fragments include `EnergyGridOperationsWorkbench`, `EnergyGridOperationsDetail`, and `EnergyGridOperationsAssistantPanel`.

### 1. Feeder and substation asset hierarchy hardening
   **Key:** `grid_asset`
   **Justification:** Operators need feeder, bay, breaker, recloser, transformer, regulator, capacitor bank, and DER intertie relationships to be explicit or switching plans and outage boundaries become guesswork.
   **Improvement:** Extend the asset model so every record carries voltage class, parent asset, normal state, phasing, protection zone, feeder assignment, substation assignment, GIS reference, and SCADA point references. Make feeder-to-device lineage visible before any switching or restoration action is approved.
   **Acceptance evidence:** Migration and model tests cover parent-child integrity, voltage-class validation, and feeder lineage queries; the workbench shows a feeder tree with substation, breaker, and downstream device rollups; sample asset imports prove DER interties and mobile substations fit the same structure.
   **Current Domain Evidence Used:** `grid_asset`; `POST /grid-assets`; `grid_asset_management`; `EnergyGridOperationsWorkbench`.

### 2. Field-level asset quality gates for controllable devices
   **Key:** `grid_asset_management`
   **Justification:** A breaker without interrupting rating, a recloser without operating mode, or a switch without normal position is operationally unsafe data.
   **Improvement:** Add device-specific validation profiles for breakers, switches, reclosers, sectionalizers, transformers, regulators, capacitor banks, and DER interties so the package rejects incomplete or contradictory equipment records before they influence topology or dispatch decisions.
   **Acceptance evidence:** Validation tests reject missing ratings, impossible phase combinations, and duplicate SCADA tags; UI error states explain which field blocks energization-related workflows; release evidence includes a passing device-quality report for seed data.
   **Current Domain Evidence Used:** `grid_asset_management`; `grid_asset`; `seed_data.py`; `EnergyGridOperationsDetail`.

### 3. Electrically accurate feeder graph modeling
   **Key:** `grid_topology`
   **Justification:** Restoration logic, switching safety, and contingency analysis depend on an explicit graph of energized paths, normally open ties, and islandable segments.
   **Improvement:** Represent feeder sections, normally open points, substation bus ties, backfeed paths, and DER-supported islands in the topology model, with directional connectivity and phase-aware pathfinding for both normal and contingency states.
   **Acceptance evidence:** Pathfinding tests prove operators can trace source-to-load paths, identify backfeed candidates, and detect phase mismatches; projection checks show stale topology versions; workbench overlays distinguish current and proposed energized states.
   **Current Domain Evidence Used:** `grid_topology`; `reliability_constraint`; `GET /energy-grid-operations-workbench`; `EnergyGridOperationsWorkbench`.

### 4. Asset intake that respects utility source systems
   **Key:** `POST /grid-assets`
   **Justification:** Utilities rarely create assets by hand only once; they reconcile GIS, SCADA, commissioning records, and field corrections over time.
   **Improvement:** Expand the asset intake boundary to support idempotent upsert by utility asset identifier, commissioning evidence, GIS geometry reference, SCADA tag mapping, and as-left field correction notes without allowing direct writes around package validation.
   **Acceptance evidence:** Contract tests cover create, correction, and duplicate-replay cases; request examples show GIS and SCADA references carried through to read models; release evidence includes a rejected import case for conflicting feeder assignments.
   **Current Domain Evidence Used:** `POST /grid-assets`; `grid_asset`; `idempotent_handlers`; `tests/test_contract.py`.

### 5. Switching order step sequencing with hold points
   **Key:** `switching_order`
   **Justification:** Safe switching requires an ordered sequence of open, close, test, ground, tag, and verify steps with explicit stop conditions.
   **Improvement:** Model switching orders as structured step lists with preconditions, hold points, expected telemetry confirmation, clearance references, and reversal instructions so the system can catch an unsafe step before the dispatcher issues it.
   **Acceptance evidence:** Workflow tests fail orders with impossible step order, missing isolation verification, or missing tag-out evidence; the detail view shows hold points and required confirmations; release evidence includes a passing planned-maintenance switching scenario.
   **Current Domain Evidence Used:** `switching_order`; `energy_grid_operations_workflow`; `EnergyGridOperationsDetail`; `energy_grid_operations_create_grid_asset_workflow`.

### 6. Pre-execution switching simulation at the API boundary
   **Key:** `POST /switching-orders`
   **Justification:** Dispatchers need to know whether a proposed sequence creates backfeed, overload, or trapped generation before the first step is executed.
   **Improvement:** Let the switching-order API accept validation-only and simulation requests that compare current topology against proposed step outcomes, highlight overloaded restoration paths, and flag feeders that lose source or violate clearance rules.
   **Acceptance evidence:** API contract tests prove simulation requests do not mutate state; returned payloads show impacted feeders, violated constraints, and required approvals; release evidence includes a blocked switching case caused by an unintended backfeed path.
   **Current Domain Evidence Used:** `POST /switching-orders`; `switching_order`; `grid_topology`; `reliability_constraint`.

### 7. Dispatch instructions that reflect actual grid objectives
   **Key:** `dispatch_instruction`
   **Justification:** Real dispatch work spans feeder load relief, capacitor switching, regulator changes, DER curtailment, emergency transfers, and restoration support, not a single generic command shape.
   **Improvement:** Enrich dispatch instructions with objective type, control target, target interval, expected load movement, voltage-support intent, DER participation, operator reason code, and rollback conditions so instructions are traceable to grid outcomes.
   **Acceptance evidence:** Model and API tests cover load-relief, voltage-support, DER-curtailment, and restoration-support instructions; the workbench shows active instructions by feeder and substation; acceptance fixtures prove rollback conditions are required for reversible controls.
   **Current Domain Evidence Used:** `dispatch_instruction`; `POST /dispatch-instructions`; `EnergyGridOperationsWorkbench`; `energy_grid_operations_workflow`.

### 8. Constraint-aware dispatch request handling
   **Key:** `POST /dispatch-instructions`
   **Justification:** A dispatch API that ignores thermal, voltage, crew-safety, or switching-window constraints will produce instructions operators cannot safely execute.
   **Improvement:** Gate dispatch requests on current constraint projections, telemetry freshness, active outages, and overlapping switching orders, and return explicit conflict objects when an instruction would overstep a feeder, substation transformer, or restoration boundary.
   **Acceptance evidence:** Contract tests reject instructions during stale telemetry, active lockout, or transformer-overload conditions; API responses include conflict codes and the violated constraint identifiers; release evidence includes a successful dispatch after the conflicting switching order closes.
   **Current Domain Evidence Used:** `POST /dispatch-instructions`; `dispatch_instruction`; `reliability_constraint`; `GET /energy-grid-operations-workbench`.

### 9. Outage lifecycle depth for planned and unplanned events
   **Key:** `outage_event`
   **Justification:** Grid control rooms need more than open and closed outage states; they work through trip, patrol, isolate, repair, partial restore, full restore, and post-event review.
   **Improvement:** Introduce explicit outage states for protective operation, confirmed outage, patrol assigned, isolated, repair in progress, partial restoration, full restoration, and closed review, with cause coding and restoration clock behavior tied to each phase.
   **Acceptance evidence:** State-transition tests cover planned and forced outages; the detail view shows restoration milestones and elapsed time; release evidence includes one partial-restoration example and one misoperation correction example.
   **Current Domain Evidence Used:** `outage_event`; `POST /outage-events`; `EnergyGridOperationsDetail`; `energy_grid_operations_workflow`.

### 10. Outage intake that preserves feeder-section impact
    **Key:** `POST /outage-events`
    **Justification:** Incoming outage reports often start as alarm bursts or OMS clusters, and operators need the affected feeder sections, upstream device, and restoration estimate captured immediately.
    **Improvement:** Extend the outage-event intake boundary so requests can carry initiating device, impacted feeder sections, estimated customers or load at risk, crew ETA, restoration hypothesis, and correlation identifiers for bursty alarm ingestion.
    **Acceptance evidence:** Contract tests accept batched alarm correlations without duplicating outage records; responses show initiating-device lineage and restoration placeholders; release evidence includes a storm-mode burst ingestion scenario with correct deduplication.
    **Current Domain Evidence Used:** `POST /outage-events`; `outage_event`; `idempotent_handlers`; `retry_dead_letter_evidence`.

### 11. Forecast modeling at feeder, substation, and DER granularity
    **Key:** `load_forecast`
    **Justification:** Operators plan switching and dispatch at the feeder and substation level, while DER-heavy circuits need visibility into net load and reverse-flow risk.
    **Improvement:** Store interval forecasts by substation, feeder, and optional downstream segment with separate native load, DER contribution, weather sensitivity, confidence bands, and contingency-adjusted forecast variants.
    **Acceptance evidence:** Schema and analytics tests cover substation rollup, feeder decomposition, and DER-adjusted net-load calculation; the workbench shows forecast confidence bands beside actual telemetry; release evidence includes a feeder with midday reverse-flow risk.
    **Current Domain Evidence Used:** `load_forecast`; `energy_grid_operations_analytics`; `EnergyGridOperationsWorkbench`; `energy_grid_operations_risk_score`.

### 12. Forecast API contracts with source and confidence lineage
    **Key:** `POST /load-forecasts`
    **Justification:** Control-room trust depends on knowing whether a forecast came from a planning run, operator override, weather-driven model, or DER curtailment assumption.
    **Improvement:** Require the load-forecast API to capture source system, forecast horizon, interval size, confidence band, weather station or model reference, DER availability assumptions, and override reason when a human changes the baseline.
    **Acceptance evidence:** Contract tests reject forecasts without source lineage or confidence metadata; accepted payloads surface provenance in the detail UI; release evidence includes one planner forecast and one operator override with clear provenance.
    **Current Domain Evidence Used:** `POST /load-forecasts`; `load_forecast`; `EnergyGridOperationsDetail`; `tests/test_contract.py`.

### 13. Reliability constraints that model grid operating reality
    **Key:** `reliability_constraint`
    **Justification:** Operators make decisions against thermal limits, voltage envelopes, breaker duty cycles, crew access restrictions, and switching windows, not a single generic threshold.
    **Improvement:** Define constraint types for feeder loading, transformer reserve, voltage regulation, protection coordination, crew safety lockout, switching window, DER export, and restoration sequence dependency, each with scope, severity, and expiry logic.
    **Acceptance evidence:** Constraint tests prove overlapping limits resolve deterministically; UI panels show which feeder or substation each active constraint governs; release evidence includes a blocked backfeed due to transformer reserve margin.
    **Current Domain Evidence Used:** `reliability_constraint`; `rule_engine`; `parameter_engine`; `EnergyGridOperationsWorkbench`.

### 14. Restoration path projections from the network graph
    **Key:** `grid_topology`
    **Justification:** During outage restoration, dispatchers need ranked candidate paths, expected switching count, and constraint impact instead of manually tracing the single-line.
    **Improvement:** Produce restoration projections that rank backfeed and resupply paths by switching complexity, expected load pickup, constrained devices, DER support, and required field verification steps.
    **Acceptance evidence:** Projection tests show multiple restoration candidates for a feeder lockout; the workbench compares candidate paths side by side; release evidence includes one accepted path and one rejected path due to voltage-drop risk.
    **Current Domain Evidence Used:** `grid_topology`; `outage_event`; `reliability_constraint`; `GET /energy-grid-operations-workbench`.

### 15. Control-room workbench aligned to grid operations
    **Key:** `EnergyGridOperationsWorkbench`
    **Justification:** Grid operators need one screen that combines switching queues, outage state, forecast stress, active constraints, and telemetry staleness by feeder and substation.
    **Improvement:** Redesign the primary workbench around feeder and substation cards, active switching sequences, outage restoration clocks, constraint banners, forecast-vs-actual load deltas, and stale-projection warnings.
    **Acceptance evidence:** UI contracts cover normal, storm, and maintenance modes; integration tests show operator filters by territory, substation, feeder, and event severity; release evidence includes screenshots with active switching and outage queues visible together.
    **Current Domain Evidence Used:** `EnergyGridOperationsWorkbench`; `GET /energy-grid-operations-workbench`; `energy_grid_operations_workbench_metric`; `energy_grid_operations_analytics`.

### 16. Detail screens that read like an operator’s one-line and event log
    **Key:** `EnergyGridOperationsDetail`
    **Justification:** Operators investigating an event need the asset context, timeline, switching intent, outage progression, and approvals on one page.
    **Improvement:** Turn the detail view into a domain-specific drilldown that shows feeder map context, substation source, open points, active constraints, event timeline, switching steps, dispatch actions, and restoration decisions with clear chronology.
    **Acceptance evidence:** UI tests cover asset, switching-order, outage-event, and constraint-specific detail states; timeline panels show causality without raw table inspection; release evidence includes one outage drilldown and one switching-order drilldown.
    **Current Domain Evidence Used:** `EnergyGridOperationsDetail`; `grid_asset`; `switching_order`; `outage_event`.

### 17. Assistant panel skills that respect operator authority
    **Key:** `EnergyGridOperationsAssistantPanel`
    **Justification:** A useful grid-operations assistant should summarize switching risk, draft restoration notes, and extract permit data, but it must not silently issue control actions.
    **Improvement:** Add named assistant skills for switching-check review, restoration summary drafting, SCADA-alarm clustering explanation, permit extraction, and release-evidence preparation, all behind preview-first interactions and human approval gates.
    **Acceptance evidence:** Skill manifests list allowed actions and blocked actions; UI tests prove the panel shows cited source records and required approvers; release evidence includes one approved summary draft and one blocked mutation attempt.
    **Current Domain Evidence Used:** `EnergyGridOperationsAssistantPanel`; `ai_agent_task_assistance`; `agentic_document_instruction_intake`; `energy_grid_operations_governed_ai_agent_execution`.

### 18. Query boundary that exposes freshness and scope
    **Key:** `GET /energy-grid-operations-workbench`
    **Justification:** A workbench query is unsafe if operators cannot see whether the data is stale, partial, or scoped to the wrong feeder set.
    **Improvement:** Return projection timestamps, consumed-event lag, territory scope, feeder filters, substation filters, and active-mode context with every workbench response so the UI can warn when the view is stale or incomplete.
    **Acceptance evidence:** Contract tests verify freshness metadata and filter echoes; UI tests show stale-view banners and scope chips; release evidence includes a simulated lagged projection with visible warning state.
    **Current Domain Evidence Used:** `GET /energy-grid-operations-workbench`; `EnergyGridOperationsWorkbench`; `appgen_x_outbox_inbox_eventing`; `OperationalKpiChanged`.

### 19. Risk scoring tuned to grid conditions rather than generic workflow age
    **Key:** `energy_grid_operations_risk_score`
    **Justification:** A meaningful grid risk score needs to surface feeder overload exposure, weather stress, switching complexity, outage spread, and DER unpredictability.
    **Improvement:** Rebuild the risk score around feeder loading margin, asset criticality, restoration complexity, forecast uncertainty, weather severity, protection-device anomaly signals, and crew safety exposure so it predicts operational risk instead of only process lateness.
    **Acceptance evidence:** Analytics tests show score drivers for overload, storm, and switching-heavy scenarios; the workbench explains top contributing factors; release evidence includes calibration output for low, medium, and high operational risk cases.
    **Current Domain Evidence Used:** `energy_grid_operations_risk_score`; `load_forecast`; `reliability_constraint`; `energy_grid_operations_autonomous_anomaly_detection`.

### 20. Reliability and restoration metrics that control rooms actually use
    **Key:** `energy_grid_operations_workbench_metric`
    **Justification:** Operators and reliability engineers need SAIDI, SAIFI, CAIDI, MAIFI, restoration age, switching backlog age, and feeder stress counts in the same metric surface.
    **Improvement:** Expand workbench metrics to include reliability indices, active outage duration buckets, restoration pace, switching-order completion rate, forecast miss by feeder, and stale-telemetry counts with drill-through into the underlying events.
    **Acceptance evidence:** Metric definition tests validate formula inputs and aggregation windows; dashboard snapshots show utility-level and feeder-level views; release evidence includes a reconciled metric pack against fixture outage and switching histories.
    **Current Domain Evidence Used:** `energy_grid_operations_workbench_metric`; `outage_event`; `switching_order`; `energy_grid_operations_analytics`.

### 21. Creation events with grid-operational context
    **Key:** `EnergyGridOperationsCreated`
    **Justification:** Downstream consumers cannot act safely if a creation event omits whether it represents an asset, switching order, outage, dispatch instruction, or constraint with feeder context.
    **Improvement:** Publish creation events with aggregate type, aggregate identifier, feeder or substation scope, actor class, initial lifecycle state, source command, and topology-impact flag so projections and downstream workbenches do not reverse-engineer intent.
    **Acceptance evidence:** Event schema tests show typed creation payloads for assets, switching orders, outages, and constraints; example events document feeder scope and topology impact; release evidence includes emitted-event snapshots from a representative control-room scenario.
    **Current Domain Evidence Used:** `EnergyGridOperationsCreated`; `grid_asset`; `switching_order`; `outage_event`.

### 22. Update events that show what changed and why it matters
    **Key:** `EnergyGridOperationsUpdated`
    **Justification:** Dispatchers and auditors need to see whether an update changed a restoration ETA, switching step, feeder assignment, or constraint severity without diffing entire records.
    **Improvement:** Emit structured update events that classify changes as topology, timing, safety, forecast, outage, or approval changes and include revision number, changed fields, and whether operators must re-review the affected record.
    **Acceptance evidence:** Event contract tests verify field-delta groups and revision numbers; consumer projections display re-review badges when safety or topology changes occur; release evidence includes one benign metadata update and one safety-impacting update.
    **Current Domain Evidence Used:** `EnergyGridOperationsUpdated`; `switching_order`; `dispatch_instruction`; `outage_event`.

### 23. Approval events that prove dispatcher authority and policy basis
    **Key:** `EnergyGridOperationsApproved`
    **Justification:** A switching or restoration approval means little without the approver role, the policy version, and the boundary conditions that were accepted.
    **Improvement:** Include approver identity class, approval reason, governing policy version, active constraint snapshot, and required follow-up actions in approval events so approvals can be replayed during post-event review.
    **Acceptance evidence:** Event tests cover switching, outage-restoration, and dispatch approvals; workbench detail panels show policy basis and approver chain; release evidence includes one approval replay that reconstructs the exact accepted conditions.
    **Current Domain Evidence Used:** `EnergyGridOperationsApproved`; `permissions`; `PolicyChanged`; `continuous_release_assurance`.

### 24. Exception events that map to operator remediation paths
    **Key:** `EnergyGridOperationsExceptionOpened`
    **Justification:** “Exception opened” is only useful if operators know whether they are facing stale telemetry, blocked clearance, overload risk, forecast drift, or failed restoration.
    **Improvement:** Classify exception events by outage, switching, dispatch, constraint, telemetry, and release-governance causes, with severity, owner role, affected feeder scope, and expected remediation workflow.
    **Acceptance evidence:** Event and UI tests show exception buckets and owner assignment; workbench queues sort by severity and restoration impact; release evidence includes one safety-blocking exception and one data-quality exception with different handling paths.
    **Current Domain Evidence Used:** `EnergyGridOperationsExceptionOpened`; `retry_dead_letter_evidence`; `EnergyGridOperationsWorkbench`; `energy_grid_operations_risk_score`.

### 25. Policy change handling tied to live operating rules
    **Key:** `PolicyChanged`
    **Justification:** When switching or safety policy changes, the package must recalculate who can approve which actions and which active orders need review.
    **Improvement:** Consume policy-change events to recompute dispatcher authority, clearance requirements, restoration hold points, DER export limits, and storm-mode overrides, then open exceptions on any active record whose accepted policy is now outdated.
    **Acceptance evidence:** Handler tests show policy updates reopening affected switching orders and dispatch instructions; projection freshness checks prove recalculation reaches the workbench; release evidence includes one policy change that invalidates a pending switching approval.
    **Current Domain Evidence Used:** `PolicyChanged`; `switching_order`; `dispatch_instruction`; `permissions`.

### 26. Audit sealing tied to control-room evidence
    **Key:** `AuditEventSealed`
    **Justification:** Operators need immutable proof that clearances, approvals, and restoration declarations were recorded and sealed after the fact.
    **Improvement:** Link sealed audit events back to switching steps, outage milestones, dispatch approvals, and release bundles so every high-risk action has a visible integrity marker and retrieval path from the operator UI.
    **Acceptance evidence:** Consumed-event tests attach sealed references to relevant records; the detail view shows seal status and audit evidence links; release evidence includes one sealed restoration declaration and one sealed switching approval.
    **Current Domain Evidence Used:** `AuditEventSealed`; `EnergyGridOperationsDetail`; `energy_grid_operations_cryptographic_audit_proofs`; `RELEASE_EVIDENCE.md`.

### 27. KPI change handling that updates reliability posture in place
    **Key:** `OperationalKpiChanged`
    **Justification:** Reliability thresholds change throughout storm response and seasonal operations, and the workbench should react without manual recalculation.
    **Improvement:** Consume KPI-change events to refresh reliability targets, restoration urgency bands, feeder stress flags, and escalation thresholds so operator dashboards reflect the latest operating posture as soon as KPI policy changes arrive.
    **Acceptance evidence:** Event-handler tests show updated metric thresholds on the workbench; stale-view warnings clear after projection catch-up; release evidence includes one KPI shift that reorders feeder restoration priority.
    **Current Domain Evidence Used:** `OperationalKpiChanged`; `energy_grid_operations_workbench_metric`; `EnergyGridOperationsWorkbench`; `energy_grid_operations_analytics`.

### 28. Event-sourced timeline that merges operations into one history
    **Key:** `energy_grid_operations_event_sourced_operational_history`
    **Justification:** Post-event analysis depends on replaying alarms, switching steps, approvals, dispatch changes, and restoration milestones in the order operators experienced them.
    **Improvement:** Build an event-sourced history stream that records control-room commands, SCADA-linked confirmations, outage transitions, and projection checkpoints with correlation IDs so the package can reconstruct the exact operational narrative.
    **Acceptance evidence:** Replay tests produce the same workbench state after full history rebuild; timeline views distinguish commands from confirmations; release evidence includes one replayable storm-restoration sequence from trip to final restoration.
    **Current Domain Evidence Used:** `energy_grid_operations_event_sourced_operational_history`; `switching_order`; `outage_event`; `appgen_x_outbox_inbox_eventing`.

### 29. Tenant isolation that matches utility operating boundaries
    **Key:** `energy_grid_operations_multi_tenant_policy_isolation`
    **Justification:** A shared platform for multiple utilities or regions must never leak feeder names, outage state, or switching authority across tenant boundaries.
    **Improvement:** Enforce tenant isolation on asset queries, workbench filters, event streams, assistant summaries, and release artifacts so each utility or operating region sees only its own feeders, substations, and policy context.
    **Acceptance evidence:** Isolation tests prove searches, projections, events, and assistant responses are tenant-scoped; negative fixtures verify no cross-tenant feeder lookup succeeds; release evidence includes a passing multi-tenant boundary report.
    **Current Domain Evidence Used:** `energy_grid_operations_multi_tenant_policy_isolation`; `permissions`; `EnergyGridOperationsWorkbench`; `RELEASE_EVIDENCE.md`.

### 30. Schema evolution that can absorb new field equipment classes
    **Key:** `energy_grid_operations_schema_evolution_resilience`
    **Justification:** Grid operations data evolves as utilities add mobile substations, battery systems, dynamic line rating sensors, and new DER control points.
    **Improvement:** Add schema-evolution rules that allow new device classes and telemetry attributes without breaking existing topology, switching, outage, and analytics projections, with explicit compatibility checks before activation.
    **Acceptance evidence:** Migration dry runs show backward-compatible rollout of a new device class; read-model tests prove existing workbench panels stay intact; release evidence includes one staged schema extension for battery inverter metadata.
    **Current Domain Evidence Used:** `energy_grid_operations_schema_evolution_resilience`; `grid_asset`; `owned_schema_migrations_models`; `SPECIFICATION.md`.

### 31. Anomaly detection aimed at electrical and operational failure modes
    **Key:** `energy_grid_operations_autonomous_anomaly_detection`
    **Justification:** Grid operators care about breaker chatter, impossible restoration jumps, oscillating dispatch targets, forecast collapse, and telemetry silence more than generic anomaly scores.
    **Improvement:** Train anomaly detection around control-room patterns such as repeated open-close cycles, outage fan-out inconsistent with topology, restoration ETA regressions, sudden forecast divergence, and dispatch instructions that fight active constraints.
    **Acceptance evidence:** Detection tests cover breaker chatter, stale telemetry, and restoration-sequence anomalies; workbench cards explain why each anomaly fired; release evidence includes reviewer outcomes for true-positive and false-positive examples.
    **Current Domain Evidence Used:** `energy_grid_operations_autonomous_anomaly_detection`; `switching_order`; `outage_event`; `load_forecast`.

### 32. Document understanding for switching sheets and crew packets
    **Key:** `energy_grid_operations_semantic_document_instruction_understanding`
    **Justification:** Switching instructions, outage packets, and tailboards often arrive as documents before they become governed structured records.
    **Improvement:** Teach the package to parse switching sheets, restoration runbooks, clearance forms, and crew tailboards into draft switching orders, outage updates, and safety evidence with source-span citations and confidence markers.
    **Acceptance evidence:** Extraction tests show step lists, feeder identifiers, hold points, and safety notes captured correctly; assistant previews cite source spans before draft creation; release evidence includes one parsed switching sheet and one parsed restoration memo.
    **Current Domain Evidence Used:** `energy_grid_operations_semantic_document_instruction_understanding`; `agentic_document_instruction_intake`; `switching_order`; `EnergyGridOperationsAssistantPanel`.

### 33. Policy defaults that reflect operating modes, not a single static rulebook
    **Key:** `ENERGY_GRID_OPERATIONS_DEFAULT_POLICY`
    **Justification:** Normal operations, storm mode, wildfire de-energization, planned maintenance, and black-start recovery require different default thresholds and approval paths.
    **Improvement:** Define named default-policy profiles for normal, storm, emergency restoration, planned maintenance, and high-risk operating modes, with clear inheritance and explicit workbench visibility when the active policy profile changes.
    **Acceptance evidence:** Configuration tests validate profile inheritance and override order; the workbench shows the active mode banner and policy delta; release evidence includes one storm-mode switch that tightens approval and restoration thresholds.
    **Current Domain Evidence Used:** `ENERGY_GRID_OPERATIONS_DEFAULT_POLICY`; `configuration_schema`; `PolicyChanged`; `EnergyGridOperationsWorkbench`.

### 34. Counterfactual simulation for restoration and switching choices
    **Key:** `energy_grid_operations_counterfactual_scenario_simulation`
    **Justification:** Dispatchers regularly ask what happens if they restore via a tie switch, hold a feeder open longer, or curtail DER before picking up load.
    **Improvement:** Provide simulation workups that compare restoration and switching alternatives against expected load pickup, voltage risk, crew travel, DER participation, and constraint violations without mutating live state.
    **Acceptance evidence:** Scenario tests compare at least two restoration paths and one DER-curtailment branch; UI results show side-by-side outcomes with violated constraints highlighted; release evidence includes a chosen scenario and the rejected alternatives.
    **Current Domain Evidence Used:** `energy_grid_operations_counterfactual_scenario_simulation`; `grid_topology`; `reliability_constraint`; `EnergyGridOperationsWorkbench`.

### 35. Cryptographic proofs for safety-critical actions
    **Key:** `energy_grid_operations_cryptographic_audit_proofs`
    **Justification:** Switching approvals, clearance confirmations, and restoration declarations should be tamper-evident long after the operating shift ends.
    **Improvement:** Seal safety-critical actions with chained hashes over actor, time, record revision, active constraint snapshot, and referenced documents so the package can prove no later edit altered what was accepted in the field.
    **Acceptance evidence:** Proof-verification tests detect modified approval payloads; the detail view surfaces proof status for high-risk actions; release evidence includes one hash-chain verification bundle for a switching-and-restoration sequence.
    **Current Domain Evidence Used:** `energy_grid_operations_cryptographic_audit_proofs`; `AuditEventSealed`; `switching_order`; `RELEASE_EVIDENCE.md`.

### 36. Continuous control tests for switching safety and restoration integrity
    **Key:** `energy_grid_operations_continuous_control_testing`
    **Justification:** Safety and reliability controls lose value if they run only at release time instead of during live operations.
    **Improvement:** Execute continuous controls for missing isolation verification, absent clearance evidence, overlapping switching authority, stale outage states, unresolved high-severity exceptions, and restoration declarations made before confirmation telemetry arrives.
    **Acceptance evidence:** Control assertions fire in runtime fixtures and surface on the workbench; failing controls block approval where appropriate; release evidence includes a control report for switching safety, outage consistency, and projection freshness.
    **Current Domain Evidence Used:** `energy_grid_operations_continuous_control_testing`; `energy_grid_operations_control_assertion`; `switching_order`; `outage_event`.

### 37. Sustainability awareness that never outranks reliability
    **Key:** `energy_grid_operations_carbon_and_sustainability_awareness`
    **Justification:** Operators increasingly need to consider DER dispatch and losses, but reliability and safety must still dominate every decision.
    **Improvement:** Add carbon- and loss-aware advisory calculations to compare dispatch and restoration alternatives, while clearly labeling them as secondary to safety, thermal, voltage, and restoration constraints.
    **Acceptance evidence:** Analytics tests show advisory carbon deltas for DER-curtailment and feeder-transfer options; UI labels make advisory status explicit; release evidence includes one case where a lower-carbon option is rejected because it violates reliability constraints.
    **Current Domain Evidence Used:** `energy_grid_operations_carbon_and_sustainability_awareness`; `dispatch_instruction`; `reliability_constraint`; `energy_grid_operations_analytics`.

### 38. Event federation that keeps external integrations at declared boundaries
    **Key:** `energy_grid_operations_cross_pbc_event_federation`
    **Justification:** Grid operations depend on weather, crews, outage management, and audit systems, but the package must consume them through explicit events and projections rather than hidden table reads.
    **Improvement:** Define declared event contracts and projection adapters for external outage, weather, crew, and audit signals so the package can enrich workbench views and decisions without breaking ownership boundaries.
    **Acceptance evidence:** Contract tests verify no direct foreign-table dependency appears in package code paths; integration fixtures show event ingestion updates projections only through declared boundaries; release evidence includes a dependency map for all federated signals.
    **Current Domain Evidence Used:** `energy_grid_operations_cross_pbc_event_federation`; `consumes`; `appgen_x_outbox_inbox_eventing`; `RELEASE_EVIDENCE.md`.

### 39. Governed AI execution for dispatcher and analyst copilots
    **Key:** `energy_grid_operations_governed_ai_agent_execution`
    **Justification:** Assistant automation is useful only when it stays within safe skills, approved data scope, and visible human review.
    **Improvement:** Limit AI execution to bounded skills such as summarizing outage progression, proposing switching-risk checklists, drafting restoration comms, and preparing release evidence, with explicit permission checks and preview/confirm flows on every state-changing action.
    **Acceptance evidence:** Policy tests prove blocked actions for unauthorized users and hidden mutation paths; assistant transcripts cite the exact records and permissions consulted; release evidence includes a governance report for all enabled grid-operations skills.
    **Current Domain Evidence Used:** `energy_grid_operations_governed_ai_agent_execution`; `ai_agent_task_assistance`; `permissions`; `EnergyGridOperationsAssistantPanel`.

### 40. Configuration schema that matches territory and operating-calendar reality
    **Key:** `configuration_schema`
    **Justification:** Utilities run different switching windows, crew calendars, storm escalation thresholds, and feeder naming conventions by territory.
    **Improvement:** Expand configuration schema coverage for territory calendars, storm modes, switching cutover windows, restoration target bands, telemetry freshness thresholds, DER response timing, and feeder naming patterns, with validation before activation.
    **Acceptance evidence:** Schema tests reject invalid calendars and contradictory thresholds; configuration workbench diff views show territory-specific overrides; release evidence includes one approved config change and one rejected unsafe change.
    **Current Domain Evidence Used:** `configuration_schema`; `configuration_workbench`; `ENERGY_GRID_OPERATIONS_DEFAULT_POLICY`; `ENERGY_GRID_OPERATIONS_RETRY_LIMIT`.

### 41. Rule engine coverage for electrical and safety policy
    **Key:** `rule_engine`
    **Justification:** Switching and restoration approval depends on explicit rules for backfeed prevention, transformer reserve, clearance sequencing, and DER isolation.
    **Improvement:** Encode electrical and safety rules in the rule engine so operators can trace why a backfeed path is blocked, why a switching order needs another approver, or why a DER-enabled restoration path needs extra verification.
    **Acceptance evidence:** Rule tests cover backfeed, reserve-margin, clearance, and DER-islanding cases; workbench detail views show which rule fired and with what inputs; release evidence includes rule-version snapshots for a representative outage restoration run.
    **Current Domain Evidence Used:** `rule_engine`; `switching_order`; `reliability_constraint`; `energy_grid_operations_policy_rule`.

### 42. Parameter tuning for storm response and alarm surges
    **Key:** `parameter_engine`
    **Justification:** Grid operations need live tuning for alarm dedupe windows, forecast horizons, restoration urgency, and anomaly sensitivity during storm or emergency conditions.
    **Improvement:** Use the parameter engine for bounded runtime tuning of outage clustering windows, switching-step timeout alerts, forecast confidence floors, anomaly thresholds, and restoration escalation timers with audit-friendly change history.
    **Acceptance evidence:** Parameter tests show safe bounds and rollback behavior; the workbench exposes active parameter overrides during storm mode; release evidence includes one temporary storm override with subsequent rollback proof.
    **Current Domain Evidence Used:** `parameter_engine`; `energy_grid_operations_runtime_parameter`; `outage_event`; `configuration_workbench`.

### 43. Owned schema depth for steps, milestones, and telemetry references
    **Key:** `owned_schema_migrations_models`
    **Justification:** Grid operations need owned structures for switching steps, restoration milestones, and telemetry references instead of burying those details in opaque blobs.
    **Improvement:** Add owned schema models for switching steps, safety clearances, outage milestones, telemetry confirmation references, and restoration decisions so operational state stays queryable and governable within package boundaries.
    **Acceptance evidence:** Migration tests prove new tables and relationships are package-owned; model tests show step-level and milestone-level queries; release evidence includes schema snapshots tied to a switching-order lifecycle and an outage-restoration lifecycle.
    **Current Domain Evidence Used:** `owned_schema_migrations_models`; `switching_order`; `outage_event`; `migrations/001_initial.sql`.

### 44. Outbox and inbox boundaries that reflect grid-event flow
    **Key:** `appgen_x_outbox_inbox_eventing`
    **Justification:** Switching, outage, KPI, and audit events arrive asynchronously, and operators need clear lineage from domain mutation to emitted or consumed projections.
    **Improvement:** Strengthen inbox and outbox handling with event partitioning by utility and territory, correlation IDs for outage and switching flows, projection checkpoints, and explicit freshness reporting from the event pipeline into the workbench.
    **Acceptance evidence:** Eventing tests show ordered publication and replay for feeder-scoped events; projection lag is visible in the workbench API; release evidence includes emitted and consumed event lineage for a full outage-restoration scenario.
    **Current Domain Evidence Used:** `appgen_x_outbox_inbox_eventing`; `EnergyGridOperationsCreated`; `PolicyChanged`; `GET /energy-grid-operations-workbench`.

### 45. Duplicate-event safety for SCADA, outage, and KPI feeds
    **Key:** `idempotent_handlers`
    **Justification:** SCADA alarm storms and repeated external events should not create duplicate outage records, repeated approvals, or inflated reliability metrics.
    **Improvement:** Make event handlers idempotent across trip alarms, outage updates, KPI refreshes, and audit seals by keying on source event identity, feeder scope, and record revision before any projection or aggregate mutation occurs.
    **Acceptance evidence:** Handler tests prove repeated alarm and KPI events do not duplicate domain state; dead-letter cases isolate truly conflicting replays; release evidence includes duplicate-ingestion fixtures with stable output state.
    **Current Domain Evidence Used:** `idempotent_handlers`; `outage_event`; `OperationalKpiChanged`; `AuditEventSealed`.

### 46. Dead-letter evidence with operator-safe replay decisions
    **Key:** `retry_dead_letter_evidence`
    **Justification:** Failed event processing becomes operational risk when it hides outage updates, stale constraints, or missing approvals.
    **Improvement:** Turn dead-letter handling into an operator-facing evidence flow that records failed source event, affected feeder or substation, processing error, replay safety assessment, and final resolution outcome before any retry occurs.
    **Acceptance evidence:** Workbench dead-letter views group failures by operational impact; replay tests prove safe retries restore missing projections without double effects; release evidence includes one dead-letter closure with operator rationale.
    **Current Domain Evidence Used:** `retry_dead_letter_evidence`; `appgen_x_outbox_inbox_eventing`; `EnergyGridOperationsExceptionOpened`; `EnergyGridOperationsWorkbench`.

### 47. Permission model aligned to real control-room roles
    **Key:** `permissions`
    **Justification:** Dispatcher, switching supervisor, reliability engineer, outage manager, field safety reviewer, and audit observer roles need sharply different powers.
    **Improvement:** Expand permission coverage so each high-risk action states who can create, revise, approve, simulate, or close it, and whether a second approver is required during storm mode, DER-islanding cases, or high-severity restoration work.
    **Acceptance evidence:** Authorization tests cover role-specific create, approve, and simulate actions; UI action states hide or disable unsupported controls; release evidence includes a role matrix with dual-approval requirements for safety-critical paths.
    **Current Domain Evidence Used:** `permissions`; `energy_grid_operations.read`; `energy_grid_operations.approve`; `EnergyGridOperationsAssistantPanel`.

### 48. Document intake focused on switching and restoration packets
    **Key:** `agentic_document_instruction_intake`
    **Justification:** Many field-driven operations begin with a PDF switching program, a restoration packet, or a crew note rather than structured API input.
    **Improvement:** Make document intake a governed front door for switching programs, outage restoration plans, protection memos, and crew safety notes, with extraction into draft records and mandatory citation of the originating document spans.
    **Acceptance evidence:** Intake tests cover PDFs and text documents with feeder identifiers, step lists, and safety notes; assistant previews show extracted fields alongside citations; release evidence includes one approved switching draft created from a document packet.
    **Current Domain Evidence Used:** `agentic_document_instruction_intake`; `energy_grid_operations_semantic_document_instruction_understanding`; `switching_order`; `EnergyGridOperationsAssistantPanel`.

### 49. Release assurance that proves operational readiness, not only syntax
    **Key:** `continuous_release_assurance`
    **Justification:** A release to a control-room package should prove topology logic, safety rules, event projections, and reliability metrics still behave under representative operating cases.
    **Improvement:** Expand release assurance to run feeder-restoration simulations, switching safety controls, outage replay checks, event schema snapshots, metric reconciliations, and assistant governance checks before a version is considered releasable.
    **Acceptance evidence:** Release pipelines emit a domain-specific assurance bundle with passing simulation, replay, control, and metric checks; failing gates point to the exact operational regression; release evidence includes dated bundle references for the candidate version.
    **Current Domain Evidence Used:** `continuous_release_assurance`; `energy_grid_operations_event_sourced_operational_history`; `energy_grid_operations_workbench_metric`; `RELEASE_EVIDENCE.md`.

### 50. Release evidence that reads like a utility operations readiness pack
    **Key:** `RELEASE_EVIDENCE.md`
    **Justification:** Auditors and operations leaders need concise proof that the package is safe for switching, outage handling, forecasting, and restoration under declared constraints.
    **Improvement:** Reshape release evidence into a grid-operations readiness pack with sections for feeder-topology checks, switching simulation results, outage replay summaries, reliability-metric reconciliation, event boundary proofs, assistant governance evidence, and unresolved operational risks.
    **Acceptance evidence:** The release evidence format includes dated links to contract tests, scenario runs, event schemas, projection freshness snapshots, and control results; reviewers can verify why the package is safe to release without reading source code first.
    **Current Domain Evidence Used:** `RELEASE_EVIDENCE.md`; `SPECIFICATION.md`; `tests/test_contract.py`; `continuous_release_assurance`.
