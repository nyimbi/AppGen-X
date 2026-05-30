"""Domain behavior tests for public sector case management improve1 controls."""

from ..public_sector_case_control import (
    CASE_ALLOWED_DATABASE_BACKENDS,
    CASE_OWNED_TABLES,
    CONTROL_SPECS,
    evaluate_public_sector_case_control,
    improve1_public_sector_case_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    public_sector_case_management_configure_runtime,
    public_sector_case_management_empty_state,
    public_sector_case_management_runtime_capabilities,
)
from ..ui import public_sector_case_management_render_workbench, public_sector_case_management_ui_contract


def _configured_state():
    return public_sector_case_management_configure_runtime(
        public_sector_case_management_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PUBLIC_SECTOR_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_public_sector_case_controls_are_executable_and_owned():
    contract = improve1_public_sector_case_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == CASE_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_public_sector_case_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in CASE_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PublicSectorCaseManagement")
        assert result["evidence"]["service_api"].startswith("POST /public-sector-case-management/improve1/")


def test_runtime_ui_and_release_expose_public_sector_case_control_contract():
    state = _configured_state()
    assert state["configuration"]["database_backend"] == "postgresql"
    runtime = public_sector_case_management_runtime_capabilities()
    ui = public_sector_case_management_ui_contract()
    workbench = public_sector_case_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["public_sector_case_control"]["capability_count"] == 50
    assert "evaluate_public_sector_case_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["public_sector_case_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["public_sector_case_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["public_sector_case_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_public_sector_case_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_intake_eligibility_evidence_appeal_and_correspondence_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 15, 18, 19, 20, 21, 22, 23):
        _blocked(feature_number)


def test_privacy_agent_event_retention_continuity_and_release_controls_are_gated():
    for feature_number in (24, 25, 26, 27, 28, 29, 30, 34, 35, 36, 37, 38, 39, 40, 43, 44, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_public_sector_case_control(35, {"agent_preview_only": False})["ok"] is False
    assert evaluate_public_sector_case_control(29, {"supervisor_approval": False})["ok"] is False
    assert evaluate_public_sector_case_control(1, {"human_confirmation": False})["ok"] is False
    assert evaluate_public_sector_case_control(41, {"non_mutating_simulation": False})["ok"] is False
    assert evaluate_public_sector_case_control(21, {"privacy_evidence_complete": False})["ok"] is False
    assert evaluate_public_sector_case_control(28, {"program_rule_trace_complete": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_public_sector_case_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_public_sector_case_control(38, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_public_sector_case_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_public_sector_case_control(39, {"shared_table_access": True})
    direct_dependency = evaluate_public_sector_case_control(3, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_public_sector_case_control(1, payload)
    assert result["ok"] is True
    assert payload["intake_envelope_id"].startswith("multi_channel_intake_envelope")
    assert payload["multi_channel_intake_envelope_verified"] is True
    assert result["side_effects"] == ()
