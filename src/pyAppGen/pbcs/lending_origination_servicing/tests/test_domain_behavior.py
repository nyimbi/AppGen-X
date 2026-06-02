"""Domain behavior tests for lending origination and servicing improve1 controls."""

from ..lending_control import (
    LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS,
    LENDING_CONTROL_OWNED_TABLES,
    evaluate_lending_control,
    improve1_lending_control_contract,
    sample_payload_for,
)
from ..release_evidence import validate_release_evidence
from ..runtime import lending_origination_servicing_runtime_capabilities
from ..ui import lending_origination_servicing_render_workbench, lending_origination_servicing_ui_contract


def test_all_fifty_lending_controls_are_executable_and_owned():
    contract = improve1_lending_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["allowed_database_backends"] == LENDING_CONTROL_ALLOWED_DATABASE_BACKENDS
    for feature_number in range(1, 51):
        result = evaluate_lending_control(feature_number)
        assert result["ok"] is True
        assert result["side_effects"] == ()
        assert all(table in LENDING_CONTROL_OWNED_TABLES for table in result["evidence"]["owned_tables"])
        assert result["evidence"]["ui_surface"].startswith("LendingOriginationServicing")
        assert result["evidence"]["service_api"].startswith("POST /lending-origination-servicing/improve1/")


def test_runtime_ui_and_release_expose_lending_control_contract():
    runtime = lending_origination_servicing_runtime_capabilities()
    ui = lending_origination_servicing_ui_contract()
    workbench = lending_origination_servicing_render_workbench()
    release = validate_release_evidence()
    assert runtime["ok"] is True
    assert runtime["lending_control"]["capability_count"] == 50
    assert "evaluate_lending_control" in runtime["operations"]
    assert ui["ok"] is True
    assert len(ui["lending_control_panels"]) == 50
    assert workbench["ok"] is True
    assert len(workbench["lending_control_agent_tools"]) == 50
    assert release["ok"] is True
    assert release["lending_control"]["ok"] is True


def test_origination_underwriting_closing_and_boarding_have_negative_paths():
    cases = (
        (1, "normalized_party_roles_approved"),
        (4, "identity_fraud_kyc_gate_passed"),
        (7, "affordability_ratios_policy_versioned"),
        (8, "underwriting_policy_lineage_immutable"),
        (11, "approval_to_fund_blockers_cleared"),
        (12, "boarding_terms_reconciled"),
    )
    for feature, key in cases:
        result = evaluate_lending_control(feature, {key: False})
        assert result["ok"] is False
        assert result["findings"]


def test_servicing_collections_payoff_and_special_status_controls_are_gated():
    payment = evaluate_lending_control(18, {"payment_allocation_waterfall_applied": False})
    collections = evaluate_lending_control(20, {"delinquency_bucket_strategy_selected": False})
    modification = evaluate_lending_control(24, {"modification_accounting_approved": False})
    payoff = evaluate_lending_control(25, {"payoff_quote_per_diem_reproducible": False})
    special = evaluate_lending_control(28, {"special_status_contact_blocks_enforced": False})
    complaint = evaluate_lending_control(30, {"complaint_regulatory_clock_active": False})
    assert not payment["ok"] and not collections["ok"] and not modification["ok"]
    assert not payoff["ok"] and not special["ok"] and not complaint["ok"]


def test_compliance_agent_release_and_dashboard_controls_are_enforced():
    notice = evaluate_lending_control(31, {"notice_obligation_template_versioned": False})
    fair_lending = evaluate_lending_control(32, {"fair_lending_disparity_reviewed": False})
    agent = evaluate_lending_control(43, {"agent_intake_confirmation_required": False})
    underwriter = evaluate_lending_control(44, {"human_confirmation": False})
    audit = evaluate_lending_control(46, {"audit_agent_cites_existing_evidence": False})
    release = evaluate_lending_control(47, {"release_traceability_pack_complete": False})
    controls = evaluate_lending_control(48, {"sealed_control_test_verified": False})
    dashboard = evaluate_lending_control(49, {"synthetic_portfolio_dashboard_covered": False})
    assert not notice["ok"] and not fair_lending["ok"] and not agent["ok"] and not underwriter["ok"]
    assert not audit["ok"] and not release["ok"] and not controls["ok"] and not dashboard["ok"]


def test_database_eventing_and_owned_boundary_constraints_are_enforced():
    bad_backend = evaluate_lending_control(1, {"database_backend": "sqlite"})
    bad_event = evaluate_lending_control(48, {"event_contract": "ExternalBus"})
    stream_picker = evaluate_lending_control(38, {"stream_engine_picker_visible": True})
    shared_table = evaluate_lending_control(36, {"shared_table_access": True})
    assert bad_backend["ok"] is False
    assert bad_event["ok"] is False
    assert stream_picker["ok"] is False
    assert shared_table["ok"] is False


def test_sample_payloads_remain_side_effect_free_and_specific():
    payload = sample_payload_for(25)
    result = evaluate_lending_control(25, payload)
    assert result["ok"] is True
    assert payload["payoff_quote_per_diem_reproducible"] is True
    assert result["side_effects"] == ()
