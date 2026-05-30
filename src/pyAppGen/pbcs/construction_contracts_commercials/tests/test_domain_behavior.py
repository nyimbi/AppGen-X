from pyAppGen.pbcs.construction_contracts_commercials.commercial_control import (
    CAPABILITY_TABLES,
    COMMERCIAL_CONTROL_CAPABILITIES,
    COMMERCIAL_CONTROL_FUNCTIONS,
    EVENT_CONTRACT,
    REQUIRED_FIELDS,
    evaluate_commercial_control,
    improve1_commercial_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.construction_contracts_commercials.runtime import (
    CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS,
    construction_contracts_commercials_build_release_evidence,
    construction_contracts_commercials_runtime_capabilities,
    construction_contracts_commercials_runtime_smoke,
    construction_contracts_commercials_ui_contract,
)


def test_all_50_commercial_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(COMMERCIAL_CONTROL_CAPABILITIES) == 50
    assert set(COMMERCIAL_CONTROL_CAPABILITIES) == set(COMMERCIAL_CONTROL_FUNCTIONS)

    for capability in COMMERCIAL_CONTROL_CAPABILITIES:
        result = COMMERCIAL_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("construction_contracts_commercials_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == "pbc.construction_contracts_commercials.events"
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == ("postgresql", "mysql", "mariadb")
        assert result["agent_skill"].startswith("construction_contracts_commercials_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_commercial_controls_reject_missing_fields_and_foreign_table_access():
    first = COMMERCIAL_CONTROL_CAPABILITIES[0]
    missing = evaluate_commercial_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("project_schedule_table",)
    rejected = evaluate_commercial_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("project_schedule_table",)


def test_contract_payment_variation_notice_and_waiver_controls_surface_review_findings():
    lifecycle = sample_payload_for("contract_commercial_lifecycle")
    lifecycle["target_stage"] = "quietly_closed"
    lifecycle_review = evaluate_commercial_control("contract_commercial_lifecycle", lifecycle)
    assert lifecycle_review["status"] == "review_required"
    assert "invalid_contract_lifecycle_stage" in lifecycle_review["domain_findings"]

    pricing = sample_payload_for("contract_type_and_pricing_basis")
    pricing["pricing_basis"] = "spreadsheet_only"
    pricing_review = evaluate_commercial_control("contract_type_and_pricing_basis", pricing)
    assert "unsupported_pricing_basis" in pricing_review["domain_findings"]

    sov = sample_payload_for("scope_and_schedule_of_values")
    sov["current_claimed"] = 120
    sov["remaining_balance"] = 100
    sov_review = evaluate_commercial_control("scope_and_schedule_of_values", sov)
    assert "schedule_of_values_overclaim" in sov_review["domain_findings"]

    pay = sample_payload_for("pay_application_intake")
    pay["certification_state"] = "under_review"
    pay["payment_event_requested"] = True
    pay_review = evaluate_commercial_control("pay_application_intake", pay)
    assert "payment_event_blocked_until_certified" in pay_review["domain_findings"]

    variation = sample_payload_for("variation_order_lifecycle")
    variation["approval_route"] = "pending"
    variation["executed_amount"] = 5000
    variation_review = evaluate_commercial_control("variation_order_lifecycle", variation)
    assert "unapproved_variation_cannot_increase_contract_value" in variation_review["domain_findings"]

    waiver = sample_payload_for("lien_waiver_governance")
    waiver["conditional_status"] = "missing"
    waiver_review = evaluate_commercial_control("lien_waiver_governance", waiver)
    assert "payment_blocked_by_invalid_lien_waiver" in waiver_review["domain_findings"]


def test_agent_document_permission_boundary_and_portal_controls_require_governance():
    agent = sample_payload_for("agent_assisted_contract_review")
    agent["human_approval"] = False
    agent_review = evaluate_commercial_control("agent_assisted_contract_review", agent)
    assert "agent_review_requires_citations_and_approval" in agent_review["domain_findings"]
    assert agent_review["requires_human_confirmation"] is True

    crud = sample_payload_for("governed_agent_crud_commands")
    crud["confirmation"] = False
    crud_review = evaluate_commercial_control("governed_agent_crud_commands", crud)
    assert "agent_crud_requires_confirmation" in crud_review["domain_findings"]

    document = sample_payload_for("commercial_document_ingestion")
    document["confidence"] = 0.41
    document_review = evaluate_commercial_control("commercial_document_ingestion", document)
    assert "low_confidence_document_extraction_requires_review" in document_review["domain_findings"]

    role = sample_payload_for("role_based_permission_model")
    role["role"] = "guest"
    role_review = evaluate_commercial_control("role_based_permission_model", role)
    assert "unauthorized_commercial_role" in role_review["domain_findings"]

    portal = sample_payload_for("contractor_portal_contract")
    portal["internal_notes_redaction"] = False
    portal_review = evaluate_commercial_control("contractor_portal_contract", portal)
    assert "portal_must_redact_internal_assessment_notes" in portal_review["domain_findings"]

    overlap = sample_payload_for("package_overlap_guardrails")
    overlap["schedule_dependency"] = "project_schedule_table"
    overlap_review = evaluate_commercial_control("package_overlap_guardrails", overlap)
    assert "overlap_guardrail_blocks_foreign_table_ownership" in overlap_review["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_commercial_control_contract():
    contract = improve1_commercial_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CONSTRUCTION_CONTRACTS_COMMERCIALS_ALLOWED_DATABASE_BACKENDS

    runtime = construction_contracts_commercials_runtime_capabilities()
    smoke = construction_contracts_commercials_runtime_smoke()
    release = construction_contracts_commercials_build_release_evidence()
    ui = construction_contracts_commercials_ui_contract()

    assert runtime["improve1_commercial_control"]["ok"] is True
    assert smoke["improve1_commercial_control"]["ok"] is True
    assert any(check["id"] == "improve1_commercial_control" and check["ok"] for check in smoke["checks"])
    assert release["generated_artifacts"]["improve1_commercial_control"]["capability_count"] == 50
    assert len(ui["commercial_control_panels"]) == 50
    assert ui["commercial_control_contract"]["ok"] is True
