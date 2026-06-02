"""Identity KYC/AML behavior checks for the improve1 executable control surface."""

from ..identity_control import (
    EVENT_CONTRACT,
    IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    IDENTITY_CONTROL_OWNED_TABLES,
    IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_identity_control,
    improve1_identity_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import identity_kyc_aml_compliance_build_release_evidence, identity_kyc_aml_compliance_runtime_capabilities
from ..ui import identity_kyc_aml_compliance_render_workbench, identity_kyc_aml_compliance_ui_contract


def test_all_improve1_features_have_executable_identity_control_evidence():
    contract = improve1_identity_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == IDENTITY_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == IDENTITY_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in IDENTITY_CONTROL_OWNED_TABLES
            assert table.startswith("identity_kyc_aml_compliance_")


def test_runtime_release_and_ui_expose_identity_control_contract():
    runtime = identity_kyc_aml_compliance_runtime_capabilities()
    runtime_release = identity_kyc_aml_compliance_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = identity_kyc_aml_compliance_ui_contract()
    workbench = identity_kyc_aml_compliance_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_identity_control_contract" in runtime["operations"]
    assert runtime["identity_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["identity_control"]["ok"] is True
    assert release["ok"] is True and release["identity_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["identity_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["identity_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["identity_control_service_actions"]) == 50


def test_profile_lifecycle_requires_transition_evidence_and_event():
    result = evaluate_identity_control(1, {"allowed_transition": False, "mandatory_evidence": "", "lifecycle_event_emitted": False})
    assert result["ok"] is False
    assert "lifecycle" in result["findings"][0]


def test_onboarding_classification_requires_obligations():
    result = evaluate_identity_control(2, {"customer_type": "", "jurisdiction": "", "obligation_set_attached": False})
    assert result["ok"] is False
    assert "classification" in result["findings"][0]


def test_duplicate_identity_resolution_blocks_unresolved_candidates():
    result = evaluate_identity_control(3, {"duplicate_candidates": ("profile-2",), "lineage_preserved": False})
    assert result["ok"] is False
    assert "duplicate" in result["findings"][0]


def test_document_authenticity_and_liveness_controls_block_bad_proofing():
    document = evaluate_identity_control(5, {"authenticity_state": "tampered", "expiry_state": "expired", "identity_consistency": False})
    liveness = evaluate_identity_control(6, {"liveness_outcome": "fail", "face_match_confidence": 0.31})
    assert document["ok"] is False and "document" in document["findings"][0]
    assert liveness["ok"] is False and "liveness" in liveness["findings"][0]


def test_screening_and_pep_boundaries_block_unresolved_or_wrong_closure():
    sanctions = evaluate_identity_control(7, {"unresolved_blocking_hit": True})
    pep = evaluate_identity_control(8, {"sanctions_only_close_blocked": False})
    assert sanctions["ok"] is False and "sanctions" in sanctions["findings"][0]
    assert pep["ok"] is False and "PEP" in pep["findings"][0]


def test_beneficial_ownership_and_edd_require_complete_control_evidence():
    ownership = evaluate_identity_control(10, {"ultimate_owner_reached": False})
    edd = evaluate_identity_control(15, {"packet_complete": False})
    assert ownership["ok"] is False and "beneficial ownership" in ownership["findings"][0]
    assert edd["ok"] is False and "EDD" in edd["findings"][0]


def test_sar_str_and_maker_checker_boundaries_are_enforced():
    filing = evaluate_identity_control(23, {"external_filing_mutation_blocked": False})
    approval = evaluate_identity_control(24, {"segregation_enforced": False, "same_user_blocked": False})
    assert filing["ok"] is False and "SAR/STR" in filing["findings"][0]
    assert approval["ok"] is False and "maker-checker" in approval["findings"][0]


def test_idempotency_file_safety_and_event_contracts_use_appgen_boundaries():
    idempotency = evaluate_identity_control(29, {"duplicate_profile_prevented": False, "stable_response": False})
    file_safety = evaluate_identity_control(30, {"malware_scan": "infected", "unsafe_file_blocked": False})
    events = evaluate_identity_control(32, {"appgen_contract": "external", "event_topic": "foreign.topic", "stream_engine_picker_visible": True})
    assert idempotency["ok"] is False and "idempotency" in idempotency["findings"][0]
    assert file_safety["ok"] is False and "file-safety" in file_safety["findings"][0]
    assert events["ok"] is False and "AppGen-X" in events["findings"][0]


def test_agent_skills_require_citations_confirmation_and_no_direct_mutation():
    for feature in (45, 46, 47):
        result = evaluate_identity_control(feature, {"human_confirmation": False, "direct_mutation_blocked": False, "source_citations": ()})
        assert result["ok"] is False
        assert "agent skills" in result["findings"][0]


def test_tenant_residency_and_end_to_end_control_proof_are_required():
    tenancy = evaluate_identity_control(49, {"queue_leakage_blocked": False, "cross_tenant_access_blocked": False})
    end_to_end = evaluate_identity_control(50, {"events_emitted": False, "release_documents_updated": False})
    assert tenancy["ok"] is False and "multi-tenant" in tenancy["findings"][0]
    assert end_to_end["ok"] is False and "end-to-end" in end_to_end["findings"][0]
