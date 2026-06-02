
"""Domain behavior tests for energy trading improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.energy_trading_risk.runtime import (
    energy_trading_risk_build_release_evidence,
    energy_trading_risk_runtime_capabilities,
    energy_trading_risk_runtime_smoke,
)
from pyAppGen.pbcs.energy_trading_risk.trading_control import (
    TRADING_ALLOWED_DATABASE_BACKENDS,
    TRADING_DECLARED_DEPENDENCIES,
    TRADING_OWNED_TABLES,
    TRADING_REQUIRED_EVENT_TOPIC,
    evaluate_trading_control,
    improve1_trading_control_contract,
)
from pyAppGen.pbcs.energy_trading_risk.ui import energy_trading_risk_ui_contract


def test_all_improve1_controls_have_executable_domain_evidence():
    contract = improve1_trading_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == "AppGen-X"
    assert contract["required_event_topic"] == TRADING_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == TRADING_ALLOWED_DATABASE_BACKENDS
    assert contract["stream_engine_picker_visible"] is False

    for item in contract["capabilities"]:
        evidence = item["evidence"]
        assert item["ok"] is True, item
        assert evidence["owned_tables"]
        assert evidence["required_fields"]
        assert evidence["ui_surface"]
        assert evidence["service_api"]
        assert evidence["test"] == "tests/test_domain_behavior.py"
        assert evidence["event_contract"] == "AppGen-X"
        assert evidence["side_effects"] == ()
        assert set(evidence["owned_tables"]).issubset(set(TRADING_OWNED_TABLES))
        assert set(evidence["declared_dependencies"]).issubset(set(TRADING_DECLARED_DEPENDENCIES))


def test_trading_control_contract_is_visible_in_runtime_release_and_ui_surfaces():
    release = energy_trading_risk_build_release_evidence()
    runtime = energy_trading_risk_runtime_smoke()
    capabilities = energy_trading_risk_runtime_capabilities()
    ui = energy_trading_risk_ui_contract()

    assert release["ok"] is True
    assert release["generated_artifacts"]["trading_control"]["ok"] is True
    assert runtime["ok"] is True
    assert runtime["checks_by_id"]["improve1_trading_control_contract"] is True
    assert runtime["trading_control"]["capability_count"] == 50
    assert "improve1_trading_control_contract" in capabilities["operations"]
    assert len(capabilities["improve1_trading_control_capabilities"]) == 50
    assert ui["trading_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["trading_control_panels"]) == 50


def test_trade_capture_market_curve_and_settlement_guardrails_block_bad_inputs():
    missing_trade_economics = evaluate_trading_control(1, {"price_formula": ""})
    bad_curve = evaluate_trading_control(9, {"implausible_price": True})
    unexplained_settlement = evaluate_trading_control(25, {"variance_explained": False})

    assert missing_trade_economics["ok"] is False
    assert "complete economics" in missing_trade_economics["findings"][0]
    assert bad_curve["ok"] is False
    assert "market price curves" in bad_curve["findings"][0]
    assert unexplained_settlement["ok"] is False
    assert "unexplained variances" in unexplained_settlement["findings"][0]


def test_nomination_schedule_var_and_limit_controls_are_domain_specific():
    nomination_cutoff = evaluate_trading_control(5, {"post_cutoff_exception": True, "operator_reason": ""})
    schedule_mismatch = evaluate_trading_control(6, {"nominated_volume": 100.0, "scheduled_volume": 80.0, "tolerance": 1.0, "exception_opened": False})
    var_exception = evaluate_trading_control(16, {"exception_streak": 3, "model_review_required": False})
    non_dry_run = evaluate_trading_control(18, {"dry_run": False})

    assert nomination_cutoff["ok"] is False
    assert "post-cutoff" in nomination_cutoff["findings"][0]
    assert schedule_mismatch["ok"] is False
    assert "mismatch" in schedule_mismatch["findings"][0]
    assert var_exception["ok"] is False
    assert "model review" in var_exception["findings"][0]
    assert non_dry_run["ok"] is False
    assert "dry-run" in non_dry_run["findings"][0]


def test_boundary_idempotency_agent_and_override_controls_enforce_governance():
    hidden_boundary = evaluate_trading_control(33, {"foreign_table_scan": ("credit.foreign_table",)})
    unsafe_replay = evaluate_trading_control(34, {"safe_replay": False})
    assistant_commit = evaluate_trading_control(40, {"mutation_preview": False})
    expired_override = evaluate_trading_control(45, {"expired_override_active": True})
    foreign_boundary = evaluate_trading_control(47, {"foreign_table_reference": "finance.settlement"})

    assert hidden_boundary["ok"] is False
    assert "foreign table" in hidden_boundary["findings"][0]
    assert unsafe_replay["ok"] is False
    assert "idempotent API replay" in unsafe_replay["findings"][0]
    assert assistant_commit["ok"] is False
    assert "preview" in assistant_commit["findings"][0]
    assert expired_override["ok"] is False
    assert "expired overrides" in expired_override["findings"][0]
    assert foreign_boundary["ok"] is False
    assert "foreign-table" in foreign_boundary["findings"][0]


def test_release_event_resilience_and_trade_to_settlement_controls_are_gated():
    incomplete_release = evaluate_trading_control(46, {"unresolved_exception_count": 1})
    bad_schema = evaluate_trading_control(48, {"compatibility_result": "breaking"})
    missing_drill = evaluate_trading_control(49, {"recovery_evidence": ""})
    failed_lifecycle = evaluate_trading_control(50, {"settlement_step": "failed"})

    assert incomplete_release["ok"] is False
    assert "unresolved exceptions" in incomplete_release["findings"][0]
    assert bad_schema["ok"] is False
    assert "compatibility proof" in bad_schema["findings"][0]
    assert missing_drill["ok"] is False
    assert "resilience drills" in missing_drill["findings"][0]
    assert failed_lifecycle["ok"] is False
    assert "lifecycle step" in failed_lifecycle["findings"][0]
