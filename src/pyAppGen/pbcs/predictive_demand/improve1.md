# Predictive Demand PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `predictive_demand`. Each improvement is specific to demand forecasting, demand sensing, consensus planning, shortage prediction, replenishment guidance, and governed forecasting operations so the PBC can move toward complete specialist-grade domain coverage.

## Current Domain Evidence Used

- Domain scope: demand planning, forecast modeling, inventory coverage analysis, shortage detection, consensus planning, governed demand-intelligence workbenches, and AppGen-X event-driven signal projection.
- Owned planning surface: `forecast_model`, `forecast_run`, `demand_signal`, `forecast_result`, `planning_horizon`, `forecast_driver`, `consensus_adjustment`, `scenario_version`, `shortage_risk`, `replenishment_recommendation`, `forecast_exception`, `model_drift_signal`, `planning_rule`, `planning_parameter`, `governed_model_evidence`, and `forecast_audit_proof`.
- Declared operations: model registration, signal ingestion, forecast-run orchestration, result publication, planning horizons, causal drivers, consensus adjustments, scenarios, shortage risks, replenishment recommendations, exceptions, model drift, governed model evidence, audit proofs, workbench views, and owned-table boundary verification.
- Declared integrations: consumed `OrderShipped`, `OperationalKpiChanged`, and `InventoryPoolChanged` events plus shipment, inventory-pool, and operational-KPI projections through AppGen-X contracts only.
- Declared advanced posture: event-sourced demand signals, multi-tenant planning isolation, schema-evolution-safe demand context, probabilistic confidence bands, causal-driver modeling, temporal replenishment forecasting, consensus controls, service-level safety stock, shortage alerts, governed model evidence, cryptographic forecast proofs, retry/dead-letter evidence, permissions, rules, parameters, UI fragments, and release audits.

## 50 Better-Than-World-Class Improvements

### 1. Canonical demand signal identity and deduplication

**Justification:** Predictive demand quality depends on trustworthy signal identity; shipments, inventory movements, operational KPIs, manual overrides, promotion data, and customer demand indicators can otherwise be double-counted, stale, or incorrectly merged.

**Improvement:** Add a canonical signal identity service to `demand_signal` that records source-system identity, business identity, event-time, received-time, sequence number, confidence, replacement policy, deduplication hash, and supersession links. The workbench should expose duplicate clusters, late-arrival decisions, replay impact, and agent-assisted merge recommendations before signals enter forecast runs.

### 2. Demand signal quality scoring

**Justification:** A forecast can only be as reliable as its inputs, yet the current package does not score each demand signal for completeness, freshness, credibility, sparsity, outlier risk, and business relevance.

**Improvement:** Introduce signal-quality dimensions with configurable thresholds per signal type, SKU family, location, and planning horizon. Every ingested signal should carry a quality score, failed checks, remediation tasks, and release evidence proving that low-quality signals are quarantined, down-weighted, or escalated rather than silently influencing forecasts.

### 3. Demand stream lineage graph

**Justification:** Planners need to explain exactly which source events, projections, manual inputs, and transformations contributed to a published forecast result.

**Improvement:** Add a lineage graph that links `forecast_result` back to `forecast_run`, `forecast_model`, `demand_signal`, `forecast_driver`, `consensus_adjustment`, and relevant AppGen-X inbox events. UI fragments should provide trace navigation, evidence export, and natural-language explanations of how each signal affected the final forecast.

### 4. Multi-granularity hierarchy reconciliation

**Justification:** Real demand planning operates simultaneously across SKU, product family, channel, customer segment, region, warehouse, and time hierarchies; forecasts must reconcile without contradictions across levels.

**Improvement:** Add hierarchy definitions, bottom-up/top-down/middle-out reconciliation methods, proportional allocation rules, residual handling, and variance evidence to `planning_horizon` and `forecast_result`. The workbench should show reconciliation waterfalls and flag impossible aggregates where child forecasts exceed parent constraints.

### 5. Horizon-specific model selection

**Justification:** Short-term demand sensing, medium-term replenishment planning, and long-term capacity planning require different algorithms, signal weights, and confidence semantics.

**Improvement:** Extend `forecast_model` and `planning_horizon` so model selection is horizon-aware, with separate model families for intraday, daily, weekly, monthly, seasonal, and strategic horizons. Forecast runs should record why a model was selected, what alternatives were rejected, and whether the horizon demands sensing, statistical forecasting, causal forecasting, or simulation.

### 6. Probabilistic forecast distribution storage

**Justification:** Point forecasts are inadequate for shortage, service-level, and replenishment decisions because planners need distributions, quantiles, skew, and tail exposure.

**Improvement:** Replace simple confidence bands with full probabilistic distributions on `forecast_result`, including P10/P25/P50/P75/P90/P95 values, interval calibration evidence, distribution family, and tail-risk annotations. APIs and UI should allow downstream PBCs to request service-level-specific demand quantities without reading internal tables.

### 7. Confidence calibration backtesting

**Justification:** A confidence interval is only useful if it is empirically calibrated; otherwise planners may trust uncertainty numbers that systematically understate risk.

**Improvement:** Add rolling backtests that compare realized demand to forecast intervals by SKU, location, horizon, model version, and signal set. Store calibration curves, coverage failures, bias by quantile, and remediation recommendations in governed model evidence, and surface failing intervals in the forecast workbench.

### 8. Forecast value added measurement

**Justification:** Demand teams need to know whether model output, planner overrides, consensus adjustments, and external signals improve accuracy or merely add noise.

**Improvement:** Add forecast value added metrics for every planning step: naive baseline, statistical model, causal model, demand sensing adjustment, planner override, consensus version, and published forecast. The PBC should quantify incremental accuracy, bias, latency, and cost so low-value interventions can be removed or redesigned.

### 9. Bias decomposition and root-cause classification

**Justification:** Forecast error often hides structural bias caused by promotions, stockouts, new products, regional effects, calendar shifts, or planner incentives.

**Improvement:** Add bias decomposition by product, location, customer segment, channel, forecast horizon, signal type, planner, and model version. Each persistent bias should open a `forecast_exception` with root-cause hypotheses, required evidence, owner assignment, and prevention controls.

### 10. Stockout-corrected unconstrained demand estimation

**Justification:** Sales or shipment history underestimates true demand when inventory was unavailable, producing forecasts that perpetuate shortages.

**Improvement:** Build stockout correction using declared inventory-pool projections and shortage events to estimate lost sales, censored demand, and unconstrained demand. Forecast runs should separately store observed demand, constrained demand, imputed lost demand, and unconstrained forecast quantities with confidence and evidence.

### 11. Promotion and price elasticity modeling

**Justification:** Promotions, discounts, price changes, bundles, and markdowns can dominate demand patterns and must be modeled as causal drivers rather than treated as unexplained noise.

**Improvement:** Add driver definitions for promotion mechanics, depth, duration, media intensity, price index, competitor response, and halo effects. Forecast drivers should calculate elasticity estimates, lift curves, post-promotion dips, and uncertainty, while preserving boundaries through declared price and promotion projections.

### 12. Cannibalization and halo effect graph

**Justification:** Demand for one item can reduce or increase demand for substitutes, bundles, accessories, and adjacent categories; isolated SKU forecasts misstate total demand.

**Improvement:** Introduce a cannibalization/halo graph with relationship type, strength, direction, horizon, evidence source, and confidence. Scenario versions should simulate portfolio-level demand changes, identify net-new versus transferred demand, and explain expected effects to planners.

### 13. Substitution-aware demand planning

**Justification:** When a product is unavailable, customers may switch to substitutes, defer purchase, or abandon demand, and each behavior changes replenishment decisions.

**Improvement:** Add substitution behavior models that use inventory availability, product relationships, customer segment, channel, and historical substitution evidence. Forecast results should expose expected primary demand, substitute demand, lost demand, and replenishment recommendations for each alternative.

### 14. New product introduction forecasting

**Justification:** New products lack demand history but still require launch forecasts, allocation planning, replenishment policies, and early course correction.

**Improvement:** Add NPI forecast templates with analog item selection, launch curve libraries, attribute similarity, channel launch calendars, sell-in versus sell-through separation, early signal gates, and launch-confidence decay. The UI should support planner review of analogs, assumptions, and post-launch recalibration.

### 15. End-of-life and lifecycle curve forecasting

**Justification:** Mature, declining, seasonal, replacement, and discontinued items need different demand behavior and inventory risk treatment than active-growth products.

**Improvement:** Add lifecycle states, phase-specific curves, successor/predecessor links, runout targets, residual demand estimates, obsolescence exposure, and final-buy recommendations. Forecast results should distinguish demand to satisfy, demand to discourage, and demand that should trigger substitution or clearance actions.

### 16. Intermittent and sparse demand methods

**Justification:** Spare parts, specialty items, project demand, and long-tail SKUs have irregular demand patterns that conventional smoothing methods handle poorly.

**Improvement:** Add intermittent-demand model families, zero-inflation detection, demand-size and demand-interval separation, lumpy-demand classification, and service-part policies. Forecast result distributions should show probability of any demand, expected demand size, and recommended stocking logic.

### 17. Event-driven demand sensing

**Justification:** Short-horizon demand often changes faster than batch planning cycles; the PBC already consumes AppGen-X events but needs a demand-sensing layer that reacts to new signals.

**Improvement:** Add low-latency demand sensing runs triggered by high-confidence signal changes, late orders, inventory pool movements, operational KPI shifts, promotion changes, and anomaly events. Sensing updates should create versioned deltas, planner alerts, and safe downstream publication controls.

### 18. Late-arriving signal replay

**Justification:** Real event streams contain delayed, corrected, and out-of-order signals; ignoring them creates silent forecast drift and untraceable planning decisions.

**Improvement:** Add replay windows, watermark policies, retroactive run reconstruction, superseded forecast versions, and downstream notification rules for late signals. The workbench should show whether a late signal changes published recommendations, only audit evidence, or future baselines.

### 19. Forecast version governance

**Justification:** Demand organizations need separate baseline, statistical, consensus, executive, scenario, and published versions with explicit ownership and approval.

**Improvement:** Add version families, version lineage, freeze windows, approval state, effective planning cycle, and immutable publication evidence. UI should show side-by-side versions, diffs, approval history, and policy violations for attempted edits after freeze.

### 20. Consensus planning workflow depth

**Justification:** Consensus planning is more than a single adjustment; it involves sales, operations, finance, supply, marketing, and executive negotiation under policy controls.

**Improvement:** Expand `consensus_adjustment` into structured proposals with rationale categories, stakeholder role, affected hierarchy level, quantified impact, confidence, dependency, approval path, and dispute state. The PBC agent should facilitate consensus by summarizing conflicts, evidence, and unresolved risks.

### 21. Planner override guardrails

**Justification:** Overrides can improve forecasts but can also inject bias, gaming, or untraceable decisions when not constrained and measured.

**Improvement:** Add override thresholds, required rationale, historical planner impact, peer review triggers, freeze-window controls, and automatic backtesting of accepted overrides. The UI should show override risk, expected effect on service level and inventory, and whether the agent recommends accept, revise, or escalate.

### 22. Scenario simulation workbench

**Justification:** Planners need to test demand shocks, promotions, capacity constraints, supply disruptions, market-entry changes, and macro assumptions before committing changes.

**Improvement:** Extend `scenario_version` into a full simulation surface with scenario assumptions, changed drivers, affected hierarchy scope, baseline comparison, probabilistic outcomes, shortage exposure, replenishment impact, and approval evidence. Simulations should be side-effect-free until explicitly promoted.

### 23. Causal driver registry

**Justification:** Forecast drivers must be governed business objects with meaning, validity, strength, and applicability rather than arbitrary numeric weights.

**Improvement:** Add driver taxonomy, applicability rules, effect direction, lag structure, saturation behavior, interaction terms, source projection, and model-evidence links to `forecast_driver`. The workbench should show causal assumptions, observed support, and competing explanations.

### 24. Weather, event, and calendar effects

**Justification:** Local weather, holidays, school calendars, paydays, public events, and trading-day effects often explain major short-term demand swings.

**Improvement:** Add event/calendar driver surfaces with geospatial relevance, lead/lag windows, intensity, recurrence, and confidence. Forecast runs should show how much demand was attributed to each calendar or external event and support planner overrides when local knowledge contradicts the model.

### 25. Customer segment demand projection

**Justification:** Aggregate demand can hide materially different behavior across customer cohorts, contract types, loyalty tiers, geographies, or business segments.

**Improvement:** Add segment-aware forecast slices through declared customer and order projections, with privacy-safe aggregation thresholds and no shared customer-table reads. Forecast outputs should expose segment contribution, segment-specific uncertainty, and risks from segment mix shifts.

### 26. Channel and fulfillment-mode separation

**Justification:** Store, online, marketplace, wholesale, subscription, rental, pickup, delivery, and drop-ship demand follow different patterns and require different actions.

**Improvement:** Add channel and fulfillment-mode dimensions to demand signals, models, and results, with reconciliation to product/location hierarchies. The UI should show channel transfer effects, cross-channel cannibalization, and channel-specific service-level recommendations.

### 27. Demand shaping recommendations

**Justification:** Advanced planning should not only predict demand; it should recommend actions to shape demand toward supply, margin, service, and sustainability goals.

**Improvement:** Add recommendations for promotion timing, allocation throttles, substitution nudges, channel steering, pre-order campaigns, backorder messaging, and demand deferral. Each recommendation should include expected demand movement, customer impact, policy constraints, confidence, and handoff events for commerce or pricing PBCs.

### 28. Replenishment-policy coupling

**Justification:** Demand forecasts become operationally valuable only when translated into reorder points, safety stock, order quantities, and replenishment timing.

**Improvement:** Extend `replenishment_recommendation` with policy type, lead-time assumptions, service level, lot-size constraints, review cadence, supplier/calendar constraints, minimum order quantities, inventory coverage, and sensitivity to forecast uncertainty. Recommendations must remain projections and API outputs, not direct writes into inventory or procurement tables.

### 29. Shortage-risk early warning system

**Justification:** Shortage detection after demand outstrips coverage is too late; the PBC should predict risk windows before customer promises or production schedules fail.

**Improvement:** Expand `shortage_risk` with lead-time horizon, affected demand segment, risk probability, expected lost demand, confidence, mitigation options, escalation owner, and event publication rules. The workbench should show shortage-risk heatmaps and recommended actions by urgency and value at risk.

### 30. Demand anomaly triage

**Justification:** Demand spikes, drops, repeated zeroes, abnormal returns, bot demand, and one-off projects require different treatment than ordinary forecast errors.

**Improvement:** Add anomaly categories, triage workflows, quarantine decisions, forecast treatment, and root-cause outcomes. The agent should explain whether an anomaly should be included, excluded, down-weighted, converted into an event driver, or escalated to fraud, commerce, inventory, or operations PBCs through declared contracts.

### 31. Model drift surveillance

**Justification:** Demand models degrade as markets, products, seasons, channels, and customer behavior change; drift needs active governance.

**Improvement:** Extend `model_drift_signal` with feature drift, target drift, residual drift, concept drift, calibration drift, data-quality drift, severity, and retraining recommendations. Release evidence should prove drift monitoring exists for every active model and horizon.

### 32. Forecast model champion/challenger governance

**Justification:** Organizations need controlled model evolution without risking planning stability when new algorithms are introduced.

**Improvement:** Add champion/challenger model comparisons, shadow forecasts, rollout gates, statistical significance checks, operational impact estimates, and rollback plans. The UI should compare accuracy, bias, calibration, runtime cost, interpretability, and downstream shortage/replenishment outcomes.

### 33. Explainable forecast decomposition

**Justification:** Planners and executives need to understand why a forecast changed, not just see the new number.

**Improvement:** Add decomposition output showing baseline, trend, seasonality, lifecycle, promotion, price, weather, event, stockout correction, override, consensus adjustment, and residual components. Every published forecast should include human-readable and machine-readable explanations.

### 34. Forecast exception case management

**Justification:** Forecast exceptions need ownership, deadlines, escalation, evidence, and closure criteria rather than a generic flag.

**Improvement:** Expand `forecast_exception` into a full case lifecycle with severity, reason code, impacted value, assigned role, due date, linked signals, linked forecasts, remediation actions, root cause, recurrence marker, and closure proof. The UI should support exception queues, SLA timers, and agent-drafted remediation plans.

### 35. Planning calendar and freeze governance

**Justification:** Forecast cycles depend on cutoffs, freeze periods, collaboration windows, publication deadlines, and downstream consumption schedules.

**Improvement:** Add planning-calendar records with cycle names, freeze windows, allowed roles, allowed changes, release dates, and downstream dependency events. Commands should reject or escalate changes that violate frozen periods and record policy explanations.

### 36. Demand plan publication contracts

**Justification:** Downstream PBCs require stable, typed, versioned forecast outputs rather than ad hoc result reads.

**Improvement:** Define explicit AppGen-X API and event payloads for published forecast versions, shortage alerts, replenishment recommendations, demand-shaping recommendations, and forecast exception updates. Include compatibility tests, schema-version evidence, and consumer-facing documentation generated from the PBC.

### 37. Cross-PBC boundary proof harness

**Justification:** Predictive demand must use APIs/events/projections for orders, inventory, pricing, promotions, customer, operations, and procurement context without leaking into shared tables.

**Improvement:** Add release-audit tests that scan generated models, services, routes, workbench descriptors, agent skills, and DSL output for unauthorized table references. Boundary evidence should list every external dependency, its contract type, and the exact forecast function that consumes it.

### 38. Semantic demand-document ingestion

**Justification:** Demand inputs often arrive as spreadsheets, account plans, marketing briefs, customer forecasts, allocation files, and executive instructions.

**Improvement:** Add document intake skills that parse demand documents into proposed signals, drivers, scenarios, overrides, or planning parameters with provenance and confidence. The agent must show a preview, validation issues, affected forecasts, and reversible mutations before creating records.

### 39. Forecast-agent command skills

**Justification:** The PBC agent should be able to help planners accomplish domain work, not merely answer help questions.

**Improvement:** Define first-class agent skills for ingesting signals, explaining forecast changes, creating scenarios, comparing versions, opening exceptions, recommending replenishment, detecting shortage risk, and drafting consensus summaries. Skills should use typed command previews, RBAC checks, human confirmation, and audit trails.

### 40. Forecast workbench role specialization

**Justification:** Demand planners, sales leaders, supply planners, finance users, executives, and model governors need different views over the same forecast evidence.

**Improvement:** Expand UI fragments into role-specific workbenches: demand-planner queue, consensus studio, model-governance lab, shortage command center, replenishment board, scenario studio, and executive forecast review. Each view should expose the full relevant capability surface without requiring users to inspect raw runtime artifacts.

### 41. Accuracy metric library

**Justification:** No single accuracy metric fits all demand patterns, horizons, and business costs.

**Improvement:** Add metric definitions for WAPE, MAPE, sMAPE, MASE, bias, service-level miss rate, stockout-adjusted error, interval coverage, pinball loss, and value-weighted error. Planning rules should choose appropriate metrics by demand class and prevent misleading scorecards.

### 42. Demand classification engine

**Justification:** Forecasting methods and policies should change based on demand profile: stable, seasonal, trending, lumpy, intermittent, new, declining, promotional, or event-driven.

**Improvement:** Add demand classification to forecast runs and models, with classification evidence, confidence, transition history, and recommended model families. The workbench should flag when a product/location has changed class and needs different planning treatment.

### 43. Demand data privacy and aggregation controls

**Justification:** Demand signals can reveal sensitive customer, region, contract, or strategic information, especially when segmented or event-driven.

**Improvement:** Add aggregation thresholds, sensitive segment flags, tenant isolation proofs, masking rules, and privacy-aware explanation output. APIs should suppress or coarsen forecast slices that violate configured privacy and confidentiality policies.

### 44. Carbon-aware demand planning

**Justification:** Forecast decisions influence production, fulfillment, replenishment, and transport emissions, so demand planning should expose sustainability tradeoffs.

**Improvement:** Add carbon impact estimates to scenario versions, replenishment recommendations, and demand-shaping proposals using declared projections. Planners should compare service level, margin, shortage exposure, and emissions impact before publishing a demand plan.

### 45. Forecast compute cost governance

**Justification:** Advanced forecasting can become expensive and slow across many SKUs, locations, horizons, and scenarios.

**Improvement:** Add runtime cost estimates, model execution budgets, run prioritization, cache reuse, incremental recomputation, and SLA monitoring. The workbench should show which forecast runs are expensive, stale, blocked, or safe to defer.

### 46. Planning rule and parameter impact simulator

**Justification:** Rule or parameter changes can alter thousands of forecasts, shortages, and recommendations, so planners need impact evidence before activating them.

**Improvement:** Add side-effect-free impact simulations for `planning_rule` and `planning_parameter` changes, including affected forecast count, accuracy expectation, bias risk, shortage exposure, service-level impact, and workbench diffs. The agent should explain the blast radius before requesting approval.

### 47. Cryptographic forecast evidence packets

**Justification:** Forecast outputs influence financial, operational, and customer commitments; auditors need tamper-evident proof of inputs, model version, parameters, and decisions.

**Improvement:** Expand `forecast_audit_proof` into sealed evidence packets containing signal hashes, model hashes, rule/parameter versions, forecast outputs, approval events, and publication signatures. Provide verification APIs that prove integrity without exposing sensitive demand detail.

### 48. Dead-letter and replay operations for forecasting events

**Justification:** Failed event handling can leave demand baselines stale or silently incomplete, especially when consumed signals are core forecast inputs.

**Improvement:** Build a dead-letter operations console with failure taxonomy, retry readiness, replay simulation, duplicate detection, downstream impact analysis, and safe replay commands. Every replay should produce inbox/outbox evidence and forecast-version impact notes.

### 49. End-to-end release evidence for every planning capability

**Justification:** The PBC claims many advanced capabilities; release audits must prove each one has schema, service, route, event, UI, agent, rule, parameter, and test evidence.

**Improvement:** Add a capability evidence matrix that maps every declared Predictive Demand capability to owned tables, commands, route descriptors, event contracts, workbench panels, agent skills, tests, smoke audits, and boundary checks. Release audits should fail when any capability lacks executable evidence.

### 50. Full predictive-demand operating cockpit

**Justification:** A world-class PBC must surface the entire demand-planning operating model, not scatter critical actions across disconnected fragments.

**Improvement:** Build an integrated cockpit that combines signal health, active forecast cycles, version status, consensus conflicts, exceptions, model drift, shortage risk, replenishment recommendations, scenario comparisons, publication readiness, event health, and audit evidence. The cockpit should let users drill into every capability and let the PBC agent execute approved, reversible domain actions from the same surface.
