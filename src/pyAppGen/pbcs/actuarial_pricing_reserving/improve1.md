# Actuarial Pricing and Reserving PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `actuarial_pricing_reserving` with a hand-curated actuarial roadmap. The PBC owns rating models, actuarial assumptions, experience studies, reserve estimates, loss triangles, capital scenarios, model validation, actuarial controls, governed configuration, agent assistance, and release evidence without owning policy administration, claims administration, investment accounting, or general ledger source-of-truth tables.

## Current Domain Evidence Used

- Stable PBC key: `actuarial_pricing_reserving`.
- Domain purpose: rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, and actuarial controls.
- Owned domain tables: `rating_model`, `actuarial_assumption`, `experience_study`, `reserve_estimate`, `loss_triangle`, `capital_scenario`, `model_validation`, `actuarial_pricing_reserving_policy_rule`, `actuarial_pricing_reserving_runtime_parameter`, `actuarial_pricing_reserving_schema_extension`, `actuarial_pricing_reserving_control_assertion`, `actuarial_pricing_reserving_governed_model`.
- Public APIs: `POST /rating-models`, `POST /actuarial-assumptions`, `POST /experience-studys`, `POST /reserve-estimates`, `POST /loss-triangles`, `GET /actuarial-pricing-reserving-workbench`.
- Emitted AppGen-X events: `ActuarialPricingReservingCreated`, `ActuarialPricingReservingUpdated`, `ActuarialPricingReservingApproved`, `ActuarialPricingReservingExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Rating Model Version Governance

**Justification:** Pricing models must be controlled by product, jurisdiction, segment, effective date, data vintage, and approval status.

**Improvement:** Add rating model versions with draft, candidate, validated, approved, active, suspended, retired, and superseded states plus model owner, product scope, effective window, and rollback evidence.

**Acceptance evidence:** Tests must prove historical quotes use the correct model version, retired models cannot be newly activated, and approvals are required before production use.

### 2. Rating Factor Library

**Justification:** Factors such as age band, territory, exposure, industry, credit tier, vehicle class, construction type, and deductible need explicit governance.

**Improvement:** Add factor definitions with domain, allowed values, source, transformation, monotonicity expectation, missing-value handling, and fairness review marker.

**Acceptance evidence:** Tests must validate factor schemas, reject unknown factor values, and show factor lineage for a sample premium calculation.

### 3. Premium Calculation Trace

**Justification:** Actuaries, underwriters, regulators, and auditors need to explain how base rates, relativities, modifiers, fees, taxes, and overrides produced a premium.

**Improvement:** Add calculation trace records with base rate, factor sequence, multiplicative/additive adjustments, minimum premium, rounding, override, and final indicated premium.

**Acceptance evidence:** Tests must reconstruct a premium from trace evidence and fail if any factor, model version, or override reason is missing.

### 4. Actuarial Assumption Registry

**Justification:** Loss trend, expense load, profit provision, discount rate, lapse, mortality, morbidity, inflation, and development assumptions drive material financial outcomes.

**Improvement:** Expand `actuarial_assumption` with assumption type, source study, selected value, range, rationale, sensitivity, effective period, approval, and retirement state.

**Acceptance evidence:** Tests must prove reserve and pricing runs cite active assumptions and reject unapproved or expired assumptions.

### 5. Assumption Change Impact Analysis

**Justification:** Changing a trend, loss ratio, discount rate, or development factor can materially affect rates, reserves, and capital.

**Improvement:** Add side-effect-free impact analysis comparing current and proposed assumptions across pricing indications, reserve estimates, capital scenarios, and control thresholds.

**Acceptance evidence:** Tests must generate before/after impact reports and block activation of high-impact assumptions without approval evidence.

### 6. Experience Study Cohort Definition

**Justification:** Experience studies are only credible when cohorts, exposure basis, earned period, claim inclusion, and credibility rules are explicit.

**Improvement:** Expand `experience_study` with cohort definition, exposure measure, accident/underwriting/calendar period, claim filters, exclusions, credibility method, and data vintage.

**Acceptance evidence:** Tests must reject studies with ambiguous periods or missing exposure basis and show cohort membership lineage.

### 7. Data Quality Scoring for Studies

**Justification:** Pricing and reserving decisions can be distorted by incomplete exposure, missing claim maturity, duplicate records, coding drift, or stale feeds.

**Improvement:** Add data-quality metrics for completeness, timeliness, duplication, reconciliation variance, outlier rate, missing factor rate, and dependency freshness.

**Acceptance evidence:** Tests must open quality exceptions when configured thresholds fail and show affected study outputs.

### 8. Credibility and Blending Framework

**Justification:** Small cohorts need credibility weighting against broader experience, benchmarks, or selected priors.

**Improvement:** Add credibility method, complement source, selected weight, raw indication, blended indication, and rationale to experience studies and rating selections.

**Acceptance evidence:** Tests must calculate full, partial, and zero credibility cases and preserve the selected complement evidence.

### 9. Loss Development Triangle Governance

**Justification:** Loss triangles need accident period, development age, paid/incurred basis, case reserve, count, exposure, and valuation date discipline.

**Improvement:** Expand `loss_triangle` with triangle type, valuation date, origin period, development age, measure, cumulative/incremental flag, source, and reconciliation status.

**Acceptance evidence:** Tests must validate triangle shape, detect missing diagonals, and reconstruct cumulative and incremental views.

### 10. Development Factor Selection

**Justification:** Selected link ratios and tail factors determine ultimate losses and reserves.

**Improvement:** Add observed factors, volume-weighted averages, simple averages, exclusions, tail factor, selected factor, rationale, and approver.

**Acceptance evidence:** Tests must calculate candidate factors and require selection rationale when chosen factors differ materially from indications.

### 11. Reserve Estimate Methods

**Justification:** Reserve estimates should support chain-ladder, Bornhuetter-Ferguson, expected loss ratio, frequency-severity, case reserve, and stochastic methods.

**Improvement:** Expand `reserve_estimate` with method, selected assumptions, method-specific parameters, ultimate loss, unpaid loss, IBNR, range, and method weight.

**Acceptance evidence:** Tests must run multiple methods on the same triangle and produce selected and method-level reserve evidence.

### 12. Reserve Rollforward

**Justification:** Actuarial reserve movement needs explanation between valuation dates.

**Improvement:** Add rollforward components for prior reserve, paid loss, case movement, incurred development, assumption change, exposure change, discount unwind, and selected reserve.

**Acceptance evidence:** Tests must reconcile prior and current reserves and flag unexplained movement.

### 13. Reserve Uncertainty Distribution

**Justification:** Point estimates hide parameter, process, model, and data uncertainty.

**Improvement:** Add distributions, percentiles, confidence intervals, method variance, scenario variance, and capital linkage for reserve estimates.

**Acceptance evidence:** Tests must produce percentile outputs and show distribution source for capital scenarios.

### 14. Discounting and Inflation Treatment

**Justification:** Long-tail reserves and pricing indications depend on explicit inflation and discounting assumptions.

**Improvement:** Add nominal/real basis, payment pattern, inflation curve, discount curve, currency, yield source, and sensitivity outputs.

**Acceptance evidence:** Tests must distinguish undiscounted, discounted, nominal, and real estimates with traceable assumptions.

### 15. Expense and Profit Provision Modeling

**Justification:** Pricing needs allocated expenses, acquisition costs, claims handling expenses, risk margin, and profit provision.

**Improvement:** Add expense load, variable/fixed split, allocation basis, target return, risk load, commission, and premium tax treatment.

**Acceptance evidence:** Tests must calculate indicated rate need with and without expense/profit provisions and show component trace.

### 16. Rate Adequacy Diagnostics

**Justification:** Actuaries need to know whether current rates cover expected losses, expenses, risk, and target margin.

**Improvement:** Add diagnostics for indicated change, current premium adequacy, loss ratio gap, expense gap, rate dislocation, and credibility-adjusted need.

**Acceptance evidence:** Tests must generate rate adequacy views by segment, product, and jurisdiction.

### 17. Rate Change Capping and Dislocation

**Justification:** Indicated rate changes may need caps, floors, transition rules, and dislocation analysis.

**Improvement:** Add rate change constraints, dislocation bands, policyholder impact cohorts, premium movement distribution, and selected filing change.

**Acceptance evidence:** Tests must apply capping and produce impact distributions without mutating policy records.

### 18. Regulatory Filing Support

**Justification:** Pricing changes often require actuarial memorandum, exhibits, selected assumptions, and jurisdiction-specific evidence.

**Improvement:** Add filing packet metadata, exhibit inventory, jurisdiction rules, actuarial certification, objections, responses, and approval status.

**Acceptance evidence:** Tests must generate a filing evidence packet with model, assumption, study, and impact trace.

### 19. Capital Scenario Definition

**Justification:** Capital analysis depends on stress events, reserve risk, premium risk, catastrophe, credit, market, operational, and correlation assumptions.

**Improvement:** Expand `capital_scenario` with scenario type, shock set, probability, correlation, time horizon, balance sheet basis, and affected products.

**Acceptance evidence:** Tests must run baseline and stressed scenarios and produce traceable capital impact outputs.

### 20. Solvency and Risk Appetite Metrics

**Justification:** Actuarial outputs must map to solvency ratios, risk appetite, and management thresholds.

**Improvement:** Add metrics for required capital, available capital projection, reserve risk, premium risk, tail percentile, breach threshold, and management action.

**Acceptance evidence:** Tests must identify threshold breaches and open review tasks with scenario evidence.

### 21. Catastrophe and Accumulation Inputs

**Justification:** Property, agriculture, travel, credit, and specialty lines can have concentrated catastrophe exposure.

**Improvement:** Add catastrophe peril, region, accumulation cohort, event set reference, gross/net treatment, reinsurance projection, and stress output.

**Acceptance evidence:** Tests must calculate exposure accumulation from declared projections and avoid direct policy or asset table access.

### 22. Reinsurance Impact Projection

**Justification:** Reserves, pricing, and capital can change materially after quota share, excess, aggregate, or facultative reinsurance.

**Improvement:** Store reinsurance program projections with retention, limit, share, reinstatement, attachment, exhaustion, and recoverable uncertainty.

**Acceptance evidence:** Boundary tests must prove reinsurance inputs are declared dependencies and reserve outputs include gross/net views.

### 23. Model Validation Plan

**Justification:** Rating, reserving, and capital models need independent validation before use.

**Improvement:** Expand `model_validation` with validation scope, challenger model, backtest, sensitivity, limitation, reviewer independence, finding, and remediation.

**Acceptance evidence:** Tests must block production activation when required validation is missing, failed, or expired.

### 24. Backtesting and Actual-versus-Expected

**Justification:** Actuarial models must be compared with emerging experience.

**Improvement:** Add backtest periods, predicted values, actual values, error metrics, bias, calibration, drift, and action recommendation.

**Acceptance evidence:** Tests must produce actual-versus-expected reports and open model review when thresholds fail.

### 25. Assumption Governance Calendar

**Justification:** Assumptions should be reviewed on cadence or when trigger events occur.

**Improvement:** Add review cadence, next review date, trigger conditions, owner, overdue escalation, and recertification history.

**Acceptance evidence:** Tests must open overdue assumption reviews and prevent stale assumptions from new runs when policy requires.

### 26. Actuarial Control Assertions

**Justification:** Pricing and reserving need controls over data, assumptions, selections, approvals, validation, and release.

**Improvement:** Add control assertions with population, threshold, owner, frequency, failing records, remediation, and closure evidence.

**Acceptance evidence:** Tests must open failures and require evidence before closing a control breach.

### 27. Pricing Workbench Role Views

**Justification:** Pricing actuaries, reserving actuaries, validators, product managers, finance users, and auditors need different work queues.

**Improvement:** Add workbench views for model drafts, assumption approvals, experience study quality, rate adequacy, filings, validation findings, and control failures.

**Acceptance evidence:** UI tests must prove each view maps to owned data or declared projections with permission-aware actions.

### 28. Reserve Close Workbench

**Justification:** Reserve close is a recurring workflow with deadlines, selections, rollforwards, reviews, and signoffs.

**Improvement:** Add close cycle, valuation date, open triangles, selected methods, reserve review, finance handoff event, and locked close package.

**Acceptance evidence:** Tests must block close lock until required reserve estimates, rollforwards, reviews, and controls are complete.

### 29. Finance Handoff Boundary

**Justification:** Actuarial estimates feed finance but should not write general ledger entries.

**Improvement:** Emit reserve estimate, risk margin, capital metric, and close package events with idempotency keys and evidence references.

**Acceptance evidence:** Boundary tests must fail on GL table writes and pass on declared AppGen-X event contracts.

### 30. Policy and Claims Data Dependency Freshness

**Justification:** Actuarial outputs are unsafe if policy, claim, exposure, premium, or operational KPI projections are stale.

**Improvement:** Add dependency freshness scores, last event time, data vintage, stale-block policy, and override justification.

**Acceptance evidence:** Tests must block or warn on actuarial runs when required dependency freshness is below threshold.

### 31. Large Loss and Outlier Handling

**Justification:** Large losses and outliers materially affect experience studies and reserve selections.

**Improvement:** Add large-loss threshold, catastrophe marker, outlier reason, inclusion/exclusion decision, capped amount, and sensitivity output.

**Acceptance evidence:** Tests must show selected indications with and without large-loss treatment.

### 32. Exposure On-Leveling

**Justification:** Pricing studies need current-rate-level and exposure-adjusted experience.

**Improvement:** Add on-level factors, rate history projection, exposure adjustment, premium trend, selected method, and calculation trace.

**Acceptance evidence:** Tests must calculate on-leveled premium and flag missing rate history projection.

### 33. Trend Selection Framework

**Justification:** Frequency, severity, pure premium, inflation, and exposure trends need transparent selection.

**Improvement:** Add trend candidates, fitted periods, exclusions, selected trend, confidence, sensitivity, and approval rationale.

**Acceptance evidence:** Tests must compare candidate trends and require rationale for selected departures.

### 34. Segmentation and Fairness Review

**Justification:** Rating segmentation must be actuarially sound and comply with fairness and governance policies.

**Improvement:** Add segmentation diagnostics for lift, stability, credibility, protected-attribute proxy risk, dislocation, and governance approval.

**Acceptance evidence:** Tests must generate fairness review evidence and block activation when configured thresholds fail.

### 35. Scenario and Sensitivity Library

**Justification:** Actuaries need repeatable stress tests for trend, severity, frequency, expenses, discounting, catastrophes, and reinsurance.

**Improvement:** Add scenario templates, parameter shocks, impacted models, run outputs, comparison views, and approval state.

**Acceptance evidence:** Tests must run standard and custom scenarios and preserve scenario lineage.

### 36. Actuarial Memorandum Assembly

**Justification:** Decisions require narrative evidence that ties data, methods, assumptions, selections, limitations, and approvals together.

**Improvement:** Add memo sections, exhibit references, generated drafts, reviewer comments, final signoff, and redaction profile.

**Acceptance evidence:** Tests must generate a memo package with citations to owned records and declared projections.

### 37. Agent-Assisted Actuarial Analysis

**Justification:** The actuarial agent should help summarize studies and selections while avoiding unsupported actuarial conclusions.

**Improvement:** Add agent skills for experience study summary, reserve movement explanation, assumption change rationale, model validation finding summary, and filing draft outline.

**Acceptance evidence:** Tests must require citations for each generated claim and mark unsupported statements as drafts requiring review.

### 38. Governed Agent CRUD Commands

**Justification:** The chatbot should help create and update actuarial records without silent model or reserve changes.

**Improvement:** Add command previews for create assumption, open experience study, propose selected factor, create reserve estimate, run capital scenario, record validation finding, and approve control remediation.

**Acceptance evidence:** Intent tests must require record identity, source evidence, preview, confirmation, and approval authority before mutation.

### 39. Governed Model Registry

**Justification:** Predictive pricing, reserving, and capital models require model inventory, intended use, limitations, validation, and monitoring.

**Improvement:** Register models with method type, training data vintage, feature list, validation evidence, limitation, monitoring threshold, and owner.

**Acceptance evidence:** Tests must block use of unregistered or unvalidated governed models in active rating or reserving workflows.

### 40. Model Drift Monitoring

**Justification:** Pricing and reserving models can degrade as claim mix, inflation, behavior, or operations change.

**Improvement:** Add drift metrics for input distribution, calibration, residuals, loss ratio emergence, reserve adequacy, and alert thresholds.

**Acceptance evidence:** Tests must open model review tasks when drift crosses configured thresholds.

### 41. Multi-Currency and Jurisdiction Support

**Justification:** International portfolios require currency, inflation, tax, legal, reporting, and reserving basis controls.

**Improvement:** Add currency basis, exchange rate projection, jurisdiction, reporting basis, localization rules, and conversion evidence.

**Acceptance evidence:** Tests must produce jurisdiction-specific and consolidated actuarial views without shared finance tables.

### 42. Reproducible Run Package

**Justification:** Actuarial outputs must be reproducible from data vintage, assumptions, model version, code version, and parameters.

**Improvement:** Add run package records with input snapshot references, parameter hash, model version, assumption set, actor, timestamp, and output checksum.

**Acceptance evidence:** Tests must rerun a package and detect mismatched inputs or altered outputs.

### 43. Cryptographic Actuarial Evidence Proofs

**Justification:** Rate filings, reserve close, and capital decisions need tamper-evident evidence.

**Improvement:** Add hash chains for assumption approvals, model versions, study results, reserve selections, capital scenarios, validation findings, and close packages.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 44. Dead-Letter and Retry Operations

**Justification:** Data feeds, model runs, validations, and close events can fail and must be remediated safely.

**Improvement:** Add retry reason, risk, idempotency key, replay checkpoint, remediation action, and dead-letter queue for actuarial events.

**Acceptance evidence:** Tests must replay failed events without duplicate reserve estimates, model approvals, or finance handoff events.

### 45. Seeded Actuarial Scenario Library

**Justification:** Release audits need realistic actuarial operating stories.

**Improvement:** Add seeds for new rating model, assumption change, experience study, rate indication, reserve close, capital stress, validation finding, and stale data dependency.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected workbench queues, events, and evidence packets.

### 46. Role-Based Permission Model

**Justification:** Pricing actuaries, reserving actuaries, validators, reviewers, finance users, product users, and auditors need distinct authority.

**Improvement:** Add permissions for model edit, assumption approve, reserve select, close lock, validation signoff, filing package approve, and control remediation.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 47. Management Review and Signoff

**Justification:** Material pricing, reserving, and capital decisions require explicit review by accountable roles.

**Improvement:** Add review packages with materiality, reviewer, questions, response, signoff, dissent, and final decision record.

**Acceptance evidence:** Tests must block active release of material selections without required signoffs.

### 48. Full Actuarial Release Simulation

**Justification:** A complete PBC must prove actuarial operations end to end.

**Improvement:** Add a simulation where data freshness is checked, experience study runs, assumptions are selected, rating model is validated, reserves are estimated, capital stress runs, controls pass, and finance handoff emits.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate policy, claims, reinsurance administration, finance, capital accounting, or regulatory submission ownership.

**Improvement:** Add overlap checks and declared dependency contracts for policy exposure, claims, premium, reinsurance, finance close, filings, audit, and operational KPI inputs.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose actuarial pricing and reserving capabilities through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for rating models, assumptions, experience studies, reserves, loss triangles, capital scenarios, validations, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include actuarial models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
