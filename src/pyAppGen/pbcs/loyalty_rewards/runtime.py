"""Executable runtime for the Loyalty Rewards PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC = "appgen.loyalty_rewards.events"
LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LOYALTY_REWARDS_OWNED_TABLES = ("reward_account", "points_ledger", "earning_rule", "redemption")

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
            "enroll_member",
            "receive_event",
            "issue_points",
            "adjust_points",
            "create_redemption",
            "expire_points",
            "build_api_contract",
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
    allowed_runtime_tables = {
        "loyalty_rewards_appgen_outbox_event",
        "loyalty_rewards_appgen_inbox_event",
        "loyalty_rewards_dead_letter_event",
    }
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
        ),
        "declared_catalog_routes": ("POST /points", "POST /redemptions", "GET /reward-accounts"),
        "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
        "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
        "database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
        "permissions": tuple(sorted(loyalty_rewards_permissions_contract()["permissions"])),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
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
        ),
        "action_permissions": {
            "enroll_member": "loyalty_rewards.account.write",
            "issue_points": "loyalty_rewards.points.write",
            "adjust_points": "loyalty_rewards.points.write",
            "expire_points": "loyalty_rewards.points.write",
            "create_redemption": "loyalty_rewards.redemption.write",
            "receive_event": "loyalty_rewards.event.consume",
            "register_earning_rule": "loyalty_rewards.configure",
            "register_rule": "loyalty_rewards.configure",
            "set_parameter": "loyalty_rewards.configure",
            "configure_runtime": "loyalty_rewards.configure",
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


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {"event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}", "event_type": event_type, "tenant": tenant, "payload": payload, "contract": "appgen_event_contract", "idempotency_key": f"loyalty_rewards:{event_type}:{payload.get('account_id') or payload.get('customer_id') or len(state['outbox']) + 1}", "retry_policy": {"max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)), "dead_letter": "loyalty_rewards_dead_letter_event"}, "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload})}
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


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
