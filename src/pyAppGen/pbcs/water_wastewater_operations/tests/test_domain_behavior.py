"""Domain behavior checks for water wastewater operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import water_wastewater_operations_runtime_capabilities
from ..ui import water_wastewater_operations_render_workbench, water_wastewater_operations_ui_contract
from ..water_wastewater_operations_control import (
    CONTROL_SPECS, WATER_ALLOWED_DATABASE_BACKENDS, WATER_CONTROL_OWNED_TABLES, WATER_DECLARED_DEPENDENCIES,
    WATER_REQUIRED_EVENT_TOPIC, evaluate_water_wastewater_operations_control,
    improve1_water_wastewater_operations_control_contract, sample_payload_for,
)


def test_all_50_water_controls_are_executable_and_owned():
    contract = improve1_water_wastewater_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == WATER_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["service_api"].startswith("POST /water-wastewater-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("WaterWastewaterOperations")
        assert item["evidence"]["allowed_database_backends"] == WATER_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in WATER_CONTROL_OWNED_TABLES
            assert table.startswith("water_wastewater_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in WATER_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_water_control_contract():
    runtime = water_wastewater_operations_runtime_capabilities()
    ui = water_wastewater_operations_ui_contract()
    workbench = water_wastewater_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["water_wastewater_operations_control"]["capability_count"] == 50
    assert "evaluate_water_wastewater_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["water_wastewater_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["water_wastewater_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["water_wastewater_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["water_wastewater_operations_control"]["ok"] is True


def test_water_domains_fail_closed_without_evidence():
    for feature in (1,2,3,9,13,14,22,23,24,26,28,30,31,32,50):
        result = evaluate_water_wastewater_operations_control(feature, {"plant_process_evidence_complete": False})
        assert result["ok"] is False
        assert any("treatment plant" in finding for finding in result["findings"])
    for feature in (4,5,6,7,8,10,15,24,29,35,39,40,43,44,45,47,50):
        result = evaluate_water_wastewater_operations_control(feature, {"compliance_quality_evidence_complete": False})
        assert result["ok"] is False
        assert any("sample chain" in finding for finding in result["findings"])
    for feature in (11,12,16,17,18,19,20,21,25,33,37,41,42,46,49,50):
        result = evaluate_water_wastewater_operations_control(feature, {"field_incident_evidence_complete": False})
        assert result["ok"] is False
        assert any("service interruption" in finding for finding in result["findings"])
    for feature in (34,35,36,37,38,39,40,47,48,49,50):
        result = evaluate_water_wastewater_operations_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("rules, parameters" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (8,10,11,15,17,19,20,22,24,29,35,36,37,40,43,46,49,50):
        result = evaluate_water_wastewater_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (8,10,15,17,19,20,22,24,29,37,40,43,46,49,50):
        result = evaluate_water_wastewater_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (35,36,37,49,50):
        result = evaluate_water_wastewater_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_water_wastewater_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_water_wastewater_operations_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_water_wastewater_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_water_wastewater_operations_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_water_wastewater_operations_control(3, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    plant = sample_payload_for(1)
    assert plant["operating_state_id"].startswith("treatment_plant_operating_state_model")
    assert plant["treatment_plant_operating_state_model_verified"] is True
    assert plant["side_effects"] == ()
    advisory = evaluate_water_wastewater_operations_control("boil_water_advisory_workflow")
    assert advisory["ok"] is True
    assert "public_message" in advisory["evidence"]["required_fields"]
    assert "customer_notification" in advisory["evidence"]["required_fields"]
    boundary = CONTROL_SPECS[48]
    assert boundary["route"].endswith("/cross_pbc_boundary_proof")
    assert "no_foreign_mutation" in boundary["fields"]
