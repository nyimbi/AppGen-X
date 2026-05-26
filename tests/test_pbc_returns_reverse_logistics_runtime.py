import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import returns_reverse_logistics_authorize_return
from pyAppGen.pbc import returns_reverse_logistics_build_workbench_view
from pyAppGen.pbc import returns_reverse_logistics_configure_runtime
from pyAppGen.pbc import returns_reverse_logistics_create_return_label
from pyAppGen.pbc import returns_reverse_logistics_empty_state
from pyAppGen.pbc import returns_reverse_logistics_issue_credit_adjustment
from pyAppGen.pbc import returns_reverse_logistics_receive_event
from pyAppGen.pbc import returns_reverse_logistics_record_inspection_grade
from pyAppGen.pbc import returns_reverse_logistics_register_rule
from pyAppGen.pbc import returns_reverse_logistics_render_workbench
from pyAppGen.pbc import returns_reverse_logistics_runtime_capabilities
from pyAppGen.pbc import returns_reverse_logistics_runtime_smoke
from pyAppGen.pbc import returns_reverse_logistics_set_parameter
from pyAppGen.pbc import returns_reverse_logistics_ui_contract
from pyAppGen.pbcs.returns_reverse_logistics import RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS


def test_returns_reverse_logistics_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = returns_reverse_logistics_runtime_capabilities()
    smoke = returns_reverse_logistics_runtime_smoke()

    assert runtime["format"] == "appgen.returns-reverse-logistics-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/returns_reverse_logistics"
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(RETURNS_REVERSE_LOGISTICS_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("returns_reverse_logistics")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "ReturnConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("returns_reverse_logistics",))["ok"] is True


def test_returns_reverse_logistics_runtime_applies_rules_parameters_configuration_and_ui() -> None:
    state = returns_reverse_logistics_empty_state()
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.returns.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_carriers": ("parcel_green", "parcel_one"),
            "supported_dispositions": ("restock", "refurbish", "scrap"),
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("eligibility_window_days", 30),
        ("fraud_threshold", 0.72),
        ("recovery_floor", 0.35),
        ("carbon_weight", 0.25),
        ("route_switch_threshold", 0.12),
    ):
        state = returns_reverse_logistics_set_parameter(state, name, value)["state"]
    rule = returns_reverse_logistics_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "return_policy",
            "status": "active",
            "eligibility_policy": {"max_days_since_shipment": 30, "blocked_reasons": ("final_sale",), "minimum_payment_capture_ratio": 1.0},
            "label_policy": {"preferred_carriers": ("parcel_green",), "max_cost": 15.0},
            "inspection_policy": {"restock_min": 0.85, "refurbish_min": 0.55},
            "credit_policy": {"restock_factor": 0.9, "refurbish_factor": 0.65, "scrap_factor": 0.25},
        },
    )
    state = rule["state"]
    assert rule["rule"]["compiled_hash"]

    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_ship_ops",
            "event_type": "OrderShipped",
            "idempotency_key": "order:ops:v1",
            "payload": {
                "tenant": "tenant_ops",
                "order_id": "order_ops",
                "payment_id": "pay_ops",
                "customer_id": "cust_ops",
                "shipped_at": "2026-05-20",
                "days_since_shipped": 5,
                "return_window_days": 30,
                "final_sale": False,
                "items": ({"sku": "sku_ops", "quantity": 1, "unit_price": 120.0},),
            },
        },
    )["state"]
    state = returns_reverse_logistics_receive_event(
        state,
        {
            "event_id": "evt_pay_ops",
            "event_type": "PaymentCaptured",
            "idempotency_key": "payment:ops:v1",
            "payload": {"tenant": "tenant_ops", "payment_id": "pay_ops", "order_id": "order_ops", "captured_amount": 120.0, "currency": "USD", "ledger_account": "refund_liability"},
        },
    )["state"]
    authorization = returns_reverse_logistics_authorize_return(
        state,
        {
            "return_id": "ret_ops",
            "rma": "RMA-OPS",
            "tenant": "tenant_ops",
            "order_id": "order_ops",
            "payment_id": "pay_ops",
            "customer_id": "cust_ops",
            "reason": "damaged",
            "requested_at": "2026-05-25",
            "days_since_shipped": 5,
            "items": ({"sku": "sku_ops", "quantity": 1},),
        },
    )
    state = authorization["state"]
    assert authorization["return_authorization"]["status"] == "authorized"
    state = returns_reverse_logistics_create_return_label(
        state,
        {
            "label_id": "lbl_ops",
            "return_id": "ret_ops",
            "tenant": "tenant_ops",
            "origin": "Boston",
            "destination": "New York",
            "package_weight_kg": 1.2,
            "candidate_carriers": (
                {"carrier_id": "parcel_green", "availability": True, "cost": 9.0, "carbon_intensity": 50.0, "eta_hours": 20.0, "route_health": 0.9},
            ),
        },
    )["state"]
    state = returns_reverse_logistics_record_inspection_grade(
        state,
        {"inspection_id": "insp_ops", "return_id": "ret_ops", "tenant": "tenant_ops", "condition_score": 0.9, "completeness_score": 1.0, "packaging_intact": True},
    )["state"]
    adjustment = returns_reverse_logistics_issue_credit_adjustment(state, {"adjustment_id": "adj_ops", "return_id": "ret_ops", "tenant": "tenant_ops"})
    state = adjustment["state"]
    assert adjustment["credit_adjustment"]["status"] == "issued"
    assert state["outbox"][-1]["idempotency_key"].startswith("returns_reverse_logistics:CreditAdjustmentIssued")

    workbench = returns_reverse_logistics_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["return_count"] == 1
    assert workbench["label_count"] == 1
    assert workbench["inspection_count"] == 1
    assert workbench["credit_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 5

    ui_contract = returns_reverse_logistics_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert ui_contract["configuration_editor"]["user_eventing_choice"] is False
    rendered = returns_reverse_logistics_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "returns_reverse_logistics.authorize",
            "returns_reverse_logistics.label",
            "returns_reverse_logistics.inspect",
            "returns_reverse_logistics.adjust",
            "returns_reverse_logistics.audit",
            "returns_reverse_logistics.configure",
        ),
    )
    assert rendered["ok"] is True
    assert rendered["configuration_bound"] is True
    assert not rendered["locked_actions"]


def test_returns_reverse_logistics_rejects_invalid_runtime_inputs_and_records_dead_letters() -> None:
    state = returns_reverse_logistics_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        returns_reverse_logistics_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.returns.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_carriers": ("parcel_green",),
                "supported_dispositions": ("restock",),
            },
        )
    state = returns_reverse_logistics_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.returns.events",
            "retry_limit": 1,
            "default_currency": "USD",
            "supported_carriers": ("parcel_green",),
            "supported_dispositions": ("restock",),
        },
    )["state"]
    with pytest.raises(ValueError, match="Unsupported Returns Reverse Logistics parameter"):
        returns_reverse_logistics_set_parameter(state, "stream_engine", 1)
    failed = returns_reverse_logistics_receive_event(
        state,
        {"event_id": "evt_unknown", "event_type": "UnknownEvent", "idempotency_key": "unknown:1", "attempts": 1, "payload": {"tenant": "tenant_ops"}},
    )
    assert failed["ok"] is False
    assert failed["dead_lettered"] is True
    assert len(failed["state"]["dead_letter"]) == 1
