"""Domain behavior tests for pharma quality improve1 controls."""

from ..quality_control import (
    CONTROL_SPECS,
    QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    QUALITY_CONTROL_OWNED_TABLES,
    evaluate_quality_control,
    improve1_quality_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import pharma_manufacturing_quality_runtime_capabilities
from ..ui import pharma_manufacturing_quality_render_workbench, pharma_manufacturing_quality_ui_contract


def test_all_fifty_quality_controls_are_executable_and_owned():
    contract = improve1_quality_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == QUALITY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_quality_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in QUALITY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PharmaManufacturingQuality")
        assert result["evidence"]["service_api"].startswith("POST /pharma-manufacturing-quality/improve1/")


def test_runtime_ui_and_release_expose_quality_control_contract():
    runtime = pharma_manufacturing_quality_runtime_capabilities()
    ui = pharma_manufacturing_quality_ui_contract()
    workbench = pharma_manufacturing_quality_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["quality_control"]["capability_count"] == 50
    assert "evaluate_quality_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["quality_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["quality_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["quality_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_quality_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_mbr_ebr_genealogy_deviation_capa_validation_and_release_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 19, 21, 23, 25):
        _blocked(feature_number)


def test_agent_recall_inspection_audit_crypto_and_composition_controls_are_gated():
    for feature_number in (27, 28, 29, 30, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_quality_control(18, {"quality_risk_evidence_complete": False})["ok"] is False
    assert evaluate_quality_control(27, {"agent_preview_only": False})["ok"] is False
    assert evaluate_quality_control(28, {"human_confirmation": False})["ok"] is False
    assert evaluate_quality_control(38, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_quality_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_quality_control(43, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_quality_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_quality_control(39, {"shared_table_access": True})
    direct_dependency = evaluate_quality_control(22, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(18)
    result = evaluate_quality_control(18, payload)
    assert result["ok"] is True
    assert payload["release_checklist_id"].startswith("batch_release_checklist")
    assert payload["batch_release_checklist_verified"] is True
    assert result["side_effects"] == ()
