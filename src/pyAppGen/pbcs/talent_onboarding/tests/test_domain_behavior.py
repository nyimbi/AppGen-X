"""Domain behavior checks for talent onboarding improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import talent_onboarding_runtime_capabilities
from ..talent_onboarding_control import (
    CONTROL_SPECS,
    TALENT_ALLOWED_DATABASE_BACKENDS,
    TALENT_DECLARED_DEPENDENCIES,
    TALENT_OWNED_TABLES,
    TALENT_REQUIRED_EVENT_TOPIC,
    evaluate_talent_onboarding_control,
    improve1_talent_onboarding_control_contract,
    sample_payload_for,
)
from ..ui import talent_onboarding_render_workbench, talent_onboarding_ui_contract


def test_all_50_talent_controls_are_executable_and_owned():
    contract = improve1_talent_onboarding_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TALENT_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /talent-onboarding/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TalentOnboarding")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TALENT_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TALENT_OWNED_TABLES
            assert table.startswith("talent_onboarding_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TALENT_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_talent_control_contract():
    runtime = talent_onboarding_runtime_capabilities()
    ui = talent_onboarding_ui_contract()
    workbench = talent_onboarding_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["talent_onboarding_control"]["capability_count"] == 50
    assert "evaluate_talent_onboarding_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["talent_onboarding_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["talent_onboarding_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["talent_onboarding_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["talent_onboarding_control"]["ok"] is True


def test_talent_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 43, 44, 49, 50):
        result = evaluate_talent_onboarding_control(feature, {"requisition_candidate_evidence_complete": False})
        assert result["ok"] is False
        assert any("requisition and candidate evidence" in finding for finding in result["findings"])

    for feature in (14, 15, 16, 17, 18, 19, 37, 38, 39, 40, 41, 47, 49, 50):
        result = evaluate_talent_onboarding_control(feature, {"interview_evaluation_evidence_complete": False})
        assert result["ok"] is False
        assert any("interview and evaluation evidence" in finding for finding in result["findings"])

    for feature in (20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 48, 50):
        result = evaluate_talent_onboarding_control(feature, {"check_offer_onboarding_evidence_complete": False})
        assert result["ok"] is False
        assert any("background check, offer, onboarding" in finding for finding in result["findings"])

    for feature in (34, 35, 36, 39, 40, 42, 43, 44, 45, 46, 48, 49, 50):
        result = evaluate_talent_onboarding_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("candidate proofs, audit traces" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (10, 13, 17, 19, 21, 22, 23, 25, 26, 31, 32, 36, 39, 45, 46, 50):
        result = evaluate_talent_onboarding_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (2, 3, 21, 22, 23, 25, 26, 31, 32, 36, 39, 46, 50):
        result = evaluate_talent_onboarding_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (13, 19, 36, 39, 40, 45, 46, 49, 50):
        result = evaluate_talent_onboarding_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_talent_onboarding_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_talent_onboarding_control(43, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_talent_onboarding_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_talent_onboarding_control(43, {"shared_table_access": True})["ok"] is False
    assert evaluate_talent_onboarding_control(32, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    readiness = sample_payload_for(1)
    assert readiness["readiness_gate_id"].startswith("requisition_readiness_gate")
    assert readiness["requisition_readiness_gate_verified"] is True
    assert readiness["side_effects"] == ()

    offer = evaluate_talent_onboarding_control("offer_readiness_gate")
    assert offer["ok"] is True
    assert "check_adjudication" in offer["evidence"]["required_fields"]
    assert "compensation_projection" in offer["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_hire_to_provision_proof")
    assert "emitted_events" in release_gate["fields"]
