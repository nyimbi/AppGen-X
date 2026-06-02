"""Hotel revenue management behavior checks for the improve1 executable control surface."""

from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..revenue_control import (
    EVENT_CONTRACT,
    REVENUE_CONTROL_ALLOWED_DATABASE_BACKENDS,
    REVENUE_CONTROL_OWNED_TABLES,
    REVENUE_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_revenue_control,
    improve1_revenue_control_contract,
)
from ..runtime import hotel_revenue_management_build_release_evidence, hotel_revenue_management_runtime_capabilities
from ..ui import hotel_revenue_management_render_workbench, hotel_revenue_management_ui_contract


def test_all_improve1_features_have_executable_revenue_control_evidence():
    contract = improve1_revenue_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == REVENUE_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == REVENUE_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in REVENUE_CONTROL_OWNED_TABLES
            assert table.startswith("hotel_revenue_management_")


def test_runtime_release_and_ui_expose_revenue_control_contract():
    runtime = hotel_revenue_management_runtime_capabilities()
    runtime_release = hotel_revenue_management_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = hotel_revenue_management_ui_contract()
    workbench = hotel_revenue_management_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_revenue_control_contract" in runtime["operations"]
    assert runtime["revenue_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["revenue_control"]["ok"] is True
    assert release["ok"] is True and release["revenue_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["revenue_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["revenue_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["revenue_control_service_actions"]) == 50


def test_sellable_inventory_excludes_blocked_rooms():
    result = evaluate_revenue_control(1, {"sellable_rooms": 101, "physical_rooms": 100, "pricing_excludes_blocked_rooms": False})
    assert result["ok"] is False
    assert "sellable room-type inventory" in result["findings"][0]


def test_bar_ladder_validator_blocks_invalid_public_rates():
    result = evaluate_revenue_control(3, {"bar_order_valid": False, "member_fence_valid": False, "publish_allowed": False})
    assert result["ok"] is False
    assert "BAR ladder" in result["findings"][0]


def test_channel_parity_break_requires_approved_exception():
    result = evaluate_revenue_control(6, {"parity_break": True, "approved_exception": False})
    assert result["ok"] is False
    assert "channel parity" in result["findings"][0]


def test_overbooking_respects_arrival_day_protection():
    result = evaluate_revenue_control(10, {"arrival_day_protection": False, "oversell_within_limit": False})
    assert result["ok"] is False
    assert "overbooking limits" in result["findings"][0]


def test_forecast_override_requires_approver_and_threshold_evidence():
    result = evaluate_revenue_control(24, {"required_approver": "", "variance_threshold_approved": False})
    assert result["ok"] is False
    assert "forecast override" in result["findings"][0]


def test_inventory_correction_requires_idempotent_replay_protection():
    result = evaluate_revenue_control(28, {"duplicate_replay_prevented": False, "safe_replay_allowed": False})
    assert result["ok"] is False
    assert "inventory correction" in result["findings"][0]


def test_agent_skills_block_direct_mutation():
    result = evaluate_revenue_control(34, {"command_preview": False, "human_confirmation": False, "direct_mutation_blocked": False})
    assert result["ok"] is False
    assert "hotel revenue agent" in result["findings"][0]


def test_outbound_events_use_appgen_contract_and_hide_stream_picker():
    result = evaluate_revenue_control(37, {"event_topic": "external.kafka", "stream_picker_hidden": False})
    assert result["ok"] is False
    assert "outbound revenue events" in result["findings"][0]


def test_cross_pbc_boundaries_block_foreign_table_access():
    result = evaluate_revenue_control(48, {"foreign_table_access_blocked": False, "dependency_mode": "shared_table", "owned_scope": False})
    assert result["ok"] is False
    assert "cross-PBC boundary" in result["findings"][0]


def test_go_live_scorecard_requires_release_signoff_story():
    result = evaluate_revenue_control(50, {"go_live_signoff": False, "events_emitted": False, "release_documents_updated": False})
    assert result["ok"] is False
    assert "go-live scorecard" in result["findings"][0]
