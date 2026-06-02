"""Domain behavior checks for vendor supplier 360 improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import vendor_supplier_360_runtime_capabilities
from ..ui import vendor_supplier_360_render_workbench, vendor_supplier_360_ui_contract
from ..vendor_supplier_360_control import (
    CONTROL_SPECS,
    VENDOR_ALLOWED_DATABASE_BACKENDS,
    VENDOR_CONTROL_OWNED_TABLES,
    VENDOR_DECLARED_DEPENDENCIES,
    VENDOR_REQUIRED_EVENT_TOPIC,
    evaluate_vendor_supplier_360_control,
    improve1_vendor_supplier_360_control_contract,
    sample_payload_for,
)


def test_all_50_supplier_controls_are_executable_and_owned():
    contract = improve1_vendor_supplier_360_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == VENDOR_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /vendor-supplier-360/improve1/")
        assert item["evidence"]["ui_surface"].startswith("VendorSupplier360")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == VENDOR_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in VENDOR_CONTROL_OWNED_TABLES
            assert table.startswith("vendor_supplier_360_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in VENDOR_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_supplier_control_contract():
    runtime = vendor_supplier_360_runtime_capabilities()
    ui = vendor_supplier_360_ui_contract()
    workbench = vendor_supplier_360_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["vendor_supplier_360_control"]["capability_count"] == 50
    assert "evaluate_vendor_supplier_360_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["vendor_supplier_360_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["vendor_supplier_360_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["vendor_supplier_360_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["vendor_supplier_360_control"]["ok"] is True


def test_supplier_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 19, 20, 29, 30, 46, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"master_onboarding_evidence_complete": False})
        assert result["ok"] is False
        assert any("supplier onboarding" in finding for finding in result["findings"])
    for feature in (4, 5, 8, 10, 13, 14, 15, 16, 17, 18, 23, 24, 34, 35, 36, 37, 38, 39, 40, 42, 43, 47, 49, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"risk_compliance_evidence_complete": False})
        assert result["ok"] is False
        assert any("supplier risk" in finding for finding in result["findings"])
    for feature in (21, 22, 23, 24, 25, 26, 27, 28, 31, 33, 35, 41, 48, 49, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"performance_relationship_evidence_complete": False})
        assert result["ok"] is False
        assert any("supplier segmentation" in finding for finding in result["findings"])
    for feature in (34, 39, 40, 41, 43, 44, 45, 46, 47, 48, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("policy impact" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (1, 2, 3, 4, 5, 7, 9, 10, 11, 16, 19, 20, 30, 32, 34, 36, 41, 42, 46, 47, 49, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (1, 2, 9, 10, 11, 16, 19, 20, 34, 36, 41, 42, 43, 46, 47, 49, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (41, 46, 47, 48, 50):
        result = evaluate_vendor_supplier_360_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_vendor_supplier_360_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_vendor_supplier_360_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_vendor_supplier_360_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_vendor_supplier_360_control(45, {"shared_table_access": True})["ok"] is False
    assert evaluate_vendor_supplier_360_control(22, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    readiness = sample_payload_for(1)
    assert readiness["readiness_gate_id"].startswith("supplier_onboarding_readiness_gate")
    assert readiness["supplier_onboarding_readiness_gate_verified"] is True
    assert readiness["side_effects"] == ()
    bank = evaluate_vendor_supplier_360_control("bank_change_fraud_controls")
    assert bank["ok"] is True
    assert "independent_contact_verification" in bank["evidence"]["required_fields"]
    assert "payment_hold_recommendation" in bank["evidence"]["required_fields"]
    boundary = CONTROL_SPECS[45]
    assert boundary["route"].endswith("/cross_pbc_boundary_proof")
    assert "no_foreign_mutation" in boundary["fields"]
