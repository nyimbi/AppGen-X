"""Domain behavior tests for library and archives improve1 controls."""

from ..library_control import (
    LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LIBRARY_CONTROL_OWNED_TABLES,
    evaluate_library_control,
    improve1_library_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import library_archives_management_runtime_capabilities
from ..ui import library_archives_management_render_workbench, library_archives_management_ui_contract


def test_all_fifty_library_controls_are_executable_and_owned():
    contract = improve1_library_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LIBRARY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_library_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LIBRARY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LibraryArchivesManagement")
        assert result["evidence"]["service_api"].startswith("POST /library-archives-management/improve1/")


def test_runtime_ui_and_release_expose_library_control_contract():
    runtime = library_archives_management_runtime_capabilities()
    ui = library_archives_management_ui_contract()
    workbench = library_archives_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["library_control"]["capability_count"] == 50
    assert "evaluate_library_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["library_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["library_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["library_control"]["ok"] is True


def test_cataloging_accessioning_rights_and_preservation_have_negative_paths():
    cases = (
        (1, "material_template_validation_complete"),
        (2, "authority_resolution_lineage_recorded"),
        (4, "accession_register_custody_complete"),
        (6, "donor_restriction_clause_enforced"),
        (14, "condition_survey_preservation_risk_recorded"),
        (20, "fixity_revalidation_evidence_verified"),
    )
    for feature, key in cases:
        result = evaluate_library_control(feature, {key: False})
        assert result["ok"] is False
        assert result["findings"]


def test_circulation_reading_room_digitization_and_inventory_are_gated():
    reading_room = evaluate_library_control(10, {"paging_lifecycle_state_controlled": False})
    hold = evaluate_library_control(11, {"hold_queue_priority_explained": False})
    renewal = evaluate_library_control(12, {"renewal_recall_overdue_policy_applied": False})
    digitization = evaluate_library_control(17, {"digitization_triage_rights_preservation_cleared": False})
    inventory = evaluate_library_control(44, {"inventory_discrepancy_reconciliation_opened": False})
    assert not reading_room["ok"] and not hold["ok"] and not renewal["ok"]
    assert not digitization["ok"] and not inventory["ok"]


def test_agent_projection_release_and_control_boundaries_are_enforced():
    catalog_agent = evaluate_library_control(35, {"cataloging_agent_suggestion_cited": False})
    accession_agent = evaluate_library_control(36, {"human_confirmation": False})
    rights_agent = evaluate_library_control(38, {"rights_agent_human_signoff_required": False})
    projection = evaluate_library_control(43, {"operational_readiness_projection_fresh": False})
    release = evaluate_library_control(48, {"scenario_release_evidence_mapped": False})
    controls = evaluate_library_control(49, {"repository_control_assertion_actionable": False})
    gate = evaluate_library_control(50, {"end_to_end_release_gate_passed": False})
    assert not catalog_agent["ok"] and not accession_agent["ok"] and not rights_agent["ok"]
    assert not projection["ok"] and not release["ok"] and not controls["ok"] and not gate["ok"]


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_library_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_library_control(49, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_library_control(43, {"stream_engine_picker_visible": True})
    shared_table = evaluate_library_control(29, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(39)
    result = evaluate_library_control(39, payload)
    assert result["ok"] is True
    assert payload["provenance_authenticity_ledger_sealed"] is True
    assert result["side_effects"] == ()
