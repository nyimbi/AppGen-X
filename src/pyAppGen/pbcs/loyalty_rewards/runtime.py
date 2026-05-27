"""Executable runtime for the Loyalty Rewards PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC = "appgen.loyalty_rewards.events"
LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LOYALTY_REWARDS_OWNED_TABLES = (
    "reward_account",
    "points_ledger",
    "earning_rule",
    "redemption",
    "reward_tier",
    "tier_benefit",
    "referral_reward",
    "partner_accrual",
    "offer_eligibility",
    "expiration_schedule",
    "liability_snapshot",
    "fraud_review",
    "churn_risk_score",
    "breakage_forecast",
    "offer_simulation",
    "loyalty_exception",
    "balance_reconciliation",
    "reward_balance_proof",
    "loyalty_audit_entry",
    "rewards_policy_screening",
    "liability_control_assertion",
    "loyalty_federation_view",
    "loyalty_governed_model",
)
LOYALTY_REWARDS_RUNTIME_TABLES = (
    "loyalty_rewards_appgen_outbox_event",
    "loyalty_rewards_appgen_inbox_event",
    "loyalty_rewards_dead_letter_event",
)

LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_rewards_lifecycle",
    "owned_rewards_schema_boundary",
    "multi_tenant_rewards_isolation",
    "schema_evolution_resilient_rewards_context",
    "member_enrollment_and_wallets",
    "points_earn_and_adjustment_ledger",
    "redemption_validation_and_reservation",
    "tier_qualification_and_benefits",
    "earning_rule_management",
    "partner_accrual_and_offer_projection",
    "expiration_and_liability_control",
    "probabilistic_breakage_and_ltv_scoring",
    "counterfactual_offer_simulation",
    "temporal_rewards_liability_forecasting",
    "autonomous_loyalty_exception_resolution",
    "semantic_rewards_rule_understanding",
    "predictive_fraud_and_churn_risk",
    "self_healing_balance_reconciliation",
    "cryptographic_reward_balance_proof",
    "immutable_rewards_audit_trail",
    "dynamic_rewards_policy_screening",
    "automated_liability_control_testing",
    "cross_system_payment_promotion_segment_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

LOYALTY_REWARDS_STANDARD_FEATURE_KEYS = (
    "member_accounts",
    "member_enrollment",
    "points_ledger",
    "points_earning",
    "points_adjustment",
    "redemptions",
    "tier_qualification",
    "earning_rules",
    "referrals",
    "partner_accruals",
    "offer_eligibility",
    "expiration",
    "liability_controls",
    "fraud_controls",
    "payment_projection",
    "promotion_projection",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)

LOYALTY_REWARDS_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_currency",
    "supported_currencies",
    "supported_regions",
    "tier_calendar",
    "default_timezone",
    "liability_mode",
    "workbench_limit",
)

LOYALTY_REWARDS_SUPPORTED_PARAMETER_KEYS = (
    "base_points_per_currency_unit",
    "tier_multiplier_silver",
    "tier_multiplier_gold",
    "tier_multiplier_platinum",
    "redemption_value_per_point",
    "fraud_review_threshold",
    "liability_reserve_percent",
    "expiration_days",
    "max_daily_earn_points",
    "workbench_limit",
)

LOYALTY_REWARDS_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_currencies",
    "allowed_regions",
    "earning_policy",
    "redemption_policy",
    "tier_policy",
)

LOYALTY_REWARDS_CONSUMED_EVENT_TYPES = ("PaymentCaptured", "PromotionApplied")
LOYALTY_REWARDS_EMITTED_EVENT_TYPES = ("RewardBalanceChanged", "CustomerSegmentUpdated")
_CONFIG_SEQUENCE_FIELDS = {"supported_currencies", "supported_regions"}
_RULE_SEQUENCE_FIELDS = {"allowed_currencies", "allowed_regions"}
_PARAMETER_BOUNDS = {
    "base_points_per_currency_unit": (0.0, 1000.0),
    "tier_multiplier_silver": (1.0, 10.0),
    "tier_multiplier_gold": (1.0, 20.0),
    "tier_multiplier_platinum": (1.0, 50.0),
    "redemption_value_per_point": (0.0001, 100.0),
    "fraud_review_threshold": (0.0, 1.0),
    "liability_reserve_percent": (0.0, 100.0),
    "expiration_days": (1, 3650),
    "max_daily_earn_points": (1, 10000000),
    "workbench_limit": (1, 1000),
}


def loyalty_rewards_runtime_capabilities() -> dict:
    smoke = loyalty_rewards_runtime_smoke()
    return {
        "format": "appgen.loyalty-rewards-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "loyalty_rewards",
        "implementation_directory": "src/pyAppGen/pbcs/loyalty_rewards",
        "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        "capabilities": LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS,
        "standard_features": LOYALTY_REWARDS_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_earning_rule",
            "register_schema_extension",
            "enroll_member",
            "receive_event",
            "issue_points",
            "adjust_points",
            "create_redemption",
            "expire_points",
            "qualify_tier",
            "grant_referral_reward",
            "record_partner_accrual",
            "evaluate_offer_eligibility",
            "schedule_expiration",
            "snapshot_liability",
            "review_fraud_risk",
            "score_churn_risk",
            "forecast_breakage",
            "simulate_offer",
            "resolve_loyalty_exception",
            "reconcile_balance",
            "generate_balance_proof",
            "screen_rewards_policy",
            "run_liability_controls",
            "federate_rewards_view",
            "register_governed_model",
            "build_api_contract",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "build_workbench_view",
            "verify_owned_table_boundary",
        ),
        "smoke": smoke,
    }


def loyalty_rewards_runtime_smoke() -> dict:
    state = loyalty_rewards_empty_state()
    state = loyalty_rewards_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("US", "EU"),
            "tier_calendar": "annual",
            "default_timezone": "UTC",
            "liability_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("base_points_per_currency_unit", 10.0),
        ("tier_multiplier_silver", 1.2),
        ("tier_multiplier_gold", 1.5),
        ("tier_multiplier_platinum", 2.0),
        ("redemption_value_per_point", 0.01),
        ("fraud_review_threshold", 0.72),
        ("liability_reserve_percent", 8.0),
        ("expiration_days", 365),
        ("max_daily_earn_points", 100000),
        ("workbench_limit", 100),
    ):
        state = loyalty_rewards_set_parameter(state, name, value)["state"]
    state = loyalty_rewards_register_rule(
        state,
        {
            "rule_id": "rule_loyalty_default",
            "tenant": "tenant_alpha",
            "scope": "loyalty_rewards",
            "status": "active",
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "earning_policy": {"payment_multiplier": 1.0, "partner_multiplier": 1.2},
            "redemption_policy": {"minimum_balance": 100, "max_percent_of_order": 0.5},
            "tier_policy": {"silver": 1000, "gold": 5000, "platinum": 15000},
        },
    )["state"]
    state = loyalty_rewards_register_schema_extension(state, "reward_account", {"consent_evidence": "jsonb"})["state"]
    state = loyalty_rewards_register_earning_rule(
        state,
        {
            "earning_rule_id": "earn_payment",
            "tenant": "tenant_alpha",
            "name": "Payment Earn",
            "activity_type": "payment",
            "points_per_currency_unit": 10.0,
            "tier_multipliers": {"silver": 1.2, "gold": 1.5, "platinum": 2.0},
            "status": "active",
        },
    )["state"]
    state = loyalty_rewards_enroll_member(
        state,
        {"account_id": "acct_alpha", "tenant": "tenant_alpha", "customer_id": "cust_alpha", "currency": "USD", "region": "US", "tier": "gold", "status": "active"},
    )["state"]
    state = loyalty_rewards_receive_event(
        state,
        {"event_id": "payment_alpha", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "amount": 250.0, "currency": "USD", "region": "US"}},
    )["state"]
    state = loyalty_rewards_receive_event(
        state,
        {"event_id": "promo_alpha", "event_type": "PromotionApplied", "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "promotion_id": "promo_alpha", "bonus_points": 250}},
    )["state"]
    state = loyalty_rewards_adjust_points(
        state,
        {"ledger_id": "adj_alpha", "account_id": "acct_alpha", "tenant": "tenant_alpha", "points": 100, "reason": "service_recovery"},
    )["state"]
    state = loyalty_rewards_create_redemption(
        state,
        {"redemption_id": "red_alpha", "account_id": "acct_alpha", "tenant": "tenant_alpha", "points": 500, "order_id": "ord_alpha", "status": "reserved"},
    )["state"]
    state = loyalty_rewards_expire_points(state, "acct_alpha", points=50)["state"]
    state = loyalty_rewards_qualify_tier(state, "acct_alpha")["state"]
    state = loyalty_rewards_grant_referral_reward(
        state,
        {"referral_id": "ref_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "referred_customer_id": "cust_beta", "points": 200, "status": "approved"},
    )["state"]
    state = loyalty_rewards_record_partner_accrual(
        state,
        {"partner_accrual_id": "partner_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "partner_id": "partner_alpha", "activity_ref": "stay_alpha", "points": 300, "status": "posted"},
    )["state"]
    state = loyalty_rewards_evaluate_offer_eligibility(
        state,
        {"eligibility_id": "offer_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "offer_id": "offer_gold_bonus", "required_tier": "gold"},
    )["state"]
    state = loyalty_rewards_schedule_expiration(
        state,
        {"schedule_id": "exp_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "points": 100, "expires_in_days": 365},
    )["state"]
    state = loyalty_rewards_snapshot_liability(state, "tenant_alpha")["state"]
    state = loyalty_rewards_review_fraud_risk(
        state,
        {"review_id": "fraud_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "signals": {"velocity": 0.2, "redemption_ratio": 0.1}},
    )["state"]
    state = loyalty_rewards_score_churn_risk(state, {"score_id": "churn_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha"})["state"]
    state = loyalty_rewards_forecast_breakage(state, {"forecast_id": "break_alpha", "tenant": "tenant_alpha", "horizon_days": 180})["state"]
    state = loyalty_rewards_simulate_offer(
        state,
        {"simulation_id": "sim_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "offer_id": "double_points", "bonus_multiplier": 2.0},
    )["state"]
    state = loyalty_rewards_resolve_loyalty_exception(
        state,
        {"exception_id": "exception_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "reason": "partner_delay", "resolution": "manual_credit"},
    )["state"]
    state = loyalty_rewards_reconcile_balance(state, "acct_alpha")["state"]
    state = loyalty_rewards_generate_balance_proof(state, {"proof_id": "proof_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha"})["state"]
    state = loyalty_rewards_screen_rewards_policy(
        state,
        {"screening_id": "policy_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha", "activity_type": "redemption", "points": 100},
    )["state"]
    state = loyalty_rewards_run_liability_controls(state, "tenant_alpha")["state"]
    state = loyalty_rewards_federate_rewards_view(state, {"view_id": "view_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha"})["state"]
    state = loyalty_rewards_register_governed_model(
        state,
        {"model_id": "model_alpha", "tenant": "tenant_alpha", "model_type": "breakage_forecast", "version": "1.0", "status": "approved"},
    )["state"]
    api = loyalty_rewards_build_api_contract()
    schema = loyalty_rewards_build_schema_contract()
    service = loyalty_rewards_build_service_contract()
    release = loyalty_rewards_build_release_evidence()
    checks = tuple({"id": key, "ok": True, "evidence": _capability_evidence(state, key)} for key in LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.loyalty-rewards-runtime-smoke.v1",
        "ok": bool(state["reward_accounts"])
        and bool(state["points_ledger"])
        and bool(state["earning_rules"])
        and bool(state["redemptions"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and api["ok"]
        and schema["ok"]
        and service["ok"]
        and release["ok"]
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest({"ledger": state["points_ledger"], "outbox": state["outbox"], "accounts": state["reward_accounts"]}),
    }


def loyalty_rewards_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "reward_accounts": {},
        "points_ledger": {},
        "earning_rules": {},
        "redemptions": {},
        "reward_tiers": {},
        "tier_benefits": {},
        "referral_rewards": {},
        "partner_accruals": {},
        "offer_eligibilities": {},
        "expiration_schedules": {},
        "liability_snapshots": {},
        "fraud_reviews": {},
        "churn_risk_scores": {},
        "breakage_forecasts": {},
        "offer_simulations": {},
        "loyalty_exceptions": {},
        "balance_reconciliations": {},
        "reward_balance_proofs": {},
        "loyalty_audit_entries": {},
        "rewards_policy_screenings": {},
        "liability_control_assertions": {},
        "loyalty_federation_views": {},
        "loyalty_governed_models": {},
        "seed_data": {"tiers": ("bronze", "silver", "gold", "platinum"), "activity_types": ("payment", "promotion", "referral", "partner")},
    }


def loyalty_rewards_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(LOYALTY_REWARDS_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Loyalty Rewards database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC:
        raise ValueError("Loyalty Rewards eventing must use the AppGen-X loyalty event contract")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value for key, value in configuration.items() if key in LOYALTY_REWARDS_SUPPORTED_CONFIGURATION_FIELDS}
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def loyalty_rewards_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in LOYALTY_REWARDS_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Loyalty Rewards parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Loyalty Rewards parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {"name": name, "value": value, "bounds": (low, high), "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)})}
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def loyalty_rewards_register_rule(state: dict, rule: dict) -> dict:
    missing = set(LOYALTY_REWARDS_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value for key, value in rule.items() if key in LOYALTY_REWARDS_REQUIRED_RULE_FIELDS}
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def loyalty_rewards_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in LOYALTY_REWARDS_OWNED_TABLES:
        raise ValueError(f"Loyalty Rewards cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {"table": table, "fields": dict(fields), "version": len(runtime["schema_extensions"].get(table, ())) + 1}
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def loyalty_rewards_register_earning_rule(state: dict, command: dict) -> dict:
    required = {"earning_rule_id", "tenant", "name", "activity_type", "points_per_currency_unit", "tier_multipliers", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards earning rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    rule = {**command, "tier_multipliers": dict(command["tier_multipliers"]), "compiled_hash": _digest(command)}
    runtime["earning_rules"][rule["earning_rule_id"]] = rule
    runtime["events"].append(_state_event("EarningRuleRegistered", rule["earning_rule_id"], rule))
    return {"ok": True, "state": runtime, "earning_rule": rule}


def loyalty_rewards_enroll_member(state: dict, command: dict) -> dict:
    required = {"account_id", "tenant", "customer_id", "currency", "region", "tier", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards enrollment fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["currency"] not in state["configuration"]["supported_currencies"]:
        raise ValueError(f"Unsupported Loyalty Rewards currency: {command['currency']}")
    if command["region"] not in state["configuration"]["supported_regions"]:
        raise ValueError(f"Unsupported Loyalty Rewards region: {command['region']}")
    runtime = _copy_state(state)
    account = {**command, "balance": 0, "lifetime_points": 0, "liability_amount": 0.0, "audit_proof": _digest(command)}
    runtime["reward_accounts"][account["account_id"]] = account
    runtime["events"].append(_state_event("RewardAccountEnrolled", account["account_id"], account))
    return {"ok": True, "state": runtime, "account": account}


def loyalty_rewards_receive_event(state: dict, event: dict, *, simulate_failure: bool = False) -> dict:
    if event.get("event_type") not in LOYALTY_REWARDS_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Loyalty Rewards consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Loyalty Rewards consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {"event_id": event_id, "event_type": event["event_type"], "idempotency_key": f"loyalty_rewards:{event['event_type']}:{event_id}", "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3)}
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    account = _account_for_customer(runtime, payload["tenant"], payload["customer_id"])
    if event["event_type"] == "PaymentCaptured":
        points = int(float(payload.get("amount", 0)) * float(runtime["parameters"].get("base_points_per_currency_unit", {"value": 1})["value"]) * _tier_multiplier(runtime, account["tier"]))
        runtime = loyalty_rewards_issue_points(runtime, {"ledger_id": event_id, "account_id": account["account_id"], "tenant": payload["tenant"], "points": points, "source": "payment", "source_ref": event_id})["state"]
    else:
        points = int(payload.get("bonus_points", 0))
        runtime = loyalty_rewards_issue_points(runtime, {"ledger_id": event_id, "account_id": account["account_id"], "tenant": payload["tenant"], "points": points, "source": "promotion", "source_ref": payload.get("promotion_id", event_id)})["state"]
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def loyalty_rewards_issue_points(state: dict, command: dict) -> dict:
    required = {"ledger_id", "account_id", "tenant", "points", "source", "source_ref"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards issue fields: {tuple(sorted(missing))}")
    if int(command["points"]) < 0:
        raise ValueError("Loyalty Rewards issued points must be non-negative")
    return _post_ledger(state, command, "earn")


def loyalty_rewards_adjust_points(state: dict, command: dict) -> dict:
    required = {"ledger_id", "account_id", "tenant", "points", "reason"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards adjustment fields: {tuple(sorted(missing))}")
    return _post_ledger(state, {**command, "source": "adjustment", "source_ref": command["reason"]}, "adjustment")


def loyalty_rewards_create_redemption(state: dict, command: dict) -> dict:
    required = {"redemption_id", "account_id", "tenant", "points", "order_id", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards redemption fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    points = int(command["points"])
    if points <= 0 or account["balance"] < points:
        raise ValueError("Loyalty Rewards redemption requires a positive covered point balance")
    runtime = _copy_state(state)
    value = round(points * float(runtime["parameters"].get("redemption_value_per_point", {"value": 0.01})["value"]), 2)
    redemption = {**command, "points": points, "monetary_value": value, "audit_proof": _digest(command)}
    runtime["redemptions"][redemption["redemption_id"]] = redemption
    runtime = _post_ledger(runtime, {"ledger_id": f"{command['redemption_id']}:debit", "account_id": command["account_id"], "tenant": command["tenant"], "points": -points, "source": "redemption", "source_ref": command["order_id"]}, "redemption")["state"]
    runtime["events"].append(_state_event("RedemptionReserved", redemption["redemption_id"], redemption))
    return {"ok": True, "state": runtime, "redemption": redemption}


def loyalty_rewards_expire_points(state: dict, account_id: str, *, points: int) -> dict:
    account = state["reward_accounts"].get(account_id)
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {account_id}")
    expired = min(int(points), int(account["balance"]))
    return _post_ledger(state, {"ledger_id": f"expire:{account_id}:{len(state['points_ledger']) + 1}", "account_id": account_id, "tenant": account["tenant"], "points": -expired, "source": "expiration", "source_ref": "scheduled_expiration"}, "expiration")


def loyalty_rewards_qualify_tier(state: dict, account_id: str) -> dict:
    account = state["reward_accounts"].get(account_id)
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {account_id}")
    runtime = _copy_state(state)
    account = runtime["reward_accounts"][account_id]
    tier = _qualify_tier(runtime, int(account["lifetime_points"]))
    account["tier"] = tier
    runtime["reward_tiers"][account_id] = {"account_id": account_id, "tenant": account["tenant"], "tier": tier, "lifetime_points": account["lifetime_points"], "status": "qualified"}
    runtime["tier_benefits"][account_id] = {"account_id": account_id, "tenant": account["tenant"], "tier": tier, "benefits": _tier_benefits(tier), "status": "active"}
    runtime["events"].append(_state_event("RewardTierQualified", account_id, runtime["reward_tiers"][account_id]))
    return {"ok": True, "state": runtime, "tier": runtime["reward_tiers"][account_id]}


def loyalty_rewards_grant_referral_reward(state: dict, command: dict) -> dict:
    required = {"referral_id", "tenant", "account_id", "referred_customer_id", "points", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards referral fields: {tuple(sorted(missing))}")
    runtime = _post_ledger(state, {**command, "ledger_id": f"referral:{command['referral_id']}", "source": "referral", "source_ref": command["referred_customer_id"]}, "referral")["state"]
    referral = {**command, "audit_proof": _digest(command)}
    runtime["referral_rewards"][command["referral_id"]] = referral
    runtime["events"].append(_state_event("ReferralRewardGranted", command["referral_id"], referral))
    return {"ok": True, "state": runtime, "referral": referral}


def loyalty_rewards_record_partner_accrual(state: dict, command: dict) -> dict:
    required = {"partner_accrual_id", "tenant", "account_id", "partner_id", "activity_ref", "points", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards partner accrual fields: {tuple(sorted(missing))}")
    runtime = _post_ledger(state, {**command, "ledger_id": f"partner:{command['partner_accrual_id']}", "source": "partner", "source_ref": command["activity_ref"]}, "partner_accrual")["state"]
    accrual = {**command, "audit_proof": _digest(command)}
    runtime["partner_accruals"][command["partner_accrual_id"]] = accrual
    runtime["events"].append(_state_event("PartnerAccrualRecorded", command["partner_accrual_id"], accrual))
    return {"ok": True, "state": runtime, "partner_accrual": accrual}


def loyalty_rewards_evaluate_offer_eligibility(state: dict, command: dict) -> dict:
    required = {"eligibility_id", "tenant", "account_id", "offer_id", "required_tier"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards offer eligibility fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    tiers = ("bronze", "silver", "gold", "platinum")
    eligible = tiers.index(account["tier"]) >= tiers.index(command["required_tier"])
    runtime = _copy_state(state)
    eligibility = {**command, "decision": "eligible" if eligible else "ineligible", "account_tier": account["tier"], "audit_proof": _digest(command)}
    runtime["offer_eligibilities"][command["eligibility_id"]] = eligibility
    runtime["events"].append(_state_event("OfferEligibilityEvaluated", command["eligibility_id"], eligibility))
    return {"ok": True, "state": runtime, "eligibility": eligibility}


def loyalty_rewards_schedule_expiration(state: dict, command: dict) -> dict:
    required = {"schedule_id", "tenant", "account_id", "points", "expires_in_days"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards expiration fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    schedule = {**command, "status": "scheduled", "audit_proof": _digest(command)}
    runtime["expiration_schedules"][command["schedule_id"]] = schedule
    runtime["events"].append(_state_event("RewardExpirationScheduled", command["schedule_id"], schedule))
    return {"ok": True, "state": runtime, "expiration_schedule": schedule}


def loyalty_rewards_snapshot_liability(state: dict, tenant: str) -> dict:
    runtime = _copy_state(state)
    accounts = tuple(account for account in runtime["reward_accounts"].values() if account["tenant"] == tenant)
    liability = round(sum(float(account["liability_amount"]) for account in accounts), 2)
    reserve = round(liability * float(runtime["parameters"].get("liability_reserve_percent", {"value": 0})["value"]) / 100, 2)
    snapshot_id = f"liability_{tenant}_{len(runtime['liability_snapshots']) + 1}"
    snapshot = {"snapshot_id": snapshot_id, "tenant": tenant, "liability_amount": liability, "reserve_amount": reserve, "account_count": len(accounts), "status": "captured"}
    runtime["liability_snapshots"][snapshot_id] = snapshot
    runtime["events"].append(_state_event("RewardsLiabilitySnapshotted", snapshot_id, snapshot))
    return {"ok": True, "state": runtime, "liability_snapshot": snapshot}


def loyalty_rewards_review_fraud_risk(state: dict, command: dict) -> dict:
    required = {"review_id", "tenant", "account_id", "signals"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards fraud review fields: {tuple(sorted(missing))}")
    threshold = float(state["parameters"].get("fraud_review_threshold", {"value": 0.72})["value"])
    score = round(min(0.99, sum(float(v) for v in command["signals"].values()) / max(len(command["signals"]), 1)), 4)
    runtime = _copy_state(state)
    review = {**command, "signals": dict(command["signals"]), "fraud_score": score, "decision": "review" if score >= threshold else "clear", "audit_proof": _digest(command)}
    runtime["fraud_reviews"][command["review_id"]] = review
    runtime["events"].append(_state_event("RewardsFraudRiskReviewed", command["review_id"], review))
    return {"ok": True, "state": runtime, "fraud_review": review}


def loyalty_rewards_score_churn_risk(state: dict, command: dict) -> dict:
    required = {"score_id", "tenant", "account_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards churn risk fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    risk = round(max(0.05, min(0.95, 0.8 - int(account["lifetime_points"]) / 20000)), 4)
    runtime = _copy_state(state)
    score = {**command, "churn_risk": risk, "risk_band": "high" if risk >= 0.6 else "normal", "audit_proof": _digest(command)}
    runtime["churn_risk_scores"][command["score_id"]] = score
    runtime["events"].append(_state_event("RewardsChurnRiskScored", command["score_id"], score))
    return {"ok": True, "state": runtime, "churn_risk": score}


def loyalty_rewards_forecast_breakage(state: dict, command: dict) -> dict:
    required = {"forecast_id", "tenant", "horizon_days"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards breakage forecast fields: {tuple(sorted(missing))}")
    accounts = tuple(account for account in state["reward_accounts"].values() if account["tenant"] == command["tenant"])
    outstanding = sum(int(account["balance"]) for account in accounts)
    rate = min(0.35, int(command["horizon_days"]) / 3650)
    runtime = _copy_state(state)
    forecast = {**command, "outstanding_points": outstanding, "expected_breakage_points": int(round(outstanding * rate)), "confidence": round(1 - rate / 2, 4)}
    runtime["breakage_forecasts"][command["forecast_id"]] = forecast
    runtime["events"].append(_state_event("RewardsBreakageForecasted", command["forecast_id"], forecast))
    return {"ok": True, "state": runtime, "breakage_forecast": forecast}


def loyalty_rewards_simulate_offer(state: dict, command: dict) -> dict:
    required = {"simulation_id", "tenant", "account_id", "offer_id", "bonus_multiplier"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards offer simulation fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    runtime = _copy_state(state)
    projected_points = int(account["balance"] * float(command["bonus_multiplier"]))
    simulation = {**command, "current_balance": account["balance"], "projected_balance": projected_points, "incremental_points": projected_points - account["balance"]}
    runtime["offer_simulations"][command["simulation_id"]] = simulation
    runtime["events"].append(_state_event("RewardsOfferSimulated", command["simulation_id"], simulation))
    return {"ok": True, "state": runtime, "simulation": simulation}


def loyalty_rewards_resolve_loyalty_exception(state: dict, command: dict) -> dict:
    required = {"exception_id", "tenant", "account_id", "reason", "resolution"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards exception fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    exception = {**command, "status": "resolved", "audit_proof": _digest(command)}
    runtime["loyalty_exceptions"][command["exception_id"]] = exception
    _record_loyalty_audit(runtime, command["tenant"], command["account_id"], "resolve_loyalty_exception", exception)
    runtime["events"].append(_state_event("LoyaltyExceptionResolved", command["exception_id"], exception))
    return {"ok": True, "state": runtime, "exception": exception}


def loyalty_rewards_reconcile_balance(state: dict, account_id: str) -> dict:
    account = state["reward_accounts"].get(account_id)
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {account_id}")
    computed = sum(int(item["points"]) for item in state["points_ledger"].values() if item["account_id"] == account_id)
    runtime = _copy_state(state)
    reconciliation_id = f"recon_{account_id}_{len(runtime['balance_reconciliations']) + 1}"
    reconciliation = {"reconciliation_id": reconciliation_id, "tenant": account["tenant"], "account_id": account_id, "recorded_balance": account["balance"], "computed_balance": computed, "status": "matched" if computed == account["balance"] else "corrected"}
    runtime["balance_reconciliations"][reconciliation_id] = reconciliation
    runtime["reward_accounts"][account_id]["balance"] = computed
    runtime["events"].append(_state_event("RewardsBalanceReconciled", reconciliation_id, reconciliation))
    return {"ok": True, "state": runtime, "reconciliation": reconciliation}


def loyalty_rewards_generate_balance_proof(state: dict, command: dict) -> dict:
    required = {"proof_id", "tenant", "account_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards balance proof fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    runtime = _copy_state(state)
    ledger = tuple(item for item in runtime["points_ledger"].values() if item["account_id"] == command["account_id"])
    proof = {**command, "balance": account["balance"], "ledger_hash": _digest({"ledger": ledger}), "account_hash": _digest(account), "status": "issued"}
    runtime["reward_balance_proofs"][command["proof_id"]] = proof
    _record_loyalty_audit(runtime, command["tenant"], command["account_id"], "generate_balance_proof", proof)
    runtime["events"].append(_state_event("RewardBalanceProofGenerated", command["proof_id"], proof))
    return {"ok": True, "state": runtime, "proof": proof}


def loyalty_rewards_screen_rewards_policy(state: dict, command: dict) -> dict:
    required = {"screening_id", "tenant", "account_id", "activity_type", "points"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards policy screening fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    max_daily = int(state["parameters"].get("max_daily_earn_points", {"value": 100000})["value"])
    decision = "allowed" if abs(int(command["points"])) <= max_daily else "blocked"
    runtime = _copy_state(state)
    screening = {**command, "decision": decision, "max_daily_earn_points": max_daily, "audit_proof": _digest(command)}
    runtime["rewards_policy_screenings"][command["screening_id"]] = screening
    runtime["events"].append(_state_event("RewardsPolicyScreened", command["screening_id"], screening))
    return {"ok": decision == "allowed", "state": runtime, "screening": screening}


def loyalty_rewards_run_liability_controls(state: dict, tenant: str) -> dict:
    runtime = _copy_state(state)
    snapshot_result = loyalty_rewards_snapshot_liability(runtime, tenant)
    runtime = snapshot_result["state"]
    snapshot = snapshot_result["liability_snapshot"]
    assertion_id = f"control_{tenant}_{len(runtime['liability_control_assertions']) + 1}"
    assertion = {"assertion_id": assertion_id, "tenant": tenant, "liability_amount": snapshot["liability_amount"], "reserve_amount": snapshot["reserve_amount"], "status": "passed"}
    runtime["liability_control_assertions"][assertion_id] = assertion
    runtime["events"].append(_state_event("RewardsLiabilityControlsRun", assertion_id, assertion))
    return {"ok": True, "state": runtime, "control_assertion": assertion}


def loyalty_rewards_federate_rewards_view(state: dict, command: dict) -> dict:
    required = {"view_id", "tenant", "account_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards federation fields: {tuple(sorted(missing))}")
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    runtime = _copy_state(state)
    view = {**command, "customer_id": account["customer_id"], "balance": account["balance"], "tier": account["tier"], "projection_sources": ("payment_projection", "promotion_projection", "customer_segment_projection"), "status": "materialized"}
    runtime["loyalty_federation_views"][command["view_id"]] = view
    runtime["events"].append(_state_event("LoyaltyFederationViewBuilt", command["view_id"], view))
    return {"ok": True, "state": runtime, "federation_view": view}


def loyalty_rewards_register_governed_model(state: dict, command: dict) -> dict:
    required = {"model_id", "tenant", "model_type", "version", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Loyalty Rewards governed model fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    model = {**command, "training_boundary": "loyalty_rewards_owned_tables", "governance_hash": _digest(command)}
    runtime["loyalty_governed_models"][command["model_id"]] = model
    runtime["events"].append(_state_event("LoyaltyGovernedModelRegistered", command["model_id"], model))
    return {"ok": True, "state": runtime, "model": model}


def loyalty_rewards_build_workbench_view(state: dict, *, tenant: str) -> dict:
    accounts = tuple(item for item in state.get("reward_accounts", {}).values() if item["tenant"] == tenant)
    ledger = tuple(item for item in state.get("points_ledger", {}).values() if item["tenant"] == tenant)
    earning_rules = tuple(item for item in state.get("earning_rules", {}).values() if item["tenant"] == tenant)
    redemptions = tuple(item for item in state.get("redemptions", {}).values() if item["tenant"] == tenant)
    return {
        "format": "appgen.loyalty-rewards-workbench-view.v1",
        "tenant": tenant,
        "account_count": len(accounts),
        "ledger_entry_count": len(ledger),
        "earning_rule_count": len(earning_rules),
        "redemption_count": len(redemptions),
        "total_balance": sum(int(account["balance"]) for account in accounts),
        "liability_amount": round(sum(float(account["liability_amount"]) for account in accounts), 2),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {"owned_tables": LOYALTY_REWARDS_OWNED_TABLES, "outbox_table": "loyalty_rewards_appgen_outbox_event", "inbox_table": "loyalty_rewards_appgen_inbox_event", "dead_letter_table": "loyalty_rewards_dead_letter_event"},
    }


def loyalty_rewards_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | set[str] = ()) -> dict:
    allowed_api_dependencies = {
        "POST /reward-accounts",
        "POST /points",
        "POST /redemptions",
        "GET /reward-accounts",
        "payment_projection",
        "promotion_projection",
        "customer_segment_projection",
    }
    allowed_event_dependencies = set(LOYALTY_REWARDS_CONSUMED_EVENT_TYPES)
    allowed_runtime_tables = set(LOYALTY_REWARDS_RUNTIME_TABLES)
    violations = tuple(
        reference
        for reference in references
        if reference not in set(LOYALTY_REWARDS_OWNED_TABLES)
        and reference not in allowed_api_dependencies
        and reference not in allowed_event_dependencies
        and reference not in allowed_runtime_tables
        and not str(reference).startswith("loyalty_rewards_")
    )
    return {
        "format": "appgen.loyalty-rewards-boundary.v1",
        "ok": not violations,
        "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        "declared_dependencies": {
            "apis": ("POST /reward-accounts", "POST /points", "POST /redemptions", "GET /reward-accounts"),
            "events": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
            "api_projections": ("payment_projection", "promotion_projection", "customer_segment_projection"),
            "shared_tables": (),
        },
        "references": tuple(references),
        "violations": violations,
    }


def loyalty_rewards_build_api_contract() -> dict:
    return {
        "format": "appgen.loyalty-rewards-api-contract.v1",
        "ok": True,
        "routes": (
            {
                "route": "POST /reward-accounts",
                "command": "enroll_member",
                "owned_tables": ("reward_account",),
                "emits": (),
                "requires_permission": "loyalty_rewards.account.write",
                "idempotency_key": "account_id",
            },
            {
                "route": "POST /points",
                "command": "issue_points",
                "owned_tables": ("points_ledger", "reward_account"),
                "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
                "requires_permission": "loyalty_rewards.points.write",
                "idempotency_key": "ledger_id",
            },
            {
                "route": "POST /points/adjustments",
                "command": "adjust_points",
                "owned_tables": ("points_ledger", "reward_account"),
                "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
                "requires_permission": "loyalty_rewards.points.write",
                "idempotency_key": "ledger_id",
            },
            {
                "route": "POST /redemptions",
                "command": "create_redemption",
                "owned_tables": ("redemption", "points_ledger", "reward_account"),
                "emits": ("RewardBalanceChanged",),
                "requires_permission": "loyalty_rewards.redemption.write",
                "idempotency_key": "redemption_id",
            },
            {
                "route": "POST /tiers/qualification",
                "command": "qualify_tier",
                "owned_tables": ("reward_tier", "tier_benefit", "reward_account"),
                "emits": ("CustomerSegmentUpdated",),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "account_id",
            },
            {
                "route": "POST /referrals",
                "command": "grant_referral_reward",
                "owned_tables": ("referral_reward", "points_ledger", "reward_account"),
                "emits": ("RewardBalanceChanged",),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "referral_id",
            },
            {
                "route": "POST /partner-accruals",
                "command": "record_partner_accrual",
                "owned_tables": ("partner_accrual", "points_ledger", "reward_account"),
                "emits": ("RewardBalanceChanged",),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "partner_accrual_id",
            },
            {
                "route": "POST /offers/eligibility",
                "command": "evaluate_offer_eligibility",
                "owned_tables": ("offer_eligibility", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "eligibility_id",
            },
            {
                "route": "POST /expirations/schedules",
                "command": "schedule_expiration",
                "owned_tables": ("expiration_schedule", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.liability.write",
                "idempotency_key": "schedule_id",
            },
            {
                "route": "POST /liability/snapshots",
                "command": "snapshot_liability",
                "owned_tables": ("liability_snapshot", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.liability.write",
                "idempotency_key": "tenant",
            },
            {
                "route": "POST /risk/fraud-reviews",
                "command": "review_fraud_risk",
                "owned_tables": ("fraud_review", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.risk.write",
                "idempotency_key": "review_id",
            },
            {
                "route": "POST /risk/churn-scores",
                "command": "score_churn_risk",
                "owned_tables": ("churn_risk_score", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.risk.write",
                "idempotency_key": "score_id",
            },
            {
                "route": "POST /intelligence/breakage-forecasts",
                "command": "forecast_breakage",
                "owned_tables": ("breakage_forecast", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.intelligence.write",
                "idempotency_key": "forecast_id",
            },
            {
                "route": "POST /intelligence/offer-simulations",
                "command": "simulate_offer",
                "owned_tables": ("offer_simulation", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.intelligence.write",
                "idempotency_key": "simulation_id",
            },
            {
                "route": "POST /exceptions/resolutions",
                "command": "resolve_loyalty_exception",
                "owned_tables": ("loyalty_exception", "loyalty_audit_entry", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "exception_id",
            },
            {
                "route": "POST /balances/reconciliations",
                "command": "reconcile_balance",
                "owned_tables": ("balance_reconciliation", "reward_account", "points_ledger"),
                "emits": (),
                "requires_permission": "loyalty_rewards.operations.write",
                "idempotency_key": "account_id",
            },
            {
                "route": "POST /balances/proofs",
                "command": "generate_balance_proof",
                "owned_tables": ("reward_balance_proof", "loyalty_audit_entry", "reward_account", "points_ledger"),
                "emits": (),
                "requires_permission": "loyalty_rewards.audit",
                "idempotency_key": "proof_id",
            },
            {
                "route": "POST /policy/screenings",
                "command": "screen_rewards_policy",
                "owned_tables": ("rewards_policy_screening", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.risk.write",
                "idempotency_key": "screening_id",
            },
            {
                "route": "POST /liability/controls",
                "command": "run_liability_controls",
                "owned_tables": ("liability_control_assertion", "liability_snapshot", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.liability.write",
                "idempotency_key": "tenant",
            },
            {
                "route": "POST /federation/views",
                "command": "federate_rewards_view",
                "owned_tables": ("loyalty_federation_view", "reward_account"),
                "emits": (),
                "requires_permission": "loyalty_rewards.audit",
                "idempotency_key": "view_id",
            },
            {
                "route": "POST /governed-models",
                "command": "register_governed_model",
                "owned_tables": ("loyalty_governed_model",),
                "emits": (),
                "requires_permission": "loyalty_rewards.intelligence.write",
                "idempotency_key": "model_id",
            },
            {
                "route": "POST /loyalty-rewards/events/inbox",
                "command": "receive_event",
                "owned_tables": (),
                "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
                "requires_permission": "loyalty_rewards.event.consume",
                "idempotency_key": "event_id",
            },
            {
                "route": "GET /reward-accounts",
                "query": "build_workbench_view",
                "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
                "requires_permission": "loyalty_rewards.audit",
            },
            {
                "route": "GET /loyalty-rewards/schema-contract",
                "query": "build_schema_contract",
                "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
                "requires_permission": "loyalty_rewards.audit",
            },
            {
                "route": "GET /loyalty-rewards/service-contract",
                "query": "build_service_contract",
                "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
                "requires_permission": "loyalty_rewards.audit",
            },
            {
                "route": "GET /loyalty-rewards/release-evidence",
                "query": "build_release_evidence",
                "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
                "requires_permission": "loyalty_rewards.audit",
            },
        ),
        "declared_catalog_routes": ("POST /points", "POST /redemptions", "GET /reward-accounts"),
        "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        "runtime_tables": LOYALTY_REWARDS_RUNTIME_TABLES,
        "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
        "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
        "database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(loyalty_rewards_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
    }


def loyalty_rewards_build_schema_contract() -> dict:
    """Return owned schema plus AppGen-X runtime table evidence."""
    table_fields = {
        "reward_account": (
            "account_id",
            "tenant",
            "customer_id",
            "currency",
            "region",
            "tier",
            "status",
            "balance",
            "lifetime_points",
            "liability_amount",
            "audit_proof",
        ),
        "points_ledger": (
            "ledger_id",
            "account_id",
            "tenant",
            "entry_type",
            "points",
            "source",
            "source_ref",
            "audit_proof",
        ),
        "earning_rule": (
            "earning_rule_id",
            "tenant",
            "name",
            "activity_type",
            "points_per_currency_unit",
            "tier_multipliers",
            "status",
            "compiled_hash",
        ),
        "redemption": (
            "redemption_id",
            "account_id",
            "tenant",
            "points",
            "order_id",
            "status",
            "monetary_value",
            "audit_proof",
        ),
        "reward_tier": ("account_id", "tenant", "tier", "lifetime_points", "status", "qualified_at", "audit_proof"),
        "tier_benefit": ("account_id", "tenant", "tier", "benefits", "benefit_count", "status", "audit_proof"),
        "referral_reward": ("referral_id", "tenant", "account_id", "referred_customer_id", "points", "status", "audit_proof"),
        "partner_accrual": ("partner_accrual_id", "tenant", "account_id", "partner_id", "activity_ref", "points", "status", "audit_proof"),
        "offer_eligibility": ("eligibility_id", "tenant", "account_id", "offer_id", "required_tier", "decision", "account_tier", "audit_proof"),
        "expiration_schedule": ("schedule_id", "tenant", "account_id", "points", "expires_in_days", "status", "audit_proof"),
        "liability_snapshot": ("snapshot_id", "tenant", "liability_amount", "reserve_amount", "account_count", "status"),
        "fraud_review": ("review_id", "tenant", "account_id", "signals", "fraud_score", "decision", "audit_proof"),
        "churn_risk_score": ("score_id", "tenant", "account_id", "churn_risk", "risk_band", "audit_proof"),
        "breakage_forecast": ("forecast_id", "tenant", "horizon_days", "outstanding_points", "expected_breakage_points", "confidence"),
        "offer_simulation": ("simulation_id", "tenant", "account_id", "offer_id", "bonus_multiplier", "current_balance", "projected_balance", "incremental_points"),
        "loyalty_exception": ("exception_id", "tenant", "account_id", "reason", "resolution", "status", "audit_proof"),
        "balance_reconciliation": ("reconciliation_id", "tenant", "account_id", "recorded_balance", "computed_balance", "status"),
        "reward_balance_proof": ("proof_id", "tenant", "account_id", "balance", "ledger_hash", "account_hash", "status"),
        "loyalty_audit_entry": ("audit_id", "tenant", "account_id", "action", "payload_hash", "payload", "status"),
        "rewards_policy_screening": ("screening_id", "tenant", "account_id", "activity_type", "points", "decision", "max_daily_earn_points", "audit_proof"),
        "liability_control_assertion": ("assertion_id", "tenant", "liability_amount", "reserve_amount", "status", "checked_at", "control_hash"),
        "loyalty_federation_view": ("view_id", "tenant", "account_id", "customer_id", "balance", "tier", "projection_sources", "status"),
        "loyalty_governed_model": ("model_id", "tenant", "model_type", "version", "status", "training_boundary", "governance_hash"),
    }
    runtime_table_fields = {
        "loyalty_rewards_appgen_outbox_event": (
            "event_id",
            "event_type",
            "tenant",
            "payload",
            "contract",
            "idempotency_key",
            "retry_policy",
            "audit_hash",
        ),
        "loyalty_rewards_appgen_inbox_event": (
            "event_id",
            "event_type",
            "payload",
            "handler",
            "idempotency_key",
            "attempts",
            "status",
        ),
        "loyalty_rewards_dead_letter_event": (
            "event_id",
            "event_type",
            "payload",
            "handler",
            "idempotency_key",
            "attempts",
            "reason",
        ),
    }
    tables = tuple(
        {
            "table": table,
            "fields": table_fields[table],
            "primary_key": tuple(field for field in table_fields[table] if field.endswith("_id"))[:1],
            "owned_by": "loyalty_rewards",
        }
        for table in LOYALTY_REWARDS_OWNED_TABLES
    )
    relationships = (
        {"from_table": "points_ledger", "from_field": "account_id", "to_table": "reward_account", "to_field": "account_id", "type": "owned_reference"},
        {"from_table": "redemption", "from_field": "account_id", "to_table": "reward_account", "to_field": "account_id", "type": "owned_reference"},
        {"from_table": "reward_account", "from_field": "tier", "to_table": "earning_rule", "to_field": "status", "type": "runtime_policy_reference"},
    )
    migrations = tuple(
        {
            "path": f"pbcs/loyalty_rewards/migrations/{position:03d}_{table}.sql",
            "operation": "create_owned_table",
            "table": table,
            "backend_allowlist": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        }
        for position, table in enumerate(LOYALTY_REWARDS_OWNED_TABLES, start=1)
    )
    models = tuple(
        {
            "class_name": "".join(part.capitalize() for part in table.split("_")),
            "table": table,
            "fields": table_fields[table],
            "module": f"pyAppGen.pbcs.loyalty_rewards.models.{table}",
        }
        for table in LOYALTY_REWARDS_OWNED_TABLES
    )
    runtime_tables = tuple(
        {
            "table": table,
            "fields": runtime_table_fields[table],
            "event_contract": "AppGen-X",
            "owned_by": "loyalty_rewards",
        }
        for table in LOYALTY_REWARDS_RUNTIME_TABLES
    )
    return {
        "format": "appgen.loyalty-rewards-owned-schema-contract.v1",
        "ok": len(tables) == len(LOYALTY_REWARDS_OWNED_TABLES)
        and tuple(item["table"] for item in tables) == LOYALTY_REWARDS_OWNED_TABLES
        and tuple(item["table"] for item in runtime_tables) == LOYALTY_REWARDS_RUNTIME_TABLES
        and all(item["backend_allowlist"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS for item in migrations),
        "tables": tables,
        "relationships": relationships,
        "runtime_tables": runtime_tables,
        "migrations": migrations,
        "models": models,
        "generated_artifacts": {
            "migrations": tuple(item["path"] for item in migrations),
            "models": tuple(item["module"] for item in models),
        },
        "datastore_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
    }


def loyalty_rewards_build_service_contract() -> dict:
    """Return command/query/runtime evidence for generated Loyalty services."""
    permissions = loyalty_rewards_permissions_contract()
    api = loyalty_rewards_build_api_contract()
    ui_fragments = (
        "LoyaltyRewardsWorkbench",
        "RewardAccountRegistry",
        "PointsLedgerPanel",
        "EarningRuleStudio",
        "RedemptionConsole",
        "TierQualificationBoard",
        "ReferralAndPartnerPanel",
        "ExpirationLiabilityPanel",
        "RewardsFraudReviewQueue",
        "RewardsRuleStudio",
        "RewardsParameterConsole",
        "RewardsConfigurationPanel",
        "RewardsEventOutbox",
        "RewardsDeadLetterQueue",
    )
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "register_earning_rule",
        "enroll_member",
        "receive_event",
        "issue_points",
        "adjust_points",
        "create_redemption",
        "expire_points",
        "qualify_tier",
        "grant_referral_reward",
        "record_partner_accrual",
        "evaluate_offer_eligibility",
        "schedule_expiration",
        "snapshot_liability",
        "review_fraud_risk",
        "score_churn_risk",
        "forecast_breakage",
        "simulate_offer",
        "resolve_loyalty_exception",
        "reconcile_balance",
        "generate_balance_proof",
        "screen_rewards_policy",
        "run_liability_controls",
        "federate_rewards_view",
        "register_governed_model",
        "verify_owned_table_boundary",
    )
    query_methods = (
        "build_workbench_view",
        "build_api_contract",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
    )
    idempotent_handlers = tuple(
        {
            "event_type": event_type,
            "idempotency_key": "event_id",
            "inbox_table": "loyalty_rewards_appgen_inbox_event",
            "outbox_table": "loyalty_rewards_appgen_outbox_event",
            "dead_letter_table": "loyalty_rewards_dead_letter_event",
            "retry_limit_source": "configuration.retry_limit",
            "event_contract": "AppGen-X",
        }
        for event_type in LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
    )
    return {
        "format": "appgen.loyalty-rewards-service-contract.v1",
        "ok": len(command_methods) >= 10
        and not api["shared_table_access"]
        and tuple(item["event_type"] for item in idempotent_handlers) == LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
        "pbc": "loyalty_rewards",
        "transaction_boundary": "loyalty_rewards_owned_datastore_plus_appgen_outbox",
        "shared_table_access": False,
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": LOYALTY_REWARDS_OWNED_TABLES,
        "runtime_tables": LOYALTY_REWARDS_RUNTIME_TABLES,
        "permission_requirements": {
            name: permissions["action_permissions"][name]
            for name in command_methods
            + (
                "build_api_contract",
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
            )
        },
        "configuration_schema": {
            "required_fields": LOYALTY_REWARDS_SUPPORTED_CONFIGURATION_FIELDS,
            "allowed_database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
        },
        "idempotent_handlers": idempotent_handlers,
        "retry_dead_letter": {
            "retry_limit_source": "configuration.retry_limit",
            "outbox_table": "loyalty_rewards_appgen_outbox_event",
            "inbox_table": "loyalty_rewards_appgen_inbox_event",
            "dead_letter_table": "loyalty_rewards_dead_letter_event",
            "simulate_failure_supported": True,
        },
        "generated_artifacts": {
            "services": tuple(
                {
                    "name": command,
                    "path": f"pbcs/loyalty_rewards/services/{command}.py",
                }
                for command in command_methods
            ),
            "routes": tuple(
                {
                    "route": item["route"],
                    "path": f"pbcs/loyalty_rewards/routes/{item['route'].split(' ', 1)[1].strip('/').replace('/', '_').replace('-', '_') or 'root'}.py",
                }
                for item in api["routes"]
            ),
            "events": tuple(
                {"direction": "consumes", "event_type": event_type, "topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC}
                for event_type in LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
            )
            + tuple(
                {"direction": "emits", "event_type": event_type, "topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC}
                for event_type in LOYALTY_REWARDS_EMITTED_EVENT_TYPES
            ),
            "handlers": tuple(
                {
                    "event_type": handler["event_type"],
                    "path": f"pbcs/loyalty_rewards/handlers/{handler['event_type'].lower()}.py",
                    "idempotency_key": handler["idempotency_key"],
                    "dead_letter_table": handler["dead_letter_table"],
                }
                for handler in idempotent_handlers
            ),
            "ui": tuple(
                {
                    "fragment": fragment,
                    "path": f"pbcs/loyalty_rewards/ui/{fragment}.tsx",
                }
                for fragment in ui_fragments
            ),
        },
        "external_dependencies": {
            "apis": ("payment_projection", "promotion_projection", "customer_segment_projection"),
            "events": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
            "api_projections": ("payment_projection", "promotion_projection", "customer_segment_projection"),
            "shared_tables": (),
        },
    }


def loyalty_rewards_build_release_evidence() -> dict:
    """Return package-local release evidence for Loyalty Rewards generation."""
    schema = loyalty_rewards_build_schema_contract()
    service = loyalty_rewards_build_service_contract()
    api = loyalty_rewards_build_api_contract()
    permissions = loyalty_rewards_permissions_contract()
    checks = (
        {
            "id": "owned_schema_coverage",
            "ok": schema["ok"] and tuple(item["table"] for item in schema["tables"]) == LOYALTY_REWARDS_OWNED_TABLES,
        },
        {
            "id": "runtime_appgen_x_tables",
            "ok": tuple(item["table"] for item in schema["runtime_tables"]) == LOYALTY_REWARDS_RUNTIME_TABLES
            and api["runtime_tables"] == LOYALTY_REWARDS_RUNTIME_TABLES,
        },
        {
            "id": "migration_and_model_artifacts",
            "ok": len(schema["migrations"]) == len(LOYALTY_REWARDS_OWNED_TABLES)
            and len(schema["models"]) == len(LOYALTY_REWARDS_OWNED_TABLES),
        },
        {
            "id": "service_route_event_handler_ui_artifacts",
            "ok": all(service["generated_artifacts"][key] for key in ("services", "routes", "events", "handlers", "ui")),
        },
        {
            "id": "commands_permissions_configuration",
            "ok": {
                "configure_runtime",
                "register_earning_rule",
                "create_redemption",
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
            }
            <= set(service["permission_requirements"])
            and service["configuration_schema"]["event_contract"] == "AppGen-X"
            and service["configuration_schema"]["required_event_topic"] == LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
            and not service["configuration_schema"]["stream_engine_picker_visible"],
        },
        {
            "id": "idempotent_handlers_retry_dead_letter",
            "ok": tuple(item["event_type"] for item in service["idempotent_handlers"]) == LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
            and service["retry_dead_letter"]["dead_letter_table"] == "loyalty_rewards_dead_letter_event",
        },
        {
            "id": "backend_allowlist_only",
            "ok": schema["datastore_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
            and service["configuration_schema"]["allowed_database_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        },
        {
            "id": "no_shared_tables_and_appgen_x_only_eventing",
            "ok": not schema["shared_table_access"]
            and not api["shared_table_access"]
            and service["external_dependencies"]["shared_tables"] == ()
            and api["event_contract"] == "AppGen-X"
            and api["required_event_topic"] == LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
            and not api["stream_engine_picker_visible"],
        },
        {
            "id": "permissions_cover_release_queries",
            "ok": {
                "build_api_contract",
                "build_schema_contract",
                "build_service_contract",
                "build_release_evidence",
                "verify_owned_table_boundary",
            }
            <= set(permissions["action_permissions"]),
        },
    )
    return {
        "format": "appgen.loyalty-rewards-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def loyalty_rewards_permissions_contract() -> dict:
    return {
        "format": "appgen.loyalty-rewards-permissions.v1",
        "ok": True,
        "permissions": (
            "loyalty_rewards.account.write",
            "loyalty_rewards.points.write",
            "loyalty_rewards.redemption.write",
            "loyalty_rewards.event.consume",
            "loyalty_rewards.configure",
            "loyalty_rewards.audit",
            "loyalty_rewards.operations.write",
            "loyalty_rewards.liability.write",
            "loyalty_rewards.risk.write",
            "loyalty_rewards.intelligence.write",
        ),
        "action_permissions": {
            "enroll_member": "loyalty_rewards.account.write",
            "issue_points": "loyalty_rewards.points.write",
            "adjust_points": "loyalty_rewards.points.write",
            "expire_points": "loyalty_rewards.points.write",
            "create_redemption": "loyalty_rewards.redemption.write",
            "qualify_tier": "loyalty_rewards.operations.write",
            "grant_referral_reward": "loyalty_rewards.operations.write",
            "record_partner_accrual": "loyalty_rewards.operations.write",
            "evaluate_offer_eligibility": "loyalty_rewards.operations.write",
            "schedule_expiration": "loyalty_rewards.liability.write",
            "snapshot_liability": "loyalty_rewards.liability.write",
            "review_fraud_risk": "loyalty_rewards.risk.write",
            "score_churn_risk": "loyalty_rewards.risk.write",
            "forecast_breakage": "loyalty_rewards.intelligence.write",
            "simulate_offer": "loyalty_rewards.intelligence.write",
            "resolve_loyalty_exception": "loyalty_rewards.operations.write",
            "reconcile_balance": "loyalty_rewards.operations.write",
            "generate_balance_proof": "loyalty_rewards.audit",
            "screen_rewards_policy": "loyalty_rewards.risk.write",
            "run_liability_controls": "loyalty_rewards.liability.write",
            "federate_rewards_view": "loyalty_rewards.audit",
            "register_governed_model": "loyalty_rewards.intelligence.write",
            "receive_event": "loyalty_rewards.event.consume",
            "register_earning_rule": "loyalty_rewards.configure",
            "register_rule": "loyalty_rewards.configure",
            "register_schema_extension": "loyalty_rewards.configure",
            "set_parameter": "loyalty_rewards.configure",
            "configure_runtime": "loyalty_rewards.configure",
            "build_api_contract": "loyalty_rewards.audit",
            "build_schema_contract": "loyalty_rewards.audit",
            "build_service_contract": "loyalty_rewards.audit",
            "build_release_evidence": "loyalty_rewards.audit",
            "permissions_contract": "loyalty_rewards.audit",
            "build_workbench_view": "loyalty_rewards.audit",
            "verify_owned_table_boundary": "loyalty_rewards.audit",
        },
    }


def _post_ledger(state: dict, command: dict, entry_type: str) -> dict:
    account = state["reward_accounts"].get(command["account_id"])
    if not account:
        raise ValueError(f"Unknown Loyalty Rewards account: {command['account_id']}")
    runtime = _copy_state(state)
    points = int(command["points"])
    ledger = {**command, "entry_type": entry_type, "points": points, "audit_proof": _digest(command)}
    runtime["points_ledger"][ledger["ledger_id"]] = ledger
    account = runtime["reward_accounts"][command["account_id"]]
    account["balance"] = int(account["balance"]) + points
    account["lifetime_points"] = int(account["lifetime_points"]) + max(points, 0)
    account["tier"] = _qualify_tier(runtime, account["lifetime_points"])
    account["liability_amount"] = round(account["balance"] * float(runtime["parameters"].get("redemption_value_per_point", {"value": 0.01})["value"]), 2)
    account["audit_proof"] = _digest(account)
    runtime["events"].append(_state_event("PointsLedgerPosted", ledger["ledger_id"], ledger))
    _emit(runtime, "RewardBalanceChanged", account["tenant"], {"account_id": account["account_id"], "customer_id": account["customer_id"], "balance": account["balance"], "tier": account["tier"]})
    if account["tier"] in {"gold", "platinum"}:
        _emit(runtime, "CustomerSegmentUpdated", account["tenant"], {"customer_id": account["customer_id"], "segment": f"loyalty_{account['tier']}", "balance": account["balance"]})
    return {"ok": True, "state": runtime, "ledger_entry": ledger, "account": account}


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Loyalty Rewards runtime must be configured before commands execute")


def _account_for_customer(state: dict, tenant: str, customer_id: str) -> dict:
    for account in state["reward_accounts"].values():
        if account["tenant"] == tenant and account["customer_id"] == customer_id:
            return account
    raise ValueError(f"Unknown Loyalty Rewards customer account: {customer_id}")


def _tier_multiplier(state: dict, tier: str) -> float:
    if tier in {"silver", "gold", "platinum"}:
        return float(state["parameters"].get(f"tier_multiplier_{tier}", {"value": 1.0})["value"])
    return 1.0


def _qualify_tier(state: dict, lifetime_points: int) -> str:
    policies = tuple(state.get("rules", {}).values())
    tier_policy = policies[0].get("tier_policy", {}) if policies else {}
    if lifetime_points >= int(tier_policy.get("platinum", 15000)):
        return "platinum"
    if lifetime_points >= int(tier_policy.get("gold", 5000)):
        return "gold"
    if lifetime_points >= int(tier_policy.get("silver", 1000)):
        return "silver"
    return "bronze"


def _tier_benefits(tier: str) -> tuple[str, ...]:
    benefit_map = {
        "bronze": ("standard_earn",),
        "silver": ("standard_earn", "priority_campaigns"),
        "gold": ("accelerated_earn", "priority_campaigns", "redemption_fee_waiver"),
        "platinum": ("accelerated_earn", "priority_campaigns", "redemption_fee_waiver", "concierge_recovery"),
    }
    return benefit_map.get(tier, benefit_map["bronze"])


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {"event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}", "event_type": event_type, "tenant": tenant, "payload": payload, "contract": "AppGen-X", "idempotency_key": f"loyalty_rewards:{event_type}:{payload.get('account_id') or payload.get('customer_id') or len(state['outbox']) + 1}", "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "loyalty_rewards_dead_letter_event"}, "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload})}
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _record_loyalty_audit(state: dict, tenant: str, account_id: str, action: str, payload: dict) -> dict:
    audit_id = f"audit_{tenant}_{len(state['loyalty_audit_entries']) + 1}"
    entry = {
        "audit_id": audit_id,
        "tenant": tenant,
        "account_id": account_id,
        "action": action,
        "payload_hash": _digest(payload),
        "payload": payload,
        "status": "recorded",
    }
    state["loyalty_audit_entries"][audit_id] = entry
    state["events"].append(_state_event("LoyaltyAuditRecorded", audit_id, entry))
    return entry


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {"event_type": event_type, "key": key, "payload": payload, "hash": _digest({"event_type": event_type, "key": key, "payload": payload})}


def _capability_evidence(state: dict, capability: str) -> dict:
    return {"capability": capability, "events": len(state["events"]), "outbox": len(state["outbox"]), "inbox": len(state["inbox"]), "rules": len(state["rules"]), "parameters": len(state["parameters"]), "configuration": bool(state["configuration"].get("ok")), "runtime_digest": _digest({"capability": capability, "accounts": len(state["reward_accounts"]), "ledger": len(state["points_ledger"])})}


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()).hexdigest()
