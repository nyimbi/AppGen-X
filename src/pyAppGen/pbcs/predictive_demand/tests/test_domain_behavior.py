"""Domain behavior tests for predictive demand improve1 controls."""

from ..demand_control import (
    CONTROL_SPECS,
    DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
    DEMAND_CONTROL_OWNED_TABLES,
    evaluate_demand_control,
    improve1_demand_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
    predictive_demand_configure_runtime,
    predictive_demand_empty_state,
    predictive_demand_runtime_capabilities,
)
from ..ui import predictive_demand_render_workbench, predictive_demand_ui_contract


def _configured_state():
    return predictive_demand_configure_runtime(
        predictive_demand_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_uom": "each",
            "supported_regions": ("global",),
            "supported_signal_types": ("shipment", "inventory", "operational", "manual", "promotion"),
            "planning_granularity": "sku_location_day",
            "default_timezone": "UTC",
            "shortage_policy": "service_level",
            "workbench_limit": 50,
        },
    )["state"]


def test_all_fifty_demand_controls_are_executable_and_owned():
    contract = improve1_demand_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == DEMAND_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_demand_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in DEMAND_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PredictiveDemand")
        assert result["evidence"]["service_api"].startswith("POST /predictive-demand/improve1/")


def test_runtime_ui_and_release_expose_demand_control_contract():
    runtime = predictive_demand_runtime_capabilities()
    ui = predictive_demand_ui_contract()
    workbench = predictive_demand_render_workbench(
        _configured_state(),
        tenant="default",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["demand_control"]["capability_count"] == 50
    assert "evaluate_demand_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["demand_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["demand_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["demand_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_demand_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_signal_forecast_probabilistic_consensus_and_shortage_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 28, 29):
        _blocked(feature_number)


def test_agent_publication_boundary_privacy_and_release_controls_are_gated():
    for feature_number in (30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_demand_control(29, {"demand_risk_evidence_complete": False})["ok"] is False
    assert evaluate_demand_control(39, {"agent_preview_only": False})["ok"] is False
    assert evaluate_demand_control(20, {"human_confirmation": False})["ok"] is False
    assert evaluate_demand_control(46, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_demand_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_demand_control(48, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_demand_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_demand_control(37, {"shared_table_access": True})
    direct_dependency = evaluate_demand_control(25, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(29)
    result = evaluate_demand_control(29, payload)
    assert result["ok"] is True
    assert payload["shortage_warning_id"].startswith("shortage_risk_early_warning_system")
    assert payload["shortage_risk_early_warning_system_verified"] is True
    assert result["side_effects"] == ()
