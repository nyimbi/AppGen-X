"""Domain behavior tests for payroll improve1 controls."""

from ..payroll_control import (
    CONTROL_SPECS,
    PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PAYROLL_CONTROL_OWNED_TABLES,
    evaluate_payroll_control,
    improve1_payroll_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import payroll_engine_runtime_capabilities
from ..ui import payroll_engine_render_workbench, payroll_engine_ui_contract


def test_all_fifty_payroll_controls_are_executable_and_owned():
    contract = improve1_payroll_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PAYROLL_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_payroll_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PAYROLL_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PayrollEngine")
        assert result["evidence"]["service_api"].startswith("POST /payroll-engine/improve1/")


def test_runtime_ui_and_release_expose_payroll_control_contract():
    runtime = payroll_engine_runtime_capabilities()
    ui = payroll_engine_ui_contract()
    workbench = payroll_engine_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["payroll_control"]["capability_count"] == 50
    assert "evaluate_payroll_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["payroll_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["payroll_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["payroll_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_payroll_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_calendar_gross_to_net_tax_deduction_and_payment_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 17, 18, 21, 23, 26):
        _blocked(feature_number)


def test_filing_correction_agent_boundary_and_run_proof_controls_are_gated():
    for feature_number in (28, 30, 31, 32, 34, 35, 38, 39, 40, 41, 43, 44, 46, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_payroll_control(18, {"payroll_risk_evidence_complete": False})["ok"] is False
    assert evaluate_payroll_control(43, {"agent_preview_only": False})["ok"] is False
    assert evaluate_payroll_control(23, {"human_confirmation": False})["ok"] is False
    assert evaluate_payroll_control(45, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_payroll_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_payroll_control(40, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_payroll_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_payroll_control(41, {"shared_table_access": True})
    direct_dependency = evaluate_payroll_control(15, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(12)
    result = evaluate_payroll_control(12, payload)
    assert result["ok"] is True
    assert payload["gross_trace_id"].startswith("gross_pay_calculation_trace")
    assert payload["gross_pay_calculation_trace_verified"] is True
    assert result["side_effects"] == ()
