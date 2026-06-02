from pyAppGen.pbcs.contract_lifecycle.application import ALLOWED_DATABASE_BACKENDS, REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.contract_lifecycle.contract_control import (
    CAPABILITY_TABLES,
    CONTRACT_CONTROL_CAPABILITIES,
    CONTRACT_CONTROL_FUNCTIONS,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    SLUG_BY_NUMBER,
    evaluate_contract_control,
    improve1_contract_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.contract_lifecycle.release_evidence import build_release_evidence
from pyAppGen.pbcs.contract_lifecycle.runtime import contract_lifecycle_runtime_capabilities, contract_lifecycle_runtime_smoke
from pyAppGen.pbcs.contract_lifecycle.ui import contract_lifecycle_ui_contract


def test_all_50_contract_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(CONTRACT_CONTROL_CAPABILITIES) == 50
    assert set(CONTRACT_CONTROL_CAPABILITIES) == set(CONTRACT_CONTROL_FUNCTIONS)

    for capability in CONTRACT_CONTROL_CAPABILITIES:
        result = CONTRACT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("contract_lifecycle_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == REQUIRED_EVENT_TOPIC
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == ALLOWED_DATABASE_BACKENDS
        assert result["agent_skill"].startswith("contract_lifecycle_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_contract_controls_reject_missing_fields_and_foreign_table_access():
    first = CONTRACT_CONTROL_CAPABILITIES[0]
    missing = evaluate_contract_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("customer_master_table",)
    rejected = evaluate_contract_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("customer_master_table",)


def test_intake_state_signature_document_and_obligation_controls_surface_review_findings():
    state = sample_payload_for(SLUG_BY_NUMBER[2])
    state["target_state"] = "quietly_signed"
    assert "invalid_contract_lifecycle_transition_target" in evaluate_contract_control(SLUG_BY_NUMBER[2], state)["domain_findings"]

    authority = sample_payload_for(SLUG_BY_NUMBER[5])
    authority["identity_verified"] = False
    assert "signing_authority_requires_verified_identity" in evaluate_contract_control(SLUG_BY_NUMBER[5], authority)["domain_findings"]

    extraction = sample_payload_for(SLUG_BY_NUMBER[8])
    extraction["confidence"] = 0.42
    assert "semantic_clause_extraction_requires_citations_and_confidence" in evaluate_contract_control(SLUG_BY_NUMBER[8], extraction)["domain_findings"]

    packet = sample_payload_for(SLUG_BY_NUMBER[10])
    packet["final_hash"] = ""
    assert "document_packet_requires_final_integrity_hash" in evaluate_contract_control(SLUG_BY_NUMBER[10], packet)["domain_findings"]

    obligation = sample_payload_for(SLUG_BY_NUMBER[20])
    obligation["evidence_requirement"] = ""
    assert "obligation_activation_requires_evidence_requirement" in evaluate_contract_control(SLUG_BY_NUMBER[20], obligation)["domain_findings"]


def test_legal_hold_boundary_agent_resilience_and_release_controls_require_governance():
    hold = sample_payload_for(SLUG_BY_NUMBER[33])
    hold.update({"legal_hold_state": "active", "destruction_eligibility": True})
    assert "legal_hold_blocks_destruction" in evaluate_contract_control(SLUG_BY_NUMBER[33], hold)["domain_findings"]

    boundary = sample_payload_for(SLUG_BY_NUMBER[42])
    boundary["dependency_mode"] = "shared_table"
    assert "cross_pbc_boundary_must_use_api_event_or_projection" in evaluate_contract_control(SLUG_BY_NUMBER[42], boundary)["domain_findings"]

    redline = sample_payload_for(SLUG_BY_NUMBER[44])
    redline["authorized_confirmation"] = False
    redline_review = evaluate_contract_control(SLUG_BY_NUMBER[44], redline)
    assert "agent_redline_review_cannot_accept_without_authorized_confirmation" in redline_review["domain_findings"]
    assert redline_review["requires_human_confirmation"] is True

    drill = sample_payload_for(SLUG_BY_NUMBER[48])
    drill["recovery_time_minutes"] = 120
    assert "resilience_drill_exceeds_recovery_target" in evaluate_contract_control(SLUG_BY_NUMBER[48], drill)["domain_findings"]

    proof = sample_payload_for(SLUG_BY_NUMBER[50])
    proof["boundary_verification"] = False
    assert "end_to_end_release_proof_requires_boundary_verification" in evaluate_contract_control(SLUG_BY_NUMBER[50], proof)["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_contract_control_contract():
    contract = improve1_contract_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == ALLOWED_DATABASE_BACKENDS

    runtime = contract_lifecycle_runtime_capabilities()
    smoke = contract_lifecycle_runtime_smoke()
    release = build_release_evidence()
    ui = contract_lifecycle_ui_contract()

    assert runtime["improve1_contract_control"]["ok"] is True
    assert smoke["improve1_contract_control"]["ok"] is True
    assert any(check["id"] == "improve1_contract_control" and check["ok"] for check in smoke["checks"])
    assert release["improve1_contract_control"]["capability_count"] == 50
    assert len(ui["contract_control_panels"]) == 50
    assert ui["contract_control_contract"]["ok"] is True
