"""Focused standalone application tests for the oil_gas_field_operations PBC."""

from pathlib import Path

from .. import release_evidence, standalone, ui


def _app():
    return standalone.OilGasFieldOperationsStandaloneApp()


def test_standalone_field_journey_runs_end_to_end():
    app = _app()
    try:
        well = app.register_well(
            {
                "tenant": "tenant-alpha",
                "well_id": "OG-7H",
                "field_name": "North Basin",
                "area_name": "Area-1",
                "pad_name": "Pad-A",
                "lease_name": "Lease-77",
                "route_code": "ROUTE-7",
                "wellbore": "7H",
                "completion": "Wolfcamp A",
                "interval_name": "Upper",
                "lifecycle_state": "producing",
                "lift_type": "esp",
                "integrity_risk": "watch",
            }
        )
        production = app.record_daily_production(
            {
                "well_id": "OG-7H",
                "production_date": "2026-05-29",
                "oil_bbl": 165.0,
                "gas_mcf": 800.0,
                "water_bbl": 100.0,
                "injected_water_bbl": 0.0,
                "gas_disposition": "sales",
                "oil_disposition": "sold",
                "measurement_basis": "allocated",
                "production_test_state": "allocation_approved",
                "downtime_hours": 2.0,
                "revision_reason": "separator_test_finalized",
            }
        )
        ticket = app.open_field_ticket(
            {
                "ticket_id": "FT-7",
                "well_id": "OG-7H",
                "ticket_type": "integrity",
                "severity": "high",
                "deferred_oil_bbl": 18.0,
                "root_cause": "annulus pressure increase",
                "requires_shutdown": False,
                "route_code": "ROUTE-7",
            }
        )
        workover = app.prepare_workover_readiness_pack(
            {
                "plan_id": "WO-7",
                "well_id": "OG-7H",
                "candidate_reason": "repeat annulus pressure and ESP instability",
                "expected_recovery_bopd": 55.0,
                "permit_status": "approved",
                "barrier_risk": "watch",
                "lift_failure_mode": "current_imbalance",
            }
        )
        hse = app.log_hse_event(
            {
                "event_id": "HSE-7",
                "well_id": "OG-7H",
                "event_classification": "release",
                "reportable": False,
                "spill_bbl": 0.5,
                "containment_status": "contained",
                "ignition_risk": False,
                "people_affected": 0,
            }
        )
        review = app.morning_production_review(
            {
                "route_code": "ROUTE-7",
                "minimum_deferred_oil_bbl": 5.0,
                "document_text": "Prepare ROUTE-7 morning review.",
                "instructions": "Read only.",
                "target_entity": "production_reading",
                "requested_action": "read",
            }
        )
        workbench = app.workbench({"route_code": "ROUTE-7"})
        rendered = ui.oil_gas_field_operations_render_standalone_workbench(workbench)

        assert well["ok"] is True
        assert production["record"]["status"] == "allocation_ready"
        assert ticket["record"]["workbench_queue"] == "route_attention"
        assert workover["record"]["status"] == "ready"
        assert hse["record"]["status"] == "monitoring"
        assert review["review"]["summary"]["high_priority_wells"] == 1
        assert workbench["summary"]["producing_wells"] == 1
        assert workbench["summary"]["open_field_tickets"] == 1
        assert rendered["ok"] is True
    finally:
        app.close()


def test_standalone_contract_smoke_and_docs_presence():
    contract = standalone.oil_gas_field_operations_standalone_app_contract()
    smoke = standalone.oil_gas_field_operations_standalone_app_smoke()
    docs = standalone.documentation_presence()
    evidence = release_evidence.build_release_evidence()

    assert contract["ok"] is True
    assert smoke["ok"] is True
    assert docs["ok"] is True
    assert evidence["standalone_app"]["ok"] is True
    assert evidence["standalone_smoke"]["ok"] is True


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
