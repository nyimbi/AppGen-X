import pytest

from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_OWNED_TABLES
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.loyalty_rewards import LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.loyalty_rewards import implementation_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_adjust_points
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_api_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_release_evidence
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_schema_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_service_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_build_workbench_view
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_configure_runtime
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_create_redemption
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_empty_state
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_enroll_member
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_issue_points
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_permissions_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_receive_event
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_register_earning_rule
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_register_rule
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_register_schema_extension
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_render_workbench
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_runtime_capabilities
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_runtime_smoke
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_set_parameter
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_ui_contract
from pyAppGen.pbcs.loyalty_rewards import loyalty_rewards_verify_owned_table_boundary


def test_loyalty_rewards_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = loyalty_rewards_runtime_capabilities()
    smoke = loyalty_rewards_runtime_smoke()
    contract = implementation_contract()
    schema = loyalty_rewards_build_schema_contract()
    service = loyalty_rewards_build_service_contract()
    release = loyalty_rewards_build_release_evidence()

    assert runtime["format"] == "appgen.loyalty-rewards-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/loyalty_rewards"
    assert runtime["owned_tables"] == LOYALTY_REWARDS_OWNED_TABLES
    assert {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(runtime["operations"])
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(LOYALTY_REWARDS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["api_contract"]["ok"] is True
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence_contract"]["ok"] is True
    assert contract["required_event_topic"] == LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
    assert contract["permissions_contract"]["action_permissions"]["create_redemption"] == "loyalty_rewards.redemption.write"
    assert schema["ok"] is True
    assert service["ok"] is True
    assert release["ok"] is True
    assert not release["blocking_gaps"]


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
    extension = loyalty_rewards_register_schema_extension(
        state, "reward_account", {"consent_evidence": "jsonb"}
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1
    state = loyalty_rewards_enroll_member(
        state,
        {"account_id": "acct_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "currency": "USD", "region": "US", "tier": "gold", "status": "active"},
    )["state"]
    state = loyalty_rewards_receive_event(
        state,
        {"event_id": "pay_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "amount": 100.0, "currency": "USD", "region": "US"}},
    )["state"]
    duplicate = loyalty_rewards_receive_event(
        state,
        {"event_id": "pay_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "amount": 100.0, "currency": "USD", "region": "US"}},
    )
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
    assert duplicate["handler"]["status"] == "duplicate"
    assert len(duplicate["state"]["inbox"]) == 1
    assert state["outbox"][-1]["idempotency_key"].startswith("loyalty_rewards:RewardBalanceChanged")
    assert {event["contract"] for event in state["outbox"]} == {"AppGen-X"}

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

    api_contract = loyalty_rewards_build_api_contract()
    assert api_contract["database_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == "AppGen-X"
    assert api_contract["required_event_topic"] == LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["shared_table_access"] is False
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "enroll_member",
        "issue_points",
        "adjust_points",
        "create_redemption",
        "receive_event",
    }
    assert {route["query"] for route in api_contract["routes"] if "query" in route} >= {
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    }
    permissions = loyalty_rewards_permissions_contract()
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "loyalty_rewards.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "loyalty_rewards.audit"

    schema = loyalty_rewards_build_schema_contract()
    assert tuple(item["table"] for item in schema["tables"]) == LOYALTY_REWARDS_OWNED_TABLES
    assert tuple(item["table"] for item in schema["runtime_tables"]) == (
        "loyalty_rewards_appgen_outbox_event",
        "loyalty_rewards_appgen_inbox_event",
        "loyalty_rewards_dead_letter_event",
    )
    assert len(schema["migrations"]) == len(LOYALTY_REWARDS_OWNED_TABLES)
    assert len(schema["models"]) == len(LOYALTY_REWARDS_OWNED_TABLES)
    assert schema["generated_artifacts"]["migrations"][0].startswith("pbcs/loyalty_rewards/migrations/")
    assert schema["generated_artifacts"]["models"][0].startswith("pyAppGen.pbcs.loyalty_rewards.models.")
    assert schema["shared_table_access"] is False
    assert schema["datastore_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS

    service = loyalty_rewards_build_service_contract()
    assert "create_redemption" in service["command_methods"]
    assert "build_release_evidence" in service["query_methods"]
    assert service["configuration_schema"]["allowed_database_backends"] == LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
    assert service["configuration_schema"]["required_event_topic"] == LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
    assert service["configuration_schema"]["event_contract"] == "AppGen-X"
    assert service["configuration_schema"]["stream_engine_picker_visible"] is False
    assert service["permission_requirements"]["receive_event"] == "loyalty_rewards.event.consume"
    assert service["permission_requirements"]["build_release_evidence"] == "loyalty_rewards.audit"
    assert tuple(item["event_type"] for item in service["idempotent_handlers"]) == LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
    assert all(item["idempotency_key"] == "event_id" for item in service["idempotent_handlers"])
    assert service["retry_dead_letter"]["inbox_table"] == "loyalty_rewards_appgen_inbox_event"
    assert service["retry_dead_letter"]["outbox_table"] == "loyalty_rewards_appgen_outbox_event"
    assert service["retry_dead_letter"]["dead_letter_table"] == "loyalty_rewards_dead_letter_event"
    assert service["retry_dead_letter"]["simulate_failure_supported"] is True
    assert service["external_dependencies"]["shared_tables"] == ()
    assert any(item["name"] == "create_redemption" for item in service["generated_artifacts"]["services"])
    assert any(item["route"] == "GET /loyalty-rewards/release-evidence" for item in service["generated_artifacts"]["routes"])
    assert any(item["event_type"] == "PaymentCaptured" and item["direction"] == "consumes" for item in service["generated_artifacts"]["events"])
    assert any(item["event_type"] == "RewardBalanceChanged" and item["direction"] == "emits" for item in service["generated_artifacts"]["events"])
    assert any(item["event_type"] == "PaymentCaptured" for item in service["generated_artifacts"]["handlers"])
    assert any(item["fragment"] == "RewardsEventOutbox" for item in service["generated_artifacts"]["ui"])

    release = loyalty_rewards_build_release_evidence()
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert {
        "owned_schema_coverage",
        "runtime_appgen_x_tables",
        "migration_and_model_artifacts",
        "service_route_event_handler_ui_artifacts",
        "commands_permissions_configuration",
        "idempotent_handlers_retry_dead_letter",
        "backend_allowlist_only",
        "no_shared_tables_and_appgen_x_only_eventing",
        "permissions_cover_release_queries",
    } == {check["id"] for check in release["checks"]}


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
    assert failed["handler"]["attempts"] == 3
    assert len(failed["state"]["dead_letter"]) == 1
    assert failed["state"]["dead_letter"][0]["handler"]["status"] == "dead_letter"

    boundary = loyalty_rewards_verify_owned_table_boundary(
        (
            "reward_account",
            "points_ledger",
            "earning_rule",
            "redemption",
            "PaymentCaptured",
            "promotion_projection",
            "loyalty_rewards_appgen_outbox_event",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("reward_account", "points_ledger", "earning_rule", "redemption")
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "promotion_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = loyalty_rewards_verify_owned_table_boundary(("customer_account",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer_account",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        loyalty_rewards_register_schema_extension(state, "customer_account", {"tier": "text"})


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
