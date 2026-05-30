"""Domain behavior checks for research grants management improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..research_grants_management_control import (
    CONTROL_SPECS,
    RESEARCH_ALLOWED_DATABASE_BACKENDS,
    RESEARCH_DECLARED_DEPENDENCIES,
    RESEARCH_OWNED_TABLES,
    RESEARCH_REQUIRED_EVENT_TOPIC,
    evaluate_research_grants_management_control,
    improve1_research_grants_management_control_contract,
    sample_payload_for,
)
from ..runtime import research_grants_management_runtime_capabilities
from ..ui import research_grants_management_render_workbench, research_grants_management_ui_contract


def test_all_50_research_grants_controls_are_executable_and_owned():
    contract = improve1_research_grants_management_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == RESEARCH_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /research-grants-management/improve1/")
        assert item["evidence"]["ui_surface"].startswith("ResearchGrantsManagement")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == RESEARCH_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in RESEARCH_OWNED_TABLES
            assert table.startswith("research_grants_management_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in RESEARCH_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_research_control_contract():
    runtime = research_grants_management_runtime_capabilities()
    ui = research_grants_management_ui_contract()
    workbench = research_grants_management_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["research_grants_management_control"]["capability_count"] == 50
    assert "evaluate_research_grants_management_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["research_grants_management_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["research_grants_management_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["research_grants_management_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["research_grants_management_control"]["ok"] is True


def test_pre_award_compliance_and_financial_controls_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 38, 39, 40):
        result = evaluate_research_grants_management_control(feature, {"pre_award_evidence_complete": False})
        assert result["ok"] is False
        assert any("pre-award evidence" in finding for finding in result["findings"])

    for feature in (6, 11, 12, 13, 14, 15, 17, 23, 24, 28, 31, 32, 33, 34, 43, 48, 50):
        result = evaluate_research_grants_management_control(feature, {"compliance_evidence_complete": False})
        assert result["ok"] is False
        assert any("compliance evidence" in finding for finding in result["findings"])

    for feature in (7, 8, 9, 10, 19, 20, 21, 27, 29, 30, 31, 32, 40, 46, 47, 50):
        result = evaluate_research_grants_management_control(feature, {"financial_evidence_complete": False})
        assert result["ok"] is False
        assert any("financial evidence" in finding for finding in result["findings"])


def test_proposal_award_assistant_and_approval_controls_are_gated():
    for feature in (2, 3, 5, 6, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 23, 30, 32, 38, 39, 40, 41, 45, 47, 48, 50):
        result = evaluate_research_grants_management_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (2, 3, 6, 8, 9, 10, 14, 16, 17, 18, 19, 20, 21, 23, 30, 31, 32, 38, 39, 40, 45, 47, 48, 50):
        result = evaluate_research_grants_management_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (5, 6, 8, 16, 20, 26, 27, 35, 38, 39, 40, 41, 44, 49, 50):
        result = evaluate_research_grants_management_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("preview-only" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_research_grants_management_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_research_grants_management_control(42, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_research_grants_management_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_research_grants_management_control(43, {"shared_table_access": True})["ok"] is False
    assert evaluate_research_grants_management_control(12, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    opportunity = sample_payload_for(1)
    assert opportunity["program_identifier"].startswith("funding_opportunity_source_registry")
    assert opportunity["funding_opportunity_source_registry_verified"] is True
    assert opportunity["side_effects"] == ()

    budget = evaluate_research_grants_management_control("budget_line_item_allowability_and_justification_rules")
    assert budget["ok"] is True
    assert "cost_category" in budget["evidence"]["required_fields"]
    assert "prior_approval_required" in budget["evidence"]["required_fields"]

    closeout = CONTROL_SPECS[47]
    assert closeout["route"].endswith("/final_technical_financial_and_invention_closeout_pack")
    assert "sponsor_acceptance_state" in closeout["fields"]
