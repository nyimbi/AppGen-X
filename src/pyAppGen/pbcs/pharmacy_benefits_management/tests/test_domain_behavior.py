"""Domain behavior tests for pharmacy benefits improve1 controls."""

from ..benefits_control import (
    BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS,
    BENEFITS_CONTROL_OWNED_TABLES,
    CONTROL_SPECS,
    evaluate_benefits_control,
    improve1_benefits_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import pharmacy_benefits_management_runtime_capabilities
from ..ui import pharmacy_benefits_management_render_workbench, pharmacy_benefits_management_ui_contract


def test_all_fifty_benefits_controls_are_executable_and_owned():
    contract = improve1_benefits_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == BENEFITS_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_benefits_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in BENEFITS_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PharmacyBenefitsManagement")
        assert result["evidence"]["service_api"].startswith("POST /pharmacy-benefits-management/improve1/")


def test_runtime_ui_and_release_expose_benefits_control_contract():
    runtime = pharmacy_benefits_management_runtime_capabilities()
    ui = pharmacy_benefits_management_ui_contract()
    workbench = pharmacy_benefits_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["benefits_control"]["capability_count"] == 50
    assert "evaluate_benefits_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["benefits_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["benefits_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["benefits_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_benefits_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_formulary_pa_claim_rebate_and_clinical_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 14, 15, 17, 18, 21, 22, 25):
        _blocked(feature_number)


def test_agent_affordability_audit_model_release_and_composition_controls_are_gated():
    for feature_number in (19, 24, 27, 28, 29, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_benefits_control(18, {"benefit_risk_evidence_complete": False})["ok"] is False
    assert evaluate_benefits_control(37, {"agent_preview_only": False})["ok"] is False
    assert evaluate_benefits_control(38, {"human_confirmation": False})["ok"] is False
    assert evaluate_benefits_control(44, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_benefits_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_benefits_control(36, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_benefits_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_benefits_control(49, {"shared_table_access": True})
    direct_dependency = evaluate_benefits_control(33, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(6)
    result = evaluate_benefits_control(6, payload)
    assert result["ok"] is True
    assert payload["criteria_rule_id"].startswith("prior_authorization_clinical_criteria_engine")
    assert payload["prior_authorization_clinical_criteria_engine_verified"] is True
    assert result["side_effects"] == ()
