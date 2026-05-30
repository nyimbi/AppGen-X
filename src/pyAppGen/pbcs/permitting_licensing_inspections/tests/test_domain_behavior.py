"""Domain behavior tests for permitting improve1 controls."""

from ..permit_control import (
    CONTROL_SPECS,
    PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PERMIT_CONTROL_OWNED_TABLES,
    evaluate_permit_control,
    improve1_permit_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import permitting_licensing_inspections_runtime_capabilities
from ..ui import permitting_licensing_inspections_render_workbench, permitting_licensing_inspections_ui_contract


def test_all_fifty_permit_controls_are_executable_and_owned():
    contract = improve1_permit_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PERMIT_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_permit_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PERMIT_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PermittingLicensingInspections")
        assert result["evidence"]["service_api"].startswith("POST /permitting-licensing-inspections/improve1/")


def test_runtime_ui_and_release_expose_permit_control_contract():
    runtime = permitting_licensing_inspections_runtime_capabilities()
    ui = permitting_licensing_inspections_ui_contract()
    workbench = permitting_licensing_inspections_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["permit_control"]["capability_count"] == 50
    assert "evaluate_permit_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["permit_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["permit_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["permit_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_permit_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_intake_plan_review_fee_issuance_and_inspection_controls_are_gated():
    for feature_number in (1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17):
        _blocked(feature_number)


def test_notice_hearing_portal_agent_policy_and_go_live_controls_are_gated():
    for feature_number in (18, 19, 23, 24, 25, 26, 28, 29, 32, 33, 34, 35, 36, 37, 38, 40, 44, 45, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_permit_control(16, {"permit_risk_evidence_complete": False})["ok"] is False
    assert evaluate_permit_control(34, {"agent_preview_only": False})["ok"] is False
    assert evaluate_permit_control(9, {"human_confirmation": False})["ok"] is False
    assert evaluate_permit_control(41, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_permit_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_permit_control(29, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_permit_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_permit_control(44, {"shared_table_access": True})
    direct_dependency = evaluate_permit_control(38, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(9)
    result = evaluate_permit_control(9, payload)
    assert result["ok"] is True
    assert payload["issuance_gate_id"].startswith("permit_issuance_readiness_gate")
    assert payload["permit_issuance_readiness_gate_verified"] is True
    assert result["side_effects"] == ()
