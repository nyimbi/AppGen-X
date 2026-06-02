"""Focused standalone tests for Mining Operations Management."""

from pathlib import Path

from pyAppGen.pbcs.mining_operations_management import controls
from pyAppGen.pbcs.mining_operations_management import forms
from pyAppGen.pbcs.mining_operations_management import release_evidence
from pyAppGen.pbcs.mining_operations_management import routes
from pyAppGen.pbcs.mining_operations_management import standalone
from pyAppGen.pbcs.mining_operations_management import ui
from pyAppGen.pbcs.mining_operations_management import wizards


def test_standalone_app_executes_shift_workflow():
    app = standalone.MiningOperationsManagementStandaloneApp()
    registered = app.register_defaults()
    assert registered["ok"] is True

    plan = app.submit_form(
        "mine_plan_hierarchy_intake",
        {
            "tenant": "tenant_test",
            "plan_id": "plan_test",
            "plan_period": "2026-W22",
            "mining_method": "open_pit",
            "pit_phase": "Phase-2",
            "bench_or_stope": "Bench-4505",
            "planned_tonnes": 180000,
            "planned_grade": 1.72,
            "ore_destination": "crusher",
        },
    )
    fleet = app.submit_form(
        "fleet_capability_card",
        {
            "tenant": "tenant_test",
            "fleet_asset_id": "truck_test",
            "equipment_class": "truck",
            "payload_band": "220t",
            "approved_areas": ("PB-05", "PB-06"),
            "availability_state": "available",
            "fuel_type": "diesel",
        },
    )
    blast = app.submit_form(
        "blast_readiness_packet",
        {
            "tenant": "tenant_test",
            "blast_packet_id": "blast_test",
            "plan_id": "plan_test",
            "pit_location_id": "PB-05-Bench-4505",
            "hole_count": 42,
            "powder_factor": 0.84,
            "clearance_confirmed": True,
            "re_entry_status": "released",
            "geotech_risk": "medium",
        },
    )
    shift = app.submit_form(
        "shift_target_board",
        {
            "tenant": "tenant_test",
            "shift_id": "shift_day_test",
            "plan_id": "plan_test",
            "shift_name": "day",
            "target_ore_tonnes": 24000,
            "target_waste_tonnes": 18000,
            "target_truck_loads": 126,
            "critical_constraint": "crusher_queue",
        },
    )
    dispatch = app.submit_form(
        "dispatch_assignment",
        {
            "tenant": "tenant_test",
            "dispatch_id": "dispatch_test",
            "shift_id": "shift_day_test",
            "fleet_asset_id": "truck_test",
            "mining_area": "PB-05",
            "route_status": "open",
            "material_destination": "crusher",
            "queue_length": 3,
        },
    )
    boundary = app.submit_form(
        "ore_boundary_decision",
        {
            "tenant": "tenant_test",
            "boundary_decision_id": "boundary_test",
            "dig_block_id": "DB-77",
            "grade_band": "1.5-1.8g/t",
            "destination_changed": True,
            "approved_by": "ore_control_supervisor",
            "assay_reference": "ASSAY-22",
        },
    )
    stockpile = app.submit_form(
        "stockpile_movement",
        {
            "tenant": "tenant_test",
            "movement_id": "movement_test",
            "stockpile_id": "SP-1",
            "movement_type": "build",
            "tonnes_delta": 8500,
            "estimated_grade": 1.61,
            "source_reference": "DB-77",
        },
    )
    geotech = app.submit_form(
        "geotech_conditional_access",
        {
            "tenant": "tenant_test",
            "access_id": "access_test",
            "area_id": "PB-05",
            "access_state": "conditional",
            "allowed_equipment": ("truck", "loader"),
            "monitoring_source": "radar",
            "review_due_shift": "night",
        },
    )
    handover = app.submit_form(
        "shift_handover_note",
        {
            "tenant": "tenant_test",
            "handover_id": "handover_test",
            "shift_id": "shift_day_test",
            "delay_code": "crusher_queue",
            "open_issues": ("crusher_queue", "ore_pass_watch"),
            "plant_feed_risk": "medium",
            "status": "open",
        },
    )

    workbench = app.build_workbench("tenant_test")
    control_center = app.control_center()
    rendered = ui.mining_operations_management_render_standalone_workbench(workbench)

    assert all(
        item["ok"] is True
        for item in (plan, fleet, blast, shift, dispatch, boundary, stockpile, geotech, handover)
    )
    assert workbench["plan_count"] == 1
    assert workbench["dispatch_assignment_count"] == 1
    assert workbench["stockpile_tonnes_delta"] == 8500.0
    assert control_center["dispatch_boundary"]["violations"] == ()
    assert control_center["ore_boundary"]["unapproved_destination_changes"] == ()
    assert rendered["ok"] is True
    assert rendered["cards"]


def test_routes_wizards_controls_and_release_evidence_are_wired():
    app = standalone.MiningOperationsManagementStandaloneApp()
    app.register_defaults()

    create = routes.dispatch_standalone_route(
        "POST",
        "/app/mining-operations-management/forms/mine-plan-hierarchy-intake",
        {
            "tenant": "tenant_route",
            "plan_id": "plan_route",
            "plan_period": "2026-W23",
            "mining_method": "open_pit",
            "pit_phase": "Phase-3",
            "bench_or_stope": "Bench-4510",
            "planned_tonnes": 120000,
            "planned_grade": 1.44,
            "ore_destination": "stockpile",
        },
        app=app,
    )
    wizard = routes.dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/wizards/weekly-plan-to-shift",
        {"plan_id": "plan_route"},
        app=app,
    )
    workbench = routes.dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/workbench",
        {"tenant": "tenant_route"},
        app=app,
    )
    controls_view = routes.dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/controls",
        app=app,
    )
    release = routes.dispatch_standalone_route(
        "GET",
        "/app/mining-operations-management/release-evidence",
        app=app,
    )
    package_release = release_evidence.build_release_evidence()
    standalone_smoke = standalone.mining_operations_management_standalone_smoke()

    assert create["ok"] is True
    assert wizard["ok"] is True
    assert workbench["ok"] is True
    assert controls_view["ok"] is True
    assert release["ok"] is True
    assert forms.mining_operations_management_form_catalog()["ok"] is True
    assert wizards.mining_operations_management_wizard_catalog()["ok"] is True
    assert controls.mining_operations_management_control_catalog()["ok"] is True
    assert package_release["standalone_app"]["ok"] is True
    assert package_release["documentation"]["ok"] is True
    assert standalone_smoke["ok"] is True


def test_package_local_docs_exist_for_release_evidence():
    base = Path(__file__).resolve().parent.parent
    for name in ("SPECIFICATION.md", "improve1.md", "implementation-plan.md", "RELEASE_EVIDENCE.md"):
        assert (base / name).exists() is True
