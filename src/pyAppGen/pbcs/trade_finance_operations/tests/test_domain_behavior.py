"""Domain behavior checks for trade finance operations improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import trade_finance_operations_runtime_capabilities
from ..trade_finance_operations_control import (
    CONTROL_SPECS,
    TRADE_ALLOWED_DATABASE_BACKENDS,
    TRADE_CONTROL_OWNED_TABLES,
    TRADE_DECLARED_DEPENDENCIES,
    TRADE_REQUIRED_EVENT_TOPIC,
    evaluate_trade_finance_operations_control,
    improve1_trade_finance_operations_control_contract,
    sample_payload_for,
)
from ..ui import trade_finance_operations_render_workbench, trade_finance_operations_ui_contract


def test_all_50_trade_finance_controls_are_executable_and_owned():
    contract = improve1_trade_finance_operations_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TRADE_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /trade-finance-operations/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TradeFinanceOperations")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TRADE_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TRADE_CONTROL_OWNED_TABLES
            assert table.startswith("trade_finance_operations_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TRADE_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_trade_control_contract():
    runtime = trade_finance_operations_runtime_capabilities()
    ui = trade_finance_operations_ui_contract()
    workbench = trade_finance_operations_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["trade_finance_operations_control"]["capability_count"] == 50
    assert "evaluate_trade_finance_operations_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["trade_finance_operations_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["trade_finance_operations_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["trade_finance_operations_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["trade_finance_operations_control"]["ok"] is True


def test_trade_finance_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 48, 50):
        result = evaluate_trade_finance_operations_control(feature, {"instrument_evidence_complete": False})
        assert result["ok"] is False
        assert any("instrument evidence" in finding for finding in result["findings"])
    for feature in (6, 7, 8, 9, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 40, 45, 50):
        result = evaluate_trade_finance_operations_control(feature, {"document_compliance_evidence_complete": False})
        assert result["ok"] is False
        assert any("document and compliance evidence" in finding for finding in result["findings"])
    for feature in (3, 10, 17, 18, 28, 29, 30, 34, 35, 46, 47, 49, 50):
        result = evaluate_trade_finance_operations_control(feature, {"settlement_exposure_evidence_complete": False})
        assert result["ok"] is False
        assert any("settlement and exposure evidence" in finding for finding in result["findings"])
    for feature in (36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 50):
        result = evaluate_trade_finance_operations_control(feature, {"operations_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("operations and agent evidence" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (4, 9, 10, 12, 13, 14, 19, 20, 28, 35, 41, 42, 43, 46, 50):
        result = evaluate_trade_finance_operations_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (4, 9, 10, 12, 13, 14, 19, 20, 28, 35, 46, 50):
        result = evaluate_trade_finance_operations_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (41, 42, 43, 46, 49, 50):
        result = evaluate_trade_finance_operations_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reviewable CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_trade_finance_operations_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_trade_finance_operations_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_trade_finance_operations_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_trade_finance_operations_control(38, {"shared_table_access": True})["ok"] is False
    assert evaluate_trade_finance_operations_control(19, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    taxonomy = sample_payload_for(1)
    assert taxonomy["lc_taxonomy_id"].startswith("canonical_letter_of_credit_taxonomy")
    assert taxonomy["canonical_letter_of_credit_taxonomy_verified"] is True
    assert taxonomy["side_effects"] == ()
    examination = evaluate_trade_finance_operations_control("document_examination_workbench")
    assert examination["ok"] is True
    assert "examiner_finding" in examination["evidence"]["required_fields"]
    assert "examiner_narrative" in examination["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/go_live_control_gates_and_release_readiness")
    assert "runbook_signoff" in release_gate["fields"]
