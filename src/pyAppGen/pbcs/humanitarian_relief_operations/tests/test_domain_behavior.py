"""Humanitarian relief operations behavior checks for the improve1 executable control surface."""

from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..relief_control import (
    EVENT_CONTRACT,
    RELIEF_CONTROL_ALLOWED_DATABASE_BACKENDS,
    RELIEF_CONTROL_OWNED_TABLES,
    RELIEF_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_relief_control,
    improve1_relief_control_contract,
)
from ..runtime import humanitarian_relief_operations_build_release_evidence, humanitarian_relief_operations_runtime_capabilities
from ..ui import humanitarian_relief_operations_render_workbench, humanitarian_relief_operations_ui_contract


def test_all_improve1_features_have_executable_relief_control_evidence():
    contract = improve1_relief_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == RELIEF_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == RELIEF_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in RELIEF_CONTROL_OWNED_TABLES
            assert table.startswith("humanitarian_relief_operations_")


def test_runtime_release_and_ui_expose_relief_control_contract():
    runtime = humanitarian_relief_operations_runtime_capabilities()
    runtime_release = humanitarian_relief_operations_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = humanitarian_relief_operations_ui_contract()
    workbench = humanitarian_relief_operations_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_relief_control_contract" in runtime["operations"]
    assert runtime["relief_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["relief_control"]["ok"] is True
    assert release["ok"] is True and release["relief_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["relief_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["relief_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["relief_control_service_actions"]) == 50


def test_household_triage_requires_verified_confident_assessment():
    result = evaluate_relief_control(1, {"assessor_confidence": 0.2, "review_status": "draft", "action_ready_queue": False})
    assert result["ok"] is False
    assert "household needs triage" in result["findings"][0]


def test_beneficiary_registration_blocks_unresolved_duplicates():
    result = evaluate_relief_control(2, {"duplicate_candidates": ("hh-2",), "dedupe_rationale": "", "distribution_approval_allowed": False})
    assert result["ok"] is False
    assert "duplicate" in result["findings"][0]


def test_warehouse_lot_control_blocks_quarantined_stock():
    result = evaluate_relief_control(6, {"quarantine_status": "quarantined", "expired_or_quarantined_blocked": False})
    assert result["ok"] is False
    assert "warehouse lot" in result["findings"][0]


def test_distribution_reconciliation_blocks_unexplained_variance():
    result = evaluate_relief_control(9, {"unaccounted_qty": 12, "final_approval_allowed": False})
    assert result["ok"] is False
    assert "distribution reconciliation" in result["findings"][0]


def test_referral_workflow_masks_survivor_narrative():
    result = evaluate_relief_control(16, {"minimum_necessary_disclosure": False, "survivor_narrative_masked": False, "restricted_access_audit": False})
    assert result["ok"] is False
    assert "survivor confidentiality" in result["findings"][0]


def test_agent_guardrails_block_unsafe_mutation_and_prompts():
    result = evaluate_relief_control(25, {"direct_mutation_blocked": False, "unauthorized_prompt_denied": False})
    assert result["ok"] is False
    assert "humanitarian agent" in result["findings"][0]


def test_validation_only_api_does_not_mutate_live_records():
    result = evaluate_relief_control(26, {"validation_only_route": False, "no_live_mutation": False, "owned_boundary": False})
    assert result["ok"] is False
    assert "validation APIs" in result["findings"][0]


def test_idempotent_field_posting_prevents_duplicate_records():
    result = evaluate_relief_control(30, {"duplicate_record_prevented": False, "stable_response": False})
    assert result["ok"] is False
    assert "idempotent field posting" in result["findings"][0]


def test_cross_boundary_events_block_foreign_tables():
    result = evaluate_relief_control(42, {"dependency_mode": "shared_table", "foreign_table_access_blocked": False, "event_contract": "external"})
    assert result["ok"] is False
    assert "cross-boundary" in result["findings"][0]


def test_high_risk_assistance_requires_dual_control():
    result = evaluate_relief_control(49, {"segregation_enforced": False, "assistance_blocked_until_approved": False})
    assert result["ok"] is False
    assert "dual control" in result["findings"][0]
