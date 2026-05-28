# Wealth Portfolio Management PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `wealth_portfolio_management` with wealth and advisory specific improvements for client portfolios, investment mandates, suitability, rebalancing, performance, fee schedules, advisory reviews, restrictions, compliance, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `wealth_portfolio_management`.
- Domain purpose: client portfolios, mandates, suitability, rebalancing, performance, fees, and advisory controls.
- Owned records include `client_portfolio`, `investment_mandate`, `suitability_profile`, `rebalance_order`, `performance_snapshot`, `fee_schedule`, `advisory_review`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /client-portfolios`, `POST /investment-mandates`, `POST /suitability-profiles`, `POST /rebalance-orders`, `POST /performance-snapshots`, and `GET /wealth-portfolio-management-workbench`.
- Workbench surfaces include `WealthPortfolioManagementWorkbench`, `WealthPortfolioManagementDetail`, and `WealthPortfolioManagementAssistantPanel`.
- AppGen-X events include `WealthPortfolioManagementCreated`, `WealthPortfolioManagementUpdated`, `WealthPortfolioManagementApproved`, and `WealthPortfolioManagementExceptionOpened`.

## 50 High-Impact Improvements

### 1. Client portfolio lifecycle model

**Justification:** Portfolios move through proposal, opened, funded, active, restricted, under review, transitioning, closed, and archived states.

**Improvement:** Add explicit `client_portfolio` states with transition reason, required evidence, responsible advisor, allowed commands, and AppGen-X events.

**Acceptance evidence:** Tests must reject invalid transitions and show next allowed actions in `WealthPortfolioManagementWorkbench`.

### 2. Client identity and household boundary

**Justification:** Portfolio decisions depend on client, household, entity, tax, and relationship data without owning the master client system.

**Improvement:** Store client and household projections with role, authority, jurisdiction, tax profile, relationship, and freshness from declared dependencies.

**Acceptance evidence:** Boundary tests must prove client data is projected and no external client table is mutated.

### 3. Investment mandate structure

**Justification:** Mandates define objectives, constraints, benchmark, time horizon, liquidity needs, and permitted strategies.

**Improvement:** Expand `investment_mandate` with objective, benchmark, model, target risk, liquidity reserve, time horizon, tax treatment, and allowed asset classes.

**Acceptance evidence:** Tests must block portfolios without an approved active mandate.

### 4. Mandate versioning and consent

**Justification:** Mandate changes require client consent and must preserve prior investment instructions.

**Improvement:** Add mandate versions with effective dates, consent evidence, changed fields, advisor approval, and supersession reason.

**Acceptance evidence:** Tests must reconstruct the active mandate at any historical date.

### 5. Suitability profile completeness

**Justification:** Recommendations must reflect risk tolerance, capacity, knowledge, experience, objectives, liquidity, and constraints.

**Improvement:** Expand `suitability_profile` with scored components, source evidence, review date, missing items, and advisor attestation.

**Acceptance evidence:** Tests must block recommendations when required suitability fields are stale or incomplete.

### 6. Risk tolerance and risk capacity reconciliation

**Justification:** A client may tolerate risk psychologically but lack financial capacity to absorb losses.

**Improvement:** Add reconciliation logic between stated tolerance, financial capacity projection, portfolio objective, and recommended risk band.

**Acceptance evidence:** Tests must flag mismatches and require advisor rationale for overrides.

### 7. Investment restriction controls

**Justification:** Clients may restrict issuers, sectors, products, geographies, ESG factors, leverage, derivatives, or illiquid assets.

**Improvement:** Add restriction records with type, scope, source, effective period, severity, exception path, and affected holdings projection.

**Acceptance evidence:** Tests must block rebalance orders that breach hard restrictions.

### 8. Model portfolio alignment

**Justification:** Many portfolios target a model but require drift tolerance, client restrictions, cash needs, and tax constraints.

**Improvement:** Store model projection, target weights, tolerance bands, substitutions, restriction overrides, and model version freshness.

**Acceptance evidence:** Boundary tests must show model data is projected and not mutated.

### 9. Holdings and position boundary

**Justification:** Portfolio management needs holdings and cash but should not own custody or accounting books.

**Improvement:** Store holdings projections with security, quantity, market value, cost basis projection, cash, account, date, and data freshness.

**Acceptance evidence:** Boundary tests must prove positions are projection inputs and no custody table is mutated.

### 10. Drift monitoring

**Justification:** Portfolios drift from targets due to markets, cash flows, restrictions, and corporate actions.

**Improvement:** Add drift calculations by asset class, sector, security, account, model, and mandate tolerance with severity and reason.

**Acceptance evidence:** Tests must calculate drift and open rebalance candidates.

### 11. Rebalance order lifecycle

**Justification:** Rebalancing requires proposal, review, approval, order staging, execution handoff, cancellation, and post-trade validation.

**Improvement:** Expand `rebalance_order` with lifecycle state, proposed trades, rationale, restrictions check, approval, handoff event, and validation status.

**Acceptance evidence:** Tests must block order handoff until suitability and restriction checks pass.

### 12. Tax-aware rebalancing

**Justification:** Taxable portfolios require awareness of gains, losses, holding periods, wash-sale risk, and client tax preferences.

**Improvement:** Add tax impact projections, realized gain estimate, loss harvesting candidate, tax budget, and override rationale.

**Acceptance evidence:** Tests must show tax impact in rebalance proposals and flag wash-sale risk.

### 13. Cash management rules

**Justification:** Portfolios need cash for withdrawals, fees, taxes, distributions, and liquidity reserves.

**Improvement:** Add cash reserve targets, planned cash flows, sweep instructions, overdraft prevention, and rebalance cash constraints.

**Acceptance evidence:** Tests must reject rebalances that violate minimum cash reserve rules.

### 14. Income and distribution planning

**Justification:** Retirees, trusts, and foundations often require planned income distributions and liquidity.

**Improvement:** Add distribution schedules with amount, frequency, funding source, tax projection, cash buffer, and shortfall warnings.

**Acceptance evidence:** Tests must create cash tasks when projected income is insufficient.

### 15. Performance snapshot governance

**Justification:** Performance must be calculated consistently by period, benchmark, cash flow treatment, fees, and currency.

**Improvement:** Expand `performance_snapshot` with period, method, benchmark, start/end values, flows, net/gross basis, and approval.

**Acceptance evidence:** Tests must reproduce performance snapshots and reject missing benchmark evidence.

### 16. Benchmark assignment and history

**Justification:** Benchmark changes can distort performance evaluation and must be governed.

**Improvement:** Add benchmark projection, blend weights, effective periods, rationale, and client/advisor approval.

**Acceptance evidence:** Tests must preserve historical benchmark assignments.

### 17. Fee schedule depth

**Justification:** Advisory fees may be tiered, householded, waived, minimum, performance-based, or account-specific.

**Improvement:** Expand `fee_schedule` with tier rules, household aggregation, exclusions, billing frequency, waiver, minimum, and effective dates.

**Acceptance evidence:** Tests must calculate fee estimates and preserve waiver evidence.

### 18. Fee billing boundary

**Justification:** Portfolio management needs fee status but should not own invoicing or cash movement.

**Improvement:** Store fee billing projections with billed amount, paid status, adjustment, account source, and freshness.

**Acceptance evidence:** Boundary tests must prove billing data is projected and no billing table is mutated.

### 19. Advisory review workflow

**Justification:** Client portfolios need recurring reviews covering suitability, performance, mandate, fees, restrictions, and next actions.

**Improvement:** Expand `advisory_review` with review type, due date, agenda, findings, client contact evidence, recommendations, and follow-ups.

**Acceptance evidence:** Tests must open overdue review exceptions and close reviews only with required evidence.

### 20. Client communication timeline

**Justification:** Recommendations, reviews, disclosures, fees, restrictions, and performance need clear client communication evidence.

**Improvement:** Add communication records with template, channel, language, delivery evidence, client response, and linked portfolio event.

**Acceptance evidence:** UI tests must show portfolio communication timeline.

### 21. Proposal and recommendation package

**Justification:** Advisors need explainable proposals for allocation, trades, tax impact, suitability, and expected outcomes.

**Improvement:** Add proposal packages with recommendation rationale, alternatives considered, risk impact, cost impact, disclosures, and approval.

**Acceptance evidence:** Tests must generate proposal evidence before rebalance approval.

### 22. Product and security eligibility boundary

**Justification:** Portfolio decisions depend on security master, product approvals, risk ratings, and restrictions outside this PBC.

**Improvement:** Store instrument eligibility projections with product type, risk rating, approval status, jurisdiction, and freshness.

**Acceptance evidence:** Boundary tests must prove security data is projected and not mutated.

### 23. Concentration risk controls

**Justification:** Portfolios can become overexposed to an issuer, sector, geography, currency, asset class, or employer stock.

**Improvement:** Add concentration checks with threshold, exposure basis, mandate rule, severity, and recommended remediation.

**Acceptance evidence:** Tests must flag concentration breaches and block orders that worsen hard breaches.

### 24. Liquidity risk monitoring

**Justification:** Illiquid holdings can conflict with withdrawals, emergencies, and mandate liquidity requirements.

**Improvement:** Add liquidity buckets, liquidation horizon, gate/lockup projection, cash need comparison, and warning rules.

**Acceptance evidence:** Tests must warn when projected liquidity cannot satisfy planned needs.

### 25. ESG and values alignment

**Justification:** Some clients require values-based restrictions, preferences, or reporting.

**Improvement:** Store ESG preference profile, restricted categories, positive tilts, exception handling, and alignment score.

**Acceptance evidence:** Tests must detect holdings that conflict with client preferences.

### 26. Alternative investment commitments

**Justification:** Private funds and alternatives require commitments, capital calls, distributions, NAV, and liquidity planning.

**Improvement:** Add alternative investment projections with commitment, unfunded amount, call schedule, distribution, NAV date, and eligibility checks.

**Acceptance evidence:** Tests must include alternative liquidity and exposure in portfolio views.

### 27. Corporate action impact workflow

**Justification:** Splits, mergers, tenders, calls, and reorganizations can affect mandates, restrictions, and performance.

**Improvement:** Store corporate action projections, affected positions, required elections, due dates, and advisor response.

**Acceptance evidence:** Tests must open action tasks and update portfolio impact when events arrive.

### 28. Client cash flow event handling

**Justification:** Deposits, withdrawals, transfers, charitable gifts, and required distributions affect rebalancing and performance.

**Improvement:** Add cash flow projections with type, amount, timing, source, planned/unplanned flag, and rebalance impact.

**Acceptance evidence:** Tests must adjust drift and cash reserve views after cash flow events.

### 29. Managed account transition planning

**Justification:** New portfolios often require staged transition from legacy holdings with tax, restriction, and market impact constraints.

**Improvement:** Add transition plans with legacy holdings, liquidation order, tax budget, restricted assets, time horizon, and progress.

**Acceptance evidence:** Tests must generate staged transition tasks and track completion.

### 30. Household portfolio aggregation

**Justification:** Advisors manage goals, risk, restrictions, fees, and exposure across related accounts and entities.

**Improvement:** Add household aggregation views with accounts, portfolios, mandates, exposure, performance, fees, and review status.

**Acceptance evidence:** UI tests must show household-level and account-level drilldowns.

### 31. Compliance pre-trade checks

**Justification:** Orders must satisfy suitability, mandate, restrictions, concentration, product eligibility, and disclosure requirements before handoff.

**Improvement:** Add pre-trade check results with pass/fail, rule version, severity, override authority, and evidence.

**Acceptance evidence:** Tests must block order handoff when hard checks fail.

### 32. Post-trade validation boundary

**Justification:** Execution happens elsewhere, but portfolio management must validate fills and resulting drift.

**Improvement:** Store execution projections, fills, rejected orders, trade date, settlement status, and resulting allocation.

**Acceptance evidence:** Boundary tests must prove execution data is projected and no trading table is mutated.

### 33. Exception taxonomy

**Justification:** Suitability, restriction, drift, fee, review, data-quality, performance, and order exceptions need different handling.

**Improvement:** Add exception categories, severity, blocked action, owner, due date, escalation, closure evidence, and reopen reason.

**Acceptance evidence:** Tests must route exceptions to correct workbench queues.

### 34. Workbench portfolio command board

**Justification:** Advisors need one surface for portfolio state, mandate, suitability, drift, performance, fees, restrictions, and reviews.

**Improvement:** Add command board with portfolio summary, risk band, drift, cash, performance, tasks, communications, and assistant panel.

**Acceptance evidence:** UI tests must expose command board sections and governed actions.

### 35. Rule and parameter workbench

**Justification:** Advisory firms tune review intervals, drift thresholds, risk bands, fee rules, concentration limits, and approval policies.

**Improvement:** Add governed editors for portfolio thresholds, suitability recency, fee tiers, review cadence, and order approval rules.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 36. Agent-assisted portfolio review

**Justification:** Advisors need concise review packets from holdings, mandate, performance, suitability, and communication history.

**Improvement:** Add assistant skills that summarize portfolio status, explain drift, draft review agendas, and list required follow-ups.

**Acceptance evidence:** Tests must verify assistant output cites owned records and declared projections.

### 37. Agent-assisted proposal drafting

**Justification:** Recommendations should be explainable, compliant, and tailored to mandate and suitability.

**Improvement:** Add assistant proposal drafts with rationale, alternatives, suitability check, restriction check, fee impact, and disclosure reminders.

**Acceptance evidence:** Tests must require advisor approval before proposals become rebalance orders.

### 38. Agent safety restrictions

**Justification:** AI must not silently place trades, change mandates, alter suitability, approve fees, or send regulated advice.

**Improvement:** Require agent proposals to declare command, affected records, financial impact, suitability impact, evidence, confidence, and approval role.

**Acceptance evidence:** Tests must block high-impact agent writes without explicit approval.

### 39. AppGen-X event specialization

**Justification:** Wealth management composes with client, custody, trading, billing, documents, compliance, and communications through events.

**Improvement:** Define typed events for portfolio opened, mandate approved, suitability updated, rebalance proposed, order handed off, performance certified, and review completed.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 40. Point-in-time portfolio reconstruction

**Justification:** Reviews, complaints, and audits require reconstructing mandate, suitability, holdings projections, and recommendations at a point in time.

**Improvement:** Add event replay for portfolio state, mandate, suitability, restrictions, rebalance proposals, performance snapshots, and reviews.

**Acceptance evidence:** Tests must reproduce historical portfolio snapshots from owned events.

### 41. Cryptographic advisory evidence packet

**Justification:** Client complaints and regulatory reviews require tamper-evident recommendation and review evidence.

**Improvement:** Add hash-linked packets for suitability, mandate, recommendation, rebalance, fee schedule, performance snapshot, and advisory review.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 42. Complaint and dispute linkage

**Justification:** Complaints about advice, fees, performance, restrictions, or trades must influence portfolio actions.

**Improvement:** Store complaint projections with category, status, affected records, blocked actions, response deadline, and resolution.

**Acceptance evidence:** Tests must surface active complaints and block configured actions.

### 43. Fiduciary review evidence

**Justification:** Fiduciary programs need evidence that recommendations serve client objectives and documented constraints.

**Improvement:** Add fiduciary review fields for best-interest rationale, cost comparison, alternatives, conflicts, and disclosure evidence.

**Acceptance evidence:** Tests must require fiduciary evidence for covered recommendation types.

### 44. Conflict of interest controls

**Justification:** Proprietary products, revenue sharing, advisor compensation, and gifts can create conflicts.

**Improvement:** Store conflict projections, disclosure requirement, mitigation, approval, and client acknowledgement.

**Acceptance evidence:** Tests must block recommendations with unresolved conflicts.

### 45. Data-quality scoring

**Justification:** Stale holdings, missing suitability, outdated mandates, and absent benchmark assignments undermine advice.

**Improvement:** Add data-quality scores by portfolio with issue type, severity, remediation task, and trend.

**Acceptance evidence:** Tests must flag incomplete portfolios and show remediation queues.

### 46. Risk scenario analysis

**Justification:** Clients need to understand downside, rate, inflation, currency, and market-shock impact.

**Improvement:** Add scenario snapshots with assumptions, projected impact, vulnerable holdings, mandate implications, and advisor notes.

**Acceptance evidence:** Tests must generate scenario evidence without mutating portfolio state.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic wealth workflows execute after composition.

**Improvement:** Add smoke scenarios for portfolio opening, mandate approval, suitability update, drift detection, rebalance proposal, performance snapshot, and advisory review.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for every scenario.

### 48. Cross-PBC boundary proof

**Justification:** Wealth management touches client, custody, market data, trading, billing, documents, and compliance without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Advisor daily briefing

**Justification:** Advisors need concise status for reviews due, drift, cash needs, restrictions, client events, and compliance exceptions.

**Improvement:** Add briefing generator with portfolio priorities, client follow-ups, rebalance candidates, review deadlines, and risk alerts.

**Acceptance evidence:** Tests must generate briefings from owned records and projections.

### 50. Wealth portfolio command center

**Justification:** Users need one operational surface for client portfolio, mandate, suitability, drift, performance, fees, reviews, and agent guidance.

**Improvement:** Add command center with portfolio timeline, mandate card, suitability status, drift chart, performance panel, fee view, review queue, and assistant panel.

**Acceptance evidence:** UI tests must expose command center context and governed actions without raw datastore access.
