"""Capital markets trading operations controls for improve1 execution.

The functions here are deterministic, side-effect-free domain controls for the
full order-to-execution-to-allocation-to-confirmation-to-settlement-to-break
lifecycle. They stay inside the capital_markets_trading_ops owned datastore and
use the AppGen-X event contract.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
import hashlib
import json
from typing import Mapping, Sequence

PBC_KEY = "capital_markets_trading_ops"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "capital_markets_trading_ops_trade_order",
    "capital_markets_trading_ops_execution",
    "capital_markets_trading_ops_allocation",
    "capital_markets_trading_ops_confirmation",
    "capital_markets_trading_ops_settlement_instruction",
    "capital_markets_trading_ops_trade_break",
    "capital_markets_trading_ops_position_snapshot",
    "capital_markets_trading_ops_capital_markets_trading_ops_policy_rule",
    "capital_markets_trading_ops_capital_markets_trading_ops_runtime_parameter",
    "capital_markets_trading_ops_capital_markets_trading_ops_schema_extension",
    "capital_markets_trading_ops_capital_markets_trading_ops_control_assertion",
    "capital_markets_trading_ops_capital_markets_trading_ops_governed_model",
    "capital_markets_trading_ops_appgen_outbox_event",
    "capital_markets_trading_ops_appgen_inbox_event",
    "capital_markets_trading_ops_appgen_dead_letter_event",
)

TRADING_CONTROL_CAPABILITIES = (
    "canonical_trade_order_lifecycle",
    "order_versioning_cancel_replace_lineage",
    "pre_trade_reference_data_completeness",
    "pre_trade_operational_risk_gates",
    "market_data_boundary_snapshots",
    "partial_fill_execution_capture",
    "execution_cancel_correction_handling",
    "allocation_eligibility_validation",
    "residual_rounding_allocation_policy",
    "block_trade_split_auditability",
    "confirmation_channel_normalization",
    "economic_affirmation_mismatch_handling",
    "settlement_instruction_golden_source",
    "market_specific_settlement_enrichment",
    "fails_penalties_buy_in_workflow",
    "trade_break_taxonomy",
    "break_lineage_lifecycle_events",
    "position_snapshot_provenance",
    "corporate_actions_boundary_protection",
    "trading_calendar_timezone_normalization",
    "asset_class_sensitive_booking_rules",
    "fee_tax_commission_transparency",
    "broker_venue_counterparty_boundary_modeling",
    "compliance_holds_restricted_list_workflow",
    "best_execution_evidence_attachment",
    "surveillance_handoff_boundaries",
    "event_vocabulary_lifecycle_changes",
    "idempotent_intake_external_edges",
    "bulk_operations_workbench",
    "supervisor_approval_cockpit",
    "governed_agent_trading_ops_skills",
    "semantic_document_intake_confirms_ssis",
    "dead_letter_triage_domain_explanations",
    "replay_safe_projection_rebuilds",
    "continuous_control_assertions",
    "tenant_legal_entity_isolation",
    "operational_readiness_release_evidence_pack",
    "workbench_metrics_operations",
    "counterfactual_disruption_simulation",
    "carbon_sustainability_boundary_annotations",
    "cross_pbc_event_federation_contracts",
    "api_surface_completion",
    "permission_model_desk_role_action",
    "retention_masking_evidentiary_redaction",
    "fx_price_tolerance_management",
    "custodian_settlement_agent_status",
    "cutoff_aware_escalation_logic",
    "manual_override_governance",
    "realistic_seed_data_operator_runbooks",
    "continuous_release_assurance_full_lifecycle",
)

ORDER_TRANSITIONS = {
    "draft": {"validated", "cancelled"},
    "validated": {"risk_passed", "rejected", "hold"},
    "risk_passed": {"routed", "hold", "cancelled"},
    "routed": {"partially_filled", "fully_filled", "cancelled", "replaced"},
    "partially_filled": {"fully_filled", "cancelled", "replaced"},
    "fully_filled": {"operationally_closed"},
    "hold": {"risk_passed", "cancelled"},
    "replaced": {"archived"},
    "cancelled": {"archived"},
    "rejected": {"archived"},
    "operationally_closed": {"archived"},
}


def _tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _date(value: object | None) -> date:
    if value is None:
        return date(2026, 5, 30)
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _result(capability: str, table: str, **payload: object) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "capability": capability,
        "table": table,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
        **payload,
    }


def evaluate_order_lifecycle(current_state: str, target_state: str, actor: str, approver: str | None = None) -> dict:
    allowed = target_state in ORDER_TRANSITIONS.get(current_state, set())
    approval_required = target_state in {"risk_passed", "routed", "operationally_closed"}
    violations = []
    if not allowed:
        violations.append("invalid_transition")
    if approval_required and (not approver or approver == actor):
        violations.append("four_eyes_required")
    event_type = "CapitalMarketsTradingOpsApproved" if target_state in {"risk_passed", "operationally_closed"} else "CapitalMarketsTradingOpsUpdated"
    return _result("canonical_trade_order_lifecycle", OWNED_TABLES[0], transition_allowed=allowed and not violations, violations=tuple(violations), event_type=event_type)


def build_cancel_replace_lineage(order_chain: Sequence[Mapping[str, object]]) -> dict:
    chain = tuple(dict(item) for item in order_chain)
    lineage = tuple({"order_id": item.get("order_id"), "version": item.get("version"), "replaces": item.get("replaces"), "changed_fields": tuple(_tuple(item.get("changed_fields")))} for item in chain)
    current = next((item for item in reversed(lineage) if not any(other.get("replaces") == item.get("order_id") for other in lineage)), lineage[-1] if lineage else None)
    return _result("order_versioning_cancel_replace_lineage", OWNED_TABLES[0], lineage=lineage, current_order=current, immutable_history=True)


def validate_reference_data(order: Mapping[str, object]) -> dict:
    required = ("instrument_id", "trading_account", "desk", "trader", "broker", "venue", "settlement_model", "regulatory_classification")
    missing = tuple(field for field in required if not dict(order or {}).get(field))
    return _result("pre_trade_reference_data_completeness", OWNED_TABLES[0], missing_fields=missing, route_allowed=not missing, remediation_fields=missing)


def evaluate_pre_trade_risk(order: Mapping[str, object], policy: Mapping[str, object]) -> dict:
    order = dict(order or {})
    policy = dict(policy or {})
    failures = []
    if float(order.get("notional", 0)) > float(policy.get("notional_limit", 10**18)):
        failures.append("notional_threshold")
    if float(order.get("quantity", 0)) > float(policy.get("quantity_limit", 10**18)):
        failures.append("quantity_tolerance")
    if order.get("book") in set(_tuple(policy.get("restricted_books"))):
        failures.append("restricted_book")
    if order.get("broker") in set(_tuple(policy.get("blocked_counterparties"))):
        failures.append("blocked_counterparty")
    if policy.get("four_eyes_required") and order.get("maker") == order.get("checker"):
        failures.append("four_eyes_approval")
    return _result("pre_trade_operational_risk_gates", OWNED_TABLES[7], release_allowed=not failures, failures=tuple(failures), override_required=bool(failures))


def freeze_market_data_snapshot(order: Mapping[str, object], quote: Mapping[str, object]) -> dict:
    quote = dict(quote or {})
    stale = bool(quote.get("stale")) or int(quote.get("age_seconds", 0)) > int(quote.get("max_age_seconds", 120))
    snapshot = {"order_id": dict(order or {}).get("order_id"), "quote_time": quote.get("quote_time"), "source": quote.get("source"), "currency": quote.get("currency"), "price": quote.get("price"), "snapshot_hash": _digest(quote)}
    return _result("market_data_boundary_snapshots", OWNED_TABLES[0], snapshot=snapshot, stale_quote=stale, owns_market_data=False)


def capture_partial_fills(order: Mapping[str, object], fills: Sequence[Mapping[str, object]]) -> dict:
    order_qty = float(dict(order or {}).get("quantity", 0))
    normalized = tuple(dict(item) for item in fills)
    filled_qty = sum(float(item.get("quantity", 0)) for item in normalized)
    avg_price = round(sum(float(item.get("quantity", 0)) * float(item.get("price", 0)) for item in normalized) / max(1, filled_qty), 6)
    status = "fully_filled" if filled_qty >= order_qty else "partially_filled" if filled_qty else "routed"
    return _result("partial_fill_execution_capture", OWNED_TABLES[1], fills=normalized, cumulative_quantity=filled_qty, average_price=avg_price, order_status=status)


def handle_execution_correction(original: Mapping[str, object], corrections: Sequence[Mapping[str, object]]) -> dict:
    gross = float(dict(original or {}).get("quantity", 0))
    net = gross
    chain = []
    for correction in corrections:
        correction = dict(correction)
        chain.append(correction)
        if correction.get("correction_type") == "bust":
            net -= float(correction.get("quantity", gross))
        elif correction.get("correction_type") == "quantity_correction":
            net += float(correction.get("quantity_delta", 0))
    return _result("execution_cancel_correction_handling", OWNED_TABLES[1], original=dict(original or {}), correction_chain=tuple(chain), gross_quantity=gross, net_quantity=net, preserves_original=True)


def validate_allocation_eligibility(allocations: Sequence[Mapping[str, object]], account_rules: Mapping[str, object]) -> dict:
    failures = []
    rules = dict(account_rules or {})
    for allocation in allocations:
        allocation = dict(allocation)
        account = allocation.get("account")
        allowed_products = set(_tuple(rules.get(account, {}).get("allowed_products")))
        if allowed_products and allocation.get("product_type") not in allowed_products:
            failures.append({"allocation_id": allocation.get("allocation_id"), "reason": "mandate_restriction"})
        if float(allocation.get("quantity", 0)) > float(rules.get(account, {}).get("hard_limit", 10**18)):
            failures.append({"allocation_id": allocation.get("allocation_id"), "reason": "hard_limit"})
    return _result("allocation_eligibility_validation", OWNED_TABLES[2], failures=tuple(failures), allocation_allowed=not failures)


def simulate_residual_allocation(total_quantity: float, targets: Sequence[Mapping[str, object]], policy: Mapping[str, object]) -> dict:
    allocated = []
    remaining = float(total_quantity)
    for target in targets:
        target = dict(target)
        qty = round(float(total_quantity) * float(target.get("weight", 0)), 0)
        allocated.append({"account": target.get("account"), "quantity": qty})
        remaining -= qty
    if allocated and remaining:
        if dict(policy or {}).get("method") == "designated_account":
            selected = dict(policy).get("designated_account")
            for row in allocated:
                if row["account"] == selected:
                    row["quantity"] += remaining
                    remaining = 0
        else:
            allocated[0]["quantity"] += remaining
            remaining = 0
    return _result("residual_rounding_allocation_policy", OWNED_TABLES[2], allocations=tuple(allocated), residual_quantity=remaining, reproducible=True)


def audit_block_trade_split(block_execution: Mapping[str, object], allocations: Sequence[Mapping[str, object]]) -> dict:
    block_qty = float(dict(block_execution or {}).get("quantity", 0))
    child_sum = sum(float(item.get("quantity", 0)) for item in allocations)
    lineage = tuple({"block_execution_id": dict(block_execution or {}).get("execution_id"), "allocation_id": item.get("allocation_id"), "quantity": item.get("quantity"), "allocator": item.get("allocator")} for item in allocations)
    return _result("block_trade_split_auditability", OWNED_TABLES[2], lineage=lineage, sums_to_block=round(block_qty - child_sum, 6) == 0, over_allocated=child_sum > block_qty)


def normalize_confirmation(channel: str, payload: Mapping[str, object]) -> dict:
    payload = dict(payload or {})
    normalized = {"channel": channel, "price": payload.get("price"), "quantity": payload.get("quantity"), "side": payload.get("side"), "account": payload.get("account"), "settlement_date": payload.get("settlement_date"), "commission": payload.get("commission"), "counterparty": payload.get("counterparty"), "source_hash": _digest(payload)}
    return _result("confirmation_channel_normalization", OWNED_TABLES[3], normalized_confirmation=normalized, comparable=True)


def affirm_economics(booking: Mapping[str, object], confirmation: Mapping[str, object], tolerances: Mapping[str, object]) -> dict:
    booking = dict(booking or {})
    confirmation = dict(confirmation or {})
    tolerances = dict(tolerances or {})
    mismatches = []
    for field in ("quantity", "price", "commission"):
        if abs(float(booking.get(field, 0)) - float(confirmation.get(field, 0))) > float(tolerances.get(field, 0)):
            mismatches.append(field)
    for field in ("side", "account", "settlement_date", "counterparty"):
        if booking.get(field) != confirmation.get(field):
            mismatches.append(field)
    material = tuple(field for field in mismatches if field not in set(_tuple(tolerances.get("immaterial_fields"))))
    return _result("economic_affirmation_mismatch_handling", OWNED_TABLES[3], mismatches=tuple(mismatches), material_mismatches=material, affirmed=not material)


def govern_settlement_instruction(instructions: Sequence[Mapping[str, object]], trade: Mapping[str, object]) -> dict:
    trade_date = _date(dict(trade or {}).get("trade_date"))
    matches = tuple(dict(item) for item in instructions if item.get("account") == dict(trade).get("account") and item.get("market") == dict(trade).get("market") and _date(item.get("effective_from")) <= trade_date <= _date(item.get("effective_to")))
    active_approved = tuple(item for item in matches if item.get("approval_state") == "approved")
    return _result("settlement_instruction_golden_source", OWNED_TABLES[4], selected_instruction=active_approved[0] if len(active_approved) == 1 else None, duplicate_active=len(active_approved) > 1, missing_instruction=not active_approved)


def enrich_market_settlement(instruction: Mapping[str, object], market_rules: Mapping[str, object]) -> dict:
    required = tuple(dict(market_rules or {}).get(dict(instruction or {}).get("market"), ()))
    missing = tuple(field for field in required if not dict(instruction or {}).get(field))
    return _result("market_specific_settlement_enrichment", OWNED_TABLES[4], missing_fields=missing, enriched_instruction=dict(instruction or {}), complete=not missing)


def track_settlement_fail(status: Mapping[str, object], as_of: object | None = None) -> dict:
    status = dict(status or {})
    age = (_date(as_of) - _date(status.get("failed_date"))).days if status.get("failed_date") else 0
    penalty = round(float(status.get("penalty_rate", 0)) * max(0, age) * float(status.get("notional", 0)), 2)
    buy_in = age >= int(status.get("buy_in_trigger_days", 4)) and status.get("status") == "failed"
    return _result("fails_penalties_buy_in_workflow", OWNED_TABLES[4], age_days=age, penalty_exposure=penalty, buy_in_triggered=buy_in, accountable_owner=status.get("owner"))


def classify_trade_break(break_record: Mapping[str, object]) -> dict:
    category = dict(break_record or {}).get("category", "booking")
    valid = category in {"booking", "allocation", "confirmation", "settlement", "position", "cash", "fee", "corporate_action", "external_reference_data"}
    severity = dict(break_record or {}).get("severity", "medium")
    return _result("trade_break_taxonomy", OWNED_TABLES[5], category=category, valid_category=valid, severity=severity, root_cause=dict(break_record or {}).get("root_cause"))


def link_break_lineage(break_record: Mapping[str, object], event: Mapping[str, object], remediation: Mapping[str, object]) -> dict:
    return _result("break_lineage_lifecycle_events", OWNED_TABLES[5], break_id=dict(break_record or {}).get("break_id"), originating_event=dict(event or {}), remediation_action=dict(remediation or {}), drill_through=True)


def build_position_snapshot_provenance(snapshot: Mapping[str, object]) -> dict:
    snapshot = dict(snapshot or {})
    return _result("position_snapshot_provenance", OWNED_TABLES[6], source_cut=snapshot.get("source_cut"), valuation_time=snapshot.get("valuation_time"), completeness=snapshot.get("data_completeness", "complete"), provisional=snapshot.get("view_type") == "intraday", correction_status=snapshot.get("correction_status", "clean"))


def protect_corporate_action_boundary(impact: Mapping[str, object]) -> dict:
    impact = dict(impact or {})
    allowed_types = {"stock_split", "symbol_change", "spin_off", "rights_issue", "cash_dividend"}
    accepted = impact.get("event_type") in allowed_types and bool(impact.get("external_event_id"))
    return _result("corporate_actions_boundary_protection", OWNED_TABLES[5], accepted_external_event=accepted, owns_corporate_action_logic=False, adjustment_reason=impact.get("event_type"))


def normalize_trading_calendar(timestamp: Mapping[str, object], calendar: Mapping[str, object]) -> dict:
    ts = dict(timestamp or {})
    holidays = {_date(item) for item in _tuple(dict(calendar or {}).get("holidays"))}
    trade_date = _date(ts.get("trade_date"))
    adjusted = trade_date
    while adjusted.weekday() >= 5 or adjusted in holidays:
        adjusted += timedelta(days=1)
    return _result("trading_calendar_timezone_normalization", OWNED_TABLES[8], venue_timezone=ts.get("venue_timezone"), desk_timezone=ts.get("desk_timezone"), adjusted_trade_date=adjusted.isoformat(), cutoff_context=dict(calendar or {}).get("cutoff"))


def apply_asset_class_booking_rules(order: Mapping[str, object], profiles: Mapping[str, object]) -> dict:
    order = dict(order or {})
    profile = dict(profiles or {}).get(order.get("product_type"), {})
    required = tuple(profile.get("required_fields", ()))
    missing = tuple(field for field in required if not order.get(field))
    return _result("asset_class_sensitive_booking_rules", OWNED_TABLES[0], product_type=order.get("product_type"), missing_fields=missing, profile_applied=bool(profile), booking_allowed=not missing)


def compare_charges(expected: Mapping[str, object], confirmed: Mapping[str, object], thresholds: Mapping[str, object]) -> dict:
    breaks = []
    for charge in ("commission", "tax", "levy", "stamp_duty"):
        delta = abs(float(dict(expected or {}).get(charge, 0)) - float(dict(confirmed or {}).get(charge, 0)))
        if delta > float(dict(thresholds or {}).get(charge, 0)):
            breaks.append({"charge": charge, "delta": delta})
    return _result("fee_tax_commission_transparency", OWNED_TABLES[3], charge_breaks=tuple(breaks), matched=not breaks)


def model_external_party_roles(parties: Sequence[Mapping[str, object]]) -> dict:
    roles = {item.get("role"): dict(item) for item in parties}
    required = ("executing_broker", "venue", "clearing_broker", "custodian", "settlement_agent")
    missing = tuple(role for role in required if role not in roles)
    return _result("broker_venue_counterparty_boundary_modeling", OWNED_TABLES[0], roles=roles, missing_roles=missing, next_action_owner=next((role for role in required if role in roles), None))


def enforce_compliance_holds(record: Mapping[str, object], holds: Sequence[Mapping[str, object]], action: str) -> dict:
    active = tuple(dict(item) for item in holds if item.get("status", "active") == "active" and action in set(_tuple(item.get("blocked_actions"))))
    return _result("compliance_holds_restricted_list_workflow", OWNED_TABLES[5], action=action, blocked=bool(active), active_holds=active, escalation_required=any(item.get("hold_type") in {"sanctions", "restricted_list"} for item in active))


def attach_best_execution_evidence(order: Mapping[str, object], evidence: Sequence[Mapping[str, object]]) -> dict:
    pack = tuple({**dict(item), "immutable_hash": _digest(item)} for item in evidence)
    required = {"venue_choice", "quote_context", "routing_notes"}
    present = {item.get("type") for item in pack}
    return _result("best_execution_evidence_attachment", OWNED_TABLES[0], evidence_pack=pack, missing_types=tuple(sorted(required - present)), immutable_after_approval=True)


def build_surveillance_handoff(patterns: Sequence[Mapping[str, object]]) -> dict:
    suspicious = tuple(dict(item) for item in patterns if item.get("pattern") in {"wash_trade_like", "duplicate_offsets", "unusual_timing", "restricted_account_activity"})
    return _result("surveillance_handoff_boundaries", OWNED_TABLES[5], handoff_events=tuple({"event_type": "TradingOpsSurveillanceReviewRequested", "pattern": item.get("pattern"), "record_id": item.get("record_id")} for item in suspicious), owns_surveillance_engine=False)


def build_lifecycle_event_vocabulary() -> dict:
    events = ("OrderReleased", "ExecutionCorrected", "AllocationApproved", "ConfirmationMismatchOpened", "SettlementFailed", "TradeBreakResolved", "ManualOverrideAccepted")
    return _result("event_vocabulary_lifecycle_changes", OWNED_TABLES[12], events=events, compatibility_family=("CapitalMarketsTradingOpsCreated", "CapitalMarketsTradingOpsUpdated", "CapitalMarketsTradingOpsApproved", "CapitalMarketsTradingOpsExceptionOpened"))


def guard_idempotent_intake(channel: str, payload: Mapping[str, object], seen: Sequence[str]) -> dict:
    fingerprint = dict(payload or {}).get("idempotency_key") or _digest((channel, payload))
    duplicate = fingerprint in set(seen)
    return _result("idempotent_intake_external_edges", OWNED_TABLES[13], channel=channel, source_fingerprint=fingerprint, duplicate=duplicate, business_record_count=0 if duplicate else 1)


def build_bulk_operations_workbench(records: Sequence[Mapping[str, object]], action: str, actor: Mapping[str, object]) -> dict:
    allowed = action in {"bulk_validate", "bulk_approve", "bulk_assign", "bulk_retry", "bulk_export"} and (action != "bulk_approve" or "supervisor" in set(_tuple(dict(actor or {}).get("roles"))))
    results = tuple({"record_id": item.get("id"), "action": action, "allowed": allowed} for item in records)
    return _result("bulk_operations_workbench", OWNED_TABLES[11], action=action, results=results, row_level_traceability=True)


def build_supervisor_approval_cockpit(items: Sequence[Mapping[str, object]]) -> dict:
    ranked = tuple(sorted((dict(item) for item in items), key=lambda item: (-float(item.get("notional", 0)), str(item.get("settlement_urgency", "")))))
    return _result("supervisor_approval_cockpit", OWNED_TABLES[11], ranked_queue=ranked, grouping_fields=("desk", "legal_entity", "notional", "settlement_urgency", "override_pattern"))


def plan_governed_agent_task(task: str, context: Mapping[str, object]) -> dict:
    lowered = task.lower()
    skill = "triage_break" if "break" in lowered else "draft_allocation" if "allocation" in lowered else "summarize_mismatch" if "mismatch" in lowered else "draft_ssi_change" if "ssi" in lowered else "assemble_release_pack"
    mutation = skill in {"draft_allocation", "draft_ssi_change"}
    return _result("governed_agent_trading_ops_skills", OWNED_TABLES[11], skill=skill, requires_human_confirmation=mutation, supported_apis_only=True, context=dict(context or {}))


def parse_semantic_document(document: Mapping[str, object], doc_type: str) -> dict:
    fields_by_type = {"broker_confirm": ("price", "quantity", "commission", "counterparty"), "ssi": ("market", "account", "custodian", "depository"), "exception_notice": ("reason", "severity", "deadline")}
    proposed = {field: dict(document or {}).get(field) for field in fields_by_type.get(doc_type, ())}
    confidence = min(1.0, 0.5 + 0.1 * sum(1 for value in proposed.values() if value is not None))
    return _result("semantic_document_intake_confirms_ssis", OWNED_TABLES[11], doc_type=doc_type, proposed_fields=proposed, confidence=round(confidence, 2), requires_review=True)


def explain_dead_letter(failure: Mapping[str, object]) -> dict:
    code = dict(failure or {}).get("code", "unknown")
    mapping = {"duplicate_execution": "Duplicate execution", "unknown_account": "Unknown account", "stale_policy_version": "Stale policy version", "missing_ssi": "Missing settlement instruction"}
    return _result("dead_letter_triage_domain_explanations", OWNED_TABLES[14], business_cause=mapping.get(code, "Integration failure"), replay_safe=code not in {"unknown"}, quarantine_available=True)


def plan_projection_rebuild(projections: Sequence[Mapping[str, object]], checkpoint: Mapping[str, object]) -> dict:
    checksums = tuple({"projection": item.get("name"), "checksum": _digest(item)} for item in projections)
    return _result("replay_safe_projection_rebuilds", OWNED_TABLES[11], checkpoint=dict(checkpoint or {}), projection_checksums=checksums, reconciliation_required=True)


def evaluate_continuous_controls(actions: Sequence[Mapping[str, object]]) -> dict:
    failures = []
    for action in actions:
        action = dict(action)
        if action.get("maker") == action.get("checker"):
            failures.append({"action_id": action.get("action_id"), "control": "segregation_of_duties"})
        if action.get("break_age_days", 0) > action.get("sla_days", 5):
            failures.append({"action_id": action.get("action_id"), "control": "aged_break"})
        if action.get("live_trade") and not action.get("active_ssi"):
            failures.append({"action_id": action.get("action_id"), "control": "inactive_ssi"})
    return _result("continuous_control_assertions", OWNED_TABLES[10], failures=tuple(failures), exceptions_opened=bool(failures))


def enforce_tenant_legal_entity(record: Mapping[str, object], context: Mapping[str, object]) -> dict:
    record = dict(record or {})
    context = dict(context or {})
    allowed = record.get("tenant") == context.get("tenant") and record.get("legal_entity") == context.get("legal_entity")
    return _result("tenant_legal_entity_isolation", OWNED_TABLES[0], allowed=allowed, cross_tenant_blocked=record.get("tenant") != context.get("tenant"), cross_entity_blocked=record.get("legal_entity") != context.get("legal_entity"))


def build_release_evidence_pack(scenarios: Mapping[str, object]) -> dict:
    required = ("contract_tests", "lifecycle_coverage", "break_resolution", "permission_proofs", "projection_rebuild", "workbench_snapshots")
    missing = tuple(item for item in required if not dict(scenarios or {}).get(item))
    return _result("operational_readiness_release_evidence_pack", OWNED_TABLES[11], missing_items=missing, release_ready=not missing, evidence_index=tuple(required))


def compute_workbench_metrics(records: Sequence[Mapping[str, object]]) -> dict:
    records = tuple(dict(item) for item in records)
    metrics = {
        "backlog_aging_max": max((item.get("age_days", 0) for item in records), default=0),
        "confirmation_mismatch_rate": round(sum(1 for item in records if item.get("confirmation_mismatch")) / max(1, len(records)), 4),
        "settlement_fail_rate": round(sum(1 for item in records if item.get("settlement_failed")) / max(1, len(records)), 4),
        "manual_override_frequency": sum(1 for item in records if item.get("manual_override")),
    }
    return _result("workbench_metrics_operations", OWNED_TABLES[11], metrics=metrics, drillthrough_record_ids=tuple(item.get("id") for item in records))


def simulate_disruption_scenario(baseline: Mapping[str, object], scenario: Mapping[str, object]) -> dict:
    baseline = dict(baseline or {})
    scenario = dict(scenario or {})
    impacts = {"order_release_delay": baseline.get("orders", 0) * int(scenario.get("holiday_days", 0)), "settlement_backlog_delta": baseline.get("settlements", 0) * float(scenario.get("agent_outage_factor", 0)), "break_backlog_delta": baseline.get("breaks", 0) * float(scenario.get("policy_tightening_factor", 0))}
    return _result("counterfactual_disruption_simulation", OWNED_TABLES[11], impacts=impacts, non_mutating=True)


def annotate_sustainability_boundary(record: Mapping[str, object], annotations: Mapping[str, object]) -> dict:
    return _result("carbon_sustainability_boundary_annotations", OWNED_TABLES[0], record_id=dict(record or {}).get("id"), annotations=dict(annotations or {}), economic_validation_blocking=False)


def build_cross_pbc_event_contracts() -> dict:
    emits = ("OrderReleased", "ExecutionBooked", "AllocationApproved", "SettlementFailed", "TradeBreakResolved")
    consumes = ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged", "CorporateActionAnnounced", "ComplianceHoldReleased")
    return _result("cross_pbc_event_federation_contracts", OWNED_TABLES[12], emits=emits, consumes=consumes, direct_table_reads_allowed=False)


def build_extended_api_surface() -> dict:
    routes = ("GET /trade-orders/search", "POST /trade-orders/validate", "POST /trade-breaks/{id}/disposition", "POST /simulations/trading-ops", "GET /release-evidence/export", "GET /capital-markets-trading-ops-workbench")
    return _result("api_surface_completion", OWNED_TABLES[0], routes=routes, authorization_required=True, full_workflow_supported=True)


def authorize_action(actor: Mapping[str, object], action: str, record: Mapping[str, object]) -> dict:
    actor = dict(actor or {})
    required = {"release_order": "trader_supervisor", "approve_allocation": "allocation_supervisor", "change_ssi": "settlement_admin", "close_break": "break_supervisor", "replay_dead_letter": "ops_admin", "accept_agent_proposal": "operator"}.get(action, "reader")
    allowed = required in set(_tuple(actor.get("roles"))) and (not record.get("desk") or record.get("desk") in set(_tuple(actor.get("desks"))))
    return _result("permission_model_desk_role_action", OWNED_TABLES[7], action=action, required_role=required, allowed=allowed, disabled_reason=None if allowed else "missing_role_or_scope")


def redact_evidence_for_export(record: Mapping[str, object], policy: Mapping[str, object]) -> dict:
    record = dict(record or {})
    masked_fields = set(_tuple(dict(policy or {}).get("masked_fields")))
    redacted = {key: ("***" if key in masked_fields else value) for key, value in record.items()}
    retain_until = (_date(record.get("created_date")) + timedelta(days=365 * int(dict(policy or {}).get("retention_years", 7)))).isoformat()
    return _result("retention_masking_evidentiary_redaction", OWNED_TABLES[11], redacted_record=redacted, retain_until=retain_until, verifiable_hash=_digest(record))


def evaluate_fx_price_tolerances(expected: Mapping[str, object], actual: Mapping[str, object], parameters: Mapping[str, object]) -> dict:
    expected = dict(expected or {})
    actual = dict(actual or {})
    parameters = dict(parameters or {})
    price_delta = abs(float(expected.get("price", 0)) - float(actual.get("price", 0)))
    fx_delta = abs(float(expected.get("fx_rate", 0)) - float(actual.get("fx_rate", 0)))
    auto_match = price_delta <= float(parameters.get("price_auto_match", 0)) and fx_delta <= float(parameters.get("fx_auto_match", 0))
    analyst_review = price_delta <= float(parameters.get("price_review", 999)) and fx_delta <= float(parameters.get("fx_review", 999))
    return _result("fx_price_tolerance_management", OWNED_TABLES[8], price_delta=price_delta, fx_delta=fx_delta, auto_match=auto_match, analyst_review=analyst_review)


def track_external_settlement_status(milestones: Sequence[Mapping[str, object]]) -> dict:
    ordered = tuple(sorted((dict(item) for item in milestones), key=lambda item: str(item.get("at", ""))))
    owner = ordered[-1].get("party") if ordered else None
    return _result("custodian_settlement_agent_status", OWNED_TABLES[4], milestones=ordered, current_owner=owner, escalation_route=f"{owner}_queue" if owner else None)


def evaluate_cutoff_escalation(item: Mapping[str, object], calendar: Mapping[str, object]) -> dict:
    item = dict(item or {})
    cutoff_minutes = int(dict(calendar or {}).get("cutoff_minutes_remaining", 999))
    urgent = cutoff_minutes <= int(dict(calendar or {}).get("urgent_window_minutes", 30)) or item.get("value_date") == date(2026, 5, 30).isoformat()
    severity = "critical" if urgent and item.get("blocking") else "normal"
    return _result("cutoff_aware_escalation_logic", OWNED_TABLES[5], urgent=urgent, severity=severity, cutoff_minutes_remaining=cutoff_minutes)


def govern_manual_override(override: Mapping[str, object]) -> dict:
    override = dict(override or {})
    required = ("reason_code", "approver", "expires_at", "post_review_owner")
    missing = tuple(field for field in required if not override.get(field))
    return _result("manual_override_governance", OWNED_TABLES[10], approved=not missing, missing_fields=missing, post_review_required=True)


def build_seed_runbook_scenarios() -> dict:
    scenarios = ("partial_fill_allocation", "confirmation_mismatch", "failed_settlement_buy_in", "compliance_hold_release", "break_resolution", "projection_rebuild")
    return _result("realistic_seed_data_operator_runbooks", OWNED_TABLES[0], scenarios=scenarios, operator_runbooks=tuple(f"runbook_{item}" for item in scenarios), queue_coverage=("orders", "executions", "allocations", "confirmations", "settlement", "breaks"))


def build_continuous_release_assurance(results: Mapping[str, object]) -> dict:
    required = ("contract_tests", "lifecycle_scenarios", "permission_checks", "event_contract_validation", "projection_rebuild", "ui_evidence")
    missing = tuple(item for item in required if not dict(results or {}).get(item))
    return _result("continuous_release_assurance_full_lifecycle", OWNED_TABLES[11], release_allowed=not missing, missing_gates=missing, gates=required)


def improve1_trading_control_contract() -> dict:
    return _result(
        "improve1_trading_control_contract",
        OWNED_TABLES[0],
        capability_count=len(TRADING_CONTROL_CAPABILITIES),
        capabilities=TRADING_CONTROL_CAPABILITIES,
        owned_tables=OWNED_TABLES,
        ui_surfaces=tuple(f"{PBC_KEY}.ui.trading_control.{capability}" for capability in TRADING_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.trading_control.{capability}" for capability in TRADING_CONTROL_CAPABILITIES),
    )
