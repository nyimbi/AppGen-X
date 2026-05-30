"""Domain behavior tests for music royalties improve1 controls."""

from ..release_evidence import validate_release_evidence
from ..royalties_rights_control import (
    CONTROL_SPECS,
    ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS,
    ROYALTIES_CONTROL_OWNED_TABLES,
    evaluate_royalties_rights_control,
    improve1_royalties_rights_control_contract,
    sample_payload_for,
)
from ..runtime import music_royalties_rights_runtime_capabilities
from ..ui import music_royalties_rights_render_workbench, music_royalties_rights_ui_contract


def test_all_fifty_royalties_controls_are_executable_and_owned():
    contract = improve1_royalties_rights_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == ROYALTIES_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_royalties_rights_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in ROYALTIES_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MusicRoyaltiesRights")
        assert result["evidence"]["service_api"].startswith("POST /music-royalties-rights/improve1/")


def test_runtime_ui_and_release_expose_royalties_control_contract():
    runtime = music_royalties_rights_runtime_capabilities()
    ui = music_royalties_rights_ui_contract()
    workbench = music_royalties_rights_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["royalties_rights_control"]["capability_count"] == 50
    assert "evaluate_royalties_rights_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["royalties_rights_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["royalties_rights_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["royalties_rights_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_royalties_rights_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_repertoire_identity_split_license_usage_and_statement_controls_are_gated():
    for feature_number in (1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 14, 17, 18, 20, 21):
        _blocked(feature_number)


def test_payment_tax_dispute_event_agent_and_release_controls_are_gated():
    for feature_number in (22, 23, 24, 25, 26, 27, 28, 29, 34, 35, 36, 40, 41, 42, 43, 44, 45, 49, 50):
        _blocked(feature_number)
    assert evaluate_royalties_rights_control(25, {"money_or_rights_evidence_complete": False})["ok"] is False
    assert evaluate_royalties_rights_control(40, {"agent_preview_only": False})["ok"] is False
    assert evaluate_royalties_rights_control(36, {"human_confirmation": False})["ok"] is False
    assert evaluate_royalties_rights_control(14, {"non_mutating_simulation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_royalties_rights_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_royalties_rights_control(34, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_royalties_rights_control(50, {"stream_engine_picker_visible": True})
    shared_table = evaluate_royalties_rights_control(46, {"shared_table_access": True})
    direct_dependency = evaluate_royalties_rights_control(26, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(21)
    result = evaluate_royalties_rights_control(21, payload)
    assert result["ok"] is True
    assert payload["statement_line_id"].startswith("statement_calculation_traceability")
    assert payload["statement_calculation_traceability_down_to_line_and_rule_level_verified"] is True
    assert result["side_effects"] == ()
