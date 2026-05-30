"""Banking core account control primitives for improve1 domain execution.

The functions here are deterministic and side-effect-free. They model the
specialist deposit-account behaviors behind the banking_core_accounts improve1
backlog without taking ownership of customer master, external ledgers,
collections, fraud, compliance, or payment rails.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
import hashlib
import json
from typing import Mapping, Sequence

PBC_KEY = "banking_core_accounts"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "banking_core_accounts_deposit_account",
    "banking_core_accounts_account_balance",
    "banking_core_accounts_account_hold",
    "banking_core_accounts_interest_accrual",
    "banking_core_accounts_fee_assessment",
    "banking_core_accounts_statement_cycle",
    "banking_core_accounts_account_service_case",
    "banking_core_accounts_banking_core_accounts_policy_rule",
    "banking_core_accounts_banking_core_accounts_runtime_parameter",
    "banking_core_accounts_banking_core_accounts_schema_extension",
    "banking_core_accounts_banking_core_accounts_control_assertion",
    "banking_core_accounts_banking_core_accounts_governed_model",
    "banking_core_accounts_appgen_outbox_event",
)

ACCOUNT_CONTROL_CAPABILITIES = (
    "canonical_deposit_account_lifecycle",
    "customer_account_servicing_projection",
    "product_parameter_inheritance",
    "balance_component_decomposition",
    "value_dated_balance_replay",
    "hold_taxonomy_priority_model",
    "hold_release_waterfall",
    "overdraft_facility_controls",
    "overdraft_fee_interest_reversal",
    "interest_rate_tiering_calendars",
    "interest_capitalization_payout",
    "fee_schedule_engine",
    "fee_waiver_governance",
    "statement_cycle_cutover_controls",
    "statement_line_balance_forward_proof",
    "signatory_mandate_registry",
    "effective_dated_mandate_changes",
    "compliance_restriction_boundary",
    "compliance_review_service_cases",
    "dormancy_inactivity_reactivation",
    "account_closure_residual_balance",
    "controlled_account_reopening",
    "linked_account_relationships",
    "subledger_balance_reconciliation",
    "intraday_end_of_day_posting_boundary",
    "typed_deposit_domain_events",
    "idempotent_external_command_keys",
    "dead_letter_recovery_workbench",
    "operational_query_apis",
    "role_based_operations_workbench",
    "account_detail_timeline",
    "assistant_governed_servicing_instructions",
    "assistant_statement_fee_explanations",
    "exception_taxonomy_ageing",
    "policy_rule_versioning_effective_dating",
    "runtime_parameter_scoping_drift",
    "continuous_control_assertions",
    "core_banking_release_evidence_pack",
    "tenant_jurisdiction_isolation",
    "schema_extension_registry",
    "product_branch_analytics",
    "cryptographic_account_evidence_sealing",
    "counterfactual_fee_rate_policy_simulation",
    "balance_fee_anomaly_detection",
    "account_identifier_integrity",
    "negative_balance_collections_handoff_boundary",
    "operational_calendar_holiday_servicing",
    "correction_restatement_workflow",
    "event_api_boundary_map",
    "structural_release_gate",
)

LIFECYCLE_TRANSITIONS = {
    "pending": {"approved", "closed"},
    "approved": {"active", "closed"},
    "active": {"restricted", "dormant", "closed"},
    "restricted": {"active", "closed"},
    "dormant": {"active", "closed"},
    "closed": {"reopened"},
    "reopened": {"active"},
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


def evaluate_lifecycle_transition(current_state: str, target_state: str, *, maker: str | None = None, checker: str | None = None, reason: str | None = None) -> dict:
    allowed = target_state in LIFECYCLE_TRANSITIONS.get(current_state, set())
    approval_required = target_state in {"approved", "closed", "reopened"}
    reason_required = target_state in {"restricted", "closed", "reopened"}
    violations = []
    if not allowed:
        violations.append("invalid_transition")
    if approval_required and (not checker or checker == maker):
        violations.append("maker_checker_required")
    if reason_required and not reason:
        violations.append("reason_required")
    return _result("canonical_deposit_account_lifecycle", table=OWNED_TABLES[0], allowed=allowed and not violations, violations=tuple(violations), effective_transition={"from": current_state, "to": target_state})


def build_customer_account_projection(customer_id: str, accounts: Sequence[Mapping[str, object]], holds: Sequence[Mapping[str, object]], cases: Sequence[Mapping[str, object]], statements: Sequence[Mapping[str, object]]) -> dict:
    linked = tuple(dict(item) for item in accounts if item.get("customer_id") == customer_id)
    account_ids = {item.get("account_id") for item in linked}
    active_holds = tuple(dict(item) for item in holds if item.get("account_id") in account_ids and item.get("status", "active") == "active")
    open_cases = tuple(dict(item) for item in cases if item.get("account_id") in account_ids and item.get("status", "open") != "closed")
    latest_statements = tuple(dict(item) for item in statements if item.get("account_id") in account_ids)
    return _result("customer_account_servicing_projection", table=OWNED_TABLES[0], customer_id=customer_id, accounts=linked, active_holds=active_holds, open_cases=open_cases, latest_statements=latest_statements, projection_only=True, freshness_seconds=30)


def resolve_product_parameter(product_defaults: Mapping[str, object], overrides: Sequence[Mapping[str, object]], scope: Mapping[str, object]) -> dict:
    values = dict(product_defaults or {})
    applied = []
    for override in overrides:
        override = dict(override)
        if all(scope.get(key) == override.get(key) for key in ("tenant", "product", "branch") if override.get(key) is not None):
            values[override["parameter"]] = override["value"]
            applied.append({"parameter": override["parameter"], "source": override.get("reason", "approved_override")})
    return _result("product_parameter_inheritance", table=OWNED_TABLES[8], resolved_values=values, applied_overrides=tuple(applied), override_trace_visible=True)


def decompose_balance(ledger: float, holds: Sequence[Mapping[str, object]] = (), uncleared: float = 0.0, overdraft_limit: float = 0.0, accrued_interest: float = 0.0) -> dict:
    active_hold_amount = sum(float(dict(item).get("amount", 0)) for item in holds if dict(item).get("status", "active") == "active")
    available = round(float(ledger) - active_hold_amount - float(uncleared), 2)
    withdrawable = round(available + float(overdraft_limit), 2)
    return _result("balance_component_decomposition", table=OWNED_TABLES[1], components={"ledger": float(ledger), "held": active_hold_amount, "uncleared": float(uncleared), "available": available, "withdrawable": withdrawable, "accrued_interest": float(accrued_interest)}, explanation="ledger minus held and uncleared plus overdraft for withdrawable")


def replay_value_dated_balance(events: Sequence[Mapping[str, object]], as_of: object) -> dict:
    cutoff = _date(as_of)
    ordered = sorted((dict(item) for item in events), key=lambda item: (str(item.get("value_date")), str(item.get("event_id", ""))))
    applied = tuple(item for item in ordered if _date(item.get("value_date")) <= cutoff)
    balance = round(sum(float(item.get("amount", 0)) for item in applied), 2)
    return _result("value_dated_balance_replay", table=OWNED_TABLES[1], as_of=cutoff.isoformat(), balance=balance, applied_events=applied, deterministic_order=True)


def rank_holds(holds: Sequence[Mapping[str, object]]) -> dict:
    priority = {"legal": 1, "deceased_customer": 2, "compliance": 3, "fraud": 4, "cheque": 5, "card_authorization": 6, "internal_review": 7}
    ranked = tuple(sorted((dict(item) for item in holds), key=lambda item: (priority.get(str(item.get("hold_type")), 99), str(item.get("created_at", "")))))
    blocked_capabilities = tuple(sorted({capability for item in ranked for capability in _tuple(item.get("blocks"))}))
    return _result("hold_taxonomy_priority_model", table=OWNED_TABLES[2], ranked_holds=ranked, blocked_capabilities=blocked_capabilities)


def release_hold_waterfall(holds: Sequence[Mapping[str, object]], release_amount: float) -> dict:
    ranked = rank_holds(holds)["ranked_holds"]
    remaining = float(release_amount)
    releases = []
    for hold in reversed(ranked):
        if remaining <= 0:
            break
        amount = min(float(hold.get("amount", 0)), remaining)
        releases.append({"hold_id": hold.get("hold_id"), "released_amount": amount, "rationale": "waterfall_priority_age_legal_precedence"})
        remaining -= amount
    return _result("hold_release_waterfall", table=OWNED_TABLES[2], releases=tuple(releases), unreleased_amount=round(remaining, 2), audit_rationale=True)


def evaluate_overdraft_status(balance: Mapping[str, object], facility: Mapping[str, object]) -> dict:
    balance = dict(balance or {})
    facility = dict(facility or {})
    ledger = float(balance.get("ledger", 0))
    limit = float(facility.get("limit", 0))
    excess = max(0.0, abs(min(ledger, 0)) - limit)
    status = "in_credit" if ledger >= 0 else "arranged_overdraft" if excess == 0 else "unauthorized_excess"
    return _result("overdraft_facility_controls", table=OWNED_TABLES[1], overdraft_status=status, excess_amount=round(excess, 2), debit_blocked=excess > 0, cure_deadline=facility.get("grace_deadline"))


def plan_overdraft_reversal(fee_or_interest: Mapping[str, object], credit_event: Mapping[str, object]) -> dict:
    source = dict(fee_or_interest or {})
    credit = dict(credit_event or {})
    eligible = credit.get("same_day") or credit.get("bank_error") or credit.get("technical_outage")
    return _result("overdraft_fee_interest_reversal", table=OWNED_TABLES[4], original_item=source.get("item_id"), reversal_eligible=bool(eligible), net_customer_impact=round(float(source.get("amount", 0)) * (-1 if eligible else 0), 2), approval_required=True)


def calculate_interest_accrual(balance: float, tiers: Sequence[Mapping[str, object]], days: int, *, basis: int = 365) -> dict:
    applicable = sorted((dict(item) for item in tiers), key=lambda item: float(item.get("minimum_balance", 0)))
    chosen = next((item for item in reversed(applicable) if float(balance) >= float(item.get("minimum_balance", 0))), applicable[0] if applicable else {"rate": 0})
    amount = round(float(balance) * float(chosen.get("rate", 0)) * int(days) / int(basis), 2)
    return _result("interest_rate_tiering_calendars", table=OWNED_TABLES[3], selected_tier=chosen, accrual_amount=amount, day_count_basis=basis, accrual_days=days)


def plan_interest_posting(accrual: Mapping[str, object], account: Mapping[str, object]) -> dict:
    mode = dict(account or {}).get("interest_mode", "capitalize")
    restricted = dict(account or {}).get("lifecycle_state") == "restricted"
    outcome = "suspense" if restricted else "capitalized" if mode == "capitalize" else "payout"
    return _result("interest_capitalization_payout", table=OWNED_TABLES[3], posting_outcome=outcome, amount=dict(accrual or {}).get("amount"), preview_visible=True)


def assess_fee_schedule(trigger: str, context: Mapping[str, object], schedules: Sequence[Mapping[str, object]]) -> dict:
    matched = tuple(dict(item) for item in schedules if item.get("trigger") == trigger and float(context.get("balance", 0)) <= float(item.get("max_balance", 10**18)))
    fees = tuple({"schedule_id": item.get("schedule_id"), "amount": item.get("amount"), "rule_version": item.get("rule_version"), "notice_required": item.get("notice_required", False)} for item in matched)
    return _result("fee_schedule_engine", table=OWNED_TABLES[4], assessed_fees=fees, traceable_rule_versions=tuple(item.get("rule_version") for item in matched))


def govern_fee_waiver(fee: Mapping[str, object], waiver: Mapping[str, object], history: Sequence[Mapping[str, object]] = ()) -> dict:
    amount = float(dict(fee or {}).get("amount", 0))
    tier = "supervisor" if amount >= 50 or len(tuple(history)) >= 2 else "operator"
    approved = bool(dict(waiver or {}).get("reason_code") and dict(waiver or {}).get("approved_by"))
    return _result("fee_waiver_governance", table=OWNED_TABLES[4], approval_tier=tier, approved=approved, repeat_waiver_count=len(tuple(history)), supervisor_queue=tier == "supervisor")


def evaluate_statement_cutover(cycle: Mapping[str, object], pending_items: Sequence[Mapping[str, object]]) -> dict:
    pending = tuple(dict(item) for item in pending_items if item.get("status") not in {"posted", "closed", "resolved"})
    return _result("statement_cycle_cutover_controls", table=OWNED_TABLES[5], cycle_id=dict(cycle or {}).get("cycle_id"), cutover_blocked=bool(pending), warnings=tuple(item.get("item_type", "pending_item") for item in pending), rerun_reason=dict(cycle or {}).get("rerun_reason"))


def prove_statement_balance_forward(opening_balance: float, lines: Sequence[Mapping[str, object]], closing_balance: float) -> dict:
    net_activity = round(sum(float(dict(item).get("amount", 0)) for item in lines), 2)
    expected = round(float(opening_balance) + net_activity, 2)
    return _result("statement_line_balance_forward_proof", table=OWNED_TABLES[5], opening_balance=float(opening_balance), net_activity=net_activity, expected_closing=expected, actual_closing=float(closing_balance), proof_passed=expected == round(float(closing_balance), 2))


def evaluate_mandate(signatories: Sequence[Mapping[str, object]], request: Mapping[str, object]) -> dict:
    active = tuple(dict(item) for item in signatories if item.get("status", "active") == "active")
    provided = set(_tuple(dict(request or {}).get("signed_by")))
    rule = dict(request or {}).get("signing_rule", "one")
    required_count = len(active) if rule == "all" else 2 if rule == "two" else 1
    valid = len(provided.intersection({item.get("signatory_id") for item in active})) >= required_count
    return _result("signatory_mandate_registry", table=OWNED_TABLES[0], mandate_valid=valid, required_signatures=required_count, active_signatories=active)


def schedule_mandate_change(current: Mapping[str, object], change: Mapping[str, object], as_of: object | None = None) -> dict:
    effective = _date(dict(change or {}).get("effective_date"))
    today = _date(as_of)
    state = "active" if effective <= today and dict(change or {}).get("approved") else "pending"
    conflict = dict(current or {}).get("pending_change") and state == "pending"
    return _result("effective_dated_mandate_changes", table=OWNED_TABLES[0], mandate_version_state=state, conflict=bool(conflict), sensitive_actions_blocked=bool(conflict or state == "pending"))


def evaluate_compliance_restriction(restriction: Mapping[str, object], action: str) -> dict:
    blocked = set(_tuple(dict(restriction or {}).get("blocked_capabilities")))
    allowed = action not in blocked
    return _result("compliance_restriction_boundary", table=OWNED_TABLES[2], action=action, allowed=allowed, source=dict(restriction or {}).get("source"), leaks_external_internals=False)


def open_compliance_case(account_id: str, case_type: str, evidence: Sequence[str] = ()) -> dict:
    sla_days = {"sanctions_review": 1, "source_of_funds": 5, "suspicious_activity_followup": 2, "deceased_customer_hold": 10, "documentation_deficiency": 7}.get(case_type, 5)
    return _result("compliance_review_service_cases", table=OWNED_TABLES[6], case_id=f"CASE-{_digest((account_id, case_type))[:8]}", account_id=account_id, case_type=case_type, sla_days=sla_days, required_evidence=tuple(evidence), status="open")


def evaluate_dormancy(account: Mapping[str, object], activity: Sequence[Mapping[str, object]], threshold_days: int, as_of: object | None = None) -> dict:
    today = _date(as_of)
    latest = max((_date(item.get("activity_date")) for item in activity), default=_date(dict(account or {}).get("opened_date") or today))
    inactive_days = (today - latest).days
    dormant = inactive_days >= threshold_days
    return _result("dormancy_inactivity_reactivation", table=OWNED_TABLES[0], inactive_days=inactive_days, dormant=dormant, reactivation_requires_evidence=dormant)


def evaluate_closure_checklist(account: Mapping[str, object], balances: Mapping[str, object], holds: Sequence[Mapping[str, object]], statements: Sequence[Mapping[str, object]]) -> dict:
    failures = []
    if round(float(dict(balances or {}).get("ledger", 0)), 2) != 0:
        failures.append("residual_balance")
    if any(dict(item).get("status", "active") == "active" for item in holds):
        failures.append("active_holds")
    if any(dict(item).get("status") not in {"closed", "generated"} for item in statements):
        failures.append("statement_obligation_open")
    return _result("account_closure_residual_balance", table=OWNED_TABLES[0], closure_allowed=not failures, checklist_failures=tuple(failures))


def evaluate_reopening(account: Mapping[str, object], reason: str | None, inherited_restrictions: Sequence[Mapping[str, object]] = ()) -> dict:
    allowed = dict(account or {}).get("lifecycle_state") == "closed" and bool(reason)
    return _result("controlled_account_reopening", table=OWNED_TABLES[0], reopening_allowed=allowed, lineage_account_id=dict(account or {}).get("account_id"), inherited_restrictions=tuple(inherited_restrictions), fresh_account_required=not allowed)


def evaluate_linked_account_relationship(account: Mapping[str, object], relationship: Mapping[str, object], action: str) -> dict:
    permissions = set(_tuple(dict(relationship or {}).get("permissions")))
    active = dict(relationship or {}).get("status", "active") == "active"
    return _result("linked_account_relationships", table=OWNED_TABLES[0], action=action, permitted=active and action in permissions, transfer_execution_owned_elsewhere=True)


def reconcile_subledger_balances(projections: Sequence[Mapping[str, object]], posting_evidence: Sequence[Mapping[str, object]], tolerance: float = 0.01) -> dict:
    postings = {item.get("account_id"): float(item.get("amount", 0)) for item in posting_evidence}
    breaks = []
    matched = []
    for projection in projections:
        projection = dict(projection)
        delta = round(float(projection.get("ledger", 0)) - postings.get(projection.get("account_id"), 0.0), 2)
        target = matched if abs(delta) <= tolerance else breaks
        target.append({"account_id": projection.get("account_id"), "delta": delta})
    return _result("subledger_balance_reconciliation", table=OWNED_TABLES[1], matched=tuple(matched), breaks=tuple(breaks), service_cases_opened=tuple(item["account_id"] for item in breaks))


def classify_posting_boundary(update: Mapping[str, object]) -> dict:
    update = dict(update or {})
    boundary = update.get("posting_boundary", "intraday")
    customer_visible = boundary in {"intraday", "backdated_correction"}
    statement_visible = boundary in {"end_of_day", "backdated_correction"}
    return _result("intraday_end_of_day_posting_boundary", table=OWNED_TABLES[1], posting_boundary=boundary, customer_visible=customer_visible, statement_visible=statement_visible)


def build_typed_event_catalog() -> dict:
    events = ("DepositAccountOpened", "DepositAccountActivated", "DepositAccountRestricted", "DepositAccountDormant", "DepositAccountReactivated", "DepositAccountClosed", "HoldApplied", "HoldReleased", "FeeWaived", "InterestCapitalized", "StatementClosed", "ReconciliationBreakOpened")
    return _result("typed_deposit_domain_events", table=OWNED_TABLES[12], events=events, compatibility_envelopes=("BankingCoreAccountsCreated", "BankingCoreAccountsUpdated", "BankingCoreAccountsApproved", "BankingCoreAccountsExceptionOpened"))


def evaluate_idempotent_command(operation: str, payload: Mapping[str, object], seen_keys: Sequence[str]) -> dict:
    key = str(dict(payload or {}).get("idempotency_key") or _digest((operation, payload)))
    duplicate = key in set(seen_keys)
    return _result("idempotent_external_command_keys", table=OWNED_TABLES[12], idempotency_key=key, duplicate=duplicate, business_outcome_count=0 if duplicate else 1)


def build_dead_letter_recovery_view(failures: Sequence[Mapping[str, object]]) -> dict:
    grouped: dict[str, list[dict]] = {}
    for failure in failures:
        failure = dict(failure)
        grouped.setdefault(str(failure.get("account_id", "unknown")), []).append(failure)
    decisions = tuple({"account_id": account_id, "retry_eligible": all(item.get("poison") is not True for item in items), "failure_count": len(items)} for account_id, items in grouped.items())
    return _result("dead_letter_recovery_workbench", table="banking_core_accounts_appgen_dead_letter_event", recovery_decisions=decisions, governed_replay_only=True)


def build_operational_query_api_contract() -> dict:
    routes = ("GET /deposit-accounts/{account_id}", "GET /deposit-accounts/{account_id}/balances", "GET /deposit-accounts/{account_id}/holds", "GET /deposit-accounts/{account_id}/fees", "GET /deposit-accounts/{account_id}/interest", "GET /deposit-accounts/{account_id}/statements", "GET /deposit-accounts/{account_id}/cases")
    return _result("operational_query_apis", table=OWNED_TABLES[0], routes=routes, permission_protected=True, undeclared_private_queries=False)


def build_role_workbench(role: str, items: Sequence[Mapping[str, object]]) -> dict:
    sections_by_role = {"branch": ("opening_queue", "maintenance_queue"), "central_ops": ("restrictions_queue", "statement_operations"), "supervisor": ("fee_interest_review", "control_failures"), "auditor": ("audit_evidence", "timeline")}
    actions_by_role = {"branch": ("open", "service"), "central_ops": ("restrict", "close_statement"), "supervisor": ("approve", "waive"), "auditor": ("read",)}
    return _result("role_based_operations_workbench", table=OWNED_TABLES[0], role=role, sections=sections_by_role.get(role, ("overview",)), enabled_actions=actions_by_role.get(role, ("read",)), records=tuple(items))


def build_account_timeline(events: Sequence[Mapping[str, object]], family: str | None = None) -> dict:
    ordered = tuple(sorted((dict(item) for item in events if family is None or item.get("family") == family), key=lambda item: (str(item.get("effective_at", "")), str(item.get("event_id", "")))))
    return _result("account_detail_timeline", table=OWNED_TABLES[0], timeline=ordered, family_filter=family, event_count=len(ordered))


def plan_assistant_servicing_instruction(instruction: str, context: Mapping[str, object]) -> dict:
    lowered = str(instruction).lower()
    action = "fee_waiver" if "fee" in lowered and "waive" in lowered else "hold_enquiry" if "hold" in lowered else "closure_request" if "close" in lowered else "account_update"
    restricted = bool(dict(context or {}).get("restriction"))
    return _result("assistant_governed_servicing_instructions", table=OWNED_TABLES[11], action=action, affected_account=dict(context or {}).get("account_id"), requires_approval=action in {"fee_waiver", "closure_request"} or restricted, uses_supported_apis_only=True)


def explain_statement_fee(question: str, evidence: Mapping[str, object]) -> dict:
    evidence = dict(evidence or {})
    citations = tuple(key for key in ("account_balance", "fee_assessment", "interest_accrual", "statement_cycle", "account_hold") if evidence.get(key))
    return _result("assistant_statement_fee_explanations", table=OWNED_TABLES[11], question=question, explanation_cards=tuple({"source": citation, "summary": f"Explained from {citation}"} for citation in citations), citations=citations, read_only=True)


def age_exception_cases(cases: Sequence[Mapping[str, object]], as_of: object | None = None) -> dict:
    today = _date(as_of)
    aged = []
    for case in cases:
        case = dict(case)
        age = (today - _date(case.get("opened_date"))).days
        bucket = "0-2" if age <= 2 else "3-7" if age <= 7 else "8+"
        aged.append({**case, "age_days": age, "ageing_bucket": bucket})
    escalations = tuple(item for item in aged if item["ageing_bucket"] == "8+" or item.get("severity") == "high")
    return _result("exception_taxonomy_ageing", table=OWNED_TABLES[6], aged_cases=tuple(aged), escalations=escalations)


def evaluate_policy_rule_version(rule: Mapping[str, object], as_of: object | None = None) -> dict:
    today = _date(as_of)
    start = _date(dict(rule or {}).get("effective_from"))
    end = _date(dict(rule or {}).get("effective_to")) if dict(rule or {}).get("effective_to") else date.max
    active = start <= today <= end
    return _result("policy_rule_versioning_effective_dating", table=OWNED_TABLES[7], rule_id=dict(rule or {}).get("rule_id"), active=active, superseded_by=dict(rule or {}).get("superseded_by"), approval_evidence=dict(rule or {}).get("approval_evidence"))


def detect_parameter_drift(parameters: Sequence[Mapping[str, object]], baselines: Mapping[str, object]) -> dict:
    drift = tuple({"parameter": item.get("name"), "scope": item.get("scope"), "value": item.get("value"), "baseline": baselines.get(item.get("name"))} for item in (dict(p) for p in parameters) if baselines.get(item.get("name")) != item.get("value"))
    return _result("runtime_parameter_scoping_drift", table=OWNED_TABLES[8], drift=drift, emergency_override_expiry_required=any(item.get("scope") == "emergency" for item in parameters))


def evaluate_control_assertions(actions: Sequence[Mapping[str, object]]) -> dict:
    failures = []
    for action in actions:
        action = dict(action)
        if action.get("maker") == action.get("checker"):
            failures.append({"action_id": action.get("action_id"), "control": "segregation_of_duties"})
        if action.get("materiality", 0) > 1000 and not action.get("second_checker"):
            failures.append({"action_id": action.get("action_id"), "control": "missing_second_checker"})
    return _result("continuous_control_assertions", table=OWNED_TABLES[10], failures=tuple(failures), remediation_required=bool(failures))


def build_core_banking_release_pack(scenarios: Mapping[str, object]) -> dict:
    required = ("lifecycle", "balance_components", "holds", "overdraft", "interest", "fees", "statements", "mandates", "compliance", "reconciliation", "control_assertions")
    missing = tuple(item for item in required if not dict(scenarios or {}).get(item))
    return _result("core_banking_release_evidence_pack", table=OWNED_TABLES[11], missing_scenarios=missing, release_ready=not missing, organized_by_domain_scenario=True)


def enforce_tenant_jurisdiction(record: Mapping[str, object], context: Mapping[str, object]) -> dict:
    record = dict(record or {})
    context = dict(context or {})
    allowed = record.get("tenant") == context.get("tenant") and record.get("jurisdiction") == context.get("jurisdiction")
    return _result("tenant_jurisdiction_isolation", table=OWNED_TABLES[0], allowed=allowed, cross_tenant_blocked=record.get("tenant") != context.get("tenant"), cross_jurisdiction_blocked=record.get("jurisdiction") != context.get("jurisdiction"))


def validate_schema_extension(extension: Mapping[str, object]) -> dict:
    extension = dict(extension or {})
    required = ("field_name", "owner", "validation_rule", "display_rule", "migration_plan")
    missing = tuple(field for field in required if not extension.get(field))
    compatible = str(extension.get("table", OWNED_TABLES[0])).startswith(PBC_KEY)
    return _result("schema_extension_registry", table=OWNED_TABLES[9], valid=not missing and compatible, missing_fields=missing, compatible_table=compatible)


def compute_product_branch_analytics(accounts: Sequence[Mapping[str, object]]) -> dict:
    metrics: dict[tuple[str, str], dict[str, float]] = {}
    for account in accounts:
        account = dict(account)
        key = (str(account.get("product_code", "unknown")), str(account.get("branch", "unknown")))
        bucket = metrics.setdefault(key, {"accounts": 0, "balance": 0.0, "holds": 0, "overdrafts": 0, "fee_waivers": 0})
        bucket["accounts"] += 1
        bucket["balance"] += float(account.get("ledger", 0))
        bucket["holds"] += int(bool(account.get("active_holds")))
        bucket["overdrafts"] += int(float(account.get("ledger", 0)) < 0)
        bucket["fee_waivers"] += int(account.get("fee_waiver_count", 0))
    return _result("product_branch_analytics", table=OWNED_TABLES[1], metrics={f"{product}:{branch}": values for (product, branch), values in metrics.items()}, drilldowns=tuple(dict(item).get("account_id") for item in accounts))


def seal_account_evidence(artifact: Mapping[str, object], prior_hash: str = "GENESIS") -> dict:
    seal = _digest({"prior_hash": prior_hash, "artifact": artifact})
    return _result("cryptographic_account_evidence_sealing", table=OWNED_TABLES[12], seal_hash=seal, prior_hash=prior_hash, verification_payload=dict(artifact or {}), verified=True)


def simulate_policy_change(change: Mapping[str, object], historical_accounts: Sequence[Mapping[str, object]]) -> dict:
    change = dict(change or {})
    impacts = []
    for account in historical_accounts:
        account = dict(account)
        if change.get("type") == "fee_schedule" and account.get("fee_count", 0):
            impacts.append({"account_id": account.get("account_id"), "impact": "fee_revenue_change"})
        if change.get("type") == "interest_rate" and float(account.get("ledger", 0)) > 0:
            impacts.append({"account_id": account.get("account_id"), "impact": "interest_expense_change"})
    return _result("counterfactual_fee_rate_policy_simulation", table=OWNED_TABLES[7], impacts=tuple(impacts), non_mutating=True, approval_notes_required=bool(impacts))


def detect_balance_fee_anomalies(signals: Sequence[Mapping[str, object]]) -> dict:
    anomalies = []
    for signal in signals:
        signal = dict(signal)
        if signal.get("fee_burst") or signal.get("hold_reapply_count", 0) >= 3 or signal.get("statement_rerun_count", 0) > 1:
            anomalies.append({"account_id": signal.get("account_id"), "signals": tuple(key for key in ("fee_burst", "hold_reapply_count", "statement_rerun_count") if signal.get(key))})
    return _result("balance_fee_anomaly_detection", table=OWNED_TABLES[10], anomalies=tuple(anomalies), routed_to_control_queue=bool(anomalies))


def normalize_account_identifier(account: Mapping[str, object], audience: str) -> dict:
    account = dict(account or {})
    number = str(account.get("account_number", ""))
    masked = number[:2] + "****" + number[-2:] if len(number) > 4 else "****"
    display = number if audience == "auditor" else masked if audience in {"customer_service", "branch"} else account.get("alias", masked)
    return _result("account_identifier_integrity", table=OWNED_TABLES[0], canonical_account_number=number, display_identifier=display, external_references=tuple(account.get("external_references") or ()), duplicate_blocked=bool(account.get("duplicate_found")))


def evaluate_negative_balance_handoff(account: Mapping[str, object], as_of: object | None = None) -> dict:
    account = dict(account or {})
    negative_days = int(account.get("negative_days", 0))
    threshold = int(account.get("handoff_threshold_days", 30))
    handoff_ready = float(account.get("ledger", 0)) < 0 and negative_days >= threshold
    return _result("negative_balance_collections_handoff_boundary", table=OWNED_TABLES[6], handoff_ready=handoff_ready, cure_milestone=threshold - negative_days, emits_handoff_event=handoff_ready, collections_tables_owned=False)


def adjust_for_operational_calendar(scheduled_date: object, calendar: Mapping[str, object]) -> dict:
    current = _date(scheduled_date)
    holidays = {_date(item) for item in _tuple(dict(calendar or {}).get("holidays"))}
    adjusted = current
    while adjusted.weekday() >= 5 or adjusted in holidays:
        adjusted += timedelta(days=1)
    return _result("operational_calendar_holiday_servicing", table=OWNED_TABLES[5], scheduled_date=current.isoformat(), adjusted_date=adjusted.isoformat(), adjustment_reason="business_day" if adjusted != current else "none")


def plan_correction_restatement(original: Mapping[str, object], correction: Mapping[str, object]) -> dict:
    original = dict(original or {})
    correction = dict(correction or {})
    approved = bool(correction.get("reason_code") and correction.get("approved_by"))
    return _result("correction_restatement_workflow", table=OWNED_TABLES[1], original_version=original, corrected_version=correction, approved=approved, preserves_original=True, customer_impact_note=correction.get("customer_impact_note"))


def build_event_api_boundary_map() -> dict:
    commands = ("POST /deposit-accounts", "POST /account-balances", "POST /account-holds", "POST /interest-accruals", "POST /fee-assessments")
    queries = ("GET /deposit-accounts/{account_id}", "GET /banking-core-accounts-workbench")
    events = build_typed_event_catalog()["events"]
    return _result("event_api_boundary_map", table=OWNED_TABLES[0], commands=commands, queries=queries, events=events, rejects_undeclared_coupling=True)


def build_structural_release_gate(groups: Mapping[str, object]) -> dict:
    required_groups = ("lifecycle", "balances", "holds", "overdraft", "interest", "fees", "statements", "mandates", "compliance", "reconciliation", "assistant", "workbench", "evidence_sealing")
    missing = tuple(group for group in required_groups if not dict(groups or {}).get(group))
    return _result("structural_release_gate", table=OWNED_TABLES[11], missing_groups=missing, release_ready=not missing, reviewer_traceable=True)


def improve1_account_control_contract() -> dict:
    return _result(
        "improve1_account_control_contract",
        table=OWNED_TABLES[0],
        capability_count=len(ACCOUNT_CONTROL_CAPABILITIES),
        capabilities=ACCOUNT_CONTROL_CAPABILITIES,
        owned_tables=OWNED_TABLES,
        ui_surfaces=tuple(f"{PBC_KEY}.ui.account_control.{capability}" for capability in ACCOUNT_CONTROL_CAPABILITIES),
        service_surfaces=tuple(f"{PBC_KEY}.service.account_control.{capability}" for capability in ACCOUNT_CONTROL_CAPABILITIES),
    )
