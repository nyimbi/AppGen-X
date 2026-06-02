"""Laboratory information management behavior checks for the improve1 executable control surface."""

from ..lab_control import (
    EVENT_CONTRACT,
    LAB_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LAB_CONTROL_OWNED_TABLES,
    LAB_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_lab_control,
    improve1_lab_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import laboratory_information_management_build_release_evidence, laboratory_information_management_runtime_capabilities
from ..ui import laboratory_information_management_render_workbench, laboratory_information_management_ui_contract


def test_all_improve1_features_have_executable_lab_control_evidence():
    contract = improve1_lab_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == LAB_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == LAB_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in LAB_CONTROL_OWNED_TABLES
            assert table.startswith("laboratory_information_management_")


def test_runtime_release_and_ui_expose_lab_control_contract():
    runtime = laboratory_information_management_runtime_capabilities()
    runtime_release = laboratory_information_management_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = laboratory_information_management_ui_contract()
    workbench = laboratory_information_management_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_lab_control_contract" in runtime["operations"]
    assert runtime["lab_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["lab_control"]["ok"] is True
    assert release["ok"] is True and release["lab_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["lab_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["lab_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["lab_control_service_actions"]) == 50


def test_accessioning_and_custody_block_duplicate_or_gap_risks():
    accession = evaluate_lab_control(1, {"duplicate_accession_blocked": False})
    custody = evaluate_lab_control(2, {"custody_gap_blocked": False})
    assert accession["ok"] is False and "Sample Identity" in accession["findings"][0]
    assert custody["ok"] is False and "Chain of Custody" in custody["findings"][0]


def test_order_matching_qc_and_result_review_block_invalid_release():
    matching = evaluate_lab_control(5, {"mismatch_blocked": False})
    qc = evaluate_lab_control(9, {"release_blocked_on_fail": False})
    review = evaluate_lab_control(12, {"release_blocked_until_reviewed": False})
    assert matching["ok"] is False and "Order-to-Sample" in matching["findings"][0]
    assert qc["ok"] is False and "Quality Control" in qc["findings"][0]
    assert review["ok"] is False and "Result Validation" in review["findings"][0]


def test_critical_notification_and_agent_safeguards_are_required():
    critical = evaluate_lab_control(13, {"release_requires_notification_evidence": False})
    agent = evaluate_lab_control(28, {"human_confirmation": False, "direct_mutation_blocked": False})
    crud = evaluate_lab_control(29, {"human_confirmation": False, "direct_mutation_blocked": False})
    assert critical["ok"] is False and "Critical Result" in critical["findings"][0]
    assert agent["ok"] is False and "Agent" in agent["findings"][0]
    assert crud["ok"] is False and "Governed Agent" in crud["findings"][0]


def test_instrument_events_and_reporting_boundary_use_appgen_contracts():
    instrument = evaluate_lab_control(30, {"appgen_contract": "external", "event_topic": "foreign.topic"})
    reporting = evaluate_lab_control(31, {"no_external_mutation": False})
    assert instrument["ok"] is False and "Instrument Integration" in instrument["findings"][0]
    assert reporting["ok"] is False and "Result Reporting" in reporting["findings"][0]


def test_result_proofs_overlap_guardrails_and_composition_are_required():
    proof = evaluate_lab_control(42, {"proof_verified": False})
    overlap = evaluate_lab_control(49, {"shared_table_blocked": False})
    composition = evaluate_lab_control(50, {"dsl_fragment": False, "agent_skills": False})
    assert proof["ok"] is False and "Cryptographic" in proof["findings"][0]
    assert overlap["ok"] is False and "Package Overlap" in overlap["findings"][0]
    assert composition["ok"] is False and "Composition DSL" in composition["findings"][0]
