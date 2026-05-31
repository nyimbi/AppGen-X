"""Domain behavior checks for utilities metering billing improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import utilities_metering_billing_runtime_capabilities
from ..ui import utilities_metering_billing_render_workbench, utilities_metering_billing_ui_contract
from ..utilities_metering_billing_control import (
    CONTROL_SPECS,
    UTILITY_ALLOWED_DATABASE_BACKENDS,
    UTILITY_CONTROL_OWNED_TABLES,
    UTILITY_DECLARED_DEPENDENCIES,
    UTILITY_REQUIRED_EVENT_TOPIC,
    evaluate_utilities_metering_billing_control,
    improve1_utilities_metering_billing_control_contract,
    sample_payload_for,
)


def test_all_50_utility_controls_are_executable_and_owned():
    contract = improve1_utilities_metering_billing_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == UTILITY_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /utilities-metering-billing/improve1/")
        assert item["evidence"]["ui_surface"].startswith("UtilitiesMeteringBilling")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == UTILITY_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in UTILITY_CONTROL_OWNED_TABLES
            assert table.startswith("utilities_metering_billing_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in UTILITY_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_utility_control_contract():
    runtime = utilities_metering_billing_runtime_capabilities()
    ui = utilities_metering_billing_ui_contract()
    workbench = utilities_metering_billing_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["utilities_metering_billing_control"]["capability_count"] == 50
    assert "evaluate_utilities_metering_billing_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["utilities_metering_billing_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["utilities_metering_billing_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["utilities_metering_billing_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["utilities_metering_billing_control"]["ok"] is True


def test_utility_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 14, 27, 28, 29, 47, 49, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"service_meter_evidence_complete": False})
        assert result["ok"] is False
        assert any("service point" in finding for finding in result["findings"])
    for feature in (8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 31, 32, 48, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"read_billing_evidence_complete": False})
        assert result["ok"] is False
        assert any("read validation" in finding for finding in result["findings"])
    for feature in (23, 24, 25, 26, 30, 33, 34, 35, 36, 37, 38, 39, 46, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"adjustment_payment_evidence_complete": False})
        assert result["ok"] is False
        assert any("adjustment, rebilling" in finding for finding in result["findings"])
    for feature in (40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("agent skills" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (2, 4, 11, 14, 23, 24, 27, 28, 30, 34, 36, 39, 40, 41, 42, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (2, 11, 23, 24, 27, 28, 30, 34, 36, 39, 41, 42, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (40, 41, 42, 46, 50):
        result = evaluate_utilities_metering_billing_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_utilities_metering_billing_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_utilities_metering_billing_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_utilities_metering_billing_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_utilities_metering_billing_control(45, {"shared_table_access": True})["ok"] is False
    assert evaluate_utilities_metering_billing_control(25, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    service_point = sample_payload_for(1)
    assert service_point["service_point_identity_id"].startswith("service_point_master_identity")
    assert service_point["service_point_master_identity_verified"] is True
    assert service_point["side_effects"] == ()
    trace = evaluate_utilities_metering_billing_control("read_to_bill_validation_explainability")
    assert trace["ok"] is True
    assert "source_read_set" in trace["evidence"]["required_fields"]
    assert "bill_segment" in trace["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/go_live_cutover_and_hypercare_evidence")
    assert "hypercare_exit" in release_gate["fields"]
