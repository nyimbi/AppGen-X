"""Domain behavior checks for telecom subscription lifecycle improve1 controls."""

from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import telecom_subscription_lifecycle_runtime_capabilities
from ..telecom_subscription_lifecycle_control import (
    CONTROL_SPECS,
    SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS,
    SUBSCRIPTION_DECLARED_DEPENDENCIES,
    SUBSCRIPTION_OWNED_TABLES,
    SUBSCRIPTION_REQUIRED_EVENT_TOPIC,
    evaluate_telecom_subscription_lifecycle_control,
    improve1_telecom_subscription_lifecycle_control_contract,
    sample_payload_for,
)
from ..ui import telecom_subscription_lifecycle_render_workbench, telecom_subscription_lifecycle_ui_contract


def test_all_50_subscription_controls_are_executable_and_owned():
    contract = improve1_telecom_subscription_lifecycle_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == SUBSCRIPTION_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]
        assert item["side_effects"] == ()
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["evidence"]["service_api"].startswith("POST /telecom-subscription-lifecycle/improve1/")
        assert item["evidence"]["ui_surface"].startswith("TelecomSubscriptionLifecycle")
        assert item["evidence"]["event_contract"] == "AppGen-X"
        assert item["evidence"]["allowed_database_backends"] == SUBSCRIPTION_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]:
            assert table in SUBSCRIPTION_OWNED_TABLES
            assert table.startswith("telecom_subscription_lifecycle_")
        for dependency in item["evidence"]["declared_dependencies"]:
            assert dependency in SUBSCRIPTION_DECLARED_DEPENDENCIES


def test_runtime_ui_and_release_surfaces_expose_subscription_control_contract():
    runtime = telecom_subscription_lifecycle_runtime_capabilities()
    ui = telecom_subscription_lifecycle_ui_contract()
    workbench = telecom_subscription_lifecycle_render_workbench()
    release = build_release_evidence()
    validation = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["telecom_subscription_lifecycle_control"]["capability_count"] == 50
    assert "evaluate_telecom_subscription_lifecycle_control" in runtime["operations"]
    assert ui["ok"] is True
    assert ui["stream_engine_picker_visible"] is False
    assert len(ui["telecom_subscription_lifecycle_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["telecom_subscription_lifecycle_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["telecom_subscription_lifecycle_control"]["ok"] is True
    assert validation["ok"] is True
    assert validation["telecom_subscription_lifecycle_control"]["ok"] is True


def test_subscription_domains_fail_closed_without_evidence():
    for feature in (1, 2, 3, 4, 5, 6, 7, 13, 15, 33, 43, 44, 46, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"subscription_identity_evidence_complete": False})
        assert result["ok"] is False
        assert any("subscription identity evidence" in finding for finding in result["findings"])
    for feature in (8, 9, 10, 11, 12, 13, 14, 15, 27, 28, 29, 34, 35, 40, 49, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"plan_activation_evidence_complete": False})
        assert result["ok"] is False
        assert any("plan and activation evidence" in finding for finding in result["findings"])
    for feature in (16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 30, 48, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"port_usage_roaming_evidence_complete": False})
        assert result["ok"] is False
        assert any("portability, usage, roaming" in finding for finding in result["findings"])
    for feature in (31, 32, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"churn_governance_evidence_complete": False})
        assert result["ok"] is False
        assert any("churn, retention" in finding for finding in result["findings"])


def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (7, 10, 13, 15, 16, 18, 19, 25, 29, 32, 33, 36, 42, 45, 47, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"human_confirmation": False})
        assert result["ok"] is False
        assert any("human confirmation" in finding for finding in result["findings"])
    for feature in (7, 15, 18, 25, 32, 33, 36, 42, 45, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"approver_separate_from_initiator": False})
        assert result["ok"] is False
        assert any("separated approval" in finding for finding in result["findings"])
    for feature in (7, 29, 30, 31, 32, 36, 45, 47, 50):
        result = evaluate_telecom_subscription_lifecycle_control(feature, {"agent_preview_only": False})
        assert result["ok"] is False
        assert any("reversible CRUD previews" in finding for finding in result["findings"])


def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_telecom_subscription_lifecycle_control(1, {"database_backend": "sqlite"})["ok"] is False
    assert evaluate_telecom_subscription_lifecycle_control(50, {"event_topic": "custom.stream"})["ok"] is False
    assert evaluate_telecom_subscription_lifecycle_control(50, {"stream_engine_picker_visible": True})["ok"] is False
    assert evaluate_telecom_subscription_lifecycle_control(30, {"shared_table_access": True})["ok"] is False
    assert evaluate_telecom_subscription_lifecycle_control(27, {"dependency_access_mode": "shared_table"})["ok"] is False


def test_sample_payloads_are_domain_specific_and_side_effect_free():
    aggregate = sample_payload_for(1)
    assert aggregate["subscription_aggregate_id"].startswith("canonical_customer_subscription")
    assert aggregate["canonical_customer_subscription_aggregate_verified"] is True
    assert aggregate["side_effects"] == ()
    port = evaluate_telecom_subscription_lifecycle_control("number_portability_case_model")
    assert port["ok"] is True
    assert "donor_network" in port["evidence"]["required_fields"]
    assert "cutover_window" in port["evidence"]["required_fields"]
    release_gate = CONTROL_SPECS[50]
    assert release_gate["route"].endswith("/production_readiness_scorecard_and_go_live_evidence")
    assert "runbook_reference" in release_gate["fields"]
