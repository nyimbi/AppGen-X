import pytest

from pyAppGen.pbc import pbc_implementation_contract
from pyAppGen.pbc import pbc_implementation_release_audit
from pyAppGen.pbc import price_promotion_engine_apply_promotion
from pyAppGen.pbc import price_promotion_engine_build_api_contract
from pyAppGen.pbc import price_promotion_engine_build_workbench_view
from pyAppGen.pbc import price_promotion_engine_configure_runtime
from pyAppGen.pbc import price_promotion_engine_empty_state
from pyAppGen.pbc import price_promotion_engine_permissions_contract
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
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.price_promotion_engine import PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
from pyAppGen.pbcs.price_promotion_engine import implementation_contract
from pyAppGen.pbcs.price_promotion_engine import price_promotion_engine_build_release_evidence
from pyAppGen.pbcs.price_promotion_engine import price_promotion_engine_build_schema_contract
from pyAppGen.pbcs.price_promotion_engine import price_promotion_engine_build_service_contract
from pyAppGen.pbcs.price_promotion_engine import price_promotion_engine_register_schema_extension


def test_price_promotion_engine_runtime_exposes_hardened_contract_surface() -> None:
    runtime = price_promotion_engine_runtime_capabilities()
    smoke = price_promotion_engine_runtime_smoke()
    schema = price_promotion_engine_build_schema_contract()
    service = price_promotion_engine_build_service_contract()
    release = price_promotion_engine_build_release_evidence()
    local_contract = implementation_contract()

    assert runtime["format"] == "appgen.price-promotion-engine-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/price_promotion_engine"
    assert runtime["owned_tables"] == PRICE_PROMOTION_ENGINE_OWNED_TABLES
    assert runtime["runtime_tables"] == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    assert runtime["required_event_topic"] == PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
    assert runtime["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
    assert runtime["consumes"] == PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES
    assert runtime["emits"] == PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES
    assert len(runtime["standard_features"]) >= 25
    assert "campaign_budgets" in runtime["standard_features"]
    assert "performance_telemetry" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    assert schema["ok"] is True
    assert len(schema["tables"]) == len(PRICE_PROMOTION_ENGINE_OWNED_TABLES)
    assert len(schema["migrations"]) == len(PRICE_PROMOTION_ENGINE_OWNED_TABLES)
    assert tuple(item["table"] for item in schema["runtime_tables"]) == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    assert service["ok"] is True
    assert "receive_event" in service["idempotent_handlers"]
    assert "build_release_evidence" in service["query_methods"]
    assert release["ok"] is True
    assert not release["blocking_gaps"]

    assert local_contract["schema_contract"]["ok"] is True
    assert local_contract["service_contract"]["ok"] is True
    assert local_contract["release_evidence_contract"]["ok"] is True
    assert local_contract["runtime_tables"] == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    assert local_contract["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT

    contract = pbc_implementation_contract("price_promotion_engine")
    assert contract["source_package"]["ok"] is True
    assert contract["source_package"]["advanced_runtime"]["ok"] is True
    assert contract["source_package"]["schema_contract"]["ok"] is True
    assert contract["source_package"]["service_contract"]["ok"] is True
    assert contract["source_package"]["release_evidence_contract"]["ok"] is True
    assert contract["source_package"]["required_event_topic"] == PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
    assert contract["source_package"]["permissions_contract"]["action_permissions"]["build_release_evidence"] == "price_promotion_engine.audit"
    assert contract["source_package"]["ui_contract"]["ok"] is True
    assert "PriceSimulationLab" in contract["source_package"]["ui_contract"]["fragments"]
    assert pbc_implementation_release_audit(("price_promotion_engine",))["ok"] is True


def test_price_promotion_engine_runtime_covers_table_stakes_and_binding_evidence() -> None:
    state = _configured_state()
    state = price_promotion_engine_register_loyalty_tier(
        state,
        {"tier_id": "tier_ops", "tenant": "tenant_ops", "name": "Ops Tier", "rank": 5, "discount_percent": 5.0, "status": "active"},
    )["state"]
    extension = price_promotion_engine_register_schema_extension(
        state,
        "price_decision",
        {"pricing_model_features": "jsonb", "simulation_state": "jsonb"},
    )
    state = extension["state"]
    assert extension["extension"]["version"] == 1
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
            "price_list_id": "list_ops",
            "price_book_id": "book_ops",
            "channel": "digital_store",
            "customer_id": "cust_ops",
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
            "channels": ("digital_store",),
            "customer_ids": ("cust_ops",),
            "stackable": True,
            "status": "active",
            "budget_amount": 1000.0,
            "budget_currency": "USD",
            "approval_status": "approved",
        },
    )["state"]
    processed = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "segment_ops",
            "event_type": "CustomerSegmentUpdated",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_ops", "segment": "vip", "loyalty_tier_id": "tier_ops"},
        },
    )
    state = processed["state"]
    state = price_promotion_engine_receive_event(
        state,
        {
            "event_id": "forecast_ops",
            "event_type": "ForecastUpdated",
            "payload": {"tenant": "tenant_ops", "sku": "sku_ops", "demand_index": 1.1, "confidence": 0.95},
        },
    )["state"]
    quoted = price_promotion_engine_quote_price(
        state,
        {
            "decision_id": "decision_ops",
            "tenant": "tenant_ops",
            "customer_id": "cust_ops",
            "sku": "sku_ops",
            "region": "US",
            "currency": "USD",
            "channel": "digital_store",
            "quantity": 12,
            "promotion_codes": ("OPS10",),
        },
    )
    state = quoted["state"]
    assert quoted["price_decision"]["optimized_unit_price"] < 120.0
    assert quoted["price_decision"]["eligible_promotions"] == ("promo_ops",)
    assert quoted["price_decision"]["price_list_id"] == "list_ops"
    assert quoted["price_decision"]["price_book_id"] == "book_ops"
    state = price_promotion_engine_apply_promotion(state, "decision_ops", "promo_ops")["state"]
    assert state["outbox"][-1]["idempotency_key"].startswith("price_promotion_engine:PromotionApplied")
    assert state["outbox"][-1]["contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT

    workbench = price_promotion_engine_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["ok"] is True
    assert workbench["price_list_count"] == 1
    assert workbench["price_book_count"] == 1
    assert workbench["promotion_count"] == 1
    assert workbench["coupon_count"] == 1
    assert workbench["approval_count"] == 1
    assert workbench["budget_count"] == 1
    assert workbench["simulation_count"] == 1
    assert workbench["telemetry_count"] >= 2
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 13
    assert workbench["binding_evidence"]["runtime_tables"] == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    assert workbench["binding_evidence"]["eventing"]["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT

    ui_contract = price_promotion_engine_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert ui_contract["configuration_editor"]["required_event_topic"] == PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
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
    assert rendered["binding_evidence"]["tenant_counts"]["simulations"] == 1

    api_contract = price_promotion_engine_build_api_contract()
    assert api_contract["database_backends"] == PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
    assert api_contract["event_contract"] == PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
    assert api_contract["required_event_topic"] == PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
    assert api_contract["stream_engine_picker_visible"] is False
    assert api_contract["shared_table_access"] is False
    assert {route["command"] for route in api_contract["routes"] if "command" in route} >= {
        "register_price_rule",
        "register_promotion",
        "register_loyalty_tier",
        "quote_price",
        "apply_promotion",
        "receive_event",
    }
    assert {route["query"] for route in api_contract["routes"] if "query" in route} >= {
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    }
    permissions = price_promotion_engine_permissions_contract()
    assert permissions["action_permissions"]["verify_owned_table_boundary"] == "price_promotion_engine.audit"
    assert permissions["action_permissions"]["build_release_evidence"] == "price_promotion_engine.audit"
    assert processed["handler"]["status"] == "processed"


def test_price_promotion_engine_rejects_invalid_inputs_and_proves_release_boundary_and_dead_letters() -> None:
    state = price_promotion_engine_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        price_promotion_engine_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
                "retry_limit": 3,
                "default_currency": "USD",
                "supported_currencies": ("USD",),
                "supported_regions": ("US",),
                "pricing_calendars": ("standard",),
                "default_timezone": "UTC",
                "decision_mode": "policy",
                "workbench_limit": 50,
                "approval_mode": "manager_review",
                "simulation_horizon_days": 30,
                "telemetry_window_minutes": 15,
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
    duplicate = price_promotion_engine_receive_event(
        failed["state"],
        {
            "event_id": "evt_dup",
            "event_type": "CustomerSegmentUpdated",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_dup", "segment": "growth"},
        },
    )
    duplicate = price_promotion_engine_receive_event(
        duplicate["state"],
        {
            "event_id": "evt_dup",
            "event_type": "CustomerSegmentUpdated",
            "payload": {"tenant": "tenant_ops", "customer_id": "cust_dup", "segment": "growth"},
        },
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1
    assert duplicate["handler"]["status"] == "duplicate"

    boundary = price_promotion_engine_verify_owned_table_boundary(
        (
            "price_list",
            "promotion_approval",
            PRICE_PROMOTION_ENGINE_RUNTIME_TABLES[0],
            "customer_segment_projection",
            "ForecastUpdated",
        )
    )
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == PRICE_PROMOTION_ENGINE_OWNED_TABLES
    assert boundary["runtime_tables"] == PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()
    assert "customer_segment_projection" in boundary["declared_dependencies"]["api_projections"]
    violated = price_promotion_engine_verify_owned_table_boundary(("customer_segment",))
    assert violated["ok"] is False
    assert violated["violations"] == ("customer_segment",)
    with pytest.raises(ValueError, match="cannot extend non-owned table"):
        price_promotion_engine_register_schema_extension(state, "customer_segment", {"segment": "text"})

    release = price_promotion_engine_build_release_evidence()
    assert release["ok"] is True
    assert not release["blocking_gaps"]
    assert {check["id"] for check in release["checks"]} >= {
        "owned_schema_depth",
        "service_contract_depth",
        "event_idempotency_evidence",
        "table_stakes_coverage",
    }


def _configured_state() -> dict:
    state = price_promotion_engine_empty_state()
    state = price_promotion_engine_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD",),
            "supported_regions": ("US",),
            "pricing_calendars": ("standard", "holiday"),
            "default_timezone": "UTC",
            "decision_mode": "policy",
            "workbench_limit": 50,
            "approval_mode": "manager_review",
            "simulation_horizon_days": 30,
            "telemetry_window_minutes": 15,
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
        ("approval_discount_threshold_percent", 15.0),
        ("campaign_budget_guardrail", 0.9),
        ("coupon_reuse_limit", 5),
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
            "stacking_policy": {"max_promotions": 2, "group": "ops"},
            "exclusion_policy": {"excluded_promotion_ids": (), "reason": "none"},
            "approval_policy": {"required_above_discount": 15.0, "approver_role": "pricing_manager"},
            "budget_policy": {"default_budget_amount": 1000.0, "currency": "USD"},
        },
    )["state"]
    return state
