"""Domain behavior tests for legal matter management improve1 controls."""

from ..legal_control import (LEGAL_CONTROL_ALLOWED_DATABASE_BACKENDS, LEGAL_CONTROL_OWNED_TABLES, evaluate_legal_control, improve1_legal_control_contract, sample_payload_for)
from ..release_evidence import validate_release_evidence
from ..runtime import legal_matter_management_runtime_capabilities
from ..ui import legal_matter_management_render_workbench, legal_matter_management_ui_contract


def test_all_fifty_legal_controls_are_executable_and_owned():
    contract = improve1_legal_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LEGAL_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_legal_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LEGAL_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LegalMatterManagement")
        assert result["evidence"]["service_api"].startswith("POST /legal-matter-management/improve1/")


def test_runtime_ui_and_release_expose_legal_control_contract():
    runtime = legal_matter_management_runtime_capabilities()
    ui = legal_matter_management_ui_contract()
    workbench = legal_matter_management_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["legal_control"]["capability_count"] == 50
    assert "evaluate_legal_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["legal_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["legal_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["legal_control"]["ok"] is True


def test_intake_conflicts_holds_deadlines_and_privilege_have_negative_paths():
    cases = ((1, "intake_triage_confidence_approved"), (2, "conflict_clearance_recorded"), (5, "hold_scope_simulated"), (8, "deadline_dual_control_approved"), (13, "privilege_review_supervised"))
    for feature, key in cases:
        result = evaluate_legal_control(feature, {key: False})
        assert result["ok"] is False
        assert result["findings"]


def test_evidence_counsel_settlement_closure_and_projection_boundaries_are_gated():
    evidence = evaluate_legal_control(15, {"chain_of_custody_gap_blocked": False})
    counsel = evaluate_legal_control(20, {"invoice_compliance_review_complete": False})
    settlement = evaluate_legal_control(24, {"settlement_approval_policy_satisfied": False})
    closure = evaluate_legal_control(39, {"closure_obligations_cleared": False})
    boundary = evaluate_legal_control(47, {"projection_boundary_verified": False})
    assert not evidence["ok"] and not counsel["ok"] and not settlement["ok"] and not closure["ok"] and not boundary["ok"]


def test_agent_partition_release_and_workbench_controls_are_enforced():
    partition = evaluate_legal_control(44, {"sensitive_partition_enforced": False})
    agent = evaluate_legal_control(45, {"agent_intake_confirmation_required": False})
    drafting = evaluate_legal_control(46, {"legal_draft_human_approved": False})
    release = evaluate_legal_control(48, {"release_evidence_pack_verified": False})
    workbench = evaluate_legal_control(50, {"complete_workbench_coverage_visible": False})
    assert not partition["ok"] and not agent["ok"] and not drafting["ok"] and not release["ok"] and not workbench["ok"]


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_legal_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_legal_control(48, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_legal_control(47, {"stream_engine_picker_visible": True})
    shared_table = evaluate_legal_control(31, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(22)
    result = evaluate_legal_control(22, payload)
    assert result["ok"] is True
    assert payload["case_exposure_model_governed"] is True
    assert result["side_effects"] == ()
