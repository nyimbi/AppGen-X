"""Domain behavior tests for quality assurance improve1 controls."""

from ..quality_assurance_control import (
    CONTROL_SPECS,
    QA_ALLOWED_DATABASE_BACKENDS,
    QA_OWNED_TABLES,
    evaluate_quality_assurance_control,
    improve1_quality_assurance_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
    quality_assurance_configure_runtime,
    quality_assurance_empty_state,
    quality_assurance_runtime_capabilities,
)
from ..ui import quality_assurance_render_workbench, quality_assurance_ui_contract


def _configured_state():
    return quality_assurance_configure_runtime(
        quality_assurance_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "allowed_sites": ("factory_east", "dc_east"),
            "allowed_inspection_sources": ("production", "receipt"),
            "allowed_hold_reasons": ("defect", "spc_breach", "supplier_review"),
            "allowed_dispositions": ("rework", "scrap", "release", "return_to_supplier"),
            "default_timezone": "UTC",
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_quality_assurance_controls_are_executable_and_owned():
    contract = improve1_quality_assurance_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == QA_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_quality_assurance_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in QA_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("QualityAssurance")
        assert result["evidence"]["service_api"].startswith("POST /quality-assurance/improve1/")


def test_runtime_ui_and_release_expose_quality_assurance_control_contract():
    state = _configured_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    runtime = quality_assurance_runtime_capabilities()
    ui = quality_assurance_ui_contract()
    workbench = quality_assurance_render_workbench(
        state,
        tenant="tenant-smoke",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["quality_assurance_control"]["capability_count"] == 50
    assert "evaluate_quality_assurance_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["quality_assurance_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["quality_assurance_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["quality_assurance_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_quality_assurance_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_inspection_calibration_spc_hold_and_capa_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 18, 19, 24):
        _blocked(feature_number)


def test_compliance_agent_boundary_resilience_and_release_controls_are_gated():
    for feature_number in (25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_quality_assurance_control(37, {"agent_preview_only": False})["ok"] is False
    assert evaluate_quality_assurance_control(15, {"supervisor_approval": False})["ok"] is False
    assert evaluate_quality_assurance_control(1, {"human_confirmation": False})["ok"] is False
    assert evaluate_quality_assurance_control(40, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_quality_assurance_control(25, {"compliance_evidence_complete": False})["ok"] is False
    assert evaluate_quality_assurance_control(23, {"quality_risk_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_quality_assurance_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_quality_assurance_control(32, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_quality_assurance_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_quality_assurance_control(33, {"shared_table_access": True})
    direct_dependency = evaluate_quality_assurance_control(4, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_quality_assurance_control(1, payload)
    assert result["ok"] is True
    assert payload["plan_readiness_id"].startswith("inspection_plan_readiness_gate")
    assert payload["inspection_plan_readiness_gate_verified"] is True
    assert result["side_effects"] == ()
