"""Domain behavior tests for mortgage servicing improve1 controls."""

from ..mortgage_servicing_control import (
    CONTROL_SPECS,
    MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MORTGAGE_SERVICING_CONTROL_OWNED_TABLES,
    evaluate_mortgage_servicing_control,
    improve1_mortgage_servicing_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import mortgage_servicing_runtime_capabilities
from ..ui import mortgage_servicing_render_workbench, mortgage_servicing_ui_contract


def test_all_fifty_mortgage_servicing_controls_are_executable_and_owned():
    contract = improve1_mortgage_servicing_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MORTGAGE_SERVICING_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_mortgage_servicing_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MORTGAGE_SERVICING_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MortgageServicing")
        assert result["evidence"]["service_api"].startswith("POST /mortgage-servicing/improve1/")


def test_runtime_ui_and_release_expose_mortgage_servicing_control_contract():
    runtime = mortgage_servicing_runtime_capabilities()
    ui = mortgage_servicing_ui_contract()
    workbench = mortgage_servicing_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["mortgage_servicing_control"]["capability_count"] == 50
    assert "evaluate_mortgage_servicing_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["mortgage_servicing_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["mortgage_servicing_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["mortgage_servicing_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_mortgage_servicing_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_boarding_payment_escrow_statement_and_notice_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 8, 9, 10, 12, 14, 15):
        _blocked(feature_number)


def test_delinquency_loss_mitigation_foreclosure_and_investor_controls_are_gated():
    for feature_number in (17, 18, 19, 20, 21, 22, 23, 25, 26, 28, 31, 33):
        _blocked(feature_number)


def test_agent_event_reconstruction_audit_risk_boundary_and_workspace_controls_are_gated():
    for feature_number in (38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_mortgage_servicing_control(41, {"human_confirmation": False})["ok"] is False
    assert evaluate_mortgage_servicing_control(42, {"agent_preview_only": False})["ok"] is False
    assert evaluate_mortgage_servicing_control(48, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_mortgage_servicing_control(26, {"borrower_impact_evidence_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_mortgage_servicing_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_mortgage_servicing_control(44, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_mortgage_servicing_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_mortgage_servicing_control(49, {"shared_table_access": True})
    direct_dependency = evaluate_mortgage_servicing_control(13, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(4)
    result = evaluate_mortgage_servicing_control(4, payload)
    assert result["ok"] is True
    assert payload["principal_allocation"].startswith("payment_application_waterfall")
    assert payload["payment_application_waterfall_verified"] is True
    assert result["side_effects"] == ()
