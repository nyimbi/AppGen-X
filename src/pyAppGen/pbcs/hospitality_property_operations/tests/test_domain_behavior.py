"""Hospitality property operations behavior checks for the improve1 executable control surface."""

from ..hospitality_control import (
    EVENT_CONTRACT,
    HOSPITALITY_CONTROL_ALLOWED_DATABASE_BACKENDS,
    HOSPITALITY_CONTROL_OWNED_TABLES,
    HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC,
    evaluate_hospitality_control,
    improve1_hospitality_control_contract,
)
from ..release_evidence import build_release_evidence, release_readiness_manifest, validate_release_evidence
from ..runtime import hospitality_property_operations_build_release_evidence, hospitality_property_operations_runtime_capabilities
from ..ui import hospitality_property_operations_render_workbench, hospitality_property_operations_ui_contract


def test_all_improve1_features_have_executable_hotel_control_evidence():
    contract = improve1_hospitality_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["event_contract"] == EVENT_CONTRACT == "AppGen-X"
    assert contract["required_event_topic"] == HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC
    assert contract["allowed_database_backends"] == HOSPITALITY_CONTROL_ALLOWED_DATABASE_BACKENDS == ("postgresql", "mysql", "mariadb")
    assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True
        assert item["evidence"]["test"] == "tests/test_domain_behavior.py"
        assert item["missing_fields"] == ()
        assert item["foreign_tables"] == ()
        assert item["undeclared_dependencies"] == ()
        for table in item["evidence"]["owned_tables"]:
            assert table in HOSPITALITY_CONTROL_OWNED_TABLES
            assert table.startswith("hospitality_property_operations_")


def test_runtime_release_and_ui_expose_hotel_control_contract():
    runtime = hospitality_property_operations_runtime_capabilities()
    runtime_release = hospitality_property_operations_build_release_evidence()
    release = build_release_evidence()
    manifest = release_readiness_manifest()
    validation = validate_release_evidence()
    ui = hospitality_property_operations_ui_contract()
    workbench = hospitality_property_operations_render_workbench()
    assert runtime["ok"] is True
    assert "improve1_hospitality_control_contract" in runtime["operations"]
    assert runtime["hospitality_control"]["capability_count"] == 50
    assert runtime_release["ok"] is True and runtime_release["hospitality_control"]["ok"] is True
    assert release["ok"] is True and release["hospitality_control"]["ok"] is True
    assert manifest["ok"] is True and "release_rehearsal" in manifest["sections"]
    assert validation["ok"] is True and validation["hospitality_control"]["ok"] is True
    assert ui["ok"] is True and len(ui["full_capability_surface"]["hospitality_control_panels"]) == 50
    assert workbench["ok"] is True and len(workbench["hospitality_control_service_actions"]) == 50


def test_sellable_room_state_blocks_dirty_or_held_rooms():
    result = evaluate_hospitality_control(1, {"housekeeping_status": "dirty", "inspection_status": "pending", "maintenance_hold_status": "safety", "sellable_state": "withheld"})
    assert result["ok"] is False
    assert "sellable room state" in result["findings"][0]


def test_reservation_requires_guarantee_evidence():
    result = evaluate_hospitality_control(3, {"guarantee_status": "tentative", "deposit_evidence": ""})
    assert result["ok"] is False
    assert "reservation lifecycle" in result["findings"][0]


def test_guest_stay_preserves_room_history_for_moves():
    result = evaluate_hospitality_control(5, {"room_history": (), "departure_readiness": False})
    assert result["ok"] is False
    assert "guest stay lifecycle" in result["findings"][0]


def test_inspection_quality_blocks_room_release():
    result = evaluate_hospitality_control(8, {"pass_fail_score": "fail", "release_allowed": False})
    assert result["ok"] is False
    assert "inspection quality" in result["findings"][0]


def test_assistant_panel_requires_citations_and_no_direct_mutation():
    result = evaluate_hospitality_control(19, {"cited_recommendation": False, "human_confirmation": False, "direct_mutation_blocked": False})
    assert result["ok"] is False
    assert "assistant panel" in result["findings"][0]


def test_boundary_safe_projection_blocks_shared_tables():
    result = evaluate_hospitality_control(24, {"dependency_mode": "shared_table", "foreign_table_access_blocked": False})
    assert result["ok"] is False
    assert "boundary-safe projections" in result["findings"][0]


def test_cross_domain_boundaries_do_not_own_external_masters():
    result = evaluate_hospitality_control(26, {"guest_master_owned": True, "supplier_master_owned": True, "payment_ledger_owned": True, "foreign_mutation_blocked": False})
    assert result["ok"] is False
    assert "declared hotel boundaries" in result["findings"][0]


def test_crypto_proof_requires_valid_ordered_digest():
    result = evaluate_hospitality_control(31, {"proof_verified": False, "altered_order_detected": True, "payload_digest_valid": False})
    assert result["ok"] is False
    assert "cryptographic" in result["findings"][0]


def test_event_contract_hides_stream_picker():
    result = evaluate_hospitality_control(46, {"event_topic": "external.kafka", "stream_picker_hidden": False})
    assert result["ok"] is False
    assert "typed emitted events" in result["findings"][0]


def test_release_proof_requires_arrival_to_room_ready_story():
    result = evaluate_hospitality_control(50, {"events_emitted": False, "assistant_summary_generated": False, "release_documents_updated": False})
    assert result["ok"] is False
    assert "arrival-to-room-ready" in result["findings"][0]
