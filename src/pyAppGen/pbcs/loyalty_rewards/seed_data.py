"""Executable seed-data contract for the loyalty_rewards PBC."""

from __future__ import annotations

import copy

from .runtime import LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC


PBC_KEY = "loyalty_rewards"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_currency": "USD",
    "supported_currencies": ("USD", "KES"),
    "supported_regions": ("US", "KE"),
    "tier_calendar": "annual",
    "default_timezone": "UTC",
    "liability_mode": "reserved",
    "workbench_limit": 100,
}

DEFAULT_PARAMETERS = {
    "base_points_per_currency_unit": 10.0,
    "tier_multiplier_silver": 1.2,
    "tier_multiplier_gold": 1.6,
    "tier_multiplier_platinum": 2.1,
    "redemption_value_per_point": 0.01,
    "fraud_review_threshold": 0.72,
    "liability_reserve_percent": 8.0,
    "expiration_days": 365,
    "max_daily_earn_points": 100000,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "loyalty_rewards.default_program_policy",
        "tenant": "tenant_alpha",
        "scope": "loyalty_rewards",
        "status": "active",
        "allowed_currencies": ("USD", "KES"),
        "allowed_regions": ("US", "KE"),
        "earning_policy": {"payment_multiplier": 1.0, "partner_multiplier": 1.25},
        "redemption_policy": {"minimum_balance": 100, "max_percent_of_order": 0.5},
        "tier_policy": {"silver": 1000, "gold": 5000, "platinum": 15000},
    },
)

DEFAULT_EARNING_RULES = (
    {
        "earning_rule_id": "earn_card_spend_alpha",
        "tenant": "tenant_alpha",
        "name": "Card Spend Earn",
        "activity_type": "payment",
        "points_per_currency_unit": 10.0,
        "tier_multipliers": {"bronze": 1.0, "silver": 1.2, "gold": 1.6, "platinum": 2.1},
        "status": "active",
    },
)

DEFAULT_MEMBERS = (
    {
        "account_id": "acct_alpha",
        "tenant": "tenant_alpha",
        "customer_id": "cust_alpha",
        "currency": "USD",
        "region": "US",
        "tier": "bronze",
        "status": "active",
    },
)

DEFAULT_POINT_COMMANDS = (
    {
        "ledger_id": "ledger_alpha_payment",
        "account_id": "acct_alpha",
        "tenant": "tenant_alpha",
        "points": 1200,
        "source": "payment",
        "source_ref": "payment_alpha_001",
    },
)

DEFAULT_REDEMPTIONS = (
    {
        "redemption_id": "redeem_alpha",
        "account_id": "acct_alpha",
        "tenant": "tenant_alpha",
        "points": 250,
        "order_id": "order_alpha_001",
        "status": "reserved",
    },
)

DEFAULT_PARTNER_ACCRUALS = (
    {
        "partner_accrual_id": "partner_alpha_001",
        "tenant": "tenant_alpha",
        "account_id": "acct_alpha",
        "partner_id": "air_alpha",
        "activity_ref": "flt_001",
        "points": 180,
        "status": "posted",
    },
)

DEFAULT_OFFER_EVALUATIONS = (
    {
        "eligibility_id": "offer_alpha_001",
        "tenant": "tenant_alpha",
        "account_id": "acct_alpha",
        "offer_id": "offer_bonus_alpha",
        "required_tier": "silver",
    },
)

DEFAULT_FRAUD_REVIEWS = (
    {
        "review_id": "fraud_alpha_001",
        "tenant": "tenant_alpha",
        "account_id": "acct_alpha",
        "signals": {"velocity": 0.81, "device_risk": 0.63, "partner_risk": 0.52},
    },
)

DEFAULT_GOVERNED_MODELS = (
    {
        "model_id": "loyalty_propensity_2026_05",
        "tenant": "tenant_alpha",
        "model_type": "offer_propensity",
        "version": "2026.05",
        "status": "approved",
    },
)

DEFAULT_EVENT_COMMANDS = (
    {
        "event_type": "PaymentCaptured",
        "event_id": "payment_captured_alpha",
        "payload": {"tenant": "tenant_alpha", "customer_id": "cust_alpha", "amount": 125.5},
    },
)

SEED_DATA = (
    {
        "table": "loyalty_rewards_reward_account",
        "rows": ({"code": "LOYALTY-ACCOUNT-ALPHA", "status": "active"},),
    },
    {
        "table": "loyalty_rewards_earning_rule",
        "rows": ({"code": "LOYALTY-EARN-RULE-ALPHA", "status": "active"},),
    },
    {
        "table": "loyalty_rewards_partner_accrual",
        "rows": ({"code": "LOYALTY-PARTNER-ALPHA", "status": "posted"},),
    },
    {
        "table": "loyalty_rewards_loyalty_governed_model",
        "rows": ({"code": "LOYALTY-MODEL-ALPHA", "status": "approved"},),
    },
)


def _copy(value):
    return copy.deepcopy(value)


def default_configuration() -> dict:
    return _copy(DEFAULT_CONFIGURATION)


def default_parameter_values() -> dict:
    return _copy(DEFAULT_PARAMETERS)


def default_rules() -> tuple[dict, ...]:
    return _copy(DEFAULT_RULES)


def default_earning_rules() -> tuple[dict, ...]:
    return _copy(DEFAULT_EARNING_RULES)


def default_members() -> tuple[dict, ...]:
    return _copy(DEFAULT_MEMBERS)


def default_point_commands() -> tuple[dict, ...]:
    return _copy(DEFAULT_POINT_COMMANDS)


def default_redemptions() -> tuple[dict, ...]:
    return _copy(DEFAULT_REDEMPTIONS)


def default_partner_accruals() -> tuple[dict, ...]:
    return _copy(DEFAULT_PARTNER_ACCRUALS)


def default_offer_evaluations() -> tuple[dict, ...]:
    return _copy(DEFAULT_OFFER_EVALUATIONS)


def default_fraud_reviews() -> tuple[dict, ...]:
    return _copy(DEFAULT_FRAUD_REVIEWS)


def default_governed_models() -> tuple[dict, ...]:
    return _copy(DEFAULT_GOVERNED_MODELS)


def default_event_commands() -> tuple[dict, ...]:
    return _copy(DEFAULT_EVENT_COMMANDS)


def seed_plan() -> dict:
    """Return deterministic seed rows and standalone bootstrap bundles."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    bundle = {
        "configuration": default_configuration(),
        "parameters": default_parameter_values(),
        "rules": default_rules(),
        "earning_rules": default_earning_rules(),
        "members": default_members(),
        "point_commands": default_point_commands(),
        "redemptions": default_redemptions(),
        "partner_accruals": default_partner_accruals(),
        "offer_evaluations": default_offer_evaluations(),
        "fraud_reviews": default_fraud_reviews(),
        "governed_models": default_governed_models(),
        "events": default_event_commands(),
    }
    return {
        "ok": bool(SEED_DATA) and all(bundle.values()),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": _copy(SEED_DATA),
        "standalone_bundle": bundle,
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    """Validate seed ownership, bundle completeness, and topic alignment."""
    invalid_tables = tuple(item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_"))
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    plan = seed_plan()
    bundle = plan["standalone_bundle"]
    bundle_gaps = tuple(
        name
        for name in (
            "configuration",
            "parameters",
            "rules",
            "earning_rules",
            "members",
            "point_commands",
            "redemptions",
            "partner_accruals",
            "offer_evaluations",
            "fraud_reviews",
            "governed_models",
            "events",
        )
        if not bundle.get(name)
    )
    invalid_event_topic = bundle["configuration"]["event_topic"] != LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
    return {
        "ok": not invalid_tables and not invalid_rows and not bundle_gaps and not invalid_event_topic,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "bundle_gaps": bundle_gaps,
        "invalid_event_topic": invalid_event_topic,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    bundle = validation["plan"]["standalone_bundle"]
    return {
        "ok": validation["ok"]
        and bundle["configuration"]["database_backend"] == "postgresql"
        and len(bundle["members"]) >= 1
        and len(bundle["point_commands"]) >= 1
        and len(bundle["governed_models"]) >= 1,
        "validation": validation,
        "side_effects": (),
    }
