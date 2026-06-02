"""Domain behavior tests for privacy consent improve1 controls."""

from ..privacy_control import (
    CONTROL_SPECS,
    PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    PRIVACY_CONTROL_OWNED_TABLES,
    evaluate_privacy_control,
    improve1_privacy_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
    privacy_consent_governance_configure_runtime,
    privacy_consent_governance_empty_state,
    privacy_consent_governance_runtime_capabilities,
)
from ..ui import privacy_consent_governance_render_workbench, privacy_consent_governance_ui_contract


def _configured_state():
    return privacy_consent_governance_configure_runtime(
        privacy_consent_governance_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PRIVACY_CONSENT_GOVERNANCE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_policy_family": "global-privacy",
            "workbench_limit": 50,
            "default_jurisdiction": "GDPR",
            "supported_jurisdictions": ("GDPR", "CCPA", "LGPD"),
            "default_locale": "en",
            "dsr_sla_days": 30,
            "consent_reconfirmation_days": 365,
            "retention_review_days": 90,
            "cross_border_risk_threshold": 0.7,
        },
    )["state"]


def test_all_fifty_privacy_controls_are_executable_and_owned():
    contract = improve1_privacy_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == PRIVACY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_privacy_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in PRIVACY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("PrivacyConsentGovernance")
        assert result["evidence"]["service_api"].startswith("POST /privacy-consent-governance/improve1/")


def test_runtime_ui_and_release_expose_privacy_control_contract():
    runtime = privacy_consent_governance_runtime_capabilities()
    ui = privacy_consent_governance_ui_contract()
    workbench = privacy_consent_governance_render_workbench(
        _configured_state(),
        tenant="tenant_demo",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["privacy_control"]["capability_count"] == 50
    assert "evaluate_privacy_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["privacy_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["privacy_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["privacy_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_privacy_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_identity_consent_notice_dsr_and_retention_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 23, 24, 25):
        _blocked(feature_number)


def test_policy_incident_event_boundary_agent_and_release_controls_are_gated():
    for feature_number in (26, 28, 29, 30, 31, 32, 33, 36, 37, 38, 40, 41, 42, 43, 44, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_privacy_control(13, {"privacy_risk_evidence_complete": False})["ok"] is False
    assert evaluate_privacy_control(43, {"agent_preview_only": False})["ok"] is False
    assert evaluate_privacy_control(24, {"human_confirmation": False})["ok"] is False
    assert evaluate_privacy_control(25, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_privacy_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_privacy_control(41, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_privacy_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_privacy_control(42, {"shared_table_access": True})
    direct_dependency = evaluate_privacy_control(22, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(10)
    result = evaluate_privacy_control(10, payload)
    assert result["ok"] is True
    assert payload["dsr_intake_gate_id"].startswith("data_subject_request_intake_gate")
    assert payload["data_subject_request_intake_gate_verified"] is True
    assert result["side_effects"] == ()
