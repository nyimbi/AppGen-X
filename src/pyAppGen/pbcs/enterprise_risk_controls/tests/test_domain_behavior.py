"""Domain behavior checks for enterprise_risk_controls improve1 controls."""

from pyAppGen.pbcs.enterprise_risk_controls.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.enterprise_risk_controls.risk_control import (
    RISK_ALLOWED_DATABASE_BACKENDS,
    RISK_DECLARED_DEPENDENCIES,
    RISK_OWNED_TABLES,
    RISK_REQUIRED_EVENT_TOPIC,
    evaluate_risk_control,
    improve1_risk_control_contract,
)
from pyAppGen.pbcs.enterprise_risk_controls.runtime import (
    enterprise_risk_controls_build_release_evidence,
    enterprise_risk_controls_runtime_capabilities,
    enterprise_risk_controls_runtime_smoke,
)
from pyAppGen.pbcs.enterprise_risk_controls.ui import enterprise_risk_controls_ui_contract


def test_all_improve1_controls_have_executable_domain_evidence():
    contract = improve1_risk_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == RISK_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == RISK_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in RISK_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in RISK_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_risk_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = enterprise_risk_controls_runtime_capabilities()
    runtime_release = enterprise_risk_controls_build_release_evidence()
    smoke = enterprise_risk_controls_runtime_smoke()
    release = build_release_evidence()
    ui = enterprise_risk_controls_ui_contract()
    assert runtime["ok"] is True
    assert runtime["risk_control"]["ok"] is True
    assert "improve1_risk_control_contract" in runtime["operations"]
    assert len(runtime["improve1_risk_control_capabilities"]) == 50
    assert runtime_release["risk_control"]["ok"] is True
    assert release["risk_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["risk_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["risk_control_panels"]) == 50


def test_risk_intake_appetite_kri_and_assessment_guardrails_are_domain_specific():
    assert evaluate_risk_control(2, {"readiness_status": "draft"})["ok"] is False
    assert "incomplete draft risk" in evaluate_risk_control(2, {"readiness_status": "draft"})["findings"][0]
    assert evaluate_risk_control(3, {"residual_impact": 6})["ok"] is False
    assert evaluate_risk_control(4, {"simulation_result": "fail"})["ok"] is False
    assert evaluate_risk_control(5, {"quarantine_status": "quarantined"})["ok"] is False
    assert evaluate_risk_control(6, {"breach_drivers": ()})["ok"] is False


def test_control_evidence_attestation_exception_and_remediation_gates_are_enforced():
    assert evaluate_risk_control(10, {"independence_check": "failed"})["ok"] is False
    assert evaluate_risk_control(11, {"owned_metadata_only": False})["ok"] is False
    assert evaluate_risk_control(12, {"completeness_score": 0.5})["ok"] is False
    assert evaluate_risk_control(16, {"legal_acknowledgement": False})["ok"] is False
    assert evaluate_risk_control(17, {"independence_preserved": False})["ok"] is False
    assert evaluate_risk_control(21, {"closure_approval": False})["ok"] is False


def test_cross_pbc_access_sensitive_agent_and_model_controls_preserve_boundaries():
    cross = evaluate_risk_control(41)
    assert cross["ok"] is True
    assert cross["payload"]["owned_mutation_only"] is True
    assert set(cross["evidence"]["declared_dependencies"]).issubset(RISK_DECLARED_DEPENDENCIES)
    assert evaluate_risk_control(30, {"declared_projection_only": False})["ok"] is False
    assert evaluate_risk_control(31, {"segregation_failure": True})["ok"] is False
    assert evaluate_risk_control(38, {"api_enforcement": "disabled"})["ok"] is False
    assert evaluate_risk_control(39, {"human_confirmation": False})["ok"] is False
    assert evaluate_risk_control(29, {"validation_status": "draft"})["ok"] is False


def test_committee_lineage_resilience_narrative_release_and_workbench_controls_are_gated():
    assert evaluate_risk_control(23, {"immutable_snapshot": False})["ok"] is False
    assert evaluate_risk_control(26, {"integrity_proof": ""})["ok"] is False
    assert evaluate_risk_control(36, {"committee_visibility": False})["ok"] is False
    assert evaluate_risk_control(43, {"traceability_proof": ""})["ok"] is False
    assert evaluate_risk_control(46, {"temporal_consistency": False})["ok"] is False
    assert evaluate_risk_control(48, {"owner_approval": False})["ok"] is False
    assert evaluate_risk_control(49, {"retry_dead_letter_tests": "missing"})["ok"] is False
    assert evaluate_risk_control(50, {"auditor_view": "hidden"})["ok"] is False
