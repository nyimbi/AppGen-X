"""Domain behavior checks for reinsurance management improve1 controls."""

from ..reinsurance_management_control import (
    CONTROL_SPECS,
    REINSURANCE_ALLOWED_DATABASE_BACKENDS,
    REINSURANCE_DECLARED_DEPENDENCIES,
    REINSURANCE_OWNED_TABLES,
    REINSURANCE_REQUIRED_EVENT_TOPIC,
    evaluate_reinsurance_management_control,
    improve1_reinsurance_management_control_contract,
    sample_payload_for,
)
from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import reinsurance_management_runtime_capabilities
from ..ui import reinsurance_management_render_workbench, reinsurance_management_ui_contract


def test_all_50_reinsurance_controls_are_executable_and_owned():
    contract = improve1_reinsurance_management_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == REINSURANCE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /reinsurance-management/improve1/")
        assert item["evidence"]["ui_surface"].startswith("ReinsuranceManagement")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == REINSURANCE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in REINSURANCE_OWNED_TABLES
            assert table.startswith("reinsurance_management_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in REINSURANCE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_reinsurance_control_contract():
    runtime = reinsurance_management_runtime_capabilities()
    ui = reinsurance_management_ui_contract()
    workbench = reinsurance_management_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["reinsurance_management_control"]["capability_count"] == 50
    assert "evaluate_reinsurance_management_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["reinsurance_management_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["reinsurance_management_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["reinsurance_management_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["reinsurance_management_control"]["ok"] is True


def test_financial_exposure_and_document_controls_fail_closed_without_evidence():
    for feature in (8, 13, 15, 17, 18, 19, 20, 21, 22, 23, 25, 31, 34, 45, 46, 49):
        result = evaluate_reinsurance_management_control(feature, {"financial_reconciliation_complete": False})
        assert result["ok"] is False
        assert any("financial reconciliation" in finding for finding in result["findings"])

    for feature in (1, 4, 7, 9, 10, 24, 28, 29, 30, 42, 43, 49, 50):
        result = evaluate_reinsurance_management_control(feature, {"exposure_evidence_complete": False})
        assert result["ok"] is False
        assert any("exposure evidence" in finding for finding in result["findings"])

    for feature in (1, 2, 5, 6, 11, 12, 16, 26, 27, 31, 32, 36, 37, 41, 46, 47):
        result = evaluate_reinsurance_management_control(feature, {"document_evidence_complete": False})
        assert result["ok"] is False
        assert any("document evidence" in finding for finding in result["findings"])


def test_treaty_placement_agent_and_approval_controls_are_gated():
    for feature in (2, 5, 6, 8, 13, 16, 17, 18, 21, 23, 25, 28, 31, 32, 35, 36, 37, 38, 42, 46, 47, 50):
        result = evaluate_reinsurance_management_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (2, 4, 5, 6, 8, 13, 16, 17, 18, 19, 21, 23, 25, 28, 31, 32, 35, 38, 39, 41, 46, 47, 50):
        result = evaluate_reinsurance_management_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (6, 31, 35, 36, 37, 38, 44, 47, 50):
        result = evaluate_reinsurance_management_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("preview-only" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_reinsurance_management_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_reinsurance_management_control(39, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_reinsurance_management_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_reinsurance_management_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_reinsurance_management_control(22, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    treaty = sample_payload_for(1)
    assert treaty["treaty_type"].startswith("treaty_structure_model")
    assert treaty["treaty_structure_model_verified"] is True
    assert treaty["side_effects"] == ()

    cession_trace = evaluate_reinsurance_management_control("cession_calculation_trace")
    assert cession_trace["ok"] is True
    assert "gross_amount" in cession_trace["evidence"]["required_fields"]
    assert "commission_amount" in cession_trace["evidence"]["required_fields"]

    boundary = CONTROL_SPECS[48]
    assert boundary["route"].endswith("/cross_pbc_boundary_proof")
    assert "dependency_reference" in boundary["fields"]
