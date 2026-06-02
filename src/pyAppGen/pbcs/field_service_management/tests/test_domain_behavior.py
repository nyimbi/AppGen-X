"""Domain behavior checks for field_service_management improve1 controls."""

from pyAppGen.pbcs.field_service_management.field_control import (
    FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FIELD_CONTROL_DECLARED_DEPENDENCIES,
    FIELD_CONTROL_OWNED_TABLES,
    FIELD_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_field_control,
    improve1_field_control_contract,
)
from pyAppGen.pbcs.field_service_management.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.field_service_management.runtime import (
    field_service_management_build_release_evidence,
    field_service_management_runtime_capabilities,
    field_service_management_runtime_smoke,
)
from pyAppGen.pbcs.field_service_management.ui import field_service_management_ui_contract


def test_all_improve1_controls_have_executable_field_evidence():
    contract = improve1_field_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == FIELD_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in FIELD_CONTROL_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in FIELD_CONTROL_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_field_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = field_service_management_runtime_capabilities()
    runtime_release = field_service_management_build_release_evidence()
    smoke = field_service_management_runtime_smoke()
    release = build_release_evidence()
    ui = field_service_management_ui_contract()
    assert runtime["ok"] is True
    assert runtime["field_control"]["ok"] is True
    assert "improve1_field_control_contract" in runtime["operations"]
    assert len(runtime["improve1_field_control_capabilities"]) == 50
    assert runtime_release["field_control"]["ok"] is True
    assert release["field_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["field_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["field_control_panels"]) == 50


def test_dispatch_location_skill_tool_and_safety_controls_are_gated():
    assert evaluate_field_control(1, {"entitlement_lookup": ""})["ok"] is False
    assert evaluate_field_control(2, {"allowed_transition": False})["ok"] is False
    assert evaluate_field_control(4, {"profile_completeness_score": 0.2})["ok"] is False
    assert evaluate_field_control(5, {"expiry_date": "2025-01-01"})["ok"] is False
    assert evaluate_field_control(7, {"consent_basis": "expired"})["ok"] is False
    assert evaluate_field_control(9, {"hard_constraints": "violated"})["ok"] is False
    assert evaluate_field_control(10, {"dispatcher_approval": False})["ok"] is False
    assert evaluate_field_control(11, {"weighted_assignment_score": 0.1})["ok"] is False
    assert evaluate_field_control(16, {"calibration_status": "expired"})["ok"] is False
    assert evaluate_field_control(17, {"completion_allowed": False})["ok"] is False
    assert evaluate_field_control(23, {"safety_gate_complete": False})["ok"] is False


def test_mobile_parts_customer_finance_fleet_and_agent_controls_are_enforced():
    assert evaluate_field_control(21, {"safe_merge_decision": "unsafe"})["ok"] is False
    assert evaluate_field_control(22, {"blocked_tasks": ("diagnosis",)})["ok"] is False
    assert evaluate_field_control(29, {"approval_status": "pending", "scope_block": "none"})["ok"] is False
    assert evaluate_field_control(38, {"contact_confirmation": "missing"})["ok"] is False
    assert evaluate_field_control(42, {"finance_mutation_blocked": False})["ok"] is False
    assert evaluate_field_control(44, {"fleet_master_mutation_blocked": False})["ok"] is False
    assert evaluate_field_control(45, {"source_citations": ()})["ok"] is False
    assert evaluate_field_control(46, {"human_confirmation": False})["ok"] is False


def test_boundary_release_and_complete_workbench_controls_are_enforced():
    assert evaluate_field_control(48, {"owned_table_mutation_only": False})["ok"] is False
    assert evaluate_field_control(49, {"retry_dead_letter_tests": "failed"})["ok"] is False
    assert evaluate_field_control(49, {"privacy_consent_tests": "failed"})["ok"] is False
    assert evaluate_field_control(49, {"offline_replay_smoke": "failed"})["ok"] is False
    assert evaluate_field_control(50, {"technician_workbench": False})["ok"] is False
    assert evaluate_field_control(50)["ok"] is True
