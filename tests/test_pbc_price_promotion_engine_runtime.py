import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import price_promotion_engine_apply_promotion
from pyAppGen.pbc import price_promotion_engine_build_workbench_view
from pyAppGen.pbc import price_promotion_engine_configure_runtime
from pyAppGen.pbc import price_promotion_engine_empty_state
from pyAppGen.pbc import price_promotion_engine_quote_price
from pyAppGen.pbc import price_promotion_engine_receive_event
from pyAppGen.pbc import price_promotion_engine_register_loyalty_tier
from pyAppGen.pbc import price_promotion_engine_register_price_rule
from pyAppGen.pbc import price_promotion_engine_register_promotion
from pyAppGen.pbc import price_promotion_engine_register_rule
from pyAppGen.pbc import price_promotion_engine_render_workbench
from pyAppGen.pbc import price_promotion_engine_runtime_capabilities
from pyAppGen.pbc import price_promotion_engine_runtime_smoke
from pyAppGen.pbc import price_promotion_engine_set_parameter
from pyAppGen.pbc import price_promotion_engine_ui_contract
from pyAppGen.pbc import price_promotion_engine_verify_owned_table_boundary
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS


def test_price_promotion_engine_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = price_promotion_engine_runtime_capabilities()
    smoke = price_promotion_engine_runtime_smoke()

    assert runtime["format"] == "appgen.price-promotion-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/price_promotion_engine"
    assert runtime["owned_tables"] == PRICE_PROMOTION_ENGINE_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 18
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    contract = pbc_implementation_contract("price_promotion_engine")
    assert contract["source_package"]["ok"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "PriceConfigurationPanel" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("price_promotion_engine",))["ok"] is True


def test_price_promotion_engine_runtime_applies_rules_parameters_configuration_events_and_ui() -> None:
    state = _configured_state()
    state = price_promotion_engine_register_loyalty_tier(
        state,
        {"tier_id": "tier_ops", "tenant": "tenant_ops", "name": "Ops Tier", "rank": 5, "discount_percent": 5.0, "status": "active"},
    )["state"]
    state = price_promotion_engine_register_price_rule(
        state,
        {
            "price_rule_id": "price_ops",
            "tenant": "tenant_ops",
            "sku": "sku_ops",
            "region": "US",
            "currency": "USD",
            "base_price": 120.0,
            "cost": 60.0,
            "segments": ("growth", "vip"),
            "volume_breaks": ((10, 0.05), (20, 0.1)),
            "status": "active",
        },
    )["state"]
    state = price_promotion_engine_register_promotion(
        state,
        {
            "promotion_id": "promo_ops",
            "tenant": "tenant_ops",
            "code": "OPS10",
            "discount_percent": 10.0,
            "segments": ("growth", "vip"),
            "regions": ("US",),
            "currencies": ("USD",),
            "stackable": True,
            "status": "active",
        },
    )["state"]
    state = price_promotion_engine_receive_event(
        state,
        {"event_id": "segment_ops", "event_type": "CustomerSegmentUpdated", "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "segment": "vip", "loyalty_tier_id": "tier_ops"}},
    )["state"]
    state = price_promotion_engine_receive_event(
        state,
        {"event_id": "forecast_ops", "event_type": "ForecastUpdated", "payload": {"tenant": "tenant_ops", "sku": "sku_ops", "demand_index": 1.1, "confidence": 0.95}},
    )["state"]
    quoted = price_promotion_engine_quote_price(
        state,
        {"decision_id": "decision_ops", "tenant": "tenant_ops", "customer_id": "cust_ops", "sku": "sku_ops", "region": "US", "currency": "USD", "quantity": 12, "promotion_codes": ("OPS10",)},
    )
    state = quoted["state"]
    assert quoted["price_decision"]["optimized_unit_price"] < 120.0
    assert quoted["price_decision"]["eligible_promotions"] == ("promo_ops",)
    state = price_promotion_engine_apply_promotion(state, "decision_ops", "promo_ops")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("price_promotion_engine:PromotionApplied")

    workbench = price_promotion_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["price_rule_count"] == 1
    assert workbench["promotion_count"] == 1
    assert workbench["loyalty_tier_count"] == 1
    assert workbench["decision_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10

    ui_contract = price_promotion_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    rendered = price_promotion_engine_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "price_promotion_engine.price.write",
            "price_promotion_engine.promotion.write",
            "price_promotion_engine.quote",
            "price_promotion_engine.event.consume",
            "price_promotion_engine.configure",
            "price_promotion_engine.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == PRICE_PROMOTION_ENGINE_OWNED_TABLES


def test_price_promotion_engine_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = price_promotion_engine_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        price_promotion_engine_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.price_promotion.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "pricing_calendars": ("standard",),
                "default_timezone": "UTC",
                "decision_mode": "policy",
                "workbench_limit": 50,
            },
        )

    state = _configured_state()
    with pytest.raises(ValueError, match="Unsupported Price Promotion Engine parameter"):
        price_promotion_engine_set_parameter(state, "stream_engine", 1)

    failed = price_promotion_engine_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "ForecastUpdated", "payload": {"tenant": "tenant_ops", "sku": "sku_fail"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = price_promotion_engine_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ("price_rule", "promotion", "loyalty_tier", "price_decision")
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state() -> dict:
    state = price_promotion_engine_empty_state()
    state = price_promotion_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.price_promotion.events",
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "pricing_calendars": ("standard", "holiday"),
            "default_timezone": "UTC",
            "decision_mode": "policy",
            "workbench_limit": 50,
        },
    )["state"]
    for name, value in (
        ("margin_floor_percent", 15.0),
        ("promotion_stack_limit", 2),
        ("elasticity_weight", 0.25),
        ("forecast_weight", 0.25),
        ("segment_weight", 0.25),
        ("loyalty_weight", 0.25),
        ("risk_review_threshold", 0.8),
        ("discount_ceiling_percent", 40.0),
        ("decision_ttl_minutes", 60),
        ("workbench_limit", 50),
    ):
        state = price_promotion_engine_set_parameter(state, name, value)["state"]
    state = price_promotion_engine_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "price_promotion_engine",
            "status": "active",
            "allowed_currencies": ("USD",),
            "allowed_regions": ("US",),
            "allowed_segments": ("growth", "vip"),
            "promotion_policy": {"stackable": True, "requires_active_window": True},
            "margin_policy": {"floor_percent": 15.0, "review_above_risk": 0.8},
        },
    )["state"]
    return state
