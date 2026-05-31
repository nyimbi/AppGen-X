"""Domain behavior checks for waste recycling operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import waste_recycling_operations_runtime_capabilities
from ..ui import waste_recycling_operations_render_workbench, waste_recycling_operations_ui_contract
from ..waste_recycling_operations_control import (
    CONTROL_SPECS,
    WASTE_ALLOWED_DATABASE_BACKENDS,
    WASTE_CONTROL_OWNED_TABLES,
    WASTE_DECLARED_DEPENDENCIES,
    WASTE_REQUIRED_EVENT_TOPIC,
    evaluate_waste_recycling_operations_control,
    improve1_waste_recycling_operations_control_contract,
    sample_payload_for,
)


def test_all_50_waste_controls_are_executable_and_owned():
    contract = improve1_waste_recycling_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == WASTE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /waste-recycling-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("WasteRecyclingOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == WASTE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in WASTE_CONTROL_OWNED_TABLES
            assert table.startswith("waste_recycling_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in WASTE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_waste_control_contract():
    runtime = waste_recycling_operations_runtime_capabilities()
    ui = waste_recycling_operations_ui_contract()
    workbench = waste_recycling_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["waste_recycling_operations_control"]["capability_count"] == 50
    assert "evaluate_waste_recycling_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["waste_recycling_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["waste_recycling_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["waste_recycling_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["waste_recycling_operations_control"]["ok"] is True


def test_waste_domains_fail_closed_without_evidence():
    for feature in (1,2,3,4,5,6,7,8,15,17,18,19,20,29,30,31,34,35,44,45,49,50):
        result = evaluate_waste_recycling_operations_control(feature, {"route_service_evidence_complete": False})
        assert result["ok"] is False
        assert any("route service" in finding for finding in result["findings"])
    for feature in (9,10,11,12,13,14,16,21,22,26,27,32,33,43,46,50):
        result = evaluate_waste_recycling_operations_control(feature, {"material_facility_evidence_complete": False})
        assert result["ok"] is False
        assert any("material streams" in finding for finding in result["findings"])
    for feature in (10,12,14,23,24,28,30,31,33,36,39,42,44,48,50):
        result = evaluate_waste_recycling_operations_control(feature, {"compliance_safety_evidence_complete": False})
        assert result["ok"] is False
        assert any("contamination" in finding for finding in result["findings"])
    for feature in (36,37,38,39,40,41,42,47,48,49,50):
        result = evaluate_waste_recycling_operations_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("rule parameters" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (8,10,12,14,15,18,19,23,28,29,30,31,33,37,38,39,42,49,50):
        result = evaluate_waste_recycling_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (14,18,23,28,30,31,33,39,42,49,50):
        result = evaluate_waste_recycling_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (37,38,39,49,50):
        result = evaluate_waste_recycling_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_waste_recycling_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_waste_recycling_operations_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_waste_recycling_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_waste_recycling_operations_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_waste_recycling_operations_control(4, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    route = sample_payload_for(1)
    assert route["route_lifecycle_id"].startswith("waste_route_lifecycle_model")
    assert route["waste_route_lifecycle_model_verified"] is True
    assert route["side_effects"] == ()
    hazmat = evaluate_waste_recycling_operations_control("hazardous_material_exception_handling")
    assert hazmat["ok"] is True
    assert "crew_safety_instruction" in hazmat["evidence"]["required_fields"]
    assert "disposal_path" in hazmat["evidence"]["required_fields"]
    boundary = CONTROL_SPECS[48]
    assert boundary["route"].endswith("/cross_pbc_boundary_proof")
    assert "no_foreign_mutation" in boundary["fields"]
