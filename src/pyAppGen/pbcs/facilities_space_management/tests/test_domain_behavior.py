"""Domain behavior checks for facilities_space_management improve1 controls."""

from pyAppGen.pbcs.facilities_space_management.facilities_control import (
    FACILITIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FACILITIES_CONTROL_DECLARED_DEPENDENCIES,
    FACILITIES_CONTROL_OWNED_TABLES,
    FACILITIES_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_facilities_control,
    improve1_facilities_control_contract,
)
from pyAppGen.pbcs.facilities_space_management.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.facilities_space_management.runtime import (
    facilities_space_management_build_release_evidence,
    facilities_space_management_runtime_capabilities,
    facilities_space_management_runtime_smoke,
)
from pyAppGen.pbcs.facilities_space_management.ui import facilities_space_management_ui_contract


def test_all_improve1_controls_have_executable_facilities_evidence():
    contract = improve1_facilities_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == FACILITIES_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == FACILITIES_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in FACILITIES_CONTROL_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in FACILITIES_CONTROL_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_facilities_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = facilities_space_management_runtime_capabilities()
    runtime_release = facilities_space_management_build_release_evidence()
    smoke = facilities_space_management_runtime_smoke()
    release = build_release_evidence()
    ui = facilities_space_management_ui_contract()
    assert runtime["ok"] is True
    assert runtime["facilities_control"]["ok"] is True
    assert "improve1_facilities_control_contract" in runtime["operations"]
    assert len(runtime["improve1_facilities_control_capabilities"]) == 50
    assert runtime_release["facilities_control"]["ok"] is True
    assert release["facilities_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["facilities_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["facilities_control_panels"]) == 50


def test_reservation_occupancy_privacy_and_setup_controls_are_gated():
    assert evaluate_facilities_control(1, {"site_status": "unknown"})["ok"] is False
    assert evaluate_facilities_control(2, {"map_version": ""})["ok"] is False
    assert evaluate_facilities_control(6, {"capacity_validation": "failed"})["ok"] is False
    assert evaluate_facilities_control(7, {"hr_mutation_blocked": False})["ok"] is False
    assert evaluate_facilities_control(8, {"maintenance_block_check": "blocked"})["ok"] is False
    assert evaluate_facilities_control(10, {"confirmation_gate": "missing"})["ok"] is False
    assert evaluate_facilities_control(13, {"aggregation_threshold": 1})["ok"] is False


def test_move_safety_access_lease_and_inclusive_controls_block_domain_edge_cases():
    assert evaluate_facilities_control(15, {"release_criteria": "unmet"})["ok"] is False
    assert evaluate_facilities_control(17, {"critical_dependencies_open": ("it_setup",)})["ok"] is False
    assert evaluate_facilities_control(18, {"policy_basis": ""})["ok"] is False
    assert evaluate_facilities_control(20, {"hazard_severity": "critical", "space_block_decision": "not_blocked"})["ok"] is False
    assert evaluate_facilities_control(25, {"foreign_mutation_blocked": False})["ok"] is False
    assert evaluate_facilities_control(27, {"violation_blocked": False})["ok"] is False
    assert evaluate_facilities_control(31, {"access_respected": False})["ok"] is False


def test_agent_boundary_release_event_and_workbench_controls_are_enforced():
    assert evaluate_facilities_control(40, {"source_citations": ()})["ok"] is False
    assert evaluate_facilities_control(41, {"materiality": "material", "approval_required": False})["ok"] is False
    assert evaluate_facilities_control(43, {"foreign_work_order_mutation": ("work_order",)})["ok"] is False
    assert evaluate_facilities_control(44, {"shared_table_mutation_blocked": False})["ok"] is False
    assert evaluate_facilities_control(48, {"retry_dead_letter_tests": "missing"})["ok"] is False
    assert evaluate_facilities_control(49, {"unknown_event_mutation_blocked": False})["ok"] is False
    assert evaluate_facilities_control(50, {"employee_workbench": False})["ok"] is False
    assert evaluate_facilities_control(50)["ok"] is True
