from pyAppGen.pbcs.defense_readiness_logistics.agent import document_instruction_plan
from pyAppGen.pbcs.defense_readiness_logistics.defense_app import (
    assess_unit_readiness,
    build_defense_workbench,
    controls_contract,
    defense_app_smoke_test,
    empty_defense_state,
    forms_contract,
    plan_logistics_movement,
    project_maintenance_status,
    record_mission_asset,
    release_deployment_plan,
    score_supply_readiness,
    single_pbc_app_contract,
    validate_deployment_kit,
    wizards_contract,
)
from pyAppGen.pbcs.defense_readiness_logistics.services import DefenseReadinessLogisticsService


def _ready_payload():
    return {
        "unit_id": "unit-a",
        "unit_name": "Alpha",
        "mission_set": "theater_entry",
        "personnel": {
            "available": 42,
            "required": 40,
            "certified_roles": 9,
            "required_certified_roles": 8,
        },
        "serviceable_assets": 8,
        "required_assets": 6,
        "supply": {"critical_fill_rate": 0.97},
        "ammo_fill_rate": 0.92,
        "fuel_days": 4,
        "inspection_evidence": ("inspection-pack-1",),
        "commander_approved": True,
    }


def test_single_pbc_app_surfaces_forms_wizards_and_blocking_controls():
    app = single_pbc_app_contract()

    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["database_backed"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert {form["command"] for form in forms_contract()["forms"]} >= {
        "assess_unit_readiness",
        "project_maintenance_status",
        "score_supply_readiness",
        "plan_logistics_movement",
        "release_deployment_plan",
    }
    assert any(wizard["wizard_id"] == "single_pbc_launch_wizard" for wizard in wizards_contract()["wizards"])
    assert all(control["blocks_on_failure"] for control in controls_contract()["controls"])


def test_readiness_blocks_missing_people_assets_supply_fuel_ammo_and_evidence():
    state = empty_defense_state()
    result = assess_unit_readiness(
        state,
        {
            "unit_id": "unit-blocked",
            "personnel": {"available": 3, "required": 10, "certified_roles": 1, "required_certified_roles": 3},
            "serviceable_assets": 0,
            "required_assets": 2,
            "supply": {"critical_fill_rate": 0.25},
            "ammo_fill_rate": 0.1,
            "fuel_days": 0,
        },
    )

    readiness = result["unit_readiness"]
    assert readiness["validated_status"] == "degraded"
    assert set(readiness["blockers"]) >= {
        "personnel_shortfall",
        "certification_shortfall",
        "asset_outage",
        "supply_deficit",
        "ammo_deficit",
        "fuel_deficit",
        "inspection_evidence_missing",
    }
    assert result["state"]["outbox"][-1]["event_contract"] == "AppGen-X"


def test_maintenance_supply_kit_movement_and_release_flow():
    state = empty_defense_state()
    ready = assess_unit_readiness(state, _ready_payload())
    asset = record_mission_asset(
        ready["state"],
        {"asset_id": "veh-1", "unit_id": "unit-a", "asset_type": "vehicle", "serial": "SER-1", "serviceability": "serviceable"},
    )
    maintenance = project_maintenance_status(
        asset["state"],
        {
            "asset_id": "veh-1",
            "fault_codes": ("PMCS",),
            "required_parts": ("filter",),
            "available_parts": ("filter",),
            "projected_return": "D+0",
            "confidence": 0.91,
            "restored": True,
        },
    )
    supply = score_supply_readiness(
        maintenance["state"],
        {
            "unit_id": "unit-a",
            "mission_set": "theater_entry",
            "demand": {"class_ix": 10, "medical": 4},
            "on_hand": {"class_ix": 10, "medical": 4},
            "fuel_required": 100,
            "fuel_available": 120,
        },
    )
    kit = validate_deployment_kit(
        supply["state"],
        {
            "kit_id": "kit-a",
            "required_items": ("medical", "comms", "tools"),
            "packed_items": ("medical", "comms", "tools"),
            "mission_critical_items": ("medical", "comms"),
        },
    )
    movement = plan_logistics_movement(
        kit["state"],
        {
            "movement_id": "move-a",
            "deployment_id": "dep-a",
            "mode": "convoy",
            "route_reviewed": True,
            "load_plan": {"segregation_checked": True},
            "fuel_required": 80,
            "fuel_available": 100,
            "asset_ids": ("veh-1",),
            "window": "D1",
            "commander_approved": True,
        },
    )
    released = release_deployment_plan(
        movement["state"],
        {"deployment_id": "dep-a", "unit_id": "unit-a", "kit_id": "kit-a", "movement_id": "move-a"},
    )

    assert maintenance["ok"] is True
    assert supply["ok"] is True
    assert kit["ok"] is True
    assert movement["ok"] is True
    assert released["ok"] is True
    assert released["deployment_plan"]["status"] == "released"
    assert build_defense_workbench(released["state"])["queue_counts"]["commander_readiness_board"] == 0


def test_release_blocks_until_readiness_kit_and_movement_are_valid():
    blocked = release_deployment_plan(empty_defense_state(), {"deployment_id": "dep-blocked"})

    assert blocked["ok"] is False
    assert set(blocked["deployment_plan"]["blockers"]) == {
        "unit_not_deployment_ready",
        "deployment_kit_not_complete",
        "movement_not_released",
    }


def test_movement_controls_mode_specific_and_double_booking_rules():
    state = empty_defense_state()
    first = plan_logistics_movement(
        state,
        {"movement_id": "move-1", "mode": "convoy", "route_reviewed": True, "asset_ids": ("veh-1",), "window": "D1", "commander_approved": True},
    )
    second = plan_logistics_movement(
        first["state"],
        {"movement_id": "move-2", "mode": "airlift", "weight": 120, "aircraft_weight_limit": 100, "asset_ids": ("veh-1",), "window": "D1"},
    )

    assert first["ok"] is True
    assert second["ok"] is False
    assert set(second["logistics_movement"]["blockers"]) >= {
        "aircraft_weight_limit_exceeded",
        "asset_double_booked",
    }


def test_agent_document_plan_is_stable_and_domain_routed():
    first = document_instruction_plan("convoy order 17", "create movement order")
    second = document_instruction_plan("convoy order 17", "create movement order")
    shortage = document_instruction_plan("fuel shortage memo", "create shortage mitigation")

    assert first["document_digest"] == second["document_digest"]
    assert first["domain_plan"]["target_table"] == "defense_readiness_logistics_logistics_movement"
    assert shortage["domain_plan"]["proposed_operation"] == "score_supply_readiness"
    assert first["requires_human_confirmation"] is True


def test_stateful_service_executes_single_pbc_domain_commands():
    service = DefenseReadinessLogisticsService()
    readiness = service.assess_unit_readiness(_ready_payload())
    asset = service.record_mission_asset({"asset_id": "veh-svc", "unit_id": "unit-a", "serviceability": "serviceable"})
    workbench = service.build_defense_workbench({})

    assert readiness["ok"] is True
    assert asset["ok"] is True
    assert workbench["ok"] is True
    assert "unit-a" in service.state["units"]
    assert "veh-svc" in service.state["assets"]


def test_defense_app_smoke_covers_end_to_end_release():
    assert defense_app_smoke_test()["ok"] is True
