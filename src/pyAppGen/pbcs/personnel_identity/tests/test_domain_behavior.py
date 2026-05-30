"""Domain behavior tests for personnel identity improve1 controls."""

from ..identity_control import (
    CONTROL_SPECS,
    IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    IDENTITY_CONTROL_OWNED_TABLES,
    evaluate_identity_control,
    improve1_identity_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import personnel_identity_runtime_capabilities
from ..ui import personnel_identity_render_workbench, personnel_identity_ui_contract


def test_all_fifty_identity_controls_are_executable_and_owned():
    contract = improve1_identity_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_identity_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in IDENTITY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PersonnelIdentity")
        assert result["evidence"]["service_api"].startswith("POST /personnel-identity/improve1/")


def test_runtime_ui_and_release_expose_identity_control_contract():
    runtime = personnel_identity_runtime_capabilities()
    ui = personnel_identity_ui_contract()
    workbench = personnel_identity_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["identity_control"]["capability_count"] == 50
    assert "evaluate_identity_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["identity_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["identity_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["identity_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_identity_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_department_employee_role_privacy_and_provisioning_controls_are_gated():
    for feature_number in (1, 2, 3, 5, 6, 7, 8, 9, 11, 16, 17, 18, 21, 22, 23, 24, 25, 26, 29, 31):
        _blocked(feature_number)


def test_audit_agent_simulation_crypto_and_workforce_proof_controls_are_gated():
    for feature_number in (32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_identity_control(17, {"identity_risk_evidence_complete": False})["ok"] is False
    assert evaluate_identity_control(42, {"agent_preview_only": False})["ok"] is False
    assert evaluate_identity_control(16, {"human_confirmation": False})["ok"] is False
    assert evaluate_identity_control(44, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_identity_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_identity_control(39, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_identity_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_identity_control(40, {"shared_table_access": True})
    direct_dependency = evaluate_identity_control(23, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(5)
    result = evaluate_identity_control(5, payload)
    assert result["ok"] is True
    assert payload["identity_spine_id"].startswith("employee_identity_spine")
    assert payload["employee_identity_spine_verified"] is True
    assert result["side_effects"] == ()
