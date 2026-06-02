"""Domain behavior checks for enterprise_search_vector improve1 controls."""

from pyAppGen.pbcs.enterprise_search_vector.release_evidence import build_release_evidence, validate_release_evidence
from pyAppGen.pbcs.enterprise_search_vector.runtime import enterprise_search_vector_runtime_capabilities, enterprise_search_vector_runtime_smoke
from pyAppGen.pbcs.enterprise_search_vector.search_control import (
    SEARCH_ALLOWED_DATABASE_BACKENDS,
    SEARCH_DECLARED_DEPENDENCIES,
    SEARCH_OWNED_TABLES,
    SEARCH_REQUIRED_EVENT_TOPIC,
    evaluate_search_control,
    improve1_search_control_contract,
)
from pyAppGen.pbcs.enterprise_search_vector.ui import enterprise_search_vector_ui_contract


def test_all_improve1_controls_have_executable_search_evidence():
    contract = improve1_search_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == SEARCH_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == SEARCH_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for capability in contract["capabilities"]:
        evidence = capability["evidence"]
        assert capability["ok"] is True
        assert evidence["owned_tables"]
        assert all(table in SEARCH_OWNED_TABLES for table in evidence["owned_tables"])
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert all(dependency in SEARCH_DECLARED_DEPENDENCIES for dependency in evidence["declared_dependencies"])
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()


def test_search_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    runtime = enterprise_search_vector_runtime_capabilities()
    smoke = enterprise_search_vector_runtime_smoke()
    release = build_release_evidence()
    ui = enterprise_search_vector_ui_contract()
    assert runtime["ok"] is True
    assert runtime["search_control"]["ok"] is True
    assert "improve1_search_control_contract" in runtime["operations"]
    assert len(runtime["improve1_search_control_capabilities"]) == 50
    assert release["search_control"]["ok"] is True
    assert validate_release_evidence()["ok"] is True
    assert smoke["ok"] is True
    assert ui["search_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["search_control_panels"]) == 50


def test_source_projection_acl_redaction_and_model_governance_are_enforced():
    assert evaluate_search_control(2, {"declared_projection_contract": False})["ok"] is False
    assert evaluate_search_control(7, {"approval_status": "draft"})["ok"] is False
    assert evaluate_search_control(9, {"pre_rank_filtering": False})["ok"] is False
    assert evaluate_search_control(10, {"leakage_tests": "failed"})["ok"] is False
    assert evaluate_search_control(14, {"allowed_response_behavior": "freeform"})["ok"] is False


def test_ranking_freshness_retention_and_quality_gates_are_search_specific():
    assert evaluate_search_control(12, {"confidence": 0.2})["ok"] is False
    assert evaluate_search_control(17, {"regression_status": "failed"})["ok"] is False
    assert evaluate_search_control(19, {"restricted_index": True, "policy_approval": False})["ok"] is False
    assert evaluate_search_control(20, {"verification_status": "failed"})["ok"] is False
    assert evaluate_search_control(21, {"query_exclusion": False})["ok"] is False
    assert evaluate_search_control(30, {"regression_tests": "missing"})["ok"] is False


def test_agent_answer_boundary_event_and_tenant_controls_block_unsafe_search_use():
    assert evaluate_search_control(35, {"prompt_injection_score": 0.9})["ok"] is False
    assert evaluate_search_control(36, {"source_citations": ()})["ok"] is False
    assert evaluate_search_control(37, {"unsupported_answer_block": ("blocked",)})["ok"] is False
    assert evaluate_search_control(41, {"query_test": "failed"})["ok"] is False
    assert evaluate_search_control(46, {"human_confirmation": False})["ok"] is False
    assert evaluate_search_control(47, {"foreign_table_access": ("product_table",)})["ok"] is False
    assert evaluate_search_control(48, {"unknown_event_mutation": ("mutated",)})["ok"] is False


def test_release_evidence_and_complete_workbench_controls_are_gated():
    assert evaluate_search_control(49, {"retry_dead_letter_tests": "missing"})["ok"] is False
    assert evaluate_search_control(50, {"support_analyst_view": "hidden"})["ok"] is False
    assert evaluate_search_control(27, {"opt_in_policy": False})["ok"] is False
    assert evaluate_search_control(45, {"approval": "pending"})["ok"] is False
