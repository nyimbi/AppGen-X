"""Domain behavior tests for loyalty rewards improve1 controls."""

from ..loyalty_control import (
    CONTROL_SPECS,
    LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LOYALTY_CONTROL_OWNED_TABLES,
    evaluate_loyalty_control,
    improve1_loyalty_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import loyalty_rewards_runtime_capabilities
from ..ui import loyalty_rewards_render_workbench, loyalty_rewards_ui_contract


def test_all_fifty_loyalty_controls_are_executable_and_owned():
    contract = improve1_loyalty_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LOYALTY_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_loyalty_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LOYALTY_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LoyaltyRewards")
        assert result["evidence"]["service_api"].startswith("POST /loyalty-rewards/improve1/")


def test_runtime_ui_and_release_expose_loyalty_control_contract():
    runtime = loyalty_rewards_runtime_capabilities()
    ui = loyalty_rewards_ui_contract()
    workbench = loyalty_rewards_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["loyalty_control"]["capability_count"] == 50
    assert "evaluate_loyalty_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["loyalty_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["loyalty_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["loyalty_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_loyalty_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_enrollment_ledger_tier_redemption_and_expiration_negative_paths():
    for feature_number in (1, 4, 9, 12, 15, 18):
        _blocked(feature_number)


def test_partner_referral_offer_fraud_reconciliation_and_proof_controls_are_gated():
    for feature_number in (20, 22, 24, 27, 29, 30):
        _blocked(feature_number)


def test_policy_consent_agent_event_ui_resilience_and_release_controls_are_enforced():
    for feature_number in (31, 33, 43, 44, 45, 46, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_loyalty_control(43, {"human_confirmation": False})["ok"] is False
    assert evaluate_loyalty_control(44, {"human_confirmation": False})["ok"] is False


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_loyalty_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_loyalty_control(47, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_loyalty_control(47, {"stream_engine_picker_visible": True})
    shared_table = evaluate_loyalty_control(46, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(30)
    result = evaluate_loyalty_control(30, payload)
    assert result["ok"] is True
    assert payload["cryptographic_balance_proof_verified"] is True
    assert result["side_effects"] == ()
