"""Domain behavior checks for telecom network operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import telecom_network_operations_runtime_capabilities
from ..telecom_network_operations_control import (
    CONTROL_SPECS,
    TELECOM_ALLOWED_DATABASE_BACKENDS,
    TELECOM_DECLARED_DEPENDENCIES,
    TELECOM_OWNED_TABLES,
    TELECOM_REQUIRED_EVENT_TOPIC,
    evaluate_telecom_network_operations_control,
    improve1_telecom_network_operations_control_contract,
    sample_payload_for,
)
from ..ui import telecom_network_operations_render_workbench, telecom_network_operations_ui_contract


def test_all_50_telecom_controls_are_executable_and_owned():
    contract = improve1_telecom_network_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TELECOM_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /telecom-network-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TelecomNetworkOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TELECOM_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TELECOM_OWNED_TABLES
            assert table.startswith("telecom_network_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TELECOM_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_telecom_control_contract():
    runtime = telecom_network_operations_runtime_capabilities()
    ui = telecom_network_operations_ui_contract()
    workbench = telecom_network_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["telecom_network_operations_control"]["capability_count"] == 50
    assert "evaluate_telecom_network_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["telecom_network_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["telecom_network_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["telecom_network_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["telecom_network_operations_control"]["ok"] is True


def test_telecom_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 11, 14, 15, 17, 18, 29, 30, 35, 36, 37, 44, 46, 49, 50):
        result = evaluate_telecom_network_operations_control(feature, {"topology_inventory_evidence_complete": False})
        assert result["ok"] is False
        assert any("topology and inventory evidence" in finding for finding in result["findings"])
    for feature in (5, 6, 7, 9, 10, 12, 13, 16, 19, 21, 22, 24, 25, 26, 27, 28, 41, 43, 45, 50):
        result = evaluate_telecom_network_operations_control(feature, {"alarm_outage_sla_evidence_complete": False})
        assert result["ok"] is False
        assert any("alarm, outage" in finding for finding in result["findings"])
    for feature in (8, 20, 23, 31, 32, 33, 34, 39, 40, 47, 48, 50):
        result = evaluate_telecom_network_operations_control(feature, {"planned_field_restoration_evidence_complete": False})
        assert result["ok"] is False
        assert any("planned work" in finding for finding in result["findings"])
    for feature in (26, 27, 28, 30, 36, 38, 39, 40, 42, 45, 46, 47, 49, 50):
        result = evaluate_telecom_network_operations_control(feature, {"governance_release_evidence_complete": False})
        assert result["ok"] is False
        assert any("telecom event taxonomy" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (6, 8, 9, 20, 21, 23, 24, 25, 31, 32, 34, 36, 40, 45, 48, 50):
        result = evaluate_telecom_network_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (8, 9, 20, 23, 24, 31, 32, 34, 40, 47, 48, 50):
        result = evaluate_telecom_network_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (21, 22, 23, 24, 25, 48, 50):
        result = evaluate_telecom_network_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_telecom_network_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_telecom_network_operations_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_telecom_network_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_telecom_network_operations_control(30, {"shared_table_access": True})["ok"] is False
    assert evaluate_telecom_network_operations_control(14, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    site = sample_payload_for(1)
    assert site["site_hierarchy_id"].startswith("canonical_site_hierarchy")
    assert site["canonical_site_hierarchy_and_geospatial_identity_verified"] is True
    assert site["side_effects"] == ()
    outage = evaluate_telecom_network_operations_control("outage_lifecycle_and_major_incident_control")
    assert outage["ok"] is True
    assert "bridge_commander" in outage["evidence"]["required_fields"]
    assert "restoration_eta" in outage["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/manifest_to_backlog_traceability_gate")
    assert "manifest_event_contract" in release_gate["fields"]
