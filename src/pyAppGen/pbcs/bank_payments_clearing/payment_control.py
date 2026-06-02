"""Bank payment clearing control primitives for improve1 domain execution.

The functions in this module are deterministic and side-effect-free. They model
payments-specific controls, simulations, boundaries, workbench views, and agent
preview behavior without owning account, fraud, notification, treasury, FX, or
ledger tables.
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta
import hashlib
import json
from typing import Mapping, Sequence

PBC_KEY = "bank_payments_clearing"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "bank_payments_clearing_payment_instruction",
    "bank_payments_clearing_clearing_batch",
    "bank_payments_clearing_settlement_file",
    "bank_payments_clearing_return_item",
    "bank_payments_clearing_exception_case",
    "bank_payments_clearing_bank_reconciliation",
    "bank_payments_clearing_participant_bank",
    "bank_payments_clearing_bank_payments_clearing_control_assertion",
    "bank_payments_clearing_appgen_outbox_event",
)

PAYMENT_CONTROL_CAPABILITIES = (
    "payment_instruction_state_machine",
    "payment_rail_classification",
    "participant_bank_registry",
    "beneficiary_originator_validation",
    "limits_velocity_controls",
    "payment_screening_boundary",
    "clearing_batch_assembly",
    "cutoff_calendar_management",
    "settlement_file_generation",
    "settlement_acknowledgement_handling",
    "return_item_lifecycle",
    "exception_case_taxonomy",
    "repair_queue_workflow",
    "cancellation_recall_handling",
    "liquidity_settlement_funding_checks",
    "bank_reconciliation_matching",
    "nostro_internal_account_boundary",
    "fee_charge_evidence",
    "operational_risk_controls",
    "maker_checker_authorization",
    "payment_message_validation",
    "duplicate_payment_prevention",
    "real_time_payment_finality",
    "card_settlement_batch_support",
    "cross_border_payment_controls",
    "fx_rate_boundary",
    "customer_notification_events",
    "payment_operations_workbench",
    "agent_payment_investigation",
    "governed_agent_crud_commands",
    "participant_bank_health_monitoring",
    "clearing_window_forecast",
    "payment_volume_risk_analytics",
    "return_reason_trend_analysis",
    "reconciliation_break_aging",
    "payment_file_security_controls",
    "cyber_fraud_incident_boundary",
    "regulatory_reporting_triggers",
    "exception_root_cause_analytics",
    "replay_safe_idempotency",
    "dead_letter_retry_operations",
    "cryptographic_payment_evidence",
    "privacy_minimum_necessary_views",
    "configuration_impact_simulation",
    "seeded_payments_scenario_library",
    "role_based_permission_model",
    "settlement_close_finance_handoff",
    "full_payments_release_simulation",
    "package_overlap_guardrails",
    "composition_dsl_unified_agent_exposure",
)

VALID_TRANSITIONS = {
    "drafted": {"validated", "repair_required", "canceled"},
    "validated": {"screened", "approved", "repair_required", "canceled"},
    "screened": {"approved", "held", "repair_required"},
    "approved": {"released", "canceled"},
    "released": {"batched", "settled", "timeout_unknown", "recall_requested"},
    "batched": {"cleared", "returned", "reversed"},
    "cleared": {"settled", "returned"},
    "settled": {"reconciled", "returned", "archived"},
    "returned": {"repaired", "reversed", "reconciled"},
    "repaired": {"validated", "screened"},
    "timeout_unknown": {"settled", "rejected", "investigation_opened"},
    "reconciled": {"archived"},
}

RAIL_PROFILES = {
    "ach": {"format": "ach_batch", "limit": 100000.0, "requires_batch": True, "settlement_basis": "deferred_net", "cutoff": "17:00", "finality": "returnable"},
    "wire": {"format": "iso_20022_pacs008", "limit": 10000000.0, "requires_batch": False, "settlement_basis": "gross", "cutoff": "16:00", "finality": "near_final"},
    "instant": {"format": "iso_20022_instant", "limit": 25000.0, "requires_batch": False, "settlement_basis": "real_time_final", "cutoff": "24x7", "finality": "irrevocable"},
    "card_settlement": {"format": "card_scheme_cycle", "limit": 5000000.0, "requires_batch": True, "settlement_basis": "scheme_net", "cutoff": "23:00", "finality": "scheme_rules"},
    "cross_border": {"format": "iso_20022_cbpr", "limit": 1000000.0, "requires_batch": False, "settlement_basis": "correspondent", "cutoff": "15:00", "finality": "correspondent_dependent"},
}


def _tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _date(value: object | None) -> date:
    if value is None:
        return date(2026, 5, 30)
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    return date.fromisoformat(str(value)[:10])


def _result(capability: str, **payload: object) -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "capability": capability,
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
        **payload,
    }


def evaluate_payment_state_transition(current_state: str, target_state: str) -> dict:
    allowed = target_state in VALID_TRANSITIONS.get(current_state, set())
    return _result("payment_instruction_state_machine", table=OWNED_TABLES[0], current_state=current_state, target_state=target_state, allowed=allowed, evidence_event="BankPaymentsClearingUpdated" if allowed else "BankPaymentsClearingExceptionOpened")


def classify_payment_rail(instruction: Mapping[str, object]) -> dict:
    instruction = dict(instruction or {})
    profile = dict(RAIL_PROFILES.get(str(instruction.get("rail")), {}))
    amount = float(instruction.get("amount", 0))
    findings = []
    if not profile:
        findings.append("unsupported_rail")
    elif amount > profile["limit"]:
        findings.append("rail_limit_breach")
    if profile.get("requires_batch") and not instruction.get("effective_date"):
        findings.append("effective_date_required_for_batch_rail")
    return _result("payment_rail_classification", table=OWNED_TABLES[0], rail=instruction.get("rail"), rail_profile=profile, findings=tuple(findings), valid=not findings)


def evaluate_participant_bank(profile: Mapping[str, object], *, rail: str | None = None) -> dict:
    profile = dict(profile or {})
    supported = set(_tuple(profile.get("supported_rails")))
    active = profile.get("status", "active") == "active"
    supports_rail = rail is None or rail in supported
    return _result("participant_bank_registry", table=OWNED_TABLES[6], participant_bank_id=profile.get("participant_bank_id"), routable=active and supports_rail and bool(profile.get("routing_identifier")), status=profile.get("status", "active"), supports_rail=supports_rail, historical_transactions_preserved=True)


def validate_party_details(instruction: Mapping[str, object]) -> dict:
    instruction = dict(instruction or {})
    findings = []
    if not str(instruction.get("beneficiary_account", "")).isdigit():
        findings.append("beneficiary_account_format")
    if not instruction.get("beneficiary_name"):
        findings.append("beneficiary_name_required")
    if not instruction.get("originator_authorized"):
        findings.append("originator_not_authorized")
    if instruction.get("rail") == "cross_border" and not instruction.get("beneficiary_address"):
        findings.append("beneficiary_address_required")
    return _result("beneficiary_originator_validation", table=OWNED_TABLES[0], valid=not findings, findings=tuple(findings), repairable=bool(findings) and set(findings) <= {"beneficiary_account_format", "beneficiary_name_required", "beneficiary_address_required"})


def enforce_limits_velocity(instruction: Mapping[str, object], exposure: Mapping[str, object], limits: Mapping[str, object]) -> dict:
    amount = float(dict(instruction or {}).get("amount", 0))
    daily_used = float(dict(exposure or {}).get("daily_amount", 0))
    transaction_limit = float(dict(limits or {}).get("transaction_limit", amount + 1))
    daily_limit = float(dict(limits or {}).get("daily_limit", daily_used + amount + 1))
    breaches = []
    if amount > transaction_limit:
        breaches.append("transaction_limit_breach")
    if daily_used + amount > daily_limit:
        breaches.append("daily_velocity_breach")
    return _result("limits_velocity_controls", table=OWNED_TABLES[0], breaches=tuple(breaches), approval_tier="elevated" if breaches else "standard", override_required=bool(breaches))


def evaluate_screening_boundary(screening: Mapping[str, object], references: Sequence[str] = ()) -> dict:
    screening = dict(screening or {})
    direct_table_refs = tuple(ref for ref in references if ref.startswith(("sanctions_", "fraud_", "aml_")) and ref.endswith("table"))
    fresh = screening.get("freshness") in {"current", "same_day"}
    clear = screening.get("decision") == "clear"
    return _result("payment_screening_boundary", table=OWNED_TABLES[0], decision=screening.get("decision"), fresh=fresh, clear=clear, boundary_ok=not direct_table_refs, forbidden_references=direct_table_refs, hold_required=not fresh or not clear)


def assemble_batch_plan(instructions: Sequence[Mapping[str, object]], *, rail: str, participant_bank_id: str, finalized: bool = False) -> dict:
    if finalized:
        return _result("clearing_batch_assembly", table=OWNED_TABLES[1], can_add_items=False, reason="batch_finalized", item_count=0, total=0.0, hash_total=_digest(()))
    items = tuple(dict(item) for item in instructions if item.get("rail") == rail and item.get("participant_bank_id") == participant_bank_id and item.get("state", "released") == "released")
    total = round(sum(float(item.get("amount", 0)) for item in items), 2)
    return _result("clearing_batch_assembly", table=OWNED_TABLES[1], can_add_items=True, item_count=len(items), total=total, hash_total=_digest(tuple((item.get("instruction_id"), item.get("amount"), item.get("currency")) for item in items)), finalization_lock=bool(items))


def calculate_next_clearing_window(now: str, calendar: Mapping[str, object]) -> dict:
    calendar = dict(calendar or {})
    current = datetime.fromisoformat(now)
    if calendar.get("emergency_closure"):
        next_day = current.date() + timedelta(days=1)
        return _result("cutoff_calendar_management", table=OWNED_TABLES[1], eligible_now=False, next_window=datetime.combine(next_day, time(9, 0)).isoformat(), reason="emergency_closure")
    cutoff_text = str(calendar.get("cutoff", "17:00"))
    if cutoff_text == "24x7":
        return _result("cutoff_calendar_management", table=OWNED_TABLES[1], eligible_now=True, next_window=current.isoformat(), reason="always_open")
    cutoff_hour, cutoff_minute = (int(part) for part in cutoff_text.split(":", 1))
    cutoff = datetime.combine(current.date(), time(cutoff_hour, cutoff_minute))
    missed = current > cutoff or str(current.date()) in set(_tuple(calendar.get("holidays")))
    next_day = current.date() + timedelta(days=1) if missed else current.date()
    return _result("cutoff_calendar_management", table=OWNED_TABLES[1], eligible_now=not missed, next_window=datetime.combine(next_day, time(cutoff_hour, cutoff_minute)).isoformat(), reason="missed_cutoff" if missed else "current_window")


def build_settlement_file_control(batch: Mapping[str, object], *, sequence: int, encryption: Mapping[str, object] | None = None) -> dict:
    batch = dict(batch or {})
    content = {"batch_id": batch.get("batch_id"), "sequence": sequence, "item_count": batch.get("item_count", 0), "control_total": batch.get("total_amount", batch.get("total", 0)), "hash_total": batch.get("hash_total")}
    checksum = _digest(content)
    security = dict(encryption or {})
    return _result("settlement_file_generation", table=OWNED_TABLES[2], content=content, checksum=checksum, signature=f"appgen_payment_file_sig_{checksum[:20]}", transmission_ready=bool(security.get("encrypted", True) and security.get("signature", True)))


def process_acknowledgement_control(file_record: Mapping[str, object], acknowledgement: Mapping[str, object], seen_ack_ids: Sequence[str] = ()) -> dict:
    acknowledgement = dict(acknowledgement or {})
    duplicate = acknowledgement.get("acknowledgement_id") in set(seen_ack_ids)
    accepted = int(acknowledgement.get("accepted_count", 0))
    rejected = int(acknowledgement.get("rejected_count", 0))
    item_count = int(dict(file_record or {}).get("item_count", 0))
    ack_type = "duplicate" if duplicate else "accepted" if accepted == item_count and rejected == 0 else "partial" if accepted else "rejected"
    return _result("settlement_acknowledgement_handling", table=OWNED_TABLES[2], duplicate=duplicate, ack_type=ack_type, repair_required=ack_type in {"partial", "rejected"})


def process_return_lifecycle(return_item: Mapping[str, object], original_instruction: Mapping[str, object]) -> dict:
    reason = str(dict(return_item or {}).get("reason_code", "administrative"))
    repairable = reason in {"administrative", "closed_account"}
    late = reason == "late_return" or bool(dict(return_item or {}).get("late"))
    return _result("return_item_lifecycle", table=OWNED_TABLES[3], reason_code=reason, repair_eligible=repairable and not late, financial_impact=float(dict(original_instruction or {}).get("amount", 0)), notification_required=True, state="representment_ready" if repairable and not late else "reversal_required")


def route_exception_case(exception: Mapping[str, object]) -> dict:
    exception = dict(exception or {})
    taxonomy = {"validation": "repair_operations", "screening": "risk_operations", "liquidity": "treasury_coordination", "participant": "network_operations", "file": "clearing_operations", "acknowledgement": "clearing_operations", "return": "returns_operations", "reconciliation": "reconciliation_operations", "outage": "incident_operations"}
    kind = str(exception.get("exception_type", "validation"))
    return _result("exception_case_taxonomy", table=OWNED_TABLES[4], exception_type=kind, owner_queue=taxonomy.get(kind, "payment_operations"), closure_requires_evidence=True, severity=exception.get("severity", "medium"))


def plan_repair_workflow(original: Mapping[str, object], corrected: Mapping[str, object], approvals: Sequence[Mapping[str, object]]) -> dict:
    original = dict(original or {})
    corrected = dict(corrected or {})
    changed_fields = tuple(key for key, value in corrected.items() if original.get(key) != value)
    approvers = {item.get("role") for item in approvals}
    material = any(field in {"amount", "beneficiary_account", "currency", "participant_bank_id"} for field in changed_fields)
    dual_ok = not material or {"maker", "checker"} <= approvers
    return _result("repair_queue_workflow", table=OWNED_TABLES[0], changed_fields=changed_fields, material_repair=material, dual_approval_satisfied=dual_ok, rescreening_required=bool(changed_fields))


def evaluate_cancellation_recall(instruction: Mapping[str, object], participant_response: Mapping[str, object] | None = None) -> dict:
    state = dict(instruction or {}).get("state")
    if state in {"drafted", "validated", "approved"}:
        outcome = "cancellable"
    elif state in {"released", "batched", "cleared"}:
        outcome = "recall_only"
    elif state in {"settled", "reconciled"}:
        outcome = "too_late"
    else:
        outcome = "manual_review"
    if dict(participant_response or {}).get("response") == "rejected":
        outcome = "participant_rejected"
    return _result("cancellation_recall_handling", table=OWNED_TABLES[0], outcome=outcome, customer_communication_required=True)


def evaluate_liquidity_funding(instruction_or_batch: Mapping[str, object], liquidity: Mapping[str, object]) -> dict:
    amount = float(dict(instruction_or_batch or {}).get("amount", dict(instruction_or_batch or {}).get("total_amount", 0)))
    available = float(dict(liquidity or {}).get("available", 0))
    buffer = float(dict(liquidity or {}).get("buffer", 0))
    fresh = dict(liquidity or {}).get("freshness") in {"current", "same_day", None}
    hold = available < amount + buffer or not fresh
    return _result("liquidity_settlement_funding_checks", table=OWNED_TABLES[1], hold=hold, freshness_ok=fresh, available=available, required=amount + buffer)


def match_bank_reconciliation(instructions: Sequence[Mapping[str, object]], statement_lines: Sequence[Mapping[str, object]], tolerance: float = 0.01) -> dict:
    by_ref = {item.get("external_reference"): dict(item) for item in instructions}
    matches = []
    breaks = []
    fees = []
    for line in statement_lines:
        line = dict(line)
        if line.get("line_type") == "fee":
            fees.append(line)
            continue
        instruction = by_ref.get(line.get("external_reference"))
        if not instruction:
            breaks.append({"line": line, "reason": "unmatched_statement_line"})
            continue
        delta = abs(float(line.get("amount", 0)) - float(instruction.get("amount", 0)))
        matches.append({"instruction_id": instruction.get("instruction_id"), "match_type": "one_to_one" if delta <= tolerance else "amount_variance", "delta": round(delta, 2)})
        if delta > tolerance:
            breaks.append({"line": line, "reason": "amount_variance"})
    return _result("bank_reconciliation_matching", table=OWNED_TABLES[5], matches=tuple(matches), fees=tuple(fees), breaks=tuple(breaks), reconciled=not breaks)


def validate_account_projection_boundary(references: Sequence[str]) -> dict:
    forbidden = tuple(ref for ref in references if ref.startswith(("gl_", "ledger_", "core_account_", "nostro_")) and ref.endswith("table"))
    return _result("nostro_internal_account_boundary", table=OWNED_TABLES[5], boundary_ok=not forbidden, forbidden_references=forbidden, projection_sources=("balance_projection_api", "statement_projection_event"))


def build_fee_charge_evidence(fees: Sequence[Mapping[str, object]]) -> dict:
    fees = tuple(dict(item) for item in fees)
    explicit = tuple(item for item in fees if item.get("fee_type") != "deducted")
    deducted = tuple(item for item in fees if item.get("fee_type") == "deducted")
    return _result("fee_charge_evidence", table=OWNED_TABLES[5], explicit_fees=explicit, deducted_fees=deducted, billing_event_required=bool(fees), mutates_billing_tables=False)


def evaluate_operational_risk_controls(population: Sequence[Mapping[str, object]], thresholds: Mapping[str, object]) -> dict:
    population = tuple(dict(item) for item in population)
    failures = []
    if sum(1 for item in population if item.get("maker") == item.get("checker")) > int(dict(thresholds or {}).get("maker_checker_conflicts", 0)):
        failures.append("maker_checker_conflict_population")
    if sum(1 for item in population if item.get("state") == "breaks_open") > int(dict(thresholds or {}).get("reconciliation_breaks", 0)):
        failures.append("reconciliation_break_threshold")
    return _result("operational_risk_controls", table=OWNED_TABLES[7], failures=tuple(failures), remediation_required=bool(failures))


def enforce_maker_checker(command: Mapping[str, object], actor_roles: Sequence[str]) -> dict:
    command = dict(command or {})
    conflict = command.get("maker") == command.get("checker")
    authorized = command.get("required_role", "approver") in set(actor_roles)
    return _result("maker_checker_authorization", table=OWNED_TABLES[0], allowed=not conflict and authorized, conflict=conflict, authorized=authorized, emergency_override_required=conflict or not authorized)


def validate_payment_message(message: Mapping[str, object], schema: Mapping[str, object]) -> dict:
    message = dict(message or {})
    required = tuple(dict(schema or {}).get("required_fields") or ())
    missing = tuple(field for field in required if not message.get(field))
    conditional = tuple(rule for rule in _tuple(dict(schema or {}).get("conditional_rules")) if rule.get("when") in message and not message.get(rule.get("then")))
    return _result("payment_message_validation", table=OWNED_TABLES[0], missing_fields=missing, conditional_failures=conditional, valid=not missing and not conditional, schema_version=dict(schema or {}).get("version"))


def score_duplicate_payment(instruction: Mapping[str, object], history: Sequence[Mapping[str, object]]) -> dict:
    instruction = dict(instruction or {})
    matches = []
    near = []
    for item in history:
        item = dict(item)
        exact = all(item.get(field) == instruction.get(field) for field in ("originator_id", "beneficiary_account", "amount", "currency", "value_date", "purpose", "external_reference"))
        similar = sum(item.get(field) == instruction.get(field) for field in ("beneficiary_account", "amount", "currency", "value_date")) >= 3
        if exact:
            matches.append(item)
        elif similar:
            near.append(item)
    return _result("duplicate_payment_prevention", table=OWNED_TABLES[0], exact_duplicates=tuple(matches), near_duplicates=tuple(near), block_release=bool(matches), review_required=bool(near))


def evaluate_realtime_finality(instruction: Mapping[str, object], network_response: Mapping[str, object]) -> dict:
    response = dict(network_response or {})
    status = response.get("status")
    if status == "accepted":
        finality_state = "final"
    elif status == "timeout":
        finality_state = "timeout_unknown"
    elif status == "late_confirmation":
        finality_state = "resolved_after_timeout"
    else:
        finality_state = "rejected"
    return _result("real_time_payment_finality", table=OWNED_TABLES[0], finality_state=finality_state, retry_allowed=finality_state == "rejected", customer_message_required=True)


def reconcile_card_settlement_cycle(cycle: Mapping[str, object]) -> dict:
    cycle = dict(cycle or {})
    presentments = float(cycle.get("presentment_total", 0))
    fees = float(cycle.get("interchange", 0)) + float(cycle.get("scheme_fees", 0))
    expected = round(presentments - fees - float(cycle.get("chargebacks", 0)), 2)
    variance = round(float(cycle.get("settlement_amount", 0)) - expected, 2)
    return _result("card_settlement_batch_support", table=OWNED_TABLES[1], expected_settlement=expected, variance=variance, chargeback_link_required=variance != 0)


def evaluate_cross_border_controls(instruction: Mapping[str, object]) -> dict:
    instruction = dict(instruction or {})
    required = ("correspondent_chain", "purpose_code", "charge_bearer", "country", "regulatory_report_flag")
    missing = tuple(field for field in required if not instruction.get(field))
    return _result("cross_border_payment_controls", table=OWNED_TABLES[0], missing_fields=missing, valid=not missing, owns_fx_tables=False, owns_compliance_tables=False)


def evaluate_fx_projection(fx_quote: Mapping[str, object], as_of: object | None = None) -> dict:
    quote = dict(fx_quote or {})
    expiry = datetime.fromisoformat(str(quote.get("expiry", "2026-05-30T23:59:00")))
    now = datetime.fromisoformat(str(as_of or "2026-05-30T12:00:00"))
    stale = expiry < now or quote.get("freshness") == "stale"
    return _result("fx_rate_boundary", table=OWNED_TABLES[0], stale=stale, block_payment=stale, quote_reference=quote.get("quote_id"), mutates_rate_tables=False)


def build_notification_event(payment: Mapping[str, object], notification_type: str) -> dict:
    event = {"event_type": "CustomerNotificationRequested", "contract": EVENT_CONTRACT, "payload": {"payment_id": dict(payment or {}).get("instruction_id"), "template": notification_type, "recipient_projection": dict(payment or {}).get("recipient_projection"), "deadline": dict(payment or {}).get("notification_deadline")}}
    return _result("customer_notification_events", table=OWNED_TABLES[8], event=event, mutates_notification_tables=False)


def build_operations_workbench_queues(items: Sequence[Mapping[str, object]]) -> dict:
    items = tuple(dict(item) for item in items)
    queues = {
        "validation_fails": tuple(item for item in items if item.get("state") == "repair_required"),
        "screening_holds": tuple(item for item in items if item.get("screening_decision") == "hold"),
        "pending_approvals": tuple(item for item in items if item.get("state") == "validated"),
        "cutoff_risk": tuple(item for item in items if item.get("cutoff_risk")),
        "returns": tuple(item for item in items if item.get("state") == "returned"),
        "reconciliation_breaks": tuple(item for item in items if item.get("state") == "breaks_open"),
    }
    return _result("payment_operations_workbench", table=OWNED_TABLES[0], queues=queues, permission_aware_actions=True)


def build_payment_investigation_summary(payment: Mapping[str, object], evidence: Sequence[Mapping[str, object]]) -> dict:
    evidence = tuple(dict(item) for item in evidence)
    return _result("agent_payment_investigation", table=OWNED_TABLES[0], summary={"payment_id": dict(payment or {}).get("instruction_id"), "state": dict(payment or {}).get("state"), "evidence_count": len(evidence)}, citations=tuple(item.get("evidence_id") for item in evidence if item.get("evidence_id")), requires_confirmation_for_mutation=True)


def plan_governed_agent_command(action: str, payment_identity: Mapping[str, object], actor: Mapping[str, object]) -> dict:
    required = ("payment_id", "action", "evidence", "preview", "confirmation", "authority")
    payload = {"payment_id": dict(payment_identity or {}).get("payment_id"), "action": action, "evidence": dict(payment_identity or {}).get("evidence"), "preview": True, "confirmation": dict(payment_identity or {}).get("confirmation"), "authority": dict(actor or {}).get("authority")}
    missing = tuple(field for field in required if not payload.get(field))
    return _result("governed_agent_crud_commands", table=OWNED_TABLES[0], command_preview=payload, missing_requirements=missing, executable=not missing, requires_human_confirmation=True)


def evaluate_participant_health(health: Mapping[str, object]) -> dict:
    health = dict(health or {})
    outage = health.get("outage_state") in {"degraded", "down"}
    reject_rate = float(health.get("reject_rate", 0))
    latency = float(health.get("ack_latency_minutes", 0))
    route_hold = outage or reject_rate > 0.05 or latency > 30
    reasons = tuple(reason for reason, active in (("participant_outage", outage), ("high_reject_rate", reject_rate > 0.05), ("ack_latency", latency > 30)) if active)
    return _result("participant_bank_health_monitoring", table=OWNED_TABLES[6], route_hold=route_hold, health_reasons=reasons, fallback_rule=health.get("fallback_rule"))


def forecast_clearing_window_risk(inputs: Mapping[str, object]) -> dict:
    inputs = dict(inputs or {})
    risk_score = min(1.0, 0.1 * int(inputs.get("pending_items", 0)) + 0.15 * int(inputs.get("approval_backlog", 0)) + 0.2 * int(inputs.get("screening_holds", 0)) + (0.4 if inputs.get("liquidity_shortage") else 0))
    return _result("clearing_window_forecast", table=OWNED_TABLES[1], risk_score=round(risk_score, 2), cutoff_risk=risk_score >= 0.7, explanations=tuple(key for key, value in inputs.items() if value))


def compute_payment_risk_analytics(payments: Sequence[Mapping[str, object]]) -> dict:
    payments = tuple(dict(item) for item in payments)
    by_rail: dict[str, int] = {}
    total_value = 0.0
    exceptions = 0
    for item in payments:
        by_rail[str(item.get("rail", "unknown"))] = by_rail.get(str(item.get("rail", "unknown")), 0) + 1
        total_value += float(item.get("amount", 0))
        exceptions += int(bool(item.get("exception_type")))
    return _result("payment_volume_risk_analytics", table=OWNED_TABLES[0], by_rail=by_rail, total_value=round(total_value, 2), exception_count=exceptions, drilldowns=tuple(item.get("instruction_id") for item in payments if item.get("exception_type")))


def analyze_return_reason_trends(returns: Sequence[Mapping[str, object]], threshold: int = 2) -> dict:
    counts: dict[str, int] = {}
    for item in returns:
        reason = str(dict(item).get("reason_code", "unknown"))
        counts[reason] = counts.get(reason, 0) + 1
    prevention = tuple({"reason_code": reason, "task": "open_prevention_task"} for reason, count in counts.items() if count >= threshold and reason in {"administrative", "closed_account"})
    return _result("return_reason_trend_analysis", table=OWNED_TABLES[3], trends=counts, prevention_tasks=prevention)


def age_reconciliation_breaks(breaks: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _date(as_of)
    aged = []
    escalations = []
    for item in breaks:
        item = dict(item)
        age = (today - _date(item.get("opened_date"))).days
        bucket = "0-2" if age <= 2 else "3-7" if age <= 7 else "8+"
        record = {**item, "age_days": age, "bucket": bucket}
        aged.append(record)
        if age > 7 and float(item.get("amount", 0)) > 1000:
            escalations.append(record)
    return _result("reconciliation_break_aging", table=OWNED_TABLES[5], aged_breaks=tuple(aged), escalations=tuple(escalations), closure_requires_match_or_writeoff=True)


def evaluate_file_security_controls(file_record: Mapping[str, object]) -> dict:
    file_record = dict(file_record or {})
    missing = tuple(field for field in ("encrypted", "signature", "key_version", "checksum", "transmission_endpoint") if not file_record.get(field))
    return _result("payment_file_security_controls", table=OWNED_TABLES[2], missing_security_evidence=missing, transmission_blocked=bool(missing))


def build_investigation_boundary_event(payment: Mapping[str, object], indicators: Sequence[str]) -> dict:
    event = {"event_type": "PaymentInvestigationRequested", "contract": EVENT_CONTRACT, "payload": {"payment_id": dict(payment or {}).get("instruction_id"), "risk_indicators": tuple(indicators), "hold_state": dict(payment or {}).get("state")}}
    return _result("cyber_fraud_incident_boundary", table=OWNED_TABLES[8], event=event, mutates_fraud_tables=False, mutates_cyber_tables=False)


def create_regulatory_report_candidate(payment: Mapping[str, object]) -> dict:
    payment = dict(payment or {})
    trigger = float(payment.get("amount", 0)) >= 10000 or payment.get("cross_border") or payment.get("incident")
    report_type = "cross_border_value_report" if payment.get("cross_border") else "large_value_report" if float(payment.get("amount", 0)) >= 10000 else "incident_report"
    return _result("regulatory_reporting_triggers", table=OWNED_TABLES[4], report_required=bool(trigger), report_type=report_type if trigger else None, deadline="T+1" if trigger else None, correction_history=tuple(payment.get("report_corrections") or ()))


def analyze_exception_root_causes(exceptions: Sequence[Mapping[str, object]]) -> dict:
    categories: dict[str, int] = {}
    for item in exceptions:
        category = str(dict(item).get("root_cause", dict(item).get("exception_type", "operator_action")))
        categories[category] = categories.get(category, 0) + 1
    remediation = tuple({"root_cause": key, "task": "open_remediation"} for key, count in categories.items() if count >= 2)
    return _result("exception_root_cause_analytics", table=OWNED_TABLES[4], root_causes=categories, remediation_tasks=remediation)


def apply_idempotency_guard(operation: str, payload: Mapping[str, object], seen_keys: Sequence[str]) -> dict:
    key = _digest((operation, payload))
    duplicate = key in set(seen_keys)
    return _result("replay_safe_idempotency", table=OWNED_TABLES[8], idempotency_key=key, duplicate=duplicate, financial_outcome_changed=not duplicate)


def plan_dead_letter_retry(dead_letter: Mapping[str, object]) -> dict:
    dead_letter = dict(dead_letter or {})
    retry_count = int(dead_letter.get("retry_count", 0))
    manual_gate = retry_count >= int(dead_letter.get("max_attempts", 3)) or dead_letter.get("risk") == "high"
    return _result("dead_letter_retry_operations", table="bank_payments_clearing_appgen_dead_letter_event", retry_allowed=not manual_gate, manual_release_gate=manual_gate, replay_checkpoint=dead_letter.get("checkpoint"))


def build_payment_proof_chain(events: Sequence[Mapping[str, object]]) -> dict:
    chain = []
    previous = "GENESIS"
    for event in events:
        event = dict(event)
        digest = _digest({"previous": previous, "event": event})
        chain.append({"event_id": event.get("event_id"), "previous_hash": previous, "hash": digest})
        previous = digest
    return _result("cryptographic_payment_evidence", table=OWNED_TABLES[8], proof_chain=tuple(chain), terminal_hash=previous, tamper_evident=bool(chain))


def apply_privacy_view(record: Mapping[str, object], role: str) -> dict:
    record = dict(record or {})
    sensitive = {"beneficiary_account", "screening_evidence", "originator_account", "beneficiary_address"}
    allowed_sensitive = role in {"investigator", "auditor"}
    view = {key: (value if allowed_sensitive or key not in sensitive else "REDACTED") for key, value in record.items()}
    return _result("privacy_minimum_necessary_views", table=OWNED_TABLES[0], role=role, view=view, redacted_fields=tuple(key for key in sensitive if key in record and not allowed_sensitive))


def simulate_configuration_impact(change: Mapping[str, object], recent_items: Sequence[Mapping[str, object]]) -> dict:
    change = dict(change or {})
    impacted = []
    for item in recent_items:
        item = dict(item)
        if change.get("parameter") == "transaction_limit" and float(item.get("amount", 0)) > float(change.get("new_value", 0)):
            impacted.append({"item_id": item.get("instruction_id"), "impact": "would_breach_new_limit"})
        if change.get("parameter") == "participant_status" and item.get("participant_bank_id") == change.get("participant_bank_id"):
            impacted.append({"item_id": item.get("instruction_id"), "impact": "participant_status_change"})
    return _result("configuration_impact_simulation", table=OWNED_TABLES[7], impacted_items=tuple(impacted), activation_requires_review=bool(impacted))


def seeded_payments_scenario_library() -> dict:
    scenarios = ("clean_batch_payment", "wire_approval", "instant_payment_timeout", "screening_hold", "return_item", "file_reject", "reconciliation_break", "recall", "stale_liquidity_projection")
    return _result("seeded_payments_scenario_library", table=OWNED_TABLES[0], scenarios=scenarios, expected_queues=("repair", "returns", "reconciliation_breaks", "cutoff_risk"))


def evaluate_role_permission(command: str, actor: Mapping[str, object]) -> dict:
    role_grants = {
        "operator": {"create", "repair", "open_exception"},
        "approver": {"approve", "release", "recall"},
        "reconciliation_user": {"close_reconciliation_break"},
        "auditor": {"read"},
        "admin": {"create", "repair", "approve", "release", "cancel", "recall", "process_return", "close_exception", "transmit_file", "close_reconciliation_break"},
    }
    roles = set(_tuple(dict(actor or {}).get("roles")))
    allowed = any(command in role_grants.get(role, set()) for role in roles)
    return _result("role_based_permission_model", table=OWNED_TABLES[7], command=command, allowed=allowed, disabled_ui_action=not allowed)


def build_finance_handoff_events(settlement: Mapping[str, object]) -> dict:
    settlement = dict(settlement or {})
    event_types = ("SettlementClosed", "PaymentFeeAccrued", "PaymentReturnPosted", "ReconciliationBreakOpened")
    events = tuple({"event_type": event_type, "contract": EVENT_CONTRACT, "idempotency_key": _digest((event_type, settlement.get("settlement_id"))), "evidence_reference": settlement.get("evidence_reference")} for event_type in event_types)
    return _result("settlement_close_finance_handoff", table=OWNED_TABLES[8], events=events, mutates_finance_tables=False, replay_safe=True)


def run_full_payments_release_simulation() -> dict:
    instruction = {"instruction_id": "PAY-SIM", "rail": "ach", "participant_bank_id": "BANK-A", "amount": 1250.0, "currency": "USD", "beneficiary_account": "123456789", "beneficiary_name": "Supplier", "originator_authorized": True, "external_reference": "EXT-SIM", "screening_evidence": {"decision": "clear", "freshness": "current"}, "state": "released"}
    participant = evaluate_participant_bank({"participant_bank_id": "BANK-A", "routing_identifier": "021000021", "supported_rails": ("ach",), "status": "active"}, rail="ach")
    validation = validate_party_details(instruction)
    rail = classify_payment_rail({**instruction, "effective_date": "2026-05-30"})
    release = enforce_maker_checker({"maker": "maker", "checker": "checker", "required_role": "approver"}, ("approver",))
    batch = assemble_batch_plan((instruction,), rail="ach", participant_bank_id="BANK-A")
    file_control = build_settlement_file_control({"batch_id": "BATCH-SIM", "item_count": 1, "total_amount": 1250.0, "hash_total": batch["hash_total"]}, sequence=1, encryption={"encrypted": True, "signature": True})
    ack = process_acknowledgement_control({"item_count": 1}, {"acknowledgement_id": "ACK-SIM", "accepted_count": 1, "rejected_count": 0})
    recon = match_bank_reconciliation((instruction,), ({"external_reference": "EXT-SIM", "amount": 1250.0},))
    workbench = build_operations_workbench_queues((instruction,))
    checks = (participant, validation, rail, release, batch, file_control, ack, recon, workbench)
    return _result("full_payments_release_simulation", table=OWNED_TABLES[0], checks=checks, complete=all(item["ok"] for item in checks) and recon["reconciled"], emitted_events=("BankPaymentsClearingCreated", "BankPaymentsClearingApproved", "SettlementClosed"))


def evaluate_overlap_guardrails(references: Sequence[str]) -> dict:
    banned_prefixes = ("core_accounts_", "fraud_", "treasury_", "notification_", "regulatory_reporting_", "gl_")
    forbidden = tuple(ref for ref in references if ref.startswith(banned_prefixes) and ref.endswith("table"))
    declared = ("account_balance_projection_api", "screening_decision_event", "fx_quote_projection_api", "liquidity_projection_event", "customer_notification_requested_event", "finance_handoff_event", "audit_event_sealed")
    return _result("package_overlap_guardrails", table=OWNED_TABLES[0], ok=not forbidden, forbidden_references=forbidden, declared_dependencies=declared)


def build_composition_dsl_agent_exposure() -> dict:
    dsl = {
        "pbc": PBC_KEY,
        "models": OWNED_TABLES[:7],
        "routes": ("POST /payment-instructions", "POST /clearing-batches", "POST /settlement-files", "POST /return-items", "GET /bank-payments-clearing-workbench"),
        "services": ("create_validated_payment_instruction", "release_payment_instruction", "assemble_clearing_batch", "reconcile_bank_statement"),
        "ui_fragments": ("BankPaymentsClearingWorkbench", "PaymentInstructionReleaseConsole", "ReturnAndReconciliationWorkbench"),
        "agent_skills": ("payment_status_summary", "return_explanation", "repair_recommendation", "reconciliation_break_analysis", "cutoff_impact_summary"),
        "event_contract": EVENT_CONTRACT,
        "stream_engine_picker_visible": False,
    }
    return _result("composition_dsl_unified_agent_exposure", table=OWNED_TABLES[0], dsl=dsl, generated_app_ready=True)


def improve1_payment_control_contract() -> dict:
    return _result(
        "improve1_payment_control_contract",
        table=OWNED_TABLES[0],
        capability_count=len(PAYMENT_CONTROL_CAPABILITIES),
        capabilities=PAYMENT_CONTROL_CAPABILITIES,
        owned_tables=OWNED_TABLES,
        ui_surfaces=tuple(f"{PBC_KEY}.ui.payment_control.{capability}" for capability in PAYMENT_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.payment_control.{capability}" for capability in PAYMENT_CONTROL_CAPABILITIES),
    )
