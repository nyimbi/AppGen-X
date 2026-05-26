import pytest

from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_OWNED_TABLES
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_adjust_points
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_workbench_view
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_configure_runtime
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_create_redemption
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_empty_state
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_enroll_member
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_issue_points
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_receive_event
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_register_earning_rule
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_register_rule
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_render_workbench
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_runtime_capabilities
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_runtime_smoke
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_set_parameter
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_ui_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_verify_owned_table_boundary


def test_loyalty_rewards_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = loyalty_rewards_runtime_capabilities()
    smoke = loyalty_rewards_runtime_smoke()

    assert runtime["format"] == "appgen.loyalty-rewards-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/loyalty_rewards"
    assert runtime["owned_tables"] == LOYALTY_REWARDS_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]


def test_loyalty_rewards_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    state = loyalty_rewards_register_earning_rule(
        state,
        {
            "earning_rule_id": "earn_ops",
            "tenant": "tenant_ops",
            "name": "Payment Earn",
            "activity_type": "payment",
            "points_per_currency_unit": 10.0,
            "tier_multipliers": {"silver": 1.2, "gold": 1.5, "platinum": 2.0},
            "status": "active",
        },
    )["state"]
    state = loyalty_rewards_enroll_member(
        state,
        {"account_id": "acct_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "currency": "USD", "region": "US", "tier": "gold", "status": "active"},
    )["state"]
    state = loyalty_rewards_receive_event(
        state,
        {"event_id": "pay_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "amount": 100.0, "currency": "USD", "region": "US"}},
    )["state"]
    state = loyalty_rewards_issue_points(
        state,
        {"ledger_id": "bonus_ops", "account_id": "acct_ops", "tenant": "tenant_ops", "points": 250, "source": "referral", "source_ref": "ref_ops"},
    )["state"]
    state = loyalty_rewards_adjust_points(
        state,
        {"ledger_id": "adj_ops", "account_id": "acct_ops", "tenant": "tenant_ops", "points": 100, "reason": "service_recovery"},
    )["state"]
    state = loyalty_rewards_create_redemption(
        state,
        {"redemption_id": "red_ops", "account_id": "acct_ops", "tenant": "tenant_ops", "points": 500, "order_id": "ord_ops", "status": "reserved"},
    )["state"]
    assert state["reward_accounts"]["acct_ops"]["balance"] > 0
    assert state["outbox"][-1]["idempotency_key"].startswith("loyalty_rewards:RewardBalanceChanged")

    workbench = loyalty_rewards_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["account_count"] == 1
    assert workbench["ledger_entry_count"] == 4
    assert workbench["earning_rule_count"] == 1
    assert workbench["redemption_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = loyalty_rewards_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = loyalty_rewards_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "loyalty_rewards.account.write",
            "loyalty_rewards.points.write",
            "loyalty_rewards.redemption.write",
            "loyalty_rewards.event.consume",
            "loyalty_rewards.configure",
            "loyalty_rewards.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == LOYALTY_REWARDS_OWNED_TABLES


def test_loyalty_rewards_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = loyalty_rewards_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        loyalty_rewards_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.loyalty_rewards.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "tier_calendar": "annual",
                "default_timezone": "UTC",
                "liability_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Loyalty Rewards parameter"):
        loyalty_rewards_set_parameter(state, "stream_engine", 1)

    failed = loyalty_rewards_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "customer_id": "cust_missing"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = loyalty_rewards_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("reward_account", "points_ledger", "earning_rule", "redemption")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = loyalty_rewards_empty_state()
    state = loyalty_rewards_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.loyalty_rewards.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "tier_calendar": "annual",
            "default_timezone": "UTC",
            "liability_mode": "policy",
            "workbench_limit": 50,
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
        ("workbench_limit", 50),
    ):
        state = loyalty_rewards_set_parameter(state, name, value)["state"]
    state = loyalty_rewards_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "loyalty_rewards",
            "status": "active",
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "earning_policy": {"payment_multiplier": 1.0, "partner_multiplier": 1.2},
            "redemption_policy": {"minimum_balance": 100, "max_percent_of_order": 0.5},
            "tier_policy": {"silver": 1000, "gold": 5000, "platinum": 15000},
        },
    )["state"]
    return state
