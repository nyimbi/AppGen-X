"""Domain behavior tests for provider revenue cycle improve1 controls."""

from ..revenue_cycle_control import (
    CONTROL_SPECS,
    REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
    REVENUE_CYCLE_OWNED_TABLES,
    evaluate_revenue_cycle_control,
    improve1_revenue_cycle_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import (
    PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
    provider_revenue_cycle_configure_runtime,
    provider_revenue_cycle_empty_state,
    provider_revenue_cycle_runtime_capabilities,
)
from ..ui import provider_revenue_cycle_render_workbench, provider_revenue_cycle_ui_contract


def _configured_state():
    return provider_revenue_cycle_configure_runtime(
        provider_revenue_cycle_empty_state(),
        {
            "database_backend": "postgresql",
            "event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "workbench_limit": 100,
        },
    )["state"]


def test_all_fifty_revenue_cycle_controls_are_executable_and_owned():
    contract = improve1_revenue_cycle_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_revenue_cycle_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in REVENUE_CYCLE_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("ProviderRevenueCycle")
        assert result["evidence"]["service_api"].startswith("POST /provider-revenue-cycle/improve1/")


def test_runtime_ui_and_release_expose_revenue_cycle_control_contract():
    runtime = provider_revenue_cycle_runtime_capabilities()
    ui = provider_revenue_cycle_ui_contract()
    workbench = provider_revenue_cycle_render_workbench(
        _configured_state(),
        tenant="tenant-smoke",
        principal_permissions=tuple(dict.fromkeys(ui["action_permissions"].values())),
    )
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["revenue_cycle_control"]["capability_count"] == 50
    assert "evaluate_revenue_cycle_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["revenue_cycle_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["revenue_cycle_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["revenue_cycle_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_revenue_cycle_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_account_registration_charge_claim_denial_and_payment_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 7, 9, 10, 12, 13, 14, 15, 16, 18, 20, 21, 24, 28):
        _blocked(feature_number)


def test_agent_document_model_boundary_close_and_release_controls_are_gated():
    for feature_number in (31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_revenue_cycle_control(14, {"revenue_risk_evidence_complete": False})["ok"] is False
    assert evaluate_revenue_cycle_control(32, {"agent_preview_only": False})["ok"] is False
    assert evaluate_revenue_cycle_control(28, {"human_confirmation": False})["ok"] is False
    assert evaluate_revenue_cycle_control(25, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_revenue_cycle_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_revenue_cycle_control(36, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_revenue_cycle_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_revenue_cycle_control(37, {"shared_table_access": True})
    direct_dependency = evaluate_revenue_cycle_control(3, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(1)
    result = evaluate_revenue_cycle_control(1, payload)
    assert result["ok"] is True
    assert payload["account_readiness_id"].startswith("patient_account_revenue_readiness")
    assert payload["patient_account_revenue_readiness_verified"] is True
    assert result["side_effects"] == ()
