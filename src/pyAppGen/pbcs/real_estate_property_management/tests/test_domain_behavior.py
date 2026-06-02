"""Domain behavior checks for real estate property management improve1 controls."""

from ..real_estate_property_management_control import (
    CONTROL_SPECS,
    REAL_ESTATE_ALLOWED_DATABASE_BACKENDS,
    REAL_ESTATE_DECLARED_DEPENDENCIES,
    REAL_ESTATE_OWNED_TABLES,
    REAL_ESTATE_REQUIRED_EVENT_TOPIC,
    evaluate_real_estate_property_management_control,
    improve1_real_estate_property_management_control_contract,
    sample_payload_for,
)
from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import real_estate_property_management_runtime_capabilities
from ..ui import real_estate_property_management_render_workbench, real_estate_property_management_ui_contract


def test_all_50_real_estate_controls_are_executable_and_owned():
    contract = improve1_real_estate_property_management_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == REAL_ESTATE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /real-estate-property-management/improve1/")
        assert item["evidence"]["ui_surface"].startswith("RealEstatePropertyManagement")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == REAL_ESTATE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in REAL_ESTATE_OWNED_TABLES
            assert table.startswith("real_estate_property_management_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in REAL_ESTATE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_real_estate_control_contract():
    runtime = real_estate_property_management_runtime_capabilities()
    ui = real_estate_property_management_ui_contract()
    workbench = real_estate_property_management_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["real_estate_property_management_control"]["capability_count"] == 50
    assert "evaluate_real_estate_property_management_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["real_estate_property_management_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["real_estate_property_management_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["real_estate_property_management_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["real_estate_property_management_control"]["ok"] is True


def test_financial_controls_fail_closed_without_reconciliation_or_separate_approval():
    financial_features = (6, 7, 8, 9, 11, 21, 23, 24, 34, 35, 38, 48, 50)
    for feature in financial_features:
        result = evaluate_real_estate_property_management_control(feature, {"financial_reconciliation_complete": False})
        assert result["ok"] is False
        assert any("financial reconciliation" in finding for finding in result["findings"])

    approval_features = (3, 9, 11, 13, 19, 21, 23, 24, 25, 34, 35, 36, 38, 39, 44, 48, 49, 50)
    for feature in approval_features:
        result = evaluate_real_estate_property_management_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])


def test_leasing_notice_maintenance_and_mobile_controls_are_gated():
    for feature in (4, 12, 13, 15, 20, 25, 29, 30, 46, 49):
        result = evaluate_real_estate_property_management_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (10, 14, 15, 16, 17, 20, 21, 22, 45, 46, 47):
        result = evaluate_real_estate_property_management_control(feature, {"field_evidence_complete": False})
        assert result["ok"] is False
        assert any("field operations evidence" in finding for finding in result["findings"])

    for feature in (4, 12, 14, 17, 23, 24, 28, 29, 30, 36, 40, 41, 49, 50):
        result = evaluate_real_estate_property_management_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("preview-only" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_real_estate_property_management_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_real_estate_property_management_control(31, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_real_estate_property_management_control(45, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_real_estate_property_management_control(37, {"shared_table_access": True})["ok"] is False
    assert evaluate_real_estate_property_management_control(5, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    portfolio = sample_payload_for(1)
    assert portfolio["portfolio_code"].startswith("portfolio_and_building_hierarchy")
    assert portfolio["portfolio_and_building_hierarchy_verified"] is True
    assert portfolio["side_effects"] == ()

    rent_roll = evaluate_real_estate_property_management_control("rent_roll_snapshots_with_drill_through")
    assert rent_roll["ok"] is True
    assert "contracted_rent" in rent_roll["evidence"]["required_fields"]
    assert "arrears_balance" in rent_roll["evidence"]["required_fields"]

    schema_evolution = CONTROL_SPECS[44]
    assert schema_evolution["route"].endswith("/schema_evolution_for_units_notices_and_renewals")
    assert "migration_sequence" in schema_evolution["fields"]
