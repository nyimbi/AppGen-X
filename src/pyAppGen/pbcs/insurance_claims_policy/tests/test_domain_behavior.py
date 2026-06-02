"""Insurance claims and policy behavior checks for the improve1 executable control surface."""

from ..claims_control import (
    CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS,
    CLAIMS_CONTROL_OWNED_TABLES,
    CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC,
    EVENT_CONTRACT,
    evaluate_claims_control,
    improve1_claims_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import insurance_claims_policy_build_release_evidence, insurance_claims_policy_runtime_capabilities
from ..ui import insurance_claims_policy_render_workbench, insurance_claims_policy_ui_contract


def test_all_improve1_features_have_executable_claims_control_evidence():
    contract = improve1_claims_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == CLAIMS_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == CLAIMS_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in CLAIMS_CONTROL_OWNED_TABLES
            assert table.startswith("insurance_claims_policy_")


def test_runtime_release_and_ui_expose_claims_control_contract():
    runtime = insurance_claims_policy_runtime_capabilities()
    runtime_release = insurance_claims_policy_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = insurance_claims_policy_ui_contract()
    workbench = insurance_claims_policy_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_claims_control_contract" in runtime["operations"]
    assert runtime["claims_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["claims_control"]["ok"] is True
    assert release["ok"] is True and release["claims_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["claims_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["claims_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["claims_control_service_actions"]) == 50


def test_policy_issuance_blocks_until_readiness_evidence_is_complete():
    result = evaluate_claims_control(2, {"policyholder_verified": False, "risk_details_complete": False, "policy_created_blocked_until_ready": False})
    assert result["ok"] is False
    assert "Policy Issuance Readiness Gate" in result["findings"][0]


def test_effective_dated_policy_versioning_reconstructs_loss_time_terms():
    result = evaluate_claims_control(6, {"current_record_not_used_for_loss": False, "version_cited": False})
    assert result["ok"] is False
    assert "Effective-Dated Policy Versioning" in result["findings"][0]


def test_claimant_payee_authority_blocks_unresolved_payments():
    result = evaluate_claims_control(11, {"payment_blocked_without_authority": False})
    assert result["ok"] is False
    assert "Claimant Role" in result["findings"][0]


def test_coverage_letters_and_fair_claim_timers_have_governed_controls():
    coverage = evaluate_claims_control(13, {"decision_citations": ""})
    letter = evaluate_claims_control(14, {"waiver_guard": False})
    fair_claims = evaluate_claims_control(20, {"breach_exception_opened": False})
    assert coverage["ok"] is False and "coverage reasoning" in " ".join(coverage["findings"]).lower()
    assert letter["ok"] is False and "Reservation" in letter["findings"][0]
    assert fair_claims["ok"] is False and "Regulatory Fair Claims" in fair_claims["findings"][0]


def test_fraud_and_adverse_action_paths_require_human_review():
    fraud = evaluate_claims_control(21, {"human_review_before_adverse_action": False, "confidence": 0.2})
    governance = evaluate_claims_control(48, {"human_review": False, "adverse_action_guard": False})
    assert fraud["ok"] is False and "Fraud Signal Fusion" in fraud["findings"][0]
    assert governance["ok"] is False and "Claim Fraud Governance" in governance["findings"][0]


def test_settlement_authority_and_disbursement_controls_block_unsafe_payment():
    authority = evaluate_claims_control(30, {"payment_blocked_until_approved": False, "release_complete": False})
    payment = evaluate_claims_control(31, {"duplicate_payment_check": False, "payee_validation": False})
    assert authority["ok"] is False and "Settlement Authority" in authority["findings"][0]
    assert payment["ok"] is False and "Payment Calculation" in payment["findings"][0]


def test_agent_intake_requires_citations_confirmation_and_no_direct_mutation():
    result = evaluate_claims_control(36, {"source_citations": (), "human_confirmation": False, "direct_mutation_blocked": False})
    assert result["ok"] is False
    assert "Agent-Assisted" in result["findings"][0]


def test_cross_pbc_projection_boundaries_block_shared_tables():
    result = evaluate_claims_control(45, {"dependency_mode": "shared_table", "foreign_table_access_blocked": False})
    assert result["ok"] is False
    assert "Cross-PBC" in result["findings"][0]


def test_end_to_end_release_evidence_requires_full_claims_execution():
    result = evaluate_claims_control(50, {"events_emitted": False, "release_documents_updated": False})
    assert result["ok"] is False
    assert "End-to-End" in result["findings"][0]
