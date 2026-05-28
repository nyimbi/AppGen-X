# Project Portfolio Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `project_portfolio_management`. Each improvement is specific to portfolio intake, business-case governance, prioritization, stage gates, dependencies, resources, benefits, risks, financial governance, executive decisioning, and continuous portfolio control so the PBC can move toward complete specialist-grade domain coverage.

## Current Domain Evidence Used

- Domain scope: initiative intake, business cases, portfolio scoring, prioritization, stage gates, dependencies, resources, benefits, risks, issues, change requests, financial snapshots, exceptions, policy rules, runtime parameters, governed models, and executive portfolio governance.
- Owned operational surface: `portfolio_item`, `portfolio_program`, `business_case`, `portfolio_score`, `prioritization_run`, `stage_gate`, `gate_decision`, `project_dependency`, `resource_demand`, `resource_assignment`, `benefit_hypothesis`, `benefit_realization`, `portfolio_risk`, `portfolio_issue`, `change_request`, `portfolio_financial_snapshot`, `portfolio_exception_case`, `portfolio_policy_rule`, `portfolio_runtime_parameter`, `portfolio_schema_extension`, `portfolio_control_assertion`, and `portfolio_governed_model`.
- Declared operations: portfolio item intake, business-case creation, scoring, prioritization, gate definition and decisions, dependency mapping, resource demand forecasting, resource assignment, benefit hypotheses, benefit measurement, risk and issue handling, change requests, financial snapshots, portfolio exceptions, rule compilation, and tradeoff simulation.
- Declared integrations: consumed `BudgetApproved`, `EmployeeCreated`, `RiskAssessed`, and `PolicyChanged` events plus emitted `PortfolioItemIntaked`, `BusinessCaseApproved`, `PrioritizationPublished`, `GateDecisionRecorded`, `BenefitRealizationMeasured`, and `PortfolioExceptionOpened`.
- Declared advanced posture: optimization-based prioritization, counterfactual portfolio tradeoffs, dependency graph risk propagation, benefit realization forecasting, continuous governance controls, AI-assisted business-case critique, AppGen-X eventing, owned boundaries, UI workbenches, agent skills, configuration, rules, parameters, release evidence, and runtime smoke checks.

## 50 Better-Than-World-Class Improvements

### 1. Strategic objective traceability graph

**Justification:** Portfolio decisions are only defensible when every initiative connects to strategic objectives, measurable outcomes, executive commitments, and explicit tradeoffs.

**Improvement:** Add a strategic-objective graph that links `portfolio_item`, `portfolio_program`, `business_case`, `benefit_hypothesis`, and `portfolio_score` to objectives, OKRs, regulatory mandates, customer outcomes, and enterprise themes. The workbench should expose orphaned initiatives, overfunded themes, underfunded commitments, and agent-generated explanations of how each portfolio item supports strategy.

### 2. Intake quality and readiness scoring

**Justification:** Poorly formed initiative requests consume governance time and distort prioritization before business cases are complete.

**Improvement:** Add intake readiness scoring for problem clarity, sponsor authority, strategic fit, expected benefit, cost basis, risk statement, dependency awareness, resource ask, compliance impact, and evidence completeness. Intake commands should route low-readiness items to remediation queues with precise missing-evidence tasks.

### 3. Portfolio item taxonomy and archetypes

**Justification:** Mandatory compliance work, innovation bets, platform investments, cost takeout, customer commitments, technical debt, and operational fixes should not be scored as if they were identical.

**Improvement:** Add portfolio item archetypes with required evidence, scoring dimensions, approval paths, financial methods, risk tolerances, and gate templates. UI views should let executives compare like with like and prevent misleading rank-ordering across incompatible initiative classes.

### 4. Business-case assumption ledger

**Justification:** Business cases often fail because assumptions about cost, timing, benefits, adoption, regulation, and constraints are undocumented or never revisited.

**Improvement:** Extend `business_case` with an assumption ledger that records assumption type, owner, confidence, evidence source, expiration date, sensitivity, validation plan, and decision impact. The PBC agent should extract assumptions from documents and require confirmation before they influence scoring.

### 5. Benefit hypothesis design studio

**Justification:** Benefit tracking is weak when hypotheses are vague, lagging, unowned, or disconnected from measurable operational changes.

**Improvement:** Expand `benefit_hypothesis` with outcome metric, baseline, target, realization mechanism, leading indicators, lagging indicators, measurement owner, data source contract, attribution logic, and expected realization curve. The UI should flag benefits that cannot be measured through declared APIs/events/projections.

### 6. Dynamic scoring model governance

**Justification:** Portfolio scores can become political black boxes unless criteria, weights, thresholds, and model changes are governed and explainable.

**Improvement:** Add versioned score models with criteria libraries, weighting methods, normalization rules, mandatory criteria, excluded criteria, threshold policies, and approval history. Every `portfolio_score` should include a transparent score breakdown, model version, and explanation of why the item ranked where it did.

### 7. Multi-objective optimization prioritization

**Justification:** Portfolio prioritization must balance strategic value, cost, risk, capacity, timing, dependencies, compliance, resilience, sustainability, and option value, not just rank by a single score.

**Improvement:** Extend `prioritization_run` with multi-objective optimization, constraint definitions, Pareto frontier output, selected frontier point, rejected alternatives, and executive rationale. The workbench should let leaders explore tradeoffs without committing changes until a prioritization scenario is published.

### 8. Constraint-aware capital allocation

**Justification:** Portfolio approval must respect budget envelopes, funding source restrictions, fiscal periods, capitalization rules, and reserved capacity.

**Improvement:** Add capital allocation constraints to prioritization and financial snapshots using declared budget projections only. The PBC should show funding gaps, stranded budget, fiscal-period mismatches, approval dependencies, and recommended sequencing for value delivery under budget constraints.

### 9. Capacity and skill supply modeling

**Justification:** A portfolio can be financially approved yet impossible to deliver because critical skills, teams, vendors, or decision-makers are unavailable.

**Improvement:** Expand `resource_demand` and `resource_assignment` with skill taxonomy, role criticality, scarcity, ramp time, location, availability windows, confidence, and declared workforce projections. Prioritization should account for bottleneck skills and show capacity heatmaps by period.

### 10. Resource contention conflict detection

**Justification:** Shared teams are routinely overcommitted across initiatives, creating hidden delays, morale risk, and executive escalation.

**Improvement:** Add conflict detection that compares resource demand, assignment, priority, timing, and skill constraints across portfolio items. The UI should expose conflicts, affected milestones, possible swaps, fairness implications, and agent-proposed resolution plans.

### 11. Dependency graph critical path analysis

**Justification:** Portfolio risk is often dominated by cross-project dependencies, predecessor decisions, shared platforms, vendor commitments, and regulatory dates.

**Improvement:** Extend `project_dependency` into a typed dependency graph with dependency kind, strength, lead/lag, required evidence, risk propagation, and critical path contribution. The workbench should show dependency chains, blocked value, and the initiatives that would unblock the most portfolio benefit.

### 12. Dependency health and propagation scoring

**Justification:** A dependency list is insufficient unless the portfolio can quantify how dependency slippage affects cost, schedule, benefit, and risk exposure.

**Improvement:** Add dependency health metrics, probability of delay, downstream impact, mitigation status, and propagation simulations. When a dependency changes, the PBC should update affected portfolio scores, gate readiness, benefit timing, and exception queues through side-effect-free planning output.

### 13. Stage-gate evidence package templates

**Justification:** Gate decisions require different evidence at idea, business case, funding, delivery, launch, benefit realization, and closure stages.

**Improvement:** Add configurable gate templates with required documents, metrics, risk checks, financial evidence, dependency confirmations, resource commitments, benefit evidence, and control assertions. Gate decision UI should show missing evidence, waiver requests, and policy explanations before approval.

### 14. Gate decision dissent and conditional approval

**Justification:** Real governance bodies rarely produce simple approve/reject decisions; they create conditions, dissent, deferrals, split approvals, and time-bound follow-ups.

**Improvement:** Extend `gate_decision` with conditional approval terms, dissent records, decision participants, quorum, delegated authority, action items, expiry dates, and escalation triggers. Emitted events should distinguish approved, conditionally approved, deferred, rejected, and reopened gate outcomes.

### 15. Portfolio Kanban and lifecycle state machine

**Justification:** Portfolio items need explicit lifecycle states from concept through intake, case, prioritization, approval, delivery, benefits, closure, suspension, cancellation, or archival.

**Improvement:** Add a governed lifecycle state machine with allowed transitions, role permissions, required evidence, emitted events, and exception paths. UI boards should show portfolio flow, aging, bottlenecks, queue health, and WIP limits by governance stage.

### 16. Executive scenario planning

**Justification:** Executives need to test budget cuts, accelerated strategy shifts, resource shortages, regulatory deadlines, merger effects, and market shocks before portfolio changes are made.

**Improvement:** Add side-effect-free executive scenarios with changed constraints, selected items, rejected items, delayed items, benefit timing, risk exposure, capacity use, financial envelopes, and sustainability impact. The agent should narrate tradeoffs and generate board-ready scenario summaries.

### 17. Real-options valuation

**Justification:** Some initiatives create strategic optionality, learning, resilience, or market access that conventional ROI scoring undervalues.

**Improvement:** Add real-options fields and valuation methods for defer, expand, abandon, stage, switch, and learn options. Business cases should record option assumptions, triggers, expiration, uncertainty, and decision checkpoints so innovation and platform bets can be governed properly.

### 18. Portfolio risk aggregation

**Justification:** Individual project risks do not reveal concentration risk, correlated exposure, systemic dependency fragility, or aggregate delivery risk.

**Improvement:** Extend `portfolio_risk` with aggregation dimensions, correlation groups, contagion paths, risk appetite thresholds, residual exposure, and mitigation coverage. The workbench should show portfolio-level heatmaps and risk-adjusted prioritization effects.

### 19. Risk appetite and tolerance enforcement

**Justification:** Portfolio decisions should respect explicit risk appetite, not rely on ad hoc executive judgment at each meeting.

**Improvement:** Add appetite statements, tolerance ranges, breach logic, escalation routes, and exception approvals to `portfolio_policy_rule`. Prioritization and gate decisions should produce evidence when a selection breaches appetite or requires risk acceptance.

### 20. Issue escalation and executive intervention workflow

**Justification:** Portfolio issues need timely escalation when they threaten strategic value, compliance commitments, financial exposure, or critical milestones.

**Improvement:** Expand `portfolio_issue` with escalation level, decision needed, owner, due date, impacted items, recommended intervention, unresolved blocker type, and decision history. Executive dashboards should show only material portfolio issues with clear asks and consequences.

### 21. Change request portfolio impact analysis

**Justification:** Scope, timing, funding, and resource changes can alter the entire portfolio, not just the individual project.

**Improvement:** Extend `change_request` with portfolio-level impact calculations for cost, benefit, score, risk, capacity, dependency, gate schedule, and strategic alignment. Change approval should require a before/after portfolio view and publish events only after approved.

### 22. Benefits realization attribution

**Justification:** Benefits are often claimed without proving which initiative, external factor, or operational change caused the result.

**Improvement:** Expand `benefit_realization` with attribution model, comparison baseline, counterfactual evidence, contributing initiatives, external confounders, confidence, and validation method. The agent should flag over-claimed benefits and suggest evidence needed for credible realization.

### 23. Benefit leakage and erosion detection

**Justification:** Expected value erodes through delays, adoption gaps, cost increases, scope compromises, and operational noncompliance.

**Improvement:** Add benefit leakage categories, early warning indicators, erosion amount, recovery actions, and owner accountability. The portfolio cockpit should show value at risk and recommend whether to intervene, rebaseline, defer, or stop an initiative.

### 24. Post-investment review lifecycle

**Justification:** Portfolio learning requires structured reviews after delivery and benefit realization, not just approval and execution tracking.

**Improvement:** Add post-investment review records for planned versus actual cost, schedule, scope, benefits, risk, assumptions, lessons, and future scoring calibration. Gate closure should require review evidence for material initiatives.

### 25. Strategic balance analytics

**Justification:** Executives need to know whether the portfolio is overconcentrated in run-the-business work, compliance, innovation, growth, resilience, or cost reduction.

**Improvement:** Add balance analytics across strategy, archetype, risk, horizon, value stream, customer segment, geography, regulatory driver, and investment class. UI should show under/overweight areas and simulate rebalancing options.

### 26. Portfolio dependency on external PBC projections

**Justification:** Portfolio governance requires budget, workforce, risk, procurement, delivery, and sustainability context while preserving owned table boundaries.

**Improvement:** Add explicit projection descriptors for financial envelopes, employee capacity, supplier commitments, risk assessments, procurement approvals, and sustainability metrics. Release audits should prove these are accessed only through declared APIs/events/projections and never through foreign table writes.

### 27. Financial snapshot variance analysis

**Justification:** Financial snapshots must explain changes in forecast cost, committed cost, actuals, benefits, capitalization, and contingency over time.

**Improvement:** Expand `portfolio_financial_snapshot` with baseline version, current forecast, variance drivers, funding source, capitalization treatment, contingency use, remaining exposure, and materiality thresholds. Workbench views should provide waterfall explanations for every material variance.

### 28. Funding tranche governance

**Justification:** Large initiatives are often funded in tranches tied to evidence, gates, milestones, or learning outcomes.

**Improvement:** Add tranche definitions, release criteria, consumed amount, remaining authorization, gate dependency, and revocation rules. Gate decisions should be able to release, hold, reduce, or redirect funding without losing audit traceability.

### 29. Portfolio stop, pause, pivot, and restart controls

**Justification:** World-class portfolio management must actively stop low-value work, pause constrained work, pivot assumptions, and restart only when evidence improves.

**Improvement:** Add lifecycle transitions and decision packages for stop, pause, pivot, and restart with sunk-cost disclosure, residual obligations, resource release, benefit loss, dependency impact, and executive authorization. The agent should identify candidates for termination or pivot.

### 30. Initiative health signal fusion

**Justification:** Portfolio health should combine schedule, cost, scope, benefit, risk, dependency, resource, stakeholder, and governance signals rather than rely on manual color statuses.

**Improvement:** Add health scoring that fuses internal portfolio records with declared external projections and event signals. Each health score should include component contributions, data freshness, confidence, and action recommendations.

### 31. Predictive delivery risk scoring

**Justification:** Governance bodies need early warnings before initiatives miss gates, exceed budget, lose sponsors, or fail benefits.

**Improvement:** Add predictive risk models in `portfolio_governed_model` for delivery slippage, cost overrun, benefit erosion, resource contention, and gate failure. Store model evidence, drift checks, fairness considerations, and explainable drivers for each prediction.

### 32. Governance meeting agenda automation

**Justification:** Portfolio boards waste time when agendas do not focus on material decisions, exceptions, tradeoffs, and required approvals.

**Improvement:** Add agenda generation that selects items needing decisions, groups related dependencies, ranks by materiality, surfaces dissent, and drafts decision packets. The agent should produce meeting summaries and convert decisions into typed gate, issue, change, or prioritization commands.

### 33. Decision rights and authority matrix

**Justification:** Portfolio actions must respect who can approve intake, funding, gates, changes, exceptions, waivers, and cancellation.

**Improvement:** Add an authority matrix with role, threshold, domain, delegation, quorum, separation-of-duties, and emergency override rules. Every command should return required authority evidence and reject or escalate unauthorized decisions.

### 34. Portfolio policy studio

**Justification:** Governance rules change by strategy, region, investment type, risk class, funding level, and compliance context.

**Improvement:** Expand `portfolio_policy_rule` into a policy studio with rule templates, impact previews, conflict detection, approval workflow, versioning, and simulation against historical decisions. Policy changes should show affected items before activation.

### 35. Runtime parameter impact simulation

**Justification:** Threshold changes such as minimum score, capacity buffer, gate warning days, and materiality levels can reshape portfolio queues and executive workload.

**Improvement:** Add parameter impact simulation that reports affected portfolio items, changed scores, new gate warnings, resource conflicts, benefit-materiality changes, and exception volume. The agent should explain blast radius before requesting parameter-change approval.

### 36. Control assertion evidence automation

**Justification:** Portfolio governance must prove controls over approvals, scoring, funding, risk acceptance, benefit tracking, and exceptions continuously.

**Improvement:** Expand `portfolio_control_assertion` with control objective, test method, sample population, failure evidence, remediation, owner, and next test date. Release audits and UI should show control effectiveness by portfolio process.

### 37. Portfolio audit reconstruction

**Justification:** Auditors and executives need to reconstruct why a portfolio looked a certain way at a past decision date.

**Improvement:** Add time-travel reconstruction that rebuilds portfolio items, scores, scenarios, gates, dependencies, financial snapshots, risks, and decisions as of a transaction time and valid time. Exportable evidence packets should include hashes and decision lineage.

### 38. Cryptographic decision proof packets

**Justification:** High-stakes funding and cancellation decisions require tamper-evident proof of inputs, authorities, votes, evidence, and emitted events.

**Improvement:** Add sealed decision proof packets for prioritization runs, gate decisions, business-case approvals, change requests, and funding tranches. Verification APIs should prove integrity without exposing sensitive portfolio details.

### 39. Portfolio document and presentation ingestion

**Justification:** Initiative proposals, business cases, status decks, spreadsheets, and board packs contain key portfolio facts that should become governed records.

**Improvement:** Add semantic document ingestion that extracts initiatives, assumptions, benefits, costs, risks, dependencies, decisions, and action items into proposed commands. The agent must show source citations, confidence, validation errors, and reversible CRUD previews.

### 40. Agent-assisted business case critique

**Justification:** The spec declares AI-assisted critique, but the PBC should provide deep, structured feedback on evidence quality, assumptions, benefit logic, risk, and feasibility.

**Improvement:** Add agent skills that critique business cases against archetype-specific rubrics, identify missing evidence, challenge weak assumptions, compare to historical outcomes, and propose improvements. Critiques should be saved as owned evidence, not as ungoverned chat text.

### 41. Portfolio exception case management

**Justification:** Exceptions such as policy waivers, emergency approvals, missing evidence, risk breaches, and dependency failures need structured lifecycle handling.

**Improvement:** Expand `portfolio_exception_case` with exception type, affected item, policy breached, authority required, temporary controls, expiry date, remediation owner, recurrence marker, and closure proof. UI queues should prioritize exceptions by materiality and aging.

### 42. Initiative intake marketplace

**Justification:** Organizations often receive more ideas than they can assess; intake needs transparent comparison, sponsor collaboration, and duplicate prevention.

**Improvement:** Add an intake marketplace where sponsors can submit, enrich, merge, comment on, and track initiative candidates. Duplicate detection should identify overlapping ideas, competing sponsorship, and consolidation opportunities before business-case work begins.

### 43. Portfolio communication and stakeholder map

**Justification:** Portfolio outcomes depend on sponsor support, impacted stakeholders, adoption owners, governance participants, and communication obligations.

**Improvement:** Add stakeholder maps with sponsor, beneficiary, impacted group, decision-maker, approver, change champion, and communications owner. Gate and change workflows should require communications readiness for material initiatives.

### 44. Regulatory and compliance commitment tracking

**Justification:** Compliance initiatives often have external deadlines, mandated controls, evidence requirements, and penalty exposure that require special governance.

**Improvement:** Add compliance commitment records with obligation source, deadline, regulator/customer, penalty exposure, evidence package, dependency, and waiver status. Prioritization should protect mandatory commitments and quantify risk of deferral.

### 45. Sustainability and carbon portfolio lens

**Justification:** Portfolio investment choices can materially affect emissions, resilience, and sustainability commitments.

**Improvement:** Add sustainability impact scoring for carbon, waste, energy, social impact, and resilience using declared projections. Executive scenarios should show how selected portfolios shift sustainability commitments alongside cost, benefit, and risk.

### 46. Portfolio anomaly detection

**Justification:** Unusual scoring changes, repeated gate waivers, benefit overclaims, resource gaming, budget fragmentation, or approval clustering can signal governance failure.

**Improvement:** Add anomaly detection for portfolio operations with typology, severity, explanation, false-positive handling, and remediation workflows. Detected anomalies should open `portfolio_exception_case` records when material.

### 47. Continuous portfolio close and reforecast cycle

**Justification:** Portfolio governance should maintain always-current forecasts rather than wait for monthly manual reporting cycles.

**Improvement:** Add continuous close routines that refresh financial snapshots, benefits, capacity, risks, dependencies, and decision queues from declared events and projections. The workbench should show freshness, stale inputs, blocked refreshes, and publication readiness.

### 48. Executive narrative generation with evidence citations

**Justification:** Leaders need concise explanations of portfolio health, changes, decisions, and risks that can be traced to governed evidence.

**Improvement:** Add narrative generation that cites portfolio items, scores, dependencies, benefits, financial snapshots, risks, issues, and decisions. Narratives should clearly distinguish facts, forecasts, assumptions, recommendations, and unresolved evidence gaps.

### 49. Complete role-based portfolio workbench

**Justification:** Sponsors, portfolio managers, finance, resource managers, risk teams, executives, and auditors require different workflows over the same controlled data.

**Improvement:** Expand UI fragments into role-specific workbenches: sponsor intake, portfolio manager command center, executive decision room, finance portfolio view, resource capacity view, benefits realization board, risk and exception console, and auditor evidence room. Each view should expose all relevant commands, metrics, and agent actions.

### 50. End-to-end portfolio release evidence matrix

**Justification:** A world-class PBC must prove every portfolio capability has owned schema, services, APIs, events, handlers, UI, agent skills, rules, parameters, tests, and boundary evidence.

**Improvement:** Add a release evidence matrix mapping every Project Portfolio Management capability to its tables, commands, route descriptors, AppGen-X event contracts, idempotent handlers, workbench panels, agent skills, permissions, smoke tests, and cross-PBC boundary checks. Release audits should fail whenever a claimed capability lacks executable proof.
