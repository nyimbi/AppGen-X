"""Domain behavior tests for livestock herd improve1 controls."""

from ..livestock_control import (
    LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LIVESTOCK_CONTROL_OWNED_TABLES,
    evaluate_livestock_control,
    improve1_livestock_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import livestock_herd_management_runtime_capabilities
from ..ui import livestock_herd_management_render_workbench, livestock_herd_management_ui_contract


def test_all_fifty_livestock_controls_are_executable_and_owned():
    contract = improve1_livestock_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LIVESTOCK_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_livestock_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LIVESTOCK_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LivestockHerdManagement")
        assert result["evidence"]["service_api"].startswith("POST /livestock-herd-management/improve1/")


def test_runtime_ui_and_release_expose_livestock_control_contract():
    runtime = livestock_herd_management_runtime_capabilities()
    ui = livestock_herd_management_ui_contract()
    workbench = livestock_herd_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["livestock_control"]["capability_count"] == 50
    assert "evaluate_livestock_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["livestock_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["livestock_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["livestock_control"]["ok"] is True


def test_identity_health_treatment_withdrawal_and_biosecurity_negative_paths():
    cases = (
        (1, "tag_history_identity_continuity_verified"),
        (6, "quarantine_release_criteria_met"),
        (7, "clinical_taxonomy_reportability_coded"),
        (9, "treatment_ledger_schedule_complete"),
        (10, "withdrawal_residue_release_date_enforced"),
    )
    for feature, key in cases:
        result = evaluate_livestock_control(feature, {key: False})
        assert result["ok"] is False
        assert result["findings"]


def test_breeding_feed_movement_and_compliance_controls_are_gated():
    breeding = evaluate_livestock_control(15, {"breeding_eligibility_rule_cited": False})
    birth = evaluate_livestock_control(18, {"offspring_lineage_created_from_birth": False})
    ration = evaluate_livestock_control(20, {"feed_ration_nutrient_evidence_complete": False})
    feed_boundary = evaluate_livestock_control(22, {"feed_inventory_projection_only_used": False})
    movement = evaluate_livestock_control(26, {"movement_permit_arrival_confirmed": False})
    report = evaluate_livestock_control(29, {"regulatory_report_due_exception_handled": False})
    assert not breeding["ok"] and not birth["ok"] and not ration["ok"]
    assert not feed_boundary["ok"] and not movement["ok"] and not report["ok"]


def test_weather_staff_equipment_agents_events_and_release_controls_are_enforced():
    weather = evaluate_livestock_control(35, {"heat_stress_mitigation_task_closed": False})
    staff = evaluate_livestock_control(36, {"staff_competency_projection_verified": False})
    equipment = evaluate_livestock_control(37, {"equipment_readiness_blocks_session": False})
    agent = evaluate_livestock_control(43, {"human_confirmation": False})
    eventing = evaluate_livestock_control(46, {"appgen_event_boundary_verified": False})
    audit = evaluate_livestock_control(47, {"cryptographic_audit_packet_verified": False})
    boundary = evaluate_livestock_control(50, {"cross_pbc_boundary_proof_passed": False})
    assert not weather["ok"] and not staff["ok"] and not equipment["ok"] and not agent["ok"]
    assert not eventing["ok"] and not audit["ok"] and not boundary["ok"]


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_livestock_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_livestock_control(47, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_livestock_control(46, {"stream_engine_picker_visible": True})
    shared_table = evaluate_livestock_control(22, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(27)
    result = evaluate_livestock_control(27, payload)
    assert result["ok"] is True
    assert payload["birth_to_sale_trace_packet_complete"] is True
    assert result["side_effects"] == ()
