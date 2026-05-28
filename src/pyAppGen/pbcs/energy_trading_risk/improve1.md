# Energy Trading and Risk PBC Improvement Backlog

Built from `manifest.py` and the current package boundary for `energy_trading_risk`. Every item is specific to energy trading and risk operations and includes explicit acceptance evidence.

## Current Domain Evidence Used

- PBC key: `energy_trading_risk`
- Description: energy contracts, positions, nominations, settlement, mark-to-market, exposure, and risk limits
- Owned tables: `energy_contract`, `trade_position`, `nomination`, `schedule`, `settlement`, `exposure_limit`, `market_price_curve`, `energy_trading_risk_policy_rule`, `energy_trading_risk_runtime_parameter`, `energy_trading_risk_schema_extension`, `energy_trading_risk_control_assertion`, `energy_trading_risk_governed_model`
- APIs: `POST /energy-contracts`, `POST /trade-positions`, `POST /nominations`, `POST /schedules`, `POST /settlements`, `GET /energy-trading-risk-workbench`
- Emits: `EnergyTradingRiskCreated`, `EnergyTradingRiskUpdated`, `EnergyTradingRiskApproved`, `EnergyTradingRiskExceptionOpened`
- Consumes: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`
- UI fragments: `EnergyTradingRiskWorkbench`, `EnergyTradingRiskDetail`, `EnergyTradingRiskAssistantPanel`
- Docs: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`

### 1. Trade capture safety case

**Key:** `energy_trading_risk_trade_capture_safety_case`

**Justification:** Energy trades should not enter the book without proving trader intent, product shape, delivery window, pricing terms, counterparty, and approval context; otherwise downstream P&L, VaR, scheduling, and settlement are corrupted at source.

**Improvement:** Add a trade capture safety case that blocks final creation until the package has validated book, strategy, buy or sell side, volume, price formula, delivery profile, optionality flags, and whether the trade is physical, financial, or linked.

**Acceptance evidence:** `POST /trade-positions` fixtures showing accepted and rejected trade captures, visible safety-case badges in `EnergyTradingRiskWorkbench`, and release evidence tying each approved capture to `EnergyTradingRiskCreated` or `EnergyTradingRiskExceptionOpened`.

**Current Domain Evidence Used:** `trade_position`, `energy_contract`, `POST /trade-positions`, `EnergyTradingRiskWorkbench`, `EnergyTradingRiskCreated`, `EnergyTradingRiskExceptionOpened`

### 2. Trade amendment and cancel lineage

**Key:** `energy_trading_risk_trade_amend_cancel_lineage`

**Justification:** Energy desks backdate corrections, split deals, cancel stale tickets, and restate economics; the package needs an auditable lineage instead of overwriting prior trade facts.

**Improvement:** Record amendment, cancel, recapture, and correction chains on `trade_position` so every live position can be traced back to the original ticket and every superseded ticket remains visible for audit and P&L explain.

**Acceptance evidence:** Lineage graphs in `EnergyTradingRiskDetail`, tests proving cancelled trades stop contributing to exposure while preserved history still replays, and emitted update evidence through `EnergyTradingRiskUpdated`.

**Current Domain Evidence Used:** `trade_position`, `EnergyTradingRiskDetail`, `EnergyTradingRiskUpdated`, `energy_trading_risk_event_sourced_operational_history`

### 3. Position netting and exposure buckets

**Key:** `energy_trading_risk_position_netting_buckets`

**Justification:** Gross trade counts do not tell risk operators what the desk actually carries; energy risk is managed by net exposures across commodity, location, tenor, and strategy buckets.

**Improvement:** Build netting logic that aggregates `trade_position` into configurable exposure buckets by commodity, hub, delivery period, book, trader, strategy, and physical versus financial status.

**Acceptance evidence:** Net and gross position snapshots on the workbench, tests for bucket rollups after new trade loads, and release evidence showing bucket definitions used in risk reports.

**Current Domain Evidence Used:** `trade_position`, `exposure_limit`, `GET /energy-trading-risk-workbench`, `energy_trading_risk_analytics`

### 4. Effective-dated revaluation calendar

**Key:** `energy_trading_risk_revaluation_calendar_control`

**Justification:** Valuation mistakes frequently come from using the wrong market date, settlement date, or cutover calendar for a position set.

**Improvement:** Add an effective-dated valuation calendar for `trade_position` that pins each position run to a market close, timezone, holiday calendar, and valuation cut timestamp.

**Acceptance evidence:** Revaluation runs showing the chosen market date and close time, negative tests for late price use after cutoff, and `RELEASE_EVIDENCE.md` entries for official close processing.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `RELEASE_EVIDENCE.md`, `energy_trading_risk_runtime_parameter`

### 5. Nomination versioning and cutoff governance

**Key:** `energy_trading_risk_nomination_cutoff_governance`

**Justification:** Nominations change repeatedly before gate closure; without versioned cutoff handling the package cannot explain which nomination was valid when operators or pipelines acted.

**Improvement:** Add versioned `nomination` lifecycle states for draft, submitted, accepted, superseded, blocked, and post-cutoff exception, with explicit market or transport cutoff timestamps and operator reason codes.

**Acceptance evidence:** Multi-version nomination timelines, cutoff breach alerts in the UI, and regression tests proving post-cutoff changes require exception evidence before approval.

**Current Domain Evidence Used:** `nomination`, `POST /nominations`, `EnergyTradingRiskApproved`, `EnergyTradingRiskExceptionOpened`, `EnergyTradingRiskWorkbench`

### 6. Nomination versus schedule reconciliation

**Key:** `energy_trading_risk_nomination_schedule_reconciliation`

**Justification:** Energy operations fail when nominated volumes and scheduled volumes drift silently across hours, locations, or counterparties.

**Improvement:** Reconcile `nomination` and `schedule` by interval, delivery point, counterparty, and product so mismatches create actionable exceptions before physical operations or settlement are affected.

**Acceptance evidence:** Reconciliation grids with interval-level differences, automatic exception creation when tolerances are breached, and release evidence for same-day repair workflows.

**Current Domain Evidence Used:** `nomination`, `schedule`, `POST /nominations`, `POST /schedules`, `EnergyTradingRiskExceptionOpened`

### 7. Schedule feasibility and pathing checks

**Key:** `energy_trading_risk_schedule_feasibility_checks`

**Justification:** A schedule that ignores capacity, delivery path, or operational constraints is unusable no matter how clean the data entry looks.

**Improvement:** Add schedule feasibility checks for capacity limits, delivery path consistency, start and end continuity, ramp changes, and prohibited delivery combinations across `schedule`.

**Acceptance evidence:** Pre-submit failures for impossible schedules, approved exception paths for operator overrides, and workbench evidence showing the exact feasibility rule hit.

**Current Domain Evidence Used:** `schedule`, `POST /schedules`, `energy_trading_risk_policy_rule`, `EnergyTradingRiskWorkbench`

### 8. Imbalance exposure estimation

**Key:** `energy_trading_risk_imbalance_exposure_estimation`

**Justification:** Imbalance is a direct energy-trading risk surface; if nominated, scheduled, and actual expected flows diverge, exposure appears before settlement does.

**Improvement:** Estimate imbalance exposure from trade commitments, latest `nomination`, active `schedule`, and price assumptions so operators can see likely imbalance cost before closeout.

**Acceptance evidence:** Interval-level imbalance estimates on the workbench, variance thresholds that open exceptions, and release evidence comparing estimates against realized settlement outcomes.

**Current Domain Evidence Used:** `trade_position`, `nomination`, `schedule`, `settlement`, `market_price_curve`, `GET /energy-trading-risk-workbench`

### 9. Market price staleness and boundary checks

**Key:** `energy_trading_risk_market_price_boundary_checks`

**Justification:** Mark-to-market and risk numbers are unsafe when the package cannot detect stale, missing, duplicated, or out-of-bound market curves.

**Improvement:** Add validation on `market_price_curve` for as-of timestamp freshness, duplicate strips, negative or implausible price intervals, missing hub points, and unexpected day-over-day jumps.

**Acceptance evidence:** Curve validation reports, blocked valuation runs when mandatory strips are stale, and release evidence showing which curve set fed each approved valuation.

**Current Domain Evidence Used:** `market_price_curve`, `energy_trading_risk_analytics`, `EnergyTradingRiskExceptionOpened`, `RELEASE_EVIDENCE.md`

### 10. Market price gap fill governance

**Key:** `energy_trading_risk_market_price_gap_fill_governance`

**Justification:** Price gaps occur in real operations, but silent interpolation turns an operational shortcut into an untraceable valuation assumption.

**Improvement:** Support governed gap-fill policies for `market_price_curve`, including carry-forward, neighboring strip interpolation, proxy hub substitution, and hard stop, with approval requirements by materiality.

**Acceptance evidence:** Gap-fill decision logs, side-by-side valuation explain before and after fill, and tests proving high-materiality gaps cannot auto-fill without exception approval.

**Current Domain Evidence Used:** `market_price_curve`, `energy_trading_risk_policy_rule`, `energy_trading_risk_runtime_parameter`, `EnergyTradingRiskApproved`

### 11. Mark-to-market explain pack

**Key:** `energy_trading_risk_mark_to_market_explain_pack`

**Justification:** Traders and controllers need to see why MTM moved, not just that it moved.

**Improvement:** Produce an explain pack for each valuation run that decomposes MTM by trade, bucket, price curve, volume, time decay, location basis, and amendments since the last official run.

**Acceptance evidence:** Drill-through explain views from `EnergyTradingRiskWorkbench`, signed valuation snapshots in `RELEASE_EVIDENCE.md`, and regression tests on known MTM cases.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `GET /energy-trading-risk-workbench`, `RELEASE_EVIDENCE.md`

### 12. Realized versus unrealized P&L split

**Key:** `energy_trading_risk_realized_unrealized_pnl_split`

**Justification:** Risk and finance decisions diverge when the package mixes realized settlement outcomes with open-position valuation.

**Improvement:** Separate realized and unrealized P&L across `trade_position` and `settlement`, with clear transitions when delivery periods close, invoices land, or settlement is finalized.

**Acceptance evidence:** P&L statements showing both views side by side, tests proving closed delivery intervals roll from unrealized to realized, and release evidence for period-end close.

**Current Domain Evidence Used:** `trade_position`, `settlement`, description mentions mark-to-market, `energy_trading_risk_analytics`

### 13. P&L attribution by risk driver

**Key:** `energy_trading_risk_pnl_attribution_by_driver`

**Justification:** Energy desks need to explain whether daily P&L came from curve moves, volume changes, basis changes, time decay, or booking corrections.

**Improvement:** Add daily P&L attribution that tags changes by risk driver and links each attribution component back to the contributing `trade_position`, curve points, and operational edits.

**Acceptance evidence:** Attribution views with drill-through, back-to-front reconciliation between attribution and total P&L, and exception evidence when unexplained residuals exceed thresholds.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `EnergyTradingRiskUpdated`, `EnergyTradingRiskWorkbench`

### 14. VaR model coverage across books and tenors

**Key:** `energy_trading_risk_var_coverage_matrix`

**Justification:** A VaR number is misleading if portions of the book, illiquid tenors, or bespoke structures are excluded without visibility.

**Improvement:** Create a VaR coverage matrix showing which books, products, delivery horizons, and curve points are included, proxied, or excluded from VaR calculations.

**Acceptance evidence:** Coverage reports linked from the workbench, failed approval when excluded exposure breaches materiality, and release evidence capturing the coverage snapshot used for official VaR.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `EnergyTradingRiskWorkbench`, `RELEASE_EVIDENCE.md`

### 15. Stress scenario library for energy books

**Key:** `energy_trading_risk_stress_scenario_library`

**Justification:** Energy portfolios break on transport outages, hub dislocations, curve shocks, and volatility spikes that a single VaR view will not capture.

**Improvement:** Add a governed stress library with price shock, basis shock, shape shock, volume curtailment, counterparty downgrade, and settlement delay scenarios, each versioned and reviewable.

**Acceptance evidence:** Scenario catalogs in the UI, repeatable stress outputs tied to a scenario version, and release evidence proving that official stress packs used approved scenarios only.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `energy_trading_risk_counterfactual_scenario_simulation`, `EnergyTradingRiskAssistantPanel`

### 16. VaR backtesting and breach analysis

**Key:** `energy_trading_risk_var_backtesting_exceptions`

**Justification:** VaR without backtesting drifts into ritual; operators need evidence that actual P&L behavior is still consistent with the configured model.

**Improvement:** Compare daily realized P&L against prior VaR, classify exceptions, store explanatory context, and route repeated exceptions into model review and release gating.

**Acceptance evidence:** Backtesting exception tables, streak alerts in the workbench, and release evidence blocking new model approval when unresolved exception counts exceed policy.

**Current Domain Evidence Used:** `trade_position`, `settlement`, `energy_trading_risk_predictive_risk_scoring`, `energy_trading_risk_governed_model`

### 17. Limit hierarchy by desk, book, and trader

**Key:** `energy_trading_risk_limit_hierarchy`

**Justification:** Energy trading limits are applied at several levels; a flat limit table cannot show whether a breach belongs to a trader, desk, book, commodity, or counterparty slice.

**Improvement:** Expand `exposure_limit` into hierarchical limits with inheritance, overrides, emergency reductions, and separate treatment for gross, net, VaR, stress loss, and concentration limits.

**Acceptance evidence:** Hierarchy views in `EnergyTradingRiskWorkbench`, tests proving inherited limits resolve deterministically, and exception logs for manual overrides.

**Current Domain Evidence Used:** `exposure_limit`, `trade_position`, description mentions risk limits, `GET /energy-trading-risk-workbench`

### 18. Pre-book limit checks

**Key:** `energy_trading_risk_prebook_limit_checks`

**Justification:** Catching limit breaches after a trade is already booked creates unnecessary reversals and exposure spikes.

**Improvement:** Add a pre-book risk check on `POST /trade-positions` that evaluates proposed trade impact on net position, VaR, stress loss, and counterparty concentration before final acceptance.

**Acceptance evidence:** Dry-run responses for proposed trades, blocked submissions with reason codes, and audit evidence showing who approved any override path.

**Current Domain Evidence Used:** `POST /trade-positions`, `trade_position`, `exposure_limit`, `EnergyTradingRiskApproved`

### 19. Limit breach case management

**Key:** `energy_trading_risk_limit_breach_case_management`

**Justification:** A breach needs controlled triage, not only a flag on a dashboard.

**Improvement:** Open structured cases for limit breaches with owner, severity, required action, temporary waiver window, remediation plan, and closure evidence linked to the breached position set.

**Acceptance evidence:** Breach case boards in the workbench, timed escalation tests, and release evidence proving aged critical breaches block approval cycles.

**Current Domain Evidence Used:** `exposure_limit`, `EnergyTradingRiskExceptionOpened`, `EnergyTradingRiskWorkbench`, `energy_trading_risk_workflow`

### 20. Credit exposure aggregation

**Key:** `energy_trading_risk_credit_exposure_aggregation`

**Justification:** Counterparty risk is not visible if open trades, unsettled amounts, and concentration are reviewed in different places with different timing.

**Improvement:** Aggregate current credit exposure across open `trade_position`, pending `settlement`, and contract-level thresholds so operators can see counterparty risk in one view.

**Acceptance evidence:** Counterparty exposure ladders, breached-threshold exceptions, and release evidence showing the exposure snapshot used in daily credit review.

**Current Domain Evidence Used:** `trade_position`, `settlement`, `energy_contract`, `exposure_limit`, `EnergyTradingRiskWorkbench`

### 21. Collateral and margin evidence

**Key:** `energy_trading_risk_collateral_margin_evidence`

**Justification:** When exposure rises, the package should show whether margin was called, posted, disputed, or overdue rather than leaving credit control outside the workflow.

**Improvement:** Add collateral status, margin call records, disputes, and due dates to the counterparty risk flow so exposure decisions can distinguish covered and uncovered exposure.

**Acceptance evidence:** Margin status views, overdue call alerts, and release evidence showing how collateral changed the reported net credit exposure.

**Current Domain Evidence Used:** `energy_contract`, `settlement`, description mentions exposure, `EnergyTradingRiskAssistantPanel`

### 22. Counterparty terms linkage

**Key:** `energy_trading_risk_counterparty_terms_linkage`

**Justification:** Pricing optionality, nomination rules, settlement timelines, and credit triggers often live in the contract terms, not in the trade ticket alone.

**Improvement:** Link `energy_contract` terms directly to `trade_position`, `nomination`, and `settlement` behavior so the package can enforce contract-specific cutoffs, tolerance bands, pricing formulas, and payment terms.

**Acceptance evidence:** Contract-term drill-through in the detail view, tests showing contract-specific rules change downstream behavior, and approval evidence for manual term overrides.

**Current Domain Evidence Used:** `energy_contract`, `trade_position`, `nomination`, `settlement`, `POST /energy-contracts`

### 23. Confirmation lifecycle management

**Key:** `energy_trading_risk_confirmation_lifecycle`

**Justification:** Unconfirmed trades are a direct operational and legal risk for energy desks.

**Improvement:** Track confirmation drafted, sent, acknowledged, disputed, repaired, and fully matched states, with linkage back to trade economics and amendment history.

**Acceptance evidence:** Confirmation status queues, aging reports for unconfirmed trades, and release evidence proving material open confirmations are reviewed before close.

**Current Domain Evidence Used:** `trade_position`, `energy_contract`, `EnergyTradingRiskWorkbench`, `EnergyTradingRiskUpdated`

### 24. Confirmation break matching

**Key:** `energy_trading_risk_confirmation_break_matching`

**Justification:** Breaks on volume, price, delivery point, delivery period, or settlement terms need structured matching rather than manual email searches.

**Improvement:** Add break classification and side-by-side compare flows that show which economic fields differ between internal position data and the external confirmation view.

**Acceptance evidence:** Break dashboards, field-level difference views, and exception records opened automatically for unmatched economic terms.

**Current Domain Evidence Used:** `trade_position`, `EnergyTradingRiskDetail`, `EnergyTradingRiskExceptionOpened`, `energy_trading_risk_semantic_document_instruction_understanding`

### 25. Settlement statement validation

**Key:** `energy_trading_risk_settlement_statement_validation`

**Justification:** Settlement disputes are expensive when the package cannot prove the path from scheduled or delivered volume to billed amount.

**Improvement:** Validate `settlement` against contracted price rules, scheduled or nominated quantities, applicable fees, imbalance adjustments, and prior-period corrections before final approval.

**Acceptance evidence:** Settlement variance reports, blocked approvals for unexplained deltas, and signed close packs in `RELEASE_EVIDENCE.md`.

**Current Domain Evidence Used:** `settlement`, `schedule`, `nomination`, `energy_contract`, `POST /settlements`, `RELEASE_EVIDENCE.md`

### 26. Settlement hold reason codes

**Key:** `energy_trading_risk_settlement_hold_reason_codes`

**Justification:** Operators need a consistent explanation for why cash cannot move, especially across dispute, missing price, missing schedule, missing approval, or counterparty documentation issues.

**Improvement:** Add governed hold codes and release codes on `settlement` so every blocked settlement can be routed, aged, and reported consistently.

**Acceptance evidence:** Hold aging buckets, release workflows with dual evidence, and exception metrics showing top recurring hold causes.

**Current Domain Evidence Used:** `settlement`, `EnergyTradingRiskExceptionOpened`, `EnergyTradingRiskWorkbench`, `energy_trading_risk_policy_rule`

### 27. Timezone and market-calendar control

**Key:** `energy_trading_risk_timezone_calendar_control`

**Justification:** Energy delivery, nomination, and settlement windows cross market calendars and daylight-saving changes that routinely create silent hour mismatches.

**Improvement:** Centralize timezone and market-calendar logic for `trade_position`, `nomination`, `schedule`, and `settlement`, including DST transitions, market holidays, and hour-ending conventions.

**Acceptance evidence:** Calendar test packs for spring and fall cutovers, UI display of authoritative market timezone per record, and release evidence for calendar updates.

**Current Domain Evidence Used:** `trade_position`, `nomination`, `schedule`, `settlement`, `energy_trading_risk_runtime_parameter`

### 28. Unit and currency conversion audit

**Key:** `energy_trading_risk_unit_currency_conversion_audit`

**Justification:** Energy books break when MWh, therm, barrel, or currency conversions are applied inconsistently across capture, valuation, and settlement.

**Improvement:** Record governed conversion factors, effective dates, rounding rules, and source evidence for every unit or currency transformation used by the package.

**Acceptance evidence:** Conversion explain views, tests on canonical cross-unit cases, and settlement close evidence showing the exact conversion set applied.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `settlement`, `energy_trading_risk_runtime_parameter`, `RELEASE_EVIDENCE.md`

### 29. Physical and financial linkage

**Key:** `energy_trading_risk_physical_financial_linkage`

**Justification:** Hedging, proxy pricing, and operational exposure cannot be understood if physical positions and financial hedges live as unrelated rows.

**Improvement:** Allow linked position groups that tie physical and financial `trade_position` records together for hedge explain, risk offset visibility, and exception routing when the relationship breaks.

**Acceptance evidence:** Linked-position views, residual exposure reports after hedge pairing, and tests proving broken links open exceptions before official risk approval.

**Current Domain Evidence Used:** `trade_position`, description mentions positions and exposure, `EnergyTradingRiskExceptionOpened`, `EnergyTradingRiskDetail`

### 30. Hedge offset explain

**Key:** `energy_trading_risk_hedge_offset_explain`

**Justification:** A hedge only helps if operators can see how much risk it actually offsets and where basis or timing mismatch remains.

**Improvement:** Add hedge offset explain that quantifies remaining basis, timing, volume, and price risk after linked positions are combined.

**Acceptance evidence:** Offset dashboards by book and delivery month, residual-risk alerts, and release evidence for approved hedge effectiveness review packs.

**Current Domain Evidence Used:** `trade_position`, `market_price_curve`, `GET /energy-trading-risk-workbench`, `RELEASE_EVIDENCE.md`

### 31. Location basis risk surfaces

**Key:** `energy_trading_risk_location_basis_surfaces`

**Justification:** Hub-to-node and location spread risk is a core energy-specific risk that generic mark-to-market views hide.

**Improvement:** Model basis surfaces on top of `market_price_curve` so positions are exposed to both outright curve moves and location differential moves.

**Acceptance evidence:** Basis decomposition in MTM and stress outputs, visible source hubs and nodes in explain packs, and tests on basis-only shock cases.

**Current Domain Evidence Used:** `market_price_curve`, `trade_position`, `energy_trading_risk_counterfactual_scenario_simulation`, `energy_trading_risk_analytics`

### 32. Liquidity horizon and concentration view

**Key:** `energy_trading_risk_liquidity_concentration_view`

**Justification:** Long-dated or thinly traded energy positions deserve different escalation than near-term liquid exposures.

**Improvement:** Add liquidity horizon, concentration, and exit difficulty dimensions to risk views so operators can separate easily unwound exposure from sticky or concentrated risk.

**Acceptance evidence:** Concentration heatmaps, approval gates for concentrated exposures, and release evidence showing concentration review before risk signoff.

**Current Domain Evidence Used:** `trade_position`, `exposure_limit`, `EnergyTradingRiskWorkbench`, `EnergyTradingRiskApproved`

### 33. Market-data and policy event boundary

**Key:** `energy_trading_risk_market_policy_event_boundary`

**Justification:** Price refreshes and policy changes should enter through declared event boundaries, not hidden table reads or ad hoc scripts.

**Improvement:** Harden event handling so market-data refresh decisions, policy changes, and operational KPI impacts are captured through inbox flows, idempotent handlers, and boundary evidence before they affect risk outputs.

**Acceptance evidence:** Event replay tests, idempotency proofs for repeated boundary events, and release evidence mapping each official risk run to the consumed policy and KPI events.

**Current Domain Evidence Used:** `PolicyChanged`, `OperationalKpiChanged`, `appgen_x_outbox_inbox_eventing`, `idempotent_handlers`, `retry_dead_letter_evidence`

### 34. API contract versioning and idempotency

**Key:** `energy_trading_risk_api_contract_idempotency`

**Justification:** Trade, nomination, schedule, and settlement loads are often retried by upstream orchestrators; duplicate writes and silent contract drift are unacceptable in a risk package.

**Improvement:** Add explicit idempotency keys, request fingerprints, schema version evidence, and replay-safe response handling across the write APIs.

**Acceptance evidence:** API tests proving safe retries for all five write endpoints, schema-version checks in release packs, and exception evidence when a caller reuses a key with changed payload content.

**Current Domain Evidence Used:** `POST /energy-contracts`, `POST /trade-positions`, `POST /nominations`, `POST /schedules`, `POST /settlements`, `idempotent_handlers`

### 35. Dead-letter replay for risk operations

**Key:** `energy_trading_risk_dead_letter_replay`

**Justification:** When event handlers fail, operators need controlled replay that preserves auditability and avoids duplicate risk actions.

**Improvement:** Expose a replay console for energy-trading dead letters with root-cause tagging, safe retry windows, payload redaction, and post-replay verification of projection consistency.

**Acceptance evidence:** Replay runbooks in the UI, tests for duplicate-event defense after replay, and release evidence summarizing unresolved dead letters before approval.

**Current Domain Evidence Used:** `retry_dead_letter_evidence`, `EnergyTradingRiskAssistantPanel`, `EnergyTradingRiskWorkbench`, `EnergyTradingRiskUpdated`

### 36. Trader position workbench

**Key:** `energy_trading_risk_trader_position_workbench`

**Justification:** Traders need a focused surface for intraday position, P&L, limit headroom, and confirmation status rather than a generic all-purpose screen.

**Improvement:** Extend `EnergyTradingRiskWorkbench` with a trader-focused view that emphasizes live net position, daily P&L, upcoming nominations, confirmation breaks, and headroom to key limits.

**Acceptance evidence:** Role-specific workbench screenshots, navigation tests, and release evidence showing the trader surface in the shipped package.

**Current Domain Evidence Used:** `EnergyTradingRiskWorkbench`, `EnergyTradingRiskDetail`, `trade_position`, `nomination`, `exposure_limit`

### 37. Risk control tower workbench

**Key:** `energy_trading_risk_control_tower_workbench`

**Justification:** Risk controllers need a different lens than traders: VaR, stress, concentration, model coverage, and unresolved exceptions.

**Improvement:** Add a risk-control workbench centered on official risk runs, model coverage, limit hierarchy, VaR backtesting, stress outputs, and open breach cases.

**Acceptance evidence:** Controller dashboard coverage in the UI, filtered evidence drilldown by risk date, and release screenshots included in `RELEASE_EVIDENCE.md`.

**Current Domain Evidence Used:** `EnergyTradingRiskWorkbench`, `exposure_limit`, `energy_trading_risk_governed_model`, `RELEASE_EVIDENCE.md`

### 38. Scheduling operations workbench

**Key:** `energy_trading_risk_scheduling_operations_workbench`

**Justification:** Scheduling teams need interval-level visibility into nomination, schedule, cutoff, and imbalance issues, not only financial summaries.

**Improvement:** Add a scheduling workbench for hourly or interval views, cutoff timers, mismatches, path feasibility issues, and pending operator repairs.

**Acceptance evidence:** Scheduler queue screenshots, interval drill-through tests, and release evidence showing unresolved cutoff or mismatch counts before deploy signoff.

**Current Domain Evidence Used:** `schedule`, `nomination`, `EnergyTradingRiskWorkbench`, `EnergyTradingRiskDetail`, `POST /schedules`

### 39. Credit and settlement operations workbench

**Key:** `energy_trading_risk_credit_settlement_workbench`

**Justification:** Credit and settlement operators need aged disputes, unpaid amounts, collateral status, and counterparty concentration in one place.

**Improvement:** Add a combined credit and settlement surface for unsettled cash, disputed items, collateral coverage, payment term breaches, and pending release actions.

**Acceptance evidence:** Operator views with aging ladders, linked dispute detail, and release evidence proving that critical aged items are visible before package release.

**Current Domain Evidence Used:** `settlement`, `energy_contract`, `exposure_limit`, `EnergyTradingRiskWorkbench`, `GET /energy-trading-risk-workbench`

### 40. Trade capture assistant skill

**Key:** `energy_trading_risk_trade_capture_agent_skill`

**Justification:** Agent assistance is useful only if it can help prepare complex trade capture while staying inside domain permissions and previewing its mutations.

**Improvement:** Define a trade-capture assistant skill that can draft trade inputs, normalize structured tickets, flag missing economics, and preview the exact write it would submit.

**Acceptance evidence:** Skill metadata surfaced in `EnergyTradingRiskAssistantPanel`, permission-aware mutation previews, and tests proving the assistant cannot post a trade without explicit operator action.

**Current Domain Evidence Used:** `ai_agent_task_assistance`, `agentic_document_instruction_intake`, `EnergyTradingRiskAssistantPanel`, `trade_position`

### 41. Nomination repair assistant skill

**Key:** `energy_trading_risk_nomination_repair_agent_skill`

**Justification:** Nomination repair is repetitive and time-sensitive; an assistant should accelerate operator work without hiding cutoff risk.

**Improvement:** Add an assistant skill that suggests repaired `nomination` payloads, highlights interval mismatches, and prepares exception narratives for post-cutoff edits.

**Acceptance evidence:** Side-by-side proposed versus current nomination views, operator-accepted repair flows, and tests proving the assistant cites the rule or cutoff it is working around.

**Current Domain Evidence Used:** `nomination`, `EnergyTradingRiskAssistantPanel`, `energy_trading_risk_policy_rule`, `EnergyTradingRiskExceptionOpened`

### 42. Limit triage assistant skill

**Key:** `energy_trading_risk_limit_triage_agent_skill`

**Justification:** Limit breaches need fast triage, but an assistant must explain whether the problem is position growth, curve movement, concentration, or missing offsets.

**Improvement:** Add a limit-triage assistant that prepares breach summaries, proposes investigation paths, and drafts waiver requests with explicit impacted books, traders, and exposure types.

**Acceptance evidence:** Assistant-generated triage packets, operator approval logs, and tests proving the assistant cannot close a breach case or grant a waiver by itself.

**Current Domain Evidence Used:** `exposure_limit`, `trade_position`, `EnergyTradingRiskAssistantPanel`, `EnergyTradingRiskApproved`

### 43. Settlement break resolution assistant skill

**Key:** `energy_trading_risk_settlement_break_agent_skill`

**Justification:** Settlement analysts often spend hours matching lines and explaining deltas that the package already knows how to calculate.

**Improvement:** Add a settlement-break assistant that summarizes disputed amounts, traces price and volume deltas, and prepares a repair or dispute package for operator review.

**Acceptance evidence:** Assistant trace output linked from settlement detail, accepted repair drafts, and tests proving the assistant references the underlying schedule or nomination evidence before recommending action.

**Current Domain Evidence Used:** `settlement`, `schedule`, `nomination`, `EnergyTradingRiskAssistantPanel`, `energy_trading_risk_semantic_document_instruction_understanding`

### 44. Agent action preview and dual control

**Key:** `energy_trading_risk_agent_action_dual_control`

**Justification:** High-impact actions in a risk package require human review; assistant convenience cannot bypass approvals.

**Improvement:** Enforce preview, approval, and second-eyes rules for assistant actions that touch trades, nominations after cutoff, settlements on hold, or official risk approvals.

**Acceptance evidence:** UI previews for every governed assistant action, tests for blocked assistant commits without approval, and release evidence listing all assistant actions that require dual control.

**Current Domain Evidence Used:** `ai_agent_task_assistance`, `permissions`, `EnergyTradingRiskAssistantPanel`, `EnergyTradingRiskApproved`

### 45. Override approval evidence

**Key:** `energy_trading_risk_override_approval_evidence`

**Justification:** Price-gap overrides, limit waivers, post-cutoff nomination changes, and settlement releases must be explainable long after the urgent decision has passed.

**Improvement:** Standardize override evidence across the package with reason code, approver, validity window, impacted objects, compensating controls, and follow-up tasks.

**Acceptance evidence:** Override registers, expiry alerts, and release evidence proving no expired override was active during an official approval or close run.

**Current Domain Evidence Used:** `EnergyTradingRiskApproved`, `EnergyTradingRiskExceptionOpened`, `energy_trading_risk_control_assertion`, `RELEASE_EVIDENCE.md`

### 46. Valuation and risk release pack

**Key:** `energy_trading_risk_valuation_risk_release_pack`

**Justification:** Official risk output should ship with the evidence needed to defend prices, positions, P&L, VaR, stress, and open exceptions.

**Improvement:** Extend `RELEASE_EVIDENCE.md` generation so every official run includes position snapshot ID, price set ID, scenario set version, limit status, unresolved exception counts, and approver evidence.

**Acceptance evidence:** A complete release pack in `RELEASE_EVIDENCE.md`, links back to underlying run artifacts, and tests proving incomplete packs fail release checks.

**Current Domain Evidence Used:** `RELEASE_EVIDENCE.md`, `trade_position`, `market_price_curve`, `exposure_limit`, `energy_trading_risk_governed_model`

### 47. Owned-boundary proof for operational data

**Key:** `energy_trading_risk_owned_boundary_proof`

**Justification:** Risk packages are prone to direct reads into adjacent domains for credit, logistics, or finance shortcuts; that creates hidden coupling and unverifiable results.

**Improvement:** Add release checks proving trading and risk workflows touch only owned tables and declared API or event boundaries, with failures when direct foreign-table dependencies are introduced.

**Acceptance evidence:** Static checks, runtime guard tests, and boundary proof attached to each package release.

**Current Domain Evidence Used:** `energy_contract`, `trade_position`, `nomination`, `schedule`, `settlement`, `market_price_curve`, `appgen_x_outbox_inbox_eventing`

### 48. Event schema release evidence

**Key:** `energy_trading_risk_event_schema_release_evidence`

**Justification:** External consumers of trading and risk events need stability; otherwise release regressions show up in downstream controls after the package is deployed.

**Improvement:** Version emitted event schemas, record compatibility evidence for each release, and prove that `EnergyTradingRiskCreated`, `EnergyTradingRiskUpdated`, `EnergyTradingRiskApproved`, and `EnergyTradingRiskExceptionOpened` still meet declared contracts.

**Acceptance evidence:** Event schema snapshots, compatibility test runs, and release entries linking emitted event versions to the package version.

**Current Domain Evidence Used:** `EnergyTradingRiskCreated`, `EnergyTradingRiskUpdated`, `EnergyTradingRiskApproved`, `EnergyTradingRiskExceptionOpened`, `RELEASE_EVIDENCE.md`

### 49. Resilience drills for price and settlement outages

**Key:** `energy_trading_risk_price_settlement_resilience_drills`

**Justification:** Energy operations need a practiced response when prices arrive late, settlement feeds fail, or a critical handler backlog forms near market close.

**Improvement:** Add resilience drills for stale price curves, failed settlement loads, delayed policy events, and dead-letter spikes, with explicit degraded-mode procedures and recovery evidence.

**Acceptance evidence:** Drill run summaries, degraded-mode workbench indicators, and release evidence showing the latest successful drill before production signoff.

**Current Domain Evidence Used:** `market_price_curve`, `settlement`, `retry_dead_letter_evidence`, `OperationalKpiChanged`, `RELEASE_EVIDENCE.md`

### 50. End-to-end trade-to-settlement control test

**Key:** `energy_trading_risk_trade_to_settlement_control_test`

**Justification:** The package should prove that a realistic trade can flow through capture, positioning, nomination, scheduling, valuation, limit evaluation, confirmation, and settlement with evidence at each step.

**Improvement:** Create a release-gated end-to-end control test that runs a representative energy trade through the full lifecycle, including P&L, VaR, stress, credit exposure, limits, confirmations, and settlement checkpoints.

**Acceptance evidence:** One reproducible control-test pack per release, linked screenshots from the workbench surfaces, emitted event traces, and a final signoff entry in `RELEASE_EVIDENCE.md`.

**Current Domain Evidence Used:** `trade_position`, `nomination`, `schedule`, `settlement`, `market_price_curve`, `exposure_limit`, `EnergyTradingRiskWorkbench`, `RELEASE_EVIDENCE.md`
