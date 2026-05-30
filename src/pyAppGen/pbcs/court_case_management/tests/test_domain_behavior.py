from pyAppGen.pbcs.court_case_management.court_control import (
    CAPABILITY_TABLES,
    COURT_CONTROL_CAPABILITIES,
    COURT_CONTROL_FUNCTIONS,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    SLUG_BY_NUMBER,
    evaluate_court_control,
    improve1_court_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.court_case_management.runtime import (
    COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
    COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    court_case_management_build_release_evidence,
    court_case_management_runtime_capabilities,
    court_case_management_runtime_smoke,
)
from pyAppGen.pbcs.court_case_management.ui import court_case_management_ui_contract


def test_all_50_court_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(COURT_CONTROL_CAPABILITIES) == 50
    assert set(COURT_CONTROL_CAPABILITIES) == set(COURT_CONTROL_FUNCTIONS)

    for capability in COURT_CONTROL_CAPABILITIES:
        result = COURT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("court_case_management_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
        assert result["agent_skill"].startswith("court_case_management_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_court_controls_reject_missing_fields_and_foreign_table_access():
    first = COURT_CONTROL_CAPABILITIES[0]
    missing = evaluate_court_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("county_party_table",)
    rejected = evaluate_court_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("county_party_table",)


def test_case_filing_docket_order_hearing_and_service_controls_surface_review_findings():
    numbering = sample_payload_for(SLUG_BY_NUMBER[1])
    numbering["sequence"] = 0
    assert "case_numbering_requires_positive_sequence_and_venue" in evaluate_court_control(SLUG_BY_NUMBER[1], numbering)["domain_findings"]

    filing = sample_payload_for(SLUG_BY_NUMBER[3])
    filing["intake_state"] = "quietly_accepted"
    assert "filing_intake_state_invalid" in evaluate_court_control(SLUG_BY_NUMBER[3], filing)["domain_findings"]

    docket = sample_payload_for(SLUG_BY_NUMBER[5])
    docket["sequence_number"] = -1
    assert "docket_entry_requires_positive_sequence" in evaluate_court_control(SLUG_BY_NUMBER[5], docket)["domain_findings"]

    order = sample_payload_for(SLUG_BY_NUMBER[7])
    order.update({"order_state": "entered", "signature_metadata": ""})
    assert "entered_order_requires_signature_metadata" in evaluate_court_control(SLUG_BY_NUMBER[7], order)["domain_findings"]

    service = sample_payload_for(SLUG_BY_NUMBER[11])
    service["proof_document"] = ""
    assert "service_completion_requires_proof_document" in evaluate_court_control(SLUG_BY_NUMBER[11], service)["domain_findings"]


def test_sealed_public_agent_boundary_retention_and_post_judgment_controls_require_governance():
    projection = sample_payload_for(SLUG_BY_NUMBER[15])
    projection["seal_filter"] = False
    assert "public_docket_projection_requires_seal_filter" in evaluate_court_control(SLUG_BY_NUMBER[15], projection)["domain_findings"]

    triage = sample_payload_for(SLUG_BY_NUMBER[25])
    triage["confirmation_state"] = "auto_commit"
    triage_review = evaluate_court_control(SLUG_BY_NUMBER[25], triage)
    assert "filing_triage_agent_must_not_auto_commit" in triage_review["domain_findings"]
    assert triage_review["requires_human_confirmation"] is True

    boundary = sample_payload_for(SLUG_BY_NUMBER[47])
    boundary["motion_table"] = "shared_motion_table"
    assert "owned_schema_expansion_must_stay_inside_pbc_namespace" in evaluate_court_control(SLUG_BY_NUMBER[47], boundary)["domain_findings"]

    retention = sample_payload_for(SLUG_BY_NUMBER[45])
    retention.update({"destruction_hold": "active", "retrieval_audit": "destroy_requested"})
    assert "destruction_hold_blocks_archive_destruction" in evaluate_court_control(SLUG_BY_NUMBER[45], retention)["domain_findings"]

    post = sample_payload_for(SLUG_BY_NUMBER[50])
    post["closure_readiness"] = "ready"
    assert "case_closure_blocked_by_open_post_judgment_obligations" in evaluate_court_control(SLUG_BY_NUMBER[50], post)["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_court_control_contract():
    contract = improve1_court_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS

    runtime = court_case_management_runtime_capabilities()
    smoke = court_case_management_runtime_smoke()
    release = court_case_management_build_release_evidence()
    ui = court_case_management_ui_contract()

    assert runtime["improve1_court_control"]["ok"] is True
    assert smoke["improve1_court_control"]["ok"] is True
    assert any(check["id"] == "improve1_court_control" and check["ok"] for check in smoke["checks"])
    assert release["generated_artifacts"]["improve1_court_control"]["capability_count"] == 50
    assert len(ui["court_control_panels"]) == 50
    assert ui["court_control_contract"]["ok"] is True
