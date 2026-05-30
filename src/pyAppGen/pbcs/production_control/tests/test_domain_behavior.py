"""Domain behavior tests for production control improve1 controls."""

from ..production_control_control import (
    CONTROL_SPECS,
    PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PRODUCTION_CONTROL_CONTROL_OWNED_TABLES,
    evaluate_production_control,
    improve1_production_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
    production_control_configure_runtime,
    production_control_empty_state,
    production_control_runtime_capabilities,
)
from ..ui import production_control_render_workbench, production_control_ui_contract


def _configured_state():
    return production_control_configure_runtime(
        production_control_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("factory_east", "factory_west"),
            "allowed_work_center_types": ("assembly", "test", "pack"),
            "allowed_downtime_reasons": ("maintenance", "material", "quality", "microstop"),
            "allowed_production_routes": ("make", "assemble", "inspect"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_production_controls_are_executable_and_owned():
    contract = improve1_production_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PRODUCTION_CONTROL_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_production_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PRODUCTION_CONTROL_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("ProductionControl")
        assert result["evidence"]["service_api"].startswith("POST /production-control/improve1/")


def test_runtime_ui_and_release_expose_production_control_contract():
    runtime = production_control_runtime_capabilities()
    ui = production_control_ui_contract()
    workbench = production_control_render_workbench(
        _configured_state(),
        tenant="tenant_demo",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["production_control"]["capability_count"] == 50
    assert "evaluate_production_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["production_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["production_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["production_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_production_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_work_center_order_schedule_execution_and_quality_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 16, 17, 18, 21, 22, 23, 24):
        _blocked(feature_number)


def test_oee_exception_event_boundary_agent_and_release_controls_are_gated():
    for feature_number in (25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 38, 39, 41, 42, 43, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_production_control(10, {"production_risk_evidence_complete": False})["ok"] is False
    assert evaluate_production_control(39, {"agent_preview_only": False})["ok"] is False
    assert evaluate_production_control(23, {"human_confirmation": False})["ok"] is False
    assert evaluate_production_control(30, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_production_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_production_control(35, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_production_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_production_control(36, {"shared_table_access": True})
    direct_dependency = evaluate_production_control(13, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(10)
    result = evaluate_production_control(10, payload)
    assert result["ok"] is True
    assert payload["start_validation_id"].startswith("production_start_validation")
    assert payload["production_start_validation_verified"] is True
    assert result["side_effects"] == ()
