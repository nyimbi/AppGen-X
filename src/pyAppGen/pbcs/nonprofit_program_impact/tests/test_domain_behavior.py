"""Domain behavior tests for nonprofit impact improve1 controls."""

from ..impact_control import (
    CONTROL_SPECS,
    IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS,
    IMPACT_CONTROL_OWNED_TABLES,
    evaluate_impact_control,
    improve1_impact_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import nonprofit_program_impact_runtime_capabilities
from ..ui import nonprofit_program_impact_render_workbench, nonprofit_program_impact_ui_contract


def test_all_fifty_impact_controls_are_executable_and_owned():
    contract = improve1_impact_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == IMPACT_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_impact_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in IMPACT_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("NonprofitProgramImpact")
        assert result["evidence"]["service_api"].startswith("POST /nonprofit-program-impact/improve1/")


def test_runtime_ui_and_release_expose_impact_control_contract():
    runtime = nonprofit_program_impact_runtime_capabilities()
    ui = nonprofit_program_impact_ui_contract()
    workbench = nonprofit_program_impact_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["impact_control"]["capability_count"] == 50
    assert "evaluate_impact_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["impact_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["impact_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["impact_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_impact_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_program_beneficiary_service_outcome_and_donor_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25):
        _blocked(feature_number)


def test_safeguarding_partner_agent_privacy_and_release_controls_are_gated():
    for feature_number in (13, 14, 15, 19, 20, 26, 27, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45, 50):
        _blocked(feature_number)
    assert evaluate_impact_control(14, {"sensitive_impact_evidence_complete": False})["ok"] is False
    assert evaluate_impact_control(33, {"agent_preview_only": False})["ok"] is False
    assert evaluate_impact_control(15, {"human_confirmation": False})["ok"] is False
    assert evaluate_impact_control(45, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_impact_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_impact_control(36, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_impact_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_impact_control(43, {"shared_table_access": True})
    direct_dependency = evaluate_impact_control(38, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_impact_control(1, payload)
    assert result["ok"] is True
    assert payload["theory_of_change_id"].startswith("theory_of_change_model_per_program")
    assert payload["theory_of_change_model_per_program_verified"] is True
    assert result["side_effects"] == ()
