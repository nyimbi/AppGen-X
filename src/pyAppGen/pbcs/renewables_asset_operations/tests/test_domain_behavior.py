"""Domain behavior checks for renewables asset operations improve1 controls."""

from ..renewables_asset_operations_control import (
    CONTROL_SPECS,
    RENEWABLES_ALLOWED_DATABASE_BACKENDS,
    RENEWABLES_DECLARED_DEPENDENCIES,
    RENEWABLES_OWNED_TABLES,
    RENEWABLES_REQUIRED_EVENT_TOPIC,
    evaluate_renewables_asset_operations_control,
    improve1_renewables_asset_operations_control_contract,
    sample_payload_for,
)
from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import renewables_asset_operations_runtime_capabilities
from ..ui import renewables_asset_operations_render_workbench, renewables_asset_operations_ui_contract


def test_all_50_renewables_controls_are_executable_and_owned():
    contract = improve1_renewables_asset_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == RENEWABLES_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /renewables-asset-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("RenewablesAssetOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == RENEWABLES_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in RENEWABLES_OWNED_TABLES
            assert table.startswith("renewables_asset_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in RENEWABLES_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_renewables_control_contract():
    runtime = renewables_asset_operations_runtime_capabilities()
    ui = renewables_asset_operations_ui_contract()
    workbench = renewables_asset_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["renewables_asset_operations_control"]["capability_count"] == 50
    assert "evaluate_renewables_asset_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["renewables_asset_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["renewables_asset_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["renewables_asset_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["renewables_asset_operations_control"]["ok"] is True


def test_safety_performance_and_commercial_controls_fail_closed_without_evidence():
    for feature in (13, 18, 19, 20, 21, 22, 23, 24, 31, 34, 38, 39, 44, 48, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"safety_evidence_complete": False})
        assert result["ok"] is False
        assert any("safety evidence" in finding for finding in result["findings"])

    for feature in (2, 4, 5, 6, 7, 8, 14, 15, 16, 28, 29, 30, 31, 32, 36, 49, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"performance_evidence_complete": False})
        assert result["ok"] is False
        assert any("performance evidence" in finding for finding in result["findings"])

    for feature in (7, 8, 9, 10, 11, 15, 19, 32, 35, 36, 41, 43, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"commercial_evidence_complete": False})
        assert result["ok"] is False
        assert any("commercial evidence" in finding for finding in result["findings"])


def test_operations_agent_approval_and_field_controls_are_gated():
    for feature in (7, 8, 9, 10, 11, 12, 19, 20, 21, 22, 23, 32, 34, 35, 36, 40, 41, 44, 46, 47, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (2, 7, 8, 9, 10, 11, 19, 21, 22, 23, 32, 34, 35, 36, 44, 45, 46, 47, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (17, 27, 31, 32, 35, 36, 40, 41, 43, 47, 50):
        result = evaluate_renewables_asset_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("preview-only" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_renewables_asset_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_renewables_asset_operations_control(25, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_renewables_asset_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_renewables_asset_operations_control(42, {"shared_table_access": True})["ok"] is False
    assert evaluate_renewables_asset_operations_control(3, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    hierarchy = sample_payload_for(1)
    assert hierarchy["hierarchy_node_id"].startswith("asset_hierarchy_and_technology_specific_master_data")
    assert hierarchy["asset_hierarchy_and_technology_specific_master_data_verified"] is True
    assert hierarchy["side_effects"] == ()

    curtailment = evaluate_renewables_asset_operations_control("curtailment_taxonomy")
    assert curtailment["ok"] is True
    assert "mw_requested" in curtailment["evidence"]["required_fields"]
    assert "compensation_status" in curtailment["evidence"]["required_fields"]

    readiness = CONTROL_SPECS[50]
    assert readiness["route"].endswith("/production_readiness_dashboard_and_go_live_exit_criteria")
    assert "go_live_gate" in readiness["fields"]
