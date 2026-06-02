"""Insurance underwriting behavior checks for the improve1 executable control surface."""

from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import insurance_underwriting_build_release_evidence, insurance_underwriting_runtime_capabilities
from ..ui import insurance_underwriting_render_workbench, insurance_underwriting_ui_contract
from ..underwriting_control import (
    EVENT_CONTRACT,
    UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS,
    UNDERWRITING_CONTROL_OWNED_TABLES,
    UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_underwriting_control,
    improve1_underwriting_control_contract,
)


def test_all_improve1_features_have_executable_underwriting_control_evidence():
    contract = improve1_underwriting_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == UNDERWRITING_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == UNDERWRITING_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in UNDERWRITING_CONTROL_OWNED_TABLES
            assert table.startswith("insurance_underwriting_")


def test_runtime_release_and_ui_expose_underwriting_control_contract():
    runtime = insurance_underwriting_runtime_capabilities()
    runtime_release = insurance_underwriting_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = insurance_underwriting_ui_contract()
    workbench = insurance_underwriting_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_underwriting_control_contract" in runtime["operations"]
    assert runtime["underwriting_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["underwriting_control"]["ok"] is True
    assert release["ok"] is True and release["underwriting_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["underwriting_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["underwriting_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["underwriting_control_service_actions"]) == 50


def test_submission_completeness_blocks_incomplete_quotes():
    result = evaluate_underwriting_control(2, {"missing_fields": ("risk_address",), "completeness_score": 0.4, "quote_blocked_until_complete": False})
    assert result["ok"] is False
    assert "Submission Completeness" in result["findings"][0]


def test_authority_matrix_blocks_decisions_without_authority():
    result = evaluate_underwriting_control(7, {"decision_blocked_without_authority": False})
    assert result["ok"] is False
    assert "Underwriting Authority" in result["findings"][0]


def test_actuarial_model_boundary_cannot_mutate_training_data():
    result = evaluate_underwriting_control(9, {"training_data_not_mutated": False})
    assert result["ok"] is False
    assert "Actuarial Model" in result["findings"][0]


def test_bind_package_requires_policy_handoff_readiness():
    result = evaluate_underwriting_control(15, {"policy_handoff_ready": False, "authority_approval": False})
    assert result["ok"] is False
    assert "Bind Package" in result["findings"][0]


def test_reinsurance_and_sanction_boundaries_block_unsafe_approval():
    reinsurance = evaluate_underwriting_control(19, {"dependency_mode": "shared_table", "foreign_table_access_blocked": False})
    sanctions = evaluate_underwriting_control(22, {"approval_blocked_until_clear": False})
    assert reinsurance["ok"] is False and "Reinsurance" in reinsurance["findings"][0]
    assert sanctions["ok"] is False and "Compliance" in sanctions["findings"][0]


def test_agent_assistance_requires_confirmation_and_no_direct_mutation():
    for feature in (29, 30):
        result = evaluate_underwriting_control(feature, {"human_confirmation": False, "direct_mutation_blocked": False})
        assert result["ok"] is False
        assert "agent" in result["findings"][0].lower()


def test_policy_handoff_and_overlap_guardrails_block_shared_table_mutation():
    handoff = evaluate_underwriting_control(47, {"foreign_policy_table_not_mutated": False})
    overlap = evaluate_underwriting_control(49, {"shared_table_blocked": False})
    assert handoff["ok"] is False and "Policy Administration" in handoff["findings"][0]
    assert overlap["ok"] is False and "Package Overlap" in overlap["findings"][0]


def test_composition_dsl_and_unified_agent_exposure_are_required():
    result = evaluate_underwriting_control(50, {"dsl_fragment": False, "agent_skills": False, "side_effect_free_registration": False})
    assert result["ok"] is False
    assert "Composition DSL" in result["findings"][0]
