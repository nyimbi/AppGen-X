"""Domain behavior tests for notifications improve1 controls."""

from ..notifications_control import (
    CONTROL_SPECS,
    NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS,
    NOTIFICATION_CONTROL_OWNED_TABLES,
    evaluate_notification_control,
    improve1_notification_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import notifications_empty_state, notifications_runtime_capabilities
from ..ui import notifications_render_workbench, notifications_ui_contract


def test_all_fifty_notification_controls_are_executable_and_owned():
    contract = improve1_notification_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == NOTIFICATION_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_notification_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in NOTIFICATION_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("Notifications")
        assert result["evidence"]["service_api"].startswith("POST /notifications/improve1/")


def test_runtime_ui_and_release_expose_notification_control_contract():
    runtime = notifications_runtime_capabilities()
    ui = notifications_ui_contract()
    permissions = tuple(dict.fromkeys(ui.get("action_permissions", {}).values()))
    workbench = notifications_render_workbench(notifications_empty_state(), tenant="smoke", principal_permissions=permissions)
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["notification_control"]["capability_count"] == 50
    assert "evaluate_notification_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["notification_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["notification_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["notification_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_notification_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_template_consent_delivery_provider_and_campaign_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 15, 16, 17, 18, 19, 23, 24, 26, 27):
        _blocked(feature_number)


def test_security_analytics_agent_resilience_and_release_controls_are_gated():
    for feature_number in (28, 29, 30, 32, 33, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_notification_control(15, {"delivery_risk_evidence_complete": False})["ok"] is False
    assert evaluate_notification_control(45, {"agent_preview_only": False})["ok"] is False
    assert evaluate_notification_control(19, {"human_confirmation": False})["ok"] is False
    assert evaluate_notification_control(14, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_notification_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_notification_control(43, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_notification_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_notification_control(44, {"shared_table_access": True})
    direct_dependency = evaluate_notification_control(7, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(17)
    result = evaluate_notification_control(17, payload)
    assert result["ok"] is True
    assert payload["attempt_state"].startswith("delivery_attempt_state_machine")
    assert payload["delivery_attempt_state_machine_verified"] is True
    assert result["side_effects"] == ()
