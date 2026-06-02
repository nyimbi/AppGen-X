"""Domain behavior tests for land development improve1 controls."""

from ..land_control import (
    LAND_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LAND_CONTROL_OWNED_TABLES,
    evaluate_land_control,
    improve1_land_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import land_real_estate_development_runtime_capabilities
from ..ui import land_real_estate_development_render_workbench, land_real_estate_development_ui_contract


def test_all_fifty_land_controls_are_executable_and_owned():
    contract = improve1_land_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LAND_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_land_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert result["evidence"]["owned_tables"]
        assert all(table in LAND_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LandRealEstateDevelopment")
        assert result["evidence"]["service_api"].startswith("POST /land-real-estate-development/improve1/")


def test_runtime_ui_and_release_expose_land_control_contract():
    runtime = land_real_estate_development_runtime_capabilities()
    ui = land_real_estate_development_ui_contract()
    workbench = land_real_estate_development_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["land_control"]["capability_count"] == 50
    assert "evaluate_land_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["land_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["land_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["land_control"]["ok"] is True


def test_parcel_identity_and_assemblage_block_incomplete_control():
    identity = evaluate_land_control(1, {"canonical_identity_confirmed": False})
    assemblage = evaluate_land_control(2, {"control_threshold_met": False})
    assert identity["ok"] is False
    assert any("parcel identity" in finding for finding in identity["findings"])
    assert assemblage["ok"] is False
    assert any("controlled acreage" in finding for finding in assemblage["findings"])


def test_title_environmental_and_infrastructure_risks_block_readiness():
    title = evaluate_land_control(4, {"fatal_exception_blocks_acquisition": False})
    environmental = evaluate_land_control(5, {"unresolved_environmental_issue_blocks_go": False})
    infrastructure = evaluate_land_control(17, {"will_serve_valid": False})
    assert title["ok"] is False
    assert environmental["ok"] is False
    assert infrastructure["ok"] is False
    assert any("title exceptions" in finding for finding in title["findings"])
    assert any("environmental diligence" in finding for finding in environmental["findings"])
    assert any("will-serve" in finding for finding in infrastructure["findings"])


def test_entitlement_permit_and_handoff_gates_have_negative_paths():
    dependency = evaluate_land_control(8, {"dependency_sequence_valid": False})
    permit = evaluate_land_control(20, {"completeness_score_green": False})
    comments = evaluate_land_control(21, {"unresolved_comments_block_resubmittal": False})
    handoff = evaluate_land_control(25, {"governed_handoff_packet_signed": False})
    assert dependency["ok"] is False
    assert permit["ok"] is False
    assert comments["ok"] is False
    assert handoff["ok"] is False


def test_agent_event_evidence_and_archive_controls_are_governed():
    agent_task = evaluate_land_control(44, {"human_confirmation": False})
    event_handler = evaluate_land_control(47, {"idempotent_event_handler": False})
    evidence_pack = evaluate_land_control(48, {"integrity_proof_verified": False})
    closeout = evaluate_land_control(49, {"open_obligations_block_archive": False})
    assert agent_task["ok"] is False
    assert event_handler["ok"] is False
    assert evidence_pack["ok"] is False
    assert closeout["ok"] is False
    assert any("silently assign" in finding for finding in agent_task["findings"])
    assert any("idempotent" in finding for finding in event_handler["findings"])
    assert any("integrity proofs" in finding for finding in evidence_pack["findings"])
    assert any("open obligations" in finding for finding in closeout["findings"])


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_land_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_land_control(47, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_land_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_land_control(3, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(16)
    result = evaluate_land_control(16, payload)
    assert result["ok"] is True
    assert payload["seller_price_bridge_calculated"] is True
    assert result["side_effects"] == ()
