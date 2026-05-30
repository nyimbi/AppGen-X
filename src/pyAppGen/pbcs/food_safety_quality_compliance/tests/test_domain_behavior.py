"""Food-safety behavior checks for the improve1 executable control surface."""

from ..food_control import (
    EVENT_CONTRACT,
    FOOD_CONTROL_ALLOWED_DATABASE_BACKENDS,
    FOOD_CONTROL_OWNED_TABLES,
    FOOD_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_food_control,
    improve1_food_control_contract,
)
from ..release_evidence import release_readiness_manifest, validate_release_evidence
from ..runtime import food_safety_quality_compliance_build_release_evidence, food_safety_quality_compliance_runtime_capabilities
from ..ui import food_safety_quality_compliance_render_workbench, food_safety_quality_compliance_ui_contract


def test_all_improve1_features_have_executable_food_control_evidence():
    contract = improve1_food_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == FOOD_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == FOOD_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in FOOD_CONTROL_OWNED_TABLES
            assert table.startswith("food_safety_quality_compliance_")


def test_runtime_release_and_ui_expose_food_control_contract():
    runtime = food_safety_quality_compliance_runtime_capabilities()
    release = food_safety_quality_compliance_build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = food_safety_quality_compliance_ui_contract()
    workbench = food_safety_quality_compliance_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_food_control_contract" in runtime["operations"]
    assert runtime["food_control"]["capability_count"] == 50
    assert release["ok"] is True and release["food_control"]["ok"] is True
    assert manifest["ok"] is True and "overlap_guardrails" in manifest["sections"]
    assert validation["ok"] is True and validation["food_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["food_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["food_control_service_actions"]) == 50


def test_haccp_version_governance_requires_historical_pin():
    result = evaluate_food_control(1, {"historical_reference_pinned": False})
    assert result["ok"] is False
    assert "HACCP version governance" in result["findings"][0]


def test_ccp_definition_requires_mapped_hazard_and_process_step():
    result = evaluate_food_control(2, {"mapping_complete": False, "linked_ccp": ""})
    assert result["ok"] is False
    assert "mapped process step" in result["findings"][0]


def test_monitoring_record_validates_unit_result_and_review():
    result = evaluate_food_control(4, {"unit": "unknown", "pass_fail": "fail", "review_state": "draft"})
    assert result["ok"] is False
    assert "monitoring record" in result["findings"][0]


def test_lot_genealogy_uses_declared_projection_boundary():
    result = evaluate_food_control(7, {"direct_inventory_read_blocked": False})
    assert result["ok"] is False
    assert "declared projections" in result["findings"][0]


def test_agent_crud_commands_are_preview_confirmed_and_owned():
    result = evaluate_food_control(30, {"preview": False, "confirmation": False, "owned_table_target": False, "mutation_allowed": True})
    assert result["ok"] is False
    assert "governed agent CRUD" in result["findings"][0]


def test_cryptographic_evidence_detects_tamper_and_reordering():
    result = evaluate_food_control(39, {"proof_verified": False, "tamper_detected": True, "ordering_valid": False})
    assert result["ok"] is False
    assert "cryptographic food safety evidence" in result["findings"][0]


def test_release_gate_blocks_missing_safety_checks():
    result = evaluate_food_control(42, {"ccp_check": False})
    assert result["ok"] is False
    assert "product release gate" in result["findings"][0]


def test_overlap_guardrails_block_external_table_references():
    result = evaluate_food_control(49, {"external_table_reference_blocked": False, "declared_dependency_used": False, "boundary_valid": False})
    assert result["ok"] is False
    assert "Package overlap guardrails".lower().split()[0] in result["findings"][0].lower()
