"""Domain behavior tests for policy administration improve1 controls."""

from ..policy_control import (
    CONTROL_SPECS,
    POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    POLICY_CONTROL_OWNED_TABLES,
    evaluate_policy_control,
    improve1_policy_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import policy_administration_insurance_runtime_capabilities
from ..ui import policy_administration_insurance_render_workbench, policy_administration_insurance_ui_contract


def test_all_fifty_policy_controls_are_executable_and_owned():
    contract = improve1_policy_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == POLICY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_policy_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in POLICY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PolicyAdministrationInsurance")
        assert result["evidence"]["service_api"].startswith("POST /policy-administration-insurance/improve1/")


def test_runtime_ui_and_release_expose_policy_control_contract():
    runtime = policy_administration_insurance_runtime_capabilities()
    ui = policy_administration_insurance_ui_contract()
    workbench = policy_administration_insurance_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["policy_control"]["capability_count"] == 50
    assert "evaluate_policy_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["policy_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["policy_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["policy_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_policy_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_issuance_term_coverage_endorsement_and_cancellation_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 20, 21, 22, 24, 25):
        _blocked(feature_number)


def test_projection_agent_event_boundary_and_renewal_controls_are_gated():
    for feature_number in (27, 28, 29, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_policy_control(9, {"policy_risk_evidence_complete": False})["ok"] is False
    assert evaluate_policy_control(38, {"agent_preview_only": False})["ok"] is False
    assert evaluate_policy_control(6, {"human_confirmation": False})["ok"] is False
    assert evaluate_policy_control(40, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_policy_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_policy_control(41, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_policy_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_policy_control(48, {"shared_table_access": True})
    direct_dependency = evaluate_policy_control(28, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(6)
    result = evaluate_policy_control(6, payload)
    assert result["ok"] is True
    assert payload["endorsement_id"].startswith("endorsement_transaction_model")
    assert payload["endorsement_transaction_model_verified"] is True
    assert result["side_effects"] == ()
