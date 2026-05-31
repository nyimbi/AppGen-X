"""Domain behavior checks for time labor improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import time_labor_runtime_capabilities
from ..time_labor_control import (
    CONTROL_SPECS,
    TIME_ALLOWED_DATABASE_BACKENDS,
    TIME_CONTROL_OWNED_TABLES,
    TIME_DECLARED_DEPENDENCIES,
    TIME_REQUIRED_EVENT_TOPIC,
    evaluate_time_labor_control,
    improve1_time_labor_control_contract,
    sample_payload_for,
)
from ..ui import time_labor_render_workbench, time_labor_ui_contract


def test_all_50_time_controls_are_executable_and_owned():
    contract = improve1_time_labor_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TIME_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /time-labor/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TimeLabor")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TIME_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TIME_CONTROL_OWNED_TABLES
            assert table.startswith("time_labor_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TIME_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_time_control_contract():
    runtime = time_labor_runtime_capabilities()
    ui = time_labor_ui_contract()
    workbench = time_labor_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["time_labor_control"]["capability_count"] == 50
    assert "evaluate_time_labor_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["time_labor_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["time_labor_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["time_labor_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["time_labor_control"]["ok"] is True


def test_time_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 8, 22, 33, 35, 43, 44, 49, 50):
        result = evaluate_time_labor_control(feature, {"scheduling_evidence_complete": False})
        assert result["ok"] is False
        assert any("scheduling evidence" in finding for finding in result["findings"])
    for feature in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 31, 34, 45, 47, 50):
        result = evaluate_time_labor_control(feature, {"clock_calculation_evidence_complete": False})
        assert result["ok"] is False
        assert any("clock and calculation evidence" in finding for finding in result["findings"])
    for feature in (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 48, 50):
        result = evaluate_time_labor_control(feature, {"absence_payroll_evidence_complete": False})
        assert result["ok"] is False
        assert any("absence, approval, payroll-proof" in finding for finding in result["findings"])
    for feature in (32, 36, 37, 38, 39, 40, 41, 42, 46, 47, 49, 50):
        result = evaluate_time_labor_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("policy screening, model governance" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (5, 7, 8, 21, 24, 30, 31, 42, 43, 48, 50):
        result = evaluate_time_labor_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (5, 7, 21, 24, 30, 31, 42, 48, 50):
        result = evaluate_time_labor_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (34, 40, 41, 42, 43, 49, 50):
        result = evaluate_time_labor_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_time_labor_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_time_labor_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_time_labor_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_time_labor_control(38, {"shared_table_access": True})["ok"] is False
    assert evaluate_time_labor_control(28, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    readiness = sample_payload_for(1)
    assert readiness["shift_readiness_id"].startswith("shift_readiness_gate")
    assert readiness["shift_readiness_gate_verified"] is True
    assert readiness["side_effects"] == ()
    calculation = evaluate_time_labor_control("time_entry_calculation_trace")
    assert calculation["ok"] is True
    assert "rounding_rule" in calculation["evidence"]["required_fields"]
    assert "overtime_bucket" in calculation["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_payroll_ready_hours_proof")
    assert "labor_hours_event" in release_gate["fields"]
