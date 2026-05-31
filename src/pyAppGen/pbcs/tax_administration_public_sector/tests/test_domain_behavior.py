"""Domain behavior checks for public-sector tax administration improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import tax_administration_public_sector_runtime_capabilities
from ..tax_administration_public_sector_control import (
    CONTROL_SPECS,
    TAX_ADMIN_ALLOWED_DATABASE_BACKENDS,
    TAX_ADMIN_DECLARED_DEPENDENCIES,
    TAX_ADMIN_OWNED_TABLES,
    TAX_ADMIN_REQUIRED_EVENT_TOPIC,
    evaluate_tax_administration_public_sector_control,
    improve1_tax_administration_public_sector_control_contract,
    sample_payload_for,
)
from ..ui import tax_administration_public_sector_render_workbench, tax_administration_public_sector_ui_contract


def test_all_50_tax_admin_controls_are_executable_and_owned():
    contract = improve1_tax_administration_public_sector_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TAX_ADMIN_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /tax-administration-public-sector/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TaxAdministrationPublicSector")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == TAX_ADMIN_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in TAX_ADMIN_OWNED_TABLES
            assert table.startswith("tax_administration_public_sector_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in TAX_ADMIN_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_tax_admin_control_contract():
    runtime = tax_administration_public_sector_runtime_capabilities()
    ui = tax_administration_public_sector_ui_contract()
    workbench = tax_administration_public_sector_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["tax_administration_public_sector_control"]["capability_count"] == 50
    assert "evaluate_tax_administration_public_sector_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["tax_administration_public_sector_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["tax_administration_public_sector_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["tax_administration_public_sector_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["tax_administration_public_sector_control"]["ok"] is True


def test_tax_admin_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 14, 40, 41, 43, 46, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"registration_filing_evidence_complete": False})
        assert result["ok"] is False
        assert any("registration and filing evidence" in finding for finding in result["findings"])
    for feature in (7, 8, 9, 10, 11, 12, 13, 27, 28, 45, 47, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"assessment_payment_evidence_complete": False})
        assert result["ok"] is False
        assert any("assessment, penalty" in finding for finding in result["findings"])
    for feature in (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 32, 33, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"audit_appeal_collection_evidence_complete": False})
        assert result["ok"] is False
        assert any("audit, workpaper" in finding for finding in result["findings"])
    for feature in (15, 16, 29, 30, 34, 35, 36, 37, 38, 39, 42, 44, 48, 49, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"governance_agent_evidence_complete": False})
        assert result["ok"] is False
        assert any("notice governance" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (1, 2, 5, 6, 8, 11, 13, 14, 15, 19, 20, 21, 23, 24, 25, 34, 35, 36, 37, 38, 45, 46, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (2, 8, 11, 13, 14, 15, 19, 21, 23, 24, 25, 34, 37, 45, 46, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (35, 36, 37, 38, 44, 45, 50):
        result = evaluate_tax_administration_public_sector_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_tax_administration_public_sector_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_tax_administration_public_sector_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_tax_administration_public_sector_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_tax_administration_public_sector_control(43, {"shared_table_access": True})["ok"] is False
    assert evaluate_tax_administration_public_sector_control(10, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    identity = sample_payload_for(1)
    assert identity["tin_lifecycle_id"].startswith("canonical_taxpayer_identity")
    assert identity["canonical_taxpayer_identity_and_tin_lifecycle_verified"] is True
    assert identity["side_effects"] == ()
    refund = evaluate_tax_administration_public_sector_control("refund_eligibility_and_fraud_screening")
    assert refund["ok"] is True
    assert "risk_score" in refund["evidence"]["required_fields"]
    assert "maker_checker_approval" in refund["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/go_live_release_gate_and_rollback_evidence")
    assert "rollback_drill" in release_gate["fields"]
