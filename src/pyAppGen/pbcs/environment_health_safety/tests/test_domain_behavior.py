"""Domain behavior checks for environment_health_safety improve1 controls."""

from pyAppGen.pbcs.environment_health_safety.ehs_control import (
    EHS_ALLOWED_DATABASE_BACKENDS,
    EHS_DECLARED_DEPENDENCIES,
    EHS_OWNED_TABLES,
    EHS_REQUIRED_EVENT_TOPIC,
    evaluate_ehs_control,
    improve1_ehs_control_contract,
)
from pyAppGen.pbcs.environment_health_safety.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.environment_health_safety.runtime import (
    environment_health_safety_build_release_evidence,
    environment_health_safety_runtime_capabilities,
    environment_health_safety_runtime_smoke,
)
from pyAppGen.pbcs.environment_health_safety.ui import environment_health_safety_ui_contract


def test_all_improve1_controls_have_executable_ehs_evidence():
    contract = improve1_ehs_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == EHS_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == EHS_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in EHS_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in EHS_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_ehs_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = environment_health_safety_runtime_capabilities()
    runtime_release = environment_health_safety_build_release_evidence()
    smoke = environment_health_safety_runtime_smoke()
    release = build_release_evidence()
    ui = environment_health_safety_ui_contract()
    assert runtime["ok"] is True
    assert runtime["ehs_control"]["ok"] is True
    assert "improve1_ehs_control_contract" in runtime["operations"]
    assert len(runtime["improve1_ehs_control_capabilities"]) == 50
    assert runtime_release["ehs_control"]["ok"] is True
    assert release["ehs_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["ehs_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["ehs_control_panels"]) == 50


def test_incident_investigation_permit_training_and_medical_boundaries_are_gated():
    assert evaluate_ehs_control(1, {"lifecycle_state": "unknown"})["ok"] is False
    assert evaluate_ehs_control(3, {"root_cause": ""})["ok"] is False
    assert evaluate_ehs_control(5, {"verifier_evidence": ""})["ok"] is False
    assert evaluate_ehs_control(10, {"conflict_rule": "blocked"})["ok"] is False
    assert evaluate_ehs_control(12, {"missing_prerequisites": ("gas_test",)})["ok"] is False
    assert evaluate_ehs_control(14, {"mid_job_lapse_flag": True})["ok"] is False
    assert evaluate_ehs_control(16, {"health_detail_excluded": False})["ok"] is False


def test_assistant_policy_event_and_evidence_controls_block_unsafe_ehs_actions():
    assert evaluate_ehs_control(24, {"source_citations": ()})["ok"] is False
    assert evaluate_ehs_control(25, {"no_auto_issue": False})["ok"] is False
    assert evaluate_ehs_control(27, {"no_direct_mutation": False})["ok"] is False
    assert evaluate_ehs_control(31, {"idempotent_replay": False})["ok"] is False
    assert evaluate_ehs_control(32, {"edit_blocked": False})["ok"] is False
    assert evaluate_ehs_control(40, {"tamper_check": "failed"})["ok"] is False


def test_isolation_agent_federation_release_scenario_and_metrics_are_enforced():
    assert evaluate_ehs_control(39, {"serious_notification_assertion": "failed"})["ok"] is False
    assert evaluate_ehs_control(41, {"negative_access_tests": "failed"})["ok"] is False
    assert evaluate_ehs_control(43, {"no_autonomous_permit_issue": False})["ok"] is False
    assert evaluate_ehs_control(46, {"foreign_table_access": ("maintenance_work_order",)})["ok"] is False
    assert evaluate_ehs_control(49, {"permit_issued": "missing"})["ok"] is False
    assert evaluate_ehs_control(50, {"metric_drilldown": "available"})["ok"] is True
