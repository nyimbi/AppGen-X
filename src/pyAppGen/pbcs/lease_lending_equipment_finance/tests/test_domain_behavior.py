"""Domain behavior tests for lease lending equipment finance improve1 controls."""

from ..lease_control import (
    LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LEASE_CONTROL_OWNED_TABLES,
    evaluate_lease_control,
    improve1_lease_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import lease_lending_equipment_finance_runtime_capabilities
from ..ui import lease_lending_equipment_finance_render_workbench, lease_lending_equipment_finance_ui_contract


def test_all_fifty_lease_controls_are_executable_and_owned():
    contract = improve1_lease_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LEASE_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_lease_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LEASE_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LeaseLendingEquipmentFinance")
        assert result["evidence"]["service_api"].startswith("POST /lease-lending-equipment-finance/improve1/")


def test_runtime_ui_and_release_expose_lease_control_contract():
    runtime = lease_lending_equipment_finance_runtime_capabilities()
    ui = lease_lending_equipment_finance_ui_contract()
    workbench = lease_lending_equipment_finance_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["lease_control"]["capability_count"] == 50
    assert "evaluate_lease_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["lease_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["lease_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["lease_control"]["ok"] is True


def test_origination_collateral_pricing_and_schedule_gates_have_negative_paths():
    product = evaluate_lease_control(1, {"product_structure_validated": False})
    funding = evaluate_lease_control(5, {"funding_reconciliation_passed": False})
    pricing = evaluate_lease_control(7, {"pricing_reconciles_to_cashflows": False})
    schedule = evaluate_lease_control(10, {"schedule_generation_validated": False})
    assert product["ok"] is False
    assert funding["ok"] is False
    assert pricing["ok"] is False
    assert schedule["ok"] is False


def test_servicing_residual_buyout_repo_and_investor_controls_are_gated():
    residual = evaluate_lease_control(14, {"residual_review_current": False})
    buyout = evaluate_lease_control(16, {"buyout_quote_reproducible": False})
    repo = evaluate_lease_control(23, {"repo_timeline_auditable": False})
    remittance = evaluate_lease_control(26, {"remittance_waterfall_reconciled": False})
    assert residual["ok"] is False
    assert buyout["ok"] is False
    assert repo["ok"] is False
    assert remittance["ok"] is False


def test_agent_api_release_and_authority_controls_are_enforced():
    document = evaluate_lease_control(30, {"document_extraction_cited": False})
    agent = evaluate_lease_control(47, {"agent_authority_boundary_enforced": False})
    controls = evaluate_lease_control(48, {"continuous_controls_publish_exceptions": False})
    acceptance = evaluate_lease_control(50, {"final_acceptance_rubric_signed": False})
    assert document["ok"] is False
    assert agent["ok"] is False
    assert controls["ok"] is False
    assert acceptance["ok"] is False
    assert any("authority" in finding for finding in agent["findings"])


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_lease_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_lease_control(38, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_lease_control(39, {"stream_engine_picker_visible": True})
    shared_table = evaluate_lease_control(40, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(16)
    result = evaluate_lease_control(16, payload)
    assert result["ok"] is True
    assert payload["buyout_quote_reproducible"] is True
    assert result["side_effects"] == ()
