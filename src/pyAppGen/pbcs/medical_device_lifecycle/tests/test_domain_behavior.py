"""Domain behavior tests for medical device lifecycle improve1 controls."""

from ..medical_device_control import (
    CONTROL_SPECS,
    MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MEDICAL_DEVICE_CONTROL_OWNED_TABLES,
    evaluate_medical_device_control,
    improve1_medical_device_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import medical_device_lifecycle_runtime_capabilities
from ..ui import medical_device_lifecycle_render_workbench, medical_device_lifecycle_ui_contract


def test_all_fifty_medical_device_controls_are_executable_and_owned():
    contract = improve1_medical_device_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MEDICAL_DEVICE_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_medical_device_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MEDICAL_DEVICE_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MedicalDeviceLifecycle")
        assert result["evidence"]["service_api"].startswith("POST /medical-device-lifecycle/improve1/")


def test_runtime_ui_and_release_expose_medical_device_control_contract():
    runtime = medical_device_lifecycle_runtime_capabilities()
    ui = medical_device_lifecycle_ui_contract()
    workbench = medical_device_lifecycle_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["medical_device_control"]["capability_count"] == 50
    assert "evaluate_medical_device_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["medical_device_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["medical_device_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["medical_device_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_medical_device_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_registry_assignment_implant_calibration_and_recall_controls_are_gated():
    for feature_number in (1, 2, 4, 5, 6, 9, 10, 11):
        _blocked(feature_number)


def test_firmware_cybersecurity_usage_training_incident_and_reporting_controls_are_gated():
    for feature_number in (12, 13, 14, 22, 23, 24, 31, 32):
        _blocked(feature_number)


def test_agent_boundary_disposal_simulation_proof_and_dsl_controls_are_gated():
    for feature_number in (29, 30, 33, 35, 36, 37, 38, 41, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_medical_device_control(29, {"human_confirmation": False})["ok"] is False
    assert evaluate_medical_device_control(30, {"human_confirmation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_medical_device_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_medical_device_control(33, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_medical_device_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_medical_device_control(49, {"shared_table_access": True})
    direct_dependency = evaluate_medical_device_control(35, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(41)
    result = evaluate_medical_device_control(41, payload)
    assert result["ok"] is True
    assert payload["cryptographic_device_evidence_proofs_verified"] is True
    assert result["side_effects"] == ()
