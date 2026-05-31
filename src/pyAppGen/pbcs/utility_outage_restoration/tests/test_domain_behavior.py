"""Domain behavior checks for utility outage restoration improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import utility_outage_restoration_runtime_capabilities
from ..ui import utility_outage_restoration_render_workbench, utility_outage_restoration_ui_contract
from ..utility_outage_restoration_control import (
    CONTROL_SPECS,
    OUTAGE_ALLOWED_DATABASE_BACKENDS,
    OUTAGE_CONTROL_OWNED_TABLES,
    OUTAGE_DECLARED_DEPENDENCIES,
    OUTAGE_REQUIRED_EVENT_TOPIC,
    evaluate_utility_outage_restoration_control,
    improve1_utility_outage_restoration_control_contract,
    sample_payload_for,
)


def test_all_50_outage_controls_are_executable_and_owned():
    contract = improve1_utility_outage_restoration_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == OUTAGE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /utility-outage-restoration/improve1/")
        assert item["evidence"]["ui_surface"].startswith("UtilityOutageRestoration")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == OUTAGE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in OUTAGE_CONTROL_OWNED_TABLES
            assert table.startswith("utility_outage_restoration_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in OUTAGE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_outage_control_contract():
    runtime = utility_outage_restoration_runtime_capabilities()
    ui = utility_outage_restoration_ui_contract()
    workbench = utility_outage_restoration_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["utility_outage_restoration_control"]["capability_count"] == 50
    assert "evaluate_utility_outage_restoration_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["utility_outage_restoration_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["utility_outage_restoration_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["utility_outage_restoration_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["utility_outage_restoration_control"]["ok"] is True


def test_outage_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 7, 8, 20, 21, 28, 29, 30, 38, 43, 47, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"incident_detection_evidence_complete": False})
        assert result["ok"] is False
        assert any("outage detection" in finding for finding in result["findings"])
    for feature in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 32, 35, 36, 41, 42, 43, 44, 49, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"restoration_operations_evidence_complete": False})
        assert result["ok"] is False
        assert any("switching safety" in finding for finding in result["findings"])
    for feature in (5, 6, 8, 9, 22, 23, 24, 25, 26, 27, 40, 45, 46, 49, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"customer_regulatory_evidence_complete": False})
        assert result["ok"] is False
        assert any("critical customer" in finding for finding in result["findings"])
    for feature in (31, 33, 34, 35, 36, 37, 38, 39, 47, 48, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("operator workbench" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (9, 10, 11, 12, 14, 15, 16, 23, 24, 25, 26, 29, 30, 35, 36, 39, 44, 49, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (9, 10, 11, 15, 16, 23, 24, 25, 26, 35, 36, 39, 44, 49, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (34, 35, 36, 47, 50):
        result = evaluate_utility_outage_restoration_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_utility_outage_restoration_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_utility_outage_restoration_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_utility_outage_restoration_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_utility_outage_restoration_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_utility_outage_restoration_control(4, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    lifecycle = sample_payload_for(1)
    assert lifecycle["incident_number"].startswith("outage_incident_lifecycle_state_machine")
    assert lifecycle["outage_incident_lifecycle_state_machine_verified"] is True
    assert lifecycle["side_effects"] == ()
    switching = evaluate_utility_outage_restoration_control("switching_plan_workflow")
    assert switching["ok"] is True
    assert "hold_point" in switching["evidence"]["required_fields"]
    assert "clearance_reference" in switching["evidence"]["required_fields"]
    boundary = CONTROL_SPECS[48]
    assert boundary["route"].endswith("/cross_pbc_boundary_proof")
    assert "no_foreign_mutation" in boundary["fields"]
