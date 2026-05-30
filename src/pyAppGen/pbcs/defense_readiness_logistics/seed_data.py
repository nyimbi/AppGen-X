"""Seed data for defense_readiness_logistics standalone smoke scenarios."""

from __future__ import annotations

from .defense_app import (
    allocate_fuel_reserve,
    empty_defense_state,
    record_mission_asset,
    run_readiness_validation_workflow,
    score_supply_readiness,
    validate_deployment_kit,
)
from .models import PBC_KEY


def seed_plan() -> dict:
    state = empty_defense_state()
    readiness = run_readiness_validation_workflow(
        state,
        {
            "qualification": {
                "tenant_id": "seed-tenant",
                "unit_code": "seed-alpha",
                "role_code": "vehicle-crew",
                "certified_count": 6,
                "required_count": 5,
                "available_count": 6,
            },
            "inspection": {
                "tenant_id": "seed-tenant",
                "unit_code": "seed-alpha",
                "evidence_items": ("checklist", "signature"),
                "signatures": ("inspector",),
            },
            "readiness": {
                "tenant_id": "seed-tenant",
                "unit_id": "seed-unit-alpha",
                "unit_code": "seed-alpha",
                "unit_name": "Seed Alpha",
                "mission_set": "relief_entry",
                "personnel": {"available": 18, "required": 16, "certified_roles": 5, "required_certified_roles": 4},
                "serviceable_assets": 4,
                "required_assets": 3,
                "supply": {"critical_fill_rate": 0.93},
                "ammo_fill_rate": 0.85,
                "fuel_days": 2,
                "inspection_evidence": ("seed-pack",),
                "commander_approved": True,
            },
        },
    )
    asset = record_mission_asset(
        readiness["state"],
        {"tenant_id": "seed-tenant", "asset_id": "seed-veh-1", "unit_code": "seed-alpha", "asset_code": "seed-veh-1", "asset_type": "vehicle", "serviceability": "serviceable"},
    )
    supply = score_supply_readiness(
        asset["state"],
        {
            "tenant_id": "seed-tenant",
            "unit_code": "seed-alpha",
            "mission_set": "relief_entry",
            "demand": {"repair_parts": 5, "medical": 2},
            "on_hand": {"repair_parts": 5, "medical": 2},
            "fuel_required": 50,
            "fuel_available": 60,
        },
    )
    fuel = allocate_fuel_reserve(
        supply["state"],
        {"tenant_id": "seed-tenant", "unit_code": "seed-alpha", "fuel_required": 50, "fuel_available": 70, "contingency_reserve": 10},
    )
    kit = validate_deployment_kit(
        fuel["state"],
        {
            "tenant_id": "seed-tenant",
            "unit_code": "seed-alpha",
            "kit_id": "seed-kit-1",
            "required_items": ("medical", "comms"),
            "packed_items": ("medical", "comms"),
            "mission_critical_items": ("medical", "comms"),
        },
    )
    return {
        "ok": all((readiness["ok"], asset["ok"], supply["ok"], fuel["ok"], kit["ok"])),
        "pbc": PBC_KEY,
        "records": (
            {"table": readiness["unit_readiness"]["table"], "code": readiness["unit_readiness"]["unit_code"]},
            {"table": asset["mission_asset"]["table"], "code": asset["mission_asset"]["asset_code"]},
            {"table": supply["supply_readiness"]["table"], "code": supply["supply_readiness"]["id"]},
            {"table": fuel["fuel_allocation"]["table"], "code": fuel["fuel_allocation"]["allocation_code"]},
            {"table": kit["deployment_kit"]["table"], "code": kit["deployment_kit"]["deployment_code"]},
        ),
        "side_effects": (),
    }


def validate_seed_data() -> dict:
    plan = seed_plan()
    invalid_tables = tuple(record for record in plan["records"] if not record["table"].startswith(f"{PBC_KEY}_"))
    return {"ok": plan["ok"] and not invalid_tables, "pbc": PBC_KEY, "invalid_tables": invalid_tables, "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": seed_plan()["ok"] and validate_seed_data()["ok"], "side_effects": ()}
