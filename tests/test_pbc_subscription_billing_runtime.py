import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import subscription_billing_build_api_contract
from pyAppGen.pbc import subscription_billing_build_workbench_view
from pyAppGen.pbc import subscription_billing_configure_runtime
from pyAppGen.pbc import subscription_billing_create_dunning_notice
from pyAppGen.pbc import subscription_billing_create_subscription
from pyAppGen.pbc import subscription_billing_empty_state
from pyAppGen.pbc import subscription_billing_generate_invoice
from pyAppGen.pbc import subscription_billing_receive_event
from pyAppGen.pbc import subscription_billing_record_usage
from pyAppGen.pbc import subscription_billing_register_plan
from pyAppGen.pbc import subscription_billing_register_rule
from pyAppGen.pbc import subscription_billing_register_schema_extension
from pyAppGen.pbc import subscription_billing_render_workbench
from pyAppGen.pbc import subscription_billing_runtime_capabilities
from pyAppGen.pbc import subscription_billing_runtime_smoke
from pyAppGen.pbc import subscription_billing_set_parameter
from pyAppGen.pbc import subscription_billing_permissions_contract
from pyAppGen.pbc import subscription_billing_ui_contract
from pyAppGen.pbc import subscription_billing_verify_owned_table_boundary
from pyAppGen.pbcs.subscription_billing import SUBSCRIPTION_BILLING_OWNED_TABLES
from pyAppGen.pbcs.subscription_billing import SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS


def test_subscription_billing_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = subscription_billing_runtime_capabilities()
    smoke = subscription_billing_runtime_smoke()

    assert runtime["format"] == "appgen.subscription-billing-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/subscription_billing"
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(SUBSCRIPTION_BILLING_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("subscription_billing")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert contract["source_package"]["api_contract"]["ok"] is True
    assert contract["source_package"]["permissions_contract"]["ok"] is True
    assert contract["source_package"]["owned_tables"] == SUBSCRIPTION_BILLING_OWNED_TABLES
    assert contract["source_package"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert "BillingConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("subscription_billing",))["ok"] is True


def test_subscription_billing_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = subscription_billing_empty_state()
    state = subscription_billing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.subscription.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "billing_calendars": ("monthly", "annual"),
            "default_timezone": "UTC",
            "invoice_approval_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("renewal_confidence_threshold", 0.7),
        ("churn_risk_threshold", 0.6),
        ("dunning_risk_threshold", 0.55),
        ("usage_rating_precision", 4),
        ("proration_rounding_precision", 2),
        ("retry_limit", 3),
        ("carbon_batch_window_hours", 8),
        ("discount_guardrail_percent", 30.0),
        ("approval_amount_threshold", 1000.0),
        ("workbench_limit", 50),
    ):
        state = subscription_billing_set_parameter(state, name, value)["state"]
    rule = subscription_billing_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "rule_type": "renewal",
            "allowed_plan_families": ("growth",),
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "renewal_policy": "auto_renew_with_payment_confirmation",
            "invoice_policy": "approve_below_threshold",
            "status": "active",
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]
    schema_extension = subscription_billing_register_schema_extension(
        state,
        "subscription",
        {"renewal_terms": "jsonb"},
    )
    state = schema_extension["state"]
    assert schema_extension["extension"]["version"] == 1

    state = subscription_billing_register_plan(
        state,
        {
            "plan_id": "plan_ops",
            "tenant": "tenant_ops",
            "family": "growth",
            "name": "Ops Growth",
            "currency": "USD",
            "region": "US",
            "billing_period": "monthly",
            "base_price": 80.0,
            "usage_rate": 2.0,
            "included_units": 10.0,
            "status": "active",
        },
    )["state"]
    state = subscription_billing_receive_event(
        state,
        {"event_id": "price_ops", "event_type": "PriceOptimized", "payload": {"tenant": "tenant_ops", "plan_id": "plan_ops", "optimized_rate": 1.75, "confidence": 0.9}},
    )["state"]
    state = subscription_billing_create_subscription(
        state,
        {"subscription_id": "sub_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "plan_id": "plan_ops", "start_date": "2026-01-01", "renewal_date": "2026-02-01", "region": "US", "currency": "USD", "seats": 4},
    )["state"]
    state = subscription_billing_record_usage(
        state,
        {"usage_id": "usage_ops", "tenant": "tenant_ops", "subscription_id": "sub_ops", "meter_name": "api_calls", "quantity": 35.0, "occurred_at": "2026-01-15T00:00:00Z"},
    )["state"]
    invoice = subscription_billing_generate_invoice(state, "sub_ops", period="2026-01")
    state = invoice["state"]
    state = subscription_billing_receive_event(
        state,
        {"event_id": "payment_ops", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "invoice_id": invoice["invoice"]["invoice_id"], "amount": invoice["invoice"]["amount"], "currency": "USD"}},
    )["state"]
    state = subscription_billing_create_dunning_notice(state, "sub_ops", reason="payment_watch")["state"]

    workbench = subscription_billing_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["subscription_count"] == 1
    assert workbench["invoice_count"] == 1
    assert workbench["paid_invoice_count"] == 1
    assert workbench["usage_count"] == 1
    assert workbench["dunning_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = subscription_billing_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = subscription_billing_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "subscription_billing.configure",
            "subscription_billing.subscription",
            "subscription_billing.usage",
            "subscription_billing.invoice",
            "subscription_billing.renewal",
            "subscription_billing.dunning",
            "subscription_billing.event",
            "subscription_billing.audit",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert not rendered["locked_actions"]

    api_contract = subscription_billing_build_api_contract()
    assert api_contract["ok"] is True
    assert api_contract["stream_engine_picker_visible"] is False
    assert {route["command"] for route in api_contract["routes"]} >= {
        "create_subscription",
        "record_usage",
        "generate_invoice",
        "renew_subscription",
        "create_dunning_notice",
    }
    permissions = subscription_billing_permissions_contract()
    assert "subscription_billing_admin" in permissions["roles"]
    assert "event_idempotency_required" in permissions["policy_controls"]
    boundary = subscription_billing_verify_owned_table_boundary(
        ("subscription", "billing_schedule", "payment_orchestration.PaymentCaptured", "tax_localization.POST /tax-quotes")
    )
    assert boundary["ok"] is True
    violated = subscription_billing_verify_owned_table_boundary(("customer",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer",)


def test_subscription_billing_rejects_invalid_runtime_inputs_and_records_dead_letters() -> None:
    state = subscription_billing_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        subscription_billing_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.subscription.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "billing_calendars": ("monthly",),
                "default_timezone": "UTC",
                "invoice_approval_mode": "policy",
                "workbench_limit": 50,
            },
        )
    state = subscription_billing_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.subscription.events",
            "retry_limit": 1,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "billing_calendars": ("monthly",),
            "default_timezone": "UTC",
            "invoice_approval_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    with pytest.raises(ValueError, match="Unsupported Subscription Billing parameter"):
        subscription_billing_set_parameter(state, "stream_engine", 1)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        subscription_billing_register_schema_extension(state, "customer", {"external_id": "text"})
    failed = subscription_billing_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "PaymentCaptured", "payload": {"tenant": "tenant_ops", "invoice_id": "inv_missing", "amount": 1, "currency": "USD"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1
