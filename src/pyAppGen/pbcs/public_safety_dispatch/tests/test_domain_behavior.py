"""Domain behavior tests for public safety dispatch improve1 controls."""

from ..public_safety_dispatch_control import (
    CONTROL_SPECS,
    DISPATCH_ALLOWED_DATABASE_BACKENDS,
    DISPATCH_OWNED_TABLES,
    evaluate_public_safety_dispatch_control,
    improve1_public_safety_dispatch_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PUBLIC_SAFETY_DISPATCH_REQUIRED_EVENT_TOPIC,
    public_safety_dispatch_configure_runtime,
    public_safety_dispatch_empty_state,
    public_safety_dispatch_runtime_capabilities,
)
from ..ui import public_safety_dispatch_render_workbench, public_safety_dispatch_ui_contract


def _configured_state():
    return public_safety_dispatch_configure_runtime(
        public_safety_dispatch_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PUBLIC_SAFETY_DISPATCH_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_public_safety_dispatch_controls_are_executable_and_owned():
    contract = improve1_public_safety_dispatch_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == DISPATCH_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_public_safety_dispatch_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in DISPATCH_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PublicSafetyDispatch")
        assert result["evidence"]["service_api"].startswith("POST /public-safety-dispatch/improve1/")


def test_runtime_ui_and_release_expose_public_safety_dispatch_control_contract():
    state = _configured_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    runtime = public_safety_dispatch_runtime_capabilities()
    ui = public_safety_dispatch_ui_contract()
    workbench = public_safety_dispatch_render_workbench(tenant="tenant_alpha")
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["public_safety_dispatch_control"]["capability_count"] == 50
    assert "evaluate_public_safety_dispatch_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["public_safety_dispatch_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["public_safety_dispatch_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["public_safety_dispatch_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_public_safety_dispatch_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_intake_location_unit_radio_and_records_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 16, 19, 20, 23, 24, 30, 33):
        _blocked(feature_number)


def test_ai_safety_supervisor_boundary_and_release_controls_are_gated():
    for feature_number in (21, 22, 25, 26, 27, 28, 29, 35, 36, 37, 38, 40, 41, 43, 44, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_public_safety_dispatch_control(36, {"agent_preview_only": False})["ok"] is False
    assert evaluate_public_safety_dispatch_control(29, {"supervisor_approval": False})["ok"] is False
    assert evaluate_public_safety_dispatch_control(1, {"human_confirmation": False})["ok"] is False
    assert evaluate_public_safety_dispatch_control(25, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_public_safety_dispatch_control(11, {"cad_chronology_valid": False})["ok"] is False
    assert evaluate_public_safety_dispatch_control(21, {"safety_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_public_safety_dispatch_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_public_safety_dispatch_control(39, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_public_safety_dispatch_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_public_safety_dispatch_control(44, {"shared_table_access": True})
    direct_dependency = evaluate_public_safety_dispatch_control(6, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_public_safety_dispatch_control(1, payload)
    assert result["ok"] is True
    assert payload["ng911_call_id"].startswith("ng911_call_intake_model")
    assert payload["ng911_call_intake_model_verified"] is True
    assert result["side_effects"] == ()
