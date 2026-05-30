"""Domain behavior checks for facility_energy_management improve1 controls."""

from pyAppGen.pbcs.facility_energy_management.energy_control import (
    ENERGY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    ENERGY_CONTROL_DECLARED_DEPENDENCIES,
    ENERGY_CONTROL_OWNED_TABLES,
    ENERGY_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_energy_control,
    improve1_energy_control_contract,
)
from pyAppGen.pbcs.facility_energy_management.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.facility_energy_management.runtime import (
    facility_energy_management_build_release_evidence,
    facility_energy_management_runtime_capabilities,
    facility_energy_management_runtime_smoke,
)
from pyAppGen.pbcs.facility_energy_management.ui import facility_energy_management_ui_contract


def test_all_improve1_controls_have_executable_energy_evidence():
    contract = improve1_energy_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ENERGY_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == ENERGY_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in ENERGY_CONTROL_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in ENERGY_CONTROL_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_energy_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = facility_energy_management_runtime_capabilities()
    runtime_release = facility_energy_management_build_release_evidence()
    smoke = facility_energy_management_runtime_smoke()
    release = build_release_evidence()
    ui = facility_energy_management_ui_contract()
    assert runtime["ok"] is True
    assert runtime["energy_control"]["ok"] is True
    assert "improve1_energy_control_contract" in runtime["operations"]
    assert len(runtime["improve1_energy_control_capabilities"]) == 50
    assert runtime_release["energy_control"]["ok"] is True
    assert release["energy_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["energy_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["energy_control_panels"]) == 50


def test_meter_interval_tariff_schedule_and_control_boundaries_are_gated():
    assert evaluate_energy_control(1, {"rollup_validation": "failed"})["ok"] is False
    assert evaluate_energy_control(2, {"dst_handling": "missing"})["ok"] is False
    assert evaluate_energy_control(3, {"health_status": "stale"})["ok"] is False
    assert evaluate_energy_control(4, {"service_mapping_approved": False})["ok"] is False
    assert evaluate_energy_control(5, {"revision_permission": "denied"})["ok"] is False
    assert evaluate_energy_control(6, {"tariff_calendar_valid": False})["ok"] is False
    assert evaluate_energy_control(7, {"determinant_computed": False})["ok"] is False
    assert evaluate_energy_control(8, {"non_mutating_scenario": False})["ok"] is False
    assert evaluate_energy_control(11, {"overlap_status": "conflict"})["ok"] is False
    assert evaluate_energy_control(12, {"direct_device_write_blocked": False})["ok"] is False


def test_demand_response_carbon_tenant_and_agent_controls_are_enforced():
    assert evaluate_energy_control(13, {"expired_override_effect": "active"})["ok"] is False
    assert evaluate_energy_control(14, {"blocked_recommendation": False})["ok"] is False
    assert evaluate_energy_control(15, {"overlap_check": "overlap"})["ok"] is False
    assert evaluate_energy_control(21, {"protected_load_rejected": False})["ok"] is False
    assert evaluate_energy_control(22, {"state_transition_valid": False})["ok"] is False
    assert evaluate_energy_control(24, {"shed_plan_blocked": False})["ok"] is False
    assert evaluate_energy_control(25, {"rebound_peak_controlled": False})["ok"] is False
    assert evaluate_energy_control(26, {"historical_period_rewrite_blocked": False})["ok"] is False
    assert evaluate_energy_control(33, {"source_span_citations": ()})["ok"] is False
    assert evaluate_energy_control(34, {"mutation_requires_approval": False})["ok"] is False
    assert evaluate_energy_control(35, {"evidence_complete": False})["ok"] is False


def test_event_isolation_parameters_models_freshness_and_release_drill_are_enforced():
    assert evaluate_energy_control(40, {"non_mutating_results": False})["ok"] is False
    assert evaluate_energy_control(42, {"exactly_once_business_effect": False})["ok"] is False
    assert evaluate_energy_control(43, {"cross_tenant_negative_test": "failed"})["ok"] is False
    assert evaluate_energy_control(44, {"safe_bounds": "failed"})["ok"] is False
    assert evaluate_energy_control(45, {"high_severity_passed": False})["ok"] is False
    assert evaluate_energy_control(46, {"core_key_collision_blocked": False})["ok"] is False
    assert evaluate_energy_control(48, {"high_risk_blocked_when_stale": False})["ok"] is False
    assert evaluate_energy_control(50, {"manual_database_edits_absent": False})["ok"] is False
    assert evaluate_energy_control(50)["ok"] is True
