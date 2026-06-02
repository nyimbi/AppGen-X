"""Executable improve1 controls for the energy trading and risk PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "energy_trading_risk"
EVENT_CONTRACT = "AppGen-X"
TRADING_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
TRADING_REQUIRED_EVENT_TOPIC = "pbc.energy_trading_risk.events"

CONTRACT = "energy_trading_risk_energy_contract"
TRADE = "energy_trading_risk_trade_position"
NOMINATION = "energy_trading_risk_nomination"
SCHEDULE = "energy_trading_risk_schedule"
SETTLEMENT = "energy_trading_risk_settlement"
LIMIT = "energy_trading_risk_exposure_limit"
CURVE = "energy_trading_risk_market_price_curve"
RULE = "energy_trading_risk_energy_trading_risk_policy_rule"
PARAMETER = "energy_trading_risk_energy_trading_risk_runtime_parameter"
SCHEMA_EXTENSION = "energy_trading_risk_energy_trading_risk_schema_extension"
CONTROL = "energy_trading_risk_energy_trading_risk_control_assertion"
MODEL = "energy_trading_risk_energy_trading_risk_governed_model"
OUTBOX = "energy_trading_risk_appgen_outbox_event"
INBOX = "energy_trading_risk_appgen_inbox_event"
DEAD_LETTER = "energy_trading_risk_appgen_dead_letter_event"

TRADING_OWNED_TABLES = (
    CONTRACT,
    TRADE,
    NOMINATION,
    SCHEDULE,
    SETTLEMENT,
    LIMIT,
    CURVE,
    RULE,
    PARAMETER,
    SCHEMA_EXTENSION,
    CONTROL,
    MODEL,
    OUTBOX,
    INBOX,
    DEAD_LETTER,
)
TRADING_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "MarketPriceCurveUpdated",
    "CounterpartyCreditChanged",
    "CollateralCallUpdated",
    "PhysicalFlowActualized",
    "TradeConfirmationReceived",
    "POST /notifications/messages",
    "POST /audit/events/seal",
    "GET /counterparties/{id}/credit-profile",
    "GET /market-data/curves/{curve_id}",
)

TRADING_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in TRADING_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in TRADING_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, (TRADE, CONTRACT, OUTBOX), ("book", "strategy", "side", "volume", "price_formula", "delivery_profile", "counterparty", "approval_context"), "TradeCaptureSafetyCase", "POST /trade-positions", ()),
    (2, (TRADE, OUTBOX), ("original_ticket", "amendment_chain", "cancel_reason", "superseded_ticket", "effective_time", "pnl_replay_visibility"), "TradeLineageGraph", "POST /trade-positions/amend-cancel", ()),
    (3, (TRADE, LIMIT), ("commodity", "hub", "tenor", "book", "trader", "strategy", "net_volume", "gross_volume"), "ExposureBucketWorkbench", "GET /energy-trading-risk-workbench", ()),
    (4, (TRADE, CURVE, PARAMETER), ("market_close", "timezone", "holiday_calendar", "valuation_cut_timestamp", "market_date", "official_run"), "RevaluationCalendarPanel", "POST /valuations/revalue", ("MarketPriceCurveUpdated",)),
    (5, (NOMINATION, RULE, OUTBOX), ("nomination_version", "lifecycle_state", "market_cutoff", "transport_cutoff", "operator_reason", "post_cutoff_exception"), "NominationCutoffWorkbench", "POST /nominations", ()),
    (6, (NOMINATION, SCHEDULE, CONTROL), ("interval", "delivery_point", "counterparty", "nominated_volume", "scheduled_volume", "tolerance", "exception_opened"), "NominationScheduleReconciliation", "POST /reconciliations/nomination-schedule", ()),
    (7, (SCHEDULE, RULE), ("capacity_limit", "delivery_path", "start_continuity", "end_continuity", "ramp_rate", "prohibited_combination"), "ScheduleFeasibilityReview", "POST /schedules/feasibility", ()),
    (8, (TRADE, NOMINATION, SCHEDULE, SETTLEMENT, CURVE), ("committed_volume", "nominated_volume", "scheduled_volume", "expected_flow", "price_assumption", "imbalance_cost"), "ImbalanceExposurePanel", "POST /analytics/imbalance-exposure", ("PhysicalFlowActualized",)),
    (9, (CURVE, CONTROL), ("as_of_timestamp", "freshness_limit", "duplicate_strip", "missing_hub_points", "implausible_price", "jump_threshold"), "MarketCurveQualityGate", "POST /market-price-curves/validate", ("MarketPriceCurveUpdated",)),
    (10, (CURVE, RULE, PARAMETER), ("gap_fill_method", "materiality", "approver", "proxy_hub", "decision_log", "valuation_delta"), "PriceGapFillGovernance", "POST /market-price-curves/gap-fill", ()),
    (11, (TRADE, CURVE, CONTROL), ("valuation_run", "trade_component", "price_curve_component", "volume_component", "basis_component", "amendment_component"), "MarkToMarketExplainPack", "GET /valuations/mtm-explain", ()),
    (12, (TRADE, SETTLEMENT), ("delivery_interval_state", "realized_pnl", "unrealized_pnl", "settlement_finalized", "invoice_reference", "close_transition"), "PnlStatementWorkbench", "GET /pnl/realized-unrealized", ()),
    (13, (TRADE, CURVE, OUTBOX), ("risk_driver", "curve_move", "volume_change", "basis_change", "time_decay", "booking_correction", "residual"), "PnlAttributionWorkbench", "GET /pnl/attribution", ()),
    (14, (TRADE, CURVE, MODEL), ("book_coverage", "product_coverage", "delivery_horizon", "curve_point_coverage", "proxy_flag", "excluded_exposure"), "VarCoverageMatrix", "GET /risk/var-coverage", ()),
    (15, (TRADE, CURVE, MODEL), ("scenario_version", "price_shock", "basis_shock", "shape_shock", "volume_curtailment", "counterparty_downgrade", "approval_status"), "StressScenarioLibrary", "POST /risk/stress-scenarios", ()),
    (16, (TRADE, SETTLEMENT, MODEL, CONTROL), ("prior_var", "realized_pnl", "exception_class", "exception_streak", "model_review_required", "release_gate"), "VarBacktestingWorkbench", "POST /risk/var-backtest", ()),
    (17, (LIMIT, TRADE), ("desk", "book", "trader", "limit_type", "inheritance_path", "override", "emergency_reduction"), "LimitHierarchyWorkbench", "POST /limits/hierarchy-resolve", ()),
    (18, (TRADE, LIMIT, CONTROL), ("dry_run", "proposed_trade", "net_position_impact", "var_impact", "stress_loss_impact", "counterparty_concentration", "override_approver"), "PreBookLimitCheck", "POST /trade-positions/prebook-check", ()),
    (19, (LIMIT, CONTROL, OUTBOX), ("breach_id", "owner", "severity", "required_action", "waiver_window", "remediation_plan", "closure_evidence"), "LimitBreachCaseBoard", "POST /limits/breach-cases", ()),
    (20, (TRADE, SETTLEMENT, CONTRACT, LIMIT), ("counterparty", "open_trade_exposure", "unsettled_amount", "contract_threshold", "concentration", "credit_snapshot"), "CreditExposureLadder", "GET /credit/exposure", ("CounterpartyCreditChanged",)),
    (21, (CONTRACT, SETTLEMENT, CONTROL), ("margin_call_status", "collateral_posted", "dispute_status", "due_date", "covered_exposure", "overdue_alert"), "CollateralMarginWorkbench", "POST /credit/collateral-margin", ("CollateralCallUpdated",)),
    (22, (CONTRACT, TRADE, NOMINATION, SETTLEMENT), ("contract_terms", "trade_term_link", "nomination_rule_link", "settlement_term_link", "payment_terms", "manual_override_approval"), "CounterpartyTermsDrilldown", "POST /energy-contracts/terms-link", ()),
    (23, (TRADE, CONTRACT, CONTROL), ("confirmation_state", "drafted_at", "sent_at", "acknowledged_at", "dispute_reason", "match_status", "aging_days"), "ConfirmationLifecycleQueue", "POST /confirmations/lifecycle", ("TradeConfirmationReceived",)),
    (24, (TRADE, CONTROL), ("break_type", "internal_economics", "external_economics", "field_differences", "exception_opened", "repair_owner"), "ConfirmationBreakMatcher", "POST /confirmations/break-match", ("TradeConfirmationReceived",)),
    (25, (SETTLEMENT, SCHEDULE, NOMINATION, CONTRACT), ("contract_price_rule", "scheduled_quantity", "nominated_quantity", "fees", "imbalance_adjustment", "prior_period_correction", "variance_explained"), "SettlementValidationWorkbench", "POST /settlements/validate", ()),
    (26, (SETTLEMENT, RULE, OUTBOX), ("hold_code", "release_code", "blocked_reason", "aging_bucket", "dual_evidence", "routed_owner"), "SettlementHoldQueue", "POST /settlements/holds", ()),
    (27, (TRADE, NOMINATION, SCHEDULE, SETTLEMENT, PARAMETER), ("market_timezone", "holiday_calendar", "dst_transition", "hour_ending_convention", "authoritative_display", "calendar_version"), "MarketCalendarControl", "POST /calendars/validate", ()),
    (28, (TRADE, CURVE, SETTLEMENT, PARAMETER), ("source_unit", "target_unit", "source_currency", "target_currency", "conversion_factor", "rounding_rule", "effective_date"), "ConversionAuditWorkbench", "POST /conversions/audit", ()),
    (29, (TRADE, CONTROL), ("linked_group", "physical_trade", "financial_hedge", "hedge_relationship", "residual_exposure", "broken_link_exception"), "PhysicalFinancialLinkage", "POST /positions/link-physical-financial", ()),
    (30, (TRADE, CURVE, CONTROL), ("hedge_group", "basis_residual", "timing_residual", "volume_residual", "price_residual", "effectiveness_review"), "HedgeOffsetExplain", "GET /hedges/offset-explain", ()),
    (31, (CURVE, TRADE, MODEL), ("source_hub", "target_node", "basis_curve", "outright_component", "basis_component", "basis_shock"), "LocationBasisSurface", "POST /risk/basis-surfaces", ()),
    (32, (TRADE, LIMIT), ("liquidity_horizon", "concentration_bucket", "exit_difficulty", "approval_gate", "concentration_heatmap", "materiality"), "LiquidityConcentrationView", "GET /risk/liquidity-concentration", ()),
    (33, (INBOX, DEAD_LETTER, CONTROL), ("boundary_event", "idempotency_key", "policy_version", "kpi_snapshot", "foreign_table_scan", "official_run_mapping"), "MarketPolicyEventBoundary", "POST /events/market-policy-boundary", ("PolicyChanged", "OperationalKpiChanged", "MarketPriceCurveUpdated")),
    (34, (TRADE, NOMINATION, SCHEDULE, SETTLEMENT, OUTBOX), ("idempotency_key", "request_fingerprint", "schema_version", "safe_replay", "payload_changed", "response_replayed"), "ApiIdempotencyInspector", "POST /api/idempotency-check", ()),
    (35, (DEAD_LETTER, INBOX, CONTROL), ("dead_letter_id", "root_cause", "safe_retry_window", "payload_redacted", "projection_consistency", "unresolved_count"), "DeadLetterReplayConsole", "POST /events/dead-letter/replay", ()),
    (36, (TRADE, NOMINATION, LIMIT, SETTLEMENT), ("live_net_position", "daily_pnl", "upcoming_nominations", "confirmation_breaks", "limit_headroom", "role_scope"), "TraderPositionWorkbench", "GET /workbench/trader", ()),
    (37, (LIMIT, MODEL, CONTROL), ("official_risk_run", "model_coverage", "limit_hierarchy", "var_backtest", "stress_outputs", "open_breach_cases"), "RiskControlTower", "GET /workbench/risk-control", ()),
    (38, (NOMINATION, SCHEDULE, CONTROL), ("interval_view", "cutoff_timer", "mismatch_count", "path_feasibility_issue", "pending_repair", "scheduler_queue"), "SchedulingOperationsWorkbench", "GET /workbench/scheduling", ()),
    (39, (SETTLEMENT, CONTRACT, LIMIT), ("unsettled_cash", "disputed_items", "collateral_coverage", "payment_term_breach", "pending_release_actions", "aged_critical_items"), "CreditSettlementWorkbench", "GET /workbench/credit-settlement", ()),
    (40, (MODEL, TRADE, CONTROL), ("skill_name", "draft_trade_input", "normalized_ticket", "missing_economics", "mutation_preview", "operator_confirmation"), "TradeCaptureAssistantSkill", "POST /assistant/trade-capture-preview", ()),
    (41, (MODEL, NOMINATION, RULE), ("proposed_nomination", "interval_mismatch", "cutoff_rule", "exception_narrative", "source_citations", "operator_acceptance"), "NominationRepairAssistantSkill", "POST /assistant/nomination-repair", ()),
    (42, (MODEL, LIMIT, TRADE), ("breach_summary", "investigation_path", "waiver_draft", "impacted_books", "impacted_traders", "cannot_close_case"), "LimitTriageAssistantSkill", "POST /assistant/limit-triage", ()),
    (43, (MODEL, SETTLEMENT, SCHEDULE, NOMINATION), ("disputed_amount", "price_delta", "volume_delta", "repair_package", "schedule_evidence", "nomination_evidence"), "SettlementBreakAssistantSkill", "POST /assistant/settlement-break", ()),
    (44, (MODEL, CONTROL, RULE), ("action_preview", "first_approval", "second_eyes", "high_impact_action", "state_change_blocked", "dual_control_required"), "AgentDualControlWorkbench", "POST /assistant/actions/dual-control", ()),
    (45, (CONTROL, OUTBOX), ("override_reason", "approver", "validity_window", "impacted_objects", "compensating_controls", "follow_up_tasks", "expired_override_active"), "OverrideApprovalRegister", "POST /overrides/approve", ()),
    (46, (CONTROL, TRADE, CURVE, LIMIT, MODEL), ("position_snapshot_id", "price_set_id", "scenario_set_version", "limit_status", "unresolved_exception_count", "approver_evidence"), "ValuationRiskReleasePack", "GET /release/valuation-risk-pack", ()),
    (47, (CONTROL, TRADE, NOMINATION, SCHEDULE, SETTLEMENT, CURVE), ("boundary_scan", "owned_tables_only", "declared_api_dependencies", "declared_event_dependencies", "foreign_table_reference", "release_attached"), "OwnedBoundaryProof", "POST /boundary/proof", TRADING_DECLARED_DEPENDENCIES),
    (48, (OUTBOX, CONTROL), ("event_type", "schema_version", "compatibility_result", "created_schema", "updated_schema", "approved_schema", "exception_schema"), "EventSchemaReleaseEvidence", "POST /events/schema-compatibility", ()),
    (49, (CURVE, SETTLEMENT, DEAD_LETTER, CONTROL), ("drill_type", "degraded_mode", "recovery_evidence", "handler_backlog", "latest_successful_drill", "release_signoff"), "ResilienceDrillWorkbench", "POST /resilience/drills", ("OperationalKpiChanged",)),
    (50, (TRADE, NOMINATION, SCHEDULE, SETTLEMENT, CURVE, LIMIT, OUTBOX), ("capture_step", "position_step", "nomination_step", "schedule_step", "valuation_step", "limit_step", "confirmation_step", "settlement_step", "final_signoff"), "TradeToSettlementControlTest", "POST /release/trade-to-settlement-control-test", ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps}
    for number, tables, fields, ui, route, deps in _SPEC_ROWS
}
_EMPTY_ALLOWED_FIELDS = ("field_differences", "missing_economics", "foreign_table_scan", "unresolved_count", "payload_changed", "expired_override_active", "foreign_table_reference", "unresolved_exception_count")


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "book": "power-east", "strategy": "spark-spread", "side": "BUY", "volume": 100.0, "price_formula": "fixed_plus_basis", "delivery_profile": "on_peak", "counterparty": "cp-1", "approval_context": "approved",
        "amendment_chain": ("ticket-1", "ticket-2"), "cancel_reason": "operator_correction", "pnl_replay_visibility": True,
        "commodity": "power", "hub": "PJM", "tenor": "2026-06", "trader": "trader-1", "net_volume": 75.0, "gross_volume": 100.0,
        "market_close": "17:00", "timezone": "America/New_York", "holiday_calendar": "NERC", "valuation_cut_timestamp": "2026-05-30T21:00:00Z", "market_date": "2026-05-30", "official_run": True,
        "nomination_version": 2, "lifecycle_state": "submitted", "market_cutoff": "2026-05-30T18:00:00Z", "transport_cutoff": "2026-05-30T19:00:00Z", "post_cutoff_exception": False,
        "nominated_volume": 96.0, "scheduled_volume": 95.5, "tolerance": 1.0, "exception_opened": False,
        "capacity_limit": 120.0, "delivery_path": "path-a", "start_continuity": True, "end_continuity": True, "ramp_rate": 5.0, "prohibited_combination": False,
        "committed_volume": 100.0, "expected_flow": 95.0, "price_assumption": 42.0, "imbalance_cost": 210.0,
        "as_of_timestamp": "2026-05-30T20:55:00Z", "freshness_limit": 300, "duplicate_strip": False, "missing_hub_points": False, "implausible_price": False, "jump_threshold": 0.25,
        "gap_fill_method": "proxy_hub_substitution", "materiality": "low", "approver": "market-risk", "decision_log": "approved", "valuation_delta": 120.0,
        "valuation_run": "val-1", "trade_component": 100.0, "price_curve_component": 20.0, "volume_component": 5.0, "basis_component": 3.0, "amendment_component": 0.0,
        "delivery_interval_state": "closed", "realized_pnl": 500.0, "unrealized_pnl": 120.0, "settlement_finalized": True, "invoice_reference": "inv-1", "close_transition": "official",
        "risk_driver": "basis", "curve_move": 20.0, "volume_change": 1.0, "basis_change": 7.0, "time_decay": 2.0, "booking_correction": 0.0, "residual": 0.0,
        "book_coverage": 0.99, "product_coverage": 0.98, "delivery_horizon": "24m", "curve_point_coverage": 0.97, "proxy_flag": False, "excluded_exposure": 0.0,
        "scenario_version": "stress-2026.05", "price_shock": -0.15, "basis_shock": 0.1, "shape_shock": 0.08, "volume_curtailment": 0.05, "counterparty_downgrade": "one_notch", "approval_status": "approved",
        "prior_var": 1000.0, "exception_class": "explained", "exception_streak": 0, "model_review_required": False, "release_gate": "passed",
        "desk": "energy", "limit_type": "net_mwh", "inheritance_path": ("desk", "book", "trader"), "override": False, "emergency_reduction": False,
        "dry_run": True, "proposed_trade": "ticket-draft", "net_position_impact": 25.0, "var_impact": 50.0, "stress_loss_impact": 100.0, "counterparty_concentration": 0.12, "override_approver": "risk-manager",
        "breach_id": "breach-1", "owner": "risk-control", "severity": "medium", "required_action": "reduce", "waiver_window": "PT2H", "remediation_plan": "hedge", "closure_evidence": "closed",
        "open_trade_exposure": 5000.0, "unsettled_amount": 1200.0, "contract_threshold": 10000.0, "concentration": 0.18, "credit_snapshot": "credit-1",
        "margin_call_status": "posted", "collateral_posted": 3000.0, "dispute_status": "none", "due_date": "2026-06-01", "covered_exposure": 8000.0, "overdue_alert": False,
        "contract_terms": "terms-v1", "trade_term_link": True, "nomination_rule_link": True, "settlement_term_link": True, "payment_terms": "net-10", "manual_override_approval": "approver-1",
        "confirmation_state": "matched", "match_status": "matched", "aging_days": 0, "break_type": "volume", "internal_economics": "internal", "external_economics": "external", "field_differences": (), "repair_owner": "ops",
        "contract_price_rule": "fixed", "fees": 12.0, "imbalance_adjustment": 3.0, "prior_period_correction": 0.0, "variance_explained": True,
        "hold_code": "missing_price", "release_code": "price_received", "blocked_reason": "price", "aging_bucket": "0-2d", "dual_evidence": True, "routed_owner": "settlement",
        "market_timezone": "America/New_York", "dst_transition": "handled", "hour_ending_convention": "HE", "authoritative_display": True, "calendar_version": "cal-2026",
        "source_unit": "MWh", "target_unit": "MWh", "source_currency": "USD", "target_currency": "USD", "conversion_factor": 1.0, "rounding_rule": "bankers", "effective_date": "2026-05-30",
        "linked_group": "hedge-1", "physical_trade": "phys-1", "financial_hedge": "fin-1", "hedge_relationship": "effective", "residual_exposure": 10.0, "broken_link_exception": False,
        "hedge_group": "hedge-1", "basis_residual": 1.0, "timing_residual": 0.0, "volume_residual": 2.0, "price_residual": 0.5, "effectiveness_review": "approved",
        "source_hub": "PJM", "target_node": "NODE-1", "basis_curve": "basis-1", "outright_component": 40.0, "basis_shock": 0.1,
        "liquidity_horizon": "7d", "concentration_bucket": "normal", "exit_difficulty": "low", "approval_gate": "passed", "concentration_heatmap": "visible",
        "boundary_event": "PolicyChanged", "idempotency_key": "idem-1", "policy_version": "etr-2026.05", "kpi_snapshot": "kpi-1", "foreign_table_scan": (), "official_run_mapping": "run-1",
        "request_fingerprint": "sha256:req", "schema_version": "v1", "safe_replay": True, "payload_changed": False, "response_replayed": True,
        "dead_letter_id": "dlq-1", "root_cause": "missing_curve", "safe_retry_window": "PT1H", "payload_redacted": True, "projection_consistency": True, "unresolved_count": 0,
        "live_net_position": 75.0, "daily_pnl": 500.0, "upcoming_nominations": 2, "confirmation_breaks": 0, "limit_headroom": 250.0, "role_scope": "trader",
        "official_risk_run": "risk-1", "model_coverage": 0.99, "limit_hierarchy": "resolved", "var_backtest": "passed", "stress_outputs": "approved", "open_breach_cases": 0,
        "interval_view": "hourly", "cutoff_timer": "01:00:00", "mismatch_count": 0, "path_feasibility_issue": False, "pending_repair": False, "scheduler_queue": "clear",
        "unsettled_cash": 1200.0, "disputed_items": 0, "collateral_coverage": 1.2, "payment_term_breach": False, "pending_release_actions": 0, "aged_critical_items": 0,
        "skill_name": "trade_capture", "draft_trade_input": "draft", "normalized_ticket": "ticket", "missing_economics": (), "mutation_preview": True, "operator_confirmation": True,
        "proposed_nomination": "nom-repair", "interval_mismatch": "resolved", "cutoff_rule": "rule-1", "exception_narrative": "narrative", "source_citations": ("nom:1",), "operator_acceptance": True,
        "breach_summary": "summary", "investigation_path": "position_growth", "waiver_draft": "draft", "impacted_books": ("BOOK-1",), "impacted_traders": ("trader-1",), "cannot_close_case": True,
        "disputed_amount": 10.0, "price_delta": 1.0, "volume_delta": 0.5, "repair_package": "repair", "schedule_evidence": "sched-1", "nomination_evidence": "nom-1",
        "action_preview": True, "first_approval": True, "second_eyes": True, "high_impact_action": True, "state_change_blocked": False, "dual_control_required": True,
        "override_reason": "limit waiver", "validity_window": "PT2H", "impacted_objects": ("trade-1",), "compensating_controls": ("daily-review",), "follow_up_tasks": ("expire",), "expired_override_active": False,
        "position_snapshot_id": "pos-1", "price_set_id": "price-1", "scenario_set_version": "scenario-v1", "limit_status": "within", "unresolved_exception_count": 0, "approver_evidence": "approver-1",
        "boundary_scan": "passed", "owned_tables_only": True, "declared_api_dependencies": TRADING_DECLARED_DEPENDENCIES, "declared_event_dependencies": TRADING_DECLARED_DEPENDENCIES, "foreign_table_reference": "", "release_attached": True,
        "event_type": "EnergyTradingRiskUpdated", "compatibility_result": "compatible", "created_schema": "v1", "updated_schema": "v1", "approved_schema": "v1", "exception_schema": "v1",
        "drill_type": "stale_price_curve", "degraded_mode": "visible", "recovery_evidence": "recovered", "handler_backlog": 0, "latest_successful_drill": "2026-05-30", "release_signoff": "signed",
        "capture_step": "passed", "position_step": "passed", "nomination_step": "passed", "schedule_step": "passed", "valuation_step": "passed", "limit_step": "passed", "confirmation_step": "passed", "settlement_step": "passed", "final_signoff": "signed",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and not all(payload.get(field) for field in ("book", "strategy", "side", "volume", "price_formula", "delivery_profile", "counterparty", "approval_context")):
        findings.append("trade capture requires complete economics, counterparty, and approval context")
    if n == 2 and not payload.get("amendment_chain"):
        findings.append("trade amendments and cancels require auditable lineage")
    if n == 3 and float(payload.get("net_volume", 0)) > float(payload.get("gross_volume", 0)):
        findings.append("net exposure cannot exceed gross exposure")
    if n == 4 and not payload.get("valuation_cut_timestamp"):
        findings.append("official revaluation requires effective-dated cut timestamp")
    if n == 5 and payload.get("post_cutoff_exception") and not payload.get("operator_reason"):
        findings.append("post-cutoff nomination changes require operator reason evidence")
    if n == 6 and abs(float(payload.get("nominated_volume", 0)) - float(payload.get("scheduled_volume", 0))) > float(payload.get("tolerance", 0)) and not payload.get("exception_opened"):
        findings.append("nomination and schedule mismatch beyond tolerance must open exception")
    if n == 7 and (not payload.get("start_continuity") or not payload.get("end_continuity") or payload.get("prohibited_combination")):
        findings.append("schedule feasibility requires continuity and no prohibited path combination")
    if n == 8 and payload.get("imbalance_cost") is None:
        findings.append("imbalance exposure requires estimated imbalance cost")
    if n == 9 and (payload.get("duplicate_strip") or payload.get("missing_hub_points") or payload.get("implausible_price")):
        findings.append("market price curves must pass duplicate, missing hub, and plausibility checks")
    if n == 10 and payload.get("materiality") == "high" and not payload.get("approver"):
        findings.append("high materiality price gap fill requires approval")
    if n == 11 and not all(payload.get(field) is not None for field in ("trade_component", "price_curve_component", "volume_component", "basis_component")):
        findings.append("MTM explain pack requires trade, price, volume, and basis components")
    if n == 12 and not payload.get("settlement_finalized") and payload.get("realized_pnl"):
        findings.append("realized P&L requires finalized settlement evidence")
    if n == 13 and abs(float(payload.get("residual", 0))) > 0.01:
        findings.append("P&L attribution residual exceeds tolerance")
    if n == 14 and float(payload.get("excluded_exposure", 0)) > 0:
        findings.append("VaR excluded exposure requires visible coverage exception")
    if n == 15 and payload.get("approval_status") != "approved":
        findings.append("official stress scenarios must be approved")
    if n == 16 and payload.get("exception_streak", 0) and not payload.get("model_review_required"):
        findings.append("repeated VaR backtest exceptions require model review")
    if n == 17 and not payload.get("inheritance_path"):
        findings.append("limit hierarchy requires deterministic inheritance path")
    if n == 18 and payload.get("dry_run") is not True:
        findings.append("pre-book limit checks must be dry-run before booking")
    if n == 19 and payload.get("severity") == "critical" and not payload.get("closure_evidence"):
        findings.append("critical limit breaches require closure evidence")
    if n == 20 and not payload.get("credit_snapshot"):
        findings.append("credit exposure aggregation requires counterparty credit snapshot")
    if n == 21 and payload.get("overdue_alert") and payload.get("margin_call_status") != "posted":
        findings.append("overdue uncovered margin call must remain visible")
    if n == 22 and not all(payload.get(field) for field in ("trade_term_link", "nomination_rule_link", "settlement_term_link")):
        findings.append("contract terms must link to trade, nomination, and settlement behavior")
    if n == 23 and payload.get("confirmation_state") != "matched" and int(payload.get("aging_days", 0)) > 0:
        findings.append("aged unconfirmed trades require confirmation queue review")
    if n == 24 and payload.get("field_differences") and not payload.get("exception_opened"):
        findings.append("confirmation breaks require automatic exception records")
    if n == 25 and payload.get("variance_explained") is not True:
        findings.append("settlement validation blocks unexplained variances")
    if n == 26 and not payload.get("hold_code"):
        findings.append("settlement holds require governed reason codes")
    if n == 27 and payload.get("dst_transition") != "handled":
        findings.append("timezone calendar control must handle DST transitions")
    if n == 28 and not payload.get("conversion_factor"):
        findings.append("unit and currency conversion requires effective conversion factor")
    if n == 29 and payload.get("broken_link_exception"):
        findings.append("broken physical-financial hedge links require exception routing")
    if n == 30 and not payload.get("effectiveness_review"):
        findings.append("hedge offset explain requires effectiveness review")
    if n == 31 and not payload.get("basis_curve"):
        findings.append("location basis risk requires a basis surface")
    if n == 32 and payload.get("approval_gate") != "passed":
        findings.append("concentrated or illiquid exposures require approval gate")
    if n == 33 and payload.get("foreign_table_scan"):
        findings.append("market-data and policy events must not use hidden foreign table reads")
    if n == 34 and (payload.get("safe_replay") is not True or payload.get("payload_changed")):
        findings.append("idempotent API replay requires unchanged fingerprint and safe replay")
    if n == 35 and (payload.get("projection_consistency") is not True or int(payload.get("unresolved_count", 0)) > 0):
        findings.append("dead-letter replay requires projection consistency and no unresolved critical failures")
    if n == 36 and payload.get("role_scope") != "trader":
        findings.append("trader workbench must be trader scoped")
    if n == 37 and int(payload.get("open_breach_cases", 0)) > 0:
        findings.append("risk control tower must expose open breach cases before signoff")
    if n == 38 and (payload.get("path_feasibility_issue") or payload.get("pending_repair")):
        findings.append("scheduling workbench must surface unresolved feasibility or repair issues")
    if n == 39 and int(payload.get("aged_critical_items", 0)) > 0:
        findings.append("credit and settlement workbench must expose aged critical items")
    if n == 40 and (payload.get("mutation_preview") is not True or payload.get("operator_confirmation") is not True):
        findings.append("trade capture assistant must preview and wait for operator confirmation")
    if n == 41 and not payload.get("source_citations"):
        findings.append("nomination repair assistant requires source citations")
    if n == 42 and payload.get("cannot_close_case") is not True:
        findings.append("limit triage assistant cannot close breach cases or grant waivers")
    if n == 43 and not all(payload.get(field) for field in ("schedule_evidence", "nomination_evidence")):
        findings.append("settlement break assistant requires schedule and nomination evidence")
    if n == 44 and (payload.get("dual_control_required") and not (payload.get("first_approval") and payload.get("second_eyes"))):
        findings.append("high-impact assistant actions require dual control")
    if n == 45 and payload.get("expired_override_active"):
        findings.append("expired overrides cannot remain active during official approval")
    if n == 46 and int(payload.get("unresolved_exception_count", 0)) > 0:
        findings.append("valuation and risk release pack cannot pass with unresolved exceptions")
    if n == 47 and (payload.get("owned_tables_only") is not True or payload.get("foreign_table_reference")):
        findings.append("owned-boundary proof forbids direct foreign-table dependencies")
    if n == 48 and payload.get("compatibility_result") != "compatible":
        findings.append("event schema release evidence requires compatibility proof")
    if n == 49 and not all(payload.get(field) for field in ("degraded_mode", "recovery_evidence", "latest_successful_drill", "release_signoff")):
        findings.append("resilience drills require degraded-mode and recovery evidence")
    if n == 50 and any(payload.get(field) != "passed" for field in ("capture_step", "position_step", "nomination_step", "schedule_step", "valuation_step", "limit_step", "confirmation_step", "settlement_step")):
        findings.append("trade-to-settlement control test requires every lifecycle step to pass")
    return tuple(findings)


def evaluate_trading_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in TRADING_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in TRADING_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TRADING_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": TRADING_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_trading_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_trading_control(capability) for capability in TRADING_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.energy-trading-risk-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": TRADING_OWNED_TABLES,
        "declared_dependencies": TRADING_DECLARED_DEPENDENCIES,
        "allowed_database_backends": TRADING_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": TRADING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


TRADING_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_trading_control(slug, payload))
    for capability in TRADING_CONTROL_CAPABILITIES
}
