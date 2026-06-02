"""Domain behavior tests for price promotion improve1 controls."""

from ..pricing_control import (
    CONTROL_SPECS,
    PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PRICING_CONTROL_OWNED_TABLES,
    evaluate_pricing_control,
    improve1_pricing_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
    price_promotion_engine_configure_runtime,
    price_promotion_engine_empty_state,
    price_promotion_engine_runtime_capabilities,
)
from ..ui import price_promotion_engine_render_workbench, price_promotion_engine_ui_contract


def _configured_state():
    return price_promotion_engine_configure_runtime(
        price_promotion_engine_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "supported_currencies": ("USD", "EUR"),
            "supported_regions": ("global",),
            "pricing_calendars": ("standard",),
            "default_timezone": "UTC",
            "decision_mode": "governed",
            "workbench_limit": 50,
            "approval_mode": "threshold",
            "simulation_horizon_days": 90,
            "telemetry_window_minutes": 60,
        },
    )["state"]


def test_all_fifty_pricing_controls_are_executable_and_owned():
    contract = improve1_pricing_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PRICING_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_pricing_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PRICING_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PricePromotionEngine")
        assert result["evidence"]["service_api"].startswith("POST /price-promotion-engine/improve1/")


def test_runtime_ui_and_release_expose_pricing_control_contract():
    runtime = price_promotion_engine_runtime_capabilities()
    ui = price_promotion_engine_ui_contract()
    workbench = price_promotion_engine_render_workbench(
        _configured_state(),
        tenant="default",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["pricing_control"]["capability_count"] == 50
    assert "evaluate_pricing_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["pricing_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["pricing_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["pricing_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_pricing_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_price_book_quote_margin_promotion_and_coupon_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 6, 7, 9, 10, 11, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 24):
        _blocked(feature_number)


def test_projection_event_boundary_agent_and_release_controls_are_gated():
    for feature_number in (26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 38, 39, 40, 41, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_pricing_control(12, {"pricing_risk_evidence_complete": False})["ok"] is False
    assert evaluate_pricing_control(48, {"agent_preview_only": False})["ok"] is False
    assert evaluate_pricing_control(21, {"human_confirmation": False})["ok"] is False
    assert evaluate_pricing_control(29, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_pricing_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_pricing_control(39, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_pricing_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_pricing_control(40, {"shared_table_access": True})
    direct_dependency = evaluate_pricing_control(27, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(10)
    result = evaluate_pricing_control(10, payload)
    assert result["ok"] is True
    assert payload["decision_trace_id"].startswith("quote_decision_trace")
    assert payload["quote_decision_trace_verified"] is True
    assert result["side_effects"] == ()
