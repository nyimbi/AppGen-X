"""Grant and fund accounting behavior checks for the improve1 executable control surface."""

from ..grant_control import (
    EVENT_CONTRACT,
    GRANT_CONTROL_ALLOWED_DATABASE_BACKENDS,
    GRANT_CONTROL_OWNED_TABLES,
    GRANT_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_grant_control,
    improve1_grant_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import grant_fund_accounting_build_release_evidence, grant_fund_accounting_runtime_capabilities
from ..ui import grant_fund_accounting_render_workbench, grant_fund_accounting_ui_contract


def test_all_improve1_features_have_executable_grant_control_evidence():
    contract = improve1_grant_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == GRANT_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == GRANT_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in GRANT_CONTROL_OWNED_TABLES
            assert table.startswith("grant_fund_accounting_")


def test_runtime_release_and_ui_expose_grant_control_contract():
    runtime = grant_fund_accounting_runtime_capabilities()
    runtime_release = grant_fund_accounting_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = grant_fund_accounting_ui_contract()
    workbench = grant_fund_accounting_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_grant_control_contract" in runtime["operations"]
    assert runtime["grant_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["grant_control"]["ok"] is True
    assert release["ok"] is True and release["grant_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["grant_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["grant_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["grant_control_service_actions"]) == 50


def test_award_intake_requires_funder_funding_and_source_evidence():
    result = evaluate_grant_control(1, {"funder": "", "funding_amount": 0, "source_document_evidence": "", "activation_allowed": False})
    assert result["ok"] is False
    assert "grant award intake" in result["findings"][0]


def test_semantic_award_extraction_requires_citations_and_approval():
    result = evaluate_grant_control(2, {"confidence": 0.4, "clause_citations": (), "human_approval_required": False})
    assert result["ok"] is False
    assert "semantic award extraction" in result["findings"][0]


def test_restriction_aware_cost_validation_blocks_unsupported_costs():
    result = evaluate_grant_control(6, {"allowability_result": "unallowable", "remaining_budget": -1, "documentation_complete": False})
    assert result["ok"] is False
    assert "cost validation" in result["findings"][0]


def test_drawdown_readiness_requires_paid_documented_costs():
    result = evaluate_grant_control(16, {"payment_status": "unpaid", "documentation_status": "missing", "submission_allowed": False})
    assert result["ok"] is False
    assert "drawdown readiness" in result["findings"][0]


def test_match_contribution_evidence_blocks_double_counting():
    result = evaluate_grant_control(20, {"double_counted": True, "documentation": "", "audit_evidence": ""})
    assert result["ok"] is False
    assert "match contribution" in result["findings"][0]


def test_report_to_ledger_reconciliation_requires_matching_totals():
    result = evaluate_grant_control(24, {"ledger_total": 100, "report_total": 90, "submission_blocked": True})
    assert result["ok"] is False
    assert "report-to-ledger" in result["findings"][0]


def test_closeout_readiness_requires_all_final_evidence():
    result = evaluate_grant_control(34, {"final_draws_complete": False, "funder_acceptance": False, "closeout_allowed": False})
    assert result["ok"] is False
    assert "closeout readiness" in result["findings"][0]


def test_appgen_event_reliability_rejects_stream_picker_and_wrong_topic():
    result = evaluate_grant_control(41, {"event_topic": "external.kafka", "stream_engine_picker_visible": True, "safe_replay_allowed": False})
    assert result["ok"] is False
    assert "AppGen-X event reliability" in result["findings"][0]


def test_cross_pbc_boundary_blocks_foreign_table_access():
    result = evaluate_grant_control(42, {"foreign_table_access_blocked": False, "dependency_mode": "shared_table", "owned_table_scope": False})
    assert result["ok"] is False
    assert "cross-PBC boundary" in result["findings"][0]


def test_agent_assistance_requires_preview_permission_and_confirmation():
    result = evaluate_grant_control(43, {"command_preview": False, "permission_check": False, "human_confirmation": False, "direct_mutation_blocked": False})
    assert result["ok"] is False
    assert "grant agent assistance" in result["findings"][0]


def test_release_proof_requires_end_to_end_grant_story():
    result = evaluate_grant_control(50, {"events_emitted": False, "agent_summary_generated": False, "release_documents_updated": False})
    assert result["ok"] is False
    assert "end-to-end grant release proof" in result["findings"][0]
