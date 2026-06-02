"""Domain behavior tests for maritime shipping operations improve1 controls."""

from ..maritime_control import (
    CONTROL_SPECS,
    MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS,
    MARITIME_CONTROL_OWNED_TABLES,
    evaluate_maritime_control,
    improve1_maritime_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import maritime_shipping_operations_runtime_capabilities
from ..ui import maritime_shipping_operations_render_workbench, maritime_shipping_operations_ui_contract


def test_all_fifty_maritime_controls_are_executable_and_owned():
    contract = improve1_maritime_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == MARITIME_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_maritime_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in MARITIME_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("MaritimeShippingOperations")
        assert result["evidence"]["service_api"].startswith("POST /maritime-shipping-operations/improve1/")


def test_runtime_ui_and_release_expose_maritime_control_contract():
    runtime = maritime_shipping_operations_runtime_capabilities()
    ui = maritime_shipping_operations_ui_contract()
    workbench = maritime_shipping_operations_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["maritime_control"]["capability_count"] == 50
    assert "evaluate_maritime_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["maritime_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["maritime_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["maritime_control"]["ok"] is True


def _blocked(feature_number: int):
    key = CONTROL_SPECS[feature_number]["primary_proof"]
    result = evaluate_maritime_control(feature_number, {key: False})
    assert result["ok"] is False
    assert result["findings"]


def test_voyage_port_booking_bill_and_stowage_controls_are_gated():
    for feature_number in (1, 3, 5, 7, 8, 10):
        _blocked(feature_number)


def test_charter_laytime_demurrage_bunker_compliance_and_sanctions_are_gated():
    for feature_number in (11, 12, 13, 15, 19, 20):
        _blocked(feature_number)


def test_agent_simulation_event_ui_mobile_and_release_controls_are_gated():
    for feature_number in (23, 25, 31, 32, 33, 35, 43, 45, 47, 48, 49, 50):
        _blocked(feature_number)
    assert evaluate_maritime_control(31, {"human_confirmation": False})["ok"] is False
    assert evaluate_maritime_control(33, {"human_confirmation": False})["ok"] is False


def test_database_eventing_owned_boundary_and_projection_constraints_are_enforced():
    bad_backend = evaluate_maritime_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_maritime_control(22, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_maritime_control(22, {"stream_engine_picker_visible": True})
    shared_table = evaluate_maritime_control(38, {"shared_table_access": True})
    direct_dependency = evaluate_maritime_control(18, {"dependency_access_mode": "shared_table"})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False
    assert direct_dependency["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_domain_specific():
    payload = sample_payload_for(35)
    result = evaluate_maritime_control(35, payload)
    assert result["ok"] is True
    assert payload["counterfactual_simulation_side_effect_free"] is True
    assert result["side_effects"] == ()
