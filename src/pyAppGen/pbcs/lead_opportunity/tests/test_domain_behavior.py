"""Domain behavior tests for lead opportunity improve1 controls."""

from ..lead_control import (
    LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LEAD_CONTROL_OWNED_TABLES,
    evaluate_lead_control,
    improve1_lead_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import lead_opportunity_runtime_capabilities
from ..ui import lead_opportunity_ui_contract


def test_all_fifty_lead_controls_are_executable_and_owned():
    contract = improve1_lead_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LEAD_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_lead_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LEAD_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LeadOpportunity")
        assert result["evidence"]["service_api"].startswith("POST /lead-opportunity/improve1/")


def test_runtime_ui_and_release_expose_lead_control_contract():
    runtime = lead_opportunity_runtime_capabilities()
    ui = lead_opportunity_ui_contract()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["lead_control"]["capability_count"] == 50
    assert "evaluate_lead_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["lead_control_panels"]) == 50
    assert release["ok"] is True
    assert release["lead_control"]["ok"] is True


def test_account_lead_qualification_and_opportunity_gates_have_negative_paths():
    account = evaluate_lead_control(1, {"account_readiness_gate_passed": False})
    intake = evaluate_lead_control(3, {"lead_intake_ready": False})
    qualification = evaluate_lead_control(9, {"lead_qualified_event_evidence": False})
    opportunity = evaluate_lead_control(11, {"opportunity_creation_ready": False})
    assert account["ok"] is False
    assert intake["ok"] is False
    assert qualification["ok"] is False
    assert opportunity["ok"] is False
    assert any("account hierarchy readiness" in finding for finding in account["findings"])
    assert any("lead intake" in finding for finding in intake["findings"])


def test_quote_win_boundary_and_customer_update_controls_are_gated():
    quote = evaluate_lead_control(17, {"quote_proposal_event_evidence": False})
    win = evaluate_lead_control(19, {"win_handoff_ready": False})
    boundary = evaluate_lead_control(33, {"foreign_table_access_blocked": False})
    customer_update = evaluate_lead_control(48, {"customer_update_governed": False})
    assert quote["ok"] is False
    assert win["ok"] is False
    assert boundary["ok"] is False
    assert customer_update["ok"] is False
    assert any("QuoteProposalRequested" in finding for finding in quote["findings"])
    assert any("OpportunityWon" in finding for finding in win["findings"])
    assert any("foreign" in finding for finding in boundary["findings"])


def test_agent_semantic_and_continuous_control_safety_is_enforced():
    semantic = evaluate_lead_control(40, {"no_mutation_until_confirmed": False})
    agent_plan = evaluate_lead_control(41, {"human_confirmation": False})
    controls = evaluate_lead_control(46, {"continuous_controls_pass": False})
    proof = evaluate_lead_control(50, {"end_to_end_proof_complete": False})
    assert semantic["ok"] is False
    assert agent_plan["ok"] is False
    assert controls["ok"] is False
    assert proof["ok"] is False


def test_database_eventing_and_projection_boundary_constraints_are_enforced():
    bad_backend = evaluate_lead_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_lead_control(25, {"event_contract": "Kafka"})
    stream_picker = evaluate_lead_control(32, {"stream_engine_picker_visible": True})
    projection_shared_table = evaluate_lead_control(25, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert projection_shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(14)
    result = evaluate_lead_control(14, payload)
    assert result["ok"] is True
    assert payload["forecast_reproducible"] is True
    assert result["side_effects"] == ()
