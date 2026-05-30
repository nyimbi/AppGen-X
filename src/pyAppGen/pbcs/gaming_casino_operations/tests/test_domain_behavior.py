"""Casino-domain behavior checks for the improve1 executable control surface."""

from ..casino_control import (
    CASINO_CONTROL_ALLOWED_DATABASE_BACKENDS,
    CASINO_CONTROL_OWNED_TABLES,
    CASINO_CONTROL_REQUIRED_EVENT_TOPIC,
    EVENT_CONTRACT,
    evaluate_casino_control,
    improve1_casino_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import gaming_casino_operations_build_release_evidence, gaming_casino_operations_runtime_capabilities
from ..ui import gaming_casino_operations_render_workbench, gaming_casino_operations_ui_contract


def test_all_improve1_features_have_executable_casino_control_evidence():
    contract = improve1_casino_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == CASINO_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == CASINO_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in CASINO_CONTROL_OWNED_TABLES
            assert table.startswith("gaming_casino_operations_")


def test_runtime_release_and_ui_expose_casino_control_contract():
    runtime = gaming_casino_operations_runtime_capabilities()
    runtime_release = gaming_casino_operations_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = gaming_casino_operations_ui_contract()
    workbench = gaming_casino_operations_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_casino_control_contract" in runtime["operations"]
    assert runtime["casino_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["casino_control"]["ok"] is True
    assert release["ok"] is True and release["casino_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["casino_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["casino_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["casino_control_service_actions"]) == 50


def test_patron_enrollment_requires_identity_age_and_review_evidence():
    result = evaluate_casino_control(1, {"identity_confidence": 0.2, "age_verification_status": "missing", "reviewer_evidence": ""})
    assert result["ok"] is False
    assert "patron enrollment" in result["findings"][0]


def test_restricted_patron_blocks_floor_access():
    result = evaluate_casino_control(2, {"self_excluded": True, "floor_access_allowed": False})
    assert result["ok"] is False
    assert "floor access" in result["findings"][0]


def test_table_inventory_requires_dual_control_evidence():
    result = evaluate_casino_control(4, {"supervisor_confirmation": False, "dual_control_evidence": ""})
    assert result["ok"] is False
    assert "dual-control" in result["findings"][0]


def test_slot_conversion_requires_jurisdiction_approval():
    result = evaluate_casino_control(5, {"jurisdiction_approval_state": "draft", "activation_allowed": False})
    assert result["ok"] is False
    assert "jurisdiction approval" in result["findings"][0]


def test_jackpot_cannot_close_without_meter_and_witness_evidence():
    result = evaluate_casino_control(11, {"meter_snapshot": "", "witness_evidence": "", "close_allowed": False})
    assert result["ok"] is False
    assert "jackpot" in result["findings"][0]


def test_surveillance_boundary_does_not_own_media_storage():
    result = evaluate_casino_control(22, {"media_storage_owned": True})
    assert result["ok"] is False
    assert "surveillance" in result["findings"][0]


def test_agent_mutation_guardrails_block_direct_mutation():
    result = evaluate_casino_control(38, {"command_preview": False, "permission_check": False, "mutation_allowed": True})
    assert result["ok"] is False
    assert "governed agent mutation" in result["findings"][0]


def test_external_boundary_blocks_foreign_table_ownership():
    result = evaluate_casino_control(40, {"foreign_reference_blocked": False, "finance_table_mutation_blocked": False, "loyalty_balance_owned": True})
    assert result["ok"] is False
    assert "external boundary" in result["findings"][0]


def test_release_rehearsal_requires_end_to_end_story_evidence():
    result = evaluate_casino_control(50, {"events_emitted": False, "assistant_summary_generated": False, "release_documents_updated": False})
    assert result["ok"] is False
    assert "release rehearsal" in result["findings"][0]
