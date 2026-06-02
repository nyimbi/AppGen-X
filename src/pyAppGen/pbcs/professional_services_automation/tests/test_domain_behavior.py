"""Domain behavior tests for PSA improve1 controls."""

from ..psa_control import (
    CONTROL_SPECS,
    PSA_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PSA_CONTROL_OWNED_TABLES,
    evaluate_psa_control,
    improve1_psa_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC,
    professional_services_automation_configure_runtime,
    professional_services_automation_empty_state,
    professional_services_automation_runtime_capabilities,
)
from ..ui import professional_services_automation_render_workbench, professional_services_automation_ui_contract


def _configured_state():
    return professional_services_automation_configure_runtime(
        professional_services_automation_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PROFESSIONAL_SERVICES_AUTOMATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_currency": "USD",
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_psa_controls_are_executable_and_owned():
    contract = improve1_psa_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PSA_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_psa_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PSA_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("ProfessionalServicesAutomation")
        assert result["evidence"]["service_api"].startswith("POST /professional-services-automation/improve1/")


def test_runtime_ui_and_release_expose_psa_control_contract():
    runtime = professional_services_automation_runtime_capabilities()
    ui = professional_services_automation_ui_contract()
    workbench = professional_services_automation_render_workbench(_configured_state())
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["psa_control"]["capability_count"] == 50
    assert "evaluate_psa_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["psa_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["psa_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["psa_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_psa_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_engagement_sow_staffing_time_billing_and_margin_controls_are_gated():
    for feature_number in (1, 3, 4, 5, 7, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25):
        _blocked(feature_number)


def test_risk_boundary_agent_cockpit_and_release_controls_are_gated():
    for feature_number in (27, 28, 29, 30, 31, 32, 33, 34, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_psa_control(10, {"psa_risk_evidence_complete": False})["ok"] is False
    assert evaluate_psa_control(47, {"agent_preview_only": False})["ok"] is False
    assert evaluate_psa_control(21, {"human_confirmation": False})["ok"] is False
    assert evaluate_psa_control(41, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_psa_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_psa_control(45, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_psa_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_psa_control(44, {"shared_table_access": True})
    direct_dependency = evaluate_psa_control(17, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(3)
    result = evaluate_psa_control(3, payload)
    assert result["ok"] is True
    assert payload["sow_extraction_id"].startswith("statement_of_work_semantic_extraction")
    assert payload["statement_of_work_semantic_extraction_verified"] is True
    assert result["side_effects"] == ()
