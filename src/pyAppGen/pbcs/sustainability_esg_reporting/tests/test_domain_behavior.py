"""Domain behavior checks for sustainability ESG reporting improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import sustainability_esg_reporting_runtime_capabilities
from ..sustainability_esg_reporting_control import (
    CONTROL_SPECS,
    ESG_ALLOWED_DATABASE_BACKENDS,
    ESG_DECLARED_DEPENDENCIES,
    ESG_OWNED_TABLES,
    ESG_REQUIRED_EVENT_TOPIC,
    evaluate_sustainability_esg_reporting_control,
    improve1_sustainability_esg_reporting_control_contract,
    sample_payload_for,
)
from ..ui import sustainability_esg_reporting_render_workbench, sustainability_esg_reporting_ui_contract


def test_all_50_esg_controls_are_executable_and_owned():
    contract = improve1_sustainability_esg_reporting_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == ESG_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /sustainability-esg-reporting/improve1/")
        assert item["evidence"]["ui_surface"].startswith("SustainabilityEsgReporting")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == ESG_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in ESG_OWNED_TABLES
            assert table.startswith("sustainability_esg_reporting_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in ESG_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_esg_control_contract():
    runtime = sustainability_esg_reporting_runtime_capabilities()
    ui = sustainability_esg_reporting_ui_contract()
    workbench = sustainability_esg_reporting_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()

    assert runtime["ok"] is True
    assert runtime["sustainability_esg_reporting_control"]["capability_count"] == 50
    assert "evaluate_sustainability_esg_reporting_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["sustainability_esg_reporting_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["sustainability_esg_reporting_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["sustainability_esg_reporting_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["sustainability_esg_reporting_control"]["ok"] is True


def test_esg_domains_fail_closed_without_evidence():
    for feature in (3, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 21, 32, 33, 42, 43, 48, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"carbon_accounting_evidence_complete": False})
        assert result["ok"] is False
        assert any("carbon accounting evidence" in finding for finding in result["findings"])

    for feature in (1, 16, 25, 26, 27, 28, 29, 30, 31, 38, 41, 42, 43, 49, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"disclosure_assurance_evidence_complete": False})
        assert result["ok"] is False
        assert any("disclosure and assurance evidence" in finding for finding in result["findings"])

    for feature in (18, 19, 20, 21, 22, 23, 24, 37, 39, 40, 44, 45, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"target_risk_evidence_complete": False})
        assert result["ok"] is False
        assert any("target and climate risk evidence" in finding for finding in result["findings"])

    for feature in (2, 11, 12, 34, 35, 36, 37, 38, 46, 47, 48, 49, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"supplier_social_governance_evidence_complete": False})
        assert result["ok"] is False
        assert any("supplier, social, governance" in finding for finding in result["findings"])


def test_agent_confirmation_and_approval_controls_are_gated():
    for feature in (3, 4, 5, 11, 12, 18, 20, 21, 24, 26, 27, 30, 32, 33, 38, 39, 40, 42, 46, 47, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])

    for feature in (4, 7, 18, 20, 24, 26, 27, 30, 32, 33, 38, 39, 40, 42, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])

    for feature in (5, 12, 21, 25, 26, 39, 40, 44, 45, 46, 47, 49, 50):
        result = evaluate_sustainability_esg_reporting_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("typed reversible previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_sustainability_esg_reporting_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_sustainability_esg_reporting_control(48, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_sustainability_esg_reporting_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_sustainability_esg_reporting_control(48, {"shared_table_access": True})["ok"] is False
    assert evaluate_sustainability_esg_reporting_control(7, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    ontology = sample_payload_for(1)
    assert ontology["metric_ontology_id"].startswith("esg_metric_ontology")
    assert ontology["esg_metric_ontology_and_materiality_taxonomy_verified"] is True
    assert ontology["side_effects"] == ()

    scope2 = evaluate_sustainability_esg_reporting_control("scope_2_market_based_and_location_based_accounting")
    assert scope2["ok"] is True
    assert "market_based_factor" in scope2["evidence"]["required_fields"]
    assert "retirement_check" in scope2["evidence"]["required_fields"]

    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/end_to_end_esg_release_evidence_matrix")
    assert "event_contract" in release_gate["fields"]
